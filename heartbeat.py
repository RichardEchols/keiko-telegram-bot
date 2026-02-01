"""
Kiyomi Heartbeat System - Scheduled task execution
"""
import asyncio
import logging
import os
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import pytz

from config import (
    TIMEZONE, HEARTBEAT_INTERVAL_MINUTES,
    MORNING_BRIEF_HOUR, MORNING_BRIEF_MINUTE,
    QUIET_HOURS_START, QUIET_HOURS_END,
    BOT_EMOJI, BOT_NAME, OWNER_NAME,
    OWNER_CITY, MORNING_BRIEF_SECTIONS, CUSTOM_BRIEF_SECTIONS,
    BASE_DIR, MEMORY_DIR, GEMINI_API_KEY
)
from memory_manager import (
    read_heartbeat, update_heartbeat, log_to_today,
    get_today_date
)
from executor import execute_claude
from proactive import (
    is_prep_time, do_silent_prep, is_session_idle,
    do_session_summary, is_factory_mode, run_factory_mode,
    do_rotation_check
)
from automations import AutomationEngine

logger = logging.getLogger(__name__)

# Lazy-initialized automation engine
_automation_engine = None

def _get_automation_engine():
    global _automation_engine
    if _automation_engine is None:
        _automation_engine = AutomationEngine()
    return _automation_engine

# Track last message time from Richard
_last_richard_message_time: Optional[datetime] = None
_last_heartbeat_time: Optional[datetime] = None


def update_last_message_time():
    """Update the last time Richard sent a message."""
    global _last_richard_message_time
    _last_richard_message_time = datetime.now(pytz.timezone(TIMEZONE))


def is_richard_active(minutes: int = 5) -> bool:
    """Check if Richard sent a message recently."""
    if _last_richard_message_time is None:
        return False

    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)
    threshold = now - timedelta(minutes=minutes)
    return _last_richard_message_time > threshold


def is_quiet_hours() -> bool:
    """Check if it's during quiet hours (night time)."""
    tz = pytz.timezone(TIMEZONE)
    current_hour = datetime.now(tz).hour

    if QUIET_HOURS_START > QUIET_HOURS_END:
        # Quiet hours span midnight (e.g., 23:00 to 08:00)
        return current_hour >= QUIET_HOURS_START or current_hour < QUIET_HOURS_END
    else:
        return QUIET_HOURS_START <= current_hour < QUIET_HOURS_END


# Persist morning brief state to survive restarts
from pathlib import Path
MORNING_BRIEF_STATE_FILE = Path(__file__).parent / "workspace" / ".morning_brief_date"

def _get_morning_brief_sent_date() -> Optional[str]:
    """Get the date of last morning brief from file."""
    try:
        if MORNING_BRIEF_STATE_FILE.exists():
            return MORNING_BRIEF_STATE_FILE.read_text().strip()
    except:
        pass
    return None

def is_morning_brief_time() -> bool:
    """Check if it's time for the morning brief.

    Returns True if:
    - It's between 8:30 AM and 9:30 AM (buffer for missed windows)
    - We haven't sent a brief today yet
    """
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)
    today = now.strftime("%Y-%m-%d")

    # Already sent today?
    if _get_morning_brief_sent_date() == today:
        return False

    # Check if we're in the morning brief window (8:30-9:30)
    if now.hour == MORNING_BRIEF_HOUR and now.minute >= MORNING_BRIEF_MINUTE:
        return True
    if now.hour == MORNING_BRIEF_HOUR + 1 and now.minute < 30:
        return True

    return False


def mark_morning_brief_sent():
    """Mark that we've sent the morning brief today (persisted to file)."""
    try:
        tz = pytz.timezone(TIMEZONE)
        today = datetime.now(tz).strftime("%Y-%m-%d")
        MORNING_BRIEF_STATE_FILE.write_text(today)
    except Exception as e:
        logger.error(f"Failed to save morning brief state: {e}")


def parse_heartbeat_tasks(content: str) -> List[Dict]:
    """Parse HEARTBEAT.md to extract pending tasks."""
    tasks = []
    if not content:
        return tasks

    # Find pending tasks section
    pending_section = re.search(
        r'##\s*Pending\s*Tasks\s*\n(.*?)(?=\n##|$)',
        content,
        re.DOTALL | re.IGNORECASE
    )

    if not pending_section:
        return tasks

    # Extract uncompleted tasks (lines starting with - [ ])
    task_pattern = re.compile(r'-\s*\[\s*\]\s*(.+)')
    for match in task_pattern.finditer(pending_section.group(1)):
        tasks.append({
            "description": match.group(1).strip(),
            "completed": False
        })

    return tasks


def mark_task_completed(content: str, task_description: str) -> str:
    """Mark a task as completed in the heartbeat content."""
    # Replace the uncompleted task with completed version
    pattern = re.escape(f"- [ ] {task_description}")
    replacement = f"- [x] {task_description}"
    return re.sub(pattern, replacement, content)


async def run_heartbeat(send_message_callback) -> None:
    """
    Run a heartbeat check.

    Args:
        send_message_callback: Async function to send Telegram messages
    """
    global _last_heartbeat_time

    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)

    logger.info(f"Heartbeat running at {now.strftime('%H:%M')}")

    # 1. Check for 8:00 AM silent prep time
    if is_prep_time():
        logger.info("Running 8:00 AM silent prep...")
        prep_result = await do_silent_prep()
        if prep_result["status"] == "completed":
            logger.info(f"Silent prep done: {len(prep_result.get('files_read', []))} files read")
            log_to_today(f"Silent prep completed - {prep_result.get('pending_tasks', 0)} pending tasks")
        # Don't return - continue to other checks

    # 2. Check for session idle summary
    if is_session_idle() and not is_quiet_hours():
        logger.info("Session idle - generating summary")
        await do_session_summary(send_message_callback)

    # 3. Skip regular heartbeat if Richard is actively chatting
    if is_richard_active(minutes=5):
        logger.info("Skipping heartbeat - Richard is active")
        return

    # 4. Check for morning brief time
    if is_morning_brief_time():
        await send_morning_brief(send_message_callback)
        mark_morning_brief_sent()
        _last_heartbeat_time = now
        return

    # 5. Run factory mode if enabled (overnight autonomous work)
    if is_factory_mode() and is_quiet_hours():
        logger.info("Running factory mode tasks...")
        completed = await run_factory_mode(execute_claude, send_message_callback)
        if completed:
            log_to_today(f"Factory mode completed {len(completed)} tasks: {', '.join(completed[:3])}")
        _last_heartbeat_time = now
        return

    # 6. Skip detailed checks during quiet hours (unless factory mode)
    if is_quiet_hours():
        logger.info("Quiet hours - minimal heartbeat")
        return

    # 7. Run rotation check (commitments, weather, etc.)
    rotation_msg = await do_rotation_check(send_message_callback)
    if rotation_msg:
        await send_message_callback(rotation_msg)

    # 8. Check automation triggers
    try:
        engine = _get_automation_engine()
        triggered = engine.check_triggers()
        for auto in triggered:
            result = await engine.execute_automation(auto, {})
            if result and send_message_callback:
                await send_message_callback(f"🤖 Automation: {result}")
            logger.info(f"Automation triggered: {auto.name}")
    except Exception as e:
        logger.error(f"Automation check failed: {e}")

    # 9. Read heartbeat file for pending tasks
    heartbeat_content = read_heartbeat()
    tasks = parse_heartbeat_tasks(heartbeat_content)

    if not tasks:
        logger.info("No pending tasks in heartbeat")
        _last_heartbeat_time = now
        return

    # Execute up to 2 pending tasks
    tasks_executed = 0
    for task in tasks[:2]:
        if task["completed"]:
            continue

        logger.info(f"Executing heartbeat task: {task['description'][:50]}...")

        try:
            result, success = await execute_claude(task["description"])

            if success:
                # Mark task as completed
                heartbeat_content = mark_task_completed(
                    heartbeat_content,
                    task["description"]
                )
                update_heartbeat(heartbeat_content)

                # Log to daily memory
                log_to_today(f"Heartbeat completed: {task['description'][:100]}")

                tasks_executed += 1
        except Exception as e:
            logger.error(f"Error executing heartbeat task: {e}")

    # Notify Richard if tasks were completed (outside quiet hours)
    if tasks_executed > 0 and not is_quiet_hours():
        await send_message_callback(
            f"{BOT_EMOJI} Completed {tasks_executed} background task(s)"
        )

    _last_heartbeat_time = now


def _build_morning_brief_prompt() -> str:
    """Build the morning brief prompt dynamically from config."""
    # Map standard section names to prompt instructions
    section_templates = {
        "weather": f"Weather forecast for {OWNER_CITY}",
        "news": "Top news headlines (US Politics, World News, AI & Tech — 2-3 stories each)",
        "tasks": "Tasks and priorities for the day (from COMMITMENTS.md)",
        "calendar": "Upcoming calendar events for today and tomorrow",
    }

    sections = []
    section_num = 1

    for section_key in MORNING_BRIEF_SECTIONS:
        key = section_key.strip().lower()
        if key in section_templates:
            sections.append(f"{section_num}. {section_templates[key]}")
            section_num += 1

    # Add any custom sections from config
    for custom in CUSTOM_BRIEF_SECTIONS:
        if isinstance(custom, str) and custom.strip():
            sections.append(f"{section_num}. {custom.strip()}")
            section_num += 1

    # Always include overnight work summary
    sections.append(f"{section_num}. Any overnight work summary")

    sections_text = "\n    ".join(sections)
    owner = OWNER_NAME or "the user"

    return f"""
    Generate {owner}'s morning brief. Include:
    {sections_text}

    Format it nicely for Telegram. Keep each section concise.
    """


# ============================================
# ROBUST MORNING BRIEF GENERATION
# ============================================

async def _fetch_weather(city: str) -> Optional[str]:
    """Fetch weather from wttr.in — free, no API key needed."""
    try:
        import aiohttp
        from urllib.parse import quote_plus

        # Detailed format: emoji + condition + temp + feels-like + humidity + wind
        url = f"https://wttr.in/{quote_plus(city)}?format=%c+%C+%t+|+Feels+like+%f+|+Humidity+%h+|+Wind+%w"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    weather_line = (await response.text()).strip()
                    if weather_line and "Unknown" not in weather_line:
                        return weather_line
    except Exception as e:
        logger.warning(f"Weather fetch failed for {city}: {e}")
    return None


async def _fetch_news_gemini() -> Optional[str]:
    """Generate news headlines using Gemini API via raw HTTP (no SDK hangs)."""
    api_key = GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    try:
        import aiohttp

        tz = pytz.timezone(TIMEZONE)
        today_str = datetime.now(tz).strftime("%A, %B %d, %Y")

        prompt = (
            f"Today is {today_str}. "
            "Generate exactly 3 short, current news headlines that would be relevant "
            "and interesting. Each headline should be one line with a relevant emoji prefix. "
            "Cover a mix: 1 US/World news, 1 Tech/AI, 1 general interest. "
            "Keep each headline under 80 characters. No commentary, just headlines."
        )

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=15)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    text = (
                        data.get("candidates", [{}])[0]
                        .get("content", {})
                        .get("parts", [{}])[0]
                        .get("text", "")
                    )
                    if text and len(text.strip()) > 10:
                        return text.strip()
                else:
                    body = await response.text()
                    logger.warning(f"Gemini API returned {response.status}: {body[:200]}")

    except asyncio.TimeoutError:
        logger.warning("Gemini news generation timed out (15s)")
    except Exception as e:
        logger.warning(f"Gemini news generation failed: {e}")
    return None


def _read_tasks() -> Optional[str]:
    """Read pending tasks from memory/tasks/ directory or COMMITMENTS file."""
    tasks_found = []

    # 1. Check memory/tasks/ directory
    tasks_dir = MEMORY_DIR / "tasks"
    if tasks_dir.exists() and tasks_dir.is_dir():
        for task_file in sorted(tasks_dir.glob("*.md")):
            try:
                content = task_file.read_text().strip()
                if content:
                    # Extract first line as task name
                    first_line = content.split("\n")[0].strip().lstrip("#").strip()
                    if first_line:
                        tasks_found.append(f"• {first_line}")
            except Exception:
                pass

    # Also check tasks/*.txt
    if tasks_dir.exists():
        for task_file in sorted(tasks_dir.glob("*.txt")):
            try:
                content = task_file.read_text().strip()
                for line in content.split("\n"):
                    line = line.strip()
                    if line and not line.startswith("#"):
                        tasks_found.append(f"• {line}")
            except Exception:
                pass

    # 2. Check COMMITMENTS.md for pending tasks
    from config import WORKSPACE_DIR
    commitments_file = WORKSPACE_DIR / "COMMITMENTS.md"
    if commitments_file.exists():
        try:
            content = commitments_file.read_text()
            # Extract uncompleted tasks (- [ ] lines)
            for match in re.finditer(r'-\s*\[\s*\]\s*(.+)', content):
                task_text = match.group(1).strip()
                if task_text and len(tasks_found) < 5:
                    tasks_found.append(f"• {task_text}")
        except Exception:
            pass

    # 3. Check HEARTBEAT.md for pending tasks
    heartbeat_content = read_heartbeat()
    if heartbeat_content:
        for match in re.finditer(r'-\s*\[\s*\]\s*(.+)', heartbeat_content):
            task_text = match.group(1).strip()
            if task_text and len(tasks_found) < 7:
                entry = f"• {task_text}"
                if entry not in tasks_found:
                    tasks_found.append(entry)

    if tasks_found:
        return "\n".join(tasks_found[:7])  # Max 7 tasks
    return None


async def generate_morning_brief_content() -> str:
    """
    Generate a complete morning brief using free APIs and local data.

    Works with ZERO configuration beyond OWNER_CITY.
    Each section fails gracefully — never returns empty.
    """
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)
    greeting_name = OWNER_NAME if OWNER_NAME else ""
    greeting = f"Good morning{', ' + greeting_name if greeting_name else ''}!"
    day_str = now.strftime("%A, %B %d")

    sections = []
    sections.append(f"{BOT_EMOJI} {greeting}")
    sections.append(f"📅 {day_str}\n")

    # --- Weather Section ---
    if "weather" in [s.strip().lower() for s in MORNING_BRIEF_SECTIONS]:
        try:
            weather = await _fetch_weather(OWNER_CITY)
            if weather:
                sections.append(f"🌤️ **Weather — {OWNER_CITY}**\n{weather}\n")
            else:
                sections.append(f"🌤️ **Weather**\nCouldn't fetch weather for {OWNER_CITY}.\n")
        except Exception as e:
            logger.warning(f"Weather section failed: {e}")
            # Skip silently

    # --- News Section ---
    if "news" in [s.strip().lower() for s in MORNING_BRIEF_SECTIONS]:
        try:
            news = await _fetch_news_gemini()
            if news:
                sections.append(f"📰 **Headlines**\n{news}\n")
        except Exception as e:
            logger.warning(f"News section failed: {e}")
            # Skip silently — news is nice-to-have

    # --- Tasks Section ---
    if "tasks" in [s.strip().lower() for s in MORNING_BRIEF_SECTIONS]:
        try:
            tasks = _read_tasks()
            if tasks:
                sections.append(f"📋 **Today's Tasks**\n{tasks}\n")
            else:
                sections.append(
                    "📋 **Today's Tasks**\n"
                    "No tasks yet — try telling me what you need to do today!\n"
                )
        except Exception as e:
            logger.warning(f"Tasks section failed: {e}")

    # --- Custom Sections ---
    for custom in CUSTOM_BRIEF_SECTIONS:
        if isinstance(custom, str) and custom.strip():
            sections.append(f"📌 {custom.strip()}\n")

    # --- Footer ---
    sections.append("Have a great day! 💫")

    return "\n".join(sections)


async def send_morning_brief(send_message_callback) -> None:
    """Generate and send the morning brief. Never crashes, never sends nothing."""
    logger.info("Generating morning brief...")

    try:
        brief = await generate_morning_brief_content()

        if brief and len(brief.strip()) > 20:
            await send_message_callback(brief)
            log_to_today("Morning brief sent")
        else:
            # Absolute fallback — should never happen but just in case
            greeting_name = OWNER_NAME if OWNER_NAME else ""
            fallback = (
                f"{BOT_EMOJI} Good morning{', ' + greeting_name if greeting_name else ''}! 🌅\n\n"
                f"I had trouble building the full brief today, "
                f"but I'm here and ready to help with anything you need!"
            )
            await send_message_callback(fallback)
            log_to_today("Morning brief sent (fallback)")

    except Exception as e:
        logger.error(f"Error sending morning brief: {e}")
        # Even if everything fails, send SOMETHING
        try:
            greeting_name = OWNER_NAME if OWNER_NAME else ""
            await send_message_callback(
                f"{BOT_EMOJI} Good morning{', ' + greeting_name if greeting_name else ''}! "
                f"Ready when you are. 💫"
            )
            log_to_today("Morning brief sent (emergency fallback)")
        except Exception as e2:
            logger.error(f"Even fallback morning brief failed: {e2}")


async def start_heartbeat_scheduler(send_message_callback) -> None:
    """Start the heartbeat scheduler loop."""
    logger.info(f"Starting heartbeat scheduler (every {HEARTBEAT_INTERVAL_MINUTES} minutes)")

    while True:
        try:
            await run_heartbeat(send_message_callback)
        except Exception as e:
            logger.exception(f"Heartbeat error: {e}")

        # Wait for next heartbeat
        await asyncio.sleep(HEARTBEAT_INTERVAL_MINUTES * 60)
