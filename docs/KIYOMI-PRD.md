# KIYOMI — Product Requirements Document

**Version:** 1.0 (DEFINITIVE)
**Date:** February 1, 2026
**Author:** Brock + Richard Echols
**Status:** APPROVED — Full press build

---

## The Vision

**"An AI assistant that already knows how to help you. Your computer. Your data. No setup headaches."**

Kiyomi is a pre-configured, local-first AI assistant that installs like a Mac app and works out of the box for non-technical users. She combines conversational AI (Telegram + local chat), persistent memory, pre-built business skills, and a visual dashboard — all running on the user's own machine.

### The Problem
- ChatGPT/Claude: Easy but starts blank. No memory. No skills. Cloud-only.
- ClawdBot/OpenClaw: Powerful but hard to install. Requires technical knowledge.
- Custom AI agents: Require developers to build and maintain.

### The Solution
Kiyomi fills the gap: **pre-skilled, easy install, local/private, affordable.**

### Core Differentiators
1. **Local-first** — runs on your Mac, your data never leaves your machine
2. **Pre-configured** — comes with skills and dashboard for your business vertical
3. **Persistent memory** — remembers you, your business, your preferences
4. **Telegram-native** — text her like a real assistant from your phone
5. **One-click install** — .dmg installer, no terminal ever
6. **Multi-model smart routing** — uses FREE Gemini for 80% of tasks, Claude only when needed
7. **Skills > Apps** — pre-built prompts that make Claude Code CLI build things RIGHT

---

## Target Users

### Primary: Non-technical professionals
- Lawyers, content creators, small business owners, coaches, realtors
- Age 30-70+
- "The 69-year-old dad test" — if Richard's dad can use it, anyone can
- They want an assistant, not a coding tool
- They value privacy (especially lawyers, healthcare)

### Secondary: Technical users who want pre-configuration
- Developers who don't want to configure their own agent
- Power users who want a polished experience out of the box

---

## Product Architecture

### Three Layers

```
┌──────────────────────────────────────────────┐
│           KIYOMI COCKPIT (The Face)           │
│  Mac app (.dmg) — Chat + Dashboard + Buttons  │
│  Install wizard, quick actions, voice input    │
└──────────────────┬───────────────────────────┘
                   │
┌──────────────────┴───────────────────────────┐
│           KIYOMI ENGINE (The Brain)           │
│  Telegram bot + Skills + Memory + Watchdog    │
│  Multi-model routing + Proactive behaviors    │
└──────────────────┬───────────────────────────┘
                   │
┌──────────────────┴───────────────────────────┐
│         VERTICAL TEMPLATES (The Job)          │
│  Skills + Dashboard layout + Quick actions    │
│  Pre-built prompts + Memory scaffolding       │
│  Lawyer / Content Creator / Small Business    │
└──────────────────────────────────────────────┘
```

---

## Install Experience (5 minutes, "Dad Test" compliant)

### Distribution
- **Kiyomi.dmg** — standard Mac installer
- Drag to Applications → double-click → GUI wizard opens
- NO terminal. NO command line. EVER.

### Install Wizard Flow

**Step 1: "Welcome! What's your name?"**
→ Text field
→ Personalizes Kiyomi's greeting and memory

**Step 2: "What do you do?"**
→ Big visual cards to pick:
  - ⚖️ Lawyer
  - 🎨 Content Creator
  - 🏪 Small Business
  - ⚙️ Custom (blank slate)
→ Loads the vertical template (skills, dashboard, quick actions)

**Step 3: "Let's give Kiyomi her brain! 🧠"**
→ "We need a free key from Google. I'll open the page for you."
→ Opens Google AI Studio in browser
→ "See the long code? Click 'Copy' then come back and click this big green button:"
→ **[PASTE MY KEY]** (big green button)
→ ✅ "Perfect! Kiyomi can think now."
→ This is the ONLY required API step. Gemini free tier. $0/month.

**Step 4 (OPTIONAL): "Want Kiyomi to build things for you?"**
→ "This lets Kiyomi create reports, dashboards, and documents."
→ "It requires a Claude account (~$20/month)"
→ Opens Anthropic console → guided key paste
→ **[SKIP FOR NOW]** button always visible
→ Most users skip. Power users add later.

**Step 5 (OPTIONAL): "Want Kiyomi on your phone?"**
→ "Connect to Telegram for mobile access"
→ Walks through BotFather
→ **[SKIP — JUST USE THE APP]** button
→ Default: Cockpit only. Telegram is a bonus.

**Step 6: "You're all set!"**
→ Kiyomi launches
→ First-run tutorial: 3-minute walkthrough
→ "Try saying 'Good morning' to me!"

---

## Multi-Model Smart Routing (CRITICAL for affordability)

### The Problem
Claude Max = $100/month. That kills the consumer price point.

### The Solution
Kiyomi routes each task to the cheapest model that can handle it.

| Task Type | Model | User Cost |
|-----------|-------|-----------|
| Chat, greetings, simple Q&A | Gemini Flash (free tier) | $0 |
| Memory recall, schedule, lookups | Gemini Flash (free tier) | $0 |
| Skill execution (templates) | Gemini Flash/Pro | $0-5/mo |
| Business writing, analysis | Gemini Pro or Claude Sonnet | $5-20/mo |
| Building reports, apps, dashboards | Claude Code CLI | $20/mo (Pro) |

### Routing Logic
```python
def route_task(task):
    if task.is_simple_chat or task.is_memory_lookup:
        return "gemini-flash"  # FREE
    elif task.is_skill_execution:
        return "gemini-pro"    # CHEAP
    elif task.is_complex_writing:
        return user_preferred_model  # Their choice
    elif task.is_building:
        if claude_key_available:
            return "claude-code-cli"
        else:
            return "gemini-pro"  # Fallback, less capable but works
```

### User Cost Tiers

| Tier | What Works | Monthly AI Cost |
|------|-----------|----------------|
| **Free** | Chat, memory, skills, dashboards, quick actions | $0 (Gemini free) |
| **Plus** | + complex writing, better analysis | $10-20 (Gemini paid or Claude Pro) |
| **Builder** | + builds apps, custom reports, full CLI power | $20 (Claude Pro) |

**Most users will be on the Free tier.** This is the key selling point.

---

## Kiyomi Cockpit (The Face)

### Layout
```
┌─────────────────────────────────────────────┐
│  🟢 Kiyomi — [Vertical Name]      ⚙️  🔔  │
├──────────────────┬──────────────────────────┤
│                  │                          │
│   CHAT PANEL     │    DASHBOARD PANEL       │
│                  │                          │
│  [Chat history]  │  [Quick Action Buttons]  │
│                  │  🔵 Good Morning         │
│                  │  🔵 Show Schedule        │
│                  │  🔵 Write a Letter       │
│  [Voice 🎤]     │  🔵 Monthly Report       │
│                  │                          │
│  [Type here...]  │  [Business Dashboard]    │
│                  │  - Cards / Lists / Data  │
│                  │  - Saved Reports         │
│                  │                          │
└──────────────────┴──────────────────────────┘
```

### Quick Action Buttons
Pre-built per vertical. Big, colorful, one-tap:

**Lawyer Kiyomi:**
- 🔵 Case Overview
- 🔵 SOL Deadlines
- 🔵 Draft Demand Letter
- 🔵 Billing Summary
- 🔵 Monthly Report

**Content Creator Kiyomi:**
- 🔵 Content Calendar
- 🔵 Write a Post
- 🔵 Analytics Snapshot
- 🔵 Script Ideas
- 🔵 Schedule Content

**Small Business Kiyomi:**
- 🔵 Today's Appointments
- 🔵 Revenue This Month
- 🔵 Send Reminder
- 🔵 Customer List
- 🔵 Monthly Report

### Dashboard Templates
Each vertical gets a pre-built dashboard layout:
- Cards with key metrics
- Lists with actionable items
- Color-coded status indicators
- All populated by Kiyomi's skills and memory
- Saveable as reports (PDF/HTML files)

### Voice Input
- Big microphone button in chat panel
- Whisper/native speech-to-text
- Kiyomi can read responses aloud (ElevenLabs TTS optional)
- Ideal for older/non-technical users

### Error Messages
- Never show technical errors
- "I can't think right now — my brain key might have expired. Want me to help you fix it?"
- Always offer a solution, never just an error

### Auto-Updates
- Silent background checks
- One-click update prompt: "I have an update! Install now?"
- No terminal, no git pull, no manual steps

---

## Skills Architecture (The Secret Sauce)

### What Skills Do
Skills are pre-written instruction sets that tell Kiyomi (and Claude Code CLI) EXACTLY how to perform a task. The user never writes a prompt. The skill IS the prompt engineering.

### User Experience
1. User presses "Monthly Report" button (or types "monthly report")
2. Kiyomi's `monthly-report` skill activates
3. Skill gathers data from memory files
4. If simple: Gemini formats a report (free)
5. If complex: Claude Code CLI builds an HTML report (paid tier)
6. Output saved as file, displayed in dashboard
7. User sees a beautiful report. Never touched code.

### Skill Structure (per vertical)
```
verticals/lawyer/
├── SOUL.md              # Kiyomi's personality for lawyers
├── IDENTITY.md          # "I'm your legal assistant"
├── USER.md              # Template for lawyer's info
├── COMMITMENTS.md       # Daily routines for legal practice
├── skills/
│   ├── case-tracker/    # Track cases, deadlines, status
│   ├── sol-monitor/     # Statute of limitations alerts
│   ├── demand-letter/   # Draft demand letters
│   ├── billing-tracker/ # Track hours, invoices
│   ├── legal-research/  # Research case law
│   └── monthly-report/  # Generate monthly case report
├── dashboard/
│   └── template.json    # Dashboard layout for lawyers
└── quick-actions/
    └── actions.json     # Button definitions
```

### Pre-built Prompts in Skills
Each skill contains the exact prompts that make Claude Code CLI build things correctly:
```markdown
# monthly-report SKILL.md

When the user asks for a monthly report:
1. Read all case files from memory/cases/
2. Compile: active cases, closed cases, SOL deadlines approaching
3. Generate an HTML report using this template: [exact template]
4. Save to reports/YYYY-MM-monthly-report.html
5. Display in dashboard panel
6. Tell user: "Your January report is ready! 📊"
```

---

## Telegram Integration (Optional, phone access)

### How It Works
- Kiyomi runs a Telegram bot locally
- User texts Kiyomi from their phone, anywhere
- Same skills, same memory, same personality
- Dashboard features: "Show me my cases" → Kiyomi sends a formatted summary
- Quick actions available as Telegram command buttons

### Not Required
- Cockpit is the primary interface
- Telegram adds mobile convenience
- Setup is optional in the install wizard

---

## Pricing

### Consumer
- **$297 one-time** — Kiyomi Engine + Cockpit + one vertical template
- AI cost to user: $0/month (Gemini free tier handles 80%)
- Optional: Claude Pro $20/month for building features

### Vertical Add-ons
- **$49 each** — additional vertical templates
- Or bundled: 3 templates for $99

### Agency/Custom Configuration
- **$500-2,000** — Richard personally configures Kiyomi for a specific business
- Includes: custom skills, custom dashboard, custom quick actions, onboarding call
- This is the premium service, not the core product

---

## Revenue Projections

### Conservative (Month 1-3)
- 20 sales × $297 = $5,940
- 5 verticals × $49 = $245
- 2 agency configs × $1,000 = $2,000
- **Monthly: ~$2,700**

### Growth (Month 4-6)
- 50 sales/month × $297 = $14,850
- Vertical add-ons: $1,000
- Agency: $3,000
- **Monthly: ~$6,300**

### Scale (Month 7-12)
- YouTube + word of mouth driving 100+ sales/month
- Vertical marketplace with community contributors
- **Monthly: $15,000-30,000+**

---

## Technical Requirements (Build Priorities)

### P0 — Must Have for Launch
1. **Multi-model routing** — Gemini free tier as default, Claude optional
2. **.dmg installer** — Mac app, no terminal
3. **Install wizard GUI** — 5-minute, dad-test compliant
4. **Remove hardcoded personal data** — config.py cleanup
5. **Cockpit redesign** — chat panel + dashboard panel + quick actions
6. **One vertical template complete** — Lawyer (already started)
7. **First-run tutorial** — 3-minute interactive walkthrough
8. **Skills execution on Gemini** — most skills must work without Claude

### P1 — Should Have for Launch
9. **Voice input** — microphone button, speech-to-text
10. **Report saving** — export dashboard views as PDF/HTML
11. **Auto-update mechanism** — silent background updates
12. **Error messages in plain English** — no technical jargon
13. **Second vertical template** — Content Creator
14. **Telegram integration** — optional phone access

### P2 — Nice to Have (Post-Launch)
15. **Third vertical** — Small Business
16. **Kiyomi Skills Marketplace** — community skills
17. **Config Wizard web tool** — auto-generate verticals
18. **Windows support** — expand beyond Mac
19. **Voice output** — ElevenLabs TTS responses

---

## Build Plan (Feb 1 → Feb 14 Sprint)

### Week 1 (Feb 1-7): Foundation
- [ ] Multi-model routing in engine (Gemini default)
- [ ] Remove all hardcoded personal data
- [ ] Cockpit redesign with chat + dashboard layout
- [ ] Install wizard GUI (Electron or native Swift wrapper)
- [ ] Lawyer vertical skills completion
- [ ] Quick action buttons system

### Week 2 (Feb 8-14): Polish & Package
- [ ] .dmg packaging and installer
- [ ] First-run tutorial
- [ ] Error message humanization
- [ ] Voice input integration
- [ ] Report save/export
- [ ] Testing (the wife test + the dad test)
- [ ] Landing page
- [ ] Launch video for @RichardBEchols

---

## Marketing & Launch

### Positioning
"You don't need an app. You need an assistant."

### Launch Channel
1. @RichardBEchols YouTube video: "I Built an AI Employee That Costs $0/Month to Run"
2. Patreon early access for existing members
3. Product Hunt launch
4. Twitter/X announcement

### Key Selling Points
- ✅ Installs in 5 minutes
- ✅ Runs on YOUR computer (privacy)
- ✅ $0/month AI costs (Gemini free tier)
- ✅ Pre-configured for your business
- ✅ Remembers everything
- ✅ No technical knowledge needed
- ✅ One-time purchase, no subscription

### YouTube Content Plan
1. "I Built an AI Employee That Replaced All My Apps" (launch video)
2. "Watch My 69-Year-Old Dad Install an AI Assistant" (demo/proof)
3. "Lawyer AI Assistant in 5 Minutes" (vertical demo)
4. "Why I Stopped Building Apps" (philosophy/story)

---

## Success Metrics

- **Install completion rate** > 90% (wizard must be THAT easy)
- **Day 1 engagement** > 80% (first-run tutorial hooks them)
- **Week 1 retention** > 60% (skills provide real daily value)
- **Refund rate** < 5%
- **NPS** > 50

---

## What This Replaces

- RE LawManager app → Lawyer Kiyomi (same features, no infrastructure)
- JWx app → Richard's personal Kiyomi (already replaced by Brock/Sarai)
- 11 GitHub repos → all replaced by Kiyomi configurations
- Monthly hosting/maintenance → $0 (runs locally)

---

*"He rested on the seventh day. His creation continues to create."*
*— The 7th Day Model*

---

**APPROVED by Richard Echols — February 1, 2026**
**BUILT by Brock + Arianna + Gemini + Codex**
