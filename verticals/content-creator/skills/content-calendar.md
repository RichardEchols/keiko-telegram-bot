---
name: content-calendar
vertical: content-creator
description: Plan and schedule content across all platforms
trigger: "calendar|content plan|schedule|what's planned|content pipeline|this week's content"
---

# Skill: Content Calendar Manager

Maintain a rolling content calendar across all platforms.

## Calendar File

Location: `workspace/content-calendar.md`

```markdown
# Content Calendar — [Month Year]

## Week of [Date]

| Day | Platform | Type | Title/Topic | Status | Scheduled |
|-----|----------|------|-------------|--------|-----------|
| Mon | YouTube | Long-form | "Building X in 30 min" | 📝 Script ready | Feb 3 @ 12pm |
| Tue | X/Twitter | Thread | 5 lessons from building X | 🔄 Drafted | Feb 4 @ 9am |
| Wed | YouTube | Short | Quick tip: Y feature | ⏳ Filming needed | — |
| Thu | LinkedIn | Post | Behind the scenes: Z | 💡 Idea only | — |
| Fri | YouTube | Long-form | "Why I switched to..." | 📝 Script ready | Feb 7 @ 12pm |
| Sat | Instagram | Reel | Build montage | ⏳ Editing needed | — |
| Sun | — | Rest | — | — | — |
```

## Status Legend
- 💡 Idea only
- 📝 Script/draft ready
- ⏳ Needs filming/recording
- 🎬 Filmed, needs editing
- ✅ Ready to publish
- 🔄 Drafted, needs review
- 📤 Published
- 📌 Scheduled

## Commands

- "Calendar this week" → Show current week's content plan
- "Calendar next week" → Show upcoming
- "Add to calendar [day] [platform] [topic]" → Add entry
- "Content pipeline" → Show all items by status
- "What needs filming?" → List items in ⏳ status
- "What's ready to publish?" → List items in ✅ status

## Rules

1. Always maintain 2 weeks of planned content
2. Long-form YouTube = minimum 2 per week
3. Short-form = minimum 3 per week
4. Written posts = daily if possible
5. Creator gets final say on all scheduling
