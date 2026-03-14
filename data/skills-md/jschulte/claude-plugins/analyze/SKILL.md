---
name: analyze
description: Perform initial analysis of a codebase - detect tech stack, directory structure, and completeness. Gear 1 of the 6-gear reverse engineering pipeline. Automatically detects programming languages, frameworks, architecture patterns, and generates analysis-report.md.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Initial Analysis (Gear 1 of 6)

Estimated Time: 5 minutes
Output: `analysis-report.md` in the current working directory (always here, regardless of spec_output_location)

---

## Activation Triggers

Activate this skill when the user says any of:
- "Analyze this codebase"
- "What tech stack is this using?"
- "How complete is this application?"
- "Run initial analysis"
- "Start reverse engineering process"
- Starting reverse engineering on a new or existing codebase

---

## Execution Pipeline

This skill has four phases. Execute them in order.

### Phase 0: Install Slash Commands

Run the commands in [operations/install-commands.md](operations/install-commands.md) to copy `/speckit.*` commands into the project.

If the copy command fails, log: "Slash command installation skipped -- commands can be installed later." Continue to Phase 1.

Log to user: "Phase 0 complete -- slash commands installed."

### Phase 1: Detection

#### Check for Batch Session

Follow the procedure in [operations/batch-session.md](operations/batch-session.md) to search for `.stackshift-batch-session.json`.

If a batch session is found, load its answers, save them to `.stackshift-state.json`, skip Phase 2, and proceed to Phase 3.

If reading the batch session file fails, log the error and fall back to the normal questionnaire in Phase 2.

Log to user: "Phase 1 complete -- detection type: [type]."

#### Auto-Detect Application Type

Run these detection checks in priority order. Use the first match:

1. **monorepo-service**: Parent directory is `services/` or `apps/` and `../../package.json` exists
2. **nx-app**: `nx.json` exists in current or grandparent directory
3. **turborepo-package**: `turbo.json` exists in current or grandparent directory
4. **lerna-package**: `lerna.json` exists in current or grandparent directory
5. **osiris**: Repository name starts with `ws-`
6. **v9-velocity**: `widget.vm` exists or path contains `v9/widgets/`
7. **v9-viewmodel**: Path contains `v9/viewmodel/widgets/`
8. **generic**: No specific pattern matched (default)

For detection types v9-velocity, v9-viewmodel, and osiris: these are legacy CMS widget types. Run the standard analysis phases (Phase 3) using generic analysis operations. Note in the report that this is a legacy CMS widget. If widget migration framework is selected in Phase 2, the `/stackshift.widget-migrate` command handles the specialized analysis.

### Phase 2: Questionnaire

Present the questions defined in [operations/questionnaire.md](operations/questionnaire.md).

Ask questions conversationally, one at a time or in small related groups. Wait for the user to respond before continuing. Apply the conditional logic rules from that file to determine which questions to skip.

After collecting all answers, write them to `.stackshift-state.json`.

If `.stackshift-state.json` already exists, ask the user: "Existing configuration found. Reuse it or start fresh?"

Log to user: "Phase 2 complete -- configuration saved to .stackshift-state.json."

### Phase 3: Analysis

Run all five analysis operations. For each operation, use the corresponding reference file. Run operations in parallel where possible.

1. **Detect tech stack** -- [operations/detect-stack.md](operations/detect-stack.md)
   Run all language detection commands in parallel. Missing files are normal.
   Log to user: "Analysis 1/5 complete -- tech stack detected."

2. **Extract core metadata** -- Read application name, version, description from manifest files. Read git remote URL.
   Log to user: "Analysis 2/5 complete -- metadata extracted."

3. **Analyze directory structure** -- [operations/directory-analysis.md](operations/directory-analysis.md)
   Map architecture patterns and key components.
   Log to user: "Analysis 3/5 complete -- directory structure analyzed."

4. **Scan documentation** -- [operations/documentation-scan.md](operations/documentation-scan.md)
   Assess existing documentation quality.
   Log to user: "Analysis 4/5 complete -- documentation scanned."

5. **Assess completeness** -- [operations/completeness-assessment.md](operations/completeness-assessment.md)
   Estimate completion percentages with evidence.
   Log to user: "Analysis 5/5 complete -- completeness assessed."

Before proceeding to Phase 4, verify that all five operations produced results. If any operation produced no results, re-run it once. If it still fails, record "Unable to assess" for that section and continue.

### Phase 4: Report Generation

Generate `analysis-report.md` using the template in [operations/generate-report.md](operations/generate-report.md).

Write the report to the current working directory as `analysis-report.md`.

Read the StackShift version from `.claude-plugin/plugin.json` for the report header.

Log to user: "Phase 4 complete -- analysis-report.md generated."

Present a summary of findings to the user and ask if they are ready to proceed to Gear 2 (Reverse Engineer).

---

## Path Descriptions

### Greenfield (Build New App from Business Logic)

Use when building a new application based on existing business logic, migrating to a different tech stack, or wanting platform-agnostic specifications.

Result: Specifications focus on WHAT (business requirements only), tech-stack agnostic.

Example: "Extract the business logic from this Rails app so we can rebuild it in Next.js"

### Brownfield (Manage Existing with Spec Kit)

Use when managing an existing codebase with specs, planning upgrades or refactoring, or needing specs that match current implementation.

Result: Specifications include WHAT and HOW (business logic + technical implementation), tech-stack prescriptive.

Example: "Add GitHub Spec Kit to this Next.js app so we can manage it with specs going forward"

---

## Shell Command Error Handling

Apply these rules to every shell command across all operation files:

1. **Commands that return no output**: Treat as "not found" and note the absence in the report. Do not treat as an error.
2. **Commands that fail with non-zero exit**: Log the failure and continue with remaining commands. Never abort analysis due to a single command failure.
3. **Commands that produce excessive output**: Use `head -50` for directory listings and `head -20` for grep results. Note truncation in the report if it occurs.
4. **Commands on files with spaces in names**: Use `-print0` / `-0` flags with find/xargs pipelines where practical.
5. **Always exclude**: node_modules, vendor, .git, build, dist, target, __pycache__, .next, .nuxt, coverage directories.

---

## State Cleanup

If analysis fails or is interrupted before report generation, delete `.stackshift-state.json` to prevent stale configuration from affecting re-runs.

If the user cancels mid-analysis, inform them: "Analysis was interrupted. Run the analyze skill again to restart."

---

## Cruise Control Behavior

When Cruise Control transmission is selected, the entire pipeline runs non-interactively after Phase 2. The progress log messages at each phase boundary serve as checkpoints. If any phase fails during Cruise Control, stop execution, report the failure, and ask the user how to proceed.

---

## Handling Re-analysis

If `analysis-report.md` already exists when this skill activates:
1. Ask the user: "An analysis report already exists. Update it, or skip to Gear 2?"
2. If updating: re-run the full analysis pipeline and overwrite the existing report.
3. If skipping: confirm the existing report is still accurate and proceed to Gear 2.

If the user already knows their tech stack and just wants to configure the pipeline, skip Phase 3 analysis operations and proceed directly to Phase 4 report generation using user-provided information.

---

## After Analysis

Once `analysis-report.md` is generated and reviewed, proceed to Gear 2 (Reverse Engineer) using the reverse-engineer skill.

The analysis report is Gear 1's output. Gear 2 reads it as input to generate comprehensive documentation.
