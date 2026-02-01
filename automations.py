"""
Kiyomi Automation Triggers System

Allows users to create simple if-then automations via natural language.
Stores automations as JSON in memory/automations/
"""

import json
import os
import re
import uuid
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

AUTOMATIONS_DIR = os.path.expanduser("~/kiyomi/memory/automations")

# Day name → weekday int (Monday=0 … Sunday=6)
_DAY_MAP = {
    "monday": 0, "mon": 0,
    "tuesday": 1, "tue": 1, "tues": 1,
    "wednesday": 2, "wed": 2,
    "thursday": 3, "thu": 3, "thurs": 3,
    "friday": 4, "fri": 4,
    "saturday": 5, "sat": 5,
    "sunday": 6, "sun": 6,
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_time(text: str) -> Optional[Dict[str, int]]:
    """Extract hour and minute from a time string like '9am', '2:30pm', '14:00'."""
    text = text.strip().lower()

    # 14:00 / 9:30
    m = re.match(r"(\d{1,2}):(\d{2})\s*(am|pm)?", text)
    if m:
        hour = int(m.group(1))
        minute = int(m.group(2))
        if m.group(3) == "pm" and hour < 12:
            hour += 12
        elif m.group(3) == "am" and hour == 12:
            hour = 0
        return {"hour": hour, "minute": minute}

    # 9am / 2pm
    m = re.match(r"(\d{1,2})\s*(am|pm)", text)
    if m:
        hour = int(m.group(1))
        if m.group(2) == "pm" and hour < 12:
            hour += 12
        elif m.group(2) == "am" and hour == 12:
            hour = 0
        return {"hour": hour, "minute": 0}

    # bare number (treat as hour, 24-hr)
    m = re.match(r"^(\d{1,2})$", text)
    if m:
        hour = int(m.group(1))
        if 0 <= hour <= 23:
            return {"hour": hour, "minute": 0}

    return None


def _parse_schedule(text: str) -> Optional[dict]:
    """Convert natural language into a schedule config dict.

    Returns dict with optional keys:
        hour, minute, day_of_week, interval_hours, description
    """
    lower = text.lower()

    config: dict = {"description": text.strip()}

    # --- interval: "every N hours/minutes" ---
    m = re.search(r"every\s+(\d+)\s+hour", lower)
    if m:
        config["interval_hours"] = int(m.group(1))
        return config

    m = re.search(r"every\s+(\d+)\s+minute", lower)
    if m:
        config["interval_minutes"] = int(m.group(1))
        return config

    # --- day of week ---
    for day_name, day_int in _DAY_MAP.items():
        if day_name in lower:
            config["day_of_week"] = day_int
            break

    # --- "daily" means every day, no day_of_week filter ---
    if "daily" in lower or "every day" in lower:
        config.pop("day_of_week", None)

    # --- time extraction ---
    # look for "at <time>"
    m = re.search(r"at\s+(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)", lower)
    if m:
        parsed = _parse_time(m.group(1))
        if parsed:
            config.update(parsed)
            return config

    # fallback: any time-like token
    for token in re.findall(r"\d{1,2}(?::\d{2})?\s*(?:am|pm)", lower):
        parsed = _parse_time(token)
        if parsed:
            config.update(parsed)
            return config

    # If we got a day but no time, default to 9:00 AM
    if "day_of_week" in config:
        config.setdefault("hour", 9)
        config.setdefault("minute", 0)
        return config

    # If nothing useful was extracted, return None
    if len(config) <= 1:  # only description
        return None

    return config


def _parse_keywords(text: str) -> Optional[List[str]]:
    """Extract keywords from 'about <topic>' or 'containing <words>' patterns."""
    lower = text.lower()

    for pattern in [
        r"about\s+(.+?)(?:,|\.|$)",
        r"containing\s+(.+?)(?:,|\.|$)",
        r"mentions?\s+(.+?)(?:,|\.|$)",
        r"includes?\s+(.+?)(?:,|\.|$)",
    ]:
        m = re.search(pattern, lower)
        if m:
            raw = m.group(1).strip()
            # split on 'or', 'and', commas
            parts = re.split(r"\s+(?:or|and)\s+|,\s*", raw)
            return [p.strip().strip("'\"") for p in parts if p.strip()]

    return None


def _parse_sender(text: str) -> Optional[str]:
    """Extract sender from 'from <person>' pattern."""
    m = re.search(r"from\s+([\w@.\-]+)", text, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return None


def _detect_action(text: str) -> Dict[str, str]:
    """Detect the action type and config from natural language."""
    lower = text.lower()

    if any(w in lower for w in ["summarize", "summary"]):
        return {"action_type": "summary", "action_config": {"what": text.strip()}}

    if any(w in lower for w in ["alert", "warn", "urgent"]):
        return {"action_type": "alert", "action_config": {"message": text.strip()}}

    if any(w in lower for w in ["send me", "text me", "message me", "notify me", "tell me", "remind me"]):
        return {"action_type": "message", "action_config": {"message": text.strip()}}

    # default
    return {"action_type": "message", "action_config": {"message": text.strip()}}


# ---------------------------------------------------------------------------
# Automation model
# ---------------------------------------------------------------------------

class Automation:
    """A single automation rule: trigger → action."""

    def __init__(
        self,
        id: str,
        name: str,
        trigger_type: str,
        trigger_config: dict,
        action_type: str,
        action_config: dict,
        enabled: bool = True,
    ):
        self.id = id
        self.name = name
        self.trigger_type = trigger_type   # 'schedule', 'keyword', 'condition'
        self.trigger_config = trigger_config
        self.action_type = action_type     # 'message', 'summary', 'alert', 'skill'
        self.action_config = action_config
        self.enabled = enabled
        self.created_at = datetime.now().isoformat()
        self.last_run: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "trigger_type": self.trigger_type,
            "trigger_config": self.trigger_config,
            "action_type": self.action_type,
            "action_config": self.action_config,
            "enabled": self.enabled,
            "created_at": self.created_at,
            "last_run": self.last_run,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Automation":
        auto = cls(
            id=data["id"],
            name=data["name"],
            trigger_type=data["trigger_type"],
            trigger_config=data.get("trigger_config", {}),
            action_type=data["action_type"],
            action_config=data.get("action_config", {}),
            enabled=data.get("enabled", True),
        )
        auto.created_at = data.get("created_at", auto.created_at)
        auto.last_run = data.get("last_run")
        return auto


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

class AutomationEngine:
    """Manages all automations: CRUD, trigger checking, execution."""

    def __init__(self, automations_dir: Optional[str] = None):
        self.automations_dir = automations_dir or AUTOMATIONS_DIR
        self.automations: List[Automation] = []
        self._load_automations()

    # -- persistence --------------------------------------------------------

    def _load_automations(self) -> None:
        """Load all automations from disk."""
        os.makedirs(self.automations_dir, exist_ok=True)
        self.automations = []

        for fname in os.listdir(self.automations_dir):
            if not fname.endswith(".json"):
                continue
            fpath = os.path.join(self.automations_dir, fname)
            try:
                with open(fpath, "r") as f:
                    data = json.load(f)
                self.automations.append(Automation.from_dict(data))
            except Exception as e:
                logger.warning("Failed to load automation %s: %s", fname, e)

        logger.info("Loaded %d automation(s) from %s", len(self.automations), self.automations_dir)

    def save_automation(self, automation: Automation) -> None:
        """Persist a single automation to disk."""
        os.makedirs(self.automations_dir, exist_ok=True)
        fpath = os.path.join(self.automations_dir, f"{automation.id}.json")
        try:
            with open(fpath, "w") as f:
                json.dump(automation.to_dict(), f, indent=2)
            logger.debug("Saved automation %s → %s", automation.id, fpath)
        except Exception as e:
            logger.error("Failed to save automation %s: %s", automation.id, e)

    # -- natural language creation ------------------------------------------

    def create_from_natural_language(self, user_input: str) -> Optional[Automation]:
        """Parse natural language into an Automation.

        Returns the created Automation, or None if the input cannot be parsed.
        """
        lower = user_input.lower().strip()
        if not lower:
            return None

        trigger_type: Optional[str] = None
        trigger_config: dict = {}
        action_info = _detect_action(user_input)

        # ---- detect trigger type ----

        # Schedule patterns
        schedule_patterns = [
            r"\bevery\s+(?:day|week|monday|tuesday|wednesday|thursday|friday|saturday|sunday|mon|tue|wed|thu|fri|sat|sun|\d+\s+(?:hour|minute))",
            r"\bdaily\b",
            r"\bweekly\b",
            r"\bremind\s+me\b",
        ]
        is_schedule = any(re.search(p, lower) for p in schedule_patterns)

        # Keyword/event patterns
        keyword_patterns = [
            r"\bwhen\s+(?:i\s+)?(?:get|receive)\b",
            r"\bwhen\s+.*\b(?:email|message|text)\b",
            r"\b(?:about|containing|mentions?|includes?)\b",
        ]
        is_keyword = any(re.search(p, lower) for p in keyword_patterns)

        # Condition patterns
        condition_patterns = [
            r"\bif\s+.*\b(?:deadline|due|expires?|within)\b",
            r"\bwhen\s+.*\b(?:deadline|due|expires?|within)\b",
        ]
        is_condition = any(re.search(p, lower) for p in condition_patterns)

        # --- build trigger ---

        if is_condition:
            trigger_type = "condition"
            # extract "within N days"
            m = re.search(r"within\s+(\d+)\s+day", lower)
            days = int(m.group(1)) if m else 3
            trigger_config = {
                "check": "deadline_within_days",
                "days": days,
                "description": user_input.strip(),
            }

        elif is_schedule:
            trigger_type = "schedule"
            schedule = _parse_schedule(user_input)
            if schedule is None:
                # couldn't parse a schedule — bail
                return None
            trigger_config = schedule

        elif is_keyword:
            trigger_type = "keyword"
            keywords = _parse_keywords(user_input)
            sender = _parse_sender(user_input)
            if not keywords and not sender:
                # At least grab nouns from the input as keywords
                # Simple fallback: use notable words
                words = re.findall(r"\b[a-z]{4,}\b", lower)
                stop = {"when", "that", "this", "from", "with", "about", "have", "will",
                        "send", "text", "message", "alert", "email", "every", "remind"}
                keywords = [w for w in words if w not in stop][:5]
            trigger_config = {
                "keywords": keywords or [],
                "description": user_input.strip(),
            }
            if sender:
                trigger_config["from"] = sender

        else:
            # Can't determine trigger type
            return None

        # --- create automation ---

        auto_id = uuid.uuid4().hex[:12]
        name = user_input.strip()[:80]

        auto = Automation(
            id=auto_id,
            name=name,
            trigger_type=trigger_type,
            trigger_config=trigger_config,
            action_type=action_info["action_type"],
            action_config=action_info["action_config"],
        )

        self.automations.append(auto)
        self.save_automation(auto)

        logger.info("Created automation '%s' [%s → %s]", name, trigger_type, action_info["action_type"])
        return auto

    # -- trigger checking ---------------------------------------------------

    def check_triggers(self) -> List[Automation]:
        """Check all enabled automations and return those whose triggers fired.

        Call this periodically (e.g., every heartbeat).  Keyword triggers are
        *not* checked here — use ``check_message()`` for those.
        """
        now = datetime.now()
        fired: List[Automation] = []

        for auto in self.automations:
            if not auto.enabled:
                continue

            if auto.trigger_type == "schedule":
                if self._check_schedule(auto, now):
                    fired.append(auto)

            elif auto.trigger_type == "condition":
                if self._check_condition(auto, now):
                    fired.append(auto)

            # keyword triggers are event-driven, skip here

        return fired

    def check_message(self, message: str, sender: Optional[str] = None) -> List[Automation]:
        """Check if an incoming message triggers any keyword automations."""
        lower_msg = message.lower()
        fired: List[Automation] = []

        for auto in self.automations:
            if not auto.enabled or auto.trigger_type != "keyword":
                continue

            cfg = auto.trigger_config

            # Check sender filter
            required_sender = cfg.get("from")
            if required_sender and sender:
                if required_sender.lower() not in sender.lower():
                    continue
            elif required_sender and not sender:
                continue

            # Check keywords
            keywords = cfg.get("keywords", [])
            if not keywords:
                continue
            if any(kw.lower() in lower_msg for kw in keywords):
                fired.append(auto)

        return fired

    def _check_schedule(self, auto: Automation, now: datetime) -> bool:
        """Return True if a schedule-based automation should fire now."""
        cfg = auto.trigger_config

        # Prevent double-firing: must be > 1 min since last run
        if auto.last_run:
            try:
                last = datetime.fromisoformat(auto.last_run)
                if (now - last).total_seconds() < 60:
                    return False
            except (ValueError, TypeError):
                pass

        # --- interval-based ---
        interval_hours = cfg.get("interval_hours")
        interval_minutes = cfg.get("interval_minutes")

        if interval_hours is not None:
            if auto.last_run is None:
                return True
            try:
                last = datetime.fromisoformat(auto.last_run)
                return (now - last) >= timedelta(hours=interval_hours)
            except (ValueError, TypeError):
                return True

        if interval_minutes is not None:
            if auto.last_run is None:
                return True
            try:
                last = datetime.fromisoformat(auto.last_run)
                return (now - last) >= timedelta(minutes=interval_minutes)
            except (ValueError, TypeError):
                return True

        # --- cron-like: day_of_week + hour + minute ---
        target_dow = cfg.get("day_of_week")
        target_hour = cfg.get("hour")
        target_minute = cfg.get("minute", 0)

        # day of week check
        if target_dow is not None and now.weekday() != target_dow:
            return False

        # hour/minute check (5-minute window)
        if target_hour is not None:
            target_total = target_hour * 60 + target_minute
            current_total = now.hour * 60 + now.minute
            if abs(current_total - target_total) > 5:
                return False

            # double-fire guard for cron-like (same day + hour window)
            if auto.last_run:
                try:
                    last = datetime.fromisoformat(auto.last_run)
                    if last.date() == now.date() and abs(last.hour * 60 + last.minute - target_total) <= 5:
                        return False
                except (ValueError, TypeError):
                    pass

            return True

        return False

    def _check_condition(self, auto: Automation, now: datetime) -> bool:
        """Evaluate a condition trigger. Returns True if the condition is met."""
        cfg = auto.trigger_config
        check = cfg.get("check", "")

        # double-fire guard: max once per hour for conditions
        if auto.last_run:
            try:
                last = datetime.fromisoformat(auto.last_run)
                if (now - last).total_seconds() < 3600:
                    return False
            except (ValueError, TypeError):
                pass

        if check == "deadline_within_days":
            days = cfg.get("days", 3)
            source = cfg.get("source", "")
            return self._check_deadline_files(source, days, now)

        # Unknown condition — don't fire
        logger.debug("Unknown condition check: %s", check)
        return False

    def _check_deadline_files(self, source: str, days: int, now: datetime) -> bool:
        """Scan a directory for deadline files and check proximity."""
        source_path = os.path.expanduser(source) if source else ""
        if not source_path or not os.path.isdir(source_path):
            return False

        threshold = now + timedelta(days=days)

        for fname in os.listdir(source_path):
            if not fname.endswith(".json"):
                continue
            try:
                fpath = os.path.join(source_path, fname)
                with open(fpath, "r") as f:
                    data = json.load(f)
                deadline_str = data.get("deadline") or data.get("due_date") or data.get("due")
                if deadline_str:
                    deadline = datetime.fromisoformat(deadline_str)
                    if now <= deadline <= threshold:
                        return True
            except Exception:
                continue

        return False

    # -- execution ----------------------------------------------------------

    async def execute_automation(self, automation: Automation, context: dict) -> str:
        """Execute the action for a triggered automation.

        Returns a string result suitable for sending to the user.
        """
        action = automation.action_type
        cfg = automation.action_config
        result = ""

        if action == "message":
            result = cfg.get("message", automation.name)

        elif action == "summary":
            what = cfg.get("what", "recent activity")
            result = f"📋 Summary requested: {what}"

        elif action == "alert":
            msg = cfg.get("message", automation.name)
            result = f"🚨 ALERT: {msg}"

        elif action == "skill":
            skill = cfg.get("skill", "unknown")
            result = f"🔧 Running skill: {skill}"

        else:
            result = f"Automation fired: {automation.name}"

        # Update last_run
        automation.last_run = datetime.now().isoformat()
        self.save_automation(automation)

        logger.info("Executed automation '%s' → %s", automation.name, action)
        return result

    # -- management ---------------------------------------------------------

    def list_automations(self) -> str:
        """Return a formatted string listing all automations."""
        if not self.automations:
            return (
                "📭 No automations set up yet.\n\n"
                "Try saying something like:\n"
                '• "Every Monday at 9am, send me a weekly summary"\n'
                '• "When I get an email about invoices, alert me"\n'
                '• "Remind me every day at 8am to check email"'
            )

        lines = ["📋 **Your Automations:**\n"]
        for i, auto in enumerate(self.automations, 1):
            status = "✅" if auto.enabled else "⏸️"
            trigger = auto.trigger_type.capitalize()
            action = auto.action_type.capitalize()
            last = auto.last_run[:16] if auto.last_run else "Never"
            lines.append(
                f"{i}. {status} **{auto.name}**\n"
                f"   Trigger: {trigger} | Action: {action}\n"
                f"   Last run: {last} | ID: `{auto.id}`"
            )

        return "\n".join(lines)

    def delete_automation(self, automation_id: str) -> bool:
        """Delete an automation by ID. Returns True if found and deleted."""
        for auto in self.automations:
            if auto.id == automation_id:
                self.automations.remove(auto)
                fpath = os.path.join(self.automations_dir, f"{automation_id}.json")
                try:
                    os.remove(fpath)
                except OSError as e:
                    logger.warning("Could not delete file %s: %s", fpath, e)
                logger.info("Deleted automation %s", automation_id)
                return True
        return False

    def toggle_automation(self, automation_id: str) -> Optional[bool]:
        """Toggle an automation's enabled state. Returns new state, or None if not found."""
        for auto in self.automations:
            if auto.id == automation_id:
                auto.enabled = not auto.enabled
                self.save_automation(auto)
                logger.info("Toggled automation %s → %s", automation_id, auto.enabled)
                return auto.enabled
        return None
