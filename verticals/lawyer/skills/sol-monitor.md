---
name: sol-monitor
vertical: lawyer
description: Statute of limitations tracker with alerts — missed SOL is malpractice
trigger: "SOL|statute of limitations|deadline|SOL report|expiring cases|malpractice risk"
---

# Skill: Statute of Limitations Monitor

**CRITICAL SKILL — Missed SOL = malpractice. This is the most important thing you do.**

## How It Works

Every morning at 8:00 AM, scan ALL active cases for SOL proximity:

### Alert Thresholds
| Days Remaining | Alert Level | Action |
|----------------|------------|--------|
| ≤ 7 days | 🚨 EMERGENCY | Message attorney IMMEDIATELY. Confirm receipt. |
| ≤ 14 days | 🔴 CRITICAL | Morning brief + separate urgent message |
| ≤ 30 days | 🟠 URGENT | Morning brief highlight + daily reminder |
| ≤ 60 days | 🟡 WARNING | Morning brief + weekly reminder |
| ≤ 90 days | 🔵 NOTICE | Morning brief mention |
| ≤ 180 days | ⚪ TRACKING | Monthly review mention |

### SOL Reference (Common — Verify for your jurisdiction)

**Personal Injury (General):** 2 years from date of injury
**Medical Malpractice:** 2 years (discovery rule may apply)
**Property Damage:** 3-4 years (varies by state)
**Workers' Compensation:** Varies significantly by state
**Wrongful Death:** 2 years from date of death
**Government Entity:** Notice requirement often 6 months, suit within 1-2 years

⚠️ **ALWAYS verify SOL for the specific jurisdiction and claim type.** These are general guidelines. The attorney must confirm.

### Morning SOL Report Format

```
⚖️ SOL REPORT — [DATE]

🚨 EMERGENCY (≤7 days):
  [none or list]

🔴 CRITICAL (≤14 days):
  [none or list]

🟠 URGENT (≤30 days):
  • Case #2024-0047 — Johnson v. Metro Transit — SOL: Feb 15, 2026 (15 days)

🟡 WARNING (≤60 days):
  • Case #2024-0089 — Williams v. St. Mary's — SOL: Mar 20, 2026 (48 days)

Total active cases: [X]
Cases with SOL within 180 days: [Y]
```

### Rules

1. **Never assume SOL is calculated correctly** — re-verify date of loss against SOL date
2. **Tolling events** — note any tolling (minor, mental incapacity, defendant absence)
3. **If SOL ≤ 30 days and no suit filed** — escalate every single day
4. **Keep a running log** of all SOL alerts sent in `workspace/sol-alerts.log`
