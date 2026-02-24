---
name: review-package
description: >
  Create a self-contained review package of current work for external review by another AI model
  or human reviewer. Bundles relevant files with a contextual README and instructional prompt.
  Triggers: "review package", "create review package", "hand off for review", "get a second opinion",
  "external code review", "cross-model review", "package for review", "prepare code review".
  Accepts an optional focus area argument to scope the analysis.
---

# Review Package Creator

Bundle current work into a self-contained zip with a contextual README and review prompt, ready to hand off to any external reviewer.

## Phase 1: Gather Requirements

Ask the user two questions using AskUserQuestion:

**Question 1: Review Type**
- Header: "Review type"
- Question: "What type of review do you need?"
- Options:
  1. **Code review** — Line-by-line feedback on implementation, bugs, edge cases, best practices
  2. **Architecture review** — High-level feedback on patterns, structure, design decisions
  3. **Both** — Comprehensive review covering code and architecture

**Question 2: Specific Concerns**
- Header: "Focus areas"
- Question: "Any specific concerns you want the reviewer to address?"
- multiSelect: true
- Options:
  1. **General review** — No specific focus, broad feedback welcome
  2. **Performance** — Efficiency, optimization opportunities
  3. **Security** — Vulnerabilities, input validation, auth patterns
  4. **Maintainability** — Code clarity, complexity, future extensibility

Wait for responses before proceeding.

## Phase 2: Analyze Codebase

Spawn the analyzer agent:

- **subagent_type**: `review-package-analyzer`
- **prompt**: Include focus area ($ARGUMENTS or "current work"), review type from Phase 1, and project root (cwd).

Wait for the agent to return its structured analysis.

## Phase 3: Generate README

Generate a unique suffix for temp files (e.g., timestamp: `date +%s`). Use this for all temp paths in subsequent phases.

Read `references/readme-guide.md` for structure guidelines. Write the README to `/tmp/review-readme-{suffix}.md`.

Adapt the README to the project — don't fill in a rigid template mechanically. The guide provides the sections and priorities; use judgment about what to emphasize based on the review type and analysis results.

## Phase 4: Create File List

Extract all file paths from the analysis (Core, Related, Tests, Config). Write one path per line to `/tmp/review-filelist-{suffix}.txt`.

## Phase 5: Create Package

Locate the packaging script:
```bash
find ~/.claude -path "*/review-package/scripts/create-review-zip.sh" -type f 2>/dev/null | head -1
```

Run it:
```bash
/path/to/create-review-zip.sh \
  "$(pwd)" \
  "/tmp/review-readme-{suffix}.md" \
  "/tmp/review-filelist-{suffix}.txt" \
  "review-package-$(date +%Y%m%d-%H%M%S)"
```

## Phase 6: Generate Instructional Prompt

Read `references/prompt-guide.md` for the template. Customize based on review type, focus areas, and concerns from the analysis.

Write to `/tmp/review-prompt-{suffix}.md` and copy to clipboard:
```bash
cat /tmp/review-prompt-{suffix}.md | pbcopy
```

## Phase 7: Report

Tell the user: zip location, file counts (core/related/tests), display the instructional prompt inline, and list next steps (open a new chat with any AI model, paste prompt, upload zip). Mention the prompt is on the clipboard and saved to the temp path.

Clean up temp files (keep the prompt file):
```bash
rm -f /tmp/review-readme-{suffix}.md /tmp/review-filelist-{suffix}.txt
```

## Notes

- If $ARGUMENTS is empty, the analyzer auto-detects current work from git status and recent changes
- For non-git projects, the analyzer falls back to recently-modified files
- The package is self-contained — the reviewer needs no other context
- Files are copied with directory structure preserved
- Binary files and build artifacts are excluded automatically
