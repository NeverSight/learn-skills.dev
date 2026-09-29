---
name: lcs-wizard
description: "Use this skill to generate interactive bash scripts for human-in-the-loop manual procedures (infra setup, migrations, deployments). Trigger on 'wizard', 'setup script', 'manual procedure', 'walk me through', 'interactive script'. Do NOT trigger for: code changes (use lcs-task-executor), architecture review (use lcs-codebase-doc), or documentation (use lcs-doc-finalizer)."
adapters: [claudecode, opencode]
compatibility: [claudecode, opencode]
---

# LCS Wizard Skill

Shared Coding Contract: Refer to `../lcs-shared/contract.md` for folder conventions, Handoff format, and token optimization.

**Purpose:** Generate interactive bash scripts for human-in-the-loop manual procedures (infra setup, migrations, deployments).

**Chain of Truth Level:** Standard

## OKF Frontmatter & Writing Safety

When creating artifacts, include YAML frontmatter following the schema in `../lcs-shared/contract.md`. Follow Artifact Writing Safety rules: generate content first, write one file, verify, stop on failure.

### Trigger

Activate when user wants to: create setup scripts, walk through manual procedures, generate interactive wizards, or scaffold infrastructure.

### Behavior Checklist

1. **Scope:** Read `.env.example`, config files, framework configs. Identify every required value the human needs to provide.

2. **Map the journey:** Define exact URLs to open, actions to take, variables to capture. Be specific — "open AWS console" is not enough.

3. **Author the script:** Generate script using `template.sh` helpers: `stage()`, `open_url()`, `ask_secret()`, `write_env()`. Each step should be atomic and verifiable.

4. **Verify:** Run `bash -n` for syntax check and `shellcheck` for best practices. Do NOT execute end-to-end (it blocks on human input).

5. Save to `scripts/<name>-wizard.sh`. End with Handoff instructing user to run the script manually.

### Output

- `scripts/<name>-wizard.sh` — executable bash script with human-in-the-loop prompts

> **Path Exception:** Wizard scripts are saved to the project's `scripts/` directory (documented exception in `../lcs-shared/contract.md`), not under `.lcs/work-items/`, because the human must run them manually.

## Chain of Truth Report

### Level
Standard

### Sources Checked
- `.env.example`, config files, framework configs
- `.lcs/state.md` (if present)

### Assumptions
- <label each [verified] or [unverified]>

### Actions Taken
- <Script authored, syntax-checked, saved>

### Verification
- <bash -n passed; shellcheck passed (if available)>

### Report
<1-3 sentence summary with confidence rating>

## Handoff

Next recommended skill: {context-dependent}
Next file to read: scripts/<name>-wizard.sh
Current phase: wizard
Current confidence: <low/medium/high>
Blocking questions: None
Risks to carry forward: <summary>
Source of Truth Bundle: .lcs/state.md, scripts/<name>-wizard.sh
Must Preserve IDs: None
Unresolved IDs: None
Suggested next command: Jalankan script secara manual

### Orca Tool Overlap

This skill may overlap with Orca's `wizard` tool. Decision: If the task is LCS-tracked (in `.lcs/work-items/`), use this skill for Chain of Truth traceability. If ad-hoc or external, prefer the Orca tool directly. Both paths are valid — skill provides LCS integration, Orca tool provides speed.

## Chain of Truth Level

Level: Standard

This skill follows the LCS Chain of Truth protocol at the declared level.
