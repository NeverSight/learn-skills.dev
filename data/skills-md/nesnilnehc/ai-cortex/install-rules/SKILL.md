---
name: install-rules
description: Install rules from this project or a specified Git repo into Cursor or Trae IDE. Use when the user wants to add project/global rules to their editor from ai-cortex rules/ or another repository.
tags: [automation, infrastructure, eng-standards]
version: 1.2.0
license: MIT
related_skills: [discover-skills]
recommended_scope: both
metadata:
  author: ai-cortex
---

# Skill: Install Rules

## Purpose

Install **rules** (passive constraints for AI behavior) from a rules source into an editor’s rules destination. The primary source is this project’s `rules/` directory, or a user-specified Git repository. Supported install targets: **Cursor** (`.cursor/rules/`) and **Trae IDE** (`.trae/project_rules.md` / `.trae/user_rules.md`).

## Use Cases

- **This project**: Install all or selected rules from the current repo’s `rules/` into the current project’s Cursor or Trae rules.
- **Another Git repo**: User provides `owner/repo` (and optionally branch/ref and subpath); list rules from that repo and install selected ones to Cursor or Trae.
- **Bootstrap**: After cloning ai-cortex or another rule-providing repo, install its rules so the Agent respects them in the user’s workspace.

## Behavior

1. **Resolve source**:
   - **This project**: Use the repo’s `rules/` directory. Treat `rules/INDEX.md` as the authoritative list; if present, parse the registry table to get rule names and file paths. Otherwise list all `*.md` files under `rules/` (excluding `INDEX.md`).
   - **Specified Git repo**: User supplies `owner/repo` or full clone URL, and optionally branch/ref and subpath (e.g. `rules` or `docs/rules`). The Agent must have network access to clone or fetch; state this before proceeding. Discover rules by: (a) looking for an `INDEX.md` (or equivalent) in the subpath and parsing the registry, or (b) listing `*.md` files in that directory. If the repo or path does not exist or contains no rules, report clearly and do not write files.

2. **List rules**: Output a list of installable rules (name, short description or scope). Let the user choose “all” or a subset by name.

3. **Analyze destination state (required)**:
   - **Cursor**: List existing `./.cursor/rules/*.mdc` (project-level) or the user-level rules directory if selected. Identify which target filenames already exist.
   - **Trae**: Read the selected destination file (`./.trae/project_rules.md` or `./.trae/user_rules.md`, or global user-level if selected) if it exists. Detect whether a managed block already exists (see step 6).

4. **Build an install plan (required)**:
   - For each selected rule, decide one action: `create`, `skip (identical)`, `conflict (different)`, or `update (explicit overwrite approved)`.
   - The default must be conservative:
     - Existing-but-different targets are `conflict` until the user explicitly approves overwrite.
     - Existing-and-identical targets are `skip`.
   - Output the plan before any write, including the intended target path(s) and per-rule actions.

5. **Confirm before writing**:
   - Do not create, modify, or overwrite any file under `.cursor/rules/`, `.trae/`, or any target path until the user explicitly confirms the plan.
   - If overwrites are included, require explicit confirmation that lists which rule targets will be overwritten.

6. **Install to Cursor**:
   - **Target path**: Project-level is `./.cursor/rules/` (relative to repo root); user-level is platform-dependent (e.g. `~/.cursor/rules/` if applicable). Prefer project-level unless the user asks for user-level. Create the directory if it does not exist.
   - **Format**: Write one `.mdc` file per rule. Cursor expects frontmatter with at least `description`. Optionally set `globs` (file pattern) or `alwaysApply: true`. Map source rule metadata: use `name` and `scope` (or equivalent) to build `description`; if scope indicates “all code” or “global”, set `alwaysApply: true`; otherwise leave `alwaysApply: false` and omit or set `globs` only when the source rule clearly implies a file type.
   - **Body**: Preserve the full rule body (everything after the source frontmatter). Do not drop content.
   - **Idempotency**: Before writing, normalize content (e.g., newline normalization) and compare with existing target content (if any). If identical, `skip`.
   - **Conflicts**: If the target exists and differs, do not overwrite unless the plan includes `update` and the user explicitly confirmed overwrite. Consider creating a backup (e.g. `<file>.bak`) when overwriting if the user requests it.

7. **Install to Trae (managed block)**:
   - **Target path**: Project-level is `./.trae/project_rules.md`; user-level is `./.trae/user_rules.md` (project-scoped) or `~/.trae/user_rules.md` (global, if Trae supports it). Prefer project-level unless the user asks for user-level. Create the `.trae/` directory if it does not exist.
   - **Format**: Trae uses plain Markdown.
   - **Managed block (required)**:
     - The installer must only write within a managed block to avoid modifying user-authored rules.
     - Use the following markers:
       - Begin: `<!-- ai-cortex:begin -->`
       - End: `<!-- ai-cortex:end -->`
     - If the managed block exists, replace the entire block content (idempotent update).
     - If it does not exist, insert the block (typically appended to the end of the file).
   - **Block contents**:
     - Inside the block, render one section per rule using `## Rule: <name>` headers, in a stable order (prefer the `rules/INDEX.md` registry order when available).
     - Preserve each rule body (everything after the source frontmatter). Do not add Cursor-style frontmatter.
     - Deduplicate by rule name inside the managed block (one name → one section).
   - **Idempotency**: If re-rendered managed block is identical to the current managed block, `skip` and do not rewrite the file.

8. **Output**: After installation, report per the Output contract (Appendix): the plan, executed actions (`created/updated/skipped/conflicts`), target path(s), and any conversion notes or failures.

## Input & Output

### Input

- **Source**: Default “this project” (current repo `rules/`). Or: Git repo `owner/repo` or URL, with optional branch/ref and subpath (e.g. `rules`, `docs/rules`).
- **Target**: One or both of Cursor, Trae. Both are supported.
- **Scope**: “All” rules or a subset (list of rule names).
- **Destination**: Project-level (`.cursor/rules/` for Cursor, `.trae/project_rules.md` for Trae) or user-level; default project-level.
  - **Conflict policy**: Default is conservative (no overwrite). If the user requests overwrites, the plan must mark `update` for those targets and require explicit confirmation.

### Output

- **Before install**: Rule list + destination analysis summary + install plan (`create/skip/conflict/update`) with target paths.
- **After install**: Executed actions, target path(s), and any errors or conversion notes (see Appendix: Output contract).

## Restrictions

- **No write without confirmation**: Do not create or modify files under `.cursor/rules/`, `.trae/`, or any target path without explicit user confirmation of the plan.
- **No overwrite without confirmation**: If a target already exists and differs, do not overwrite unless the user explicitly agrees and the plan includes `update` for that target.
- **Git and network**: Installing from a Git repo requires clone/fetch; state that network (and optionally git) is required and confirm before running clone/fetch.
- **Trae managed block only**: When installing to Trae, only write within the managed block (`<!-- ai-cortex:begin -->` … `<!-- ai-cortex:end -->`). Do not modify content outside the block.

## Self-Check

- [ ] **Source resolved**: Was the rules source (this repo `rules/` or specified Git repo + path) read correctly? Was `rules/INDEX.md` or equivalent used when present?
- [ ] **List shown**: Was the user shown the list of rules to be installed before any write?
- [ ] **Destination analyzed**: Were existing Cursor/Trae destinations scanned and summarized before building a plan?
- [ ] **Plan produced**: Was an explicit plan (`create/skip/conflict/update`) shown before any write?
- [ ] **Confirmation**: Was explicit user confirmation obtained before creating/modifying/overwriting any file?
- [ ] **Output contract**: Does the post-install output include the plan, executed actions, target path(s), and any conversion or failure notes?
- [ ] **Restrictions**: Were overwrites only done with explicit consent? For Trae, was content outside the managed block left untouched?

## Examples

### Example 1: Install all rules from this project to Cursor

- **Scenario**: User says “install this project’s rules into Cursor.”
- **Steps**:
  1. Read `rules/INDEX.md` and build the list of rules from the registry table (or list `rules/*.md` excluding `INDEX.md`).
  2. Analyze existing `.cursor/rules/*.mdc` and build a plan (create/skip/conflict).
  3. Present the plan and ask for confirmation.
  4. After confirmation, execute the plan: write only `create` actions; do not overwrite conflicts unless explicitly approved.
  5. Output: created/updated/skipped/conflicts and path `./.cursor/rules/`.

### Example 2: Edge case — Git repo with no INDEX, custom subpath

- **Scenario**: User wants to install rules from `other-org/repo`, branch `main`, subpath `docs/rules`. That repo has no `docs/rules/INDEX.md`, only `docs/rules/foo.md` and `docs/rules/bar.md`.
- **Steps**:
  1. State that network access is needed to clone/fetch the repo; ask for confirmation.
  2. After confirmation, clone or fetch and list `docs/rules/*.md` (e.g. foo.md, bar.md). Do not assume an INDEX; use the directory listing as the rule list.
  3. Present the list (foo, bar) and target path; ask which rules to install (or “all”) and confirm before writing.
  4. If the user selects only "foo", install only the file derived from `foo.md` to `.cursor/rules/foo.mdc` and report: installed [foo], path `./.cursor/rules/`, and that bar was skipped.

### Example 3: Install rules to Trae

- **Scenario**: User says "install this project's rules into Trae" or "install to both Cursor and Trae".
- **Steps**:
  1. Read `rules/INDEX.md` and build the list of rules.
  2. Read `.trae/project_rules.md` if it exists and detect whether the managed block already exists.
  3. Build a plan (insert managed block, update managed block, or skip if identical) and present it for confirmation.
  4. After confirmation, render the managed block with `## Rule: <name>` sections and insert/replace the block only.
  5. Output: created/updated/skipped and path `./.trae/project_rules.md`, noting managed-block behavior.

---

## Appendix: Output contract

After performing an install, the Agent must report:

| Element | Requirement |
| :--- | :--- |
| **Plan** | Show the pre-write plan with per-rule actions (`create/skip/conflict/update`) and target path(s). |
| **Executed actions** | Summarize what was actually created/updated/skipped and list any conflicts left unresolved. |
| **Installed rules** | List of rule names (or filenames) that were written (subset of executed actions). |
| **Target path** | Absolute or repo-relative path (e.g. `./.cursor/rules/` for Cursor, `./.trae/project_rules.md` for Trae). |
| **Conversion notes** | Brief note if source used a different format and how it was mapped (e.g. .md to Cursor .mdc, or .md concatenated to Trae project_rules.md). |
| **Failures** | Any rule that could not be installed (e.g. read error, write error) and reason. |
| **Trae** | If Trae was selected, note the managed block markers and confirm that content outside the block was not modified. |
