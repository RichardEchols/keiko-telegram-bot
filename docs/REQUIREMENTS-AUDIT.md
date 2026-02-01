# Requirements Audit — Kiyomi Engine

*Checked: Feb 1, 2026 at 1:00 AM*

## Current `requirements.txt`
```
python-telegram-bot[job-queue]>=21.0
python-dotenv>=1.0.0
pytz>=2024.1
aiofiles>=23.2.1
anthropic>=0.40.0
pyautogui>=0.9.54
pillow>=10.0.0
psutil>=5.9.0
```

## Missing Dependencies

| Package | Used In | Purpose |
|---------|---------|---------|
| `aiohttp` | deploy_tools.py, monitoring.py | HTTP client for deployment verification and health monitoring |

## Recommended `requirements.txt`
```
python-telegram-bot[job-queue]>=21.0
python-dotenv>=1.0.0
pytz>=2024.1
aiofiles>=23.2.1
anthropic>=0.40.0
pyautogui>=0.9.54
pillow>=10.0.0
psutil>=5.9.0
aiohttp>=3.9.0
```

## Notes

- `pyautogui` may not be needed for headless/server deployments (used for screen automation). Consider making optional.
- `anthropic` SDK is included but Kiyomi primarily uses Claude Code CLI. May be optional for some users.
- All other imports are either stdlib or local modules within the codebase.

## Local Modules (27 files, all part of the engine)
config, connection_manager, corrections, cost_tracking, deploy_tools, escalation, executor, file_handler, git_tools, heartbeat, learning, mcp_bridge, memory_manager, milestones, monitoring, plugin_system, proactive, projects, quick_actions, reminders, security, self_update, session_manager, session_state, skills, smart_response, streaming, swarm, voice, watchdog, web_tools
