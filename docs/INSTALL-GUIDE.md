# Kiyomi — Installation Guide

*From zero to AI assistant in 10 minutes.*

---

## Prerequisites

- **Mac** (macOS 13+ recommended)
- **Python 3.11+** (`python3 --version`)
- **Claude Code CLI** (from Anthropic)
- **Anthropic API key** (or Claude Max subscription)
- **Telegram account** (for messaging — other platforms coming soon)

### Get Claude Code CLI
```bash
# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Authenticate
claude login
```

### Get a Telegram Bot Token
1. Open Telegram, search for `@BotFather`
2. Send `/newbot`
3. Follow prompts to name your bot
4. Copy the bot token (looks like `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

---

## Quick Install

```bash
# 1. Clone Kiyomi
git clone https://github.com/RichardEchols/kiyomi-engine.git ~/kiyomi
cd ~/kiyomi

# 2. Set up Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
nano .env  # Fill in your tokens and keys

# 4. Set up workspace
cp -r workspace/templates/* workspace/

# 5. Personalize
nano workspace/IDENTITY.md  # Name your assistant
nano workspace/USER.md       # Tell it about yourself
nano workspace/SOUL.md       # Customize personality (optional)

# 6. Test run
python3 main.py

# 7. Set up 24/7 operation (see below)
```

---

## Environment Variables (.env)

```bash
# REQUIRED
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
ALLOWED_USER_IDS=[your_telegram_user_id]

# OPTIONAL — Enable as needed
# GEMINI_API_KEY=your_gemini_key          # Cheap research tasks
# RESEND_API_KEY=your_resend_key          # Email sending
# TWILIO_ACCOUNT_SID=your_sid             # SMS
# TWILIO_AUTH_TOKEN=your_token
# TWILIO_PHONE=+1XXXXXXXXXX
# ELEVENLABS_API_KEY=your_key             # Voice/TTS
# GROK_API_KEY=your_key                   # X/Twitter search
# SUPABASE_URL=your_url                   # Cloud database
# SUPABASE_ANON_KEY=your_key
```

### Finding Your Telegram User ID
1. Open Telegram, search for `@userinfobot`
2. Send `/start`
3. It replies with your user ID (a number like `8295554376`)

---

## 24/7 Operation (LaunchAgent)

Make Kiyomi start automatically and stay running:

```bash
# Create the LaunchAgent
cat > ~/Library/LaunchAgents/com.kiyomi.engine.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.kiyomi.engine</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/YOUR_USERNAME/kiyomi/venv/bin/python3</string>
        <string>/Users/YOUR_USERNAME/kiyomi/main.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/YOUR_USERNAME/kiyomi</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/YOUR_USERNAME/kiyomi/logs/kiyomi.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/YOUR_USERNAME/kiyomi/logs/kiyomi-error.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/Users/YOUR_USERNAME/kiyomi/venv/bin</string>
    </dict>
</dict>
</plist>
EOF

# Replace YOUR_USERNAME with your actual username
sed -i '' "s/YOUR_USERNAME/$(whoami)/g" ~/Library/LaunchAgents/com.kiyomi.engine.plist

# Load and start
launchctl load ~/Library/LaunchAgents/com.kiyomi.engine.plist
launchctl start com.kiyomi.engine
```

### Managing Kiyomi

```bash
# Check if running
launchctl list | grep kiyomi

# Stop
launchctl stop com.kiyomi.engine

# Start
launchctl start com.kiyomi.engine

# View logs
tail -f ~/kiyomi/logs/kiyomi.log
```

---

## Installing a Vertical (Optional)

If you purchased a vertical configuration (Lawyer, Realtor, Coach, etc.):

```bash
# Copy vertical files to your workspace
cp -r verticals/[your-vertical]/* ~/kiyomi/workspace/
cp verticals/[your-vertical]/skills/* ~/kiyomi/skills/

# Restart
launchctl stop com.kiyomi.engine
launchctl start com.kiyomi.engine
```

---

## The Cockpit (Web Dashboard)

Kiyomi Cockpit gives you a web interface to manage your assistant:

```bash
# In a separate terminal
cd ~/kiyomi-cockpit
npm install
npm run dev

# Open http://localhost:3000
```

Features:
- Terminal view (see what your assistant is doing)
- Chat interface (talk to it from your browser)
- File upload
- Voice recording
- Session management
- Activity dashboard

---

## Troubleshooting

### "Bot not responding"
```bash
# Check if process is running
ps aux | grep kiyomi

# Check logs
tail -50 ~/kiyomi/logs/kiyomi-error.log

# Restart
launchctl stop com.kiyomi.engine
launchctl start com.kiyomi.engine
```

### "Permission denied"
```bash
# Fix file permissions
chmod +x ~/kiyomi/main.py
chmod -R 755 ~/kiyomi/
```

### "Module not found"
```bash
# Reinstall dependencies
cd ~/kiyomi
source venv/bin/activate
pip install -r requirements.txt
```

---

## Getting Help

- **Email:** support@roiguaranteed.com
- **Community:** [Discord/Forum link TBD]
- **Documentation:** [docs link TBD]

---

*Welcome to the future of personal AI. Your assistant is ready.*
