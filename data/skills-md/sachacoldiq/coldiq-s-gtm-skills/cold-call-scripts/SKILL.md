---
name: cold-call-scripts
description: 1-minute cold call script (5 steps) and no-show phone script. Use when training SDRs on calls, building call frameworks, or handling common phone scenarios.
---

# Cold Call Scripts

For objection responses, see [references/objections.md](references/objections.md).

## 1-Minute Cold Call Script (5 Steps)

| Step | Script | Purpose |
|------|--------|---------|
| 1 | "Hey {{firstName}}, this is [Name] from ColdIQ—I know I'm catching you out of the blue." | Pattern interrupt |
| 2 | "Mind if I take 30 seconds to tell you why I called? Then you can decide if it's worth continuing." | Earn permission |
| 3 | "I work with [ICP] who are struggling with [problem]." | Establish relevance |
| 4 | "We just helped [similar company] achieve [result]." | Social proof |
| 5 | "Is that something you're dealing with right now?" | Open conversation |

## Full Script Example

```
"Hey Sarah, this is Mike from ColdIQ—I know I'm catching you out of the blue.

Mind if I take 30 seconds to tell you why I called? Then you can decide if it's worth continuing.

I work with B2B SaaS companies doing $5-20M who are struggling with inconsistent pipeline.

We just helped a company similar to yours book 40+ qualified meetings per month.

Is pipeline predictability something you're dealing with right now?"
```

## No-Show Phone Script

```
"Hey {{firstName}}, it's [Name] from ColdIQ.

We had a call scheduled for [time]—wanted to make sure everything's okay.

No worries if something came up. Would [alternative time] work better?"
```

**Key:** No guilt, assume good intent, offer easy reschedule.

## Voicemail Script (Under 20 seconds)

```
"Hey {{firstName}}, [Name] from ColdIQ.

Quick message—I work with [ICP] on [problem].

Thought it might be relevant given [trigger/observation].

I'll shoot you an email with some times. Talk soon."
```

---

## Combines with

| Skill | Why |
|-------|-----|
| `sdr-outbound-rules` | Apply same writing rules to scripts |
| `cold-email-4-sequence` | Coordinate calls with email sequence |
| `buying-signals-6` | Use signals in Step 3 |
| `linkedin-campaign-complete` | Multi-channel coordination |

## Example prompts

```
Adapt the 1-minute script for selling marketing automation to CMOs.
```

```
Write a voicemail script for following up after a website visit.
```

```
How do I handle "we already have a solution" for CRM software?
```
