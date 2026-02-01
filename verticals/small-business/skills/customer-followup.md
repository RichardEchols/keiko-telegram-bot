---
name: customer-followup
vertical: small-business
description: Customer follow-up reminders, templates, and reactivation campaigns
trigger: "follow up|follow-up|customer reminder|check in with|haven't heard from|win back|reactivate"
---

# Skill: Customer Follow-Up System

Systematic follow-ups to retain customers, close deals, and reactivate dormant accounts.

## Follow-Up Schedule

| Touchpoint | Timing | Method | Template |
|------------|--------|--------|----------|
| Post-purchase thank you | Same day | Text/Email | #thank-you |
| Service follow-up | 48 hours after | Text | #service-check |
| Review request | 5 days after | Email | #review-ask |
| Repeat booking nudge | 3-4 weeks after | Text | #rebook |
| Dormant customer check | 60 days no visit | Email | #miss-you |
| Win-back offer | 90 days no visit | Email/Text | #win-back |
| Birthday/anniversary | On date | Text | #birthday |

## Follow-Up Log

Location: `workspace/followups/[YYYY-MM].md`

```markdown
# Follow-Up Log — [Month Year]

| Date | Customer | Type | Method | Status | Response | Next Step |
|------|----------|------|--------|--------|----------|-----------|
| Feb 1 | Sarah J. | Post-service | Text | ✅ Sent | Replied — happy | Review ask in 3 days |
| Feb 1 | Mike T. | Dormant (67d) | Email | ✅ Sent | No response | Win-back in 30 days |
| Feb 2 | Lisa R. | Rebook nudge | Text | ✅ Sent | Booked Feb 10 | — |
```

## Message Templates

### #thank-you
```
Hi [Name]! Thanks for coming in today. We appreciate your business! 
If you need anything, don't hesitate to reach out. Have a great [day/evening]! 
— [Business Name]
```

### #service-check
```
Hi [Name], just checking in! How's everything going after your 
[service] on [date]? Let us know if you have any questions. 
— [Business Name]
```

### #review-ask
```
Hi [Name]! We hope you're loving your [service/product]. If you 
have a moment, we'd really appreciate a quick review — it helps 
us a lot! [Review Link]
Thank you! — [Business Name]
```

### #rebook
```
Hi [Name]! It's been about [X weeks] since your last visit. 
Ready to schedule your next [service]? We have openings this 
week! Reply or call [phone] to book. — [Business Name]
```

### #miss-you
```
Subject: We miss you, [Name]!

Hi [Name],

It's been a while since we've seen you at [Business Name], and 
we wanted to check in! We've got some [new offerings/updates] 
we think you'd love.

As a thank you for being a valued customer, here's [offer] for 
your next visit.

Hope to see you soon!
[Business Name]
```

### #win-back
```
Hi [Name], we haven't seen you in a while and we'd love to have 
you back! Here's [X% off / special offer] on your next visit. 
Valid through [date]. — [Business Name]
```

### #birthday
```
Happy Birthday, [Name]! 🎂 To celebrate, we'd love to offer you 
[birthday offer]. Valid this week! — [Business Name]
```

## Reactivation Campaign

For customers inactive 60+ days, run monthly:

1. Pull list of customers with no activity in 60-90 days
2. Send #miss-you email/text
3. Track open/response rates in follow-up log
4. If no response in 30 days → send #win-back with offer
5. If no response after win-back → mark as "inactive" and check quarterly

## Commands

- "Follow-ups due today" → List all customers needing follow-up
- "Follow up with [name]" → Show customer history and suggested template
- "Dormant customers" → List customers with no activity in 60+ days
- "Send [template] to [name]" → Prepare follow-up message
- "Follow-up stats this month" → Response rates, rebooks, reviews gained
- "Birthday list this month" → Customers with upcoming birthdays

## Rules

1. **Follow up within 48 hours of service** — no exceptions
2. Never send more than 1 follow-up per customer per week (avoid spam)
3. Personalize every message — use their name and specific service
4. Track responses — if someone opts out, respect it immediately
5. Review follow-up effectiveness monthly — which templates get responses?
6. Birthday messages go out ON the birthday, not after
