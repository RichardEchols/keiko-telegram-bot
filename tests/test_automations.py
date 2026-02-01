"""
Tests for Kiyomi Automation Triggers System
"""

import json
import os
import sys
import shutil
import tempfile
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

# Add parent dir to path so we can import automations
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from automations import (
    Automation,
    AutomationEngine,
    _parse_time,
    _parse_schedule,
    _parse_keywords,
    _parse_sender,
    _detect_action,
)


class TestParseTime(unittest.TestCase):
    """Test the _parse_time helper."""

    def test_9am(self):
        result = _parse_time("9am")
        self.assertEqual(result, {"hour": 9, "minute": 0})

    def test_2pm(self):
        result = _parse_time("2pm")
        self.assertEqual(result, {"hour": 14, "minute": 0})

    def test_12am(self):
        result = _parse_time("12am")
        self.assertEqual(result, {"hour": 0, "minute": 0})

    def test_12pm(self):
        result = _parse_time("12pm")
        self.assertEqual(result, {"hour": 12, "minute": 0})

    def test_930am(self):
        result = _parse_time("9:30am")
        self.assertEqual(result, {"hour": 9, "minute": 30})

    def test_230pm(self):
        result = _parse_time("2:30pm")
        self.assertEqual(result, {"hour": 14, "minute": 30})

    def test_14_00(self):
        result = _parse_time("14:00")
        self.assertEqual(result, {"hour": 14, "minute": 0})

    def test_9_with_space_am(self):
        result = _parse_time("9 am")
        self.assertEqual(result, {"hour": 9, "minute": 0})

    def test_invalid(self):
        result = _parse_time("not a time")
        self.assertIsNone(result)


class TestParseSchedule(unittest.TestCase):
    """Test the _parse_schedule helper."""

    def test_every_monday_at_9am(self):
        result = _parse_schedule("Every Monday at 9am")
        self.assertIsNotNone(result)
        self.assertEqual(result["day_of_week"], 0)
        self.assertEqual(result["hour"], 9)
        self.assertEqual(result["minute"], 0)

    def test_daily_at_8am(self):
        result = _parse_schedule("daily at 8am")
        self.assertIsNotNone(result)
        self.assertNotIn("day_of_week", result)
        self.assertEqual(result["hour"], 8)

    def test_every_friday_at_5pm(self):
        result = _parse_schedule("Every Friday at 5pm")
        self.assertIsNotNone(result)
        self.assertEqual(result["day_of_week"], 4)
        self.assertEqual(result["hour"], 17)

    def test_every_2_hours(self):
        result = _parse_schedule("every 2 hours")
        self.assertIsNotNone(result)
        self.assertEqual(result["interval_hours"], 2)

    def test_every_30_minutes(self):
        result = _parse_schedule("every 30 minutes")
        self.assertIsNotNone(result)
        self.assertEqual(result["interval_minutes"], 30)

    def test_every_day_at_noon(self):
        result = _parse_schedule("every day at 12pm")
        self.assertIsNotNone(result)
        self.assertNotIn("day_of_week", result)
        self.assertEqual(result["hour"], 12)

    def test_every_sunday_default_time(self):
        result = _parse_schedule("every sunday")
        self.assertIsNotNone(result)
        self.assertEqual(result["day_of_week"], 6)
        # should default to 9:00
        self.assertEqual(result["hour"], 9)

    def test_unparseable(self):
        result = _parse_schedule("hello world")
        self.assertIsNone(result)


class TestParseKeywords(unittest.TestCase):
    """Test the _parse_keywords helper."""

    def test_about_invoices(self):
        result = _parse_keywords("email about invoices")
        self.assertIsNotNone(result)
        self.assertIn("invoices", result)

    def test_containing_payment_or_invoice(self):
        result = _parse_keywords("message containing payment or invoice")
        self.assertIsNotNone(result)
        self.assertIn("payment", result)
        self.assertIn("invoice", result)

    def test_mentions_deadline(self):
        result = _parse_keywords("when it mentions deadline")
        self.assertIsNotNone(result)
        self.assertIn("deadline", result)

    def test_no_keywords(self):
        result = _parse_keywords("just a random sentence")
        self.assertIsNone(result)


class TestParseSender(unittest.TestCase):
    def test_from_email(self):
        result = _parse_sender("email from john@example.com")
        self.assertEqual(result, "john@example.com")

    def test_from_name(self):
        result = _parse_sender("message from John")
        self.assertEqual(result, "John")

    def test_no_sender(self):
        result = _parse_sender("some random text")
        self.assertIsNone(result)


class TestDetectAction(unittest.TestCase):
    def test_summary(self):
        result = _detect_action("summarize my emails")
        self.assertEqual(result["action_type"], "summary")

    def test_alert(self):
        result = _detect_action("alert me about deadlines")
        self.assertEqual(result["action_type"], "alert")

    def test_send_me(self):
        result = _detect_action("send me a weekly report")
        self.assertEqual(result["action_type"], "message")

    def test_text_me(self):
        result = _detect_action("text me the results")
        self.assertEqual(result["action_type"], "message")

    def test_remind_me(self):
        result = _detect_action("remind me to check email")
        self.assertEqual(result["action_type"], "message")

    def test_default(self):
        result = _detect_action("do something")
        self.assertEqual(result["action_type"], "message")


class TestAutomation(unittest.TestCase):
    """Test the Automation model."""

    def test_to_dict_round_trip(self):
        auto = Automation(
            id="abc123",
            name="Test Automation",
            trigger_type="schedule",
            trigger_config={"hour": 9, "minute": 0},
            action_type="message",
            action_config={"message": "Hello"},
            enabled=True,
        )
        auto.last_run = "2025-01-01T09:00:00"

        d = auto.to_dict()
        restored = Automation.from_dict(d)

        self.assertEqual(restored.id, "abc123")
        self.assertEqual(restored.name, "Test Automation")
        self.assertEqual(restored.trigger_type, "schedule")
        self.assertEqual(restored.trigger_config["hour"], 9)
        self.assertEqual(restored.action_type, "message")
        self.assertEqual(restored.action_config["message"], "Hello")
        self.assertTrue(restored.enabled)
        self.assertEqual(restored.last_run, "2025-01-01T09:00:00")
        self.assertEqual(restored.created_at, auto.created_at)

    def test_from_dict_defaults(self):
        d = {
            "id": "xyz",
            "name": "Minimal",
            "trigger_type": "keyword",
            "action_type": "alert",
        }
        auto = Automation.from_dict(d)
        self.assertTrue(auto.enabled)
        self.assertEqual(auto.trigger_config, {})
        self.assertEqual(auto.action_config, {})
        self.assertIsNone(auto.last_run)


class TestAutomationEngine(unittest.TestCase):
    """Test the AutomationEngine."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.engine = AutomationEngine(automations_dir=self.tmpdir)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    # -- natural language creation --

    def test_create_monday_summary(self):
        auto = self.engine.create_from_natural_language(
            "Every Monday at 9am, send me a weekly summary"
        )
        self.assertIsNotNone(auto)
        self.assertEqual(auto.trigger_type, "schedule")
        self.assertEqual(auto.trigger_config["day_of_week"], 0)
        self.assertEqual(auto.trigger_config["hour"], 9)
        self.assertEqual(auto.action_type, "summary")

    def test_create_email_keyword(self):
        auto = self.engine.create_from_natural_language(
            "When I get an email about invoices, alert me"
        )
        self.assertIsNotNone(auto)
        self.assertEqual(auto.trigger_type, "keyword")
        self.assertIn("invoices", auto.trigger_config.get("keywords", []))
        self.assertEqual(auto.action_type, "alert")

    def test_create_daily_reminder(self):
        auto = self.engine.create_from_natural_language(
            "Remind me every day at 8am to check email"
        )
        self.assertIsNotNone(auto)
        self.assertEqual(auto.trigger_type, "schedule")
        self.assertEqual(auto.trigger_config["hour"], 8)

    def test_create_interval(self):
        auto = self.engine.create_from_natural_language(
            "Every 2 hours, check for new messages"
        )
        self.assertIsNotNone(auto)
        self.assertEqual(auto.trigger_type, "schedule")
        self.assertEqual(auto.trigger_config["interval_hours"], 2)

    def test_create_condition_deadline(self):
        auto = self.engine.create_from_natural_language(
            "If my case deadline is within 3 days, alert me"
        )
        self.assertIsNotNone(auto)
        self.assertEqual(auto.trigger_type, "condition")
        self.assertEqual(auto.trigger_config["days"], 3)
        self.assertEqual(auto.action_type, "alert")

    def test_create_unparseable_returns_none(self):
        auto = self.engine.create_from_natural_language("hello world")
        self.assertIsNone(auto)

    def test_create_empty_returns_none(self):
        auto = self.engine.create_from_natural_language("")
        self.assertIsNone(auto)

    # -- save/load cycle --

    def test_save_load_cycle(self):
        auto = self.engine.create_from_natural_language(
            "Every Monday at 9am, send me a weekly summary"
        )
        self.assertIsNotNone(auto)

        # Verify file exists on disk
        fpath = os.path.join(self.tmpdir, f"{auto.id}.json")
        self.assertTrue(os.path.exists(fpath))

        # Load into a new engine
        engine2 = AutomationEngine(automations_dir=self.tmpdir)
        self.assertEqual(len(engine2.automations), 1)
        loaded = engine2.automations[0]
        self.assertEqual(loaded.id, auto.id)
        self.assertEqual(loaded.name, auto.name)
        self.assertEqual(loaded.trigger_type, auto.trigger_type)

    # -- listing --

    def test_list_empty(self):
        result = self.engine.list_automations()
        self.assertIn("No automations", result)

    def test_list_nonempty(self):
        self.engine.create_from_natural_language(
            "Every Monday at 9am, send me a summary"
        )
        result = self.engine.list_automations()
        self.assertIn("Your Automations", result)
        self.assertIn("Monday", result)

    # -- deletion --

    def test_delete_existing(self):
        auto = self.engine.create_from_natural_language(
            "Every Friday at 5pm, send me a report"
        )
        self.assertIsNotNone(auto)
        self.assertEqual(len(self.engine.automations), 1)

        deleted = self.engine.delete_automation(auto.id)
        self.assertTrue(deleted)
        self.assertEqual(len(self.engine.automations), 0)

        # File should be gone
        fpath = os.path.join(self.tmpdir, f"{auto.id}.json")
        self.assertFalse(os.path.exists(fpath))

    def test_delete_nonexistent(self):
        deleted = self.engine.delete_automation("nonexistent_id")
        self.assertFalse(deleted)

    # -- toggle --

    def test_toggle(self):
        auto = self.engine.create_from_natural_language(
            "Every day at 9am, send me a report"
        )
        self.assertIsNotNone(auto)
        self.assertTrue(auto.enabled)

        new_state = self.engine.toggle_automation(auto.id)
        self.assertFalse(new_state)

        new_state = self.engine.toggle_automation(auto.id)
        self.assertTrue(new_state)

    def test_toggle_nonexistent(self):
        result = self.engine.toggle_automation("fake_id")
        self.assertIsNone(result)

    # -- schedule trigger checking --

    def test_check_schedule_time_match(self):
        auto = Automation(
            id="sched1",
            name="Test",
            trigger_type="schedule",
            trigger_config={"hour": 9, "minute": 0, "description": "test"},
            action_type="message",
            action_config={"message": "hi"},
        )
        self.engine.automations = [auto]

        # Mock datetime to 9:00
        fake_now = datetime(2026, 2, 2, 9, 0, 0)  # Monday
        fired = [a for a in self.engine.automations if self.engine._check_schedule(a, fake_now)]
        self.assertEqual(len(fired), 1)

    def test_check_schedule_time_no_match(self):
        auto = Automation(
            id="sched2",
            name="Test",
            trigger_type="schedule",
            trigger_config={"hour": 9, "minute": 0, "description": "test"},
            action_type="message",
            action_config={"message": "hi"},
        )
        self.engine.automations = [auto]

        # Mock datetime to 15:00
        fake_now = datetime(2026, 2, 2, 15, 0, 0)
        fired = [a for a in self.engine.automations if self.engine._check_schedule(a, fake_now)]
        self.assertEqual(len(fired), 0)

    def test_check_schedule_day_of_week(self):
        auto = Automation(
            id="sched3",
            name="Monday only",
            trigger_type="schedule",
            trigger_config={"hour": 9, "minute": 0, "day_of_week": 0, "description": "test"},
            action_type="message",
            action_config={"message": "hi"},
        )
        self.engine.automations = [auto]

        # 2026-02-02 is a Monday (weekday=0)
        fake_monday = datetime(2026, 2, 2, 9, 0, 0)
        fired = [a for a in self.engine.automations if self.engine._check_schedule(a, fake_monday)]
        self.assertEqual(len(fired), 1)

        # 2026-02-03 is a Tuesday (weekday=1)
        fake_tuesday = datetime(2026, 2, 3, 9, 0, 0)
        fired = [a for a in self.engine.automations if self.engine._check_schedule(a, fake_tuesday)]
        self.assertEqual(len(fired), 0)

    def test_check_schedule_interval(self):
        auto = Automation(
            id="int1",
            name="Interval",
            trigger_type="schedule",
            trigger_config={"interval_hours": 2, "description": "test"},
            action_type="message",
            action_config={"message": "hi"},
        )
        # Never run before — should fire
        self.engine.automations = [auto]
        fake_now = datetime(2026, 2, 2, 10, 0, 0)
        self.assertTrue(self.engine._check_schedule(auto, fake_now))

        # Mark as just run — should NOT fire
        auto.last_run = fake_now.isoformat()
        one_hour_later = fake_now + timedelta(hours=1)
        self.assertFalse(self.engine._check_schedule(auto, one_hour_later))

        # Two hours later — should fire
        two_hours_later = fake_now + timedelta(hours=2)
        self.assertTrue(self.engine._check_schedule(auto, two_hours_later))

    def test_check_schedule_double_fire_prevention(self):
        auto = Automation(
            id="dbl1",
            name="No double fire",
            trigger_type="schedule",
            trigger_config={"hour": 9, "minute": 0, "description": "test"},
            action_type="message",
            action_config={"message": "hi"},
        )
        fake_now = datetime(2026, 2, 2, 9, 0, 0)

        # First check — should fire
        self.assertTrue(self.engine._check_schedule(auto, fake_now))

        # Mark as run
        auto.last_run = fake_now.isoformat()

        # Same time — should NOT fire again
        self.assertFalse(self.engine._check_schedule(auto, fake_now))

    # -- keyword message checking --

    def test_check_message_keyword_match(self):
        auto = Automation(
            id="kw1",
            name="Invoice alert",
            trigger_type="keyword",
            trigger_config={"keywords": ["invoice", "payment"], "description": "test"},
            action_type="alert",
            action_config={"message": "Invoice detected"},
        )
        self.engine.automations = [auto]

        fired = self.engine.check_message("Please find the invoice attached")
        self.assertEqual(len(fired), 1)

    def test_check_message_keyword_no_match(self):
        auto = Automation(
            id="kw2",
            name="Invoice alert",
            trigger_type="keyword",
            trigger_config={"keywords": ["invoice", "payment"], "description": "test"},
            action_type="alert",
            action_config={"message": "Invoice detected"},
        )
        self.engine.automations = [auto]

        fired = self.engine.check_message("Hey, how are you?")
        self.assertEqual(len(fired), 0)

    def test_check_message_sender_filter(self):
        auto = Automation(
            id="kw3",
            name="From John",
            trigger_type="keyword",
            trigger_config={
                "keywords": ["invoice"],
                "from": "john@example.com",
                "description": "test",
            },
            action_type="alert",
            action_config={"message": "Invoice from John"},
        )
        self.engine.automations = [auto]

        # Right keyword, right sender
        fired = self.engine.check_message("Here is the invoice", sender="john@example.com")
        self.assertEqual(len(fired), 1)

        # Right keyword, wrong sender
        fired = self.engine.check_message("Here is the invoice", sender="jane@example.com")
        self.assertEqual(len(fired), 0)

        # Right keyword, no sender provided
        fired = self.engine.check_message("Here is the invoice")
        self.assertEqual(len(fired), 0)

    def test_disabled_automation_skipped(self):
        auto = Automation(
            id="dis1",
            name="Disabled",
            trigger_type="keyword",
            trigger_config={"keywords": ["test"], "description": "test"},
            action_type="message",
            action_config={"message": "hi"},
            enabled=False,
        )
        self.engine.automations = [auto]

        fired = self.engine.check_message("this is a test")
        self.assertEqual(len(fired), 0)

    # -- execution --

    def test_execute_message(self):
        import asyncio

        auto = Automation(
            id="exec1",
            name="Test message",
            trigger_type="schedule",
            trigger_config={"hour": 9, "description": "test"},
            action_type="message",
            action_config={"message": "Good morning!"},
        )

        result = asyncio.run(self.engine.execute_automation(auto, {}))
        self.assertEqual(result, "Good morning!")
        self.assertIsNotNone(auto.last_run)

    def test_execute_alert(self):
        import asyncio

        auto = Automation(
            id="exec2",
            name="Alert test",
            trigger_type="keyword",
            trigger_config={"keywords": ["urgent"], "description": "test"},
            action_type="alert",
            action_config={"message": "Deadline approaching!"},
        )

        result = asyncio.run(self.engine.execute_automation(auto, {}))
        self.assertIn("🚨", result)
        self.assertIn("Deadline approaching!", result)

    def test_execute_summary(self):
        import asyncio

        auto = Automation(
            id="exec3",
            name="Summary test",
            trigger_type="schedule",
            trigger_config={"hour": 9, "description": "test"},
            action_type="summary",
            action_config={"what": "weekly emails"},
        )

        result = asyncio.run(self.engine.execute_automation(auto, {}))
        self.assertIn("📋", result)
        self.assertIn("weekly emails", result)

    # -- condition checking with deadline files --

    def test_condition_deadline_within_days(self):
        # Create a temp deadline directory with a deadline file
        deadline_dir = os.path.join(self.tmpdir, "deadlines")
        os.makedirs(deadline_dir)

        # Deadline 2 days from now
        deadline_date = (datetime.now() + timedelta(days=2)).isoformat()
        with open(os.path.join(deadline_dir, "case1.json"), "w") as f:
            json.dump({"name": "Case 1", "deadline": deadline_date}, f)

        auto = Automation(
            id="cond1",
            name="Deadline check",
            trigger_type="condition",
            trigger_config={
                "check": "deadline_within_days",
                "days": 3,
                "source": deadline_dir,
            },
            action_type="alert",
            action_config={"message": "Deadline approaching!"},
        )
        self.engine.automations = [auto]

        now = datetime.now()
        self.assertTrue(self.engine._check_condition(auto, now))

    def test_condition_deadline_not_within_days(self):
        deadline_dir = os.path.join(self.tmpdir, "deadlines2")
        os.makedirs(deadline_dir)

        # Deadline 10 days from now
        deadline_date = (datetime.now() + timedelta(days=10)).isoformat()
        with open(os.path.join(deadline_dir, "case2.json"), "w") as f:
            json.dump({"name": "Case 2", "deadline": deadline_date}, f)

        auto = Automation(
            id="cond2",
            name="Deadline check",
            trigger_type="condition",
            trigger_config={
                "check": "deadline_within_days",
                "days": 3,
                "source": deadline_dir,
            },
            action_type="alert",
            action_config={"message": "Deadline approaching!"},
        )

        now = datetime.now()
        self.assertFalse(self.engine._check_condition(auto, now))


if __name__ == "__main__":
    unittest.main()
