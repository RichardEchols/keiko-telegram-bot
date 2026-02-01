---
name: expense-tracker
vertical: small-business
description: Track business expenses, categorize by IRS category, and generate tax-ready reports
trigger: "expense|spent|receipt|business cost|tax deduction|expense report|how much did I spend"
---

# Skill: Business Expense Tracker

Track every business expense with IRS-compliant categorization for clean bookkeeping and tax prep.

## Expense Log

Location: `workspace/expenses/[YYYY-MM].md`

```markdown
# Business Expenses — [Month Year]

| Date | Vendor | Description | Category | Amount | Payment | Receipt | Tax Deductible |
|------|--------|-------------|----------|--------|---------|---------|---------------|
| Feb 1 | Staples | Printer paper, toner | Office Supplies | $87.45 | Biz Visa | ✅ | ✅ |
| Feb 2 | AT&T | Business phone line | Utilities/Phone | $125.00 | Auto-pay | ✅ | ✅ |
| Feb 3 | Uber | Client meeting downtown | Travel | $23.50 | Personal (reimburse) | ✅ | ✅ |
| Feb 5 | GoDaddy | Domain renewal | Software/Web | $18.99 | Biz Visa | ✅ | ✅ |

**Monthly Total:** $254.94
**Tax Deductible Total:** $254.94
```

## IRS Expense Categories

| Category | Examples | Schedule C Line |
|----------|----------|----------------|
| Advertising | Google Ads, flyers, business cards, social media ads | Line 8 |
| Car & Truck | Mileage, gas, insurance, maintenance (biz use %) | Line 9 |
| Insurance | Business liability, workers comp, E&O | Line 15 |
| Legal & Professional | Attorney, CPA, bookkeeper fees | Line 17 |
| Office Supplies | Paper, pens, toner, desk supplies | Line 18 |
| Rent | Office/shop rent, storage unit | Line 20b |
| Software/Web | SaaS subscriptions, hosting, domains | Line 18/27 |
| Utilities/Phone | Electric, water, internet, phone | Line 25 |
| Travel | Flights, hotels, Uber/Lyft for business | Line 24a |
| Meals | Business meals (50% deductible) | Line 24b |
| Equipment | Tools, machinery, computers (may depreciate) | Line 13/22 |
| Contractors | 1099 payments, freelancers | Line 11 |
| Education | Courses, books, conferences (biz-related) | Line 27 |

## Receipt Tracking

```
📎 RECEIPT RULES:
- Photograph/scan EVERY receipt over $25
- Store in workspace/expenses/receipts/[YYYY-MM]/
- Name format: [YYYY-MM-DD]-[vendor]-[amount].jpg
- For digital purchases, save email confirmation
- Keep receipts for 7 years (IRS requirement)
```

## Monthly Summary

Generate at end of each month:

```
💰 EXPENSE SUMMARY — [Month Year]

Total Expenses: $[X,XXX.XX]
Tax Deductible: $[X,XXX.XX]
Non-Deductible: $[XXX.XX]

By Category:
  Rent/Lease:           $[X,XXX.XX]  (XX%)
  Utilities:            $[XXX.XX]    (XX%)
  Supplies:             $[XXX.XX]    (XX%)
  Software:             $[XXX.XX]    (XX%)
  Advertising:          $[XXX.XX]    (XX%)
  [Other categories...] $[XXX.XX]    (XX%)

vs Last Month: +/- $[X,XXX.XX] ([X]%)
vs Budget: $[over/under] ([X]%)

⚠️ Notable:
- [Any unusual or large expenses]
- [Categories trending up]
- [Missing receipts that need attention]
```

## Quarterly Tax Estimate

```
📊 Q[X] EXPENSE TOTAL — [Year]

Total Deductible Expenses: $[X,XXX.XX]
Estimated Tax Savings (at [X]% bracket): $[X,XXX.XX]
Quarterly estimated tax payment reminder: [date]
```

## Commands

- "Log expense [vendor] [amount] [category]" → Add expense entry
- "Expenses this month" → Show current month totals by category
- "Expense report [month]" → Full monthly summary
- "Missing receipts" → List expenses without receipts attached
- "Tax deductions YTD" → Year-to-date deductible expenses
- "Compare expenses [month1] vs [month2]" → Side-by-side comparison
- "Biggest expenses this month" → Top 10 by amount

## Rules

1. **Log expenses same day** — don't batch them or you'll forget
2. Every expense over $25 needs a receipt — flag missing ones weekly
3. Meals are only 50% deductible — track separately
4. Personal expenses paid with business funds must be flagged immediately
5. Monthly reconciliation against bank statement is mandatory
6. Keep 7 years of records — IRS statute of limitations is 3-6 years
