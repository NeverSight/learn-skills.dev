---
name: project-rules-architect
description: "Generate or overhaul a coherent, non-redundant set of AI coding-agent instruction files for a project — a canonical entry file (AGENTS.md) plus a rules directory, wired into the target tool (OpenCode's opencode.json, Cursor's .cursor/rules/*.mdc, CLAUDE.md, or AGENTS.md alone). Built on a library of specialised rule templates selected by detected stack, not by copying a whole profile. Use this whenever the user wants to bootstrap rules for a new project, add rules to an existing one, regenerate rules for a new stack, or complains that AI-generated rule files are spaghetti — overlapping, redundant, contradictory, too vague, ignored by the agent, or inconsistent in depth from one file to the next. Also use when the user asks how to structure AGENTS.md, asks to preserve or migrate a codebase's existing conventions, or wants a repeatable process instead of re-prompting from scratch on every project. — Génère ou refond un ensemble cohérent et non redondant de fichiers d'instructions pour agents IA : un fichier d'entrée canonique (AGENTS.md) plus un répertoire de règles, branchés sur l'outil cible. Construit sur une bibliothèque de gabarits spécialisés choisis selon la stack détectée, plutôt que de copier un profil complet. Utiliser pour initialiser les règles d'un nouveau projet, en ajouter à un projet existant, régénérer les règles pour une nouvelle stack, ou quand les fichiers de règles générés sont spaghetti — redondants, contradictoires, vagues, ignorés par l'agent, ou incohérents en profondeur d'un fichier à l'autre. Utiliser aussi pour structurer AGENTS.md, ou pour donner un processus reproductible au lieu de réexpliquer les conventions à chaque session."
---

# Project Rules Architect

Produces a rule set the agent will actually follow — not a style guide it skims
and ignores. The failure this skill exists to prevent: someone asks for "all the
rules, act like a senior dev," gets fifteen files of inconsistent depth, half of
them contradicting each other, wired into nothing so none of it loads, and six
months later nobody trusts the rules enough to maintain them.

**The shape of the solution:** a library of specialised rule templates —
universal, per-domain, and per-technology — selected by probing the project, not
copied wholesale. One fact lives in exactly one template. Everything the agent
needs before it can act is in the entry file; everything else is a file it loads
when relevant.

Read `references/research-summary.md` once per session before drafting — the
evidence behind every principle below. Read `references/postmortems.md` whenever
this run consolidates existing rules, adopts a project's conventions, or ports a
pattern from another project. Both are real, previously-caught failures, not
hypothetical ones. Don't re-derive them.

## Working alongside a planning skill

If the project also runs a planning skill (Forge, or any equivalent that owns a
`.forge/` directory), this skill is called **twice**, and by the planning skill
both times. It is a callee. It never routes.

| Call | When | What it emits |
|---|---|---|
| **Context scaffold** | at project start, before the stack is known | the four context files, and nothing else |
| **Rule set** | after the planning skill has fixed the stack and what the project is about | `AGENTS.md` + the rules, wired to the target |

**The scaffold's four files are the project's cross-session memory, and neither
skill writes to them afterwards.** The agent maintains them: it appends a session
entry, records a decision, logs a correction. Neither Forge nor this skill edits
them after the scaffold call, and neither keeps a second copy of their contents.

The reason is not tidiness. A memory file is the one artefact whose value is
**cumulative across sessions**, so it is the one artefact two writers destroy
most easily: one appends, the other overwrites, and the loss is invisible because
the file still exists and still looks plausible.

| This skill owns | The planning skill owns |
|---|---|
| the shape of `AGENTS.md`, `SESSION_LOG.md`, `DECISIONS.md`, `LEARNINGS.md`, once | the product, the stack, the architecture, the plan |
| `AGENTS.md`, `{{rules dir}}/*.md` — what to follow | `.forge/*.md` — what to build, and where the project is |
| the wiring file (`opencode.json`, `.cursor/`, …) | `state.json` — status, paths, IDs, hashes |
| — | `.forge/audit/` — incidents of the planning process |

**The rule: a fact lives in exactly one file, and a decision has an owner.** The
planning skill's state file holds a pointer, not a copy. A state file containing
prose is not a state file — it is an undisciplined document, and it is neither
sortable nor indexable, and it is wrong without any signal.

**Two consequences for this skill's own work:**

- **A correction names its destination.** Anything logged in `LEARNINGS.md` says
  which rule file it will be promoted into. A correction with no target cannot be
  promoted. See `postmortems.md` Case 5.
- **The two calls are independent, and neither implies the other.** A project can
  have a scaffold and no rules — that is the normal state between the two calls,
  and it is not a half-finished rule set. Conversely a project can have rules and
  no scaffold, which is the ordinary case for anyone using this skill standalone.
  Neither gap is a defect to be reported.

---

## The six principles

Everything this skill produces obeys these. If a draft violates one, fix the
draft, not the principle.

1. **Operational policy, not documentation — with three tiers, not two.** Sort
   every sentence into exactly one bucket before deciding to cut it:

   | Tier | Test | Example | Action |
   |---|---|---|---|
   | Tutorial prose | Explains something the model knows from training | A 20-line example showing what a Server Component is | Cut |
   | **Operational prose** | Answers "what should the agent DO when X?" or "is X acceptable?" — even with no backtick command | "Split by responsibility, not by lines — a 250-line single-responsibility file is fine" | **Keep.** Rewrite tighter if possible; do not delete. |
   | Verifiable command | A literal invocation with a pass/fail outcome | `npm run lint` exits 0 | Keep |

   The test for the middle tier: *can you imagine the agent violating this?* If
   yes, it's a decision rule, not documentation, regardless of whether it has a
   command. "We value clean code" fails — nothing to violate. "Split by
   responsibility, not by lines" passes — an agent could easily split a 250-line
   file wrongly just to hit a count.

2. **One fact, one location.** Never state the same rule in two files. If it's
   cross-cutting, it lives in exactly one template and everything else
   references it by name. This is the single largest source of spaghetti — not
   bad individual rules, but the same rule drifting into two phrasings over time
   until they disagree. **The audit is a grep, not a judgement call**, and the
   cross-reference must name a section, not a file. "See `security.md`" is weak;
   "see `security.md` §Token Handling" survives a refactor of the file.

3. **Ranked, not stacked, priorities.** "Ship fast" + "full coverage" + "5-minute
   CI budget" with no ranking means the agent picks silently and you find out
   later. Every set of rules that could conflict gets an explicit order, in the
   entry file, referenced by everyone else.

4. **Start from a skeleton, grow from corrections — for FRESH rule sets only,
   and there are four situations, not two.**
   - **Context scaffold** (asked for by name, before the stack is known): emit
     the memory and context structure and **stop**. No rules, no rule set, no
     stack probe. See § The context scaffold below — this is the mode a planning
     skill calls first, and getting it wrong in either direction is expensive.
   - **Bootstrap** (no existing rules): ship a lean, correct skeleton plus a
     living-learnings section. Don't enumerate every hypothetical rule on day
     one — that's the randomness problem, guessing at situations that haven't
     happened.
   - **Consolidation** (existing rules being reorganised): every existing rule
     already represents a lesson learned. **Reorganise and dedupe; do not
     curate down.** Applying "start lean" pressure here produces exactly the
     silent content loss in `postmortems.md` Case 1. The only content you're
     licensed to remove without asking is tutorial prose and true duplicates.
   - **Adoption** (existing *code*, with or without existing rules): run
     `references/existing-project-protocol.md` in full. Detect the conventions
     the code actually has, then preserve or migrate. **This is the case the
     skill previously had no handling for, and it's the one that produces rules
     contradicting a working codebase.**

5. **Porting a pattern is not porting content.** The *pattern* is portable —
   what triggers a check, what gets verified, what file it's logged to. The
   concrete content is not: file names, library names, framework conventions
   belong to the source project and must be re-derived from this project's
   actual stack. **A rule file that references a file, library, or tool not
   present in this project is contamination** (`postmortems.md` Case 2 — and
   note that a grep for library names doesn't catch process vocabulary; a
   separate pass is needed for that). **Corollary, learned the hard way: a
   generated rule file may never name its own source template or profile.** A
   surviving "per the profiles" or a framework symbol from the wrong stack is
   both contamination and a dangling reference.

6. **Budgets are ceilings for prose and floors for gates.** These are two
   different rules, and conflating them is how a set ends up complete in its
   argument and empty in its enforcement.

   | Content | Budget | The test |
   |---|---|---|
   | **Prose** — rationale, framing, examples, history | a **ceiling**. Cut this first | Would the agent act differently without this sentence? |
   | **A gate** — a threshold, a command, an exit code, a banned list | a **floor**. Never cut it | Does it exit non-zero when violated? |

   **A gate that does not exit non-zero is not a gate.** It is a sentence, and
   it is subject to the same fate as every other sentence: an agent that is
   tired, or in a hurry, or told to "just get this done", will read past it. A
   threshold, a command and a banned list are the *cheapest* content in any
   rule file — a line each — and the only thing that survives that pressure.

   So: if the set is over budget, cut tutorial prose first, and if there isn't
   any, **add more scoped files rather than trimming operational content.** If
   it is under budget, that is not licence to cut further — it is a signal to
   ask **what is missing**, because the usual reason a generated set is thin is
   that a pressure valve fired (see § Step 0b).

6b. **The budget is per-target, and it must be measured — the read-back test
   cannot detect it.**

   The ~500-line figure in `research-summary.md` is *Cursor's own guidance*, and
   it **assumes activation modes**: a scoped file only loads when its files are
   open. **It does not transfer to a target with no scoping.**

   | Target | Scoping | Budget | |
   |---|---|---|---|
   | Cursor `.mdc` | 4 activation modes | ~500 lines **always-apply** | `mdc-frontmatter-spec.md` |
   | OpenCode `instructions` glob | **none — every file, every session** | **the whole rules directory**, hard total | Step 3b |
   | `AGENTS.md` alone | none | one file; if it outgrows one, change target | — |

   **On a target with no scoping, splitting a file saves nothing.** The glob
   loads it either way. The only levers are the total, and not putting
   trigger-based content in a file that loads unconditionally.

   **And the read-back test in Step 6 will not catch an oversized set.** It
   answers from the entry file, which is small and front-loaded — a 2×
   over-budget set passes it. Measure the total separately, in Step 3b, or not
   at all.

## The context scaffold

A planning skill calls this mode **before the stack is decided**. It is a
short-circuit: emit the four context files, emit no rules, stop.

| Emits | Never emits |
|---|---|
| `AGENTS.md` — the context the agent needs before it can act, **and the trigger for each of the three files below** | any rule file |
| `SESSION_LOG.md` — what happened, appended per session | `.opencode/rules/` |
| `DECISIONS.md` — decisions taken, and **open questions** as questions | a stack choice |
| `LEARNINGS.md` — corrections, each naming where it will be promoted | a probe result |

### The formats are normative — reproduce them, do not redesign them

The four files have **fixed shapes**, because a memory whose shape changes per
project is a memory nobody can read on the second session. They are written out in
full in `templates/memory/`; that directory is not an illustration, it is the
specification.

The formats were once **kept** and then **lost**: `provenance/synthesis-provenance.md`
records that the 8-field `SESSION_LOG.md` and the 6-field ADR form were "kept as-is"
and were "emitted alongside the entry file". No `templates/` directory was ever
emitted. The consequence was measured, not predicted — on a project whose Phase 0 ran
the full way to Phase 5, the scaffold produced a four-bullet journal, a
questions-only `DECISIONS.md` with **zero closed decisions**, and a `LEARNINGS.md`
with **zero entries**. The format was known, written down, and not normative, so
every project got its own.

| File | Shape | The field that is most often lost |
|---|---|---|
| `SESSION_LOG.md` | **8 named fields, in order**: `STARTED FROM` · `DECIDED` · `REJECTED` · `BLOCKED` · `FILES TOUCHED` · `STATUS` · `NEXT SESSION SHOULD` · `NEXT SESSION SHOULD NOT` | **`REJECTED`** — see below |
| `DECISIONS.md` | `## ADR-<NNN>: <title>` with **6 fields**: `Date` · `Statut` · `Contexte` · `Décision` · `Alternatives considérées` · `Conséquences` | **`Alternatives considérées`** |
| `LEARNINGS.md` | **one line per correction**, the fault written as a contrast, then `→ domaine: … \| Seen: …` | the contrast form |
| `AGENTS.md` | the context, then the index with description **and** trigger | the trigger |

**`REJECTED` is the field that pays for itself.** Everything else records what was
done; `REJECTED` records what was **declined and why**, and it is the only one that
stops a later session from re-proposing it. A journal without it re-litigates its
own past: on the project measured above, the refusals were the contracted
exclusions (accounting, card payments), the six slices deliberately left unplanned,
the sixteen things `client-liaison` rejected, and two invented agent paths. All four
categories were load-bearing, and none had anywhere to go.

**A closed decision is closed.** `DECISIONS.md` is an **append-only register of
closed decisions**. "Append-only" and "closed" together mean: a decision that turns
out to be wrong is **superseded by a new ADR that names the old one**, never
silently rewritten. `Statut: Actif` or `Statut: Supersédé par ADR-<NNN>` — and a
`Statut:` line is required on every entry, because an entry without one cannot be
superseded and therefore cannot be corrected.

Questions the project cannot answer yet belong in `DECISIONS.md` too, as questions,
and each one carries the trigger that will close it. But **the register's job is the
closed decisions**: a `DECISIONS.md` with open questions and no closed decision has
recorded nothing that a future session is bound by.

### The two halves of the index, and the one that is usually missing

`AGENTS.md` carries a table with a row per file. Each row needs **two** things,
and they are not the same thing:

| Half | The question it answers | Missing it means |
|---|---|---|
| **Description** | *what goes in this file?* | the file is a mystery |
| **Trigger** | *what makes me write to it, and when?* | the file stays empty forever |

A row with a description and no trigger is the most natural mistake to make,
because the table looks complete. It is not: it is an index of four containers
and no instruction to fill them, and the result is a memory that is created,
structurally sound, correctly named, and **permanently empty** — which is worse
than no memory, because it looks like progress.

The trigger is a **condition, not a category**. "Corrections" is a description.
"*When* you get something wrong twice" is a trigger. Every one of the three
needs one, and it has to be a moment the agent can recognise on its own, without
re-reading the file to work out whether the moment has arrived.

`AGENTS.md` itself needs no trigger: it is loaded, so it is the thing that fires
the other three.

**Why the scaffold holds questions and not decisions.** This is Principle 2
applied to time rather than to location: a decision recorded before the stack is
known is not a decision, it is a guess wearing a decision's clothes. PRA's own
rule — *a claim you can't source becomes a question, a proposed ADR, or an
unconfirmed entry, never a rule with a hedge* — is the same rule. So `DECISIONS.md`
opens with the questions the project cannot answer yet, and the first entry under
`Status:` is `Open`.

**Why the scaffold is not the rule set.** The rule set arrives later, once the
stack is known, and it is generated against that stack. A scaffold that already
contained rules would either have to be rewritten wholesale or — worse — survive
alongside them and be loaded twice. One owner per fact, and at this point the
facts are questions.

**Who writes to these files afterwards: not this skill, and not the planning
skill.** They are the project's cross-session memory. The agent maintains them.
This skill's job is done when the four files exist and are structurally sound —
headings present, one canonical spot for a correction in each.

**Verify before declaring done**, because the failure is silent and a scaffold
that is wrong looks exactly like a scaffold that is empty:

1. All four files exist, at the project root, with their headings.
2. **`AGENTS.md` names each of the three files twice: once for what it holds, and
   once for the condition that makes you write to it.** A description with no
   trigger is a container with no instruction to fill it.
3. `LEARNINGS.md` has exactly one place to append a correction — the audit
   already fails a set that offers two, because the stale half is the one an
   agent reads.
4. `DECISIONS.md` entries carry a `Status:` line. The scaffold's own entry is
   `Open`.
5. No file contains a rule, a threshold, a command, or a version pin. If it does,
   the scaffold has become a second rule set.
6. **Every cross-reference between the four files uses the exact uppercase name.**
   `AGENTS.md` refers to `DECISIONS.md`, never to `decisions.md` — on a
   case-sensitive filesystem the lowercase name resolves to nothing, and the
   reference fails silently at the moment somebody follows it, which is months
   later. Check the prose, not only the table: the two leak separately.
7. **The conditionals are resolved.** See below.

### The one conditional in this mode, and why it exists

`templates/memory/` carries a single `{{#if forge-present}}` block, in `AGENTS.md`
and in the ownership table of `SESSION_LOG.md`.

**Resolve it by testing the filesystem: a `.forge/` directory at the project root
means the block is kept; otherwise it is deleted.** There is no template engine,
and inventing one is a second thing to maintain.

**This is the whole point.** Those blocks used to be unconditional, so they named
`.forge/conventions.md`, `.forge/architecture.md`, `.forge/state.json` and
`.forge/audit/issues.md` as places the stack lives — in a project that has no
`.forge/` at all, which is the ordinary case for anyone using this skill
standalone. It is not a dangling link that costs nothing: it is a **false
instruction in the file every session loads first**, telling the agent the stack
lives somewhere it does not, at the moment it builds its picture of the project.

Standalone use is the common case, so the standalone branch is the one that has to
read correctly with nothing else present.

**Check both directions.** Emit the scaffold for a project without `.forge/` and
confirm no `.forge` string survives; then for one with, and confirm the
references are there. `rules-selftest.js` §`no_forge_coupling` enforces the first
direction automatically — the second has no project to run against, so it stays
a reading check.

## The template library

`references/templates/` — three tiers. **You select from it; you never copy it
wholesale, and you never edit it during a run.**

| Tier | Directory | Emitted |
|---|---|---|
| Core | `templates/core/` | Always. **Eight** files: entry file, architecture, workflow, git-workflow, quality-gates, code-review, coding standards, security |
| Domain | `templates/domain/` | Selected by detection. Eleven files: data & state, errors & async states, forms, UI components, accessibility, testing, **dependency security**, performance, i18n, design system, external system contracts |
| Technology | `templates/tech/` | Selected by detection. Eight overlays, plus four variant deltas in `tech/variants/` |

**Why eight core files, and what a ninth would have to justify.** They are the
rules that hold in any project in any language, **or the rules that decide
whether any other rule is enforceable at all**. The second half is the part
that matters: `quality-gates.md` owns the commands that make the rest checkable,
and a set that omits it has rules nothing can verify — which is the failure this
skill exists to prevent.

A ninth would have to clear the same bar, and "it is a good topic" is not the
bar. The bar is: *does every project need it before it can act, or does every
project need it before it can check whether it acted correctly?*

**Selection is a lookup, not a judgement call** — `references/stack-detection.md`
is the table, and every emitted template records the signal that triggered it.
Every omitted template records the row that excluded it. "No test runner
configured" is a finding worth surfacing; silence is not an acceptable reason.

**Variants are deltas, not replacements.** A variant states which files change
and how. Applying two variants means applying two delta files — never write a
combined variant, and never let a delta restate what it modifies.

**When you need to know *why* a template is shaped the way it is** — because you
are changing a template, adding one, or checking what a change would drop — read
`provenance/synthesis-provenance.md`. It maps every rule from the three source
projects to its template, with what was merged, deduplicated, cut, and left
project-specific.

**No run reads it.** It is the audit trail for the consolidation that produced
this library, and it is 441 lines of history. Keeping it in `references/` and
instructing every run to read it was an error: a file in the library is a file an
agent reads, and this one has no recurring value.

## Workflow

### Step 0b — Scan, and let the scan decide

**Run this before Step 1, and before any threshold is written.** Protocol in
`references/baseline-scan.md`; run it, don't read it and describe it.

The scan answers three questions in one pass, and all three used to be answered
by guessing:

1. **What is the stack, exactly?** — resolved from the manifests, not from an
   impression of them.
2. **Is the project green today?** — every gate, run, with the output captured.
   A rule set written on a project whose lint is already red must say so, or its
   Definition of Done is red on arrival and gets ignored on day one.
3. **`greenfield` or `ratchet`?** — **derived from the scan, never asked.**
   Asking makes the mode a preference; deriving it makes it a consequence, and a
   consequence is identical on two runs of the same repository.

A mode decided by interview varies with the agent's mood and with the phrasing
of the question. That variance is what produced a 6-file rule set on one project
and a 17-file one on another from the same template library.

Write the result to `docs/quality-baseline.md` — a project artefact, not part of
the rule set — and report it in the six-line form the protocol gives.

**"The command is not installed" is a result.** Record it as `absent`, propose
the installation, and emit the gate with that status. **Never** write a baseline
number that no command produced.

### Step 1 — Probe, then interview

**If the caller asked for the context scaffold, stop here** and run
§ The context scaffold. Do not probe, do not scan, do not interview, do not
produce a stack. Probing on a project whose stack has not been decided produces
a manifest match and a table of domain rows that have nothing to match — a
confident-looking report about nothing, which is the mode's entire purpose to
avoid.

Otherwise, take the stack the scan resolved, run the detection probe
(`stack-detection.md`), match the table, produce a proposed template set. Don't
ask what the repository already says.

**Then ask only the gaps the probe can't close.** Usually one or two questions:

- **Target format** — the one question that can't be inferred. See
  `references/target-formats.md`. **If the user has already stated a preferred
  structure, that is the specification, not a default to improve on.**
- **Git strategy** — trunk-based, git-flow or release-train. Also not
  derivable: both branches cost something, and they are not reversible by the
  same amount. With no preference, choose trunk-based and record it in
  `DECISIONS.md`; "no strategy" is the only option nobody can reverse.
- **Variants that are decisions rather than detections** — router, rendering
  strategy, whether a state library is wanted. A component-library axis is
  settled by what's installed; a data-access axis is a decision, so ask.
- **Monorepo or single app**, and for a monorepo, which packages are in scope
  (`references/monorepo-strategy.md`).
- **Team or solo** — affects how much day-one scaffolding is worth it.
- **Anything already decided** — closed decisions, an existing memory system, a
  design contract, a deployment story.

**If the user says "just generate something reasonable for X," don't force the
interview.** State the assumptions you're filling in and proceed. Confirm only
what would silently produce the wrong architecture — the target format is the one
that qualifies.

**Do not ask about the thresholds.** They are decided in `baseline-scan.md`
§Mode selection, and asking reintroduces exactly the variance the scan was
added to remove.

### Step 2 — Verify against real sources

**Before writing any technology-specific rule, work down the ladder in
`references/documentation-sources.md`.** The project itself first — the
manifest's exact version, the installed source, the shipped type definitions.
Then what the framework bundles for agents. Then configured MCP servers, checked
rather than assumed. Then official documentation **for the exact pinned
version**. Then the installed CLI's own help. Web search last.

**Every technology-specific claim carries a provenance marker** naming its rung,
or it's marked as a project decision with its ADR. **A claim you can't source
becomes a question, a proposed ADR, or an unconfirmed entry in
`external-system-contracts.md` — never a rule with a hedge.** "Probably X, but
verify" carries a rule's authority and a guess's reliability, and the agent acts
on it.

**Do not skip this step because the framework is familiar.** The failure it
prevents is invisible: the code compiles, looks idiomatic, and calls an API that
moved two releases ago.

### Step 3 — Choose the mode

Run the mode probe (`existing-project-protocol.md` §Mode detection). It's a
lookup:

- **No instruction files present** → Step 4.
- **Instruction files present** → **run the full existing-project protocol**,
  and in particular **Step A: detect the project's actual conventions before
  drafting a single rule.** Read the code, not the manifest. Record each
  convention with a `file:line` reference. Produce the gap report, show it to the
  user, and let them choose per dimension between preserving the project's
  conventions and staging a migration. **A rule contradicting a working
  implementation is worse than no rule** — the agent will either follow the rule
  and break the code, or follow the code and distrust the whole file.

**A project with a README and no instruction files is a bootstrap, not an
adoption.** A README is documentation, not rules.

**On a project with no code yet:** the detection probe matches the manifest and
nothing else. Every conditional-domain signal — a form, a test runner, a
localisation layer, a design contract, an external system — requires existing
code, so on day one the probe returns the core tier plus whatever the manifest
names, and the domain selection becomes a **question, not a lookup**. Say that
plainly rather than presenting a table that turned out to have nothing to match,
and do not report the day-one omissions as findings — "no test runner
configured" is true and worthless before any code exists.

### Step 3b — Measure the set before delivering it

```bash
# the target's actual instruction surface
find .opencode/rules -name '*.md' -exec cat {} + | wc -l
wc -l AGENTS.md
```

Compare against the budget for the target chosen in Step 1 (Principle 6b). If it
is over:

- **Move trigger-based content out of always-loaded files.** A section that
  applies only when a diff touches auth, or only inside one monorepo service, is
  being paid for on every session it does not apply to. This is the only lever
  that works on a glob-loaded target.
- **Compress the framing, never the rule.** A rule loses its justification clause
  before it loses its threshold, its command, or its ban.
- **Cut whole rules last**, and tutorial prose only. Budgets are ceilings, not
  targets — but a set 2× over a ceiling is a defect, not thoroughness.

### Step 4 — Draft

Fill each selected template. Three things to get right:

- **Section order is fixed and it is a priority order**: commands → definition of
  done → escalation → task-organised sections → versions and banned patterns →
  style last. An agent needs to know how to build before it needs to know how to
  format. **Style is last and is the first thing cut.**
- **Task-organised sections, not flat bullet dumps** — "when writing X", "when
  reviewing X". This is where operational-prose decision rules live, and they're
  the first thing lost in a flat list.
- **Point at one canonical example already in the codebase** rather than pasting
  a code sample. Pasted code goes stale silently; a file reference doesn't.
- **Carry the why on the rule, in one clause.** A template's `GENERATOR NOTES`
  block is deleted on emit, so anything an agent would need in order to apply a
  rule to a case the template didn't anticipate has to live on the rule itself
  (`rule-file-template.md` §The Generator Notes contract). Derivation belongs in
  the notes; application belongs on the rule.

**Three operations, and they are not interchangeable** — know which one you're
doing before merging anything:

| Operation | What happens | When |
|---|---|---|
| **Absorb** | Full content transfers to the target at comparable depth; the source is deleted because its content now lives there | The source's rules genuinely belong in the target's scope |
| **Reference** | The source stays; the target points at it by name **and section** | The source is too large or too specific to inline |
| ~~Delete and mention once~~ | Replacing substantive rules with a grep or a one-liner | **Never.** This is silent content loss wearing a structural disguise |

**After absorbing anything, verify immediately** — before moving to the next
file, while the source is still open:

1. List every discrete rule in the source: numbered items, thresholds, banned
   patterns, decision rules. Not just commands.
2. Confirm each appears in the target at comparable depth — a full sentence or
   an enforcing command, not a passing mention.
3. **If the rule count drops, something was lost — not condensed.** A 94-line
   source producing three bullets in the target is a signal, not a success.

### Step 5 — Audit

**Part A is a command. Run it before reading anything.**

```bash
node "$PRA/scripts/rules-selftest.js" <project>
```

Ten decided checks — wiring, index, placeholders, cross-references,
contradictory thresholds, `.forge/` coupling, contamination, unenforceable prose,
gates, budget. **A failure is a defect, not a discussion.** Fix it and re-run.
The script's own self-test (`node "$PRA/scripts/selftest.js"`) proves each check
detects what it claims to, so a pass is evidence and not a formality.

**Then Part B**, the judgement half of `references/audit-checklist.md`. Do not
automate it and do not report it as verified when it was not. The sections that
catch what the others can't:

- **Content preservation** — for a consolidation. Redundancy and contradiction
  checks compare the new set against *itself*; a set can be perfectly
  non-redundant while having lost a third of its rules. Requires a reconciliation
  count: *"N rules preserved, M absorbed with cross-references, K lines of
  tutorial prose cut (listed)."* If you can't state that number, you haven't
  checked.
- **Cross-project contamination** — for an adoption or a port. Part A catches the
  mechanical form; this catches the semantic one, where a borrowed idea is
  expressed in this project's vocabulary and therefore looks native.
- **Contradiction with the code** — for an adoption. For each rule, confirm the
  code doesn't already do the opposite in a load-bearing way. **No other check
  catches this**, because it compares a rule set against a codebase, not against
  itself.
- **Provenance** — every technology-specific claim traceable to a rung of the
  ladder or to an ADR.
- **Promotion** — for a project with an `external-system-contracts.md`: no
  finding sitting unpromised next to a rule it contradicts, and no finding that
  has been generally true for several sessions without reaching a rule file.
- **Divergence** — for a consolidation or an adoption with a migration: every
  detected divergence is either a preserved rule or a migration target. An
  unaccounted one is a rule that was silently dropped.

**Also check:** every "always apply" rule genuinely applies to every session
rather than being secretly scoped; every conflicting priority pair is ranked; no
instruction fails all four checkability tests (a command, a glob match, a
banned-list lookup, or the Principle 1 "would the agent violate this?" test) —
**rewrite the ones that fail, don't cut them on sight**; per-file line counts as
ceilings; every file is referenced from the index; the emitted index lists every
emitted file and no others.

### Step 6 — Wire, deliver, and set up the loop

**Wire the target format — this is part of the deliverable, not a follow-up.**
Generating Markdown without the file that makes the tool load it produces a
complete-looking, entirely inert rule set (`target-formats.md`).

**Merge, never overwrite.** An existing config file carries the user's model,
provider, and tool configuration. Add the keys; don't replace the file.

**Verify the wiring** before declaring done: the config parses; every path it
points at exists; **a glob that matches nothing is a valid configuration that
loads nothing.**

Then tell the user three things:

1. **Where the living-learnings section lives** — one canonical spot. A correction
   is added when the agent gets something wrong *twice*, not speculatively. If the
   project already has a cross-session memory system, wire learnings into it
   rather than creating a parallel mechanism.
2. **The read-back test.** From a cold session, ask the agent for its build
   command, its definition of done, and which rule files govern a given area. If
   it can't answer, the file is too long, too vague, or not being discovered.
   **Fix that before adding more content** — more rules behind a broken wiring
   are more rules that never load. In adoption mode there's a fourth question:
   *what is this project's own pattern?* If the answer describes the template
   rather than the project, the rules are wrong.
3. **The audit result**, in the reconciliation form from Step 5.

**If the templates were wrong** — a tech overlay's mechanism didn't apply, a
domain template had a rule that didn't survive contact with the real project —
**fix the template file, not just the delivered output.** The template is what
the next project copies. A correction that isn't applied there helps nobody, and
the same defect will ship again.

## What to read, per mode

Reading the wrong subset is how two runs of the same task produce different
output. **Read exactly this table, and nothing else** unless the mode changes or
a row says "on demand".

| File | Context scaffold | Bootstrap | Consolidation | Adoption |
|---|---|---|---|---|
| `SKILL.md` | ✔ | ✔ | ✔ | ✔ |
| `baseline-scan.md` | — | **✔** | ✔ | **✔** |
| `postmortems.md` | — | **✔** | ✔ | ✔ |
| `stack-detection.md` | — | ✔ | ✔ | ✔ |
| `documentation-sources.md` | — | ✔ | ✔ | ✔ |
| `target-formats.md` | — | ✔ | ✔ | ✔ |
| `monorepo-strategy.md` | — | monorepo | monorepo | monorepo |
| `research-summary.md` | — | ✔ | — | — |
| `existing-project-protocol.md` | — | — | — | ✔ |
| `audit-checklist.md` | § verify above | Step 5 | Step 5 | Step 5 |
| `rule-file-template.md` | — | on demand | on demand | on demand |
| `architecture-decision-guide.md` | — | on demand | on demand | on demand |
| `mdc-frontmatter-spec.md` | — | Cursor only | Cursor only | Cursor only |
| `provenance/synthesis-provenance.md` | **never** | **never** | **never** | **never** |

**`baseline-scan.md` is read in every mode that emits rules**, and it is read
*before* the mode probe — the scan decides the quality mode, and a protocol
read after the thing it decides has already been decided is a protocol read for
the wrong reason.

**The scaffold reads almost nothing, on purpose.** Four files are written from
one decision — where does a correction go, and where does a question go — and
every reference it read is a chance to import a rule by accident. `postmortems.md`
is skipped because contamination is a risk when you are *emitting* project content,
and this mode emits none.

**`postmortems.md` is unconditional.** Copying a template into a project *is* a
cross-project transplant — the exact operation Case 2 is about — so the
contamination rules apply in every mode, including a bootstrap that reads as
purely additive.

**`synthesis-provenance.md` is never read during a run.** It is the audit trail
for the one-time consolidation that produced this library. It is read when
*maintaining* the library — adding a template, or deciding whether a rule is
universal.

## Reference files

Everything, and what each is for. The table above says *when*; this says *what
for*, for the rows you reach on demand.

- **`templates/`** — the library. `core/` always, `domain/` and `tech/` by
  detection, `tech/variants/` as deltas.
- **`baseline-scan.md`** — the measurement pass that runs before drafting: what
  the stack is, whether the project is green, and `greenfield` vs `ratchet`.
  Owns the **quality mode**, and the baseline artefact.
- **`stack-detection.md`** — the selection table, the exclusion rows, and the
  reporting requirement. Points at `monorepo-strategy.md` for layout.
- **`monorepo-strategy.md`** — the repository's package map, its build tool,
  per-package command discovery, and the root-versus-package ownership rule.
- **`existing-project-protocol.md`** — mode detection, the light and full
  convention-detection paths, the gap report, preserve-vs-migrate, the migration
  stages.
- **`documentation-sources.md`** — the verification ladder, the citation
  requirement, and the **tool-selection rule** (a tool becomes a gate only if it
  is installed, maintained, and exits non-zero).
- **`target-formats.md`** — per-environment entry file, rules location, the
  **wiring file**, and the hook configuration. Owns monorepo **wiring**.
- `rule-file-template.md` — the section skeleton and ordering, the section-tagging
  convention, and what a template may never contain.
- `architecture-decision-guide.md` — the decision tree for file organisation and
  activation modes. Defers format questions to `target-formats.md`.
- `audit-checklist.md` — Part A is the script, Part B is the judgement.
- `postmortems.md` — real caught failures and the fix each produced. Read in
  every mode.
- `research-summary.md` — the evidence behind the principles, read once per
  session in a bootstrap.
- `mdc-frontmatter-spec.md` — Cursor `.mdc` frontmatter, the four activation
  modes, precedence.
- `../provenance/synthesis-provenance.md` — every source rule mapped to its
  template, with what was merged, deduplicated, cut, and left project-specific.
  **Maintained by hand; never read by a run.**

## Scripts

| Script | What it does | When |
|---|---|---|
| `scripts/rules-selftest.js` | Ten decided checks on a **delivered** rule set: wiring, index, placeholders, cross-references, contradictory thresholds, `.forge/` coupling, contamination, unenforceable prose, gates, budget | Step 5, and again after Step 6 |
| `scripts/selftest.js` | Proves each of those ten checks detects what it claims to, on a synthetic broken set | Before changing a check |

**The script exists because the audit checklist could not be trusted.** Every
requirement it stated was decidable, and a decidable requirement written in prose
is one the agent can report as satisfied without running anything. Measured: a
delivered rule set that was internally consistent, cleanly wired, and missing
every quality gate — and which had passed the audit as written.

**Run `scripts/selftest.js` after editing either script.** A check that has
quietly become too permissive reports "all clear" on everything, and the
failure is invisible precisely because the tool still works.
