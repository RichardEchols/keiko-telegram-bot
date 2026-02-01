# Kiyomi Install Wizard Spec

## Overview
A GUI installer that takes a non-technical user from download to "Hi Kiyomi" in under 5 minutes.
Must pass the "69-year-old dad test" — no terminal, no jargon, no confusion.

## Distribution
- **Kiyomi.dmg** for macOS
- Electron app wrapping the Kiyomi Cockpit (Next.js)
- Installer bundles: Node.js runtime, Python runtime, Kiyomi Engine, Kiyomi Cockpit
- Auto-installs dependencies silently in background

## Wizard Flow (5 Steps)

### Step 1: Welcome
```
┌──────────────────────────────────────┐
│                                      │
│         ✨ Welcome to Kiyomi         │
│                                      │
│   Your AI assistant that already     │
│   knows how to help you.             │
│                                      │
│   Let's get you set up in just       │
│   a few minutes!                     │
│                                      │
│       [What's your name?]            │
│       ┌─────────────────────┐        │
│       │                     │        │
│       └─────────────────────┘        │
│                                      │
│              [Next →]                │
│                                      │
└──────────────────────────────────────┘
```
- Text input for user's first name
- Stored in USER.md and .env as KIYOMI_OWNER_NAME
- Friendly, warm, non-technical tone

### Step 2: Choose Your Kiyomi
```
┌──────────────────────────────────────┐
│                                      │
│      What do you do? ✨              │
│                                      │
│   Pick a template, or start fresh:   │
│                                      │
│   ┌──────────┐  ┌──────────┐        │
│   │  ⚖️      │  │  🎨      │        │
│   │ Lawyer   │  │ Content  │        │
│   │          │  │ Creator  │        │
│   └──────────┘  └──────────┘        │
│                                      │
│   ┌──────────┐  ┌──────────┐        │
│   │  🏪      │  │  ⚙️      │        │
│   │ Small    │  │ Custom   │        │
│   │ Business │  │ (blank)  │        │
│   └──────────┘  └──────────┘        │
│                                      │
│     [← Back]         [Next →]       │
│                                      │
└──────────────────────────────────────┘
```
- Large visual cards (not a dropdown)
- Each card has icon + name + 1-line description
- Selecting loads: skills, dashboard template, quick actions, SOUL.md personality
- "Custom" starts with a blank Kiyomi — all general skills, no vertical

### Step 3: Give Kiyomi a Brain
```
┌──────────────────────────────────────┐
│                                      │
│   Let's give Kiyomi her brain! 🧠   │
│                                      │
│   We need a free key from Google     │
│   so Kiyomi can think.               │
│                                      │
│   It takes about 30 seconds:         │
│                                      │
│   1. Click the button below          │
│   2. Sign in with your Google account│
│   3. Click "Create API Key"          │
│   4. Click "Copy"                    │
│   5. Come back here and paste it     │
│                                      │
│   [🔗 Open Google AI Studio]         │
│                                      │
│   ┌─────────────────────────┐        │
│   │ Paste your key here...  │        │
│   └─────────────────────────┘        │
│                                      │
│   [PASTE MY KEY]  ← big green button │
│                                      │
│   ✅ Key verified! Kiyomi can think. │
│                                      │
│     [← Back]         [Next →]       │
│                                      │
└──────────────────────────────────────┘
```
- Opens https://aistudio.google.com/app/apikey in browser
- Validates key by making a test API call
- Green checkmark when verified
- If invalid: "Hmm, that doesn't look right. Try copying it again?"
- This is the ONLY required technical step

### Step 4: Optional Upgrades
```
┌──────────────────────────────────────┐
│                                      │
│   Want superpowers? (Optional) ⚡    │
│                                      │
│   These are optional upgrades.       │
│   Kiyomi works great without them!   │
│                                      │
│   ┌──────────────────────────┐       │
│   │ 🔨 Builder Mode          │       │
│   │ Let Kiyomi build reports, │       │
│   │ apps, and documents.      │       │
│   │ Requires Claude ($20/mo)  │       │
│   │ [Set up] [Skip]          │       │
│   └──────────────────────────┘       │
│                                      │
│   ┌──────────────────────────┐       │
│   │ 📱 Mobile Access          │       │
│   │ Text Kiyomi from your     │       │
│   │ phone via Telegram.       │       │
│   │ [Set up] [Skip]          │       │
│   └──────────────────────────┘       │
│                                      │
│   ┌──────────────────────────┐       │
│   │ 🎤 Voice Mode             │       │
│   │ Talk to Kiyomi instead    │       │
│   │ of typing.                │       │
│   │ [Enable] [Skip]          │       │
│   └──────────────────────────┘       │
│                                      │
│     [← Back]      [Skip All →]      │
│                                      │
└──────────────────────────────────────┘
```
- Each upgrade is independently skippable
- "Skip All" always visible — no pressure
- Builder Mode: opens Anthropic console for Claude API key
- Mobile Access: walks through Telegram BotFather
- Voice Mode: enables built-in speech-to-text (no setup needed on Mac)

### Step 5: Ready!
```
┌──────────────────────────────────────┐
│                                      │
│        🎉 You're all set!            │
│                                      │
│   Kiyomi is ready to help you.       │
│                                      │
│   ┌──────────────────────────┐       │
│   │                          │       │
│   │  "Hi [Name]! I'm Kiyomi,│       │
│   │   your [vertical] asst.  │       │
│   │   What can I help with?" │       │
│   │                          │       │
│   └──────────────────────────┘       │
│                                      │
│   Try asking me:                     │
│   • "Good morning"                   │
│   • "What can you do?"              │
│   • "Show me my dashboard"          │
│                                      │
│          [Start Using Kiyomi →]      │
│                                      │
└──────────────────────────────────────┘
```
- Shows Kiyomi's first message (pre-loaded)
- Suggests starter prompts
- Transitions into the Cockpit with first-run tutorial

## Technical Implementation

### Approach: Electron + React
- The Cockpit is already Next.js
- Wrap in Electron for .dmg distribution
- Install wizard is a set of React components (WizardStep1, WizardStep2, etc.)
- Wizard state stored in localStorage
- On completion, writes .env file and starts Kiyomi Engine daemon

### What the Wizard Does Behind the Scenes
1. Creates `~/kiyomi/` directory
2. Copies engine files to `~/kiyomi/engine/`
3. Copies selected vertical template to `~/kiyomi/skills/`
4. Writes `.env` with user's API keys
5. Writes `USER.md` with user's name
6. Installs Python dependencies silently
7. Starts Kiyomi Engine daemon (launchd on macOS)
8. Opens Cockpit app

### Dependency Bundling
The .dmg should bundle:
- Python 3.11+ (embedded, not system Python)
- Node.js 20+ (for Cockpit)
- All pip dependencies pre-installed
- All npm dependencies pre-built

User should NEVER see a terminal, a pip install, or an npm error.

## Error Handling
- All errors shown in plain English
- "Something went wrong" + friendly explanation
- "Try again" button always available
- Support link/email for stuck users
- Diagnostic log saved to ~/kiyomi/logs/install.log (for support)
