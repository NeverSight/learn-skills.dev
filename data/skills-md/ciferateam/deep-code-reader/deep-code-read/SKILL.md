---
name: deep-code-read
description: Use when you want to deeply understand an unfamiliar codebase and generate reusable cognitive skills from it, by providing a local path or GitHub URL
version: 1.0.0
homepage: https://github.com/CiferaTeam/deep-code-reader
---

# Deep Code Reader

Systematically read and understand a codebase, producing a set of verified cognitive skills that capture deep knowledge — module capabilities, design logic, data structures, state flow, and modification guides.

The core mechanism: evidence-checked questions, cumulative closed-book regression, and a fresh final exam test the generated knowledge. Passing establishes coverage of the tested questions for the recorded source version.

**Skill authoring:** Use the host agent's built-in skill creator or authoring guidance when available. Otherwise, create skills directly using the templates in this workflow: a `SKILL.md` with YAML `name` and `description`, a focused Markdown body, and relative links to supporting files. Apply this to both module skills and the global index. The ABC loop below validates the generated knowledge.

## Usage

```
/deep-code-read <source> <output-dir>
```

- **source**: local path (e.g., `./path/to/repo`) or GitHub URL (e.g., `https://github.com/org/repo`)
- **output-dir**: where generated skills are written (e.g., your platform's skills directory)

## Full Flow

You MUST follow these phases in order. Track progress across modules using your platform's task/todo tracking mechanism.

### Phase 1: Prepare

1. Determine the project name:
   - Local path → directory name
   - GitHub URL → repo name
2. If source is a URL:
   - Clone to `{output-dir}/{project-name}/`
   - If the directory already exists, skip cloning and use it
3. If source is a local path:
   - Verify the path exists and is a git repo
   - Use it directly (read-only — do NOT modify any files in the source repo)
4. Detect version:
   - Run `git tag --list` in the source repo
   - If tags exist, sort with semver-aware ordering (handle `v` prefix), recommend the latest
   - If no reasonable tags, recommend `main` or `master` branch
5. **PAUSE — present recommendation to user:**
   > "Detected the following tags/branches: [list]. I recommend tracking `{recommended}`. Confirm or specify a different target."
6. Checkout the confirmed ref

### Phase 2: Scan

1. Scan the source repo directory structure
2. Identify module boundaries using heuristics:
   - Top-level directories under `src/`, `lib/`, `pkg/`, `packages/`, or project root
   - Language-specific patterns: Python packages (`__init__.py`), Go packages, Node packages (`package.json`), etc.
   - Look for existing module documentation or manifest files
3. Analyze import/dependency relationships between modules
4. **PAUSE — present module list and dependency graph to user:**
   > "Found the following modules: [list with one-line descriptions]. Select which modules to deep-read (or 'all')."
5. Record the user's selection — one task per selected module

### Phase 3: Deep Read (Agent A)

Record the confirmed source commit with `git rev-parse HEAD` as `{source-sha}`. Read source content from that commit (for example, `git ls-tree -r --name-only <sha>` and `git show <sha>:<path>`), including evidence checked during verification. For each selected module, dispatch a subagent with the prompt template from `agent-a-prompt.md`.

**Subagent dispatch parameters:**
- `prompt`: rendered `agent-a-prompt.md` with variables filled in
- `description`: "Deep read {module-name}"

**Variables to fill in the prompt:**
- `{source-dir}`: path to the source repo
- `{module-dir}`: path to the specific module within the source repo
- `{output-dir}`: the skill output directory
- `{project-name}`: extracted project name
- `{module-name}`: the module name
- `{ref}`: the tracked tag/branch
- `{source-sha}`: the recorded source commit, also used for verification

After Agent A completes, verify the skill files were written to `{output-dir}/{project-name}-dr-{module-name}/`. Update the module's task status.

### Phase 4: Verify (ABC Loop)

For each module, run at most **3 repair rounds**, including the initial candidate. A round tests the complete regression bank and, if that passes, a fresh final exam against the same frozen candidate.

**Setup — evidence and isolation:**

- Record the source commit SHA used by A and B. If the source changes during verification, stop and regenerate against a consistent version.
- Keep a per-module verification record outside all generated skill directories, under `{output-dir}/.deep-code-read/{project-name}/{run-id}/{module-name}/`, with a unique run ID. Save question IDs, validated keys and source evidence, rejected questions and reasons, C's answers, grading decisions, round numbers, and candidate file hashes. Keep answer keys out of published skills.
- Start B and C in fresh contexts without inherited conversation, source excerpts, answer keys, or earlier answers. B receives source access; C receives only the candidate skill files and question-only input. Record isolation as `enforced` (scoped read access), `observed` (complete tool/read logs checked for allowed inputs), or `prompt_only` (instructions without independently checkable access). Treat any observed out-of-scope read as contamination. For either agent, accept a blocker response shaped as `{"status":"blocked","reason":"context_contamination|source_unavailable","detail":"..."}` instead of its normal output. Retry contamination once in a fresh context, then stop as blocked if it recurs. Source-unavailable blockers stop verification for that module; blocker responses are never graded or treated as malformed answers.
- Freeze the candidate during each round: record hashes of every skill/supporting file and check them after both exams. Any edit invalidates that round's results; test the changed candidate in the next round.

**Step 1 — Build and validate the regression bank:**

Dispatch `agent-b-prompt.md` using a model capable of accurately tracing the module's code; choose cost based on demonstrated accuracy.

Fill these variables:
- `{source-dir}`, `{module-dir}`, `{module-name}`, `{source-sha}`
- `{mode}`: `regression`
- `{previous_questions}`: JSON objects containing only `id` and `question` for all prior questions; `[]` in the first round

B returns `verification` and `recommended` arrays. The coordinator assigns stable IDs to new questions and retains the recommended questions for Phase 6. B supplies 5–8 initial questions or 3–5 additions in later rounds. **The coordinator retains every previously validated question, including previously passing and failed final-exam questions. B's new output extends this bank; it never replaces it.**

Before admitting a question, the coordinator reads the cited source ranges, relevant conditions/call sites, and checks every required fact and the answer key against `{source-sha}`. Resolve semantic ambiguities and inferred design intent before grading. Correct an erroneous key only from source evidence and record the correction. Reject invalid questions with reasons and request valid replacements to meet the round's count; permit one replacement request, then stop as blocked if the question set remains invalid. Never turn an invalid question into a skill failure or silently remove a previously failed question to obtain a pass. Replacements receive new IDs; retain the rejected IDs and reasons. Any key or question correction invalidates its prior grade; have C answer changed questions afresh before deciding the exam result.

**Step 2 — C answers the complete bank:**

Dispatch `agent-c-prompt.md` in a fresh context with:
- `{skill-dir}`: `{output-dir}/{project-name}-dr-{module-name}/`
- `{module-name}`
- `{questions}`: a JSON array projected to **exactly `id` and `question`** from the entire validated regression bank

Keep `answer_key`, `required_facts`, source evidence, grading notes, and prior answers private to the coordinator. C must return exactly one answer per supplied ID. Missing, duplicate, or unknown IDs are an invalid response, not a pass; allow one format retry in a fresh context, then stop as blocked if still malformed.

**Step 3 — Grade against checked evidence:**

The coordinator compares each answer with the validated required facts and verifies C's skill citations. Semantic grading is a reasoned judgment: record which facts are covered, missing, or contradicted and why.

- **PASS:** all required facts are supported by the candidate, with no materially incorrect or contradictory claims in the answer.
- **FAIL:** a required fact is missing, the answer contradicts the source, adds a materially false claim, lacks supporting skill evidence, or is `CANNOT_ANSWER`. Correct keywords alone do not establish a pass.
- **DISPUTED:** the question or key is ambiguous or lacks adequate source support. Resolve it from source evidence before scoring; apply the bounded correction/replacement procedure in Step 1. An unresolved dispute blocks verification.

Report `passed / all valid questions` separately for regression and final exams. An empty exam cannot pass. Invalid, replaced, and disputed questions remain visible in the record.

**Step 4 — Frozen-candidate final exam:**

Only after the complete regression bank passes, keep the same candidate frozen and dispatch a **new B** with `{mode}` = `holdout`. Provide source scope, source SHA, and prior question IDs/text only for avoiding overlap. Keep candidate skills, earlier keys, answers, scores, and repair feedback out of B's context.

B generates 5–8 new questions about useful reference knowledge: mechanisms, limits, failure conditions, and when a pattern or API applies. Rephrasing an existing question or testing the same required fact with new wording does not count as a new case. The coordinator validates the keys and checks overlap before a fresh C answers this exam, using Steps 1–3. Keep the final questions and keys away from A until grading is complete.

- **All regression and final questions pass, candidate hashes unchanged:** mark the module `verified` for that candidate and source SHA when isolation is `enforced` or `observed`; with `prompt_only` isolation, mark `partial_validated` and report that closed-book isolation could not be independently checked. Record both scores and the tested topics; this is sampled knowledge verification, not proof of exhaustive coverage.
- **Any valid question fails in either exam:** mark the candidate unverified. Append the entire validated final exam to the regression bank if one was attempted. If the current round is below 3, give A the failed questions, checked source evidence/keys, and C's answers to repair the skills. In the next round, rerun the complete bank and use a new final exam after regression passes. At round 3, transition directly to `needs_review` without dispatching another repair.
- **Candidate edits before round 3:** discard that round's grades and continue with the changed candidate in the next round, retaining every validated question from the discarded exams as regression material.
- **Failures or candidate edits at round 3:** mark `needs_review`, present the outstanding gaps and scores, and stop. Never reuse a final exam exposed to A as independent acceptance evidence or start another three-round cycle automatically.

### Phase 5: Generate Global Index

For `blocked`, `needs_review`, or `partial_validated` modules, present their status and evidence to the user and stop before claiming completion. After all selected modules are verified, generate `{output-dir}/{project-name}-dr/SKILL.md`:

```yaml
---
name: {project-name}-dr
description: Use when working with {project-name} codebase — provides comprehensive module knowledge, design logic, and modification guides (generated from {ref})
---
```

Content must include:
- Repo source (GitHub URL if applicable, or local path)
- Version: tag or commit hash
- Tracked branch
- Generation timestamp
- Each module's verified source SHA, candidate hashes, isolation level, regression/final scores, and tested topics from Phase 4; label cross-module scenarios synthesized here as unverified by the module exams
- Each module's one-line purpose (from the module skills)
- Inter-module dependency relationships (from Phase 2 scan)
- Cross-module scenario entry guides: for common operations that span multiple modules, describe which modules are involved and in what order

To generate cross-module scenarios, read ALL the module skills and synthesize typical user workflows.

### Phase 6: User Acceptance

Present the recommended questions collected from Phase 4:

> "Skills generated and verified. Here are some questions you might want to test:
> [list recommended questions]
>
> Feel free to ask any question about {project-name}. I'll answer using ONLY the generated skills."

When answering user questions in this phase:
- Read ONLY the generated skill files in `{output-dir}/{project-name}-dr*/`
- Do NOT read source code
- If you cannot answer a question from the skills alone, say so honestly — this indicates a gap

Continue until the user is satisfied or decides to end the session.

### Phase 7: Cleanup

If the source was cloned from a URL (i.e., `{output-dir}/{project-name}/` was created in Phase 1):

> "Skills are ready. The cloned source code is at `{output-dir}/{project-name}/`. Want me to delete it to save disk space, or keep it for reference?"

- User says delete → remove the cloned directory
- User says keep → leave it as is

Skip this phase if the source was a local path (we never cloned anything).

## Key Rules

- **Never modify source code** — the source repo is read-only throughout
- **Agent isolation is critical** — B and C use fresh contexts with the scoped inputs defined in Phase 4
- **Skills must be self-sufficient** — answers must be supported by the generated documents; report tested coverage and unresolved gaps
- **Track progress** — every module is a task, updated as it progresses through phases
- **Skill formatting** — follow available native authoring guidance or the included templates; check frontmatter and supporting-file links before verification
