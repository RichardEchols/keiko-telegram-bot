---
name: invoicing
vertical: small-business
description: Track invoices, payments, and accounts receivable
trigger: "invoice|new invoice|mark paid|overdue|AR report|revenue this month|accounts receivable"
---

# Skill: Invoice & Payment Tracker

Track invoices, payments, and accounts receivable. Simple. Reliable.

## Invoice Log

Location: `workspace/invoices/[YYYY].md`

```markdown
# Invoices — [Year]

| # | Date | Client | Description | Amount | Status | Paid Date |
|---|------|--------|-------------|--------|--------|-----------|
| 001 | Jan 5 | Smith Co | Monthly retainer - Jan | $2,500 | ✅ Paid | Jan 8 |
| 002 | Jan 5 | Jones LLC | Website project (2/3) | $3,000 | ⏳ Sent | — |
| 003 | Jan 15 | Davis Inc | Consulting (5 hrs) | $750 | 🔴 Overdue | — |
```

## Status Legend
- 📝 Draft
- ✉️ Sent
- ⏳ Pending (< 30 days)
- 🔴 Overdue (> 30 days)
- ✅ Paid
- ❌ Written off

## Overdue Follow-Up Schedule

| Days Overdue | Action |
|-------------|--------|
| 7 days | Friendly reminder email |
| 14 days | Phone call + email |
| 30 days | Formal notice |
| 45 days | Final notice |
| 60 days | Collection decision |

## Commands

- "New invoice [client] [amount] [description]" → Create invoice entry
- "Mark paid [invoice #]" → Update status
- "Overdue invoices" → List all unpaid past due
- "AR report" → Full accounts receivable summary
- "Revenue this month" → Total invoiced and collected
- "Client balance [name]" → What do they owe?

## Monthly Summary Format

```
💰 INVOICE SUMMARY — [Month Year]

Invoiced: $[total sent]
Collected: $[total paid]
Outstanding: $[total unpaid]
Overdue: $[total past 30 days]

Top clients by revenue:
1. [Client A] — $[amount]
2. [Client B] — $[amount]
3. [Client C] — $[amount]
```

## Rules

1. Invoice immediately upon delivery — don't delay
2. Payment terms: Net 30 unless otherwise agreed
3. Flag ANY invoice overdue > 14 days
4. Monthly AR review mandatory
5. Track write-offs separately for tax purposes
