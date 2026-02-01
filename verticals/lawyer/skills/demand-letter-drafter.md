---
name: demand-letter-drafter
vertical: lawyer
description: Draft settlement demand letters from case details
trigger: "demand letter|draft demand|settlement demand|demand package|demand for"
---

# Skill: Demand Letter Drafter

Draft settlement demand letters based on case file data.

## When to Use

- Attorney says "draft demand for case [number]"
- Case has completed medical treatment
- All medical records and bills collected

## Demand Letter Structure

```
[FIRM LETTERHEAD]
[Date]

VIA [EMAIL/CERTIFIED MAIL]

[Adjuster Name]
[Insurance Company]
[Address]

Re: Our Client: [Client Name]
    Your Insured: [Defendant Name]
    Claim #: [Claim Number]
    Date of Loss: [Date]

Dear [Adjuster]:

INTRODUCTION
- Representation statement
- Incident summary (2-3 sentences)

LIABILITY
- Facts establishing fault
- Police report reference
- Witness statements (if any)
- Traffic citations (if applicable)

INJURIES AND TREATMENT
- Initial emergency care
- Diagnostic findings
- Treatment timeline
- Surgical procedures (if any)
- Ongoing treatment needs
- Prognosis

MEDICAL SPECIALS
[Itemized list of all providers and amounts]

Provider Name                  Amount
------------------------------------------
[Hospital]                     $X,XXX.XX
[Orthopedist]                  $X,XXX.XX
[Physical Therapy]             $X,XXX.XX
[Imaging]                      $X,XXX.XX
------------------------------------------
TOTAL MEDICAL SPECIALS:        $XX,XXX.XX

OTHER DAMAGES
- Lost wages: $X,XXX.XX ([days] missed from [employer])
- Property damage: $X,XXX.XX
- Out-of-pocket expenses: $X,XXX.XX
- Future medical costs (if applicable): $X,XXX.XX

PAIN AND SUFFERING
- Impact on daily life
- Activities no longer possible
- Emotional distress
- Loss of enjoyment of life

DEMAND
Based on the foregoing, we demand the sum of $[AMOUNT] to resolve 
all claims arising from this incident.

This demand remains open for [30] days. Should we not reach a 
resolution, we are prepared to proceed with litigation.

Sincerely,

[Attorney Name], Esq.
[Firm Name]
```

## Rules

1. **Never send without attorney review** — this is a DRAFT
2. Pull all amounts from the case tracker file
3. Demand multiple is typically 3-5x medical specials for PI (attorney decides)
4. Include case law citations if attorney requests
5. Save draft to `workspace/cases/[CASE-NUMBER]-demand-draft.md`
6. Log in case activity: "Demand letter drafted — pending attorney review"
