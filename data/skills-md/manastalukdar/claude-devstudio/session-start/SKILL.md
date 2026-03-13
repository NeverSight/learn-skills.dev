---
name: session-start
description: Begin documented development session using Claude Code CLI's memory system
disable-model-invocation: true
---

# Start Development Session

I'll begin a documented coding session using Claude Code CLI's memory system.

## Token Optimization

This skill is inherently efficient due to its simple file creation workflow:

### 1. Minimal File Operations (Already Optimized)

**Pattern:** Simple file creation with template structure

```bash
# Create session file (150 tokens)
SESSION_NAME="${ARGUMENTS:-$(date +%Y-%m-%d-%H%M)}"
mkdir -p .claude/sessions
echo "# $SESSION_NAME - $(date)" > ".claude/sessions/$SESSION_NAME.md"
echo ".claude/sessions/$SESSION_NAME.md" > ".claude/sessions/.current-session"
```

**Token Usage:**
- Directory creation: ~30 tokens
- Session file write: ~80 tokens
- Current session tracking: ~40 tokens
- **Total: ~150 tokens** (no optimization needed)

### 2. Early Exit for Existing Session (85% savings)

**Pattern:** Detect active session before creating new one

```bash
# Quick check (50 tokens)
if [ -f ".claude/sessions/.current-session" ]; then
    CURRENT=$(cat ".claude/sessions/.current-session")
    if [ -f "$CURRENT" ]; then
        echo "⚠️  Active session already exists: $CURRENT"
        echo "   End it first with /session-end or use /session-current to view"
        exit 0  # 150 tokens total vs 300 tokens for duplicate creation
    fi
fi
```

**Savings:**
- Existing session: ~150 tokens (early exit)
- Duplicate creation: ~300 tokens (conflict handling)
- **150 token savings (50%)** when session active

### 3. Template-Based Session File (No LLM Generation)

**Pattern:** Use fixed template structure instead of generating content

```bash
# Template-based (100 tokens)
cat > ".claude/sessions/$SESSION_NAME.md" <<EOF
# Development Session: $SESSION_NAME

**Started:** $(date)
**Branch:** $(git branch --show-current 2>/dev/null || echo "N/A")

## Goals
- $ARGUMENTS

## Progress
<!-- Updates added via /session-update -->

## Git Status
$(git status --short 2>/dev/null | head -5 || echo "Not a git repository")
EOF
```

**Token Usage:**
- Template structure: ~100 tokens (no LLM generation)
- Alternative (LLM): ~500+ tokens (custom session structure)
- Already optimized - **80% savings vs LLM approach**

### 4. Real-World Token Usage Distribution

**Typical Scenarios:**

1. **First Session Start (150-250 tokens)**
   - Directory check/creation: 30 tokens
   - Session file write: 100 tokens
   - Git status check: 50 tokens
   - Current session tracking: 40 tokens
   - **Total: ~220 tokens**

2. **Session Exists - Early Exit (100-150 tokens)**
   - Active session check: 50 tokens
   - Warning message: 50 tokens
   - **Total: ~100 tokens**

3. **With User Questions (300-400 tokens)**
   - Session creation: 220 tokens
   - User questions (goals/context): 150 tokens
   - **Total: ~370 tokens**

**Expected Token Usage:**
- **Baseline: 150-250 tokens** (already efficient)
- **Early exit: 100-150 tokens** (50% savings)
- **Average: ~200 tokens** (minimal overhead)

### Optimization Summary

| Strategy | Savings | When Applied |
|----------|---------|--------------|
| Minimal file operations | N/A | Already optimized |
| Early exit for active session | 150 tokens (50%) | Session already active |
| Template-based structure | 400 tokens (80%) | Always (vs LLM generation) |

**Key Insight:** This skill is already near-optimal at ~200 tokens due to its simple file creation workflow. The primary optimization is the early exit pattern when a session is already active, saving 50% tokens. No LLM generation is used - all content is template-based.

I'll integrate with the native memory system by creating a session file in `.claude/sessions/` with the format `YYYY-MM-DD-HHMM-$ARGUMENTS.md` (or just `YYYY-MM-DD-HHMM.md` if no name provided). If the local `./claude` or `.claude/sessions/` directories do not exist, I will create them first.

The session file should begin with:

1. Session name and timestamp as the title
2. Session overview section with start time and context
3. Current git state and branch
4. Goals and objectives section (ask user if not clear)
5. Empty progress section ready for updates to be tracked throughout the session

After creating the file, I will create or update `.claude/sessions/.current-session` to track the active session filename.

Please tell me:

1. What are we working on today?
2. What specific goals do you want to accomplish?
3. Any context I should know about?

I'll add this session context to the newly created session file, as detailed above, ensuring our progress is tracked and can be resumed later. Keep in mind this is slighly different from Claude Code CLI's native memory management that uses the local and/or global CLAUDE.md files. We use this other approach to keep the CLAUDE.md files lean.

**Important**: I will NEVER:

- Add "Co-authored-by" or any Claude signatures
- Include "Generated with Claude Code" or similar messages
- Modify git config or user credentials
- Add any AI/assistant attribution to the commit

The session context will be preserved in the appropriate session file for reference and continuation until the session is ended.

Finally I will confirm the session has started and remind the user they can:

- Update it with `/project:session-update`
- End it with `/project:session-end`