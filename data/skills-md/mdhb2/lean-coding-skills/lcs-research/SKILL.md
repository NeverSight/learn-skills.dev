---
name: lcs-research
description: "Use this skill to investigate questions against high-trust primary sources and capture findings in cited Markdown. Trigger on 'research', 'look up docs', 'find API reference', 'check official docs', 'how does X work'. Do NOT trigger for: brainstorming (use lcs-explore), implementation (use lcs-task-executor), or code review (use lcs-code-review)."
adapters: [claudecode, opencode]
compatibility: [claudecode, opencode]
---

# LCS Research Skill

Shared Coding Contract: Refer to `../lcs-shared/contract.md` for folder conventions, Handoff format, and token optimization.

**Purpose:** Investigate a question against high-trust primary sources. Capture findings in a cited Markdown file.

**Chain of Truth Level:** Standard

## OKF Frontmatter & Writing Safety

When creating artifacts, include YAML frontmatter following the schema in `../lcs-shared/contract.md`. Follow Artifact Writing Safety rules: generate content first, write one file, verify, stop on failure.

### Trigger

Activate when user wants to: research a library/API, look up documentation, verify how something works, or gather evidence for a technical decision.

### Behavior Checklist

1. Identify the research question and required primary sources (official docs, source code, RFCs).

2. Spin up a background investigation process (or sequential deep-search if background agents unavailable).

3. **Rule:** Follow every claim back to its primary source. Do NOT cite secondary blog posts or summaries unless the primary source is unavailable. If primary source is unavailable, note it explicitly.

4. Write findings to `.lcs/work-items/{ts}-{slug}/research/<topic>.md`.

5. Include a `## Citations` section with exact URLs, file paths, and line numbers.

6. End with Handoff passing the research artifact back to the invoking skill (e.g., `lcs-explore`, `lcs-wayfinder`, `lcs-toprd`).

### Output

- `.lcs/work-items/{ts}-{slug}/research/<topic>.md` with structured findings and citations

## Chain of Truth Report

### Level
Standard

### Sources Checked
- <Primary sources consulted, with URLs/paths>
- `.lcs/state.md` (if present)

### Assumptions
- <label each [verified] or [unverified]>

### Actions Taken
- <Search and source-verification steps performed>

### Verification
- <Findings written; citations verified against primary sources>

### Report
<1-3 sentence summary with confidence rating>

## Handoff

Next recommended skill: {invoking-skill}
Next file to read: .lcs/work-items/{ts}-{slug}/research/<topic>.md
Current phase: research
Current confidence: <low/medium/high>
Blocking questions: <list or None>
Risks to carry forward: <summary>
Source of Truth Bundle: .lcs/state.md, research/<topic>.md
Must Preserve IDs: None
Unresolved IDs: None
Suggested next command: Kembali ke skill pemanggil dan lanjut flow

## Chain of Truth Level

Level: Standard

This skill follows the LCS Chain of Truth protocol at the declared level.
