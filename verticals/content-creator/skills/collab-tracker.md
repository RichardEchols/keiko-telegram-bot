---
name: collab-tracker
vertical: content-creator
description: Track brand deals, sponsorships, and collaborations from pitch to payment
trigger: "brand deal|sponsorship|collaboration|collab|sponsor|brand partnership|rate card"
---

# Skill: Collaboration & Sponsorship Tracker

Manage brand deals, sponsorships, and creator collaborations from first contact to final payment.

## Deal Tracker

Location: `workspace/collabs/deals.md`

```markdown
# Active Brand Deals — [Year]

| Brand | Type | Stage | Deliverables | Rate | Due Date | Payment Status |
|-------|------|-------|-------------|------|----------|---------------|
| TechCo | Sponsored Video | 📝 Contract Signed | 1 dedicated + 2 mentions | $5,000 | Feb 15 | ⏳ Net 30 |
| ToolApp | Affiliate | ✅ Live | Ongoing mentions + link | 30% commission | Rolling | 💰 Monthly |
| StartupX | Integration | 🤝 Negotiating | 1 dedicated video | $3,000 | TBD | — |
```

## Deal Stages

```
💡 INQUIRY      → Brand reached out or you pitched
🤝 NEGOTIATING  → Discussing terms, rates, deliverables
📝 CONTRACTED   → Agreement signed, work begins
🎬 IN PROGRESS  → Creating deliverables
✅ DELIVERED     → Content published, awaiting approval
💰 INVOICED     → Invoice sent, awaiting payment
✅ PAID          → Deal complete
❌ PASSED        → Declined or fell through (log reason)
```

## Deal File Template

One file per deal at `workspace/collabs/[brand-name]-[date].md`:

```markdown
# Deal: [Brand Name] — [Campaign Name]

## Brand Contact
- Name: [rep name]
- Email: [email]
- Role: [title]

## Deal Terms
- Type: [Sponsored Video | Integration | Affiliate | Ambassador | Gifted]
- Rate: $[amount] or [commission %]
- Payment Terms: [Net 30 | Upon delivery | 50/50 split]
- Exclusivity: [None | 30-day category | Duration of contract]
- Usage Rights: [Their channels? Paid ads? Duration?]

## Deliverables
- [ ] [Deliverable 1] — due [date]
- [ ] [Deliverable 2] — due [date]
- [ ] [Deliverable 3] — due [date]

## Approval Process
- Script/outline due: [date]
- Brand review period: [X days]
- Revisions allowed: [X rounds]
- Final approval needed before publish: [Y/N]

## Content Requirements
- Key talking points: [list]
- Required phrases/disclosures: [list]
- FTC disclosure: "Paid partnership with [Brand]" / #ad
- Links/codes: [tracking URL or promo code]

## Performance
- Views: [X]
- Clicks: [X]
- Conversions: [X]
- Brand satisfaction: [feedback]
```

## Rate Card Reference

Keep your current rates in `workspace/collabs/rate-card.md`:

```markdown
# Rate Card — [Creator Name] — Updated [Date]

| Deliverable | Rate | Notes |
|------------|------|-------|
| Dedicated YouTube video (10+ min) | $[X] | Includes 1 round of revisions |
| YouTube integration (60-90 sec) | $[X] | Within existing content |
| YouTube Shorts | $[X] | Single short-form video |
| Instagram Reel | $[X] | |
| X/Twitter thread | $[X] | |
| Bundle: Video + 2 Shorts + Tweet | $[X] | 15% bundle discount |
| Affiliate (ongoing) | [X]% commission | Minimum [X] month term |

Subscribers: [X] | Avg views: [X] | Engagement rate: [X]%
Last updated: [date]
```

## Commands

- "New deal [brand name]" → Create deal file and start tracking
- "Deal status" → Show all active deals with stages
- "Invoice [brand]" → Generate invoice for completed deliverables
- "Rate card" → Show current rates
- "Update rates" → Adjust rate card based on growth
- "Collab revenue this month" → Total sponsorship income
- "Passed deals" → Review declined deals and reasons (pattern spotting)

## Rules

1. **ALWAYS include FTC disclosure** — #ad, paid partnership, or equivalent. Non-negotiable.
2. Never agree to terms without reviewing exclusivity and usage rights carefully
3. Get contracts in writing — verbal agreements are not deals
4. Track every deal even if declined — patterns in inquiries inform rate adjustments
5. Invoice within 48 hours of deliverable completion
6. Follow up on unpaid invoices at Net 30 + 7 days, then every 14 days
