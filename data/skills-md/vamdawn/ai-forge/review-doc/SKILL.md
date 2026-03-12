---
name: review-doc
description: "Structured document review and quality improvement. Use when the user asks to review, proofread, check, audit, or improve a document (Markdown, text, or any prose file). Triggers include: 'review this doc', 'check this document', 'proofread', 'audit this spec', 'review and fix', or any request to find and fix issues in written documents. Supports reviewing against referenced standards (PRD, design docs, style guides)."
argument-hint: "[file-path]"
allowed-tools: Read, Edit, Task, Grep, Glob
---

# Document Review

## Workflow

1. **Read target document** — Read the ENTIRE file at `$ARGUMENTS` in one pass. Note total line count.
2. **Read referenced documents** — Scan for mentions of PRDs, design docs, specs, or style guides. Read each one for context. If none found, proceed without.
3. **Choose review mode** — Based on document size:
   - **≤300 lines** → Single-agent mode (Step 4a)
   - **>300 lines** → Parallel multi-agent mode (Step 4b)

### 4a. Single-Agent Review

Spawn ONE review sub-agent via Task tool (subagent_type: "general-purpose"). Pass full document content and all referenced context. Instruct the sub-agent to:
- Check correctness, structure, completeness, clarity, and grammar
- Categorize each issue as Critical / Important / Minor
- Return a markdown table: `Severity | Line | Category | Issue | Fix`
- Sort by severity (Critical first), then line number

### 4b. Parallel Multi-Agent Review

For documents >300 lines, split and review concurrently:

1. **Partition the document** — Divide by top-level headings (h1/h2) into logical sections. If no headings exist, split into chunks of ~300 lines with 20-line overlap to catch cross-boundary issues. Target 2–5 chunks; never exceed 5.
2. **Spawn parallel sub-agents** — Launch ALL sub-agents in a single message using multiple Task tool calls (subagent_type: "general-purpose"). Each sub-agent receives:
   - Its assigned section/chunk (with line number range clearly stated)
   - The full list of referenced documents for context
   - A brief summary of the rest of the document (surrounding section titles + first sentence) so it can assess cross-references
   - Instructions to check: correctness, structure, completeness, clarity, grammar
   - Instructions to return a markdown table: `Severity | Line | Category | Issue | Fix`
3. **Spawn a structure sub-agent in parallel** — In the same message as Step 2, launch one additional sub-agent that reviews the document holistically for:
   - Overall structure and logical flow
   - Missing sections or content gaps
   - Inconsistencies between sections (terminology, style, tone)
   - Duplicate or contradictory content
   - Table of contents accuracy (if present)
4. **Merge results** — Collect all sub-agent tables. Deduplicate issues that appear in overlapping regions (keep the more specific description). Combine into one unified table sorted by severity then line number.

### 5. Apply fixes

Apply ALL fixes in one pass using Edit tool.

### 6. Verify

Re-read the document. If new issues remain, do ONE more fix pass maximum.

### 7. Report

Output summary to the user using the format below.

## Output Format

```
## Document Review: [filename]

### Review Mode
[Single-agent | Parallel (N section agents + 1 structure agent)]

### Issues Found
| Severity | Line | Category | Source | Issue | Fix Applied |
|----------|------|----------|--------|-------|-------------|
| Critical | 42   | Correctness | Section 2 | Wrong endpoint URL | ✅ |
| Important | 128  | Structure | Holistic | Missing error handling section | ✅ |

### Summary
- Critical: N found, N fixed
- Important: N found, N fixed
- Minor: N found, N fixed
- Passes: 1 | Status: ✅ Complete
```

## Edge Cases

- **>1000 lines**: Read in 500-line chunks, complete full read before review.
- **No clear section boundaries**: Fall back to fixed-size ~300-line chunks with 20-line overlap.
- **No issues found**: Report clean result — do not invent issues.
- **User specifies focus area**: Prioritize that area but still do a full review pass.
- **File not found or unreadable**: Report error to user and terminate — do not proceed with review.
- **Sub-agent failure**: If one parallel sub-agent fails, merge results from successful ones and log a warning. If all fail, fall back to reviewing directly in main session.
- **Referenced document unreadable**: Log a warning in the report and continue review without that reference.
- **Overlapping issues from parallel agents**: During merge, deduplicate by line number proximity (±3 lines) and category match — keep the entry with the more actionable fix description.
