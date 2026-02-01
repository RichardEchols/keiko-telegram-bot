---
name: client-intake
vertical: lawyer
description: New client intake questionnaire and file creation for PI cases
trigger: "new client|intake|sign up client|client intake|new case intake|retainer"
---

# Skill: Client Intake

Streamline new client onboarding from first contact to signed retainer.

## Intake Form

Create intake file at `workspace/intake/[YYYY-MM-DD]-[last-name].md`:

```markdown
# New Client Intake — [Date]

## Contact Information
- Full Name:
- Date of Birth:
- SSN (last 4):
- Phone (primary):
- Phone (alt):
- Email:
- Address:
- Preferred Contact Method: [call/text/email]
- Best Time to Reach:

## Incident Details
- Date of Incident:
- Time:
- Location:
- Type: [Auto | Slip & Fall | Med Mal | Workers Comp | Dog Bite | Other]
- Brief Description:
- Police Report Filed: [Y/N] — Report #:
- Photos/Video Available: [Y/N]

## Injuries
- Primary Injuries:
- Emergency Room Visit: [Y/N] — Hospital:
- Current Treatment:
- Treating Physician:
- Prior Injuries to Same Area: [Y/N] — Details:

## Insurance Information
- Client's Auto Insurance:
- Policy #:
- At-Fault Party's Insurance (if known):
- Health Insurance:

## Employment Impact
- Employer:
- Occupation:
- Missing Work: [Y/N]
- Days Missed:

## Referral Source
- How did you hear about us:
- Referring Attorney/Client:

## Conflict Check
- Opposing Party Name:
- Opposing Party Insurance:
- ⚠️ CONFLICT CHECK RESULT: [CLEAR | CONFLICT FOUND — details]
```

## Conflict Check Process

1. Search ALL active and closed case files for opposing party name
2. Search for opposing party's insurance company + adjuster
3. Search for any related parties (family members, businesses)
4. If conflict found → **STOP** — notify attorney before proceeding
5. Log result in intake file

## Post-Intake Checklist

```
☐ Conflict check completed — CLEAR
☐ Retainer agreement prepared
☐ Fee structure explained (contingency %, costs)
☐ HIPAA authorization signed
☐ Medical records release signed
☐ Police report requested
☐ Preservation letter sent (if needed)
☐ Case file created in workspace/cases/
☐ SOL date calculated and entered
☐ Welcome packet sent to client
☐ Follow-up call scheduled (48 hours)
```

## Commands

- "New intake" → Start intake questionnaire, prompt for each field
- "Conflict check [name]" → Search all cases for conflicts
- "Intake status" → Show all pending intakes and their completion %
- "Generate retainer for [name]" → Create retainer agreement from intake data
- "Intake checklist [name]" → Show post-intake checklist with completion status

## Rules

1. **NEVER skip conflict check** — run it before ANY discussion of case details
2. Collect ALL required fields — incomplete intakes get flagged daily
3. Calculate SOL immediately upon learning date of incident
4. Log intake source for marketing ROI tracking
5. Follow up on unsigned retainers within 48 hours
6. Intake files are confidential — never share between clients
