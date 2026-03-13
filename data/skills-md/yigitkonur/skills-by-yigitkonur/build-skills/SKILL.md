---
name: build-skills
description: Use skill if you are creating or substantially revising a Claude skill and need workspace-first evidence, remote comparison, and repo-fit synthesis before writing SKILL.md.
---

# Build Skills

Build or revise Claude skills from evidence, not instinct.

## Trigger boundary

Use this skill when the task is about:

- creating a new Claude skill from scratch
- substantially redesigning an existing skill
- merging patterns from multiple skills or source corpora
- tightening a skill's triggers, workflow, routing, or guardrails without drifting from repo conventions

Do not use this skill for:

- tiny wording or formatting cleanups where outside evidence would not change the result
- general repo documentation work that is not about a Claude skill
- copying a remote skill into the workspace with minor renaming

## Non-negotiable rules

1. **Workspace first.** Inspect the current workspace before searching remotely or drafting anything.
2. **Research before synthesis for non-trivial work.** New skills, major redesigns, multi-source merges, thin local evidence, or explicit comparison requests require remote research.
3. **`skills.markdown` is the proof of research.** If non-trivial research happened, the artifact must exist before synthesis.
4. **Comparison before combination.** Build the comparison table before proposing the design.
5. **Original, repo-fit output only.** Distill patterns; do not rename-clone a source skill.
6. **Keep progressive disclosure clean.** Put trigger logic in frontmatter, workflow and decisions in `SKILL.md`, and bulky detail in `references/`.
7. **Test before shipping.** Run trigger tests and at least one functional test before declaring done.

## Artifact output

Intermediate artifacts (workspace scan, comparison table, success criteria) appear in conversation output as they are produced — show each one at the step that generates it. Persistent artifacts (`skills.markdown`, final SKILL.md, reference files) are written to disk in the target skill directory.

## Required workflow

### 1. Classify the job

- **Local-only path:** a small cleanup where triggers, structure, and core method stay intact. Examples: fixing typos, reordering sections, tightening one trigger phrase, updating a version number.
- **Full research path:** a new skill, substantial redesign, multi-source merge, thin or stale workspace, or an explicit request for outside comparison. Examples: adding a new workflow branch, rewriting the decision tree, changing the skill's category, merging two skills, or any change that alters what the skill does (not just how it reads).

Rule of thumb: if the change would alter the comparison table you'd build for this skill, it's the full research path.

### 2. Classify the skill type

Before designing, identify the skill's category:

| Category | Description | Key technique |
|---|---|---|
| **Document/Asset creation** | Creates consistent output (docs, code, designs) using Claude's built-in capabilities | Embedded style guides, quality checklists, templates |
| **Workflow automation** | Multi-step processes with consistent methodology | Step-by-step workflow with validation gates, iterative refinement |
| **MCP enhancement** | Workflow guidance on top of an MCP server's tool access | MCP call sequencing, domain expertise, error handling for API calls |

Read `references/patterns/workflow-patterns.md` to choose the right structural pattern.
If the skill enhances an MCP, also read `references/patterns/mcp-enhancement.md`.

### 3. Capture local evidence first

- Produce a tree-style inventory of the target workspace.
- Read the current `SKILL.md` fully — trigger boundary, workflow, decision rules, output contract, guardrails.
- Read every file in `references/` that is relevant to the task: open each file, read the contents, and note what it covers and where it has gaps.
- Note the reference file naming scheme, nesting depth, and whether routing in `SKILL.md` matches what actually exists on disk.
- Note repo conventions, existing reference coverage, and obvious gaps before widening scope.

> ⚠️ **Steering (from derailment testing):** Steps 3–4a concentrate 44% of all execution friction. Use the reference routing table to load only 3–5 relevant files per step, not all 22. See `references/steering/derailment-lessons.md` for common traps.

### 4. Run remote research when the job is non-trivial

Only execute this step if step 1 classified the job as **Full research path**. Skip to step 7 for local-only work (Steps 4–6 produce research artifacts that local-only changes don’t need).

> ⚠️ **Steering:** Downloaded skills frequently violate this skill’s own quality standards (line counts >1000, templates inline, no references). Treat quality problems as signal for your “avoid” column—see `references/research/source-verification.md`.

- Read `references/research-workflow.md` for the complete research protocol.
- Verify `skill-dl` is available: `skill-dl --version`. If missing, see `references/remote-sources.md` for installation. If unavailable and installation is not possible, use the `skills-as-context-search-skills` and `skills-as-context-get-skill-details` tools (requires the skills.sh MCP server), or search GitHub manually for repositories containing SKILL.md files.
- Use `skill-dl search` with 3–20 space-separated keywords to discover candidates: `skill-dl search mcp server typescript sdk --top 20`. It outputs a prioritized markdown table to stdout.
- Use `skill-dl` to download selected candidates, or run `bash references/skill-research.sh "keyword1,keyword2,keyword3"` for end-to-end parallel discovery and download in one command.
- See `references/remote-sources.md` for more `skill-dl` usage patterns and download options.
- Prefer a few diverse, relevant sources over many near-duplicates.
- Create `skills.markdown` in the workspace root summarizing what was downloaded, what was shortlisted, and why, before moving on.

### 4a. Read the downloaded corpus thoroughly

Do not skip from download to comparison. Reading is a distinct, mandatory step.

For each downloaded skill that made the shortlist:

- **Read its `SKILL.md` fully** — not just headings. Understand its trigger boundary, workflow structure, decision rules, and output contract.
- **Tree its `references/` directory** — see what files exist, how they are named, and how deeply they are nested. This reveals the skill's structural philosophy.
- **Read the 2–3 most relevant reference files** in full — pick based on filenames and the skill's routing logic.
- **Check `scripts/` if present** — scripts surface automation patterns and validation logic that prose cannot fully convey.
- **Capture notes per skill** (a heading per skill with bullets mapping to comparison table columns): overall structure, workflow style, reference organization, what it does well, what it does poorly, and 1–2 patterns worth inheriting (with exact relative paths).

Downloaded sources may not follow the quality standards this skill enforces (e.g., SKILL.md over 500 lines, missing reference routing). Note these issues — they inform the "avoid" column of your comparison table.

The notes you capture here are the raw material for the comparison table in step 5. If you skip reading, the comparison table will be fabricated from memory rather than evidence.

### 5. Compare before synthesizing

- Using your notes from Step 4a, build a markdown comparison table with at least: `Source`, `Focus`, `Strengths`, `Gaps`, `Relevant paths or sections`, and `Inherit / avoid`.
- Every row ends with a decision, not just an observation.

### 6. Define success criteria

Before drafting, write down what success looks like:

- **Trigger accuracy**: 90%+ of relevant queries should fire the skill; 0% of unrelated queries
- **Execution quality**: workflow completes without user correction
- **Token efficiency**: SKILL.md under 500 lines, references loaded only when needed

### 7. Synthesize the repo-fit result

- Rewrite for the current repo and task.
- Keep `SKILL.md` lean: trigger boundary, workflow, decision rules, output contract, guardrails, and reference routing.
- Reuse existing references instead of duplicating them.
- Add new files only when clearly necessary and explicitly routed.
- Read `references/authoring/description-engineering.md` to craft the description field.
- During drafting, focus on the key constraints: SKILL.md under 500 lines, every reference file routed, description follows the formula. Run the full `references/checklists/master-checklist.md` audit in Step 9.

### 8. Test the skill

- **Trigger tests:** Write 5+ should-trigger queries and 5+ should-NOT-trigger queries. For revisions, run each one by pasting it as a new message in Claude.ai (with only this skill enabled) or Claude Code, and record whether the skill loaded. For new skills, verify the description against your test queries manually; run live trigger tests after installation. See `references/authoring/testing-methodology.md` for the full testing guide.
- **Functional test:** Run at least one complete functional test of the primary workflow end-to-end.
- **Self-check:** Ask Claude "When would you use [skill-name]?" and verify the answer matches your intent.

> ⚠️ **Steering:** For a NEW skill, install the draft to `~/.claude/skills/[name]/` before testing triggers. Trigger tests fail silently if the skill isn’t loaded. For REVISIONS, test against the currently installed version.

### 9. Finish with repo-fit and cleanup checks

- Confirm directory name, frontmatter `name`, and canonical labels stay aligned.
- Confirm every file in `references/` is explicitly routed from `SKILL.md`.
- Confirm the result feels synthesized from evidence, not copied from the most detailed source.
- Confirm no `<` or `>` in frontmatter, no reserved names ("claude", "anthropic").
- If a shared repo issue blocks a clean result, report it instead of editing shared files by default.

## Decision rules

- If outside research would materially change the answer, do not stay local.
- If the local workspace already contains the needed detail, route to that file instead of rewriting it.
- If two sources conflict, prefer the pattern that is clearer, leaner, and more compatible with the target repo.
- Prefer patterns that improve agent decisions. Reject bulk that adds machinery without improving the outcome.
- If the draft starts resembling one source too closely, stop and convert the source notes into inherit/avoid decisions before rewriting.
- If the skill grows because of examples, templates, or long checklists, move that detail to references or cut it.
- If remote research is skipped, say why it was safe to skip.
- If the skill enhances an MCP, verify tool names against the MCP server documentation before shipping.
- If the description is broad enough to fire on unrelated queries, add negative triggers.

## Do this, not that

| Do this | Not that |
|---|---|
| inventory the workspace and read local source files first | start from remote search results or a remembered template |
| create `skills.markdown` for non-trivial research | claim research happened because you skimmed URLs |
| build a comparison table before drafting | mentally blend sources and jump to the final `SKILL.md` |
| route detailed guidance to existing references | stuff `SKILL.md` with tutorials, examples, or duplicated checklists |
| inherit patterns selectively with repo-fit reasoning | copy the most detailed source and rename it |
| define success criteria before drafting | ship without any trigger or functional tests |
| add negative triggers when scope is broad | let the skill fire on every tangentially related query |
| use validation scripts for deterministic checks | rely on prose like "validate properly" |
| read each downloaded skill's SKILL.md fully, tree its references/, and read the 2–3 most relevant reference files | skim titles and match counts, then fabricate a comparison from memory |
| verify tool prerequisites before using them (`skill-dl --version`) | assume tools are installed because the skill mentions them |
| show intermediate artifacts at the step that produces them | batch all output to the end or leave output location ambiguous |
| distinguish creation vs. revision paths in testing | write test instructions that only work for one path |

## Output contract

Unless the user wants a different format, show work in this order:

1. skill type classification (after Step 2)
2. workspace scan summary (after Step 3)
3. research summary with `skills.markdown` or explicit skip reason (after Step 4)
4. markdown comparison table (after Step 5, required for the full research path)
5. success criteria (after Step 6)
6. selection and synthesis strategy (after Step 7)
7. generated or revised skill artifacts (after Step 7)
8. trigger test results (after Step 8)
9. final repo-fit and cleanup checks (after Step 9)

## Reference routing

Load the smallest relevant set for the branch of work you are in.

### Authoring

| File | Read when |
|---|---|
| `references/authoring/skillmd-format.md` | Writing or validating frontmatter, body structure, or progressive-disclosure fit. |
| `references/authoring/description-engineering.md` | Crafting or improving the description field, trigger phrases, or negative triggers. |
| `references/authoring/decision-tree-patterns.md` | Designing branch logic, routing labels, or decision-tree structure. |
| `references/authoring/reference-file-structure.md` | Deciding what belongs in `SKILL.md` versus `references/`, or reorganizing reference layout. |
| `references/authoring/testing-methodology.md` | Planning or running trigger tests, functional tests, or performance comparisons. |

### Patterns

| File | Read when |
|---|---|
| `references/patterns/skill-organization.md` | Deciding whether to split, combine, or trim scope of a skill. |
| `references/patterns/naming-conventions.md` | Checking names, labels, file paths, and repo-native naming fit. |
| `references/patterns/workflow-patterns.md` | Choosing the right structural pattern (Sequential, Multi-MCP, Iterative, Context-aware, Domain). |
| `references/patterns/mcp-enhancement.md` | Designing a skill that enhances an existing MCP server integration. |

### Research

| File | Read when |
|---|---|
| `references/research-workflow.md` | Deciding whether remote research is mandatory or running the non-trivial research path. |
| `references/remote-sources.md` | Searching remote skill sources, selecting candidates, or downloading a research corpus. |
| `references/skill-research.sh` | Running end-to-end parallel discovery and download in one command. |
| `references/comparison-workflow.md` | Building the comparison table or separating evidence, comparison, selection, and generation. |
| `references/source-patterns.md` | Choosing what to inherit, simplify, or avoid from earlier skill patterns. |
| `references/research/source-verification.md` | Filtering low-signal sources, assessing trust, or justifying candidate selection. |
| `references/research/fact-checking.md` | Verifying claims, commands, or ecosystem details before they influence the new skill. |

### Quality and examples

| File | Read when |
|---|---|
| `references/checklists/master-checklist.md` | Running the full 90+ item quality checklist before shipping. |
| `references/examples/annotated-examples.md` | Studying strong structural patterns from real skills without copying them. |
| `references/examples/anti-patterns.md` | Auditing for bloat, overlap, weak triggers, copied structure, or missing tests. |

### Iteration and troubleshooting

| File | Read when |
|---|---|
| `references/iteration/feedback-signals.md` | Interpreting under/over-triggering signals or planning post-ship iteration. |
| `references/iteration/troubleshooting.md` | Diagnosing upload failures, trigger issues, MCP problems, or instruction-following issues. |

### Steering

| File | Read when |
|---|---|
| `references/steering/derailment-lessons.md` | Starting any skill build or revision, or when hitting friction during execution. Contains learned pitfalls from real testing. |

### Distribution

| File | Read when |
|---|---|
| `references/distribution/publishing.md` | Publishing, packaging, API distribution, or community-distribution concerns. |

## Guardrails and recovery

- Do not draft the final skill before reading the current workspace.
- Do not say research is complete unless `skills.markdown` exists for the non-trivial path.
- Do not hide the comparison table inside prose or skip it because sources "look similar."
- Do not copy a source skill wholesale, even as a temporary scaffold.
- Do not add files to `references/` unless they are needed and routed.
- Do not ship without running at least basic trigger tests.
- Do not use `<` or `>` in any frontmatter field.
- Do not use "claude" or "anthropic" in the skill name.

Recovery moves:

- **Local evidence is thin or contradictory:** say so, then widen the evidence set before drafting.
- **Research corpus is noisy:** cut it down to the few sources you can actually compare well.
- **Draft is bloating:** move detail to existing references or delete it.
- **Triggers are misfiring:** read `references/authoring/description-engineering.md` and fix.
- **MCP calls failing:** read `references/iteration/troubleshooting.md` for diagnosis.
- **Repo-fit conflict touches shared files:** report the shared issue instead of editing outside the target skill by default.

## Final checks

Before you finish, confirm all of the following:

- [ ] frontmatter `name` matches the directory name exactly
- [ ] `name` does not contain "claude" or "anthropic"
- [ ] description follows the formula: what + when + trigger phrases
- [ ] description is under 1024 characters with no `<` or `>`
- [ ] `SKILL.md` body is under 500 lines
- [ ] `SKILL.md` contains decisions and routing, not bulky reference content
- [ ] every reference file is explicitly routed
- [ ] routing verification: `for f in $(find references -name '*.md' -type f); do grep -q "$(basename $f)" SKILL.md || echo "ORPHAN: $f"; done`
- [ ] the final result is clearly synthesized from evidence and comparison
- [ ] no dead weight was added just because another skill had it
- [ ] at least 3 trigger tests passed (should-trigger and should-NOT-trigger)
- [ ] primary workflow completes without error in at least one test
- [ ] for full quality: ran `references/checklists/master-checklist.md`

Quick routing verification:

```bash
# Check for orphaned reference files (not mentioned in SKILL.md)
for f in $(find references -name '*.md' -type f); do grep -q "$(basename $f)" SKILL.md || echo "ORPHAN: $f"; done
```
