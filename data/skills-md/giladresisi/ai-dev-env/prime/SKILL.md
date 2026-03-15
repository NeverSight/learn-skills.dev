---
name: prime
description: Use when loading project context and architecture overview before starting implementation work, with optional focus on a specific area
---

# Prime: Load Project Context

## Objective

Build understanding of the codebase - either high-level overview or focused deep-dive based on whether a focus area argument is provided.

## Usage

- `/prime` - High-level overview (architecture, patterns, structure)
- `/prime "authentication system"` - Deep-dive into specific area
- `/prime "API endpoints"` - Focus on particular functionality

## Decision: Which Mode?

**Check if focus area argument was provided:**
- Arguments provided → Use **FOCUSED mode**
- No arguments → Use **HIGH-LEVEL mode**

---

## HIGH-LEVEL Mode (No Arguments)

**Goal:** Understand architecture, patterns, and structure with minimal token usage.

### Step 1: Directory Structure

Use Bash to show directory tree (2 levels max):
```bash
tree -L 2 -I 'node_modules|__pycache__|.git|dist|build|.next|coverage|venv|.venv'
```

If tree not available, use ls or alternative.

### Step 2: Count Files (Optional)

Only if in a git repo:
```bash
git ls-files | wc -l
```

### Step 3: Read Minimal Documentation

**Read at most 3 files:**
1. Root README.md (if exists)
2. CLAUDE.md or .claude/config (if exists)
3. One config file: package.json OR pyproject.toml OR tsconfig.json OR Cargo.toml

**DO NOT read:**
- Implementation files (src/, lib/, etc.)
- Test files
- Subdirectory READMEs
- Multiple config files

### Step 4: Check Git State (If Git Repo)

```bash
git status
git log -10 --oneline
```

### Step 5: Internalize Context

Build mental model of the project:
- Purpose and type of application (from README)
- Primary technologies and frameworks (from config)
- Directory structure and organization
- Key directories and their likely purposes (inferred from names)
- Main architectural patterns (if obvious from structure)

**DO NOT output this to CLI.** Keep context in memory for answering questions.

### Step 6: Output Completion

Output only:
```
Finished priming project.
```

No detailed report. Context is loaded and ready for use.

---

## FOCUSED Mode (With Argument)

**Goal:** Deep understanding of a specific area, ignore everything else.

### Step 1: Extract Keywords

From the focus area argument, identify key search terms.

Example: "authentication system" → keywords: auth, authentication, login, session, user

### Step 2: Find Relevant Files

Use Grep to search for files containing focus keywords:
```bash
grep -r "keyword1\|keyword2" --files-with-matches --include="*.py" --include="*.ts" --include="*.js"
```

Or use Glob for pattern matching:
```bash
**/*auth*/**
**/*login*/**
```

### Step 3: Read All Relevant Files

- Read ALL files found in Step 2 that are directly related
- Read imported dependencies if critical to understanding
- Read related documentation
- Go deep into implementation details

**No limit on file reading in focused mode.**

### Step 4: Analyze for Structural Blockers

**Internalize understanding** (keep in memory, don't output):
- Key functions/classes/components
- Main data structures or types
- Entry points and exports
- Dependencies & integrations
- Patterns & conventions
- Testing approach

**Detect structural problems** that would block implementation:

**Inconsistent Patterns:**
- Mixed architectural styles (e.g., some files use MVC, others use different pattern)
- Inconsistent naming conventions across files in the focus area
- Multiple ways of doing the same thing with no clear standard

**Unclear Organization:**
- Files misplaced (e.g., business logic in UI components, or vice versa)
- Unclear module boundaries or responsibilities
- Circular dependencies or tangled imports
- Missing separation of concerns

**Implementation Blockers:**
- No clear entry point or hook for the requested feature
- Conflicting patterns that make it unclear which approach to follow
- Missing architectural foundation (e.g., no state management for feature that needs it)
- Unclear how focus area integrates with rest of system

### Step 5: Output Result

**If structural blockers found:**

Output detailed blocker report:
```
Finished priming. Found structural blockers for "[focus_area]":

**Inconsistent Patterns:**
- [Specific inconsistency with file examples]
- [Another inconsistency]

**Unclear Organization:**
- [Specific organizational issue with file examples]

**Implementation Blockers:**
- [Specific blocker that prevents implementation]

**Recommendation:** [Suggest refactoring or clarification needed before proceeding]
```

**If NO structural blockers found:**

Output only:
```
Finished priming focused on "[focus_area]".
```

**DO NOT output detailed reports to CLI unless blockers are found.** Context is loaded and ready for use.

---

## Tips

- **High-level mode** optimizes for minimal context usage - great for initial orientation
- **Focused mode** goes deep - use when planning work on a specific feature/area
- Focus arguments should be descriptive: "user authentication flow" not just "auth"
- Can run high-level first, then focused on specific areas as needed
