---
name: case-tracker
vertical: lawyer
description: Track and manage active legal cases from intake to resolution
trigger: "show cases|case list|active cases|my cases|case status|new case|all cases|case aging"
---

# Skill: Case Tracker

Track and manage personal injury cases from intake to resolution.

## Case Data Structure

For each case, maintain in `workspace/cases/[CASE-NUMBER].md`:

```markdown
# Case: [CASE-NUMBER] — [Client Last Name] v. [Defendant]

## Status: [INTAKE | ACTIVE | LITIGATION | SETTLEMENT | CLOSED]
## Priority: [🔴 URGENT | 🟡 ACTIVE | 🟢 ROUTINE]

### Client
- Name: 
- Phone:
- Email:
- DOB:
- SSN (last 4):

### Incident
- Date of Loss:
- Type: [Auto | Slip & Fall | Med Mal | Workers Comp | Other]
- Location:
- Police Report #:
- Description:

### Statute of Limitations
- **SOL Date:** [YYYY-MM-DD]
- **SOL Type:** [2yr PI | 3yr property | etc.]
- **Days Remaining:** [auto-calculate]

### Insurance
- Defendant's Carrier:
- Policy #:
- Adjuster:
- Adjuster Phone:
- Policy Limits:
- UM/UIM Available:

### Medical
- Treating Providers: [list]
- Total Medical Specials: $
- Treatment Status: [Active | Completed | Pending Surgery]
- IME Scheduled: [date or N/A]

### Damages
- Medical Specials: $
- Lost Wages: $
- Property Damage: $
- Pain & Suffering (est.): $
- Total Demand (est.): $

### Settlement
- Demand Sent: [date]
- Demand Amount: $
- Last Offer: $
- Settlement Amount: $
- Settlement Date:
- Attorney Fee: $
- Net to Client: $

### Key Dates
- Intake: [date]
- Retainer Signed: [date]
- Demand Sent: [date]
- SOL: [date]
- Next Action: [description] by [date]

### Activity Log
- [YYYY-MM-DD] [action taken]
```

## Commands

- "New case" → Create intake file, prompt for required fields
- "Case status [number]" → Show case summary
- "All cases" → List all active cases with status and next action
- "SOL report" → Show all cases sorted by SOL date (nearest first)
- "Update case [number]" → Add activity or update fields
- "Settlement calc [number]" → Show damages breakdown and recommended demand range
- "Case aging" → Cases sorted by age (oldest first)
- "Overdue follow-ups" → Cases with no activity in 14+ days
