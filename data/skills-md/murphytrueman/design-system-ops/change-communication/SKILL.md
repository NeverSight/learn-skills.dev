---
name: change-communication
description: "Produce a communication package for a design system change — release notes, migration guide, and team announcement. This produces communication artefacts for changes that have already been decided, NOT the deprecation lifecycle itself. Trigger when someone says: communicate this change, breaking change announcement, how do I tell teams about this, release notes, change log, write the announcement, or anything about communicating an update, release, or breaking change to consuming teams. Do NOT trigger for planning or executing a deprecation — use deprecation-process for that, which includes its own communication plan as part of the full lifecycle."
---

# Change communication

A skill for producing a complete change communication package: release notes, migration guidance where needed, and a team announcement ready to send. Calibrated to the change type so a patch note does not read like a major incident, and a breaking change does not get buried in a routine release update.

## Context

Change communication is the part of design system work that feels like overhead until it is done badly. A breaking change that arrives without notice destroys trust faster than any number of missing components. A routine release that goes out without clear notes creates a support burden for the design systems team.

The goal is communication proportional to impact. This skill distinguishes between change types and produces output calibrated accordingly — a minor enhancement gets release notes and nothing more, while a breaking change gets a full package including migration guidance and a direct team notification.

## Boundaries

This skill communicates changes that have already been decided. It does not decide what to change, plan a deprecation lifecycle, or execute a migration — use `deprecation-process` for deprecation planning and `codemod-generator` for migration execution. If the change has not been finalised, ask the user to confirm the change details before producing communication. If the change affects no consuming teams (internal refactor with no API surface change), a communication package is unnecessary — confirm with the user and stop.

---

## Step 1: Classify the change

Ask for or confirm:
- What changed? (component, token, pattern, API, tooling, governance)
- Is it breaking? (Does it require consuming teams to change their code or designs to avoid regressions?)
- What is the scope of impact? (How many teams or products are affected?)
- Is there a migration path?

**Small-system note (fewer than 5 components):** For systems this size, calibrate communication intensity down. The audience is smaller and likely in closer contact — a breaking change to one of four components affects the entire consumer base, but that base may be a single team who you can notify directly in a standup or sync. Release notes are still required (they are the historical record), but the "announcement" may be a Slack message rather than a formal communication package. If the change is significant, a direct conversation replaces the written migration guide — walk through it together.

Classification:

**Patch** — bug fix, documentation correction, minor visual refinement with no API changes. No consuming team action required.

**Minor enhancement** — new prop, new variant, new component, new token. Backward compatible. Consuming teams can adopt at their own pace.

**Breaking change** — removed prop, renamed token, changed component API in a way that breaks existing usage, changed token values in a way that affects visual output. Consuming teams must act.

**System-level change** — governance policy, naming convention, architecture decision, tooling change. Wide blast radius, may not be technically breaking but affects how teams work with the system.

## Step 1b: Communication tailoring matrix

Before producing the communication package, assess the adoption context. The same change needs different messaging depending on how teams are engaging with the system.

**High-adoption teams** (actively using, contributing, engaged):
- Communication tone: informational. These teams will read release notes proactively.
- Migration support: self-service. Provide the migration guide and let them execute.
- Channel: standard channels (release notes, Slack announcement).

**Partial-adoption teams** (using some components, not fully engaged):
- Communication tone: supportive. Frame the change as an improvement to something they already use.
- Migration support: offer a pairing session or office hours slot.
- Channel: direct notification in addition to standard channels.

**Low-adoption or at-risk teams** (not using the system, or usage is declining):
- Communication tone: minimal. Do not over-communicate changes to teams that are not yet engaged — it creates noise.
- Migration support: N/A unless the change affects the few components they do use.
- Channel: only notify if they are directly affected.

**New teams** (recently onboarded or in onboarding):
- Communication tone: contextual. Frame the change within their onboarding experience.
- Migration support: proactive. Ensure their onboarding materials reflect the change.
- Channel: direct, through their onboarding contact.

This matrix prevents the common failure mode of communicating every change at the same intensity to every team, which trains teams to ignore system communications.

## Step 2: Produce the communication package

---

### For a patch:

**Release notes entry only**

Format:
```
[Component or token name] — [one-sentence description of the fix]
Affected: [who is affected, if anyone]
Action required: None
```

No announcement needed. Patch notes accumulate in the release log and are reviewed at the team's convenience.

---

### For a minor enhancement:

**Release notes entry + brief announcement**

**Release notes entry:**
```
[Component or token name] — [what was added]
What's new: [one to two sentences describing the addition and its purpose]
How to use it: [one sentence or a link to the documentation]
Action required: None — existing usage is unaffected
```

**Announcement (Slack or equivalent):**
Keep to three to four sentences. What was added, why it exists, where to find it. No preamble.

Template:
> [Component/token name] is now in the system. [One sentence on what it does.] [One sentence on when to use it.] Documentation is at [link].

---

### For a breaking change:

**Full package: release notes + migration guide + direct notification**

**Release notes entry:**
```
[Component or token name] — BREAKING CHANGE
What changed: [specific description of what changed]
Why it changed: [one sentence — reason, not justification]
Affected: [who is affected]
Migration: See migration guide below
Action required by: [date]
```

**Migration guide:**

The migration guide should be specific enough to follow without additional context. Include:

1. What the old behaviour was
2. What the new behaviour is
3. Step-by-step migration instructions with before/after examples where useful

```
Before:
<Button variant="danger" />

After:
<Button variant="destructive" />
```

4. Any edge cases that require special handling
5. What to do if migration is not feasible by the deadline (contact route, escalation path)

If a migration script exists or can be provided, include it or link to it here.

**Direct notification:**

Breaking changes do not wait to be discovered in release notes. Send a direct notification to all affected teams through their primary communication channel.

Template:
> **[System name] breaking change — action required by [date]**
>
> [What changed, in one sentence.]
>
> If you use [component/token name], you will need to [specific action] before [date] to avoid [specific consequence].
>
> Migration guide: [link]
> Questions: [channel or contact]

The notification should be short enough to read in thirty seconds and specific enough that someone reading it immediately knows whether they are affected.

---

### For a system-level change:

**Full package: announcement + context document + Q&A period**

System-level changes need more than release notes. They need context. Why is this changing? What does it mean for teams day-to-day? What happens to work that was done under the old system?

**Announcement:**
Lead with the change and its impact, not the reasoning. Teams want to know what they need to do before they want to understand why.

> **[What is changing] — effective [date]**
>
> [One sentence on what this means for teams using the system.]
>
> [Two to three sentences on what teams need to know: what changes in their workflow, what does not change, and what support is available.]
>
> Full context and rationale: [link to context document]
> Q&A session: [date/time or async channel]

**Context document:**
A separate document covering:
- What prompted the change
- What was considered and why this direction was chosen (reference the decision record if one exists)
- What the transition looks like — timeline, what is changing when
- What stays the same
- Known concerns and how they were addressed

**Q&A period:**
For significant system-level changes, offer a defined period for questions — either a live session or a dedicated async channel with a named response time. Close the loop after: summarise the key questions raised and the answers given, and add that summary to the context document.

---

## Step 3: Choose the channels

Different communication channels serve different purposes. Calibrate by change type:

| Channel | When to use |
|---|---|
| Release notes / changelog | Every change, every time |
| Slack / team channels | Minor enhancements and above |
| Direct team notification | Breaking changes and system-level changes |
| Email | Breaking changes with external or cross-org impact |
| Meeting / live session | System-level changes with significant workflow impact |

The default is to over-communicate rather than under-communicate. A team that learns about a breaking change from their own bug report will remember it.

## Step 4: Set a follow-up

For breaking changes and system-level changes, schedule a follow-up:
- One week before the action-required date: reminder to teams who have not yet migrated
- On the action-required date: confirmation that the change is live, any last-minute support available
- Two weeks after: review whether migration is complete, identify any teams who need additional help

Document this follow-up schedule alongside the communication so it does not get missed.

## Quality checks

- Change classification is correct — breaking changes are not communicated as minor enhancements
- Migration guide is specific enough to follow without additional context
- Direct notification for breaking changes names the specific consequence of inaction
- Channels are appropriate to the change type
- A follow-up schedule exists for breaking and system-level changes
- Announcement copy can be sent as-is — no placeholders left unfilled
