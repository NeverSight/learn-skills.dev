---
name: oss-issue-triage
description: Designs an issue and pull-request triage system a maintainer team can sustain - response targets sized against real capacity, the label taxonomy, intake cuts through structured forms and off-tracker routing, a separate security-report path, triage duty assignment, and the closing, staleness and volume-gating policy. Use whenever someone says "our issue tracker is out of control", "design an issue triage process", "set up labels for our repo", "we have 900 open issues", "should we run a stale bot", "PR backlog nobody reviews", "triage rotation", or "we are drowning in AI-generated reports" - even if they only say maintenance is overwhelming. Not good-first-issue curation - use samber/developer-relations-skills@oss-contributor-onboarding.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# OSS Issue Triage

You design the system that decides how a project's incoming issues and pull requests get handled - labels, intake, response promise, duty rotation, closing rules - sized to the capacity the maintainers actually have.

The queue is not out of control because the labels are wrong. It is out of control because inflow exceeds available attention and no written rule says what happens to the difference. Make that arithmetic explicit, then design around it.

Machine-generated submissions broke one side of it in 2025. RedMonk's Kate Holterhoff named the asymmetry for security reports (May 2026): "generating a plausible-sounding vulnerability report now costs pennies in tokens. Evaluating whether it's real still costs an hour of expert time." Inflow is no longer bounded by human effort while triage capacity still is, so every design needs a planned answer for volume, not only for classification.

Do not triage individual items, curate the first-contribution queue, review code, or handle conduct incidents. Route those elsewhere:

- First-contribution path, good first issues: samber/developer-relations-skills@oss-contributor-onboarding
- Repeat questions into docs: samber/developer-relations-skills@developer-troubleshooting-docs
- Hostile behaviour: samber/developer-relations-skills@developer-community-moderation
- Who decides scope: samber/developer-relations-skills@oss-governance
- The wider measurement framework: samber/developer-relations-skills@developer-community-health

## Interview

Ask one at a time, multiple-choice where you can, skipping what the user already answered. Questions 1-6 gate everything; without them you design a process for an imaginary project.

1. What is the effort ceiling: how many people triage today, how many hours a week can each give in a bad month, and may anyone add triagers or change tracker settings?
2. Is there a date this has to hold by - a release, an audit, a response target already published to someone?
3. Do you want this backlog cleared, or a system that still works next year with different maintainers?
4. How large is the queue: open issues, open external pull requests, age of the oldest?
5. What does the inflow look like - mostly bug reports, feature requests, or usage questions?
6. Is the project volunteer-run, company-backed, or mixed, and does anyone have a contractual response obligation?
7. Which tracker, can you change labels, templates and automation on it, and what exists today (labels, templates, contributing guide, bots)?
8. Do external pull requests count as triage work here, or does a separate review process own them?
9. Has the share of low-quality or machine-generated submissions grown in the last year, and can you estimate it?
10. Where do security reports arrive today - the public tracker, a private channel, or nowhere defined?
11. Where should usage questions go instead - a forum, a chat, discussions, nowhere yet?
12. Who may close an issue, who decides what is out of scope, and what made you open this now?

If question 1 answers effectively zero hours, stop designing and say so: the honest deliverable is a reduced intake plus a published "this project is in maintenance mode" statement, not a taxonomy nobody will apply.

Answers to 1, 2 and 3 re-rank every menu below; say which moved what.

- Hard date: promotes what acts this week (shorten the promise, chooser routing, the direction check); demotes anything paying off over a quarter.
- "Still works next year": promotes adding triagers and validated forms, both of which lose on ratio inside any single month.
- Low effort ceiling: deletes options rather than demoting them - with no authority to add people, add-triagers is not a lever and must not appear in the deliverable.

## Step 1 - Measure the queue before changing it

Export the tracker's issues and run the baseline; every later decision references these numbers.

```bash
gh issue list --state all --limit 2000 \
  --json number,title,state,createdAt,updatedAt,closedAt,labels,author,comments > issues.json
python3 scripts/triage-baseline.py issues.json --triage-prefix "kind/,priority/"
python3 scripts/triage-baseline.py issues.json --stale-days 120 --format json > baseline.json
```

It reports, from JSON arrays, JSON Lines or CSV:

- open count
- age median/p90
- untriaged share
- inactive count
- median and p90 time to first human response
- created-versus-closed flow
- label usage, including single-use labels

Without a scriptable environment, sample 50 open items by hand and estimate the same numbers - an estimate beats designing blind, and without a baseline you cannot tell whether the redesign worked.

Read the numbers back before proposing anything: a queue that is 80% usage questions needs a different intervention from one that is 80% unanswered bug reports.

Then ask what the per-item framing hides: **do these items cluster?** On a large stale backlog, grouping issues by shared root cause under a tracking issue and redirecting the rest to it often clears more queue than triaging item by item. Decide per-item versus clustering here, before designing the per-item machinery.

## Step 2 - Do the capacity arithmetic

Multiply triagers × sessions per week × minutes per session ÷ minutes per item, and compare against the baseline's inflow.

Do not import a minutes-per-item constant. Time the pilot session in step 9 and use the project's own number; until then, three minutes is a planning placeholder this skill sets, not a measured industry figure. Deep investigation is not triage - it is work triage schedules.

When capacity is below inflow, no label scheme fixes it. Three levers close the gap; pick by queue relieved per maintainer hour, not by which is quickest to type:

- efficiency: cut intake > shorten the promise > add triagers
- effort: shorten the promise (rewrite one line, defend it once) > cut intake (a day of forms and chooser configuration) > add triagers (recruit, grant permissions, calibrate - a quarter before a new triager is net positive)
- value: cut intake (permanently lowers the left side of the arithmetic) > add triagers (the only lever that raises capacity at all) > shorten the promise (nothing improves; the promise merely stops being broken)
- compliance cost: cut intake == add triagers (tied because both are internal decisions with no external counterparty) > shorten the promise where question 6 found a contractual obligation, since there the published target is a commitment and shortening it is a contract change

Efficiency starves adding triagers - the only lever that raises capacity, and the slowest to pay. Promote it whenever the project expects to still exist in a year: one that only ever cuts intake shrinks itself to fit its worst month. State the chosen lever in the deliverable so the user is not surprised in three months.

Decide the **volume-gating trigger** now, while nothing is on fire: the inflow rate or valid-report share at which the project will restrict who may open items, cap open submissions per author, or change the incentives that attract volume. Projects that adopted gating reached for it only after burnout was acute; deciding the trigger at design time makes it policy instead of crisis improvisation. [./references/worked-examples.md](./references/worked-examples.md) walks curl's collapse to a one-in-twenty valid share through this arithmetic, and shows why its answer acted on the economics of submitting rather than the speed of triage.

Set the first-response target from the capacity number, not from ambition - a human reply, not a fix and not a bot greeting. The arithmetic, volunteer-versus-company-backed differences and contractual obligations: [./references/policy-and-metrics.md](./references/policy-and-metrics.md).

## Step 3 - Design the label taxonomy

Build labels as orthogonal axes - type, state, priority, area, contributor-facing - with at most one value per axis on any item. State moves the queue; priority starts arguments, so keep it as small as the project can bear.

Size the set against the reference points in [./references/published-findings.md](./references/published-findings.md):

- ten default labels on a new repository
- five state roles plus two categories in the most-installed triage skill
- six prefixed families at Kubernetes scale

Mapping those onto a project is this skill's judgment, not a sourced rule: the honest answer usually sits between the first two and approaches the third only when ownership is genuinely split.

Two rules come from PyTorch's taxonomy - the only documented running in production, on PyTorch's own main repository:

- **Gate labelling on confidence.** Apply a label at high or medium confidence; at low confidence apply a "needs review" state instead of guessing. A guessed area label sends the item to the wrong owner and costs more than no label.
- **Never let automation apply the top priority level.** Route every candidate for it to human confirmation instead. Priority is the axis with the most downstream consequence and the least machine-checkable definition.

Axes, sized starter sets, naming rules, cleaning up an existing label mess without erasing history, the allowlist-and-validation pattern, and tracker mechanics: [./references/label-taxonomy.md](./references/label-taxonomy.md).

Present the taxonomy for approval before touching the tracker - one imposed on maintainers who did not agree to it decays within a month.

## Step 4 - Cut the intake

Capacity spent on items that should never have arrived is the largest reclaimable block. Rank the four cuts by triage minutes reclaimed per hour of setup - no compliance-cost axis applies, since none of the four creates an obligation to anyone:

- efficiency: chooser routing > validated forms > disabling blank issues > auto-applied type label
- effort: disabling blank issues == auto-applied type label (one setting, one line of form YAML) > chooser routing (needs a destination that may not exist yet) > validated forms (one form per real category, written, tested and revised when reporters skip fields)
- value: chooser routing (removes whole categories instead of speeding them up) > validated forms (turns two round-trips into one submission on every bug report, forever) > disabling blank issues (closes the bypass that makes forms optional) > auto-applied type label (one axis, seconds an item)

1. **Chooser routing** - usage questions to a forum or chat, commercial requests to a sales contact. A stopping condition: a routed report never reaches the tracker, so steps 5-8 never touch it.
2. **Validated forms** replacing markdown templates. Require exactly the fields that change the outcome; every optional field a reporter skips teaches them the form is decorative.
3. **Disable blank issues** once the forms cover the real categories.
4. **Auto-applied type label** from the form, plus the issue type where the tracker has one.

Efficiency starves option 2: highest recurring value, most setup, so a maintainer with one free evening does the toggles instead and the round-trips continue. Promote it to first when bug reports dominate inflow, where that cost is paid on every item. A project with nowhere to route usage questions (question 12) has no option 1 - delete it from this pass rather than listing it as pending work.

**Security reports leave the tracker entirely.** Every mature project examined runs the same three-element pipeline, separate from general triage:

- a private intake channel
- a named, size-capped response team
- an embargo mechanism for coordinated disclosure

Apache instructs committers never to enter vulnerability details in a public tracker. With no security list, the code host's private vulnerability reporting is the default.

Form capabilities, chooser configuration, the full security path and the volume-gating options: [./references/issue-intake-and-routing.md](./references/issue-intake-and-routing.md) - read it before writing form YAML.

## Step 5 - Assign the duty

An unowned process is not a process.

1. Name who triages, in a rotation with a stated shift length (a week is the common unit) and a named backup. Mozilla's two-tier model is the most robust documented pattern: a long-term **triage owner** accountable per component, plus a **triage duty** rotating weekly that does the work.
2. Fix a cadence and a stop rule: a session ends at its time box, not at inbox zero, so triage survives a spike.
3. Set the session order: newest untriaged first (protects the response target), then items where the reporter replied, then a fixed backlog quota.
4. Grant triage-level permissions rather than commit access - most trackers have a role for labelling, closing and assigning without write access, which is how a triage team grows past the committers.
5. Define the escalation: what a triager decides alone, what waits for a maintainer, how long that wait may be.

Three things decide whether a recurring triage meeting survives:

- a queue view built for it
- asynchronous pre-triage, so the meeting is decision-making rather than first contact
- decisions recorded as label or state changes rather than only in minutes

Rust's compiler triage meeting is the clearest example: a Zulip stream pre-triages and priority is set by replacing a label, so the output stays queryable.

## Step 6 - Give pull requests their own gate order

A pull request carries hard automated checks an issue never has; do not reuse the issue process.

Two gates are not menu items, since both are automated preconditions that fire before a human looks:

- sign-off (CLA or DCO)
- CI permission for externally authored PRs

Nothing merges without sign-off, because the licence provenance it records is the project's only account of where the code came from.

Rank the three gates that spend maintainer attention by rejections settled per minute of reviewer time - not cheapest first, which buries the direction question under the machinery:

- efficiency: direction check ("does this belong in the project") > size-based risk label > code-correctness review
- effort: direction check (a minute on title, description and linked issue) > size-based risk label (computed from the diff, but it only sorts) > code-correctness review (the expensive pass this order exists to protect)
- value: code-correctness review (the only gate that can accept a change) > direction check (settles the rejections that were never about code) > size-based risk label (routes; decides nothing)
- compliance cost: direction check == size label (tied: a maintainer reading a description and a bot measuring a diff both leave the project owing nothing) > code-correctness review (accepting a change makes the project answerable for its provenance and security posture, which is what sign-off documents)

The direction check leads because roughly two-thirds of rejected agentic PRs never needed the code read at all - the MSR 2026 mining study's breakdown of 353 manually inspected rejections is in [./references/published-findings.md](./references/published-findings.md).

Efficiency starves the code-correctness review: highest value, highest effort, permanently last. Promote it to first when a trusted repeat contributor sends a small change against an already-accepted issue - the direction question is answered before the PR opens, and running the order costs more than the read.

The per-item decision path, reply templates with weak/strong pairs, the PR deltas and the rejection knowledge base are in [./references/response-playbook.md](./references/response-playbook.md).

## Step 7 - Write the closing and staleness policy

Decide explicitly what closes automatically and what never does. The defensible line: auto-close only items waiting on a reporter who stopped replying; never one waiting on the maintainers - a confirmed bug closed by a bot tells the reporter their evidence was worthless.

Configure the sweep:

- restrict it to the waiting-on-reporter state only
- exempt the confirmed and blocked states
- warn before closing
- run the first pass in dry-run mode, so the blast radius is known before it fires

Every close carries a reason and says how to reopen.

Anchor each clock to a named waiting party rather than to the item in the abstract. Kubernetes' published clocks, the sweep configuration, and when a one-time backlog bankruptcy is legitimate: [./references/policy-and-metrics.md](./references/policy-and-metrics.md).

## Step 8 - Automate classification, never the first reply

Automate the mechanical layer first, deterministically:

- fill the area label from changed paths
- apply the type from the form
- request review from the owning team
- run the staleness clock

Every documented machine-learning triage deployment keeps a human as final decision-maker: treat model assistance as a scoring and suggestion layer, never an autonomous accept, reject or close.

Copy two patterns before considering any classifier:

- **Automate who is on duty, not what to decide.** Mozilla syncs the triage-owner field to whoever is on the rotation calendar, so requests reach the person actually working rather than piling on one name.
- **Hold the label set as a validated artifact**, so automation cannot invent labels or overwrite human work - mechanics in `label-taxonomy.md`.

Leave the first human sentence to a human. Response metrics exclude bot replies by definition and reporters discount them the same way; an auto-greeting followed by three weeks of silence makes the wait worse. When an agent posts triage comments, disclose it in the comment.

## Step 9 - Publish, run a pilot pass, measure

Publish the policy:

- write it into the repository, next to the contributing guide
- link it from the intake forms
- announce the change once, in the project's own channel

Run one real triage session with the user against the new system on 15-20 items, and time it. That produces the minutes-per-item figure step 2 deferred and exposes what the design got wrong - a missing state, an ambiguous label, a reply template that does not fit. A policy never executed once is a draft.

Re-run `triage-baseline.py` monthly for the first quarter, and iterate against three starting targets. All three are this skill's self-set baselines, not industry benchmarks - replace each with the project's own measured trend once a quarter of data exists:

- Untriaged share below 10% of open items.
- Published first-response target met on at least 90% of items.
- Net inflow at or below zero over the quarter.

Iterate until they hold, or lower the published promise to one that does.

Never read a count metric alone. CHAOSS's guidance restricts these measures to activity "primarily driven by humans", and, under machine-generated volume, closure ratios and time-to-close can improve while real maintainer burden rises. Pair every count with a human-driven signal: first response with bots and author self-replies excluded, and how many people could cover triage if one person left.

With persistent memory available, store the durable decisions:

- capacity numbers
- the agreed response target
- the label axes and their definitions
- categories routed off the tracker
- the volume-gating trigger
- declared out-of-scope requests

The next review is a diff against those.

## Invocation examples

| The user says                                        | You produce                                                                                                                         |
| ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| "We have 900 open issues and no idea where to start" | Run the baseline, read it back in plain language, then make the per-item-versus-clustering call - no taxonomy yet                   |
| "Design a triage process for our maintainer team"    | All five deliverable artefacts, in order, validated one by one                                                                      |
| "Our labels are a mess, redo them"                   | Label usage counts first, then a change list of create/rename/merge/delete with one definition and one axis per label               |
| "Should we turn on a stale bot?"                     | The waiting-on-reporter-only rule, a dry-run first pass, and the exempt-state list - plus a refusal to sweep maintainer-owned items |
| "Nobody answers PRs from outside contributors"       | The gate order from step 6 and a separate PR response target - not the issue process reused                                         |
| "We are drowning in AI-generated reports"            | The volume-gating trigger from step 2, intake economics, and the platform controls - before any classifier                          |

## Deliverable

Produce these five artefacts in order, each validated with the user before the next - never all in one silent pass:

1. **Baseline** - step 1's numbers, the one-line reading of them, and the per-item-versus-clustering call.
2. **Triage policy** - the published document: what belongs in the tracker, the response target, the states and their meanings, when items close, who triages, the volume-gating trigger. Template in [./references/policy-and-metrics.md](./references/policy-and-metrics.md).
3. **Label change list** - create, rename, merge, delete, each with a one-sentence definition and its axis.
4. **Intake change list** - forms to add or rewrite with required fields, chooser routing entries, the security path, automation to enable, each with the triage minutes it should save.
5. **Duty and gate design** - the rotation with named people and shift length, the escalation rule, the pull-request gate order.

Keep every artefact in the project's own vocabulary - real label strings, real channels, real maintainer names.

## Failure modes

Each row names a failure the steps do not already spell out; the fix is the whole row.

| Failure                                                       | Fix                                                                  |
| ------------------------------------------------------------- | -------------------------------------------------------------------- |
| Aspirational target - "24-hour response" from two volunteers  | Publish the number the baseline supports                             |
| Dormant rotation - a documented rota nobody has run in a year | Give it an owner and a liveness check; retire it loudly if it lapses |
| Priority theatre - everything is `priority/high`              | Two or three levels, defined by consequence                          |
| Big-bang migration - new labels, old forms, old saved views   | Migrate labels, forms, views and automation in one pass              |
| Triage as fixing - a session spent debugging one item         | Time-box the pass; triage schedules work; it is not the work         |
| Unmeasured redesign - new process, no idea whether it helped  | Re-run the baseline monthly                                          |

## References

- [./references/label-taxonomy.md](./references/label-taxonomy.md) - axes, starter sets, cleanup procedure, tracker mechanics.
- [./references/issue-intake-and-routing.md](./references/issue-intake-and-routing.md) - form fields, chooser, off-tracker routing, security path.
- [./references/response-playbook.md](./references/response-playbook.md) - per-item decision path, reply templates, rejection knowledge base.
- [./references/policy-and-metrics.md](./references/policy-and-metrics.md) - capacity arithmetic, policy template, closing rules, measurement plan.
- [./references/worked-examples.md](./references/worked-examples.md) - a worked capacity read and a positive/negative rotation pair.
- [./references/published-findings.md](./references/published-findings.md) - which figures are sourced and which are self-set baselines.
