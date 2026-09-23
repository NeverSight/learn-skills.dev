---
name: video-to-skill
description: "Turn a video, tutorial, playlist, or course into an installed, evidence-grounded course Skill that can teach, give practice and feedback, apply demonstrated methods, and answer reference questions. Use when the user provides video sources and wants reusable learning or operational capability."
---

<!-- argument-hint: <video-url-or-local-path>... [skill-name] -->

# Video-to-Skill

Convert demonstrated capability, not a transcript summary. Own the complete workflow from accessible source discovery through installation of one course-specific Skill.

## User contract

A normal invocation is:

```text
/video-to-skill <URL>     # Claude Code
$video-to-skill <URL>     # Codex
```

Treat supplied URLs or local paths as authorization for reversible local processing. Process every accessible playlist or course item by default, resume cached work after interruption, and keep the private evidence workspace separate from the portable Skill.

Ask only when a material boundary cannot be inferred safely: credentials are needed, local or private media would leave the machine, a billed dependency is required, scope is unexpectedly large, the user must choose between materially different curricula, or an installation name conflicts with different content.

Infer one canonical artifact language for every new build from the user's substantive request and conversation language. Honor an explicit language or locale exactly. For an ordinary personal build, use the user's language; for an explicitly public international release, recommend English unless the user named another audience. Ask only when competing language choices would materially change the intended audience and the intent cannot be inferred. Keep this separate from source caption or ASR selection.

Never ask the user to run internal commands, supervise extraction, select frame parameters, copy task payloads, or invoke a second tutor Skill. Never request an account password.

Resolve the complete expected source set before treating acquisition as complete. Preserve playlist order and explicit complete, partial, failed, skipped, inaccessible, or retired states. Continue through isolated source failures when useful material remains, never silently omit an expected item, and report how missing material limits the generated Skill.

Use the engine's product-level analysis-depth contract instead of choosing frame or task knobs. `auto` deterministically recommends `standard` or `deep` from inspected duration, item count, chapters, caption coverage, and content signals. Use an explicit `standard` or `deep` when the user requests it. Use `archival` only when the user explicitly accepts its materially higher private storage and review boundary; it is never an implicit default. Analysis depth cannot authorize hosted vision, a paid provider, credentials, media redistribution, or visual processing disabled by `visual_profile=transcript`.

The engine is model-agnostic and never calls an LLM. The host main agent dispatches native workers for semantic, multimodal, pedagogical, and critical judgment; deterministic code owns acquisition, bounded packets, task state, validation, compilation, rendering, and installation.

This workspace-centered release supports new conversions and deterministic resume. Update or fold-in of new evidence into an existing generated Skill is not implemented. Never present regeneration as a safe update, overwrite an existing different Skill, or discard human edits; retain the new workspace or staged output and state that update remains unsupported.

## Start the engine

Resolve the directory containing this `SKILL.md` to an absolute `SKILL_DIR`. Do not infer it from the conversation working directory.

```text
video-to-skill/
├── SKILL.md
├── scripts/
│   ├── video-to-skill
│   └── video-to-skill.cmd
├── pyproject.toml + src/ + scripts/video_to_skill.py
└── runtime.json + scripts/engine.py
```

On POSIX, bind and verify the absolute launcher:

```bash
V2S_ENGINE="$SKILL_DIR/scripts/video-to-skill"
"$V2S_ENGINE" --help
```

On Windows, use `scripts\video-to-skill.cmd`. The launcher owns first-use bootstrap, its private Python runtime, bounded repair, and optional capability installation. Do not activate an environment, invoke a package manager, or use `eval`.

If the launcher is missing, report that the installed generator Skill is incomplete. If bootstrap reports a missing supported Python, network failure, or a compact bundle whose recorded runtime no longer exists, report that exact condition and request repair or reinstallation. Do not improvise a replacement environment or claim extraction occurred.

Choose a durable workspace outside the generated output and installed Skill. Use the current host without asking when it is known.

## Run the durable workflow

Start a new conversion:

```bash
"$V2S_ENGINE" run SOURCES... --workspace WORKSPACE --host codex --output-language LANGUAGE --analysis-depth auto
"$V2S_ENGINE" run SOURCES... --workspace WORKSPACE --host claude --output-language LANGUAGE --analysis-depth auto
```

Always pass the inferred or explicit artifact `LANGUAGE` on a new run. Use `source` only when the user specifically wants artifacts in the source language. `--language` is a separate optional preference for source captions and ASR and never controls generated prose. If `source` evidence is uniformly known, the engine resolves it deterministically; mixed or incomplete source-language evidence requires the bounded curriculum agent to declare one canonical language under the persisted contract.

Add `--project` only when the user requested project-local installation. Add `--output` only when the user supplied a portable output path. Resume without retransmitting sources or configuration:

```bash
"$V2S_ENGINE" run --workspace WORKSPACE
```

On resume, omit `--output-language` and reuse the persisted value. Never silently change it; an explicit conflicting resume override is rejected.

### Publish another edition from the same Analyze map

When the user wants a separately named localization or a different already-planned learning path, create or resume a named edition instead of starting a new conversion:

```bash
"$V2S_ENGINE" edition WORKSPACE EDITION-NAME --host codex --output-language LANGUAGE --curriculum PATH-ID --skill-name SKILL-NAME
"$V2S_ENGINE" edition WORKSPACE EDITION-NAME --host claude --output-language LANGUAGE --from-edition SOURCE-EDITION --curriculum PATH-ID --skill-name SKILL-NAME
"$V2S_ENGINE" edition WORKSPACE EDITION-NAME --host codex --output-language LANGUAGE --plan-curriculum --skill-name SKILL-NAME
```

Use `--curriculum` to bind an existing path without another curriculum-planning worker. Use `--from-edition` only when the path and logical artifact/claim identity should come from another named edition; otherwise the legacy single-edition checkpoint is the source. Use `--plan-curriculum` only when a new learning design is actually requested. These choices are settled before artifact Authoring.

Resume with only:

```bash
"$V2S_ENGINE" edition WORKSPACE EDITION-NAME
```

A named edition never inspects, acquires, transcribes, extracts visuals, or reruns Analyze. It pins the completed integrated Analyze task, source snapshot, semantic-record digests, and analysis-depth contract, then runs only the necessary curriculum checkpoint followed by full Author, isolated behavior trials, independent Review, compilation, validation, and no-clobber installation. If source/depth refresh or a new Analyze revision changes that lineage, create a new edition name instead of silently reusing it.

Each edition has immutable language, curriculum-source, output, name, host, and installation-scope configuration. Multiple editions coexist without an active-edition switch. Submit returned tasks with ordinary `submit WORKSPACE TASK_ID RESULT_FILE`; the task scope resolves its edition. Preserve semantic IDs and, for localization of the same curriculum, logical artifact IDs, claim IDs, evidence links, and timestamps. Supply `--identity-drift-reason` only for a real structural exception. It records justification; it is not update lineage, and `parent_build_id` remains unset.

Also omit `--analysis-depth` on resume and reuse the persisted requested/effective depth and versioned budget profile. A conflicting request or profile drift is rejected. `--refresh` re-inspects the inventory; when duration, items, chapters, captions, or density signals change, the engine deterministically refreshes the contract and invalidates only affected stage/task snapshots.

`run` performs every available deterministic transition and emits one JSON envelope.

### `actions-required`

Dispatch every independent action in the returned parallel group when the host supports workers.

For a `dispatch-agent` action, use its exact `persona_hint`, absolute `task_path`, `role`, and task ID. Do not read or copy its packet through the main-agent conversation.

Give the worker only:

```text
Use the assigned expert persona.
Open TASK_PATH/task.json, packet.json, result-schema.json, and lease.json.
Perform the bounded task from workspace evidence.
Write the strict result to TASK_PATH/output/result.json.
Run ENGINE submit WORKSPACE TASK_ID TASK_PATH/output/result.json yourself.
Return only task state, result digest, material blockers, and unresolved material gaps.
```

The worker may use bounded `context`, `contact-sheet`, `frames`, `query`, and `gaps` commands when the task packet permits them. It must never write SQLite directly, inspect unrelated workspace material, return private chain-of-thought, or send large semantic results and drafts through the main agent.

For an `ask-user` action, ask the supplied prompt with its supplied options. Write the selected option to the task's strict decision result, submit it, and do not reopen settled implementation details.

After all dispatched workers finish, call `run --workspace WORKSPACE` again. Repeat until `complete` or an ordinary command failure.

### `complete`

Report the installed Skill name and path, invocation, workspace path and retention, processed and failed source counts, source and semantic coverage, instructional-affordance coverage, critic repair count, build ID, and validation results.

Also report the requested output-language intent, resolved canonical artifact language, resolution state, and whether it was deterministically resolved or agent-declared.

For a named edition, also report its deterministic edition ID and configuration digest, pinned Analyze/source/depth lineage, curriculum source and selected path, identity-drift justification if any, and edition-local completion status.

Report requested, recommended, and effective analysis depth, the recommendation reasons, and the versioned non-secret budget summary from the completion envelope.

Make partial, inaccessible, skipped, retired, and failed sources visible in the completion summary. Distinguish source-acquisition coverage from semantic coverage and state any capability limits caused by missing evidence.

End with one or two concrete next actions using the installed name:

```text
/<course-skill> start                         # Claude Code
$<course-skill> help me apply this to my work # Codex
```

Do not claim completion from a worker message. Only the engine's `complete` envelope proves that canonical state compiled, validated, and installed.

## Failure and recovery

Keep the workspace after success or failure. Never delete it merely to recover from an interrupted source, worker, review, validation, rendering, or installation stage.

Resume the same workspace after interruption. Reuse its immutable configuration, source snapshot, task directories, accepted canonical records, and completed work. Do not retransmit sources, choose a new output path, or create a replacement workspace to bypass a rejected task or conflict.

When a submission is rejected, preserve the task output and report the exact schema, lease, digest, evidence-scope, or snapshot error. Correct or redispatch only the affected durable task. Do not copy its large packet or result through the main-agent conversation.

When a source fails, continue the remaining accessible sources and let the coverage ledger carry the loss. When all useful sources are inaccessible, stop after persisting the acquisition state and explain what authorization or source change is required.

When validation or compilation fails, retain the workspace and any safe staging artifact, report the failing gate, and resume after repair. When generated or installed content conflicts with the requested name, use the coordinator's durable `ask-user` naming decision. Never overwrite different content.

## Worker roles

The logical workflow is `Analyze → Author → Review`. These are reasoning boundaries, not public commands or user-facing modes.

### Analyze

Use a senior evidence and semantic-analysis expert. Combine high-recall extraction, terminology normalization, relation linking, materiality review, disposition accounting, conflict capture, and capability-ceiling analysis in one bounded role.

Preserve questions, claims, reasons, examples, analogies, definitions, distinctions, qualifications, counterpoints, predictions, recommendations, warnings, value judgments, and open questions. Preserve relations that answer, support, explain, exemplify, qualify, contrast, depend on, update, contradict, raise, or leave another unit unresolved.

Use speech-first packets for interviews and talking heads. Inspect slides, code, UI, diagrams, or physical state only when visual evidence is material. For long courses, accept section-group tasks and then perform a dependent integration Analyze task without deleting source-specific semantic units.

The engine supplies the visual evidence index: first frame, scene-change frames, periodic fallback frames, perceptual-hash deduplication, OCR and type hints, plus bounded dense windows requested during investigation. Analyze supplies the semantic decision: propose at most 24 non-duplicate teaching candidates, each as one frame, one normalized crop, or an ordered two-to-four-frame sequence, only when it materially improves teaching or verification. Analyze never edits pixels or supplies an arbitrary image path; the engine validates the evidence IDs and deterministically materializes sanitized PNG candidates.

Every semantic unit needs a stable ID, source and time range, kind, compact summary, materiality, disposition, modality, evidence IDs, observed-versus-inferred status, confidence, and uncertainty. Merged, context-only, and omitted material needs an explicit reason.

### Author

Author has two bounded task shapes under the same internal role. First, use a principal curriculum architect to read the canonical semantic records, recommend a thematic path, and propose up to two justified alternate learning experiences. This curriculum-planning task writes only curriculum options, ordered semantic-unit sequences, and concise decision metadata—never artifact plans, claims, assets, or Markdown drafts.

The curriculum packet includes the immutable artifact-language contract. It must echo a fixed explicit or uniform-source language, or make the one constrained declaration required for mixed or unknown source evidence. That declaration is canonical. Full Author and every repair must preserve it exactly; Review audits actual prose for consistency because deterministic code does not pretend to identify the language of arbitrary Markdown reliably.

When the alternatives would materially change the learning experience, stop at the durable `ask-user` action. Otherwise the coordinator canonically selects the recommendation. Only after that selection exists, dispatch the full Agent Skill author with the selected-curriculum path and digest. The full Author must preserve the selected path and planned semantic order while binding them to justified artifacts and writing Markdown drafts inside its task output directory. Do not reopen the curriculum choice during authoring or repair.

Treat Learn, Practice, Apply, and Reference as evidence-bounded capability levels, not artifact quotas. Never exceed the Analyze capability ceiling.

Complete the instructional-affordance ledger independently from semantic coverage. Account for learning objectives, misconceptions, retrieval and transfer prompts, focused exercises, success criteria, scored rubrics, progressive hints, retry, capstone synthesis, operational playbooks, expected states, validation, recovery, quick reference, and decision rules.

Mark each affordance `provided`, `unsupported`, or `not-applicable` with a rationale. Strong capability claims require the complete corresponding surface; weaker or unsupported claims remain honest. Multiple affordances may live in one independently useful artifact.

Give every artifact a stable ID, user job, supported behaviors, normal or after-attempt disclosure, independent loading reason, semantic-unit links, affordance links, destination path, draft path, and digest. Keep solutions and answer-bearing rubrics separate and after-attempt.

Select only from the verified visual candidates in the Author packet. Retain a visual only when a specific artifact needs it, link the PNG from every `used_by` artifact, and bind it to claims that preserve the same visual or temporal evidence. Leave decorative, redundant, illegible, private, or text-recoverable candidates unused.

### Review

Use a fresh senior Agent Skill critic who is independent of both curriculum-planning and artifact-Author producers. Review the actual canonical drafts and records, not an author-supplied summary.

Audit source-meaning retention and instructional-affordance retention separately, then grounding, uncertainty, disclosure, empty invocation, runtime behavior, safety, scope, source failures, and shareability. Inspect every selected teaching visual for necessity, legibility, context, ordering, privacy, evidence grounding, and on-demand loading.

Before the final critic, let the engine render the canonical Author state into its private immutable behavior target. The engine owns a versioned scenario catalog: empty invocation, start/intake, bounded teaching, practice solution withholding, application context gathering, precise grounded reference, out-of-scope honesty, and deterministic semantic pressure cases for an opening thesis, middle example, qualification, likely misconception, prediction, unresolved question, and visual or temporal evidence when present. It marks content cases not applicable only from canonical semantic state.

Dispatch every applicable scenario as its own `behavior-trial` Review task so the host supplies a genuinely fresh context. The engine issues a distinct `execution_context_id` with each task lease and rejects a result that does not echo that binding, but this identifier does not prove operating-system, process, filesystem, or model-context isolation; the host must dispatch each trial and the final judge in genuinely separate contexts and enforce any required sandbox or read-only boundary. A trial receives only the immutable target and one prompt, records the exact bounded user/assistant exchange, generated-Skill file accesses, and side effects, and makes no pass/fail judgment. After all trials complete exactly once, dispatch a different independent Review producer to inspect the actual rendered target, canonical evidence, code-owned expectations, and raw trial files. Raw trials and structured reports remain in the private workspace and never enter the installed Skill.

Compilation accepts only the current behavior-catalog version with complete scenario accounting, verified trial and target digests, a passing critic, and passing applicable checks. Legacy boolean-only behavior reports remain preserved as history but never satisfy the current gate; resuming such a workspace creates fresh catalog trials and a new Review revision.

A failed Review completes its execution task but creates a new immutable Author revision pinned to the same selected curriculum and a fresh independent Review. Allow at most three repair cycles. Never weaken a capability claim merely to hide an affordance the evidence supports and the product needs.

## Evidence rules

- Speech establishes stated intent or explanation.
- A visible-state claim requires visual evidence.
- An action or transition normally requires ordered before and after evidence.
- A successful procedure requires the action and an observable result.
- Exact code, commands, labels, or values remain uncertain when illegible.
- Two probes that add no evidence are a stopping signal, not permission to guess.
- Low-confidence exact details never become authoritative instructions.
- Source-acquisition coverage and semantic coverage remain separate.
- Every material semantic unit receives a disposition.
- Every included core or supporting unit appears in a grounded artifact.

Use native host multimodal inspection before any hosted vision provider. Keep hosted vision disabled unless native viewing is unavailable or the user authorized the privacy and cost boundary.

## Authentication and secrets

When a source needs login, negotiate authentication once for the complete run. Offer a named browser/profile, a local Netscape `cookies.txt`, or public items only. Set `VIDEO_TO_SKILL_COOKIES_FROM_BROWSER` only for the engine invocation and never request an account password.

When browser authentication is authorized, let the engine decrypt browser cookies once, create a private temporary snapshot, and reuse isolated copies for source inspection and concurrent workers. A supplied cookie file is snapshotted rather than modified in place. The engine removes its temporary snapshots when the authentication session exits.

On macOS, a browser keychain prompt may appear once. Repeated prompts during one engine invocation indicate a failed authentication session; stop and report the failure instead of repeatedly asking the user to approve access.

Treat cookies, headers, tokens, expiring URLs, and browser snapshots as runtime secrets. Never quote them back, place them in task packets or logs, persist them in the workspace, or include them in the generated Skill.

Let the engine record tool provenance directly at its subprocess and provider boundaries. It stores stable logical runs, attempts, failures, cache reuse, normalized non-secret arguments, input digests, and workspace-relative output digests in SQLite; do not ask workers or the main agent to reconstruct or relay this data. Use `tool-runs WORKSPACE` only when a maintainer needs the canonical sanitized JSONL under `WORKSPACE/logs/`. Raw stdout, stderr, environment variables, credentials, signed URLs, private absolute paths, and tool records themselves never enter the portable generated Skill.

## Export evidence bundles

Export evidence only when the user asks for a reproducibility or preservation artifact. The engine assembles and verifies bundles directly from canonical workspace state; no LLM reads, rewrites, or transports their contents.

```bash
"$V2S_ENGINE" evidence-bundle WORKSPACE --mode compact --output /path/to/course-evidence.v2sbundle
"$V2S_ENGINE" verify-evidence-bundle /path/to/course-evidence.v2sbundle
```

A compact bundle is a deterministic shareable evidence derivative, not a generated Skill. It contains sanitized source metadata, canonical semantic/design/review records when present, observations and gaps, selected teaching visuals and contact sheets, sanitized tool-run records, and a content-addressed manifest. It never contains raw video or audio, the workspace database, caches, credentials, host paths, or a rendered generated Skill. Transcript and caption text stays excluded unless the user has explicitly authorized redistribution; only then add `--authorize-transcript-redistribution`. Add `--edition EDITION-NAME` when exporting one named edition's downstream lineage.

An archival bundle is private and sensitive. Use `--mode archival --confirm-private-archival` only after the user deliberately accepts that boundary. It may contain raw media, audio, frames, transcripts, canonical intermediates, and a consistent evidence-database snapshot, but still excludes cookies, credentials, authentication files, caches, locks, task leases, and rendered generated Skills. Keep its mode `0600`, outside the workspace, installed Skill, and ordinary Git history. Bundle mode is independent of `--analysis-depth archival`; neither option implies the other.

## Generated Skill contract

The portable package and raw workspace must be separate trees. Every generated course Skill contains five fixed root records and at least one authored Markdown artifact. A representative evidence-justified package can contain:

```text
<course-skill>/
├── SKILL.md
├── source-map.md
├── sources.md
├── provenance.json
├── build-manifest.json
├── chapters/
│   └── <topic>.md
├── exercises/
│   └── <exercise>.md
├── solutions/
│   └── <exercise>.md
├── playbooks/
│   └── <workflow>.md
├── reference/
│   └── <decision-aid>.md
├── learning-path.md
├── glossary.md
├── patterns.md
├── cheatsheet.md
└── assets/
    └── <indispensable-image>.png
```

The five fixed root records are unconditional; the remaining entries illustrate supported artifact shapes rather than a directory quota. Use `chapters/` for independently loadable teaching units, `exercises/` for practice, `solutions/` for after-attempt answers and answer-bearing rubrics, `playbooks/` for operational application, `reference/` and the allowed root reference files for fast lookup, and `assets/` only for indispensable evidence-grounded PNGs. Generated Skill instructions must tell the runtime agent to open only the visual linked by the currently relevant artifact and never preload the asset directory. A capable source should normally produce several substantial artifacts across the behaviors it genuinely supports, while a compact source may justify fewer.

Do not manufacture symmetrical directories, split files that always load together, or omit useful material merely to keep the package small. Every included artifact needs evidence links, covered affordances, and an independent loading reason. Never include raw video, audio, complete subtitles, transcripts, databases, cookies, caches, or decorative frame collections.

### Content quality floor

Generate a reusable capability product, not a transcript summary or a collection of thin index files. Preserve named frameworks, actionable principles, demonstrated techniques, source reasoning, examples, qualifications, counterpoints, warnings, failure modes, decision rules, and material open questions when the evidence contains them.

Make every independently loaded teaching artifact useful on its own. Give it a clear user job, the necessary source-grounded explanation, a concrete example when supported, and an appropriate retrieval or transfer prompt. Do not repeat the same shallow summary across `SKILL.md`, chapters, reference files, and playbooks.

For practice capability, include focused tasks, success criteria, progressive hints, retry, and a scored rubric at the depth supported by the source. Keep answers and answer-bearing rubrics separate and `after-attempt`.

For application capability, include assumptions, decision points, operational steps, expected states, observable validation, and recovery guidance when the source supports them. Label generator-created adaptations, exercises, and conceptual workflows as inference rather than pretending the source demonstrated them.

For reference capability, prioritize compact decision rules, trade-offs, thresholds, defaults, tells, smells, and source pointers over a glossary-only surface. A glossary defines terms; a reference aid helps the user decide or act.

Strong capability claims require their full instructional-affordance surface. Medium and light claims may be smaller but must remain useful. Mark unsupported or not-applicable affordances honestly instead of lowering a capability claim to hide missing product work.

Mark generated Skills with:

```html
<!-- video-to-skill:course-skill:v2 -->
```

Keep the resident `SKILL.md` concise and operational. On empty invocation it gives a course-specific welcome of no more than two short sentences, offers `start`, loads no supporting file, inspects no project, runs no command, creates no file, and waits.

After the user begins, ask only missing course-specific context, using no more than three starter questions in one turn and at most one next-step question per later turn. Skip intake when the user already supplied enough context or asked a precise question.

During use, adapt naturally across learning, practice, application, and reference without presenting a mode menu. Teach one useful cognitive move at a time, avoid dumping whole chapters unless asked, withhold solutions until an attempt or explicit request, and load only the smallest artifact needed.

Use source-grounded material first, label generator-created exercises or adaptations as inference, distinguish outside or current knowledge, answer in the user's language, and preserve honest uncertainty.

Keep learner progress in the active conversation or host memory, never in the portable package. Keep failed and partial sources visible in `sources.md`, consequential claims traceable through `provenance.json`, and private local paths out of every shareable file.

The compiler derives the strict blueprint from canonical workspace state, reads artifact bodies by verified relative path and digest, renders outside the workspace, validates structure and behavior, and installs without overwriting different same-name content.

Keep the workspace by default. `clean` remains an explicit user action.
