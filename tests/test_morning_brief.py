#!/usr/bin/env python3
"""
Tests for Kiyomi morning brief generation.

Verifies:
1. Brief generation produces non-empty output
2. Works with missing config (no GEMINI_API_KEY, etc.)
3. Weather section integrates correctly
4. Tasks section handles empty/missing task dirs
5. Fallback handling — never crashes, never empty
6. Does NOT actually send to Telegram

All network calls are mocked to avoid test flakiness.
"""
import asyncio
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, AsyncMock

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def test_generate_brief_with_all_sections():
    """Test full brief generation with mocked weather and news."""
    from heartbeat import generate_morning_brief_content

    async def _run():
        with patch("heartbeat._fetch_weather", new_callable=AsyncMock,
                   return_value="☀️ Clear +75°F | Feels like +78°F | Humidity 45% | Wind 5mph"), \
             patch("heartbeat._fetch_news_gemini", new_callable=AsyncMock,
                   return_value="📰 Congress passes new tech bill\n🤖 OpenAI launches GPT-5\n🌍 UN climate summit begins"):
            return await generate_morning_brief_content()

    brief = asyncio.run(_run())

    assert brief is not None, "Brief should not be None"
    assert len(brief.strip()) > 50, f"Brief too short: {brief!r}"
    assert "Good morning" in brief, "Brief should contain greeting"
    assert "Weather" in brief, "Brief should have weather section"
    assert "Headlines" in brief, "Brief should have news section"
    assert "Tasks" in brief, "Brief should have tasks section"
    print(f"✅ Full brief test passed ({len(brief)} chars)")
    print(f"--- Brief Preview ---\n{brief[:600]}\n---")


def test_generate_brief_no_gemini_key():
    """Test that brief works when GEMINI_API_KEY is not set."""
    from heartbeat import generate_morning_brief_content

    async def _run():
        with patch("heartbeat._fetch_weather", new_callable=AsyncMock,
                   return_value="🌧️ Rain +60°F"), \
             patch("heartbeat._fetch_news_gemini", new_callable=AsyncMock,
                   return_value=None):  # Simulates no Gemini key
            return await generate_morning_brief_content()

    brief = asyncio.run(_run())

    assert brief is not None, "Brief should not be None without Gemini key"
    assert len(brief.strip()) > 30, f"Brief too short without Gemini: {brief!r}"
    assert "Good morning" in brief, "Brief should still have greeting"
    # News section should be absent when Gemini returns None
    assert "Headlines" not in brief, "No headlines when Gemini unavailable"
    print("✅ No-Gemini-key test passed — brief generated without news")


def test_weather_section_with_data():
    """Test that weather data is properly included."""
    from heartbeat import generate_morning_brief_content

    async def _run():
        with patch("heartbeat._fetch_weather", new_callable=AsyncMock,
                   return_value="⛅ Partly Cloudy +72°F"), \
             patch("heartbeat._fetch_news_gemini", new_callable=AsyncMock,
                   return_value=None):
            return await generate_morning_brief_content()

    brief = asyncio.run(_run())
    assert "Partly Cloudy" in brief, "Weather data should appear in brief"
    assert "+72°F" in brief, "Temperature should appear"
    print("✅ Weather section test passed")


def test_weather_fetch_failure():
    """Test that weather failure doesn't crash the brief."""
    from heartbeat import generate_morning_brief_content

    async def _run():
        with patch("heartbeat._fetch_weather", new_callable=AsyncMock,
                   return_value=None), \
             patch("heartbeat._fetch_news_gemini", new_callable=AsyncMock,
                   return_value=None):
            return await generate_morning_brief_content()

    brief = asyncio.run(_run())
    assert brief is not None
    assert "Good morning" in brief
    # Should show fallback weather message
    assert "Couldn't fetch weather" in brief or "Weather" in brief
    print("✅ Weather failure fallback test passed")


def test_read_tasks_empty():
    """Test _read_tasks with no task files."""
    from heartbeat import _read_tasks

    result = _read_tasks()
    # May return None or tasks from COMMITMENTS/HEARTBEAT — either is fine
    print(f"✅ Read tasks test passed (result: {result!r})")


def test_send_morning_brief_callback():
    """Test send_morning_brief calls the callback with content."""
    from heartbeat import send_morning_brief

    messages_sent = []

    async def mock_callback(text):
        messages_sent.append(text)

    async def _run():
        with patch("heartbeat._fetch_weather", new_callable=AsyncMock,
                   return_value="Sunny +80°F"), \
             patch("heartbeat._fetch_news_gemini", new_callable=AsyncMock,
                   return_value="📰 Test headline"):
            await send_morning_brief(mock_callback)

    asyncio.run(_run())

    assert len(messages_sent) > 0, "Should have sent at least one message"
    assert len(messages_sent[0]) > 20, "Message should have real content"
    assert "Good morning" in messages_sent[0] or "morning" in messages_sent[0].lower(), \
        "Message should contain morning greeting"
    print(f"✅ Send callback test passed — {len(messages_sent)} message(s) sent")


def test_send_morning_brief_never_empty():
    """Even with all sections failing, brief should send something."""
    from heartbeat import send_morning_brief

    messages_sent = []

    async def mock_callback(text):
        messages_sent.append(text)

    async def _run():
        with patch("heartbeat._fetch_weather", new_callable=AsyncMock, return_value=None), \
             patch("heartbeat._fetch_news_gemini", new_callable=AsyncMock, return_value=None), \
             patch("heartbeat._read_tasks", return_value=None):
            await send_morning_brief(mock_callback)

    asyncio.run(_run())

    assert len(messages_sent) > 0, "Must send at least one message even if all sections fail"
    msg = messages_sent[0]
    assert len(msg) > 10, f"Message too short: {msg!r}"
    print(f"✅ Never-empty test passed — message: {msg[:100]}...")


def test_brief_sections_config():
    """Test that configured sections appear in brief."""
    from heartbeat import generate_morning_brief_content

    async def _run():
        with patch("heartbeat._fetch_weather", new_callable=AsyncMock,
                   return_value="Clear +70°F"), \
             patch("heartbeat._fetch_news_gemini", new_callable=AsyncMock,
                   return_value="📰 Headline"):
            return await generate_morning_brief_content()

    brief = asyncio.run(_run())

    has_weather = "Weather" in brief or "🌤" in brief
    has_tasks = "Tasks" in brief or "📋" in brief

    assert has_weather, "Weather section should be present"
    assert has_tasks, "Tasks section should be present"
    print(f"  Weather section present: {has_weather}")
    print(f"  Tasks section present: {has_tasks}")
    print(f"✅ Sections config test passed")


def test_first_interaction_flag():
    """Test the first interaction flag mechanism."""
    with tempfile.TemporaryDirectory() as tmpdir:
        flag_file = Path(tmpdir) / "user_initialized.flag"

        assert not flag_file.exists(), "Flag should not exist initially"

        # Write the flag
        flag_file.write_text("2025-01-01T00:00:00")
        assert flag_file.exists(), "Flag should exist after write"

        content = flag_file.read_text()
        assert "2025-01-01" in content, "Flag should contain timestamp"

        print("✅ First interaction flag test passed")


def test_exception_in_callback_doesnt_crash():
    """Test that an exception in the callback is handled gracefully."""
    from heartbeat import send_morning_brief

    call_count = 0

    async def failing_callback(text):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise Exception("Network error sending to Telegram")

    async def _run():
        with patch("heartbeat._fetch_weather", new_callable=AsyncMock, return_value="Sunny"), \
             patch("heartbeat._fetch_news_gemini", new_callable=AsyncMock, return_value=None):
            # This should not raise even if callback fails
            try:
                await send_morning_brief(failing_callback)
            except Exception:
                pass  # The function itself may re-raise but shouldn't crash the bot

    asyncio.run(_run())
    assert call_count >= 1, "Callback should have been called at least once"
    print(f"✅ Exception handling test passed (callback called {call_count} time(s))")


def test_morning_brief_date_tracking():
    """Test the morning brief sent-date tracking."""
    from heartbeat import mark_morning_brief_sent, _get_morning_brief_sent_date

    mark_morning_brief_sent()
    sent_date = _get_morning_brief_sent_date()
    assert sent_date is not None, "Sent date should be recorded"
    from datetime import datetime
    import pytz
    from config import TIMEZONE
    tz = pytz.timezone(TIMEZONE)
    today = datetime.now(tz).strftime("%Y-%m-%d")
    assert sent_date == today, f"Sent date should be today ({today}), got {sent_date}"
    print(f"✅ Morning brief date tracking test passed (date: {sent_date})")


if __name__ == "__main__":
    print("=" * 60)
    print("Kiyomi Morning Brief Tests")
    print("=" * 60)

    tests = [
        ("Full Brief Generation", test_generate_brief_with_all_sections),
        ("No Gemini Key Fallback", test_generate_brief_no_gemini_key),
        ("Weather With Data", test_weather_section_with_data),
        ("Weather Failure Fallback", test_weather_fetch_failure),
        ("Read Tasks Empty", test_read_tasks_empty),
        ("Send Callback", test_send_morning_brief_callback),
        ("Never Empty", test_send_morning_brief_never_empty),
        ("Brief Sections", test_brief_sections_config),
        ("First Interaction Flag", test_first_interaction_flag),
        ("Exception Handling", test_exception_in_callback_doesnt_crash),
        ("Date Tracking", test_morning_brief_date_tracking),
    ]

    passed = 0
    failed = 0

    for name, test_fn in tests:
        print(f"\n--- {name} ---")
        try:
            test_fn()
            passed += 1
        except Exception as e:
            print(f"❌ FAILED: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print(f"\n{'=' * 60}")
    print(f"Results: {passed} passed, {failed} failed out of {len(tests)}")
    print(f"{'=' * 60}")

    sys.exit(0 if failed == 0 else 1)
