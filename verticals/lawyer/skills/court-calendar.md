---
name: court-calendar
vertical: lawyer
description: Court date tracking and hearing preparation reminders
trigger: "court date|court calendar|hearing|mediation|trial date|deposition|court prep"
---

# Skill: Court Calendar

Track all court dates, depositions, mediations, and deadlines with preparation reminders.

## Calendar File

Location: `workspace/court-calendar.md`

```markdown
# Court Calendar — [Month Year]

| Date | Time | Case # | Type | Court/Location | Judge | Status |
|------|------|--------|------|---------------|-------|--------|
| Feb 10 | 9:30 AM | 2024-0047 | Status Conference | Fulton Superior | Hon. Williams | ✅ Prepared |
| Feb 14 | 2:00 PM | 2024-0089 | Mediation | AAA Office, Midtown | Mediator: Smith | 🔄 Preparing |
| Feb 22 | 10:00 AM | 2024-0103 | Motion Hearing | DeKalb State | Hon. Jackson | ⏳ Not Started |
| Mar 5 | 9:00 AM | 2024-0047 | Deposition (Def.) | Our Office | — | ⏳ Not Started |
```

## Alert Thresholds

| Days Before | Alert Level | Action |
|-------------|------------|--------|
| ≤ 1 day | 🚨 TOMORROW | Final prep check — confirm all materials ready |
| ≤ 3 days | 🔴 CRITICAL | Prep must be complete — review checklist |
| ≤ 7 days | 🟠 THIS WEEK | Active preparation — assemble materials |
| ≤ 14 days | 🟡 UPCOMING | Begin preparation — review case file |
| ≤ 30 days | 🔵 SCHEDULED | Awareness — note on morning brief |

## Preparation Checklists

### Status Conference
```
☐ Review case file and recent activity
☐ Prepare status update (discovery progress, settlement talks)
☐ Note any scheduling conflicts for future dates
☐ Prepare proposed scheduling order if needed
☐ Confirm court location and parking
```

### Motion Hearing
```
☐ Motion brief filed and served (verify deadline met)
☐ Response brief reviewed (if opposition filed)
☐ Reply brief filed (if applicable)
☐ Oral argument outline prepared
☐ Key cases printed for bench reference
☐ Exhibits organized and tabbed
☐ Proposed order drafted
```

### Mediation
```
☐ Mediation statement submitted to mediator
☐ Settlement authority confirmed with client
☐ Demand package assembled (medicals, bills, photos)
☐ Settlement breakdown prepared (fee, costs, net to client)
☐ Client confirmed attendance
☐ Opposing party/counsel confirmed attendance
☐ Client prepared for process (expectations, patience)
```

### Deposition
```
☐ Notice of deposition served
☐ Subpoena issued (if non-party)
☐ Outline of questions prepared
☐ Relevant documents assembled as exhibits
☐ Court reporter confirmed
☐ Videographer booked (if video depo)
☐ Conference room reserved
```

### Trial
```
☐ Trial brief filed
☐ Motions in limine filed and argued
☐ Witness list finalized and subpoenas served
☐ Exhibit list finalized — all exhibits pre-marked
☐ Jury instructions proposed
☐ Voir dire questions prepared
☐ Opening statement drafted
☐ Direct/cross examination outlines complete
☐ Closing argument outline prepared
☐ Technology tested (projector, screens, ELMO)
☐ Client prepared and wardrobe discussed
```

## Daily Court Report Format

```
⚖️ COURT CALENDAR — [DATE]

🚨 TOMORROW:
  • [Case # — Type — Time — Location]

🔴 THIS WEEK:
  • [Case # — Type — Date — Prep Status]

🟠 NEXT 14 DAYS:
  • [Case # — Type — Date — Prep Status]

Preparation items needing attention: [X]
```

## Commands

- "Court calendar" → Show all upcoming dates
- "This week's hearings" → Show next 7 days
- "Add court date [case#] [type] [date] [time] [location]" → Add new entry
- "Prep checklist [case#] [date]" → Show preparation checklist for specific hearing
- "Court prep status" → Show all upcoming dates with prep completion %
- "Reschedule [case#] [date] to [new date]" → Update calendar entry

## Rules

1. **No court date goes untracked** — if it's on the docket, it's in the calendar
2. Preparation starts minimum 14 days before any hearing
3. Trial prep starts minimum 30 days before trial date
4. Confirm ALL court dates 48 hours in advance (check court website/clerk)
5. Log preparation completion in case activity log
6. Always note continuances and reasons in the case file
