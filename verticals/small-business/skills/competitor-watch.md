---
name: competitor-watch
vertical: small-business
description: Monitor competitors, pricing, and market trends
trigger: "competitor|competition|market research|pricing|what are they charging|SWOT|market trends"
---

# Skill: Competitor Watch

Track competitors, monitor pricing, and spot market opportunities before they do.

## Competitor Profile Template

One file per competitor at `workspace/competitors/[competitor-name].md`:

```markdown
# Competitor: [Business Name]

## Overview
- **Location:** [address]
- **Website:** [URL]
- **Social Media:** [IG/FB/X links]
- **Years in business:** [X]
- **Size:** [solo / small team / X employees]
- **Google rating:** [X.X] ★ ([X] reviews)

## Services & Pricing
| Service | Their Price | Our Price | Difference |
|---------|-----------|-----------|------------|
| [Service A] | $[X] | $[X] | [+/-$X] |
| [Service B] | $[X] | $[X] | [+/-$X] |
| [Service C] | $[X] | $[X] | [+/-$X] |

## Strengths
- [What they do well]
- [What customers praise in reviews]

## Weaknesses
- [Common complaints in reviews]
- [Gaps in their offerings]

## Recent Activity
- [YYYY-MM-DD] [New service launched / price change / expansion / etc.]

## Threat Level: [🟢 Low | 🟡 Medium | 🔴 High]
```

## Competitor Comparison Matrix

Location: `workspace/competitors/comparison.md`

```markdown
# Competitive Comparison — Updated [Date]

| Factor | Us | Competitor A | Competitor B | Competitor C |
|--------|-----|-------------|-------------|-------------|
| Price (avg service) | $[X] | $[X] | $[X] | $[X] |
| Google Rating | [X.X] ★ | [X.X] ★ | [X.X] ★ | [X.X] ★ |
| Review Count | [X] | [X] | [X] | [X] |
| Online Booking | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| Social Media Active | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| Unique Offering | [X] | [X] | [X] | [X] |
| Location Quality | [X/10] | [X/10] | [X/10] | [X/10] |
| Wait Time (avg) | [X] | [X] | [X] | [X] |
```

## SWOT Framework

Run quarterly for your own business:

```
📊 SWOT ANALYSIS — [Quarter, Year]

STRENGTHS (Internal — What we do well)
• [strength 1]
• [strength 2]
• [strength 3]

WEAKNESSES (Internal — Where we struggle)
• [weakness 1]
• [weakness 2]
• [weakness 3]

OPPORTUNITIES (External — What we can capitalize on)
• [opportunity 1] — Competitor [X] is weak here
• [opportunity 2] — Market trend toward [X]
• [opportunity 3] — Underserved customer segment

THREATS (External — What could hurt us)
• [threat 1] — New competitor opening nearby
• [threat 2] — Price pressure from [X]
• [threat 3] — Economic trend affecting customers
```

## Monthly Competitive Report

```
🔍 COMPETITIVE INTEL — [Month Year]

PRICE CHANGES DETECTED:
• [Competitor] changed [service] from $[X] to $[Y]

NEW OFFERINGS:
• [Competitor] now offers [new service/product]

REVIEW TRENDS:
• [Competitor] — rating [up/down] to [X.X] ★
• Common complaints about [Competitor]: [theme]
• Common praise for [Competitor]: [theme]

SOCIAL MEDIA ACTIVITY:
• [Competitor] posted [X] times (vs our [Y])
• Their top post: [description] — [engagement]

OPPORTUNITIES TO ACT ON:
1. [Specific action based on intel]
2. [Specific action based on intel]

OUR POSITION: [Improving | Stable | Needs Attention]
```

## Monitoring Checklist (Monthly)

```
☐ Check each competitor's Google listing and reviews
☐ Visit competitor websites — note pricing/service changes
☐ Scan their social media (last 30 days of posts)
☐ Search "[competitor name]" for news/mentions
☐ Mystery shop if appropriate (check service experience)
☐ Update comparison matrix
☐ Identify 1-2 actionable insights
```

## Commands

- "Competitor check [name]" → Pull up competitor profile
- "Price comparison" → Show comparison matrix
- "SWOT analysis" → Generate or update SWOT
- "Monthly competitive report" → Full market intelligence summary
- "New competitor [name]" → Create competitor profile
- "What are they charging for [service]?" → Quick price lookup
- "Market trends" → Summary of industry trends affecting the business

## Rules

1. **Update competitor info monthly** — stale intel is useless
2. Focus on your top 3-5 direct competitors, not every business in town
3. Never copy competitors — use intel to differentiate and find gaps
4. Price isn't everything — track quality, reviews, and customer experience
5. Share competitive insights with the owner monthly to inform strategy
6. Mystery shopping must be ethical — observe as a normal customer, don't deceive
