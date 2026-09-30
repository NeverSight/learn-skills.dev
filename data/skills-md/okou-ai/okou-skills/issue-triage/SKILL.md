---
name: issue-triage
description: Triage support issues by severity, duplicates, ownership, and first-response approach.
---

## Classification System

Every incoming issue receives a **primary label** and, where relevant, a **secondary label** from the taxonomy below.

| Label | Scope | Typical Signals |
|-------|-------|-----------------|
| **Defect** | Product behaving contrary to specification or expectation | Error messages, crashes, data rendering incorrectly, regressions, unexpected output |
| **Guidance** | Customer seeking instructions or clarification | "How do I...", "Where can I find...", setup questions, configuration help |
| **Enhancement** | Request for new or changed functionality | "It would help if...", "Can you add...", "Are there plans for..." |
| **Billing** | Charges, subscriptions, invoicing, pricing, refunds | Payment failures, unexpected charges, plan changes, credit requests |
| **Access** | Login, permissions, SSO, user management | Lockouts, password resets, role assignments, MFA issues |
| **Integration** | Connectivity with external tools and APIs | Webhook failures, OAuth errors, sync problems, API response issues |
| **Security** | Threats, data exposure, compliance inquiries | Unauthorized access, vulnerability disclosures, GDPR/SOC 2 questions |
| **Data** | Integrity, migration, import/export concerns | Missing records, duplicate entries, failed imports, export formatting |
| **Reliability** | Speed, uptime, or degraded service | Timeouts, slow loading, 5xx errors, service unavailability |

### Choosing the Right Label

- When a customer describes overlapping concerns (e.g., a defect plus an enhancement wish), the **root problem** determines the primary label.
- A broken workflow the customer used to rely on is a **Defect**, not an Enhancement.
- A request for the product to work in a new way is an **Enhancement**, even if the customer frames it as something "not working."
- Prefer **Defect** when ambiguous -- investigating a potential bug is safer than dismissing one.

## Severity Levels

### P1 -- Outage / Emergency

The product is completely unusable, data is at risk, or a security incident is underway. The scope is broad (most or all users impacted) or the consequences are irreversible.

- Total service unavailability
- Active data loss, corruption, or unauthorized exposure
- Security breach in progress
- Situation is deteriorating without intervention

**Response commitment:** First reply within 60 minutes. Continuous engagement until mitigated. Status updates every 1-2 hours.

### P2 -- Severe Disruption

A key capability is non-functional, a significant user population is blocked, and no practical workaround exists.

- Core workflow broken but ancillary functions still operate
- Multiple users or a strategically important account impacted
- Time-sensitive operations are stalled
- Reasonable alternatives are not available

**Response commitment:** First reply within 4 hours. Same-day investigation. Status updates every 4 hours.

### P3 -- Moderate Impact

A feature is degraded but usable through an alternate path, or the issue affects a limited audience.

- Functionality is impaired but a workaround is viable
- Impact is inconvenient rather than blocking
- A small group of users is affected
- No urgent pressure from the customer

**Response commitment:** First reply within 1 business day. Progress update within 3 business days.

### P4 -- Minor / Informational

Cosmetic glitches, general inquiries, enhancement ideas, or problems with well-documented fixes.

- Visual imperfections with no functional consequence
- Enhancement suggestions and feedback
- Routine questions answerable from documentation
- Issues resolved by following existing instructions

**Response commitment:** First reply within 2 business days. Resolution at standard pace.

### Conditions That Warrant Upgrading Severity

Raise the severity level when any of the following occur:

- SLA window has elapsed without resolution
- A pattern emerges: three or more customers reporting the same symptom
- The customer explicitly invokes executive attention or threatens churn
- A previously viable workaround ceases to function
- The blast radius expands (additional users, systems, or data affected)

## Routing Guidelines

Direct each issue to the team best positioned to resolve it:

| Destination | Appropriate When |
|-------------|-----------------|
| **Frontline Support** | Known-solution issues, documentation-answerable questions, password resets, simple billing inquiries |
| **Senior / Technical Support** | Bugs needing investigation, non-trivial configuration, integration debugging, complex account scenarios |
| **Engineering** | Verified defects requiring code changes, infrastructure incidents, performance regressions |
| **Product Management** | High-demand feature requests, design-level workflow gaps, prioritization decisions |
| **Security Team** | Vulnerability reports, data exposure concerns, compliance-related inquiries |
| **Finance / Billing** | Refund approvals, contractual billing disputes, non-standard pricing adjustments |

## Identifying Duplicate Reports

Before routing a new issue, check for existing overlap:

1. **Symptom search:** Look for open issues with matching error text or behavioral descriptions.
2. **Customer history:** Verify the same customer has not already filed a related report.
3. **Feature-area scan:** Review recent issues in the same product surface.
4. **Known-issue registry:** Cross-reference against documented active problems.

When a match is found:

- Associate the new report with the existing issue.
- Inform the customer that the problem is tracked and being worked on.
- Append any fresh details or reproduction context from the new submission.
- Re-evaluate severity if the additional report widens the impact.

## Initial Acknowledgment Patterns

### For Defects

```
Thanks for letting us know about this. I understand that [specific
disruption] is affecting your work.

This has been logged at [severity] and our team is looking into it.
[If a workaround exists: "While we investigate, you can [workaround]."]

Expect an update from us by [timeframe based on SLA].
```

### For Guidance Requests

```
Good question! [Concise answer or pointer to documentation]

[For multi-step answers: "Here is a walkthrough:"]
[Numbered steps or explanation]

Let me know if this resolves things or if anything else comes up.
```

### For Enhancement Ideas

```
Appreciate you sharing this idea -- I can see how [desired capability]
would improve your workflow.

I have forwarded this to our product team. I cannot promise a specific
delivery date, but input like this directly shapes our priorities.

[If a partial solution exists: "In the meantime, [alternative approach]
may help."]
```

### For Billing Concerns

```
I know billing matters need quick resolution. Let me take a look.

[If straightforward: provide resolution details]
[If investigation needed: "I am reviewing your account and will
follow up by [timeframe]."]
```

### For Security Reports

```
Thank you for raising this -- we treat security matters with the
highest urgency.

This has been routed to our security team for immediate review.
You will hear back by [timeframe].

[If protective steps are advisable: "We recommend [action] in the
meantime."]
```

## Operational Guidelines

1. Read the entire thread before assigning labels -- later messages frequently alter the picture.
2. Classify based on the underlying cause, not just the surface symptom.
3. When severity is uncertain, round up -- downgrading later is far easier than recovering from a missed commitment.
4. Always check for duplicates and known issues prior to routing.
5. Attach internal notes summarizing what you have assessed and ruled out, so the next handler can pick up without re-investigation.
6. Watch for emerging patterns -- repeated low-severity reports on the same topic may signal a systemic problem that deserves elevated attention.
