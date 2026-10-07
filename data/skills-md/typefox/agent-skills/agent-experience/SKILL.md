---
name: agent-experience
description: >-
  Make a code repository agent-ready with state-of-the-art AX (Agent Experience): audit and set up
  AGENTS.md / CLAUDE.md and agent docs, wire verification sensors with self-correction messages, and
  build docs-as-memory (architecture docs, ADRs, exec plans). Use when the user wants to make a repo
  agent-ready or AI-friendly, onboard coding agents, create/review/improve AGENTS.md, CLAUDE.md, or
  other agent instruction files, set up a project for agent-first development, asks why an agent
  keeps repeating a mistake, asks any AX question (general or project-specific), or mentions
  "harness engineering", "agent readiness", "context engineering" (its repo-side slice), or "AX".
  Not for building agent runtimes or orchestration code, nor for authoring a single agent skill —
  use skill-creator for that.
---

# Agent Experience (AX)

AX is the experience AI agents have when working in a repository — how easily they can access, understand, verify, and safely change it. Two reframings drive everything in this skill. First, **onboarding happens at the start of every task**: a human onboards once, an agent re-onboards every session, so everything a new hire needs in week one, the agent needs in minute one, on every run. Second, **hallucination is what inference looks like when context is missing**: when an agent invents a build command or misuses an internal API, that is not a model defect to tolerate — it is an AX defect to fix.

**The honest test** — the single success criterion behind every artifact this skill produces: *an agent given a real ticket, with no human help, reliably reaches a green verification suite and produces a diff a reviewer accepts.* Optimize for that. Readiness checklists and scores are diagnostics for spotting neglect, never targets to maximize.

Vocabulary: write "AX" and "agent-ready" in everything you produce. When reading sources or searching the web, also recognize the synonyms: *context engineering* (the superset term — this skill is its repo-side slice), *harness engineering* (in its repo-side sense), *agent readiness*, *agent legibility*, *ambient affordances*. Generated artifacts never say "harness" — that word collides with the agent-runtime meaning.

## The control system in brief

Treat the repo-side AX setup as a control system that regulates the codebase toward its desired state. Two control directions × two execution modes give a 2×2 that classifies everything you find or create:

| | **Guides** (feedforward — steer before the agent acts) | **Sensors** (feedback — verify after it acts) |
|---|---|---|
| **Computational** (deterministic, fast, cheap — run on every change) | one-command bootstrap, task-runner command surface, scaffolding, codemods, generated reference docs, deterministic dev env | type checks, linters, tests + coverage, structural/dependency rules, mutation testing, secret scanners, the build |
| **Inferential** (LLM-run, semantic, costly — run at gates or on a schedule) | AGENTS.md, skills, docs/, ADRs (architecture decision records — short, versioned docs capturing one decision, its context, and its consequences), specs, code-level discoverability | review skills, modularity reviews, security/data reviews, doc-gardening, janitor/GC agents |

Both directions are mandatory. Feedback-only, the agent repeats the same mistakes every session — nothing steers it up front. Feedforward-only, rules accumulate but nothing ever verifies they held. Guides raise first-attempt quality; sensors give the agent a self-correction loop that fixes issues before they reach human eyes. Sensors also set the ceiling — **the sensor ceiling**: the system regulates only what some sensor observes, so a defect class nothing senses (a page that renders wrong under green tests, errors swallowed by a catch block) ships and recurs without ever triggering the loop below. Before letting more agent work land with less human review, widen sensor coverage first — every blind spot a reviewer used to cover becomes a shipped defect class.

**The steering loop** is the practice that builds and maintains the system: whenever an agent makes a mistake, engineer the repository so that mistake cannot recur — never settle for "prompt harder". Escalate any recurring failure up this ladder until it stops recurring:

1. a line in AGENTS.md →
2. a dedicated doc or skill →
3. a lint rule or structural test →
4. an architectural constraint.

Operate the loop as a coupling with a restraint. The coupling: the rule or sensor that prevents a mistake ships **in the same change as the fix** for that mistake, with the triggering incident cited inline (issue number, error, failing run) — fix and lesson never travel separately. The restraint: rules are added one per *observed* mistake, never speculatively — a mistake that hasn't happened yet can't pass the litmus test. The citation is also what keeps rules prunable: a rule that names its incident can later be re-judged against whether that failure class still occurs; a rule that names nothing is the first pruning candidate.

Keep quality left: fast computational sensors run alongside the coding session; expensive and inferential ones run post-integration or on a schedule.

**Affordances** are the structural properties that make a repo governable — what the codebase makes cheap to sense and to constrain: a strongly typed language (type checking is a free sensor), a constraining framework (its conventions abstract away whole error classes), fast build/test tooling (feedback-loop speed), clearly definable module boundaries (expressible as import rules). Start with what the codebase affords; acquiring a missing affordance (adding types, cleaning boundaries) is an investment that precedes the sensor work it enables. **Variety reduction** is the affordance you choose: committing to a topology narrows what an agent can produce, which is what makes a comprehensive control set achievable.

## Non-negotiables — the AX standards

Hold every artifact you audit or generate to these. In improve mode they are the audit checklist; in every mode they are the generation rules. Cite them by tagline when explaining findings (e.g. "this violates *map, not manual*"), as this document does itself.

1. **Repo-local or nonexistent.** Anything the agent can't reach from inside the repo effectively doesn't exist — wikis, chat threads, and people's heads are invisible. Push knowledge into versioned repo artifacts. An external system counts as reachable only where a fetch path exists (e.g. `gh` for GitHub issues); otherwise mirror a one-line summary with the link as provenance.
2. **Single source of truth.** Each fact lives in exactly one place; everything else points at it. Never vendor copies of external docs — audited vendored files have drifted 183 lines from upstream, still instructing agents to run tools removed months earlier.
3. **Map, not manual.** The root instruction file is a ≲150-line map that teaches the agent where to look next, with progressive disclosure into docs/. A giant file crowds out the task, makes everything "important" (so nothing is), rots into stale rules, and can't be mechanically verified.
4. **Every line passes the litmus test:** *would removing it cause a mistake the agent wouldn't otherwise make?* Instructions are not free: unnecessary rules cost reasoning tokens on every task, listed commands get used vastly more than unlisted ones, and unedited LLM-generated overview files *reduce* task success while raising cost (the numbers — single-study, but the best we have — are in `references/agents-md.md`). Deviations from ecosystem defaults earn lines; defaults never do.
5. **Never trust prose — verify by execution.** Every command cited in agent docs is verified by actually running it, with the exact invocation and timing recorded. A doc–reality discrepancy is a first-class finding, not noise.
6. **Run it, don't read it.** Agents demonstrably *read* check scripts and predict their results instead of executing them. Require evidence-backed verification: execute the check, capture the output to a file rather than through a pipe, and read the exit code unpiped — `cmd | tail` reports the pipe's exit status, not the command's, so a failing check piped through a pager or filter records a misleading 0.
7. **Verify the relevant output.** A change is proven at the application's observable output — the rendered page, the emitted data or file, the API response — never only at the code that produces it: code-level sensors routinely stay green over wrong output (a layout that renders broken under passing unit tests; a stream with the right schema and wrong numbers). Where the agent can't natively perceive that output — pixels, large result sets, binary formats — supplying the perception tooling that makes it legible (browser automation to see a UI, a query script over emitted data) is part of the AX setup, not an optional extra.
8. **Enforce invariants mechanically where it pays; prose where judgment is required.** State the boundary ("parse data shapes at the boundary"), enforce it with a lint or structural test, and leave the how open. A check is code the repo maintains from then on: a rule configured in a tool the repo already runs is nearly free, a bespoke script is a component with its own bugs and drift. Weigh that upkeep against the mistake it fences — a prose line is the right rung wherever the check would cost more than the mistakes it prevents.
9. **Error channels are guidance channels.** Every custom check emits messages written for agent self-correction: what's wrong, why the rule exists, what to do instead, how to record a justified exception where judgment is legitimate — and, when the rule lives in a doc, where it lives (message patterns in `references/techniques.md`).
10. **Docs are verified like code.** Freshness is mechanically checked (`scripts/check_docs.py` — its module docstring lists every check), and every artifact has an explicit lifecycle: active/completed for plans, accepted/superseded for decision records.
11. **Write-as-you-go.** Agent statelessness erases anything not captured: every interview answer and decision lands in its durable artifact immediately — never in a summary to be filed later.
12. **Every fact traces to a source.** Any statement in a generated doc traces to the repo, to output captured this session, or to the user's own words — anything else is marked `(to be confirmed)` or omitted. Product color counts: an invented name, count, or backstory is as much a fabrication as an invented database choice, and the user is never quoted or paraphrased saying something they did not say.
13. **Convention over configuration.** This skill carries opinionated defaults for the AX layer itself — which artifacts to create, doc layout, sensor wiring, message patterns — and applies them whenever the user hasn't stated otherwise. Interviews and template placeholders gather *project facts* (intent, scope, technical architecture); they never poll the user on how to design the AX layer ("would you like ADRs?" is a forbidden question). An unprompted user preference or a hard project constraint overrides a default and gets recorded as an ADR. When in doubt, convention wins.

## Pick your mode

Find the user's situation and jump in — state your chosen mode and scope before starting (that statement is Phase 0; consult alone skips it):

| Mode | Entry signals | Phases |
|---|---|---|
| **Retrofit** | Existing codebase; no or thin agent setup ("make this repo agent-ready", "onboard Claude/Codex here") | All phases 0–6, the full playbook |
| **Improve** | Agent instruction files already exist ("review our AGENTS.md", "make our agent docs follow AX standards", "why does the agent keep getting X wrong?") | All phases 0–6, scoped to the existing docs: audit against the standards, shrink, verify, restructure. Touch sensors only where docs state rules nothing enforces or where a sensor exists but is ineffective (ignored, drowning in noise, green while checking nothing) — repairing a broken sensor is always in scope; adding coverage beyond that is not |
| **Greenfield** | No code yet ("set up a new project for agent-first development") | 0, then 4–6 — phases 1–3 are skipped (no code to audit); interview-first (see Greenfield specifics) |
| **Consult** | A question about AX, general or project-specific ("what belongs in AGENTS.md?", "is our CLAUDE.md too long?"), or one small, specific change ("add the release commands to AGENTS.md") | None — no phase spine; answer or apply directly (see Consulting specifics) |

## The workflow

One shared phase spine; the mode selects which phases run and at what depth.

### Phase 0 — Scope and mode

State the mode you picked, why, what you will deliver, and the agent tools in play — every tool the request names or the repo shows traces of — before doing anything else: Phase 5 projects AGENTS.md to each of them, and a tool mentioned only in the opening request is easily lost by then. If the request is narrower than the mode's full output ("just write an AGENTS.md"), keep the audit phases — generation without audit produces exactly the bloated files this skill exists to prevent — but scale the deliverable to what was asked.

**Done when** the user knows the mode, the planned deliverables, and the agent tools in play.

### Phase 1 — Inventory and classify *(retrofit, improve)*

Inventory what exists — native Glob/Grep work over the playbook's checklist — and place every finding in the control-model grid. Empty cells are the gap list; the two cross-checks (*claims vs. enforcement* and its reverse) find the real work.

Load `references/audit-playbook.md` (Phases 1a–1b: inventory checklist, classification procedure, cross-checks).

**Done when** you have the classified inventory (matrix or equivalent — empty cells explicit), the gap list, and both cross-check lists.

### Phase 2 — Verify by execution *(any mode with existing code)*

Never trust documented commands — run them, in fresh-checkout order, and record each working invocation with its timing, labeled warm or fresh. Run `scripts/check_docs.py` over the existing agent docs. Discrepancies between docs and reality are first-class findings; probe the affordances and note sandbox friction while you are there.

Load `references/audit-playbook.md` (Phase 2: verification protocol).

**Done when** a verified command block exists (exact invocations and timings), backed by captured output, with discrepancies and friction listed.

### Phase 3 — Assess and draft with placeholders

Distill the non-inferable deltas — the playbook's six extraction passes, from deviation detection to docs triage — and draft the target artifacts: AGENTS.md from `assets/AGENTS.template.md`, plus the minimal docs/ subset this project actually warrants, with explicit `(to be confirmed)` markers wherever the repo couldn't answer. Never silently assume: a marker is a question for Phase 4; an unmarked guess is a fabrication (*every fact traces to a source*).

Load `references/audit-playbook.md` (Phase 3: distillation heuristics), `references/agents-md.md` (content model, exclusion list, drafting procedure) and `references/docs-structure.md` (which docs artifacts this project warrants).

**Done when** drafts exist and every unknown is a marker, not a guess.

### Phase 4 — Interview the placeholders

Interview the user to resolve exactly the markers, following the grill protocol: codebase-first (never ask what Phases 1–3 answered), the markers worked as a design tree in frontier rounds with a recommended answer for every question, each answer written into its durable artifact immediately (*write-as-you-go*), and questions about project facts only (*convention over configuration*). In retrofit, the first round also carries the **history-scan offer** — mining the git history, and the issue and change tracker where a fetch path exists, for the decisions the docs should make explicit; it runs only on the user's confirmation (`references/interview.md`, history-scan offer). An unattended session compresses the interview into one final round, or ships the open questions as a questionnaire artifact.

Load `references/interview.md` (protocol, session mechanics, unattended sessions, theme→destination map, spec and design-doc triage).

**Done when** no markers remain — each is resolved or recorded as an explicit open question.

### Phase 5 — Generate and wire

Produce the final artifacts:

- **AGENTS.md** per the content model, with its **projections**: the CLAUDE.md import, nested per-package files for monorepos, and a one-line import or pointer at the native location of every other agent tool in play (named in Phase 0) — never a copied body (`references/agents-md.md`, projections section). Every command in it comes from Phase 2's verified block.
- **Docs nucleus**: the minimal subset from Phase 3's triage, each artifact from its template in `assets/` (named in its `references/docs-structure.md` section). Product-specs and design-docs only where their evidence triggers fired in the triage — never as a per-module dump.
- **Sensors** per the escalation ladder for the rules Phase 3's triage promoted, each with self-correction messages (*error channels are guidance channels*). Doc freshness stays covered by running the skill's own `scripts/check_docs.py` in-session — never copy the script into the repo or wire a copy into CI: a copy stops evolving with the skill and becomes debt, so recurring doc-freshness lands on the Phase 6 roadmap as a re-audit routine, not as an install. Every sensor and command added this session gets cited in AGENTS.md — in the commands section or the definition of done — because an unlisted sensor is one no future session will run.

Load `references/techniques.md` (sensor/guide catalog, self-correction message patterns) and `references/agents-md.md` (projections, drafting rules).

**Done when** artifacts are written and sensors are wired into the dev loop or CI.

### Phase 6 — Prove it and hand off

Run every new or changed sensor and `scripts/check_docs.py` against the final state; fix what fails — evidence-backed, output captured (*run it, don't read it*). Judge each sensor by its output, not its exit code: prove it can fire, at every scope the docs claim for it, and leave neither the deliberate breakage nor verification litter in the delivered copy — the proof protocol is in the playbook. Then run the **claim check** over every doc this session wrote or changed — and every comment or message written into code or config along the way: re-read each as a skeptical reviewer and trace every factual claim to this session's evidence — captured output, a file actually read, or the user's words; anything untraceable is fixed, marked `(to be confirmed)`, or cut (*every fact traces to a source*). Then deliver:

1. The **remediation roadmap** for everything deferred, in foundational→sophisticated order (the remediation ordering in `references/audit-playbook.md`), each step small and individually shippable.
2. The **steering loop as standing practice**: tell the team that from now on, every recurring agent mistake gets engineered away up the escalation ladder — the setup you built is the seed, not the finished system.

Load `references/audit-playbook.md` (Phase 6: proof protocol, claim check, remediation ordering).

**Done when** everything green is proven with captured output, a search of the whole delivered tree for caches and build artifacts your runs created comes back empty, the claim check comes back clean, and the roadmap is delivered.

## Greenfield specifics

With no code to audit, Phases 1–3 are skipped — after Phase 0 you go straight to the interview (Phase 4), which leads: use the greenfield question bank in `references/interview.md`, loaded first. The interview gathers product and technical facts; the AX layer follows from them by convention (*convention over configuration*).

Guide stack and topology decisions by affordances and push for a topology commitment (variety reduction — both defined under the control system above). Rigid layered architecture — usually postponed until hundreds of engineers — becomes an *early* prerequisite with agents, because constraints are what allow speed without decay.

Day-one build order: root map (AGENTS.md + CLAUDE.md projection) → one-command bootstrap and task-runner command surface → in-session sensors (typecheck, lint with agent-failure-mode rules, fast tests, secrets pre-commit) → docs nucleus (`docs/ARCHITECTURE.md`, `docs/adr/` seeded with the stack/topology decisions from the interview, `docs/exec-plans/`, and `docs/product-specs/product-brief.md` holding the interview's intent answers — the one spec greenfield warrants; per-capability specs come later, spec-first per feature).

Boundary: this skill sets up the AX layer around the user's chosen project scaffolding — it does not generate the application itself. The pull to cross this line is strongest at the end, when a working feature feels like the honest proof that the loop works. It is not: the sensors firing on deliberate failures prove the loop, and a feature silently answers product questions the interview left open. The ceiling is scaffold-level — a smoke-tested placeholder route and an empty, clearly labeled schema stub; no domain logic, no seeded domain data, no working screens.

## Consulting specifics

Consult is for the light requests: the user wants to understand something about AX, or wants one specific change, and the phase spine would be ceremony. Skip the phases and the Phase 0 announcement — a question deserves an answer, not a preamble.

- **Ground answers in this skill's model.** Explain through the control system and the standards, citing taglines as everywhere else. Load only the reference file that covers the topic (e.g. `references/agents-md.md` for a question about AGENTS.md content) — not the whole set. When the answer is a *document*, route it before you write it: ARCHITECTURE.md is the **structure**, product-specs are the **promises**, design docs are the **strategy**, ADRs are the **reasons**, exec plans are the **work** — so bug-vs-intended, a disputed behaviour, or a promise that keeps being broken is a product-spec, and a deliberate mechanism agents keep breaking is a design doc, neither an ADR; `references/docs-structure.md` owns the routing. For questions about *this* project, check the actual repo state with targeted searches before answering; never speculate about files you could read.
- **Targeted changes obey the standards at the scale of the edit.** Every added line passes the litmus test; any command you write down is verified by execution first; each fact lands in its single source of truth, and the CLAUDE.md projection stays a pure `@AGENTS.md` import. What consult never does: inventory, interview, roadmap, readiness score.
- **Escalate by offer, not by action.** If the question or edit exposes a deeper problem — the file violates *map, not manual*, documented commands don't run, rules have no sensors — name it in a sentence or two and offer improve mode. Don't launch the full workflow uninvited.
- **Know when you've left consult.** "Write our AGENTS.md" or "restructure our agent docs" is artifact-scale work: that's improve or retrofit, audit included. Say you're switching modes, then switch.

## Reference files

Each phase above names the files it loads — don't read them all upfront. The index by content:

- `references/audit-playbook.md` — inventory checklist with globs, classification procedure, verification protocol, distillation heuristics, Phase 6 proof protocol and claim check, readiness checks, remediation ordering.
- `references/techniques.md` — the full guide/sensor catalog with selection criteria, self-correction message patterns, and operating the control system over time.
- `references/agents-md.md` — AGENTS.md content model in leverage order, evidence and limits, drafting procedure, CLAUDE.md and multi-tool projections; the primary reference for improve mode.
- `references/docs-structure.md` — the docs/ system of record: layout, fact routing, per-artifact when-and-how, plans, decision records, product specs and design docs (evidence-triggered), the library/framework case, hygiene invariants.
- `references/interview.md` — grill protocol, session mechanics, unattended sessions, theme→destination map, spec and design-doc triage, greenfield question bank.

## Before you're done

Check the mode's definition of done: **retrofit** — verified commands, AGENTS.md + CLAUDE.md projection, docs nucleus, wired sensors, roadmap, all proven by execution; **improve** — the docs are shorter, every line passes the litmus test, every command verified, claims-vs-enforcement resolved or on the roadmap; **greenfield** — interview answers captured in durable artifacts, day-one AX layer in place around the user's scaffolding, nothing past the scaffold ceiling; **consult** — the question answered (or the change applied and verified) grounded in the standards, with any deeper gap you spotted offered, not silently pursued or dropped.

In every mode, the standards' closing checks: *single source of truth* (a CLAUDE.md projection beside every AGENTS.md written, no vendored copies), *write-as-you-go* (no silent assumptions — open questions are recorded as open questions), *every fact traces to a source* (the claim check passed on every doc and every code or config comment you wrote or changed), and readiness scores labeled as diagnostics.
