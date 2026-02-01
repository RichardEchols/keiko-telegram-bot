---
name: client-crm
vertical: small-business
description: Track clients, leads, and pipeline with simple markdown CRM
trigger: "client|new client|new lead|client status|all clients|pipeline|follow-ups due|revenue by client"
---

# Skill: Simple Client CRM

Track clients, leads, and follow-ups. No software needed — just markdown.

## Client File

One file per client in `workspace/clients/[client-name].md`:

```markdown
# Client: [Business/Person Name]

## Contact
- Name: [name]
- Email: [email]
- Phone: [phone]
- Address: [address]
- How they found us: [referral/Google/ad/etc.]

## Status: [LEAD | ACTIVE | PAUSED | CHURNED]
## Value: $[monthly or project amount]
## Since: [start date]

## Services
- [Service 1] — $[amount] / [frequency]
- [Service 2] — $[amount] / [frequency]

## Key Dates
- First contact: [date]
- Contract signed: [date]
- Contract renewal: [date]
- Last interaction: [date]

## Notes
- [YYYY-MM-DD] [note]
- [YYYY-MM-DD] [note]

## Follow-Up History
- [YYYY-MM-DD] [what was discussed, next steps]
```

## Lead Tracking

Track leads in `workspace/leads.md`:

```markdown
# Active Leads

| Name | Source | First Contact | Last Contact | Status | Next Step | Value |
|------|--------|--------------|-------------|--------|-----------|-------|
| [name] | Google | Jan 15 | Jan 20 | Proposal sent | Follow up Feb 1 | $2,000 |
```

## Commands

- "New client [name]" → Create client file
- "New lead [name] from [source]" → Add to leads tracker
- "Client status [name]" → Show client summary
- "All clients" → List all active clients with monthly value
- "Follow-ups due" → Who needs to be contacted
- "Pipeline" → Show all leads with stage and value
- "Revenue by client" → Rank clients by revenue

## Follow-Up Rules

| Situation | Follow-up Timing |
|-----------|-----------------|
| New lead inquiry | Same day |
| Proposal sent | 3 days |
| No response after follow-up | 7 days |
| Contract discussion | 2 days |
| Active client check-in | 30 days |
| At-risk client | 14 days |

## Rules

1. **No lead sits uncontacted >24 hours**
2. **No active client goes >30 days without touchpoint**
3. Flag clients with declining engagement
4. Track total pipeline value (leads × probability)
5. Monthly client retention report
