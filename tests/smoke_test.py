#!/usr/bin/env python3
"""
Kiyomi Engine — End-to-End Smoke Test
Validates the full stack works: config, routing, imports, hygiene.
"""
import sys
import os

# Ensure the engine root is on sys.path so bare imports work
ENGINE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ENGINE_ROOT)
if ENGINE_ROOT not in sys.path:
    sys.path.insert(0, ENGINE_ROOT)

passed = 0
failed = 0


def report(ok: bool, label: str):
    global passed, failed
    if ok:
        passed += 1
        print(f"✅ {label}")
    else:
        failed += 1
        print(f"❌ {label}")


# ── Test 1: Config loads with defaults ─────────────────────────────
try:
    import config
    ok = True
    if config.BOT_NAME != 'Kiyomi':
        print(f"   BOT_NAME = {config.BOT_NAME!r}, expected 'Kiyomi'")
        ok = False
    if not isinstance(config.ALLOWED_USER_IDS, list):
        print(f"   ALLOWED_USER_IDS is {type(config.ALLOWED_USER_IDS)}, expected list")
        ok = False
    if not isinstance(config.ALLOWED_DIRECTORIES, list):
        print(f"   ALLOWED_DIRECTORIES is {type(config.ALLOWED_DIRECTORIES)}, expected list")
        ok = False
    report(ok, "Config loads with defaults")
except Exception as e:
    print(f"   Exception: {e}")
    report(False, "Config loads with defaults")


# ── Test 2: Model router classifies correctly ──────────────────────
try:
    from model_router import classify_task, select_model, TaskType

    checks = [
        (classify_task("hello") == TaskType.SIMPLE_CHAT, "hello -> SIMPLE_CHAT"),
        (classify_task("build an app") == TaskType.BUILDING, "build an app -> BUILDING"),
        (classify_task("draft an email") == TaskType.BUSINESS_WRITING, "draft an email -> BUSINESS_WRITING"),
        (classify_task("remind me at 3") == TaskType.SIMPLE_CHAT, "remind me at 3 -> SIMPLE_CHAT"),
    ]

    all_ok = True
    for ok, desc in checks:
        if not ok:
            print(f"   FAIL: {desc}")
            all_ok = False

    model = select_model(TaskType.SIMPLE_CHAT)
    if model not in ('gemini-flash', 'claude'):
        print(f"   select_model returned {model!r}, expected 'gemini-flash' or 'claude'")
        all_ok = False

    report(all_ok, "Model router classifies and routes correctly")
except Exception as e:
    print(f"   Exception: {e}")
    report(False, "Model router classifies and routes correctly")


# ── Test 3: All modules import without error ───────────────────────
try:
    import importlib

    modules = [
        'config', 'model_router', 'executor', 'corrections', 'voice',
        'swarm', 'projects', 'plugin_system', 'mcp_bridge', 'self_update',
        'heartbeat', 'monitoring', 'escalation',
    ]
    failures = []
    for mod in modules:
        try:
            importlib.import_module(mod)
        except Exception as e:
            failures.append((mod, str(e)))

    if failures:
        for mod, err in failures:
            print(f"   {mod}: {err}")
        report(False, f"All {len(modules)} modules import clean ({len(failures)} failed)")
    else:
        report(True, f"All {len(modules)} modules import clean")
except Exception as e:
    print(f"   Exception: {e}")
    report(False, "All modules import clean")


# ── Test 4: No hardcoded personal data ─────────────────────────────
try:
    import glob
    import re

    personal_patterns = [
        r'richardechols', r'richardbechols', r'8295554376',
        r'4045529941', r'sk-proj-', r'sk_[a-f0-9]{20,}',
    ]
    violations = []
    for f in glob.glob(os.path.join(ENGINE_ROOT, '*.py')):
        with open(f) as fh:
            content = fh.read()
            for pattern in personal_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    violations.append((os.path.basename(f), pattern, len(matches)))

    if violations:
        for f, pat, count in violations:
            print(f"   {f}: {count} matches for '{pat}'")
    report(len(violations) == 0, "No hardcoded personal data found")
except Exception as e:
    print(f"   Exception: {e}")
    report(False, "No hardcoded personal data found")


# ── Test 5: No Keiko references remain ─────────────────────────────
try:
    import glob
    import re

    keiko_count = 0
    keiko_files = []
    for f in glob.glob(os.path.join(ENGINE_ROOT, '*.py')):
        with open(f) as fh:
            matches = re.findall(r'\bkeiko\b', fh.read(), re.IGNORECASE)
            if matches:
                keiko_count += len(matches)
                keiko_files.append((os.path.basename(f), len(matches)))

    if keiko_files:
        for fname, cnt in keiko_files:
            print(f"   {fname}: {cnt} 'Keiko' references")
    report(keiko_count == 0, "Zero Keiko references" if keiko_count == 0 else f"{keiko_count} 'Keiko' references still exist")
except Exception as e:
    print(f"   Exception: {e}")
    report(False, "Zero Keiko references")


# ── Test 6: .env.example has all required variables ────────────────
try:
    required_vars = [
        'TELEGRAM_BOT_TOKEN', 'ALLOWED_USER_IDS', 'BOT_NAME',
        'KIYOMI_OWNER_NAME', 'KIYOMI_OWNER_CITY',
    ]
    env_example_path = os.path.join(ENGINE_ROOT, '.env.example')
    with open(env_example_path) as f:
        content = f.read()

    missing = [v for v in required_vars if v not in content]
    if missing:
        print(f"   Missing: {missing}")
    report(len(missing) == 0, f".env.example has all {len(required_vars)} required vars")
except Exception as e:
    print(f"   Exception: {e}")
    report(False, ".env.example has all required vars")


# ── Summary ────────────────────────────────────────────────────────
print("\n" + "=" * 50)
print(f"  RESULTS: {passed} passed, {failed} failed, {passed + failed} total")
print("=" * 50)
sys.exit(1 if failed else 0)
