---
name: billing-tracker
vertical: lawyer
description: Time tracking, invoice generation, and billing summaries
trigger: "log time|billing|billable hours|invoice|revenue|time entry|billing report|costs"
---

# Skill: Billing & Time Tracker

Track billable hours, case costs, and revenue for the firm.

## Time Entry Format

Log entries in `workspace/billing/[YYYY-MM].md`:

```markdown
# Billing — [Month Year]

## [YYYY-MM-DD]

| Time | Case # | Activity | Hours | Rate | Amount |
|------|--------|----------|-------|------|--------|
| 9:15 | 2024-0047 | Phone call with adjuster re: settlement offer | 0.3 | $350 | $105.00 |
| 10:00 | 2024-0089 | Review medical records from St. Mary's | 0.5 | $350 | $175.00 |
| 11:30 | 2024-0103 | Draft demand letter | 1.2 | $350 | $420.00 |

**Daily Total:** 2.0 hours | $700.00
```

## Commands

- "Log time [case#] [activity] [hours]" → Add billing entry
- "Today's billing" → Show today's time entries
- "Weekly billing report" → Summarize week's billable hours and revenue
- "Monthly billing report" → Full month summary by case
- "Case costs [case#]" → Show all costs advanced on a case
- "Revenue this month" → Total billed, collected, outstanding

## Billing Minimums

- Phone call: 0.1 hr (6 min)
- Email: 0.1 hr
- Letter/Correspondence: 0.2-0.5 hr
- Document Review: 0.3-1.0 hr (depends on volume)
- Research: 0.5-2.0 hr
- Deposition: actual time + 0.5 hr prep
- Court appearance: actual time + travel

## Cost Tracking

Track advanced costs in `workspace/billing/costs-[CASE-NUMBER].md`:

```markdown
# Costs Advanced — Case [NUMBER]

| Date | Description | Amount | Status |
|------|-------------|--------|--------|
| 2024-06-15 | Filing fee | $400.00 | Paid |
| 2024-07-20 | Medical records - St. Mary's | $85.00 | Paid |
| 2024-08-01 | Expert witness retainer | $2,500.00 | Paid |

**Total Costs Advanced:** $2,985.00
```

## Monthly Revenue Summary

```
💰 REVENUE REPORT — [Month Year]

Billable Hours: [X] hours
Hourly Revenue: $[amount]
Contingency Settlements: $[amount] (from [X] cases)
Total Revenue: $[amount]

Costs Advanced This Month: $[amount]
Net Revenue: $[amount]

Accounts Receivable: $[amount] (outstanding invoices)
```

## Rules

1. Round to nearest 0.1 hour (6 minutes)
2. Never bill client without attorney approval
3. Track contingency fee calculations separately
4. Costs advanced are recoverable from settlement — track them
5. Flag any case with costs exceeding $5,000
