"""
Kiyomi Router - Routes to Gemini (cheap) or Claude CLI (powerful).
Also handles image generation via Gemini.
"""
import asyncio
import json
import logging
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple, Callable, List

from config import (
    GEMINI_API_KEY, CLAUDE_CLI_PATH, APPS_DIR, ENABLE_CHROME,
    BASE_DIR, WORKSPACE_DIR, IDENTITY_FILE, USER_FILE,
)
from context import (
    build_prompt, add_to_history, _load_history, _read,
    get_active_project, set_active_project, PROJECTS_FILE,
)

logger = logging.getLogger(__name__)

# Track current Claude process for /cancel
_current_process: Optional[asyncio.subprocess.Process] = None
_current_description: Optional[str] = None

# Track last Claude conversation for --continue
_last_claude_cwd: Optional[str] = None


# ── routing decision ──────────────────────────────────────────

# Keywords that need Claude's power
_CLAUDE_KEYWORDS = re.compile(
    r"\b("
    r"file|deploy|git|code|build|fix|browse|commit|push|pull|merge|"
    r"refactor|debug|install|update|create|write|edit|delete|move|rename|"
    r"run|execute|test|check|verify|launch|open|project|vercel|"
    r"remember|remind|schedule|monitor|heartbeat|"
    r"true.?podcasts?|jw.?companion|nano.?banana|yt.?automation|"
    r"premier.?intelligence|health.?quest|kiyomi|portfolio|"
    r"swift|xcode|python|next\.?js|react|node"
    r")\b",
    re.IGNORECASE,
)

_URL_PATTERN = re.compile(r"https?://|www\.|\.com|\.app|\.dev|\.io")
_PATH_PATTERN = re.compile(r"[~/][\w/.-]+\.\w+|~/\w+")


_CONTINUE_PATTERNS = re.compile(
    r"^(keep going|continue|go on|carry on|what else|more|finish it|"
    r"keep at it|don't stop|and\?|next|proceed)$",
    re.IGNORECASE,
)


def should_use_claude(message: str) -> bool:
    """Return True if the message needs Claude CLI, False for Gemini."""
    if is_continue_message(message):
        return True
    if _CLAUDE_KEYWORDS.search(message):
        return True
    if _URL_PATTERN.search(message):
        return True
    if _PATH_PATTERN.search(message):
        return True
    # If message is long (likely a complex request), use Claude
    if len(message) > 300:
        return True
    return False


def is_continue_message(message: str) -> bool:
    """Return True if message is a 'keep going' type continuation."""
    return bool(_CONTINUE_PATTERNS.match(message.strip()))


# ── smart routing (Gemini pre-classify) ──────────────────────

async def smart_classify(message: str) -> bool:
    """Use Gemini to classify if message needs tools/Claude. Fallback for ambiguous messages."""
    if not GEMINI_API_KEY:
        return False
    try:
        from google import genai
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=(
                "Does this user message require any of: file system access, code editing, "
                "web browsing, git operations, deployment, running commands, or any computer tools?\n"
                "Reply with ONLY the word 'YES' or 'NO'.\n\n"
                f"Message: {message}"
            ),
        )
        answer = response.text.strip().upper() if response.text else ""
        needs_tools = "YES" in answer
        logger.debug(f"Smart classify '{message[:50]}' → {'Claude' if needs_tools else 'Gemini'}")
        return needs_tools
    except Exception as e:
        logger.debug(f"Smart classify error: {e}")
        return False


async def should_use_claude_smart(message: str) -> bool:
    """Async smart routing: keyword match first, Gemini classify as fallback."""
    # Fast path: keyword/pattern match
    if should_use_claude(message):
        return True
    # Ambiguous — ask Gemini to classify
    return await smart_classify(message)


# ── project context detection ────────────────────────────────

def _resolve_project_path(path: str) -> str:
    """Resolve $APPS_DIR and ~ in project paths."""
    if "$APPS_DIR" in path:
        path = path.replace("$APPS_DIR", str(APPS_DIR))
    return os.path.expanduser(path)


def detect_project_context(message: str) -> Optional[dict]:
    """Check if message mentions a known project. Returns project dict with resolved path."""
    try:
        if not PROJECTS_FILE.exists():
            return None
        with open(PROJECTS_FILE) as f:
            projects = json.load(f)
        msg_lower = message.lower()
        for pid, proj in projects.items():
            matched = False
            if proj["name"].lower() in msg_lower:
                matched = True
            else:
                for alias in proj.get("aliases", []):
                    if alias.lower() in msg_lower:
                        matched = True
                        break
            if matched:
                proj["path"] = _resolve_project_path(proj.get("path", ""))
                return proj
        return None
    except Exception:
        return None


# ── task chain detection ─────────────────────────────────────

_CHAIN_SPLIT = re.compile(
    r",?\s+(?:then|and then|after that|next)\s+",
    re.IGNORECASE,
)

# "and" only chains when followed by an action verb
_ACTION_CHAIN = re.compile(
    r",?\s+and\s+(?=(?:deploy|commit|push|fix|build|run|test|check|create|"
    r"update|install|delete|move|rename|open|launch|verify|restart))",
    re.IGNORECASE,
)


def detect_task_chain(message: str) -> List[str]:
    """Split a multi-step request into individual tasks."""
    # Try explicit chain words first
    if _CHAIN_SPLIT.search(message):
        steps = _CHAIN_SPLIT.split(message)
        steps = [s.strip() for s in steps if s.strip() and len(s.strip()) > 3]
        if len(steps) > 1:
            return steps

    # Try action-verb "and" chains
    if _ACTION_CHAIN.search(message):
        steps = _ACTION_CHAIN.split(message)
        steps = [s.strip() for s in steps if s.strip() and len(s.strip()) > 3]
        if len(steps) > 1:
            return steps

    return [message]


# ── post-deploy verification ─────────────────────────────────

async def verify_deploy(url: str) -> str:
    """HTTP GET a URL and check if it's live."""
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status == 200:
                    return f"✅ Verified live: {url} (200 OK)"
                else:
                    return f"⚠️ Deploy check: {url} returned {resp.status}"
    except Exception as e:
        return f"❌ Could not verify {url}: {e}"


# ── image detection ───────────────────────────────────────────

_IMAGE_PATTERNS = re.compile(
    r"^/image\b|generate\s+(an?\s+)?image|draw\s+(me\s+)?|create\s+(an?\s+)?image|"
    r"make\s+(me\s+)?(an?\s+)?image|picture\s+of",
    re.IGNORECASE,
)


def is_image_request(message: str) -> bool:
    return bool(_IMAGE_PATTERNS.search(message))


# ── Gemini route ──────────────────────────────────────────────

async def route_to_gemini(message: str) -> Tuple[str, bool]:
    """Send to Gemini 2.0 Flash for cheap/fast responses."""
    if not GEMINI_API_KEY:
        logger.warning("No Gemini API key, falling back to Claude")
        return await route_to_claude(message)

    try:
        from google import genai

        client = genai.Client(api_key=GEMINI_API_KEY)

        # Build lightweight context
        identity = _read(IDENTITY_FILE) or ""
        user_prefs = _read(USER_FILE) or ""

        # Last 3 history entries
        history = _load_history()
        history_text = ""
        for msg in history[-3:]:
            role = "Richard" if msg["role"] == "user" else "Kiyomi"
            history_text += f"{role}: {msg['content'][:200]}\n"

        system_ctx = (
            f"{identity}\n\n"
            f"You are Kiyomi, Richard's AI assistant. Be direct, concise, helpful.\n"
            f"{user_prefs[:500]}\n\n"
            f"Recent chat:\n{history_text}"
        )

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"{system_ctx}\n\nRichard: {message}",
        )

        result = response.text.strip() if response.text else ""
        if not result:
            logger.warning("Empty Gemini response, falling back to Claude")
            return await route_to_claude(message)

        return result, True

    except Exception as e:
        logger.error(f"Gemini error: {e}, falling back to Claude")
        return await route_to_claude(message)


# ── progress parsing ──────────────────────────────────────────

def _parse_progress(line: str) -> Optional[str]:
    """Parse a line of Claude CLI output for progress indicators."""
    line = line.strip()
    if not line:
        return None
    if "Reading" in line or "Read " in line:
        m = re.search(r'(?:Reading|Read)\s+[`"]?([^`"\n]+)[`"]?', line)
        if m:
            return f"📖 Reading {m.group(1).split('/')[-1]}"
    if "Writing" in line or "Wrote " in line or "Created " in line:
        m = re.search(r'(?:Writing|Wrote|Created)\s+[`"]?([^`"\n]+)[`"]?', line)
        if m:
            return f"✍️ Writing {m.group(1).split('/')[-1]}"
    if "Editing" in line or "Edit " in line:
        m = re.search(r'(?:Editing|Edit)\s+[`"]?([^`"\n]+)[`"]?', line)
        if m:
            return f"✏️ Editing {m.group(1).split('/')[-1]}"
    if line.startswith("$ ") or line.startswith("> "):
        return f"⚡ {line[:60]}"
    if "npm " in line.lower():
        if "install" in line.lower():
            return "📦 Installing packages..."
        if "build" in line.lower():
            return "🔨 Building..."
    if "vercel" in line.lower():
        return "🚀 Deploying to Vercel..."
    if "git " in line.lower():
        if "commit" in line.lower():
            return "📝 Committing..."
        if "push" in line.lower():
            return "⬆️ Pushing..."
    if "error" in line.lower():
        return f"⚠️ {line[:60]}"
    return None


# ── Claude CLI route ──────────────────────────────────────────

async def route_to_claude(
    message: str,
    working_dir: Optional[str] = None,
    progress_callback: Optional[Callable] = None,
) -> Tuple[str, bool]:
    """Send to Claude CLI with full context. Streams progress via callback."""
    global _current_process, _current_description, _last_claude_cwd

    use_continue = is_continue_message(message) and _last_claude_cwd is not None

    if working_dir is None:
        working_dir = _last_claude_cwd if use_continue else APPS_DIR

    try:
        if use_continue:
            cli_args = [
                CLAUDE_CLI_PATH, "--continue", "-p", message,
                "--dangerously-skip-permissions",
            ]
        else:
            full_prompt = build_prompt(message)
            cli_args = [
                CLAUDE_CLI_PATH, "-p", full_prompt,
                "--dangerously-skip-permissions",
            ]
        if ENABLE_CHROME:
            cli_args.append("--chrome")

        process = await asyncio.create_subprocess_exec(
            *cli_args,
            cwd=working_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        _current_process = process
        _current_description = message[:100]

        # Stream stdout line-by-line for progress
        output_lines: List[str] = []
        last_progress = ""
        last_progress_time = datetime.now()

        try:
            while True:
                total_elapsed = (datetime.now() - last_progress_time).total_seconds()

                try:
                    line = await asyncio.wait_for(
                        process.stdout.readline(), timeout=5
                    )
                except asyncio.TimeoutError:
                    if process.returncode is not None:
                        break
                    # Check total timeout
                    if (datetime.now() - last_progress_time).total_seconds() > 1800:
                        raise asyncio.TimeoutError()
                    continue

                if not line:
                    break

                line_text = line.decode("utf-8", errors="replace")
                output_lines.append(line_text)
                last_progress_time = datetime.now()

                # Send progress updates (debounced to 5s gap)
                if progress_callback:
                    progress = _parse_progress(line_text)
                    if progress and progress != last_progress:
                        elapsed = (datetime.now() - last_progress_time).total_seconds()
                        await progress_callback(progress)
                        last_progress = progress

            await asyncio.wait_for(process.wait(), timeout=30)
            stderr_data = await process.stderr.read()
            error = stderr_data.decode("utf-8", errors="replace").strip()

        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            _current_process = None
            _current_description = None
            return "Task timed out after 30 minutes.", False

        _current_process = None
        _current_description = None
        _last_claude_cwd = working_dir  # remember for --continue

        output = "".join(output_lines).strip()

        if process.returncode != 0 and error:
            logger.error(f"Claude CLI error: {error[:500]}")
            return f"Error: {error[:1000]}", False

        result = output if output else "Done (no output)"

        if len(result) > 50000:
            result = result[:50000] + "\n\n... (truncated)"

        return result, True

    except FileNotFoundError as e:
        logger.error(f"FileNotFoundError in Claude route: {e} (cli={CLAUDE_CLI_PATH}, cwd={working_dir})")
        if working_dir and not Path(working_dir).is_dir():
            return f"Working directory not found: {working_dir}", False
        return "Claude Code CLI not found. Make sure it's installed.", False
    except Exception as e:
        logger.exception(f"Error executing Claude: {e}")
        return f"Error: {e}", False


# ── image generation ──────────────────────────────────────────

async def generate_image(prompt: str) -> Tuple[Optional[Path], str]:
    """Generate an image via Gemini. Returns (file_path, message)."""
    if not GEMINI_API_KEY:
        return None, "No Gemini API key configured."

    try:
        from google import genai
        from PIL import Image
        import io

        client = genai.Client(api_key=GEMINI_API_KEY)

        # Strip /image prefix if present
        clean_prompt = re.sub(r"^/image\s*", "", prompt).strip()
        if not clean_prompt:
            return None, "Please provide an image description."

        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=clean_prompt,
            config=genai.types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            ),
        )

        # Extract image from response
        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                img = Image.open(io.BytesIO(part.inline_data.data))
                temp_dir = BASE_DIR / "temp"
                temp_dir.mkdir(exist_ok=True)
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                filepath = temp_dir / f"gemini_{ts}.png"
                img.save(filepath)
                return filepath, "Image generated"

        return None, "Gemini returned no image data."

    except Exception as e:
        logger.error(f"Image generation error: {e}")
        return None, f"Image generation failed: {e}"


# ── audio transcription ───────────────────────────────────────

async def transcribe_audio(audio_path: str) -> Tuple[str, bool]:
    """Transcribe an audio file using Gemini. Returns (transcript, success)."""
    if not GEMINI_API_KEY:
        return "No Gemini API key for transcription.", False

    try:
        from google import genai

        client = genai.Client(api_key=GEMINI_API_KEY)

        # Upload the audio file
        audio_file = client.files.upload(file=audio_path)

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                "Transcribe this audio message exactly. "
                "Return ONLY the transcription, nothing else. "
                "If there are multiple speakers, note who is speaking.",
                audio_file,
            ],
        )

        transcript = response.text.strip() if response.text else ""
        if not transcript:
            return "Could not transcribe audio — no speech detected.", False

        return transcript, True

    except Exception as e:
        logger.error(f"Transcription error: {e}")
        return f"Transcription failed: {e}", False


# ── cancel ────────────────────────────────────────────────────

async def cancel_current() -> Tuple[bool, str]:
    """Kill the running Claude process."""
    global _current_process, _current_description
    if _current_process is None:
        return False, "No task currently running."
    desc = _current_description or "Unknown task"
    try:
        _current_process.kill()
        await _current_process.wait()
        _current_process = None
        _current_description = None
        return True, f"Cancelled: {desc}"
    except Exception as e:
        return False, f"Error cancelling: {e}"
