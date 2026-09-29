---
name: investigate
description: (alamops) Grounded investigation of a feature or change before anyone plans or codes it. Fans out parallel read-only research agents over the codebase (entry points, sibling paths, test conventions, how the app runs), git history, and live library docs, then runs tiny scratchpad spikes to prove what reading can't settle. Saves what we know / proved / assume / must ask, plus a completeness inventory of every caller, propagation point and existing-data surface, to `docs/plans/<slug>-investigation.md`. Use when the user wants to investigate or research a change before building it, map its blast radius, find every call site a migration must touch, or answer a feasibility question — will this library, version or approach actually work here — before committing to it. Phase 1 of `implement`, runnable alone; accepts `--no-spikes`. Read-only on source. Not for debugging a live bug or slow page, explaining existing code, a standalone prototype whose number is the deliverable, or building the feature (implement).
---

# Investigate — ground truth before anyone plans

Your job is to find out what's actually true about the codebase, its history, and the technologies in play *before* a change gets planned — so that the questions asked of the owner are sharp, the plan is grounded in real file:line anchors, and nobody discovers in the middle of coding that a premise was false.

That last failure is the one this skill exists to prevent. Believing a claim ("the library supports that", "only two places call this", "the query will be fast enough") and finding out otherwise after a plan was approved and code was written on top of it is the most expensive way a build goes wrong. Investigation moves that discovery to the cheapest possible moment.

## Where this sits

This is Phase 1 of the `implement` delivery loop, packaged to run on its own. Its output is written for the next steps:

- **`grill`** reads the *must ask* list and turns it into questions for the owner.
- **`write-plan`** reads the findings, spike verdicts, completeness inventory, and runnability picture as its grounded context.

Nothing here requires those skills to exist — the brief stands on its own as a research document.

**Read-only on the repo.** Don't modify tracked files, don't add dependencies, don't run migrations or write to real data. Spikes write and run code, but only inside the scratchpad (see *Spikes*). The one file you create is the investigation brief under `docs/plans/`.

## 1. Pin down the change

Before spawning anything, state in one sentence what change is being contemplated and what decision the investigation should inform. "Investigate payments" gives agents nothing to aim at; "we're about to make price display currency-aware — find everything that would have to change and whether `Intl.NumberFormat` handles BRL on our Node version" does.

If the ask is too vague to aim at, ask one clarifying question rather than launching a broad sweep that returns an essay. Pick a short kebab-case slug for the feature (`currency-aware-prices`) — the brief is saved under it, and later steps look for it by that name.

If a brief for the same feature already exists under `docs/plans/`, read it first: extend it rather than redoing work that's already grounded.

## 2. Size the fan-out

Parallel agents multiply tokens, not just speed — every sub-agent carries its own context. Match the fleet to the surface area:

- **Localized change** (one module, a handful of files) → one research agent, or just do the reading inline.
- **A feature touching a few subsystems** → roughly 2–4 agents, split by subsystem so each returns fast.
- **Bigger fleets** only for genuinely independent, high-value areas.

If your harness has no sub-agent tool, run the same briefs yourself, one after another. The structure still holds; you lose only wall-clock.

## 3. The research wave — spawn in one turn

Spawn the research agents **in a single message** so they run concurrently. Use a read-only agent type (on Claude Code, `Explore` — it can still run `git` and web tools but has no edit tools, so it structurally cannot modify code). Leave the model unset so agents inherit the session's model, unless the user asked for a specific one.

- **Codebase agent(s)** — entry points, data models, sibling code paths that already solve a similar problem, reusable utilities, API/UI patterns, test conventions, and the blast-radius surfaces for this change. One of them also captures two things later steps depend on:
  - **The runnability picture** — how the app starts locally (dev command, services, env vars, seed data), the test command per layer, and whether an e2e harness exists (framework, command, fixtures). Planning needs this to decide whether e2e coverage applies; test runs need it to boot the app.
  - **The completeness inventory** — every caller of what's changing (including indirect ones: re-exports, barrels, dependency injection, dynamic dispatch, scripts and jobs outside the main source tree), every place a shape propagates (types, enums, validation, serializers, API contracts, client SDKs, fixtures, seed data, generated code), the existing data a migration would have to backfill, and the docs, config and examples that describe current behavior. The eventual plan is only as complete as this list, and enumerating it now is far cheaper than discovering it halfway through the build.
- **Git-history agent** — how similar features were built here before, recent changes to the files in scope, prior migrations, reverted attempts (a revert is a lesson someone already paid for), `CHANGELOG`/PR conventions. Uses `git log`, `git log -S`, `git blame`, `git show`.
- **Best-practices agent** — web research (when web tools are available) on current recommended patterns, library APIs, and version-specific gotchas for the technologies in play. Have it confirm live versions against what the repo pins rather than trusting memory — an API that changed between versions is exactly the kind of false premise this step exists to catch.

### Writing each brief

A sub-agent can't stop to ask you what you meant, so its one instruction has to carry everything. Every brief nails four things:

- **Objective** — the one question this agent answers, in a sentence.
- **Output** — a tight structured brief: findings with `file:line` anchors, and open questions. Not a file dump. Keep the format identical across siblings so you can merge them.
- **Tools & sources** — where to look (specific directories, `git log` on specific paths, the docs for library X at the pinned version), so the agent doesn't rediscover the map.
- **Boundaries** — read-only; which area is this agent's and which belongs to a sibling, so two agents don't cover the same ground.

## 4. Spikes — prove what reading can't

Source, history, and docs tell you what's *claimed*. Some assumptions only yield to an experiment: does this library actually do X on the version we pin, does that endpoint really return the documented shape, is this query fast enough at our row count, does the approach even run in our runtime.

When an assumption is **load-bearing** (the plan changes if it's wrong) and the research wave failed to settle it, run a spike: the smallest piece of throwaway code that answers exactly that one question.

- **Spike only what's load-bearing and unresolved.** Most unknowns are settled by reading, and a spike costs an agent, wall-clock and tokens — it has to buy a decision. Test: name the plan change that follows from each possible outcome. If you can't, you're satisfying curiosity; skip it.
- **Spikes usually form a second, smaller wave**, because you only know which assumptions survived once the research briefs are back. The exception is an unknown obvious from the request itself (a library nobody here has used, a feature whose feasibility *is* the question) — spike that in the first wave and save a round-trip. Spawn multiple spikes together.
- **One question, one spike, one verdict.** "Explore the library" comes back as an essay. "Can `pdf-lib@1.17` flatten AcroForm fields on Node 18?" comes back as yes/no plus the command that proves it.
- **Scratchpad only.** Give each spike its own directory (`<scratchpad>/spikes/<question-slug>/`, or a temp directory if your harness has no scratchpad) with its own throwaway environment — a local `package.json`, a venv. No edits to tracked files, no deps added to the repo's manifest, no writes against real data. Reading the repo is fine and usually necessary.
- **Use a writing agent type** (on Claude Code, `general-purpose`), since spikes must write and execute. That makes the scratchpad boundary a *briefed* constraint rather than a structural one, so make it the loudest line in the brief.
- **What comes back is evidence, not code**: the verdict (yes / no / inconclusive), the exact command and output or measurement that supports it, the versions and environment tested, and the artifact path so it can be re-run.
- **Inconclusive is a real verdict.** Don't let "I couldn't get it working" round up to "it doesn't work" — those lead to different plans. An inconclusive spike tells you the assumption is genuinely uncertain, which makes it a sharp question for the owner.
- **One spike is almost always worth running: would the tests even notice?** Apply the naive version of the change to a scratch copy of the repo — the obvious edit, with the obvious default — and run the existing suite. If it stays green while the output is visibly wrong (a BRL receipt with a `$` total, a report summing mixed currencies), that's one of the most important findings you can hand the planner: the current tests don't pin this behavior, so the plan has to add tests that do before anyone trusts a green run.
- **Know when it's bigger than a spike.** A spike is minutes to an hour. If answering needs a day, credentials or infrastructure you don't have, or is really a design exploration with several branches, don't absorb it — list it under *must ask* as a scoping decision (a proper time-boxed spike, a narrower scope, or planning around the uncertainty).

**Under `--no-spikes`** (or "don't run any spikes"), run no spikes at all. The unknown a spike would have settled doesn't disappear: treat it exactly like an inconclusive verdict — list it under *must ask*, marked **unverified because spikes were disabled**.

Example spike brief: *"**Objective:** answer one question — can `pdf-lib@1.17` flatten AcroForm fields on Node 18, or do we need a native binding? **Output:** verdict (yes / no / inconclusive), the exact command and its output that proves it, the versions you tested, and the path to what you built. **Tools/sources:** build a minimal repro in `<scratchpad>/spikes/pdf-flatten/` with its own `package.json` and install there; read `fixtures/sample-form.pdf` from the repo. **Boundaries:** write nothing outside that directory — do not add deps to the repo's `package.json` and do not modify any tracked file. I want the finding, not an implementation: stop as soon as the question is answered, and report 'inconclusive' rather than grinding if it isn't."*

## 5. Synthesize — this part is yours

Don't forward the agents' briefs; merge them. Cross-check where they disagree (the docs say one thing, the code does another — the code wins, and the disagreement is itself a finding). Sort everything into four buckets:

- **What we know** — facts with anchors.
- **What we proved** — spike verdicts, with what was measured and under which versions.
- **What we're assuming** — and what changes if each assumption is wrong.
- **What we must ask** — questions only the owner can answer: business rules, scope calls, trade-offs, and anything spikes left inconclusive or contradicted.

A question the repo could have answered doesn't belong on the *must ask* list — answer it. The owner's time goes to decisions, not to facts you could have looked up.

## 6. Write the brief

Save to `docs/plans/<slug>-investigation.md` (create the folder if missing; suffix `-YYYY-MM-DD` if that name is taken by an unrelated investigation, so nothing gets clobbered):

```markdown
# Investigation — <feature>
| Field | Value |
| --- | --- |
| Date | <YYYY-MM-DD> |
| Change | <one sentence: what's being contemplated and the decision this informs> |
| Agents | <e.g. 2 codebase, 1 git-history, 1 web, 1 spike> |
| Flags | <--no-spikes, or "none"> |

## 1. What we know
<facts, each with a file:line anchor or a source link>

## 2. What we proved
| Question | Verdict | Evidence (command → output / measurement) | Versions | Artifact |

## 3. What we're assuming
<assumption → what changes in the plan if it's wrong>

## 4. What we must ask the owner
<numbered; each says why it matters and, where a spike or finding bears on it, what the evidence shows>

## 5. Completeness inventory
- Callers (direct and indirect): <file:line list>
- Propagation surface: <types, enums, validation, serializers, contracts, SDKs, fixtures, seed data, generated code>
- Existing data a migration would have to backfill: <tables/rows/files, with volumes if known>
- Docs / config / examples that describe current behavior: <paths>
- What the change would orphan: <code, exports, flags>

## 6. Runnability
- Start locally: <command, services, env vars, seed data>
- Tests: <command per layer>
- E2E harness: <framework, command, fixtures — or "none found">

## 7. Risks & blast radius
<sibling paths, retries, downstream systems, rollback concerns>
```

## 7. Hand off

Tell the user where the brief is, the three or four findings that most change the picture (especially any spike that contradicted what the team believed), and the *must ask* list. Suggest the natural next step: `grill` to settle the open questions with the owner, then `write-plan` — or `implement` if they want the whole loop driven from here.
