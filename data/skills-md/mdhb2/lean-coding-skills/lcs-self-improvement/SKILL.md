---
name: lcs-self-improvement
description: 'use this skill when the user asks to analyze current conversation context, supplied conversation history, reference files, folders, project rules, existing instructions, or skills to identify friction patterns and recommend improvements. trigger for prompts like "review what went wrong", "improve future agent behavior", "analyze this conversation", "generate self-improvement recommendations", or "suggest updates to our rules or skills". do not trigger for normal debugging, routine implementation, direct rule edits, or direct skill edits unless the user asks for self-improvement analysis.'
---

# LCS Self Improvement

Platform-neutral skill for diagnostic self-improvement analysis.

## Purpose

Use this skill to analyze interaction history and project context, identify friction and success patterns, and produce reviewable recommendations without applying any changes.

## Non-Negotiable Rules

1. Do not apply changes automatically.
2. Do not edit rules, instruction files, or skills as part of this skill run.
3. Output files use timestamped structure: `.lcs/docs/self-improvements/{timestamp}-analysis.md`.
4. State tracking via `.lcs/docs/self-improvements/state.json`.
5. Navigation via auto-generated `.lcs/docs/self-improvements/index.md`.
6. Do not include raw user quotes by default.
7. If evidence is insufficient, state it and use `[TODO]` instead of guessing.

## When To Use

Use when user asks to:

- review what went wrong
- improve future agent behavior
- analyze friction in current or prior sessions
- generate self-improvement recommendations
- audit rules, instructions, or existing skills
- suggest instruction or skill improvements

Do not use for routine debugging, feature implementation, plain conversation summaries, or direct editing of rules/skills.

## Inputs

Analyze available evidence from:

- current conversation context (default when available)
- supplied files and folders
- exported logs (`.jsonl`, markdown notes, transcripts)
- project docs and instructions (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `README.md`)
- `.lcs/` content
- existing skill directories (`skills/`)

If current conversation is unavailable and user provides no files/folders, generate limited report with clear evidence limits and `[TODO]` markers.

## OKF Frontmatter & Writing Safety

- When creating analysis files (`.lcs/docs/self-improvements/{timestamp}-analysis.md`), include YAML frontmatter following the schema in `../lcs-shared/contract.md` with `artifact_type: self_improvement`.
- Follow the Artifact Writing Safety rules in contract.md — generate content first, write one file, verify, stop on failure.

## Workflow Checklist

- [ ] Phase 1: Collect available context and references
- [ ] Phase 2: Analyze friction, success patterns, and repeated issues
- [ ] Phase 3: Cross-reference existing instructions, docs, rules, and skills
- [ ] Phase 4: Generate `.lcs/docs/self-improvements/{timestamp}-analysis.md`
- [ ] Phase 5: Validate report and explain how to use it

## Phase 1 - Collect Context and References

1. Ensure output directory exists: `mkdir -p .lcs/docs/self-improvements`.
2. Generate timestamp: `YYYYMMDDHHmmss` format (14 digits, e.g., `20260529134147`).
3. Check for legacy file `.lcs/docs/self-improvements.md`:
   - If exists: migrate to `.lcs/docs/self-improvements/archive-legacy.md`
   - Log migration message to user
4. Read existing state file `.lcs/docs/self-improvements/state.json`:
   - If exists: load previous analyses and recommendations
   - If not exists: initialize empty state structure
5. Record source scope:
   - current conversation only
   - supplied file(s)
   - supplied folder(s)
   - project instructions
   - existing skills
   - combined sources
6. If only current conversation is available, treat findings as session-specific.
7. Avoid long-term trend claims unless clear repeated evidence exists.

## Phase 2 - Analyze Friction and Success Patterns

Extract and summarize:

1. User goal.
2. Friction patterns:
   - misunderstandings
   - repeated corrections
   - stale assumptions
   - constraint misses
   - workflow ambiguity
3. Success patterns:
   - effective constraints
   - effective formats
   - reusable workflow choices
4. High-impact issues:
   - repeated name/path corrections
   - stale references
   - platform-specific leakage
   - missing report/apply separation
   - privacy risk
   - weak validation
5. Improvement opportunities:
   - instruction updates
   - rule updates
   - skill updates
   - checklist updates
   - validation scripts/checks

Use summarized evidence only unless user explicitly requests raw quotes.

For deeper prompts and consistency, read `references/analysis-checkpoints.md` when needed.

## Phase 2.5 - Deduplicate Recommendations

Before finalizing recommendations:

1. Generate unique ID for each recommendation using SHA256 hash of:
   - Category (AGENTS.md, skills/, .lcs/, etc.)
   - Title/summary
   - Target location
2. Compare against previous recommendations in state.json:
   - Mark as `NEW` if ID not found in previous analyses
   - Mark as `RECURRING` if ID exists in previous analyses
   - Preserve status from state.json (pending/applied/rejected)
3. For recurring recommendations:
   - Note first seen timestamp
   - Note last seen timestamp
   - Include reference to previous analysis file(s)
4. Calculate statistics:
   - Total recommendations: X
   - New: Y
   - Recurring: Z
   - Previously applied: W (from state.json)

## Phase 3 - Cross-Reference Instructions, Docs, Rules, Skills

Inspect relevant available files, including:

- `AGENTS.md`
- `CLAUDE.md` (if present)
- `GEMINI.md` (if present)
- `README.md`
- `.lcs/`
- `.lcs/docs/`
- `.lcs/rules/`
- `skills/`

For each friction pattern, classify status:

1. `Already addressed`
2. `Partially addressed`
3. `Missing`
4. `Conflicting`
5. `Needs user decision`

If target location unclear, mark `[ASK USER]`.

For mapping recommendation types to file targets, read `references/improvement-targets.md`.

## Phase 4 - Generate Report

Create timestamped report file and update supporting files:

1. **Main report:** `.lcs/docs/self-improvements/{timestamp}-analysis.md`
2. **State file:** `.lcs/docs/self-improvements/state.json`
3. **Index file:** `.lcs/docs/self-improvements/index.md`

Use full template from `references/report-template.md`.

Mandatory report traits:

- evidence-based, no unsupported claims
- no raw user quotes by default
- uses `[TODO]` where evidence missing
- uses `[ASK USER]` where policy/preference required
- separates diagnosis from proposals
- explicitly states no changes were applied

### Report Structure Enhancements

Include in the report header:

```markdown
# Self-Improvement Analysis
**Generated:** YYYY-MM-DD HH:mm:ss
**Timestamp:** {timestamp}
**Previous analyses:** X (see index.md)
**Source scope:** [current conversation | supplied files | combined]

## Summary Statistics
- Total recommendations: X
- New recommendations: Y
- Recurring recommendations: Z
- Previously applied: W (tracked in state.json)
```

Organize recommendations into sections:

1. **New Recommendations** - Not seen in previous analyses
2. **Recurring Recommendations** - Appeared in previous analyses
   - Include note: "Also flagged in analysis {timestamp}"
   - Include first seen / last seen timestamps

### State File Structure

Update `.lcs/docs/self-improvements/state.json`:

```json
{
  "version": "1.0",
  "last_updated": "2026-05-29T13:38:25Z",
  "analyses": [
    {
      "timestamp": "20260529133823",
      "file": "20260529133823-analysis.md",
      "created_at": "2026-05-29T13:38:25Z",
      "source_scope": "current conversation",
      "recommendations_count": 5,
      "recommendations": [
        {
          "id": "sha256-first-16-chars",
          "category": "AGENTS.md",
          "title": "Brief title",
          "target_location": "AGENTS.md section 3",
          "status": "pending",
          "confidence": "high",
          "first_seen": "20260529133823",
          "last_seen": "20260529133823"
        }
      ]
    }
  ]
}
```

### Index File Structure

Generate/update `.lcs/docs/self-improvements/index.md`. It is a navigation artifact and MUST carry OKF frontmatter with `artifact_type: index` so whole-directory scans (e.g. `validate-okf.py .lcs/docs/`) pass:

```markdown
---
title: "Self-Improvement Analyses"
format_version: "okf/0.2"
authors:
  - type: agent
    name: "lcs-self-improvement"
created: "{YYYY-MM-DD}"
updated: "{YYYY-MM-DD}"
tags: [index, self-improvement]
summary: "Navigation index of self-improvement analyses"
status: active
related: []
artifact_type: index
source: "state.json"
cot_level: standard
version: "1.0"
---

# Self-Improvement Analyses

## Latest Analysis
- [2026-05-29 13:38:23](20260529133823-analysis.md) - 5 recommendations (3 new, 2 recurring)

## History
- [2026-05-28 09:15:00](20260528091500-analysis.md) - 4 recommendations
- [2026-05-27 14:20:30](20260527142030-analysis.md) - 6 recommendations

## Statistics
- Total analyses: 3
- Total unique recommendations: 12
- Status breakdown:
  - Pending: 7
  - Applied: 5
  - Rejected: 0

## How to Use
1. Review latest analysis for new recommendations
2. Check recurring recommendations (may indicate higher priority)
3. Update state.json when applying recommendations (change status to "applied")
4. Re-run analysis periodically to track improvements
```

## Phase 5 - Validate and Explain Usage

Before final response, verify:

1. `.lcs/docs/self-improvements/{timestamp}-analysis.md` exists.
2. `.lcs/docs/self-improvements/state.json` exists and is valid JSON.
3. `.lcs/docs/self-improvements/index.md` exists and includes latest analysis.
4. No instruction/rule/skill files were modified by this skill run.
5. No raw user quotes appear unless explicitly requested.
6. Every recommendation has target location or `[ASK USER]`.
7. Confidence levels are included.
8. Recommendation IDs are generated (SHA256 hash).
9. New vs recurring recommendations are clearly marked.
10. User is told report is diagnostic only.
11. User is told future behavior changes only after accepted recommendations are applied to persistent sources.

## Implementation Guidance

This report is not automatically active behavior.

To make recommendations effective in future sessions, accepted items must be applied to persistent files that agent reads, for example:

- `AGENTS.md` for general coding-agent behavior
- `CLAUDE.md` or `GEMINI.md` for model-specific behavior (only if relevant and present)
- `.lcs/rules/` for reusable local rules
- `.lcs/docs/` for process/reference documentation
- `skills/` for repeatable workflows
- `README.md` or onboarding docs for human-facing usage
- checklists/scripts for validation-heavy controls

Do not apply these updates automatically during self-improvement analysis.

## State Management

### Updating Recommendation Status

When user applies a recommendation:

1. Open `.lcs/docs/self-improvements/state.json`
2. Find recommendation by ID
3. Update status field:
   - `pending` -> `applied` (when implemented)
   - `pending` -> `rejected` (when decided against)
4. Add `applied_at` or `rejected_at` timestamp
5. Save state.json

Example manual update:
```json
{
  "id": "a1b2c3d4e5f6g7h8",
  "status": "applied",
  "applied_at": "2026-05-29T14:00:00Z"
}
```

### Migration from Legacy Format

If `.lcs/docs/self-improvements.md` exists (legacy format):

1. Move to `.lcs/docs/self-improvements/archive-legacy.md`
2. Parse recommendations (best effort)
3. Create initial state.json with:
   - Single analysis entry with timestamp "00000000000000-legacy"
   - All recommendations marked status "unknown"
   - Note in index.md about legacy migration
4. Inform user:
   ```
   Migrated legacy report to archive-legacy.md.
   Previous recommendations imported with status "unknown".
   Review and update state.json manually if needed.
   ```

### Recommendation ID Generation

Generate stable IDs using SHA256 hash of:
```
category + "|" + title + "|" + target_location
```

Take first 16 characters of hex digest for readability.

Example:
```
Input: "AGENTS.md|Add validation rule|AGENTS.md section 4"
SHA256: "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6..."
ID: "a1b2c3d4e5f6g7h8"
```

## Chain of Truth Report

### Level
Standard

### Sources Checked
- Current conversation context (when available)
- Supplied files, folders, and exported logs
- Project instructions (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `README.md`)
- `.lcs/` content and existing skill directories (`skills/`)
- `references/analysis-checkpoints.md` and `references/improvement-targets.md`

### Assumptions
- User wants diagnostic-only analysis (no automatic changes)
- Evidence available is representative of actual friction patterns
- Legacy `.lcs/docs/self-improvements.md` (if present) should be migrated

### Plan
1. Phase 1: Collect context and references
2. Phase 2: Analyze friction, success patterns, and repeated issues
3. Phase 2.5: Deduplicate recommendations against state.json
4. Phase 3: Cross-reference existing instructions, docs, rules, skills
5. Phase 4: Generate timestamped report, state.json, and index.md
6. Phase 5: Validate output files and explain usage

### Actions Taken
- Collected available context and references
- Analyzed friction and success patterns
- Generated unique recommendation IDs via SHA256
- Cross-referenced findings against existing project instructions
- Created `.lcs/docs/self-improvements/{timestamp}-analysis.md`
- Updated `.lcs/docs/self-improvements/state.json` and `index.md`

### Verification
- Output files exist: analysis.md, state.json, index.md
- state.json is valid JSON
- No instruction/rule/skill files were modified
- No raw user quotes included (unless explicitly requested)
- All recommendations have target location or `[ASK USER]`

### Report
**Confidence**: Low/Medium/High (based on evidence completeness)
**Nature**: Diagnostic only — no changes were applied automatically

## Handoff

Next recommended skill: manual review
Next file to read: .lcs/docs/self-improvements/index.md
Current phase: self_improvement_review
Current confidence: medium
Blocking questions: None
Risks to carry forward: Recommendations may be incomplete if evidence was limited; recurring items may indicate higher priority issues
Source of Truth Bundle: .lcs/docs/self-improvements/{timestamp}-analysis.md, .lcs/docs/self-improvements/state.json, .lcs/docs/self-improvements/index.md
Must Preserve IDs: None
Unresolved IDs: None
Suggested next command: Review self-improvement recommendations and decide which ones to apply

## Chain of Truth Level

Level: Standard

This skill follows the LCS Chain of Truth protocol at the declared level.
