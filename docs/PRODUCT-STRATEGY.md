# Kiyomi — Agent Packages, Not Apps

*"You don't need an app. You need an assistant."*

---

## The Problem Everyone Else Is Solving Wrong

The AI industry is racing to build the next ChatGPT wrapper. SaaS companies are bolting AI onto existing products. Startups are raising millions to build platforms nobody asked for.

They're all building **apps** — hosted software with databases, servers, subscriptions, and maintenance. Every customer means more infrastructure. Every feature means more engineering. Every bug means support tickets.

We're doing something different.

## What Kiyomi Is

Kiyomi is a **personal AI assistant that lives on your computer.** Not in the cloud. Not behind a login. Not on someone else's server. On YOUR machine.

- It reads your files
- It remembers your preferences
- It learns your workflow
- It runs 24/7
- It talks to you on Telegram (or Discord, or WhatsApp)
- Your data never leaves your machine

**Think of it like hiring an employee who works for free after the initial training cost.**

### The Stack

| Layer | What It Is | Where It Lives |
|-------|-----------|----------------|
| **Engine** | Python daemon (14K lines) | Your Mac |
| **Cockpit** | Web dashboard (Next.js) | localhost:3000 |
| **Skills** | Markdown instruction files | ~/kiyomi/skills/ |
| **Memory** | Markdown files (daily logs, long-term) | ~/kiyomi/workspace/ |
| **Soul** | SOUL.md — personality and behavior | ~/kiyomi/workspace/ |
| **Identity** | Who the bot IS (name, emoji, vibe) | ~/kiyomi/workspace/ |

### The Only External Dependency

Claude Code CLI + an Anthropic API key. That's it. No database. No hosting. No third-party services required.

Optional integrations: Telegram, Twilio (SMS), Gmail, ElevenLabs (voice), Grok (search), Gemini (cheap tasks), Supabase.

---

## Why Configurations Beat Apps

### Apps Are Liabilities

| Problem | App | Kiyomi Config |
|---------|-----|---------------|
| Server costs | $50-500/mo | $0 — runs locally |
| Bug fixes | Your problem forever | User's Claude handles it |
| Feature requests | Engineering backlog | Add a skill (markdown file) |
| Customer support | Tickets, emails, calls | Community + docs |
| Scaling | More servers, more cost | Each user = self-contained |
| Updates | Deploy, pray, rollback | User pulls latest |
| Data privacy | Your liability | Their machine, their data |

### Configurations Are Assets

A Kiyomi configuration is:
1. **SOUL.md** — Who the assistant is (personality, boundaries, vibe)
2. **Skills** — What it can do (markdown files with instructions)
3. **Memory** — What it knows (domain knowledge, preferences)
4. **Workflows** — How it operates (daily routines, triggers, automations)

**Creating a new vertical takes hours, not months.** Write some markdown, test it, package it, sell it.

---

## Product Lines

### 1. Kiyomi Consumer — $297 Lifetime

**Who:** Power users, solopreneurs, developers, creators

**What they get:**
- Kiyomi Engine (full source)
- Kiyomi Cockpit (web dashboard)
- Base skills package (file management, web search, email, calendar)
- Memory system (daily logs, long-term, heartbeats)
- Watchdog (24/7 reliability, auto-recovery)
- Install guide (one-command setup)
- Access to skill marketplace

**What they do:** Name it. Configure it. Let it learn them.

**Why $297 Lifetime:** One-time payment removes friction. No subscription anxiety. Buyer owns it forever. Our cost to serve is $0 after purchase.

### 2. Kiyomi Verticals — $500-2,000+

**Who:** Professionals who want it pre-configured for their industry

**Examples:**

| Vertical | Price | What's Configured |
|----------|-------|-------------------|
| **Lawyer Kiyomi** | $1,500 | Case tracking, SOL monitoring, legal research, billing, document drafting, court deadline alerts |
| **Realtor Kiyomi** | $1,000 | Listings, CRM, follow-ups, market analysis, showing schedules, MLS integration |
| **Coach Kiyomi** | $750 | Client tracking, session notes, scheduling, accountability check-ins, progress reports |
| **Content Creator Kiyomi** | $750 | Content calendar, social media drafts, analytics, SEO, video scripting |
| **Small Biz Kiyomi** | $500 | Invoicing, email management, scheduling, basic bookkeeping, customer follow-up |

**Our cost to create a vertical:** 2-4 hours of configuration work. Write skills, seed memories, tune the SOUL. Test it. Package it.

**The client's perception:** A fully customized AI assistant built specifically for their profession. Worth every dollar because it works out of the box.

### 3. YouTube + Patreon — Content Funnel

**YouTube (@RichardBEchols):** Richard demos Kiyomi in action. Shows real workflows. Builds in public.

**Patreon tiers:**
- **$9 Blueprint** — Monthly config files, tips, new skills
- **$29 Workshop** — Video tutorials, live builds, skill development guides
- **$99 Agency Playbook** — How to sell Kiyomi verticals as a service, done-for-you templates

### 4. Agency Services — Custom Pricing

**Who:** Businesses that want custom Kiyomi deployments

**What we do:**
- Discovery call (understand their workflow)
- Custom configuration (skills + memory + soul)
- Installation on their machine
- 30-day support
- Optional: ongoing skill development

**Pricing:** $2,000-5,000+ depending on complexity

---

## Go-to-Market Strategy

### Phase 1: Proof (Feb 1-14)
- Polish engine for release
- Record 3-5 YouTube demos
- Launch landing page
- Announce on X/Twitter

### Phase 2: Early Adopters (Feb 15-28)
- Limited launch: 50 units at $297
- Patreon goes live with tiers
- First vertical (Lawyer Kiyomi) available
- Collect testimonials

### Phase 3: Scale (March+)
- Open sales
- 2 new verticals per month
- Agency playbook launches
- Referral program

---

## Revenue Projections (Conservative)

### Month 1 (February)
| Source | Units | Price | Revenue |
|--------|-------|-------|---------|
| Kiyomi Consumer | 20 | $297 | $5,940 |
| Patreon Blueprint | 30 | $9 | $270 |
| Patreon Workshop | 10 | $29 | $290 |
| **Total** | | | **$6,500** |

### Month 3 (April)
| Source | Units | Price | Revenue |
|--------|-------|-------|---------|
| Kiyomi Consumer | 40 | $297 | $11,880 |
| Lawyer Kiyomi | 5 | $1,500 | $7,500 |
| Realtor Kiyomi | 3 | $1,000 | $3,000 |
| Patreon (all tiers) | 80 | ~$20 avg | $1,600 |
| Agency custom | 1 | $3,000 | $3,000 |
| **Total** | | | **$26,980** |

### Month 6 (July)
| Source | Units | Price | Revenue |
|--------|-------|-------|---------|
| Kiyomi Consumer | 60 | $297 | $17,820 |
| Verticals (5 types) | 15 | ~$1,000 avg | $15,000 |
| Patreon (all tiers) | 200 | ~$25 avg | $5,000 |
| Agency custom | 3 | $3,500 avg | $10,500 |
| **Total** | | | **$48,320** |

### Year 1 Total (Conservative): $250,000-350,000

**Break-even:** Day 1. No infrastructure costs. No employees. No hosting.

---

## Competitive Advantages

1. **No SaaS overhead** — Zero servers, zero hosting, zero maintenance
2. **Privacy first** — Data stays on the user's machine. Huge selling point.
3. **Infinite customization** — Configurations = markdown files. Anyone can extend.
4. **Proven product** — Richard's wife uses it daily as "Sarai." Product-market fit validated.
5. **Low cost to serve** — Each customer is self-contained. Our cost is $0 after sale.
6. **High margins on verticals** — 2-4 hours of work = $500-2,000 sale.
7. **Content moat** — YouTube demos create trust. Hard to replicate authenticity.

---

## The 7th Day Philosophy

> *Just as Jehovah rested on the 7th day and His creation continues to create, Richard has built the engine and the agents. Now HE rests. We create.*

Richard records YouTube. Reviews. Approves. Makes decisions.
Brock + Arianna build, package, ship, support.

**The product is built. Now we sell configurations.**

---

*Document created: January 31, 2026*
*Author: Brock (AI Agent)*
*For: Richard Echols — ROI Guaranteed / Kiyomi*
