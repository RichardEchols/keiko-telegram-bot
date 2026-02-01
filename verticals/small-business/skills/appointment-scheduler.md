---
name: appointment-scheduler
vertical: small-business
description: Manage appointments, availability, reminders, and no-show tracking
trigger: "appointment|schedule|booking|book appointment|cancel appointment|no show|availability|open slots"
---

# Skill: Appointment Scheduler

Manage appointments, send reminders, track no-shows, and optimize scheduling.

## Appointment Calendar

Location: `workspace/appointments/[YYYY-MM-DD].md`

```markdown
# Appointments — [Day, Month DD, YYYY]

| Time | Client | Service | Duration | Status | Notes |
|------|--------|---------|----------|--------|-------|
| 9:00 AM | Sarah Johnson | Consultation | 30 min | ✅ Confirmed | First visit |
| 10:00 AM | Mike Torres | Follow-up | 45 min | ✅ Confirmed | |
| 11:00 AM | — | OPEN | — | 🟢 Available | |
| 11:30 AM | — | OPEN | — | 🟢 Available | |
| 12:00 PM | — | LUNCH | 60 min | ⬛ Blocked | |
| 1:00 PM | Lisa Rodriguez | Service A | 60 min | ⏳ Pending | Needs to confirm |
| 2:00 PM | James Kim | Service B | 45 min | ✅ Confirmed | Returning client |
| 3:00 PM | — | OPEN | — | 🟢 Available | |
| 4:00 PM | New Client | Intake | 60 min | ✅ Confirmed | Referred by Kim |
```

## Status Legend
- ✅ Confirmed — Client responded to reminder
- ⏳ Pending — Booked but not confirmed
- 🟢 Available — Open for booking
- ⬛ Blocked — Lunch, personal, admin time
- 🔴 No-Show — Client didn't arrive
- ❌ Cancelled — Client cancelled
- 🔄 Rescheduled — Moved to new time

## Reminder Schedule

| Timing | Method | Template |
|--------|--------|----------|
| 24 hours before | Text | Reminder with date, time, location |
| 2 hours before | Text | Quick reminder (if not yet confirmed) |
| After no-show | Text/Call | Reschedule attempt |

### Reminder Templates

**24-Hour Reminder:**
```
Hi [Name]! This is a reminder of your appointment tomorrow, 
[Day] at [Time] at [Business Name] ([Address]). 
Reply YES to confirm or call [phone] to reschedule. 
See you soon!
```

**2-Hour Reminder (unconfirmed only):**
```
Hi [Name], just a quick reminder about your [Time] appointment 
today at [Business Name]. We're looking forward to seeing you!
```

**No-Show Follow-Up:**
```
Hi [Name], we missed you at your [Time] appointment today. 
No worries — life happens! Would you like to reschedule? 
Call [phone] or reply with a day/time that works. 
— [Business Name]
```

## No-Show Tracking

Location: `workspace/appointments/no-shows.md`

```markdown
# No-Show Tracker — [Year]

| Date | Client | Service | Value Lost | Attempts to Reschedule | Result |
|------|--------|---------|-----------|----------------------|--------|
| Jan 15 | John D. | Service A | $75 | 2 | Rescheduled Jan 22 |
| Jan 20 | Amy S. | Consultation | $50 | 3 | No response |

Monthly No-Show Rate: [X]%
Revenue Lost to No-Shows: $[X]
```

## Availability Rules

```
Default Business Hours: [Mon-Fri 9:00 AM - 5:00 PM]
Buffer Between Appointments: [15 minutes]
Max Appointments Per Day: [X]
Lunch Block: [12:00 PM - 1:00 PM]
Last Appointment: [4:00 PM] (ensures no overtime)
```

## Commands

- "Schedule [name] [service] [date] [time]" → Book appointment
- "Today's appointments" → Show today's schedule
- "Tomorrow's schedule" → Show tomorrow's schedule
- "Open slots [date]" → Show available times
- "Cancel [name] [date]" → Cancel and log cancellation
- "No-shows this month" → Show no-show report
- "Confirm appointments for tomorrow" → Send all 24-hour reminders
- "Reschedule [name] to [new date/time]" → Move appointment

## Rules

1. **Send 24-hour reminders for EVERY appointment** — reduces no-shows by 40%+
2. Always leave buffer time between appointments — no back-to-back stacking
3. Track no-show patterns — 3 no-shows = require prepayment or deposit
4. Block personal/admin time proactively — don't let it get booked over
5. Same-day cancellations count as no-shows for tracking purposes
6. Review no-show rate monthly — if >15%, adjust reminder or deposit policy
