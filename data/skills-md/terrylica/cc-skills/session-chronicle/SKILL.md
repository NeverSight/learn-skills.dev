---
name: session-chronicle
description: Session log provenance tracking. TRIGGERS - who created, trace origin, session archaeology, ADR reference.
allowed-tools: Read, Grep, Glob, Bash, AskUserQuestion
---

# Session Chronicle

Excavate Claude Code session logs to capture **complete provenance** for research findings, ADR decisions, and code contributions. Traces UUID chains across multiple auto-compacted sessions.

**CRITICAL PRINCIPLE**: Registry entries must be **self-contained**. Record ALL session UUIDs (main + subagent) at commit time. Future maintainers should not need to run archaeology to understand provenance.

**S3 Artifact Sharing**: Artifacts can be uploaded to S3 for team access. See [S3 Sharing ADR](/docs/adr/2026-01-02-session-chronicle-s3-sharing.md).

## When to Use This Skill

- User asks "who created this?" or "where did this come from?"
- User says "document this finding" with full session context
- ADR or research finding needs provenance tracking
- Git commit needs session UUID references
- Tracing edits across auto-compacted sessions
- **Creating a registry entry for a research session**

---

## File Ownership Model

| Directory                                 | Committed? | Purpose                                  |
| ----------------------------------------- | ---------- | ---------------------------------------- |
| `findings/registry.jsonl`                 | YES        | Master index (small, append-only NDJSON) |
| `findings/sessions/<id>/iterations.jsonl` | YES        | Iteration records (small, append-only)   |
| `outputs/research_sessions/<id>/`         | NO         | Research artifacts (large, gitignored)   |
| `tmp/`                                    | NO         | Temporary archives before S3 upload      |
| S3 `eonlabs-findings/sessions/<id>/`      | N/A        | Permanent team-shared archive            |

**Key Principle**: Only `findings/` is committed. Research artifacts go to gitignored `outputs/` and S3.

---

## Part 0: Preflight Check

Verify session storage, find project sessions, and check required tools (jq, brotli, aws, op).

**Full scripts**: [Preflight Scripts](./references/preflight-scripts.md)

Summary of steps:

1. **Verify Session Storage** - Confirm `~/.claude/projects/` exists
2. **Find Current Project Sessions** - Encode CWD path, enumerate main + subagent `.jsonl` files
3. **Verify Required Tools** - Check `jq`, `brotli`, `aws`, `op` are installed

---

## Part 1: AskUserQuestion Flows

### Flow A: Identify Target for Provenance

When the skill is triggered, first identify what the user wants to trace:

```
AskUserQuestion:
  question: "What do you want to trace provenance for?"
  header: "Target"
  multiSelect: false
  options:
    - label: "Research finding/session"
      description: "Document a research session with full session context for reproducibility"
    - label: "Specific code/feature"
      description: "Trace who created a specific function, feature, or code block"
    - label: "Configuration/decision"
      description: "Trace when and why a configuration or architectural decision was made"
    - label: "Custom search"
      description: "Search session logs for specific keywords or patterns"
```

### Flow B: Confirm GitHub Attribution

**CRITICAL**: Every registry entry MUST have GitHub username attribution.

```
AskUserQuestion:
  question: "Who should be attributed as the creator?"
  header: "Attribution"
  multiSelect: false
  options:
    - label: "Use git config user (Recommended)"
      description: "Attribute to $(git config user.name) / $(git config user.email)"
    - label: "Specify GitHub username"
      description: "I'll provide the GitHub username manually"
    - label: "Team attribution"
      description: "Multiple contributors - list all GitHub usernames"
```

### Flow C: Confirm Session Scope

**CRITICAL**: Default to ALL sessions. Registry must be self-contained.

```
AskUserQuestion:
  question: "Which sessions should be recorded in the registry?"
  header: "Sessions"
  multiSelect: false
  options:
    - label: "ALL sessions (main + subagent) (Recommended)"
      description: "Record every session file - complete provenance for future maintainers"
    - label: "Main sessions only"
      description: "Exclude agent-* subagent sessions (loses context)"
    - label: "Manual selection"
      description: "I'll specify which sessions to include"
```

**IMPORTANT**: Always default to recording ALL sessions. Subagent sessions (`agent-*`)
contain critical context from Explore, Plan, and specialized agents. Omitting them
forces future maintainers to re-run archaeology.

### Flow D: Preview Session Contexts Array

Before writing, show the user the full `session_contexts` array, then confirm:

```
AskUserQuestion:
  question: "Review the session_contexts array that will be recorded:"
  header: "Review"
  multiSelect: false
  options:
    - label: "Looks correct - proceed"
      description: "Write this to the registry"
    - label: "Add descriptions"
      description: "Let me add descriptions to some sessions"
    - label: "Filter some sessions"
      description: "Remove sessions that aren't relevant"
    - label: "Cancel"
      description: "Don't write to registry yet"
```

### Flow E: Choose Output Format

```
AskUserQuestion:
  question: "What outputs should be generated?"
  header: "Outputs"
  multiSelect: true
  options:
    - label: "registry.jsonl entry (Recommended)"
      description: "Master index entry with ALL session UUIDs and GitHub attribution"
    - label: "iterations.jsonl entries"
      description: "Detailed iteration records in sessions/<id>/"
    - label: "Full session chain archive (.jsonl.br)"
      description: "Compress sessions with Brotli for archival"
    - label: "Markdown finding document"
      description: "findings/<name>.md with embedded provenance table"
    - label: "Git commit with provenance"
      description: "Structured commit message with session references"
    - label: "Upload to S3 for team sharing"
      description: "Upload artifacts to S3 with retrieval command in commit"
```

### Flow F: Link to Existing ADR

```
AskUserQuestion:
  question: "Link this to an existing ADR or design spec?"
  header: "ADR Link"
  multiSelect: false
  options:
    - label: "No ADR link"
      description: "This is standalone or ADR doesn't exist yet"
    - label: "Specify ADR slug"
      description: "Link to an existing ADR (e.g., 2025-12-15-feature-name)"
    - label: "Create new ADR"
      description: "This finding warrants a new ADR"
```

---

## Part 2: Session Archaeology Process

Scan ALL session files, build the `session_contexts` array, and optionally trace UUID chains.

**Full scripts**: [Archaeology Scripts](./references/archaeology-scripts.md)

Summary of steps:

1. **Full Project Scan** - Enumerate all main + subagent sessions with line counts and timestamps
2. **Build session_contexts Array** - Create the array with ALL sessions (session_uuid, type, entries, description)
3. **Trace UUID Chain** (optional) - Follow parent UUID references across sessions for detailed provenance

---

## Part 3: Registry Schema

Two NDJSON files track provenance:

- **`findings/registry.jsonl`** - Master index, one self-contained JSON object per line
- **`findings/sessions/<id>/iterations.jsonl`** - Iteration-level tracking per session

**Full schema, examples, and field reference**: [Registry Schema Reference](./references/registry-schema.md)

### Required Fields (registry.jsonl)

| Field                        | Format                                      |
| ---------------------------- | ------------------------------------------- |
| `id`                         | `YYYY-MM-DD-slug`                           |
| `type`                       | `research_session` / `finding` / `decision` |
| `created_at`                 | ISO8601 timestamp                           |
| `created_by.github_username` | **MANDATORY** GitHub username               |
| `session_contexts`           | **MANDATORY** Array of ALL session UUIDs    |

---

## Part 4: Output Generation

Brotli compression for session archival and structured git commit messages with provenance.

**Full scripts and templates**: [Output Generation](./references/output-generation.md)

Summary:

- **Compression** - Brotli-9 compress each session to `outputs/research_sessions/<id>/*.jsonl.br` (gitignored)
- **Manifest** - Auto-generated `manifest.json` with target_id, count, timestamp
- **Commit message** - Template includes registry_id, attribution, session counts, S3 retrieval commands

---

## Part 5: Confirmation Workflow

### Final Confirmation Before Write

**ALWAYS** show the user what will be written before appending:

```
AskUserQuestion:
  question: "Ready to write to registry. Confirm the entry:"
  header: "Confirm"
  multiSelect: false
  options:
    - label: "Write to registry"
      description: "Append this entry to findings/registry.jsonl"
    - label: "Edit first"
      description: "Let me modify some fields before writing"
    - label: "Cancel"
      description: "Don't write anything"
```

Before this question, display:

1. Full JSON entry (pretty-printed)
2. Count of session_contexts entries
3. GitHub username attribution
4. Target file path

### Post-Write Verification

After writing, verify:

```bash
# Validate NDJSON format
tail -1 findings/registry.jsonl | jq . > /dev/null && echo "Valid JSON"

# Show what was written
echo "Entry added:"
tail -1 findings/registry.jsonl | jq '.id, .created_by.github_username, (.session_contexts | length)'
```

---

## Part 6: Workflow Summary

```
1. PREFLIGHT
   ├── Verify session storage location
   ├── Find ALL sessions (main + subagent)
   └── Check required tools (jq, brotli)

2. ASK: TARGET TYPE
   └── AskUserQuestion: What to trace?

3. ASK: GITHUB ATTRIBUTION
   └── AskUserQuestion: Who created this?

4. ASK: SESSION SCOPE
   └── AskUserQuestion: Which sessions? (Default: ALL)

5. BUILD session_contexts ARRAY
   ├── Enumerate ALL main sessions
   ├── Enumerate ALL subagent sessions
   └── Collect metadata (entries, timestamps)

6. ASK: PREVIEW session_contexts
   └── AskUserQuestion: Review before writing

7. ASK: OUTPUT FORMAT
   └── AskUserQuestion: What to generate?

8. ASK: ADR LINK
   └── AskUserQuestion: Link to ADR?

9. GENERATE OUTPUTS
   ├── Build registry.jsonl entry (with iterations_path, iterations_count)
   ├── Build iterations.jsonl entries (if applicable)
   └── Prepare commit message

10. ASK: FINAL CONFIRMATION
    └── AskUserQuestion: Ready to write?

11. WRITE & VERIFY
    ├── Append to registry.jsonl
    ├── Append to sessions/<id>/iterations.jsonl
    └── Validate NDJSON format

12. (OPTIONAL) S3 UPLOAD
    └── Upload compressed archives
```

---

## Success Criteria

1. **Complete session enumeration** - ALL main + subagent sessions recorded
2. **GitHub attribution** - `created_by.github_username` always present
3. **Self-contained registry** - Future maintainers don't need archaeology
4. **User confirmation** - Every step has AskUserQuestion confirmation
5. **Valid NDJSON** - All entries pass `jq` validation
6. **Reproducible** - Session UUIDs enable full context retrieval

---

## References

- [S3 Sharing ADR](/docs/adr/2026-01-02-session-chronicle-s3-sharing.md)
- [S3 Retrieval Guide](./references/s3-retrieval-guide.md)
- [Registry Schema Reference](./references/registry-schema.md)
- [Preflight Scripts](./references/preflight-scripts.md)
- [Archaeology Scripts](./references/archaeology-scripts.md)
- [Output Generation](./references/output-generation.md)
- [NDJSON Specification](https://github.com/ndjson/ndjson-spec)
- [jq Manual](https://jqlang.github.io/jq/manual/)
- [Brotli Compression](https://github.com/google/brotli)

---

## Troubleshooting

| Issue                     | Cause                       | Solution                                            |
| ------------------------- | --------------------------- | --------------------------------------------------- |
| Session storage not found | Claude Code not initialized | Start a Claude Code session first                   |
| No sessions in project    | Wrong path encoding         | Check encoded path matches ~/.claude/projects/      |
| jq parse error            | Malformed JSONL             | Validate each line with `jq -c .` individually      |
| brotli not found          | Missing dependency          | Install with `brew install brotli`                  |
| S3 upload fails           | Missing AWS credentials     | Configure AWS CLI or use 1Password injection        |
| UUID chain broken         | Session compacted           | Check related sessions for continuation             |
| GitHub username missing   | Attribution not set         | Always require github_username in registry entry    |
| Registry entry invalid    | Missing required fields     | Verify id, type, created_at, session_contexts exist |
