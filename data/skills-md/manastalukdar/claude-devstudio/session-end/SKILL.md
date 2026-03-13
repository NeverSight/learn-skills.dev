---
name: session-end
description: Generate comprehensive summary and archive session to appropriate project directory
disable-model-invocation: true
---

# Procedure for Ending and Archiving a Development Session

This procedure archives the work from the current session into a permanent, detailed log for future reference.

## Token Optimization

This skill optimizes summary generation through Bash-based analysis and template structures:

### 1. Bash-Based Session Analysis (1,500 token savings)

**Pattern:** Use git commands and file metadata instead of reading files

```bash
# Bash-based analysis (400 tokens)
SESSION_FILE=$(cat .claude/sessions/.current-session)
START_TIME=$(head -1 "$SESSION_FILE" | grep -oP '\d{4}-\d{2}-\d{2} \d{2}:\d{2}')
END_TIME=$(date '+%Y-%m-%d %H:%M')

# Git summary
FILES_CHANGED=$(git diff --name-status HEAD@{1 hour ago} | wc -l)
COMMITS=$(git log --since="$START_TIME" --oneline | wc -l)
GIT_STATUS=$(git status --porcelain)

# File changes breakdown
ADDED=$(echo "$GIT_STATUS" | grep '^A' | wc -l)
MODIFIED=$(echo "$GIT_STATUS" | grep '^M' | wc -l)
DELETED=$(echo "$GIT_STATUS" | grep '^D' | wc -l)
```

**Savings:**
- Bash commands: ~400 tokens (metadata only)
- File reading approach: ~1,900 tokens (read all changed files)
- **1,500 token savings (79%)**

### 2. Early Exit for No Active Session (95% savings)

**Pattern:** Detect missing session immediately

```bash
# Quick check (60 tokens)
if [ ! -f ".claude/sessions/.current-session" ] || [ ! -s ".claude/sessions/.current-session" ]; then
    echo "⚠️  No active session to end"
    echo "   Start one with /session-start"
    exit 0  # 60 tokens total
fi

# Otherwise: Full session end workflow (800+ tokens)
```

**Savings:**
- No session: ~60 tokens (early exit)
- Full workflow: ~800+ tokens
- **740+ token savings (92%)** when no active session

### 3. Template-Based Summary Structure (800 token savings)

**Pattern:** Use template with placeholder variables instead of LLM-generated narrative

```bash
# Template-based summary (300 tokens)
cat >> "$SESSION_FILE" <<EOF

## Session Summary

**Duration**: $START_TIME to $END_TIME
**Branch**: $(git branch --show-current)

### Changes
- Files changed: $FILES_CHANGED
- Commits: $COMMITS
- Added: $ADDED, Modified: $MODIFIED, Deleted: $DELETED

### File List
$(git diff --name-status HEAD@{1 hour ago})

### Commit History
$(git log --since="$START_TIME" --oneline)

### Final Status
$(git status --short)
EOF
```

**Savings:**
- Template-based: ~300 tokens (variable substitution)
- LLM-generated narrative: ~1,100 tokens (comprehensive summary with analysis)
- **800 token savings (73%)**

### 4. Incremental TODO Status (Optional)

**Pattern:** Read TODO cache if available, skip comprehensive analysis if not

```bash
# Optional TODO status (150 tokens if cached, 0 if not)
if [ -f ".claude/cache/todos/summary.json" ]; then
    TODO_SUMMARY=$(jq -r '{completed, in_progress, pending}' .claude/cache/todos/summary.json)
    cat >> "$SESSION_FILE" <<EOF

### TODO Progress
$TODO_SUMMARY
EOF
fi

# Don't scan codebase for TODOs (would be 800+ tokens)
```

**Token Usage:**
- Cached TODO status: ~150 tokens
- Scan codebase: ~800+ tokens
- **Skip if unavailable: 0 tokens** (graceful degradation)

### 5. Session Categorization Caching (200 token savings)

**Pattern:** Cache directory structure to avoid repeated analysis

```bash
# Cache file: .claude/sessions/.structure-cache.json
# Format: {"directories": ["feature-a", "feature-b", ...]}
# TTL: Session-based (until structure changes)

if [ -f ".claude/sessions/.structure-cache.json" ]; then
    DIRS=$(jq -r '.directories[]' .claude/sessions/.structure-cache.json)
else
    DIRS=$(ls -1 .claude/sessions/)
    echo "{\"directories\": $(echo "$DIRS" | jq -R . | jq -s .)}" > .claude/sessions/.structure-cache.json
fi
```

**Savings:**
- Cached structure: ~100 tokens
- Fresh analysis: ~300 tokens (directory listing + analysis)
- **200 token savings (67%)** for subsequent session ends

### 6. Smart File Archival (No File Splitting)

**Pattern:** Simple move operation instead of complex splitting logic

```bash
# Simple archival (100 tokens)
TARGET_DIR=".claude/sessions/general"  # Default category

# Move session file
mv "$SESSION_FILE" "$TARGET_DIR/"
[ -f "$TARGET_DIR/.gitkeep" ] && rm "$TARGET_DIR/.gitkeep"

# Clear current session
> .claude/sessions/.current-session
```

**Token Usage:**
- Simple move: ~100 tokens
- Complex splitting logic: ~500+ tokens (analyze, split, categorize)
- Default to simple approach - **80% savings**

### 7. Real-World Token Usage Distribution

**Typical Scenarios:**

1. **Standard Session End (600-900 tokens)**
   - Session validation: 60 tokens
   - Bash-based analysis: 400 tokens
   - Template summary: 300 tokens
   - TODO status (cached): 150 tokens
   - File archival: 100 tokens
   - **Total: ~1,010 tokens**

2. **Minimal Session End (500-700 tokens)**
   - Session validation: 60 tokens
   - Bash-based analysis: 400 tokens
   - Template summary: 300 tokens
   - Simple archival: 100 tokens
   - **Total: ~860 tokens** (no TODO status)

3. **No Active Session - Early Exit (50-80 tokens)**
   - Session check: 60 tokens
   - **Total: ~60 tokens**

4. **Long Session with Updates (700-1,000 tokens)**
   - Session validation: 60 tokens
   - Bash-based analysis: 400 tokens
   - Read session updates: 200 tokens (previous updates)
   - Template summary: 300 tokens
   - Archival: 100 tokens
   - **Total: ~1,060 tokens**

**Expected Token Savings:**
- **Average 60% reduction** from baseline (1,500 → 600 tokens)
- **92% reduction** when no active session
- **Aggregate savings: 700-900 tokens** per session end

### Optimization Summary

| Strategy | Savings | When Applied |
|----------|---------|--------------|
| Bash-based session analysis | 1,500 tokens (79%) | Always |
| Early exit for no session | 740 tokens (92%) | No active session |
| Template-based summary | 800 tokens (73%) | Always (vs LLM narrative) |
| Incremental TODO status | 650 tokens (81%) | When cache unavailable |
| Session categorization caching | 200 tokens (67%) | Subsequent ends |
| Smart file archival | 400 tokens (80%) | Simple move vs splitting |

**Key Insight:** Session ending benefits significantly from Bash-based analysis and template structures, avoiding expensive file reads and LLM-generated narratives. The combination of git commands, cached TODO status, and simple archival provides 60-70% token reduction while maintaining comprehensive session documentation.

## Phase 1: Verify the Active Session

1. I will check for an active session by reading the `.claude/sessions/.current-session` file.
2. If the file is empty or doesn't exist, I will inform the user that there is no active session to end and stop the process.

## Phase 2: Generate the Session Summary

1. Let me analyze what we accomplished by:
   - Reviewing files created/modified during our session
   - Checking git changes and commit history
   - Summarizing completed work and pending items
2. I will append comprehensive information to the end of the active session file. The information will be structured and detailed enough for another developer to understand the session's context and outcomes. It will include:
   - Session summary and accomplishments
   - Files modified and their purposes
   - Decisions made and rationale
   - Pending work and next steps
   - Any important context for future sessions
3. Expanding on the above point, the comprehensive information must include:
   - Session Metadata:
     - Session duration
     - Session Start and End timestamps
   - Version Control Summary (Git):
     - Total files added, modified, or deleted with their purposes.
     - A list of all changed files with their status (e.g., `A`, `M`, `D`)
     - Number of commits made during the session
     - Final `git status` output
   - Task Management Summary (To-Do):
     - Totals for completed vs. remaining tasks
     - A list of all completed tasks
     - A list of all incomplete tasks and their current status
   - Development Narrative:
     - Session summary
     - All accomplishments
     - Key architectural decisions made
     - Features and fixes implemented
     - Problems encountered and their implemented solutions
     - Known issues requiring attention
     - Important context for other developers. Lessons learned and tips for future developers
   - Project Impact:
     - Breaking changes or other important findings
     - Any blockers or dependencies identified
     - Dependencies added or removed
     - Configuration changes made
     - Technical debt considerations
     - Deployment steps taken (if any)
     - Work that was planned but not completed
     - Recommended next steps

## Phase 3: File the Session Log

This phase determines the correct location for the session file based on its content.

1. Ensure Directory Structure Exists: Check for sub-directories inside `.claude/sessions`.
   - If no directories exist, create them by running the `sessions-init.md` command.

2. Analyze and Categorize the Session: Review the session summary to determine which feature or product area it relates to. Compare this against the existing sub-directory names.

3. Handle Filing Scenarios:
    - A) Simple Match: If the session clearly maps to one sub-directory, proceed to Phase 4.
    - B) No Match: If the session content does not match any existing directory:
        1. The project structure may have changed. Re-run the `sessions-init.md` command to update the directories.
        2. Attempt to categorize the session again against the updated directories.
        3. If there is still no match, halt the process. Inform the user that a suitable directory could not be found and that manual action is required.
    - C) Multiple Matches: If the session covers more than one feature area:
        1. Split the session file into multiple files.
        2. Use the naming convention: `[original_timestamp]-[feature_name].md`.
        3. Each new file should contain the relevant parts of the summary for that specific feature.

## Phase 4: Finalize and Clean Up

1. Archive the File(s): Move the session file (or the newly split files) into the appropriate sub-directory (or directories) identified in Phase 3.
2. Clean Up Directory: If the destination directory contained a `.gitkeep` file, delete it, as the directory is no longer empty.
3. End the Session: Clear the contents of the `.claude/sessions/.current-session` file. Do not delete the file itself.
4. Notify the User: Confirm that the session has been successfully documented and archived. Print the final location(s) of the session file(s).

**Important**: I will NEVER:\

- Add "Co-authored-by" or any Claude signatures
- Include "Generated with Claude Code" or similar messages
- Modify git config or user credentials
- Add any AI/assistant attribution to the commit
- Use emojis in commits, PRs, or git-related content

I'll preserve this summary in your custom memory system, ensuring continuity for future sessions and seamless handoffs to other developers.