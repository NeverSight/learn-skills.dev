---
name: mux-work
description: Take a queued Mux issue from shaping to a brief, then start its build. Use when the user runs /mux-work with an issue.
argument-hint: "<owner/repo#n or issue URL>"
disable-model-invocation: true
---

You run one item of the Mux factory. Pedro answers questions, picks prototypes,
verifies visible changes and merges every PR. Everything else is yours.

## Rules

- Move the issue's Status on the "Mux" board at every step with
  `bash <this skill>/scripts/status.sh <owner/repo#n> "<Status>"`. Statuses:
  List, Queued, Shaping, Needs you, Ready, In progress, Review, Verify,
  Ready to merge, Done.
- Facts are yours to find, decisions are Pedro's. Read code, docs and history
  in **subagents**, so no thread holds whole files. Every factory subagent
  report is ≤300 words and never pastes whole files, logs or screenshots. Ask
  Pedro only what a subagent can't answer.
- Every question to Pedro goes through the question UI (`AskUserQuestion`), so
  T3 shows the thread as waiting: Size up, grilling rounds, the prototype pick,
  Gate assumptions, Doubt findings, Concepts, `decision: grill`, and the
  builder's stops and retro picks. If the tool is deferred, load it with
  `ToolSearch`; if it isn't available, ask in the `grilling` chat format.
  For retro picks and their clarifications, preserve the source issue's final
  status throughout questions, capture, retries and failure reporting. Use
  [Retro capture](retro-capture.md) as the answers record; skip steps 1–3 below.
  For other questions, run these steps once per batch, however many calls it takes:
  1. Set **Needs you**, then make the question UI calls; each blocks.
  2. After the last call, comment the answers on the issue in one comment
     (summarise; never copy secrets, tokens or private hostnames).
  3. Set the status back to the one the step was in: Shaping while shaping,
     In progress or Review in a build.

  Map the `grilling` format onto the call, and don't repeat it in chat:
  - question: `Qn - <title>: <body>`, worded so "yes" accepts the
    recommendation;
  - first option: the recommended answer, its label ending `(Recommended)`,
    the reasoning in its description. The other options are the real
    alternatives; "Other" stays for free text. Mark nothing `(Recommended)`
    when there's no honest recommendation (a prototype pick);
  - at least 2 options. A confirmation like Size up gets "Confirm" and
    "Correct it". If he picks "Correct it" without text, ask what to correct
    in a follow-up call of the same batch;
  - `header` at most 12 characters, option labels 1–5 words plus
    `(Recommended)`;
  - at most 4 questions per call. Split a longer batch (a grilling round, Gate
    assumptions, Doubt findings) into consecutive calls and keep the numbering
    going, so a round still asks the whole frontier;
  - retro picks: `multiSelect` questions whose options are the suggestions,
    none `(Recommended)`, at most 4 each, spread so each has at least 2; add
    "None" when one is left alone. No suggestions, no question.
- The issue is the only hand-over. Each step must be resumable from the issue
  alone: the brief, the map, decisions and links live in its body and comments.
- Past about 150k tokens, a thread hands off: write a handoff following
  `~/.agents/skills/handoff/SKILL.md`, post it as an issue comment, and continue
  in a fresh thread with `t3_thread_launch`.
  - Shaping thread: `/mux-work <issue>`, root workspace.
  - Build thread: only while work before the PR step remains (slices, merges, a
    review round); otherwise finish in place (PR, status, retro). Past the
    mark, start no new implementers; merge the running ones, then hand off.
    Launch with
    the message from **5. Start the build** and `workspaceStrategy`
    `{"type":"existing_worktree","worktreePath":"<build worktree>","branch":"<build branch>"}`.
    The handoff names the step and review round to resume at; the open slice
    sub-issues carry the remaining state. At a review round it also lists each
    reviewer's verdict, the open findings and the rejected findings with
    reasons.
- Never merge, never push to `main`. Commit and PR rules are in each repo's
  `AGENTS.md`.

## Grilling with docs

Wherever this skill grills (open questions in **2. Size up**, **Concepts**
step 1, `decision: grill`), load `grilling` and `domain-modeling`, the pair
upstream `grill-with-docs` loads. Challenge Pedro's terms against the repo's
`GLOSSARY.md` and ADRs, and capture each resolved term and ADR-worthy decision
the moment it settles, as `domain-modeling` says.

Shaping, concept and decision threads run in the repo's main checkout, with no
branch and no PR, so they write only to the issue and leave the checkout as
they found it. Where `domain-modeling` says to update `GLOSSARY.md` inline or
write an ADR, draft the entry instead: capture it as it settles, record it in
the batch's answers comment, then put it in the **Domain docs** section of the
brief (**3. Brief**) or the map (**Concepts**). Drafts follow `domain-modeling`'s `GLOSSARY-FORMAT.md`
and `ADR-FORMAT.md`, and an ADR draft meets its three conditions. The builder
writes them to the repo in the build PR.

## Screenshots

Keep review screenshots outside the checkout, in `${TMPDIR:-/tmp}/mux-<n>-ui/`,
and show them to Pedro in the build conversation with absolute file paths.
Never commit review screenshots or add them to PR descriptions or comments.
PR evidence is a text summary of the visual checks and their results, even when
the `pr` skill suggests screenshots. Required test fixtures and product assets
follow the repo's rules; they are separate from review captures.

## 1. Pick up

Read the issue with comments, parent, sub-issues and blockers. Then:

- **Unfinished retro capture record**: before any route below, including a
  passing brief, follow [Retro capture](retro-capture.md) to finish only the
  pending capture. Preserve the source status; do not rerun its build or retro,
  start shaping, or launch another thread. Report links and pending failures,
  then end this pickup, even if capture completes.
- A `decision: *` sub-issue: go to **Decisions** below.
- A `build` sub-issue, or any issue whose body already has a passing brief: go
  to **5. Start the build**.
- Anything else: set Shaping and start an **Explore subagent**: read the repo's
  `AGENTS.md`, `GLOSSARY.md`, relevant ADRs and the code this issue touches;
  return at most 300 words on what exists, where, and what the issue would
  change. Use `domain-modeling` vocabulary.

## 2. Size up

Decide the route yourself. Never ask Pedro to pick a route by name. Ask him to
confirm it (question UI, **Rules**), in a few lines:

- what you understood the item to be;
- the open questions you found, or "none";
- what happens next, in plain words. For example: "I'll ask you three
  questions, then write the brief", or "a subagent reproduces the bug first; I
  only ask you if the expected behaviour is unclear", or "this is too big for
  one session, so I'll turn it into a concept map".

Add the kind label (`bug`, `feature`, `improvement`, `concept`). Pedro confirms
or corrects; anything he adds is another open question. Before applying a missing
label, run [label setup](issue-tracker.md#label-setup) in the issue's repository.
Then:

- **Bug**: first start a **Diagnose subagent** with the `diagnosing-bugs` skill.
  It returns the cause, the evidence and a failing test to write. Its open
  questions join the list.
- **Open questions**: settle every one here in this thread by **Grilling
  with docs**, through the question UI, for bugs and features alike. When a
  question is about how something looks or feels, start a **Prototype subagent** with the `prototype` skill in its own
  worktree on a `prototype/<n>-<slug>` branch: two or three variants that differ
  only on that question. Tell Pedro how to open them (T3 browser preview for
  web, the run scripts in the repo's T3 project for Apple), ask for his pick
  through the question UI, and record it and the branch on the issue.
- **No open questions**: go straight to the brief.
- **Too big or unclear for one session**: go to **Concepts**.

## 3. Brief

Replace the issue body with the brief. Keep Pedro's original text under a
collapsed `<details>` block at the end.

```markdown
## What
<the change, in Pedro's domain language>

## Done when
- <observable result a reviewer can check>

## Confirmed
- <each assumption Pedro confirmed, and each decision with a link>

## Notes for the builder
<where the code is, the failing test to start from, prototype branch to follow>

## Domain docs
- Glossary: <each term to add or change, as a GLOSSARY-FORMAT.md entry>, or "none"
- ADRs: <each ADR to write, as an ADR-FORMAT.md draft>, or "none"

## Verify
<"yes" with why (visible, auth, migrations, deployment, hard to check), or "no">
```

## 4. Gate

1. Start a **Doubt subagent** with the `doubt-driven-development` skill. Give it
   only the brief and the repo path, no conversation. It tries to show the brief
   is wrong, ambiguous or incomplete, and that its **Domain docs** agree with
   the repo's `GLOSSARY.md` and ADRs, with every ADR draft meeting
   `domain-modeling`'s three conditions. Fix what it finds.
2. Ask Pedro, in one batch, every assumption he hasn't confirmed and every
   Doubt finding you can't fix yourself.
3. Set **Ready**.

## 5. Start the build

Start a new T3 thread for the build with `t3_thread_launch`:

- `workspaceStrategy`: `{"type":"worktree","baseRef":"main","branch":"<kind>/<n>-<slug>","startFromOrigin":true}`
  in the issue's repo project, where `<kind>` is `fix`, `feat` or `chore`;
- `message`: `Build <owner/repo#n>. Read <this skill>/agents/builder.md and follow it.`
  with the absolute path of this skill.

Tell Pedro the build thread's link. This shaping thread is done.

## Concepts

Run [label setup](issue-tracker.md#label-setup) for the map's repository before
creating or labelling the map and its sub-issues. Use the guide's explicit
destination selection for sub-issues that belong in another repository.

The issue becomes the **map** and gets the `concept` label. Its body:

```markdown
## Destination
<what is true when this is done>

## Decisions so far
- <gist> (#n)

## Fog
- <what we don't know yet, and can't phrase as a question yet>

## Out of scope
- <what this won't do>

## Domain docs
- <each glossary entry and ADR draft settled so far, with its decision (#n)>, or "none"

## Map
<Mermaid flowchart of the sub-issues: decisions and builds, edges for
blocked-by, closed ones styled done. Redraw it whenever a sub-issue changes.>
```

1. Grill Pedro (**Grilling with docs**) only on the destination and the
   out-of-scope list.
2. Create a sub-issue for each decision you can phrase now, labelled
   `decision: grill`, `decision: prototype`, `decision: research` or
   `decision: task`, linked with blocked-by where one needs another
   (see [native relationship commands](issue-tracker.md#native-relationships)).
   Put them in Queued. Leave the rest in Fog.
3. For `decision: research`, start the research now with the `research` skill in
   the background. Findings go on a `research/<n>-<slug>` branch; link it from
   the sub-issue.
4. Set the map to Shaping while decisions are open. Each decision runs in its own
   thread with `/mux-work <sub-issue>`.

### Decisions

Work one decision sub-issue with the method its label names (**Grilling with
docs**, prototype, research findings, or a small task). Then comment the answer
with any Domain docs drafts it settled, close it, add its gist to the map's
Decisions so far and its drafts to the map's Domain docs, and redraw the map.
Turn fog that became clear into new decision sub-issues. When a part of the
destination is fully decided, create a `build` sub-issue for it with a brief
(**3. Brief**) whose Domain docs copies the map's entries that build needs, run
the gate, set it Ready, and start its build (**5**). The map is done when the
fog is gone and every build has merged.
