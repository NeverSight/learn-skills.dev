---
name: accelint-onboard-agents
description: Onboard a repository to agent-driven development by creating or refreshing a complete AGENTS.md or CLAUDE.md through behavior-focused discovery, structured interviewing, drift-aware updates, conflict-aware synthesis, proportional updates, and preview-before-write review. Use when the user wants to create, replace, refresh, import, restructure, append to, dry-run, or review AGENTS.md or CLAUDE.md guidance, mentions agent behavior, instructions, guardrails, workflow, Claude Code conventions, package-level agent files, or monorepo inheritance, or asks how to tell an AI coding agent how to behave in a project. Also use it when the user wants behavior rules kept separate from `openspec/config.yml` or `openspec/config.yaml` project DNA. Do not use it for OpenSpec config onboarding, architecture docs, or one-line AGENTS.md or CLAUDE.md edits that do not require discovery, synthesis, or section-level review.
license: Apache-2.0
metadata:
  author: accelint
  version: "1.7.0"
---

# Onboard Agents

Guide the user through a conversational interview that produces a complete, project-specific `AGENTS.md` or `CLAUDE.md` for how an AI coding agent should behave in this repository.

## Separation of Concerns

This skill produces the **behavior layer** of the agent instruction stack.

Keep content here only when it directly improves recurring agent behavior. If a detail is better described as project background, stack fact, architecture explanation, process handbook material, or nearby reference documentation, use a canonical companion document and link to it instead of restating it here. These layers must not duplicate each other.

Canonical companion documents may include `openspec/config.yml` or `openspec/config.yaml` for project DNA, `ARCHITECTURE.md` for system structure, `CONSTRAINTS.md` for externally imposed boundaries, `EPISTEMIC-MAP.md` for validated facts vs open questions and assumptions, and `JARGON.md` for internal terminology.

Use the rule below to decide what stays in this file and what belongs in a canonical companion document.

### Hard Rule: What Does NOT Belong Here

If material does not answer "how should the agent behave?", it does not belong in `AGENTS.md` or `CLAUDE.md`.

Move that material to the appropriate canonical companion document when one exists, or leave it out.

| Belongs in AGENTS.md | Belongs in a canonical companion document |
|---|---|
| "Always run `pnpm check` before committing" | "Package manager: pnpm" |
| "Use Conventional Commits" | "TypeScript 5.x, strict mode" |
| "Ask before deleting files" | "Monorepo: Turborepo + PNPM" |
| "Prefer small, focused PRs" | "`type` over `interface`" |
| "Work as a senior TS engineer when useful" | "Domain: geospatial visualization" |
| "Never force-push to main" | "Testing: Vitest + @testing-library" |
| "Read `ARCHITECTURE.md` before changing deployment-related code" | "Service topology and deployment model" |
| "Check `CONSTRAINTS.md` before changing compliance-sensitive flows" | "The actual compliance or stakeholder constraint itself" |

### Final Inclusion Rule

Only include guidance in the final `AGENTS.md` or `CLAUDE.md` when it earns a permanent place. A detail earns that place only when it:

- changes how the agent should behave
- applies to recurring work, not a one-off task
- prevents the agent from making a repository-specific mistake or unsupported assumption
- is durable enough for standing guidance
- is valuable enough to load in every agent session

Do not include a detail just because the agent might not know it already. Include it only when it describes a repository-specific rule or exception that affects how the agent should work. Otherwise, leave it out or link to the canonical document that contains it.

Persona or identity framing is optional. Use it only when it improves behavior. Do not let role language replace operational guidance.

---

## NEVER Do When Onboarding Agents

- **NEVER run codebase discovery serially** — when discovery is needed, use parallel subagents for different behavioral domains. Serial scanning wastes time on codebases with many config files spread across directories.
- **NEVER skip needed discovery before asking questions** — infer behavioral conventions from the codebase before adding avoidable questions to the interview. A question about commit format when `commitlint.config.ts` exists wastes the user's time. For narrow refreshes, do only the scoped discovery the request needs.
- **NEVER omit required template sections from the generated AGENTS.md** — if a required section from `./assets/template.md` cannot be inferred or answered, keep that section and mark unresolved fields with `<!-- TODO: fill in -->` rather than leaving the section out. Omit optional sections only when `./assets/template.md` explicitly allows it. Missing required template sections silently shape agent behavior in unpredictable ways.
- **NEVER duplicate root-level instructions in package-level files** — if a monorepo root `AGENTS.md` or `CLAUDE.md` exists, package files should reference it and add only what is package-specific. Repeated instructions inflate context on every agent invocation.
- **NEVER preserve conflicting standing rules only because both were found** — resolve conflicts using source precedence, or surface the unresolved issue in preview instead of emitting both as authoritative guidance.
- **NEVER write the final file without showing a preview** — the user must see inferred values with source annotations and confirm before any filesystem write.

---

## Conflict Resolution and Source Precedence

When candidate rules conflict during import, refresh, or final synthesis, resolve them in this order:

1. **Direct user-confirmed answers**
2. **Confirmed repository policy or explicitly documented repository behavior**
3. **Evidence-backed inference from repository materials**
4. **Existing `AGENTS.md` or `CLAUDE.md` content that remains consistent with stronger evidence**
5. **Template defaults or generic skill defaults**
6. **`<!-- TODO: fill in -->` or an explicit open question instead of forced synthesis when conflict remains unresolved**

Apply this rule every time:

- Do not preserve conflicting rules because both were discovered.
- Do not let defaults outrank stronger repository evidence.
- Do not let old file content survive unchanged if it conflicts with current confirmed evidence.
- When uncertainty remains, surface it in preview or use a TODO instead of inventing a unified rule.

---

## Workflow at a Glance

Follow this workflow in order. Do not skip ahead. Complete each gate before moving to the next step.

### Step 0: Start progress tracking

Do this before any other workflow step.

Create a progress checklist with your task-tracking tool. If no tool is available, copy the checklist below into your working state or reply. Update it after each completed step or branch handoff.

- [ ] Step 1: Check for a monorepo root instruction file
- [ ] Step 2: Check for related documents
- [ ] Step 3: Detect the local file state
- [ ] Step 4: Confirm how to use the existing file when Mode 2 or Mode 3 was detected
- [ ] Step 5: Choose the branch inside Mode 2 or Mode 3 when needed
- [ ] Step 6: Run the selected mode playbook
- [ ] Step 7: Fill remaining behavioral gaps with parallel discovery if needed
- [ ] Step 8: Run the final editorial pass
- [ ] Step 9: Show the full labeled preview and collect review feedback
- [ ] Step 10: Write the confirmed file when this path writes output
- [ ] Step 11: Run the post-write quality check when a file was written
- [ ] Step 12: Print the completion summary

Important sequencing rule:
- **Step 1**, **Step 2**, and **Step 3** determine the local file state and detect the mode.
- **Step 4** and **Step 5** confirm the user's intent and choose the branch inside that detected mode.
- **Step 6** executes exactly one mode playbook.
- **Step 7** runs only if required template fields still have unresolved behavioral gaps.
- **Step 8** through **Step 12** finish the preview, write, and review flow.

If a narrower branch explicitly tells you to skip a later step, follow that branch. Otherwise, keep this order.

---

## Stage 1 — Detect the Starting State

Complete Stage 1 before you ask any interview question or enter any mode-specific path.

- Do not silently pick a mode.
- Always tell the user which mode you detected.
- Confirm before you continue.

### Step 1: Check for a monorepo root instruction file

Before you assess the local file, determine whether the current working directory is a package inside a monorepo.

If a root-level `AGENTS.md` or `CLAUDE.md` exists above the current directory:

1. Read the root file in full.
2. Announce: *"I found a root-level `AGENTS.md` or `CLAUDE.md` at [path]. I'll use it as context to avoid duplicating instructions that apply to all packages. The file I generate here will reference the root where appropriate rather than repeating it."*
3. In the generated file, add a header reference:
   ```markdown
   <!-- Inherits from: [relative path to root AGENTS.md or CLAUDE.md] -->
   <!-- Only package-specific overrides and additions are defined here. -->
   ```
4. During the interview, at the start of each turn, state what the root file already covers for that section before asking any questions:

   > "The root `AGENTS.md` or `CLAUDE.md` defines [summary of this section's content].

   Emit a reference in the generated file rather than repeating the content. If the user flags additions or overrides, ask the normal turn questions scoped to what is missing or different.

### Step 2: Check for related documents

After Step 1 and before local file-state detection, check for canonical companion documents that either:

- help enforce the behavior-layer boundary, or
- belong in the final `## Related Documentation` section.

Check these companion documents in order:

1. Check for `openspec/config.yml` or `openspec/config.yaml`.
   - If either file exists, read it to understand the project's stack and patterns.
   - Note its existence for the `## Related Documentation` section.
   - Announce: "Found `openspec/config.yml` or `openspec/config.yaml` — I'll use it to maintain the behavior/project-DNA boundary."
2. Check for `ARCHITECTURE.md`.
   - If it exists, read it to understand the system structure.
   - Note its existence for the `## Related Documentation` section.
   - Announce: "Found `ARCHITECTURE.md` — I'll use it when behavior guidance depends on system structure."
3. Check for other canonical companion documents, especially `CONSTRAINTS.md`, `EPISTEMIC-MAP.md`, and `JARGON.md`.
   - If one exists, read it only when the document is likely to materially affect behavior guidance, approval boundaries, or agent-facing terminology.
   - Note any that exist for the final `## Related Documentation` section.

Apply these limits during this check:

- Do not turn this step into a broad handbook scan.
- Detect canonical companion documents. Do not absorb their full contents into `AGENTS.md`.
- Read only what is needed to keep the behavior file accurate, scoped, and well-linked.

### Step 3: Detect the local file state

Requires: Steps 1 and 2 are complete.

Detect the local `AGENTS.md` or `CLAUDE.md` state.

Run this check in order:

1. Check whether a local `AGENTS.md` or `CLAUDE.md` exists in the current directory.
2. If neither file exists, select **Mode 1: Create**.
3. If a local file exists, read it before classifying the mode.
4. After you read the file, classify it exactly once:
   - If it is empty or near-blank, meaning fewer than about 10 meaningful lines, select **Mode 1: Create** with overwrite confirmation.
     Ask: *"AGENTS.md exists but appears empty — should I populate it from scratch, or preserve any current content?"*
   - If it contains the canonical template shape from `./assets/template.md`, meaning two or more canonical section headings in recognizably template-based form, select **Mode 3: Refresh**.
   - If it contains real content in an unrecognized shape, select **Mode 2: Import**.

Treat `./assets/template.md` as the canonical structure reference for recognition, refresh, and audit behavior. Use section headings exactly as defined there, preserve the template's canonical order for all required sections, and keep optional headings such as `## Optional review-specific rules` and `## Maintenance guidance` only when the template allows them.

Use the diagram below as a quick classification aid. The ordered list above is authoritative.

```text
Local `AGENTS.md` or `CLAUDE.md` in current directory?
│
├── No
│   └── MODE 1: Create
│       Full interview from scratch.
│
└── Yes
    ├── Read the file first
    └── Then classify:
        ├── Empty or near-blank (< about 10 meaningful lines)
        │   └── MODE 1: Create
        │       Ask: "AGENTS.md exists but appears empty — should I populate it from scratch, or preserve any current content?"
        ├── Canonical template shape from `./assets/template.md`
        │   └── MODE 3: Refresh
        │       Two or more canonical section headings in recognizably template-based form.
        └── Real content in an unrecognized shape
            └── MODE 2: Import
```

Done when: the file state and detected mode are explicit.

---

## Stage 2 — Confirm the Operating Path

Complete Stage 2 before you start discovery, drift scanning, or any mode-specific interview.

### Step 4: Confirm how to use the existing file

Requires: Step 3 is complete.

If Step 3 detected **Mode 2**, ask this first:

> "Before I start, this file has content that does not follow the canonical template.
> Would you like to **start fresh**, treating the existing file as a reference only
> *(recommended for an import)*, or **work with the existing file**?"

If Step 3 detected **Mode 3**, ask this first:

> "Before I start, this file already follows the canonical template.
> Would you like to **work with the existing file** *(recommended for a refresh)*,
> or **start fresh**, treating it as a reference only?"

If the user chooses **start fresh**, switch immediately to **Mode 1: Create**.

- Treat the existing file as a read-only reference.
- Carry forward any content from the existing file that is still accurate.
- Do not silently discard it.
- Use the template to control the new file’s top-level structure, not to decide whether existing guidance may remain.
- If existing guidance passes the Final Inclusion Rule but has no dedicated template heading, place it in the canonical section that governs that behavior.
- Do not add a top-level section or discard the guidance only because the template does not name it.
- Regenerate the structure from scratch.
- Then go to **Step 6a**.

If the user chooses **work with the existing file**:
- if Step 3 detected **Mode 2**, go to **Step 5a**
- if Step 3 detected **Mode 3**, go to **Step 5b**

If Step 3 already selected **Mode 1**, skip Step 4 and Step 5. Go directly to **Step 6a**.

Done when: the choice between **start fresh** and **work with the existing file** is explicit whenever Mode 2 or Mode 3 was detected.

### Step 5a: Choose the Mode 2 branch

Requires: Step 4 routed here from **Mode 2**.

Present these three options before you modify or synthesize anything:

> "This AGENTS.md has existing content with a structure I don't recognize.
> How would you like to proceed?
>
> **(a) Restructure** — I'll import your existing content, map it onto this
> skill's template sections, flag any material that belongs in a canonical
> companion document instead, run a targeted interview to fill gaps,
> and produce a merged file ready to replace the current one.
>
> **(b) Append** — I'll run the full interview and append a template-aligned
> `AGENTS.md` block below your existing content without modifying what's already there.
>
> **(c) Dry run** — I'll run the full interview and show you exactly what I
> would have generated, with no changes to the filesystem. Use this to
> evaluate fit before committing."

Branch routing:
- If the user chooses **(a)**, go to **Step 6b**.
- If the user chooses **(b)**, go to **Step 6c**.
- If the user chooses **(c)**, go to **Step 6d**.
- Do not start any branch until the user has chosen one.

Done when: the Mode 2 branch is explicit.

### Step 5b: Choose the Mode 3 refresh path

Requires: Step 4 routed here from **Mode 3**.

Only after the Mode 3 intent gate is satisfied, choose exactly one refresh path:

- **Targeted refresh** — use this when the request is already within this skill's boundary and is clearly bounded, such as:
  - one known contradiction to fix
  - one section to update from newly confirmed evidence
  - one outdated rule to remove or soften
  - one narrow addition that belongs in an existing section
  - one wrapper or conversion update where the surrounding structure is unchanged
- **Full refresh** — use this when the request is broad, the file may have drifted in several places, or the narrow update reveals a contradiction, cross-section dependency, or inconsistency that requires broader review.

Branch routing:
- If the request qualifies for targeted refresh, go to **Step 6e**.
- Otherwise, go to **Step 6f**.

Done when: the Mode 3 refresh path is explicit before refresh analysis begins.

---

## Stage 3 — Run the Selected Mode Playbook

Run exactly one Step 6 branch.

### Shared interview block for interview-based paths

Use the interview only after Stages 1 and 2 are complete. Run it conversationally. Do not dump all questions at once. Group questions into natural topic turns that map directly to the canonical template in `./assets/template.md`. That template is the source of truth for section names, section order, required-versus-optional sections, placeholder handling, and default scaffolding. If the user describes a workflow, infer related behavioral constraints and confirm them instead of asking again. Keep questions proportional to the request size. Do not ask for information that strong repository evidence already answers.

Ask only for material that belongs in the template. Do not invent extra AGENTS.md sections to hold answers the template does not define. If a topic is optional in the template, confirm whether it should be kept, adapted, or omitted based on what `./assets/template.md` allows. When consolidating answers across turns, map them back into the exact canonical sections defined in `./assets/template.md`.

**Turn 1 — What to optimize for**
- What durable priorities should the agent optimize for in this repository?
  *(Examples: follow repo workflows instead of guessing, prefer small scoped changes, make work traceable, stay aligned with existing patterns.)*
- Are there repository-specific priorities that materially affect agent behavior?
- Should the agent emphasize simplicity, speed, safety, reviewability, or some other standing priority?

**Turn 2 — How to communicate**
- How should the agent communicate? 
   *(Examples: concise, expository, conversational, adaptive)*
- Should the agent explain its reasoning, or just act?
- When making changes, are there required reporting expectations beyond what the template already says?
   *(Examples: show diffs, show full files, inline comments, separate explanation block?)*
- How should the agent handle missing information or uncertainty? 
   *(Examples: state assumptions and proceed narrowly, always aske bfore proceeding, ask for scope-changing uncertainty only?)*

**Turn 3 — How to work**
- Before making changes, what must the agent read, confirm, or state first?
- While making changes, are there standing workflow expectations beyond the template defaults?
- Before completing a task, what verification, scope checks, or safety checks must always happen?
- If the repo uses OpenSpec or another spec-driven workflow, capture the behavior here only as durable agent workflow guidance, and link to canonical docs for deeper process details.

**Turn 4 — Repository-specific commands and entry points**
- What commands should the agent prefer for setup, build, test, lint/format, and task running?
- Are there path conventions, package-manager rules, or command invocation patterns that are easy to get wrong?
- Are there any commands the agent should avoid in favor of specific repo entry points?

**Turn 5 — Decision Heuristics**
- When should the agent ask vs. proceed autonomously?
  *Good prompts: "deleting files", "changing public APIs", "modifying migrations", "adding new dependencies".*
- If scope grows mid-task, what is the default action?
- If evidence is incomplete or multiple implementations are valid, should the agent choose, ask, or present tradeoffs?

**Turn 6 — Approval and safety boundaries**
- What actions require approval before proceeding because they are risky, costly, hard to reverse, or affect shared systems?
- What hard safety boundaries must always be preserved?
  *Examples: never commit secrets, ask before schema or migration changes, do not act on production without approval.*
- Are there sandboxing, remote-environment, publishing, or externally relied-on information boundaries that should be documented here?

**Turn 7 — Quality bar for finished work**
- What checks are required before work is considered done?
- What evidence should the agent report back?
- Are there review or handoff expectations specific to this repo?

**Turn 8 — Optional review-specific rules, related documentation, and maintenance guidance**
- Does this repository use `AGENTS.md` to guide code review behavior strongly enough to keep `## Optional review-specific rules`, or should that optional section be omitted?
- Which canonical documents should appear in `## Related Documentation`, if they actually exist?
- Is there repository-specific maintenance guidance to add under `## Maintenance guidance`, or should the template defaults stand as written?

### Shared smart-defaults block for interview-based paths

Use Smart Defaults only to reduce avoidable interview load after you have already checked for stronger evidence.

A Smart Default is a confirmation prompt, not standing policy. Use one only when:

- the relevant template field still needs an answer
- direct user input does not already answer it
- repository evidence does not already answer it
- the default helps the user confirm a likely convention faster than asking from scratch

Do not use Smart Defaults to introduce new policy, broaden scope, or carry ecosystem assumptions into the generated file.

Apply these rules:

1. **Stronger evidence wins first.**
   If direct user input, repository evidence, the canonical template, or still-consistent existing guidance already answers the field, do not offer a default for that field.
2. **Offer defaults as prompts, not conclusions.**
   Phrase the default as something to confirm, reject, or refine. Do not present it as adopted policy.
3. **Keep the default proportional to the evidence.**
   Prefer narrow prompts that test one likely convention at a time. Do not turn one repository signal into a broad workflow bundle.
4. **Keep examples illustrative.**
   The example prompts below show common patterns. They are not an exhaustive checklist and they are not required in every run.
5. **Do not preserve a default after the user or repository disproves it.**
   Replace it with the stronger answer, or leave `<!-- TODO: fill in -->` if the field still cannot be confirmed.

#### Example prompt patterns

Use patterns like these only when they match the repository evidence already gathered.

**If the repo appears to use a PNPM monorepo:**
- "I found signs of a PNPM workspace. Should I treat workspace-root and package-scoped dependency changes differently in the generated guidance?"
- "Do you want the agent to prefer workspace-aware task commands when package selection matters?"

**If the repo appears to use GitHub Actions for CI:**
- "I found GitHub Actions workflows. Should the generated guidance require the agent to report or wait on specific CI checks before considering work complete?"
- "Are there required status checks or PR gates that should appear in the file?"

**If the repo appears to use Conventional Commits:**
- "I found commit-convention signals. Should the file tell the agent to use Conventional Commits, and are there repo-specific types or breaking-change rules to note?"
- "Are scope usage or footer conventions important enough to make explicit?"

**If the repo appears to use OpenSpec or another spec-driven workflow:**
- "I found signs of a spec-driven workflow. Which parts of that workflow are durable agent behavior that belong in `AGENTS.md`, and which parts should stay in canonical project documentation?"
- "For non-trivial changes, should the agent start with the documented spec workflow before implementation?"

Done when: likely conventions are confirmed, rejected, or replaced with stronger evidence, and no unconfirmed default has been carried into standing guidance.

### Step 6a: Run Mode 1 — Create

Use this branch for a fresh repo, an empty or near-blank file that the user wants populated, or an explicit **start fresh** choice.

Run this branch in order:

1. Run the **Shared interview block for interview-based paths**.
2. Run the **Shared smart-defaults block for interview-based paths**.
3. If unresolved required template fields remain, go to **Step 7**.
4. Otherwise, go to **Step 8**.

Done when: the interview answers and any confirmed smart defaults are ready for gap-filling discovery or the draft is ready for the final editorial pass.

### Step 6b: Run Mode 2 — Restructure

Use this branch only when the file has real content that this skill did not generate and the user chose **(a) Restructure**.

Run this branch in order:

1. Read the file in full.
2. Map each existing section onto the canonical template sections from `./assets/template.md`.
3. Preserve the template's section order and only keep optional sections that the template explicitly allows, such as `## Optional review-specific rules`.
4. Flag any content that violates the separation-of-concerns boundary, such as stack facts, tech versions, domain descriptions, constraints, assumptions, or internal terminology. Move that material to the appropriate canonical companion document.
   - For each violation, ask: *"This describes [X] — that belongs in a canonical companion document rather than `AGENTS.md` or `CLAUDE.md`. Should I move it to the appropriate document and leave a reference here?"*
5. Run the **Shared interview block for interview-based paths** only for uncovered gaps, meaning canonical template sections or required template fields from `./assets/template.md` with no existing coverage.
6. Apply the source-precedence rule and remove duplicate, conflicting, or adjacent-doc material before preview.
7. If required template fields still lack answers after Step 6, go to **Step 7**.
8. Otherwise, go to **Step 8**.
9. In **Step 9**, show a merged preview before writing. Carried-forward content is labelled `# from existing file`; new content is labelled `# new`.

Done when: the merged draft is ready for the final editorial pass or any remaining gaps have been routed to Step 7.

### Step 6c: Run Mode 2 — Append

Use this branch only when the file has real content that this skill did not generate and the user chose **(b) Append**.

Run this branch in order:

1. Run the **Shared interview block for interview-based paths**.
2. Run the **Shared smart-defaults block for interview-based paths**.
3. If unresolved required template fields remain, go to **Step 7**.
4. Otherwise, go to **Step 8**.
5. In **Step 10**, append the generated template-aligned block below a `---` divider and a comment: `<!-- Added by accelint-onboard-agents skill -->`.

Even in append mode, do not add conflicting standing guidance without surfacing the conflict in preview.

Done when: the appended draft is ready for the final editorial pass or any remaining gaps have been routed to Step 7.

### Step 6d: Run Mode 2 — Dry run

Use this branch only when the file has real content that this skill did not generate and the user chose **(c) Dry run**.

Run this branch in order:

1. Run the **Shared interview block for interview-based paths**.
2. Run the **Shared smart-defaults block for interview-based paths**.
3. If unresolved required template fields remain, go to **Step 7**.
4. Otherwise, go to **Step 8**.
5. In **Step 9**, stop after the labeled preview.
6. Present the output in the conversation and explicitly state: "No files were changed."
7. Offer to re-run as **(a) Restructure** or **(b) Append** if the user is satisfied.
8. Skip **Step 10** and **Step 11**. Go directly to **Step 12** after Step 9.

Done when: the dry-run draft is ready for the final editorial pass or any remaining gaps have been routed to Step 7.

### Step 6e: Run Mode 3 — Targeted refresh

Use this branch only when the file matches the skill's expected shape, the user chose to work with the existing file, and the request is one bounded update with a known target section or issue.

Run this branch in order:

1. Inspect the affected section or sections first.
2. Do only the scoped discovery needed for that bounded update.
3. Ask only the questions needed to resolve that update.
4. Avoid the full interview and full regeneration unless missing context requires it.
5. Preserve the rest of the file unless the narrow update exposes broader contradiction or drift.
6. Apply source precedence and the final editorial pass to the affected material and any directly dependent sections.
7. If the update reveals broader contradiction or drift, go to **Step 6f** before continuing.
8. If the bounded update still leaves unresolved required template fields, go to **Step 7**.
9. Otherwise, go to **Step 8**.

Done when: the targeted-refresh draft is ready for the final editorial pass, the work has been escalated to Step 6f, or any remaining required gaps have been routed to Step 7.

### Step 6f: Run Mode 3 — Full refresh

Use this branch only when the file matches the skill's expected shape, the user chose to work with the existing file, and targeted refresh is not sufficient.

Run this branch in order:

1. **Extract external findings.**
   - Check whether the invoking prompt includes a `findings:` list.
   - Parse the prompt for a `findings:` section, meaning a bulleted list of factual statements.
   - Each finding is phrased as something already known to be true, never as an instruction.
   - Example: "config.yaml's Anti-Patterns section says to avoid polling, but two archived changes chose polling for stated reasons"
   - Store these findings for later merging.
2. **Run drift detection.**
   Scan the codebase for changes since the file was last updated.

   Use the signals below as common examples, not as an exhaustive list.

   | Signal | Where to look |
   |---|---|
   | New packages added | `package.json`, workspace `package.json` files |
   | CI checks changed | `.github/workflows/` — new required gates? |
   | Husky hooks modified | `.husky/` — new pre-commit steps? |
   | New migration directory | `migrations/`, `prisma/migrations/`, `alembic/` |
   | Versioning tooling added | `.changeset/`, `.releaserc*` |
   | OpenSpec added or removed | `openspec/` directory presence |
   | New protected branches | `.github/branch-protection*`, README |
3. **Surface unresolved TODOs.**
   Find all `<!-- TODO: fill in -->` markers left from the previous run and surface them as targeted questions.
4. **Merge and announce findings before asking anything.**
   Combine the external findings from Step 6f.1, the drift findings from Step 6f.2, and the TODOs from Step 6f.3.

   Present the merged list to the user:

   > "I found [N] external findings, [M] sections that may have drifted, and [P] unresolved TODOs.
   > I'll only ask about those — the rest looks current."

   If external findings exist, note their source, for example "from completed OpenSpec change".
5. **Run the refresh interview, then preview the changed sections first.**
   Only after Step 6f.4 is complete:
   - run the targeted refresh interview for the merged finding set
   - apply source precedence
   - prune duplication and low-value carry-forward text
   - show a diff-style preview that includes only changed sections first
   - do not re-emit unchanged sections in that first refresh preview
   - still produce the full labeled preview required by Step 9 before any write
6. If the refresh still leaves unresolved required template fields, go to **Step 7**.
7. Otherwise, go to **Step 8**.

Done when: the changed-section draft is ready for the final editorial pass, with any remaining required gaps routed to Step 7 and the full labeled preview still pending in Step 9.

---

## Stage 4 — Fill Remaining Behavioral Gaps with Parallel Discovery

### Step 7: Fill remaining behavioral gaps with parallel discovery

Run Step 7 only after one Step 6 branch is complete, and only for canonical template sections or required template fields that still have unresolved behavioral gaps. If the selected Step 6 branch already has enough confirmed information, skip Step 7 and go directly to **Step 8**.

Audit every canonical template section and required template field from `./assets/template.md` that still has no answer, including `## Quality bar for finished work`, `## Related Documentation`, and `## Maintenance guidance` where applicable. For each gap, try to derive the behavioral intent directly from the codebase by using parallel subagents before you ask again or leave a `<!-- TODO: fill in -->`. A behavioral file with explicit TODOs is actionable. A file with missing required template sections silently shapes agent behavior in unpredictable ways.

Discovery fills behavioral gaps. It does not maximize output surface area. Gather broadly when needed, but carry forward only findings that pass the final inclusion rule.

Spawn discovery subagents in parallel. Do not scan serially. Each agent focuses on one behavioral domain and returns structured findings. Wait for all agents to complete. Then merge the results before Step 8.

**Spawn these agents at the same time:**

**Agent A — Version Control & Commit Conventions**
- Commit convention: `commitlint.config.*`, recent `git log --oneline`, `.gitmessage`, `.releaserc*`
- Versioning workflow: `.changeset/`, `CHANGELOG.md`, `standard-version`, `conventional-changelog`
- Forced-push protection: `.github/branch-protection*`, README mentions of branch policy
- Return: commit message format with types and examples, versioning commands, branch protection rules

**Agent B — CI/CD & Pre-commit Workflows**
- PR workflow: `.github/PULL_REQUEST_TEMPLATE.md`, `.github/workflows/` (CI gate names, required checks)
- Pre-commit checks: `.husky/`, `.lefthook.yml`, `package.json#scripts` (lint, typecheck, test)
- Return: PR conventions (size, labels, templates), pre-commit checklist with commands, CI required checks

**Agent C — Testing & Code Quality**
- Test runner: `vitest.config.*`, `jest.config.*`, `pytest.ini`, `pyproject.toml [tool.pytest]`, Playwright, Cypress
- Package manager: `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `bun.lockb`
- TypeScript project: `tsconfig.json` presence, path aliases in `tsconfig.json#paths` or `vite.config`
- Vitest config: `vitest.config.ts` — check for `clearMocks`, `mockReset`, `restoreMocks` flags
- Test file type checking: CI workflows, `package.json` scripts — check if `tsc --noEmit` runs on test files
- Return: test framework, package manager, TS-specific guardrails if applicable, vitest cleanup config

**Agent D — Security & Migrations**
- Migration files: presence of `migrations/`, `prisma/migrations/`, `alembic/`
- Secret handling: `.env.example`, `.gitignore` patterns, presence of `dotenv` or vault tooling
- Return: migration guardrails if migrations exist, secret handling practices

**Agent E — OpenSpec and spec-driven workflow**
- OpenSpec signals: `openspec/` directory, `openspec/config.yml`, `openspec/config.yaml`, and any `opsx:*` or `openspec-*` skill references
- Related workflow evidence: companion documents only when they define durable agent workflow expectations relevant to spec-driven work
- Return: whether a spec-driven workflow is in use, which parts belong in durable agent behavior guidance, and when the agent should invoke that workflow

**After all agents complete:** merge their findings into a unified discovery map.
Tag each template field as `# inferred from [source]` or leave it empty if unknown. Fields that remain empty after discovery become explicit `<!-- TODO: fill in -->` markers in the generated file, and optional template sections should be omitted only when the template explicitly allows removal.

**Preview with source annotations:**

After you merge discovery results, show a preview with trailing comments on inferred values:

```markdown
- Always run `pnpm check` before committing   # inferred from .husky/pre-commit
- Use Conventional Commits (`feat:`, `fix:`)  # inferred from commitlint.config.ts
```

**If a field cannot be inferred** — for example decision heuristics, communication style, or role definition — mark it with `<!-- TODO: fill in -->` rather than omitting the section.

Done when: remaining behavioral gaps are either resolved from repository evidence or left as explicit TODOs before Step 8.

---

## Stage 5 — Preview, Write, and Quality-Check

Do not enter Stage 5 until all earlier required steps for the chosen path are complete.

### Step 8: Run the mandatory final editorial pass before preview

Clean the assembled draft before the user reviews it.

- Deduplicate overlapping guidance across sections.
- Resolve contradictions using the source-precedence rule.
- Remove adjacent-doc or handbook-style material that does not directly govern agent behavior.
- Downgrade brittle specifics unless the specifics are evidenced, behavior-shaping, and durable.
- Replace weakly supported specifics with a durable rule, a canonical link, or `<!-- TODO: fill in -->` when confidence is too low.
- Prefer a shorter, sharper, more behavior-focused final draft over a broader but noisier one.

Done when: the draft is cleaned and ready for preview.

### Step 9: Show the labeled preview and collect review feedback

Show the full labeled preview of the cleaned `AGENTS.md` or `CLAUDE.md` before writing anything.

- Inferred values carry their source comment.
- For **Step 6b**, carried-forward content is labelled `# from existing file`; new content is labelled `# new`.
- Unresolved template fields carry `<!-- TODO: fill in -->`.
- Required template sections from `./assets/template.md` remain present in template order.
- Optional sections are kept only when they still serve the repository and `./assets/template.md` allows them.
- For refresh flows, you may show changed sections first, but the full labeled preview is still required before any write.

This gives the user a complete confidence map.

#### Gate — Collect review feedback before any write

Ask: *"Does this look right? Any sections to correct or expand before I write the file?"*

In non-interactive or headless contexts, still produce the full labeled preview and explicitly note that human confirmation could not be collected in-session. Do not claim the file was human-confirmed if it was not.

Do not write the file until this gate is satisfied or the context is explicitly non-interactive.

Done when: the review gate is satisfied, or the context is explicitly non-interactive.

### Step 10: Write the confirmed file

Run this step only for branches that write output. Skip it for **Step 6d**.

Only after the review gate is satisfied, write to `AGENTS.md` or `CLAUDE.md` in the target directory being onboarded, **stripping the inference source comments**.

Those comments are for review only and must not appear in the final file.

For the `## Related Documentation` section, include links only for files that exist in the repository and materially help agent behavior. Check each candidate file before you include its link. Adapt or remove the template's illustrative bullets (`ARCHITECTURE.md`, `CONSTRAINTS.md`, `openspec/config.yaml`, `JARGON.md`, and any other canonical doc placeholder) based on actual repository files. If `openspec/config.yml` or `openspec/config.yaml` are absent, do not include either path.

Done when: the confirmed file is written without review-only comments.

### Step 11: Run the AGENTS.md or CLAUDE.md quality check

Run this step only after Step 10 writes the file. Skip it for **Step 6d**.

After the write is complete, evaluate the generated file against `./references/rubric.md`.

Use the rubric as a structured post-write review, not as a ceremonial mention. Review the generated `AGENTS.md` or `CLAUDE.md`. If the generated file is `CLAUDE.md`, apply the same rubric to it as the repository's agent-instruction file. Consult same-directory or root-level agent-instruction wrappers and directly linked related docs only when needed to verify scope or references.

Run the review in this order:

1. Confirm the review artifact.
2. Gather only the evidence needed to score fairly.
3. Score every rubric category on the 0-5 scale.
4. Apply the category weights with this formula: `(raw score / 5) × category weight`.
5. Add review notes and the non-scored effectiveness check.

Produce a concise review result for the user that includes:

- the reviewed file path
- the total weighted score out of 100
- the corresponding letter grade using this scale:
  - **A** = 90-100
  - **B** = 75-89
  - **C** = 60-74
  - **D** = 40-59
  - **F** = 0-39
- 2-4 brief strengths
- the weakest rubric categories with their raw scores
- the highest-risk weaknesses, if any
- a short non-scored effectiveness note covering whether the file is likely to change agent behavior in practice

Use the result to drive the user-facing completion behavior:

- If the grade is **A**, tell the user you graded the generated `AGENTS.md` or `CLAUDE.md` and found the quality to be strong.
- If the grade is **B**, tell the user in a simple note that you graded the generated `AGENTS.md` or `CLAUDE.md` and found the quality to be adequate.
- If the grade is **below B**, warn the user that the file is below the desired quality bar and provide concrete remediation recommendations tied to the weakest rubric categories. Keep the remediation guidance actionable, concise, and prioritized. Also offer to revise the file to address the highest-impact issues.

Do not overstate certainty. If part of the score depends on incomplete repository evidence, say so briefly.

Done when: the user has both the generated file and the post-write quality assessment.

### Step 12: Print the completion summary

Run this step only after the applicable previous step is complete.

After the write and quality check are complete, print a brief summary of what was generated, what was inferred versus answered directly, which `<!-- TODO -->` sections still need human input, and the quality-check outcome.

For **Step 6d**, print the same brief summary except for the write and quality-check outcome, and keep the no-write status explicit.

Done when: the user has the final completion summary.

---
## AGENTS.md Template

Read and use the canonical template at: `./assets/template.md`

Treat that file as the source of truth for AGENTS.md structure, including exact section names, section order, required-versus-optional sections, placeholder handling, and default scaffolding. When generating, importing, restructuring, appending, auditing, or refreshing `AGENTS.md`, map all structure-sensitive behavior back to that template rather than to examples, checklists, or embedded section lists in this skill.

When generating or refreshing `AGENTS.md`, follow the template exactly, fill placeholders from confirmed answers or repository evidence, replace unresolved placeholders with `<!-- TODO: fill in -->`, keep required template sections, and omit optional sections only when the template explicitly allows it. Keep the final file lean and behavior-focused rather than copying illustrative text verbatim unless it is confirmed or strongly inferred.

---

## Quality Checklist

Before you consider the onboarding complete, verify that the generated file:

- preserves the behavior/project-DNA separation and redirects non-behavior material to the appropriate canonical companion document, such as `openspec/config.yml`, `openspec/config.yaml`, `ARCHITECTURE.md`, `CONSTRAINTS.md`, `EPISTEMIC-MAP.md`, or `JARGON.md`
- covers every required template section from `./assets/template.md` in the template's order, using `<!-- TODO: fill in -->` where facts remain unknown
- references root-level agent guidance instead of duplicating it in monorepo package files
- includes only related-document links that exist in the repository
- resolves contradictions using source precedence instead of preserving competing standing rules
- deduplicates overlapping guidance across sections
- removes low-value, unstable, handbook-style, or adjacent-doc material that does not materially steer agent behavior
- keeps sections lean and behavior-layer focused rather than padded for surface completeness
- treats template examples and defaults as illustrative scaffolding, not automatic policy
- preserves optional template sections only when they still fit the repository and the template allows them
- shows a full preview before any filesystem write and strips inference comments from the final file
- is reviewed against `./references/rubric.md` after writing, with the resulting quality note or remediation guidance surfaced to the user

---

## Interaction Principles

- **Parallel discovery.** When discovery is needed, spawn subagents at the same time. Do not scan config files one by one.
- **Conversational, not interrogative.** Bundle related questions into a single turn. Use plain-English expository language, not bullet-dump question lists.
- **Infer and confirm.** "You mentioned Husky — I'll assume the pre-commit hook runs `pnpm check`; can you confirm?" is better than asking from scratch.
- **Examples reduce ambiguity.** When asking about decision heuristics, offer concrete scenarios so the user can pattern-match.
- **Iterative.** Let the user amend answers before the final write.
- **Preview before writing.** Always show the full generated `AGENTS.md` or `CLAUDE.md` and get explicit confirmation before touching the filesystem.
- **Infer before asking, ask before omitting.** A file with explicit TODOs is actionable. A file with missing sections silently shapes agent behavior in unpredictable ways.
- **Proportionality matters.** Use the lightest workflow that still produces a reliable result. Keep narrow refreshes narrow unless they expose wider drift.
- **Do not cross the layer boundary.** If the user volunteers non-behavior material during this interview, acknowledge it and note that it belongs in the appropriate canonical companion document, not `AGENTS.md` or `CLAUDE.md`. Route project DNA to `openspec/config.yml` or `openspec/config.yaml` with `accelint-onboard-openspec`, system structure to `ARCHITECTURE.md` with `accelint-architecture-doc`, internal terminology to `JARGON.md` with `jargon-extractor`, assumptions and risks to `EPISTEMIC-MAP.md` with `epistemic-mapper`, and external boundaries to `CONSTRAINTS.md` with `constraints-extractor`.
- **Monorepo: reference, do not duplicate.** If a root-level `AGENTS.md` or `CLAUDE.md` exists, package-level files should reference it and add only what is specific to that package. Repeated instructions across root and package files inflate context on every agent invocation, so keep package files additive, not redundant.
- **Synthesize, then preview.** The user should review the cleaned final draft, not raw assembled notes.
