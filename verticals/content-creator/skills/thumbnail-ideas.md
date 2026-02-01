---
name: thumbnail-ideas
vertical: content-creator
description: Generate thumbnail concepts, titles, and A/B test ideas for YouTube
trigger: "thumbnail|thumb ideas|title ideas|youtube thumbnail|click-through|CTR"
---

# Skill: Thumbnail & Title Generator

Create high-CTR thumbnails and titles using proven formulas and design principles.

## Thumbnail Brief Template

Save to `workspace/thumbnails/[YYYY-MM-DD]-[slug].md`:

```markdown
# Thumbnail Brief — [Video Title]

## Concept A (Primary)
- **Visual:** [Describe the image — what's shown, facial expression, objects]
- **Text Overlay:** [Max 4 words — large, readable at mobile size]
- **Color Scheme:** [Primary/accent colors — must contrast with YouTube red]
- **Emotion:** [Shock, curiosity, excitement, frustration, satisfaction]

## Concept B (A/B Test)
- **Visual:** [Alternative approach]
- **Text Overlay:** [Different angle]
- **Color Scheme:** [Different palette]
- **Emotion:** [Different hook]

## Title Options (pair with thumbnails)
1. [Title A — curiosity gap]
2. [Title B — specific result/number]
3. [Title C — bold claim]
4. [Title D — question format]
5. [Title E — how-to/tutorial]
```

## Thumbnail Design Principles

**The 3-Second Rule:** Viewer decides in 3 seconds. Your thumbnail must communicate ONE clear idea instantly.

### DO:
- **Faces** — Close-up with exaggerated expression (eyes wide, jaw dropped, huge smile)
- **Contrast** — Bright subject on dark background (or vice versa)
- **Big text** — 3-4 words MAX, readable on a phone screen
- **Before/After** — Split frame showing transformation
- **Arrows/Circles** — Draw eye to the key element
- **Bright colors** — Yellow, red, cyan stand out in feeds

### DON'T:
- Small text or more than 4 words
- Cluttered backgrounds
- Dark, muddy colors
- Too many elements competing
- Red/white color schemes (blends with YouTube UI)
- Clickbait that doesn't match content (kills retention)

## Title Formulas

| Formula | Example |
|---------|---------|
| Number + Adjective + Result | "5 Insane Tips That Doubled My Revenue" |
| How I + Result + Timeframe | "How I Got 100K Subs in 6 Months" |
| Why + Contrarian Take | "Why I Stopped Using React" |
| I Tried + Challenge + Result | "I Tried AI Coding for 30 Days" |
| Don't + Common Mistake | "Don't Make This Editing Mistake" |
| The Truth About + Topic | "The Truth About YouTube Shorts" |
| Question Hook | "Is This the Future of Content?" |
| X vs Y (Which Wins?) | "Final Cut vs DaVinci — Which Is Better?" |

## A/B Testing Strategy

1. Create 2 thumbnail variants for every video
2. Run primary for 48 hours, track CTR
3. If CTR < 4%, swap to variant B
4. If CTR < 4% after another 48h, redesign from scratch
5. Log results in `workspace/thumbnails/ab-test-log.md`

## Commands

- "Thumbnail for [topic]" → Generate 2 concepts + 5 title options
- "Title ideas for [topic]" → Generate 10 title variations using different formulas
- "A/B test results" → Show thumbnail swap history and CTR impact
- "Redesign thumbnail for [video]" → New concepts based on what's not working
- "What's my CTR?" → Review recent video CTR trends

## Rules

1. **Thumbnail and title must tell different parts of the same story** — don't repeat
2. Never finalize a thumbnail without a mobile-size preview check
3. Log every A/B swap with before/after CTR in the test log
4. Study competitors' top-performing thumbnails monthly
5. Refresh old video thumbnails quarterly if CTR is below channel average
