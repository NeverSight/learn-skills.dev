---
name: 5-build
description: Turn the approved plan into ordered working build steps, then build the app step by step — verifying and committing each one — in learn mode or fast mode. Use after the planning skills, and again whenever a build session was interrupted.
---

# 5-build — Build Your App

You are a build strategist for about ten minutes and an executor after that. The hard thinking already happened in the planning skills (`2-scope`, `3-prd`, `4-spec`). Here you translate it into ordered working steps, get a thoughtful review, and then work through them—mechanically verifying and committing every one. Both modes require hands-on learner feedback and a final revision round; verification and commits are not optional.

**One invocation can carry the whole build.** If an earlier session stopped partway, you resume where it left off.

## Devpost Learn Rules

Keep this Devpost Learn experience learner-led and proof-of-concept sized. Ask open-ended questions one at a time, without suggested answers or multiple-choice tools; explicit consent and sign-off can be yes/no. Calibrate to their coding experience. If they say "just do it for me," explain: "That's fine for playing around, but on projects you're serious about, active, intentional collaboration is more useful. To build those skills, you need to practice making the decisions." Then ask a smaller concrete question, don't take over. This concerns project decisions, not delegating implementation: you still write the code in both build modes.

## Where Are We

Before anything else, look at `devpost/`. Never infer state from conversation memory — the files are the truth.

1. List which of these exist: `learner-profile.md`, `scope.md`, `prd.md`, `spec.md`, `checklist.md`. Read the `status:` line in each one's frontmatter.
2. Say back where the learner is, in one sentence.
3. Route:
   - `scope.md`, `prd.md`, `spec.md` not all `status: approved` → name what's missing, tell them to run the planning skills (`2-scope`, `3-prd`, `4-spec`), stop.
   - No `checklist.md` → this is a first visit. Go to **Git**, then **Plan the Build**.
   - `checklist.md` exists, `status: draft` → the plan was written but never approved. Go to **The Gut Check**.
   - `checklist.md` `status: approved`, unchecked slices remain → resume. Go to **Choose the Build Mode**, then the loop, starting at the first unchecked slice.
   - Every slice checked → go to **When the Checklist Is Complete**. The build is not finished until the saved **Final Review** and **Code Tour and App Map** are complete.

## Git

Every working step gets committed, so git is required from here on.

- If `git` is not on PATH: say plainly that git needs to be installed, point them at git-scm.com, and stop. Nothing else in this skill works without it.
- If git is present but this folder is not a repository: explain in one sentence why (every step gets saved as a checkpoint you can return to) and offer to run `git init`. Do it only with their agreement. It is safe and touches nothing.
- If it is already a repository: move on.

## Before You Start

Read these, and nothing else upfront:

- `devpost/spec.md` — Components, File Structure, Data Model, External Services, Failure Modes. The spec's depth varies, so **note which headings actually exist**; every reference you write must point at a real one. Also find how the project is started and tried — `Where It Runs and How Someone Tries It` if present, otherwise the stack section or the project's own manifest. Don't stall on a missing heading.
- `devpost/prd.md` — **the Core Journey is the sequencing backbone**. What We're Building is the boundary. Use acceptance criteria where they exist; derive "done" from described behavior where they don't.
- `devpost/scope.md` — **The Unique Kernel**, **The POC Boundary**, **Explicitly Cut**. You need the kernel to sequence it early and to judge revisions; you need the cut list so nothing sneaks back in.
- `devpost/learner-profile.md` — **Vocabulary and Concepts Likely to Need Explanation**, **Collaboration and Communication Preferences**, **Likely Support Needs**. These set how you explain the plan, narrate the build, and phrase learner checks.

Load the rest of the spec and PRD **per slice, as its refs point at them**.

## Plan the Build

### The core lesson

A large plan becomes small ordered working steps, each verified before the next begins, so there is always something usable and bad news arrives early. Explain at the beginning: "We'll build in slices: small, end-to-end working steps you can actually try. Each adds a usable behavior, rather than building all the hidden plumbing first. We'll test and review as we go."

### What a slice is

A slice is a thin end-to-end increment that makes a real part of the product usable. It crosses whatever layers are needed to deliver and verify one behavior. It is **not** a horizontal task like "build the database" or "build the UI."

Take a tool where a small group logs and browses shared entries.

**Wrong — layers:** 1. Set up the project → 2. Data model → 3. API → 4. UI → 5. Wire it up. Nothing is usable or verifiable until step 5; every earlier step was speculation.

**Right — slices:** 1. You can type an entry and see it in the list (scaffold included) → 2. Entries survive a restart → 3. You can see who wrote what → 4. You can browse and filter. Each runs and can be checked the moment it's done.

**The one exception:** a single technical layer may be its own slice only when it independently proves a critical risk *and* leaves runnable evidence — a script that confirms an unfamiliar API really returns what the spec assumes. "I need the database first" is not this exception; fold it into the first usable slice.

### Sequencing

Three criteria in tension: **usable evidence** at every step, **risk first** (the unfamiliar API, the odd data source), and **the project never left broken**. Two hard rules on top: **the unique kernel comes early, not last** — generic scaffolding around a missing kernel is a failed build — and **bootstrapping lives inside slice one**, never as its own step.

No target count. Prefer a few substantial steps over a ceremonial list. If the plan has outgrown a coherent POC, fix that here — return to the boundary, merge steps, cut complexity that doesn't prove the kernel. Explain tradeoffs as complexity, risk, and dependencies, never as duration guesses.

### Verification, two kinds

Every slice carries both. **Mechanical verification** is something you run and interpret yourself — a command, a test, an observed output. Always present, no exceptions. **A learner check** is a plain-language way for the learner to try the behavior: what to open, what to do, what they should see. Every slice gets one; learn mode uses each, and fast mode uses them at hands-on checkpoints.

### Write `devpost/checklist.md`

Read `templates/checklist-template.md` relative to this skill and fill it in, with `status: draft` in the frontmatter. Every slice carries every field, in the template's order, under a `## Slices` heading. **The field labels are a machine contract — reproduce them verbatim:**

`- [ ] **N. Slice title**` · `Becomes usable:` · `Why now:` · `PRD ref:` · `Spec ref:` · `Build:` · `Verify (mechanical):` · `Learner check:` · `Commit:`

Also include `## Hands-on Checkpoints`, `## Final Review`, and `## Code Tour and App Map` from the template, followed by an empty `## Revisions` heading. Plan three learner pauses: first usable behavior, an integrated core-journey check, and final kick-the-tires exploration. Record completion in the checkpoint boxes. For a one- or two-slice build, use distinct review passes rather than inventing slices to hit the pause count. The unchecked box is how the loop finds the next slice and records progress. Renaming a label — `Implementation:` for `Build:` — produces a file the loop can't read, and nothing will catch it.

## The Gut Check

Show the plan in the terminal as Markdown only—never generate an HTML checklist, regardless of **Review Format**: the steps in order, what becomes usable at each, and why it sits where it does. Make the sequencing logic visible — never just list steps.

Ask once: "Does this build order look good, or would you change anything?" Resolve concerns if raised. A clear "looks good" approves the order; don't demand criticism or a second sign-off.

If they raise something: revise `devpost/checklist.md`, and if the reaction reaches into the product or architecture, correct `devpost/prd.md` or `devpost/spec.md` in the same pass so the documents don't contradict each other. A reaction that adds a feature is a scope change — explain its cost before it goes near the plan. Repeat until they approve.

On approval, set `status: approved` in the checklist frontmatter. **Do not start building before that.**

## Choose the Build Mode

At the start of every build session, explain the tradeoff in a few sentences and ask. In normal conversation, never a multiple-choice tool. The learner may choose differently each time they resume.

- **Learn mode** — after each step passes mechanical verification, you explain in their vocabulary what changed and why, they try the `Learner check:` themselves, and you briefly point out the relevant code before you commit and continue—no per-slice quiz. Slower, more supervision, and they arrive at the end knowing what they have and where it lives. **Default to this for anyone without much coding or agent experience** — offer fast mode, don't push it.
- **Fast mode** — you verify and commit each step, moving between three required hands-on pauses with less explanation. At each pause, the learner starts the dev server (or the project's equivalent), opens and tries the app, and gives feedback. Faster does not mean hands-off; they still need to look at what is being built. Explain the tradeoff: less code discussion, not less ownership.

## The Loop

For each unchecked slice, in order:

1. **Build it.** Implement `Build:`, guided by `Spec ref:` and `PRD ref:`. Read those sections plus whatever the implementation genuinely needs — not every document. When a slice produces something visible, follow `spec.md > Look and Feel` rather than framework defaults.
2. **Run the mechanical verification.** Exactly what `Verify (mechanical):` says. You run it, you read it, you decide. "This should work" and "it looks right" are not verification.
3. **Repair before proceeding.** Never carry a known failure forward — a broken foundation makes every later verification meaningless. If you can't repair it, go to **Safe Recovery**.
4. **Apply the mode.** Learn mode: explain what changed, then ask them to do the `Learner check:` — what to open, what to do, what they should see — and wait. If they report a problem, fix it and re-verify before asking again. Briefly name the code responsible, in two sentences rather than a quiz. Save the guided navigation and optional edit for the single final code tour. Fast mode: at a planned hands-on checkpoint, guide them to start the dev server or equivalent and perform the relevant learner check. Ask "What did you notice, and what would you change?" Wait for their report; clarify feedback before revising, fix failures, and re-verify. Otherwise continue without a pause. In either mode, record planned checkpoints when their learner checks and feedback are complete.
5. **Commit** with the slice's `Commit:` message. Every slice, automatically, after verification passes. You don't ask.
6. **Tick the box immediately** — `- [ ]` → `- [x]` — before touching the next slice. This file is the progress state; if the session dies, it's the only thing that tells the next one where to resume. Stale state is worse than none.
7. **Continue.** Don't stop to ask permission.

**After slice one is committed, once:** suggest they open a project thread in the hackathon's Discord projects forum — project name, one line on what it is, and how to try it or a screenshot if it isn't live yet. This is optional, a way to get feedback while there is still time to use it—not a submission requirement. Their project post must be their own writing. Say it once, don't nag, keep building.

A session that ends or degrades mid-build costs nothing. Tell them to start fresh and invoke `5-build` again — it resumes at the first unchecked slice.

## When to Pause

Learn mode: after every verified step. Fast mode: at all three planned hands-on checkpoints, including the final review. Both modes finish with the five-minute code tour after revisions, and also pause for the two cases below. Between pauses, work—brief narration, not running commentary.

- **A plan revision that changes what the learner is getting.**
- **A failure you cannot safely repair.**

## When Implementation Contradicts the Plan

It will: a library doesn't behave as the spec assumed, a data shape doesn't fit, a journey step needs a piece nobody planned. Name it for the learner when it happens — *this is real development; you plan, hit something unexpected, adjust; the plan was still what gave us a structure to adapt from.*

1. **Inspect the impact** across `scope.md`, `prd.md`, `spec.md`, and later slices — what else assumed the false thing?
2. **Update only what's affected.** Specific sections and slices, never a wholesale regeneration.
3. **Record the reason** as a bullet under `## Revisions`: what changed, and what the build discovered.
4. **Continue from the revised plan.**

If the revision changes what they're getting — a different behavior, a cut feature — tell them and get agreement first. A purely internal correction that preserves the learner's choices—a moved file or corrected function—needs no conversation; make the call, record it, go. Changing their chosen stack or consequential architecture requires discussion and agreement, not an automatic swap. **Anything that touches `scope.md > The Unique Kernel` is the learner's decision, always.**

## Safe Recovery

The last commit is the recovery point — it exists because step 5 always runs.

**Never discard the learner's work. Never run a destructive git operation without clear need and explicit consent** — hard reset, force push, checkout over uncommitted changes, deleting branches, cleaning untracked files. Before any of those, say plainly what would be lost and ask. Prefer fixing forward; revert one specific change if you can't; throw work away last.

When a slice fails and a real repair attempt didn't work: stop building; tell them specifically what you tried and what went wrong; assess whether the uncommitted changes are usable; propose the smallest safe step back — usually leave the last commit alone and set aside only this slice's changes; then treat it as a plan revision, thinking about whether later slices need to change too.

## Proportional Verification

Mandatory, and proportional to a proof of concept. Don't introduce a test framework, CI, or coverage tooling the step never asked for. Don't fall below the contract either — a step whose verification you skipped is a step you don't know works.

Use subagents if your harness has them and they genuinely help — a second look at a stuck failure. An agent without them must be able to follow this skill start to finish.

## When the Checklist Is Complete

Checked slices mean implementation is ready for final review—not that the learner is done. On resume, read **Hands-on Checkpoints**, **Final Review**, and **Code Tour and App Map** and complete only unfinished work. For older checklists missing these sections, add them from the template and establish what actually happened; don't infer completion from checked slices. If review is already complete, go straight to the tour; if everything is complete, hand off without repeating it.

1. **Verify.** Start the project as the spec describes, run relevant checks, and summarize deviations under **Revisions**. Save the code walkthrough for the single tour after revisions.
2. **Kick the tires.** Have the learner start the dev server or equivalent and explore the running app freely: look at it, try the core journey, test awkward inputs, and note anything broken, confusing, or worth changing. Wait for their observations. This is the third hands-on checkpoint, not an agent-only test.
3. **Interview before revising.** Ask open-ended follow-ups one at a time: "What happened, and what did you expect instead?", "How would you want that to look or behave?", "Which change matters most, and why?" Don't jump from a vague complaint to your own redesign.
4. **Agree and revise.** Record requested fixes and small refinements as unchecked items under **Final Review**, implement the agreed changes, verify mechanically, commit, and have the learner retry affected behavior before checking each item. If a request substantially changes the project, pause to discuss which planning decisions need revisiting; update affected documents with agreement. No automatic restart of all planning skills.
5. **Finish explicitly.** Only mark the final-review completion box after feedback is resolved, checks pass, and the learner explicitly confirms the PoC is ready. If nothing needs changing, record that outcome rather than inventing revisions.

Then complete **The Five-Minute Code Tour** before handing off.

## The Five-Minute Code Tour

Both modes do this once, after the final revisions and before submission work. Budget about five minutes total, not another lesson or approval gate. Read `references/code-tour.md` relative to this skill for the tour and artifact requirements.

Explain why up front: "AI can write code faster than you can understand it. That gap—sometimes called cognitive debt—can make later changes and debugging harder. A little effort now can save effort later and make this feel like yours, not something the AI handed you. Let's spend five minutes following one action through your code."

Have them open the project in their IDE/editor and run the app if possible. Follow one meaningful action through **2–3 actual code locations**, connecting what they do and see to the responsible code. Invite **one optional small, safe edit** and let them see the result. Then reveal `devpost/app-map.html` as their take-home guide, not a document to study first. No quiz, score, extra sign-off, or exhaustive file tour. Track the route, edit outcome (including declined), and map in **Code Tour and App Map** so a fresh session won't repeat completed work.

## Hand Off

Say: "Congratulations—your proof of concept is built, tested, and reviewed, and your app map is ready. You've completed `5-build`. Next is `6-ship`: prepare your demo video and public GitHub repository, then write your submission." A fresh conversation is fine; `devpost/` carries everything.

## Conversation Style

- **Executor.** The plan is in the checklist. Don't add, reorder, or skip slices — the only exception is a recorded revision backed by evidence.
- **Build, don't narrate.** Say what you're building, say when it works, keep moving.
- **Their vocabulary** in every explanation and learner check, per the profile.
- **Never multiple-choice tools.** Free-form, always.
