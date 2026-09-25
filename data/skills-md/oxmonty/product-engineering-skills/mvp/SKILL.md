---
name: mvp
description: Interview the user section-by-section to create or update an MVP design document (roadmap + PRD) from a structured template, then hand off to the companion build-loop skills. Use whenever the user wants to define, spec, plan, or document an MVP, side project, or new tool; asks to "fill in" or instantiate mvp.md / ROADMAP.md / PRD.md; wants to tick off roadmap items after completing work; or asks to update project docs after a change. Also use when the user says things like "let's spec this out", "grill me about this project", "update the roadmap", or "mark E2 done".
---

# MVP Doc

Turn an idea into a decision-complete MVP document set — and keep that document set truthful as work lands. The bundled template (`assets/mvp-template.md`) defines the target structure; this skill defines the process. It is the entrypoint of a collection: the documents it emits are what the companion skills (`/epic`, `/demo-ideas`, `/wrap-up`, `/delegate`, `/spike`, `/regression`) run the build loop against.

There are two modes. Detect which one applies before doing anything else:

- **Create mode** — no instantiated MVP doc exists yet (or the user is starting a new project). Run the interview, then generate the docs.
- **Update mode** — a `ROADMAP.md`, `PRD.md`, or instantiated `MVP.md` already exists in the working directory or was provided. Read it first, then follow `references/editing-rules.md`. Never re-interview from scratch when a doc exists.

The documents ARE the memory. You have no state between sessions; the roadmap's checkboxes and the PRD's sections are the only persistent record of what was decided and what is done. Treat them accordingly: read them fully at the start of any session that touches the project, and reconcile them before the session ends.

## Create mode

### Step 0 — Survey before asking

Never open with questions. First, gather everything answerable without the user:

1. If there's a repo or codebase, explore it: language, entry points, existing README, package manifests, CI config, and the git remotes — an existing `origin` is the repo URL, so take it rather than asking.
2. Read any prior notes, conversation context, or linked docs the user provided.
3. For distribution naming, actually check: query the relevant registries (npm, PyPI, crates.io, Homebrew, GitHub org) for name collisions rather than asking the user to.

Then present a short "here's what I already know" summary and confirm it in one pass. Questions the codebase can answer are questions you don't ask — asking them erodes the user's trust that the interview is worth their time.

### Existing codebases (brownfield)

Create mode on a repo that already has working features changes the opening, not the process:

- The Step 0 survey becomes a **feature inventory**: enumerate the core capabilities that already work (entry points, commands, endpoints) and confirm the list with the user before any interview question.
- The document records that baseline as already-true specification, and the roadmap builds forward from it. There is no walking skeleton to build — the product already walks. E1 becomes the safety net instead: characterization tests that pin existing behavior before new epics change it. Ask (structured question) whether that regression coverage lands before new feature epics — recommend it whenever new work touches existing features.
- If the user names only a single next feature, that's a story, not a roadmap. Apply the positioning gate: ask for their plan for the product — notes, ambitions, the next three things — and interview toward a full roadmap.

### Step 1 — Walk the decision tree

Follow `references/decision-tree.md`. It maps interview phases to template sections in dependency order (identity → surfaces → workflow → validation → features/scope → API → structure → distribution/CI → roadmap synthesis). Read it now if you haven't.

Interviewing rules (these come from hard-won practice; the whole value of the skill lives here):

- **One decision at a time — the rule the interview lives or dies on.** You MUST surface exactly one decision per turn (at most two tightly coupled) through the structured question tool: `AskUserQuestion` in Claude Code, the platform's equivalent where one exists, and a single plain-text question with lettered options on any harness that has neither. Never batch decisions into a wall of questions — it bewilders, draws shallow answers, and turns the interview into a form. The widget is an enhancement; the one-decision-per-turn discipline is mandatory on every harness.
- **Every question ships with your recommendation.** Never ask an open "what do you want?" when you can propose. Format options as concrete choices, mark one "(recommended)" in its description, and say why in one clause. The user should be able to get a good document by mashing the recommended option repeatedly.
- **Context above the fold.** Print a sentence or two of plain-language framing above every question — what surfaced this decision and what it affects — legible to a junior and a staff engineer alike. The question widget shows only the options; the framing printed above it is the only context the user gets. Keep it brief enough that the question stays the focus.
- **Probe the trade-off, not the preference.** For each decision, name what each option costs. "Library-first or CLI-first?" is weak; "Library-first keeps the CLI a thin wrapper and forces a clean public API, but delays the demo-able moment — CLI-first inverts that. Which loss hurts less?" is the question.
- **Skip logic is mandatory.** Conditional sections (API design, pipeline model, artifact structure) get zero questions when they don't apply. Infer applicability from earlier answers; confirm with one yes/no only if genuinely ambiguous.
- **Draft as you go.** At the end of each phase, write that section of the document immediately and show it (or a tight summary of it). Get a quick confirm, then move on. Do not hold the whole document in your head until the end — early sections inform later questions, and the user catches misunderstandings while they're cheap.
- **The positioning clause is a gate.** Per the template: if the user cannot articulate the one-line positioning against the incumbent or gap, stop the interview and work on that first. Everything downstream depends on it.

### Step 2 — Synthesize the roadmap last, place it first

The roadmap is derived, not interviewed. Once the design sections exist:

1. Derive epics from the sections, ordered by dependency. E1 is a walking skeleton unless the user explicitly opts out — and its spine is the product's core primitive: the first stories make the hero loop run end to end in its thinnest form ("start the app, see hello world"), the closing stories ship it through **one** real channel. Proving one deploy path early is the skeleton's point; the remaining channels are their own later epic, never E1 ballast in front of the core. (Brownfield repos skip the skeleton: E1 is characterization coverage — see above.)
2. **Artifact-first epics.** Every epic above the MVP line ends in a shippable artifact someone outside the session can touch — a pushed repo, a published package, a live URL, a cut release — named in the epic's outcome line as its exit criterion. Below the MVP line, epics name the feedback loop they open instead: who uses the thing and what signal you collect. The walking skeleton is the pattern, not the exception.
3. Cap epics at ~6 stories; split anything larger (and consider splitting its design section too). Stories lead with an action verb — "Add …", "Ship …", "Template …" — and stay within two sentences.
4. Every epic links to the design subheading that specifies it. A story with no section to link to means the design is missing or the story is speculative — flag it, don't silently include it.
5. Propose the MVP line. Ask the user to confirm where it falls — this is the one roadmap question worth asking rather than inferring.
6. Present the full roadmap for reorder/veto before writing it into the doc.

### Step 3 — Emit the document set

The output shape is fixed, whatever the project's size: `ROADMAP.md` + a dated PRD (`docs/plans/<date>-prd.md`) + one file per epic under `docs/epics/`. Even a two-epic roadmap gets its epic files — there is no inline-stories layout and no shape question to ask. One shape means every companion skill (`/epic`, `/wrap-up`, `/regression`) finds stories in the same place in every project.

Why: the roadmap is high-churn state (ticked constantly) while the PRD is low-churn specification (edited only when decisions change). Separating them shrinks the blast radius of every edit — an agent ticking a checkbox never has the PRD in its diff, which is the cheapest structural defense against accretive editing. Links still work: roadmap entries point to `docs/plans/<date>-prd.md#anchor`.

`ROADMAP.md` is a thin index — the description, hero example, "Usable as" bullets, epic order with one-line outcomes, and the MVP cut (it doubles as the project's front page). Each epic's stories live in their own file, `docs/epics/E<nn>-<slug>.md`, alongside its spec link (and, once `/epic` kicks it off, its `## Acceptance criteria` and `## Exit criteria`), so a tick's blast radius is one epic's file. Zero-pad the file prefix (`E01-`, `E02-`) — unpadded, `E10` sorts between `E1` and `E2` in every directory listing. The PRD gets Workflow, Surfaces, Validation, Features, API design, Project structure, Distribution, CI/CD, Additional considerations, Competitive landscape, Tech stack, References, License, Open questions. Delete the template's instructional blockquotes and HTML comments from instantiated docs.

## The journey (close every create-mode session with this)

The documents are step one of a loop this collection runs end to end. After emitting the files, print the road ahead so the user knows the next command at each stage:

1. `/epic E1` — kick off the first epic against its PRD section; the section is the spec, the epic ends in its named artifact.
2. Build, using `/delegate` to hand implementation down while judgment stays in the main loop, `/spike` when a design question blocks a story, and `/regression` to pin each feature before its epic closes.
3. `/demo-ideas` when an epic ships — every epic should end in something you can show someone.
4. `/wrap-up` at the end of any working session — propose ticks with evidence, update the docs non-accretively, summarize.

If a companion skill isn't installed in the target project, say so and do the equivalent inline rather than skipping the step.

## Update mode

`/wrap-up` is the user-invoked face of this mode — reach for it at session end. The rules below also bind model-invoked doc edits mid-session.

Read `references/editing-rules.md` before touching an existing doc — it contains the editing philosophy and the tick-off protocol. The two non-negotiables, summarized:

1. **Rewrite, don't accrete.** When updating prose, replace obsolete text with accurate text rather than preserving the obsolete text and adding a correction. The final document should read as if it were written correctly from the beginning. History belongs in git, the changelog, or your chat summary — never inline in the doc.
2. **Propose ticks, don't strike unilaterally.** After completing work, list the stories you believe are done with one line of evidence each, ask the user to confirm (structured question: confirm all / pick / none), and only then tick. A checkbox is a claim that something is verifiably true; the user is the verifier of record unless they've told you otherwise.

## After generating or updating

- Run the accretion self-check from `references/editing-rules.md` on any file you edited.
- Verify every roadmap link resolves to a real heading (anchors break silently when headings are reworded).
- Summarize in chat what changed and what remains — the narrative goes here, not in the documents.
