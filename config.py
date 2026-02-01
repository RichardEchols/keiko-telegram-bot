"""
Kiyomi Engine Configuration - All credentials and settings
"""
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================
# TELEGRAM
# ============================================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_USER_IDS = [int(x) for x in json.loads(os.getenv("ALLOWED_USER_IDS", "[]"))]

# ============================================
# OWNER CONTACT INFO
# ============================================
OWNER_EMAIL = os.getenv("KIYOMI_OWNER_EMAIL", "")
OWNER_PHONE = os.getenv("KIYOMI_OWNER_PHONE", "")
TIMEZONE = os.getenv("KIYOMI_TIMEZONE", "UTC")

# ============================================
# BOT EMAIL (Gmail)
# ============================================
BOT_EMAIL = os.getenv("KIYOMI_BOT_EMAIL", "")
BOT_EMAIL_PASSWORD = os.getenv("BOT_EMAIL_PASSWORD")

# ============================================
# TWILIO (SMS)
# ============================================
TWILIO_PHONE = os.getenv("TWILIO_PHONE", "")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

# ============================================
# API KEYS
# ============================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
FAL_API_KEY = os.getenv("FAL_KEY")
GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_API_BASE = "https://api.x.ai/v1"
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_IDS = json.loads(os.getenv("ELEVENLABS_VOICE_IDS", "{}"))

# ============================================
# SUPABASE
# ============================================
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# ============================================
# PATHS
# ============================================
BASE_DIR = Path(__file__).parent
WORKSPACE_DIR = BASE_DIR / "workspace"
MEMORY_DIR = BASE_DIR / "memory"
LOGS_DIR = BASE_DIR / "logs"

# Workspace files
IDENTITY_FILE = WORKSPACE_DIR / "IDENTITY.md"
SOUL_FILE = WORKSPACE_DIR / "SOUL.md"
USER_FILE = WORKSPACE_DIR / "USER.md"
MEMORY_FILE = WORKSPACE_DIR / "MEMORY.md"
COMMITMENTS_FILE = WORKSPACE_DIR / "COMMITMENTS.md"
HEARTBEAT_FILE = WORKSPACE_DIR / "HEARTBEAT.md"
TOOLS_FILE = WORKSPACE_DIR / "TOOLS.md"

# Allowed directories
_home = str(Path.home())
ALLOWED_DIRECTORIES = json.loads(os.getenv("KIYOMI_ALLOWED_DIRS", json.dumps([f"{_home}/Documents/", f"{_home}/Desktop/", f"{_home}/Downloads/"])))

# ============================================
# SCHEDULE
# ============================================
HEARTBEAT_INTERVAL_MINUTES = 30
MORNING_BRIEF_HOUR = 8
MORNING_BRIEF_MINUTE = 30
QUIET_HOURS_START = 23  # 11 PM
QUIET_HOURS_END = 8     # 8 AM

# ============================================
# KIYOMI IDENTITY
# ============================================
BOT_NAME = os.getenv("KIYOMI_BOT_NAME", "Kiyomi")
BOT_EMOJI = os.getenv("KIYOMI_BOT_EMOJI", "✨")
OWNER_NAME = os.getenv("KIYOMI_OWNER_NAME", "")

# ============================================
# MORNING BRIEF CONFIGURATION
# ============================================
OWNER_CITY = os.getenv("KIYOMI_OWNER_CITY", "New York")
MORNING_BRIEF_SECTIONS = [s.strip() for s in os.getenv("KIYOMI_BRIEF_SECTIONS", "weather,news,tasks").split(",")]
CUSTOM_BRIEF_SECTIONS = json.loads(os.getenv("KIYOMI_CUSTOM_BRIEF_SECTIONS", "[]"))