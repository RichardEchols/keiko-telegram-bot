---
name: analytics-tracker
vertical: content-creator
description: Review channel and page analytics and suggest improvements
trigger: "analytics|stats|performance|views|CTR|engagement|what's working|growth rate|revenue report"
---

# Skill: Analytics Tracker

Track content performance across platforms to inform strategy.

## Weekly Analytics File

Location: `workspace/analytics/[YYYY]-W[WW].md`

```markdown
# Analytics — Week of [Date]

## YouTube

| Video | Published | Views (7d) | CTR | Avg Watch | Likes | Comments |
|-------|-----------|-----------|-----|-----------|-------|----------|
| [title] | [date] | [X] | [X%] | [X:XX] | [X] | [X] |

**Channel Stats:**
- Subscribers: [X] (+/- from last week)
- Total views this week: [X]
- Watch time (hours): [X]
- Best performer: [title] — why: [reason]
- Worst performer: [title] — why: [reason]

## X / Twitter

| Post | Impressions | Engagements | Rate | Replies | Reposts |
|------|------------|-------------|------|---------|---------|
| [summary] | [X] | [X] | [X%] | [X] | [X] |

**Account Stats:**
- Followers: [X] (+/- from last week)
- Best post: [summary]

## Instagram

| Post | Reach | Likes | Comments | Saves | Shares |
|------|-------|-------|----------|-------|--------|
| [summary] | [X] | [X] | [X] | [X] | [X] |

## LinkedIn

| Post | Impressions | Reactions | Comments |
|------|------------|-----------|----------|
| [summary] | [X] | [X] | [X] |

## Revenue

| Source | Amount | Notes |
|--------|--------|-------|
| YouTube AdSense | $[X] | |
| Sponsors | $[X] | [sponsor name] |
| Affiliate | $[X] | [product] |
| Product sales | $[X] | [product] |
| **Total** | **$[X]** | |
```

## Commands

- "Analytics this week" → Show current week summary
- "Compare to last week" → Week-over-week comparison
- "Best content this month" → Top performers by platform
- "Revenue report" → Monthly revenue breakdown
- "Growth rate" → Subscriber/follower growth trend
- "What's working?" → Analysis of top performers with patterns

## Key Metrics to Track

**YouTube:**
- CTR (Click-through rate) — target >5%
- Average view duration — target >50% of video length
- Subscriber conversion rate
- Revenue per 1000 views (RPM)

**Social Media:**
- Engagement rate — target >3%
- Follower growth rate
- Save/share ratio (indicates high-value content)
- Reply rate (indicates conversation)

## Rules

1. Creator provides raw numbers — you organize and analyze
2. Always compare to previous period
3. Identify patterns, not just numbers ("tutorials get 2x views on Tuesdays")
4. Highlight actionable insights, not vanity metrics
5. Monthly trend analysis mandatory
