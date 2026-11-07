---
name: campaign-performance-analyzer
description: "Use this skill when you need to understand how outbound campaigns are performing and what to change: \"analyse my campaign results\", \"why is this sequence underperforming\", \"compare my campaigns\", \"weekly outbound report\". Builds the funnel from contacts to meetings for each campaign, step, segment, sender and channel, benchmarks it, finds the stage where performance breaks, separates list, deliverability, copy and follow-up problems, and recommends the next test. Produces a short report a team can act on."
license: MIT
metadata:
  title: Campaign performance analyzer
  category: revops
  tags: "RevOps, SDR, Sales Leaders, Founders, Agencies"
  author: prosyo
  version: "1.0.0"
  keywords: "outbound campaign analysis, cold email metrics benchmarks, sequence performance report, claude campaign analysis skill, outbound reporting"
  inputs: "Campaign data by step and segment, Meetings and opportunities, Time period"
  outputs: "Funnel per campaign, Diagnosis, Benchmarks, Next tests, Report"
---

Use this weekly or at the end of a campaign. It answers three questions: what is working, where does it break, and what do we change next.

## Inputs

- Per campaign: contacts, sent, delivered or bounced, replies, positive replies, meetings booked and held, by step, segment, sender and channel.
- Opportunities and pipeline created from those meetings.
- The period.

## The play

### 1. Build the funnel
Contacts → delivered → replied → positive → booked → held → opportunity. Calculate each conversion. Skip open rates as a decision metric; open tracking is unreliable and often turned off for deliverability.

### 2. Benchmark
Read [references/outbound-benchmarks.md](references/outbound-benchmarks.md) for typical ranges by channel and what each gap usually means. Benchmarks are a sanity check, not a target; your own trend matters more.

### 3. Find the break
The first stage below benchmark is the problem to fix; improving later stages first is wasted effort.

| Break | Usually means | Look at |
| --- | --- | --- |
| Bounces | List quality | Source, verification, catch-alls |
| Low replies, few negatives | Not seen, or not relevant | Deliverability by sender; targeting; first line |
| Replies, few positive | Message or offer mismatch | Angle, persona, ask |
| Positive, few booked | Slow or weak reply handling | Time to respond, booking flow |
| Booked, few held | Weak qualification or reminders | No-show rate, lead time |
| Held, few opportunities | Wrong ICP or poor discovery | Fit of meetings, discovery quality |

### 4. Slice it
By step (which email gets the replies), segment (which persona or industry), sender (deliverability or skill), channel. Small slices need samples of 100+ contacts before conclusions.

### 5. Recommend the next test
One test at a time on the broken stage, with a hypothesis and a success threshold.

## Output format

```
Period: | Campaigns: | Contacts:
Funnel (all): contacts → delivered x% → replied x% → positive x% → booked x% → held x% → opps
Best / worst campaign: <name - why>
The break: <stage - evidence - likely cause>
Slices worth noting: <step, segment, sender findings with sample sizes>
Next test: <hypothesis - change - metric - threshold - sample>
Stop / scale: <campaigns to pause, campaigns to give more volume>
```

## What good looks like

- Diagnosis follows the funnel order.
- Every conclusion states its sample size.
- The report ends in one or two decisions, not twenty observations.
- The common mistake is optimising subject lines when a third of the emails bounce or land in spam.

## Rules

- MUST report sample sizes and flag anything under 100 contacts as directional.
- MUST check deliverability by sender before judging copy.
- NEVER call a test winner on fewer than 200 contacts per variant.

## Example prompts

- "Here's last month's export for 6 campaigns. What's working and what should we change?"
- "Our reply rate halved this month. Find out why."
- "Build a weekly outbound report template for our SDR team."
