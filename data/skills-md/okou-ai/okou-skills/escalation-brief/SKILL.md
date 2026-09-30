---
name: escalation-brief
description: Create escalation briefs with impact, reproduction, context, owner, and follow-up tracking.
---

## Deciding: Escalate or Resolve In-House?

### Keep It in Support When:

- A documented fix or known workaround addresses the problem
- The root cause is a configuration or setup error you can correct
- The customer needs coaching or training, not a product change
- The limitation is documented and an alternative path exists
- Historical tickets with the same profile were resolved at the support tier

### Escalate When:

- **Technical barrier**: A confirmed defect needs a code-level fix, infrastructure-level investigation is required, or data has been lost or corrupted
- **Diagnostic ceiling**: The issue exceeds support tooling or access, involves a custom deployment, or demands database-level inspection
- **Widespread harm**: Multiple customers are reporting the same problem, production is down, data integrity is compromised, or a security threat exists
- **Business stakes**: A high-value account is at risk, an SLA has been breached or is about to be, or the customer is requesting leadership involvement
- **Stalled progress**: The issue has sat open past SLA, the customer has waited an unreasonable duration, or standard troubleshooting is not advancing
- **Recurring pattern**: Three or more independent reports of the same symptom, a previously-patched issue has resurfaced, or severity is trending upward over time

## Escalation Destinations

### Support L1 to Support L2

**Sender:** Frontline support agent
**Receiver:** Senior support / technical specialists
**Trigger:** Deeper investigation, specialized product expertise, or advanced debugging is needed
**Package contents:** Issue summary, troubleshooting already performed, customer context

### Support L2 to Engineering

**Sender:** Senior support
**Receiver:** Owning engineering squad
**Trigger:** Confirmed defect, infrastructure fault, code change required, system-level inspection needed
**Package contents:** Complete reproduction procedure, environment specifics, relevant logs and error output, business impact statement, customer-facing timeline commitments

### Support L2 to Product

**Sender:** Senior support
**Receiver:** Product management
**Trigger:** Capability gap causing pain, design-level decision needed, workflow mismatch, competing priorities across customers
**Package contents:** Customer use case narrative, business impact, request frequency, competitive context if available

### Any Tier to Security

**Sender:** Any support agent
**Receiver:** Security team
**Trigger:** Possible data exposure, unauthorized access report, vulnerability disclosure, compliance risk
**Package contents:** Observations, affected parties/systems, containment measures already taken, urgency rating
**Rule:** Security escalations skip tier progression entirely -- route immediately regardless of your level.

### Any Tier to Leadership

**Sender:** Typically L2 or a support manager
**Receiver:** Support leadership or executive staff
**Trigger:** High-ARR customer signaling churn, SLA breach on a strategic account, cross-functional decision required, policy exception needed, legal or reputational risk
**Package contents:** Complete business context, revenue exposure, actions taken to date, the specific decision or intervention needed, hard deadline

## Escalation Document Structure

Assemble every escalation using this framework:

```
ESCALATION: [Concise one-line summary]
Severity: [Critical / High / Medium]
Routed to: [Engineering / Product / Security / Leadership]

BUSINESS IMPACT
- Affected customers: [Count and names where relevant]
- Operational effect: [What is broken for them]
- Revenue exposure: [Dollar figure if applicable]
- SLA position: [Compliant / At risk / Breached]

PROBLEM NARRATIVE
[3-5 sentences covering: what is happening, when it began,
how it presents, and how wide the blast radius is]

REPRODUCTION PROCEDURE (for defects)
1. [Step]
2. [Step]
3. [Step]
Expected outcome: [X]
Observed outcome: [Y]
Environment: [Browser, OS, plan tier, feature flags, etc.]

ACTIONS ALREADY TAKEN
1. [What was tried] -> [Outcome]
2. [What was tried] -> [Outcome]
3. [What was tried] -> [Outcome]

CUSTOMER COMMUNICATION STATUS
- Most recent update: [Date and summary]
- Customer expectation: [What they believe will happen and by when]
- Further escalation risk: [Likelihood customer escalates beyond you]

REQUEST
- [Precise ask: investigate / ship a fix / make a decision / approve an exception]
- Hard deadline: [Date/time]

ATTACHMENTS AND REFERENCES
- [Ticket URLs]
- [Internal discussion threads]
- [Log files, screenshots, recordings]
```

## Quantifying Business Impact

Vague escalations get deprioritized. Anchor every escalation with measurable impact across these dimensions:

| Dimension | Key Questions |
|-----------|--------------|
| **Breadth** | How many customers or end users are affected? Is the number growing? |
| **Depth** | Are they fully blocked or merely inconvenienced? |
| **Duration** | How long has this persisted? When does it become critical? |
| **Revenue** | What ARR is exposed? Are pipeline deals at risk? |
| **Reputation** | Could this reach social media or press? Is a reference account involved? |
| **Contractual** | Are SLA terms being violated? Do contractual penalties apply? |

### Quick Severity Definitions

- **Critical**: Service down, data at risk, active security incident, or multiple high-value accounts impacted. Demands immediate action.
- **High**: Core functionality broken, key customer blocked, SLA threshold approaching. Requires same-day engagement.
- **Medium**: Significant issue but a viable workaround exists; business impact is real but not time-critical. Needs resolution within the current week.

## Crafting Effective Reproduction Steps

Precise reproduction instructions are the highest-value component of any defect escalation.

1. **Establish the baseline state**: Describe account type, configuration, permissions, and any prerequisites.
2. **Use exact actions**: "Select the Export CSV button in the upper-right corner of the Reports view" not "try exporting."
3. **Specify literal inputs**: Provide the actual data values, IDs, or strings used -- not "enter a value."
4. **Record the environment**: Browser and version, operating system, account plan tier, active feature flags.
5. **State the frequency**: Reproducible every time? Intermittent? Only under specific conditions?
6. **Attach evidence**: Screenshots, exact error text, network traces, browser console output.
7. **Document eliminations**: "Reproduced in both Chrome 122 and Safari 17" / "Occurs on both staging and production."

## Post-Escalation Follow-Through

Escalation without follow-up is abandonment. Stay engaged:

| Severity | Check-in with Receiving Team | Customer-Facing Update |
|----------|------------------------------|------------------------|
| **Critical** | Every 2 hours | Every 2-4 hours (or per SLA) |
| **High** | Every 4 hours | Every 4-8 hours |
| **Medium** | Once daily | Every 1-2 business days |

### Ongoing Responsibilities

- Proactively contact the receiving team for progress; do not wait to be told.
- Update the customer even when there is nothing new: "Investigation is ongoing -- here is what has been confirmed so far."
- Re-assess severity if circumstances shift in either direction.
- Maintain a running log of all updates in the ticket for auditability.
- When resolved: confirm with the customer, close internal tracking, and capture lessons learned.

## Knowing When to De-escalate

Escalation is not permanent. Pull an issue back when:

- Investigation reveals a cause that support can address directly
- A workaround is discovered that fully unblocks the customer
- The problem self-resolves (but still document the root cause)
- Updated information changes the severity calculus

### De-escalation Procedure

- Notify the team that received the escalation
- Record the resolution or new status in the ticket
- Communicate the outcome to the customer
- Document findings so future agents benefit from the knowledge

## Operating Principles

1. Quantify impact with numbers, not adjectives -- measurable escalations get faster attention.
2. For defects, reproduction steps are non-negotiable -- they are what engineering needs most.
3. Distinguish your ask: "investigate," "fix," and "decide" are different requests with different owners.
4. Attach a deadline to every escalation -- urgency without a timeline is ambiguous.
5. You own the customer relationship throughout; escalating the technical work does not transfer that responsibility.
6. Follow up before being asked -- proactive updates build trust with both the customer and the receiving team.
7. Log everything -- the escalation record is a resource for pattern detection and process improvement.
