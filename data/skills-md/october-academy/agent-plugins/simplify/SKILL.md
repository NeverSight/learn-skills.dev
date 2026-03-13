---
name: simplify
description: Simplify and refine code for clarity, consistency, and maintainability
user-invocable: true
argument-hint: [file or scope]
---

# Code Simplification Skill

Multi-agent code analysis and simplification workflow.

## Execution Flow

```
┌─────────────────────────────────────────────────────────┐
│  1. Determine Scope (git diff or user input)            │
├─────────────────────────────────────────────────────────┤
│  2. Phase 1: 4 Analysis Agents (Parallel)               │
│     ┌─────────────────┬─────────────────┐               │
│     │  complexity-    │  pattern-       │               │
│     │  analyzer       │  checker        │               │
│     ├─────────────────┼─────────────────┤               │
│     │  naming-        │  readability-   │               │
│     │  reviewer       │  analyzer       │               │
│     └─────────────────┴─────────────────┘               │
├─────────────────────────────────────────────────────────┤
│  3. Consolidate Issues                                  │
├─────────────────────────────────────────────────────────┤
│  4. Phase 2: Issue Simplifiers (Parallel)               │
│     ┌────────┬────────┬────────┬────────┐               │
│     │ issue1 │ issue2 │ issue3 │ ...    │               │
│     └────────┴────────┴────────┴────────┘               │
├─────────────────────────────────────────────────────────┤
│  5. Present Changes & AskUserQuestion                   │
├─────────────────────────────────────────────────────────┤
│  6. Apply Selected Changes                              │
└─────────────────────────────────────────────────────────┘
```

## Step 1: Determine Scope

### With Arguments

Use provided file/directory path as scope.

### Without Arguments (Recent Changes)

```bash
git diff --name-only HEAD~3 2>/dev/null | grep -E '\.(ts|tsx|js|jsx|py|go|rs|java)$'
```

If no git changes, ask user for scope.

## Step 2: Phase 1 - Analysis Agents (Parallel)

Execute 4 agents in parallel (single message with 4 Task calls).

### Scope Context (Provide to all agents)

```
Scope:
- Files: [List of files to analyze]
- Recent changes: [git diff summary if available]
```

### Parallel Execution

```
Task(subagent_type="simplify:complexity-analyzer", ...)
Task(subagent_type="simplify:pattern-checker", ...)
Task(subagent_type="simplify:naming-reviewer", ...)
Task(subagent_type="simplify:readability-analyzer", ...)
```

| Agent | Role | Output |
|-------|------|--------|
| **complexity-analyzer** | Nested ternary, deep nesting, over-abstraction | Issue list with locations |
| **pattern-checker** | Project standards violation, inconsistency | Issue list with locations |
| **naming-reviewer** | Variable/function naming improvements | Issue list with suggestions |
| **readability-analyzer** | Readability issues, unnecessary comments | Issue list with suggestions |

## Step 3: Consolidate Issues

Merge results from all 4 agents into a unified issue list:

```markdown
## Issues Found

### Issue 1: [Title]
- **File:** path/to/file.ts:42
- **Type:** complexity | pattern | naming | readability
- **Description:** [What's wrong]
- **Suggestion:** [How to fix]

### Issue 2: [Title]
...
```

If no issues found, report "No improvements needed" and end.

## Step 4: Phase 2 - Issue Simplifiers (Parallel)

For each issue, run an issue-simplifier agent in parallel:

```
Task(subagent_type="simplify:issue-simplifier", prompt="""
Issue: [Issue title]
File: [file path]
Location: [line numbers]
Type: [issue type]
Description: [description]
Suggestion: [suggestion]

Read the file and provide the exact code change needed.
Output format:
- Original code block
- Simplified code block
- Brief explanation
""")
```

**IMPORTANT:** Run ALL issue-simplifier agents in a single message with multiple Task calls.

## Step 5: Present Changes

Compile all proposed changes:

```markdown
## Proposed Simplifications

### 1. [File:Line] - [Issue Type]
**Original:**
```[lang]
[original code]
```

**Simplified:**
```[lang]
[simplified code]
```

**Reason:** [explanation]

---

### 2. [File:Line] - [Issue Type]
...
```

## Step 6: Action Selection

```
AskUserQuestion(
    questions=[{
        "question": "Which simplifications would you like to apply?",
        "header": "Apply",
        "multiSelect": true,
        "options": [
            {"label": "Apply all (Recommended)", "description": "Apply all proposed changes"},
            {"label": "Select individually", "description": "Choose specific changes"},
            {"label": "Skip", "description": "Don't apply any changes"}
        ]
    }]
)
```

If "Select individually", present each change for approval.

## Step 7: Apply Selected Changes

Use Edit tool to apply approved changes.

---

## Principles

- **Clarity over Brevity**: Explicit, readable code over compact one-liners
- **No Nested Ternaries**: Use switch/if-else for multiple conditions
- **Reduce Complexity**: Eliminate unnecessary nesting and redundant abstractions
- **Preserve Functionality**: Never change what code does, only how it's written

## Example Improvements

- Nested ternary operators → clear if/else chains
- Deep nesting → early returns or extracted functions
- Redundant abstractions → direct implementations
- Unclear names → descriptive identifiers
