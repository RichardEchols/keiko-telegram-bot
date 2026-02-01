# Kiyomi Engine — Productization Audit

*What needs to change before we can sell this.*

---

## Current State

The engine is solid. 13,782 lines of Python. Features that actually work:
- Telegram bot interface with message routing
- Watchdog daemon (health checks, auto-recovery, memory limits, log rotation)
- Swarm intelligence (multi-agent coordination)
- Proactive behaviors (morning prep, idle detection, factory mode)
- Memory system (daily logs, long-term, file-based)
- Skills loader (markdown-based instruction files)
- Plugin system (extensible)
- Cost tracking
- Security module
- Voice workflow (ElevenLabs TTS)
- Self-update mechanism
- Session management
- Web tools, Git tools, File handler

**Verdict:** This is 80% shippable. The remaining 20% is removing Richard-specific hardcoding and adding a setup wizard.

---

## 🔴 Critical (Must Fix Before Selling)

### 1. Hardcoded Personal Data in `config.py`

**Problem:** Telegram token, Richard's email/phone, user IDs, API keys all have defaults baked in.

**Fix:**
```python
# BEFORE (leaks Richard's data to every buyer)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8549475880:AAFGvXc...")
ALLOWED_USER_IDS = [8295554376]  # ONLY Richard

# AFTER (env-only, no defaults)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_USER_IDS = json.loads(os.getenv("ALLOWED_USER_IDS", "[]"))
```

**Files affected:** `config.py`
**Effort:** 30 minutes

### 2. Hardcoded Paths in `skills.py`

**Problem:** Skills directory is `/Users/richardechols/Apps/claude-skills/` — won't exist on buyer's machine.

**Fix:**
```python
# BEFORE
SKILLS_DIR = Path("/Users/richardechols/Apps/claude-skills")

# AFTER
SKILLS_DIR = Path(os.getenv("KIYOMI_SKILLS_DIR", str(Path.home() / "kiyomi" / "skills")))
```

**Files affected:** `skills.py`
**Effort:** 15 minutes

### 3. Hardcoded Allowed Directories in `config.py`

**Problem:** `ALLOWED_DIRECTORIES` references `/Users/richardechols/` — buyer has a different username.

**Fix:**
```python
# BEFORE
ALLOWED_DIRECTORIES = [
    "/Users/richardechols/Apps/",
    "/Users/richardechols/Desktop/Work/",
    ...
]

# AFTER  
_home = str(Path.home())
ALLOWED_DIRECTORIES = json.loads(os.getenv("KIYOMI_ALLOWED_DIRS", json.dumps([
    f"{_home}/Documents/",
    f"{_home}/Desktop/",
    f"{_home}/Downloads/",
])))
```

**Files affected:** `config.py`
**Effort:** 15 minutes

### 4. Bot Name Hardcoded

**Problem:** `BOT_NAME = "Keiko"` and `BOT_EMOJI = "🦊"` — buyer should name their own.

**Fix:**
```python
BOT_NAME = os.getenv("KIYOMI_BOT_NAME", "Kiyomi")
BOT_EMOJI = os.getenv("KIYOMI_BOT_EMOJI", "✨")
```

**Files affected:** `config.py`, any files referencing "Keiko" by name
**Effort:** 20 minutes (need to grep for "Keiko" references throughout)

### 5. No `.env.example` File

**Problem:** Buyer has no idea what environment variables to set.

**Fix:** Create `.env.example` with all variables, comments explaining each one, and clear instructions.

**Effort:** 30 minutes

### 6. No Setup Script / Installer

**Problem:** No automated way to install dependencies, create directories, configure `.env`, and start the daemon.

**Fix:** Create `install.sh` that:
1. Checks prerequisites (Python 3.11+, pip)
2. Creates virtualenv and installs deps
3. Creates workspace directories
4. Walks user through `.env` configuration (interactive prompts)
5. Creates LaunchAgent plist for 24/7 operation
6. Starts the bot

**Effort:** 2-3 hours

---

## 🟡 Important (Should Fix Before Selling)

### 7. `requirements.txt` / `pyproject.toml` Missing or Incomplete

**Status:** Need to verify. All imports must be installable.

**Fix:** Generate from actual imports:
```bash
pipreqs ~/clawd/projects/kiyomi-engine/ --force
```

**Effort:** 30 minutes

### 8. Workspace Template Files

**Problem:** Workspace files (SOUL.md, USER.md, etc.) contain Richard-specific content.

**Fix:** Create template versions:
- `workspace/templates/SOUL.md.template` — generic personality
- `workspace/templates/USER.md.template` — blank user profile
- `workspace/templates/IDENTITY.md.template` — generic identity
- `workspace/templates/COMMITMENTS.md.template` — empty commitments

Setup script copies templates to workspace on first run.

**Effort:** 1 hour

### 9. README.md

**Problem:** Probably either missing or references "Keiko" throughout.

**Fix:** Write a proper README:
- What is Kiyomi
- Prerequisites
- Quick start (5 minutes)
- Configuration guide
- Skills guide
- Troubleshooting
- Contributing

**Effort:** 2 hours

### 10. Cockpit Needs Its Own Audit

**Problem:** The Next.js cockpit likely has hardcoded URLs, API endpoints, or references.

**Fix:** Audit `kiyomi-cockpit/` separately. Ensure it connects to local engine via configurable URL.

**Effort:** 1-2 hours

---

## 🟢 Nice to Have (After Launch)

### 11. Multi-Model Support
Currently tied to Claude. Adding support for GPT-4, Gemini, local models (Ollama) would expand the market.

### 12. Windows/Linux Support
Currently Mac-only (LaunchAgent). Adding systemd (Linux) and Task Scheduler (Windows) support.

### 13. Skill Marketplace
Central repo where users can browse, install, and share skills.

### 14. One-Click Vertical Installer
`kiyomi install-vertical lawyer` — downloads and applies a vertical config package.

### 15. GUI Setup Wizard
Replace CLI setup with a web-based wizard in the Cockpit.

---

## Priority Order for Shipping

| # | Task | Effort | Impact |
|---|------|--------|--------|
| 1 | Remove hardcoded data from config.py | 30 min | CRITICAL — can't sell with Richard's tokens |
| 2 | Fix skills.py paths | 15 min | CRITICAL — won't work on buyer's machine |
| 3 | Fix allowed directories | 15 min | CRITICAL — security boundary broken |
| 4 | Make bot name configurable | 20 min | HIGH — buyers want to name their own |
| 5 | Create .env.example | 30 min | HIGH — buyers need to know what to configure |
| 6 | Create workspace templates | 1 hr | HIGH — clean first-run experience |
| 7 | Write install.sh | 2-3 hr | HIGH — one-command setup is the promise |
| 8 | Verify requirements.txt | 30 min | MEDIUM — must install cleanly |
| 9 | Write README.md | 2 hr | MEDIUM — first thing buyers see |
| 10 | Audit cockpit | 1-2 hr | MEDIUM — dashboard needs to work too |

**Total estimated effort: 8-10 hours**

That's one overnight shift for Brock + Gemini.

---

*Audit completed: January 31, 2026*
*Author: Brock (AI Agent)*
