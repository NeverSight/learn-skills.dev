---
name: battle-memory
description: "Store AI Agent task output and task-relevant dialogue as project memory in .memory. Use for human-agent collaboration, cross-context continuation, handoff, and future maintenance after implementing, fixing, refactoring, or completing a feature/requirement. When loaded, read only relevant .memory records and project docs, distill important task dialogue, decide whether to create or update memory before finishing, and refine/compress/organize/archive .memory records when requested. When the user invokes battle-memory with init, initialization, install, initialize project guidance by updating AGENTS.md and CLAUDE.md with Battle Memory auto-loading instructions."
---

# Battle Memory

## Overview

Technical skill id: `battle-memory`.

Use Battle Memory to store AI Agent task output and task-relevant dialogue as durable project memory. Once loaded, act on memory proactively: do a lightweight, relevance-first memory intake before implementation, distill important dialogue after each turn, then perform a memory closeout before the final response. Read `.memory/` and project docs on demand to recover only the context needed for the current task; finish by writing or updating a focused memory record in `.memory/` when the task produces durable knowledge.

## Active Memory Protocol

Do not wait for the user to explicitly ask for memory operations. When this skill is active:

- At task start, automatically check whether `.memory/` exists and search `.memory/` plus project-doc filenames/headings for terms from the request.
- Read only the highest-signal matching memory/docs sections needed to orient the work.
- After each dialogue turn, distill task-relevant user instructions, agent findings, decisions, corrections, constraints, blockers, validation results, and follow-up commitments into candidate memory.
- During work, resume memory/docs reading only when a new implementation decision needs context.
- Before the final response, decide whether the task produced durable memory or important dialogue context. If yes, create or update a `.memory/` record without asking for another instruction.
- When the user explicitly asks to refine, compress, clean up, consolidate, organize, optimize, archive, or summarize memory, run the Memory Refinement workflow instead of merely appending another note.
- Mention the memory file in the final response when a record was created or updated.

Skip memory write only when the task is purely conversational, exploratory with no durable conclusion, a tiny mechanical change with no future value, explicitly requested not to persist memory, or impossible to record accurately.

## Initialization Workflow

When the user explicitly references `battle-memory` or `$battle-memory` and also includes an initialization keyword such as `init`, `initialization`, `install`, initialize Battle Memory guidance in the current project instead of running a normal task-memory closeout.

Perform this workflow:

1. Treat the current repository root as the target project unless the user provides a different path.
2. Read existing `AGENTS.md` and `CLAUDE.md` if present. Preserve all existing instructions and formatting outside the Battle Memory section.
3. Create either file if missing. Use UTF-8 without BOM.
4. Add or update one clearly delimited section headed `## Battle Memory` in both files. If a Battle Memory section already exists, update that section in place instead of appending a duplicate.
5. In `CLAUDE.md`, still add the Battle Memory section even if the file imports `@AGENTS.md`; Claude Code users should see the instruction directly when inspecting Claude memory.
6. Do not create `.memory/` during initialization unless the user explicitly asks to create the directory or store an initial memory record.
7. Report which files were created or updated.

Use this guidance text, adapting only language and formatting to match the target file:

```markdown
## Battle Memory

Use the battle-memory skill automatically for feature work, bug fixes, refactors, documentation maintenance, handoffs, cross-context continuation, and tasks that produce durable project knowledge.

At task start, read only the relevant `.memory/` records and project docs needed for the current decision. During work, keep task-relevant dialogue, decisions, source paths, validation results, and follow-ups in mind. Before finishing, create or update a focused `.memory/` record when the task produced durable knowledge.

Store memory in `.memory/`. Keep records concise, searchable, and tied to concrete source paths or docs. Do not store secrets, credentials, raw `.env` values, private personal data, or unnecessary raw chat logs; record redacted operational notes instead.
```

## Sensitive Information Safety

Never store secrets, credentials, private personal data, or raw confidential content in `.memory/`. Treat memory records as long-lived project documentation that may be read by future agents.

- Do not write API keys, access tokens, passwords, private keys, cookies, session values, full connection strings, `.env` values, customer data, personal identifiers, or private chat content that is not needed for future project work.
- When a secret-bearing artifact matters, record only the variable name, config key, file path, or integration boundary. Use placeholders such as `<redacted>` for values.
- Summarize sensitive dialogue at the decision level instead of copying user text verbatim.
- If source files or docs contain secrets, do not quote them in memory. Record the remediation or validation status only.
- If the user explicitly asks to persist sensitive material, refuse to store the raw value and offer a redacted operational note instead.

## Dialogue Distillation

Treat the task conversation itself as memory input. Do not store raw chat logs. Keep concise, decision-oriented summaries that help a future agent understand why the task ended up this way.

For each user/agent round, capture only durable task signal:

- New or changed user requirements.
- Corrections to previous assumptions.
- Decisions made and the reason they matter.
- Important implementation findings or source locations discovered.
- Validation results, skipped checks, blockers, and human-confirmation requirements.
- Follow-up commitments, risks, or open questions.

Do not record small talk, repeated status updates, transient tool output, or internal reasoning that does not change future work. When writing memory, include a `Dialogue Distillation` or `Conversation Trace` section if the dialogue changed scope, constraints, implementation direction, or validation expectations.

## Memory Refinement

When the user asks to refine, compress, clean up, consolidate, organize, optimize, archive, summarize, or reduce `.memory/`, actively perform a memory refinement pass. The goal is to reduce context cost while preserving the information needed for future continuation.

Use this workflow:

1. Determine the refinement scope from the user request, current task, filenames, headings, links, and file modification times. If the scope is broad but still inferable, proceed on the narrowest relevant `.memory/` subtree. Ask before rewriting unrelated memory areas.
2. Read only the target memory records and directly linked records needed to understand relationships. Do not scan all memory unless the user explicitly asks for whole-repository memory cleanup.
3. Preserve non-negotiable facts: current requirements, final decisions, source paths, code identifiers, docs references, validation status, skipped checks, blockers, risks, human-confirmation requirements, and open follow-ups.
4. Compress process history: merge repeated dialogue distillations, remove stale intermediate plans, collapse superseded attempts into one sentence when the final decision is clear, and delete transient tool output.
5. Resolve conflicts explicitly. If old memory contradicts newer verified code or newer user instructions, keep the newer verified state and add a short note such as `Supersedes: <old claim>`.
6. Prefer updating existing memory records in place. Create a new consolidated record only when multiple records are merged or when the old structure prevents retrieval.
7. Keep retrieval strong after compression: preserve stable filenames when possible, keep searchable headings, and retain implementation maps with relative source paths.
8. Do not delete useful source trace. If a record is fully superseded, mark it as superseded or replace it with a short pointer to the consolidated record instead of leaving future agents with a dead end.
9. After refinement, report which memory files were updated, consolidated, superseded, or left unchanged.

During refinement, apply these maintenance rules:

- Stale records: when the request covers broad cleanup or an aged area, list candidate memory files with modification times, prioritize the oldest records in scope, and compress them into current state, decisions, implementation map, validation, and open follow-ups. Use the user's age threshold if provided; otherwise prefer relative age within the target scope over inventing a hard cutoff.
- Plan records: identify records whose main content is a plan, todo list, task chain, next steps, or implementation proposal. Verify whether the plan was completed by checking newer related memory, linked docs, and referenced source/tests. If completed, merge the whole task chain into one concise current-state record and replace old plan records with superseded pointers or archive them when retrieval would be clearer.
- Orphaned records: treat a memory as orphaned only after checking that its source paths, docs links, related memory links, and task-chain references are missing, broken, or no longer tied to current repository behavior. Move orphaned records to `.memory/archive/` or replace them with a short archive pointer; do not silently delete them.

A refined memory record should usually keep these sections:

- Current State: the compressed, actionable truth a future agent should start from.
- Decisions: durable decisions and why they matter.
- Implementation Map: source paths, identifiers, configs, tests, and assets.
- Docs Reference Map: project-doc pages that define or informed the behavior.
- Validation: checks run, skipped checks, and human-confirmation requirements.
- Open Follow-ups: unresolved work, risks, and next actions.
- Superseded Notes: short references to obsolete claims only when needed to avoid rediscovery.

Do not treat refinement as lossy summarization of everything. Treat it as memory maintenance: remove low-value bulk, preserve execution-critical detail, and make the remaining record easier to search and continue from.

## Workflow

1. Inspect repository instructions plus the `.memory/` and project-doc structures. Use `.memory/` for task output memory. Use project docs as documentation reference and style/content guidance. If `.memory/` does not exist, note that and create it later only if durable memory should be stored.
2. Build a relevance map before reading deeply: extract task keywords, feature names, subsystem names, user-visible terms, API names, class/function names, config names, existing docs names, and expected source paths from the request.
3. Read only the smallest likely relevant `.memory/` records, project-doc pages, or sections needed for the next decision. Use navigation, filenames, headings, frontmatter, backlinks, and search hits for the relevance map. Do not bulk-read memory or docs.
4. Cross-check important memory or documentation claims against source code before relying on them for changes. Treat `.memory/` and project docs as context, not as guaranteed truth.
5. Complete the requested implementation, fix, refactor, or investigation using the recovered context.
6. Track task-relevant dialogue distillations as the conversation progresses. Merge them into the final memory record when they affect future continuation.
7. When the task is complete enough to record, read nearby or related `.memory/` records and representative project-doc pages only as needed to match naming, language, heading style, level of detail, and technical reference style.
8. Decide whether to update an existing memory record or create a new one. Prefer updating an existing topic/task memory when the feature already has a memory home; create a new Markdown file in `.memory/` only when no suitable memory record exists.
9. Record the actual shipped behavior and important dialogue-driven decisions, not the intended plan. Base the content on the final code, configuration, tests, user-facing behavior, referenced project-doc content, and task-relevant dialogue distillation.
10. Link related memory records and relevant project-doc pages when they provide context or source-of-truth details.
11. Validate the memory record for stale claims, broken local paths, missing implementation references, missing docs references, missing dialogue decisions, and mismatch with the final changes.

## Context Intake

Before editing code, use `.memory/` first for prior task output and project docs second for documentation details. Answer only the questions that matter for the task:

- What related task memory already exists?
- What feature, subsystem, workflow, or requirement is already documented in project docs?
- What source files, modules, routes, configs, schemas, commands, or assets are named by the memory or docs?
- What constraints, compatibility notes, conventions, or known limitations should shape the implementation?
- What prior decisions or follow-up notes should not be rediscovered from scratch?
- What validation or manual QA patterns does the project expect for this area?

If memory or docs are missing, stale, or contradicted by code, continue from the code and record the gap in the final memory update when relevant.

## Relevance-First Reading

Avoid blind memory and documentation reads. Select `.memory/` records, project-doc pages, or sections by observable relationship to the task:

- File or directory name matches the feature, subsystem, module, route, command, schema, or user workflow.
- Heading, table of contents entry, or docs index text contains task keywords or close synonyms.
- Document links to source files that are likely to change.
- Source files likely to change are mentioned by a document.
- Existing memory or docs link to the document from a related architecture, feature, API, or troubleshooting page.

If a repository has many memory/docs files, start by listing or searching filenames and headings. Use `Doc/README.md`, `Doc/index.md`, `docs/README.md`, `docs/index.md`, `SUMMARY.md`, or sidebars only to locate relevant project docs. Then read the narrowest matching memory records, docs pages, or sections and expand outward only when context is still missing.

Stop reading once memory or docs answer the immediate implementation question, identify the right code entry points, or reveal that source code must be inspected next. Resume reading later only when a new question appears.

Prefer this order:

1. List or search `.memory/` and project-doc filenames and headings.
2. Read navigation or index pages only to locate candidate records or docs.
3. Read the smallest relevant section of candidate memory/docs files.
4. Follow links only when the current section explicitly depends on them.
5. Switch to source code once memory or docs identify the likely implementation area.

## Naming And Code Linkage

When creating or updating memory records, make future retrieval cheap:

- Name files with stable domain terms, not generic task labels. Prefer names that include the feature, subsystem, API, module, or workflow a future agent would search for.
- Use headings that repeat the key feature or subsystem terms from the implementation and user-facing behavior.
- Include an implementation map with concrete relative source paths and the important classes, functions, routes, commands, configs, schemas, or assets.
- Include a docs reference map with the project-doc pages that informed the work or define source-of-truth behavior.
- Include a dialogue distillation section when conversation turns changed requirements, constraints, implementation direction, validation expectations, or follow-up work.
- Mention important code identifiers in prose when they are stable enough to be searched later.
- Link related memory records and docs when the repository convention supports it.
- Add aliases, keywords, or frontmatter tags only if the existing memory/docs system already uses them.
- Avoid titles such as `AI Task Notes`, `Implementation Summary`, or `Fix Details` unless the project already uses that pattern; they do not help future agents find the right memory.

## Memory Content

Include the sections that fit the project's style. Use project docs as a content reference for concrete API boundaries, validation tables, source traces, capability summaries, and known limitations, but store the task output and important dialogue distillation in `.memory/`. Keep the memory record concise and useful for a future agent that has lost conversation context.

- Task or requirement summary: what was delivered and why it exists.
- Dialogue distillation: task-relevant requirements, corrections, decisions, blockers, validation expectations, and follow-up commitments from the conversation.
- User-visible behavior: workflows, UI states, API behavior, data changes, or operational effects.
- Docs reference map: relevant project-doc pages and what they contributed.
- Implementation map: important source files, classes, modules, routes, commands, configs, schemas, tests, or assets, using relative paths that can be searched from the repository root.
- Integration notes: dependencies, contracts, events, schemas, permissions, environment variables, or migration concerns.
- Validation: tests run, checks performed, manual verification, and any checks intentionally not run.
- Continuation notes: known limitations, follow-up work, edge cases, and decisions a future agent should not rediscover.

## Writing Rules

- Use the repository's documentation language. If existing docs are Chinese, write Chinese.
- Use UTF-8 without BOM when creating or editing text files.
- Prefer relative links that work from the documentation file.
- Reference concrete source paths instead of vague module names.
- Keep memory names, headings, dialogue summaries, docs references, and implementation references aligned with the terms developers and agents will search for later.
- Keep claims traceable to code or verified behavior.
- Redact all sensitive values; record only names, paths, contracts, and decisions needed for future work.
- Do not paste large code blocks unless the docs convention requires examples.
- Do not create memory for unrelated cleanup or incidental files.
- Respect repository instructions for builds and validation; if a build requires human confirmation, record unrun build checks honestly instead of running them.

## File Placement

Use the narrowest appropriate location:

- Existing `.memory/` record: update it when the new work extends known task memory.
- Existing `.memory/` category folder: add a focused memory record when the task belongs to that category.
- `.memory/<domain-or-subsystem>/`: prefer this for new task memory when the repository has no stronger convention.
- Create `.memory/` when it does not exist and the task produced durable memory worth preserving.
- Do not store AI Agent task memory in project docs. Update project docs only when the user explicitly asks for project documentation changes or the task itself is documentation maintenance.

## Completion Checklist

- The agent made an explicit memory closeout decision before final response.
- If durable memory was produced, the memory record is in `.memory/`.
- If durable memory was produced, the memory explains the final behavior and main implementation entry points.
- If conversation turns changed task direction or constraints, the memory includes concise dialogue distillation.
- If durable memory was produced, the file name, headings, and keywords are specific enough to be found from future task requests.
- If durable memory was produced, the memory includes concrete source paths or code identifiers for the implemented behavior.
- If durable memory was produced, the memory references relevant project-doc pages when they informed the work.
- If durable memory was produced, related memory/docs links are updated when applicable.
- Validation status is recorded accurately.
- The final response mentions the memory file that was created or updated, or states that no durable memory was stored when that matters.
