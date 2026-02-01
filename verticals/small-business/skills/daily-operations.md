---
name: daily-operations
vertical: small-business
description: Daily business checklist, task management, and KPI tracking
trigger: "daily checklist|morning brief|today's tasks|daily ops|open shop|close shop|KPIs"
---

# Skill: Daily Operations Manager

Structure each business day with morning setup, task management, and evening close-out.

## Daily Log

Create daily entries at `workspace/daily-logs/[YYYY-MM-DD].md`:

```markdown
# Daily Operations — [Day, Month DD, YYYY]

## Morning Open (start of day)
- [ ] Review yesterday's unfinished tasks
- [ ] Check messages/emails — flag urgent
- [ ] Review today's appointments
- [ ] Check inventory/supplies — note low items
- [ ] Review cash/register opening balance: $____
- [ ] Team assignments posted (if applicable)
- [ ] Open sign on / systems up

## Today's Priority Tasks
1. 🔴 [URGENT — must complete today]
2. 🔴 [URGENT — must complete today]
3. 🟡 [IMPORTANT — should complete today]
4. 🟡 [IMPORTANT — should complete today]
5. 🟢 [ROUTINE — complete if time allows]

## Activity Log
| Time | Activity | Notes |
|------|----------|-------|
| 9:00 | Opened | All systems normal |
| 10:30 | [activity] | [notes] |

## Daily KPIs
- Revenue: $____
- Transactions: ____
- New customers: ____
- Appointments completed: ____ / ____ scheduled
- No-shows: ____
- Customer complaints: ____

## Evening Close (end of day)
- [ ] Close register — ending balance: $____
- [ ] Reconcile: expected $____ vs actual $____ (variance: $____)
- [ ] Lock up / alarm set
- [ ] Tomorrow's prep notes:
- [ ] Unfinished tasks carried forward:
```

## Task Priority System

| Priority | Label | Rule |
|----------|-------|------|
| 🔴 Urgent | Must do today | Revenue-impacting, client-facing, deadline-bound |
| 🟡 Important | Should do today | Maintenance, follow-ups, planning |
| 🟢 Routine | When time allows | Organizing, cleaning, non-urgent admin |
| 📌 Scheduled | Specific time | Appointments, calls, deliveries |

## Weekly Operations Summary

Every Sunday evening, generate `workspace/daily-logs/week-[YYYY-WW].md`:

```markdown
# Weekly Summary — Week of [Date]

## KPI Totals
- Total Revenue: $[X] (vs last week: $[Y] | +/-[Z]%)
- Total Transactions: [X]
- New Customers: [X]
- Appointment Rate: [X]% completed
- No-Show Rate: [X]%
- Avg Revenue/Day: $[X]

## Wins This Week
- [what went well]

## Issues This Week
- [what needs attention]

## Next Week Focus
- [top 3 priorities]
```

## Commands

- "Morning brief" → Generate today's daily log with carried-forward tasks
- "Add task [description]" → Add to today's priority list
- "Today's KPIs" → Show today's numbers
- "Close out today" → Generate evening checklist
- "Weekly summary" → Generate week's operations summary
- "What's overdue?" → Show tasks carried forward more than 2 days

## Rules

1. **Morning brief happens FIRST** — before any other work
2. Never carry a 🔴 Urgent task more than 1 day without escalation
3. Log cash discrepancies immediately — even $1 matters for patterns
4. Review KPI trends weekly — don't just track, act on patterns
5. Evening close is mandatory — even on slow days
