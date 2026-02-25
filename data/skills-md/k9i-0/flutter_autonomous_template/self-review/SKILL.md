---
name: self-review
description: Self-review before completing tasks. Multi-perspective verification using Gemini CLI + Claude subagent.
---

# Self Review Skill

Execute this self-review procedure before marking tasks as completed (TodoWrite completed).

## Trigger Conditions

Apply this skill when:
- Just before marking a task as `completed` with TodoWrite
- When explicitly invoked by the user with `/self-review` command

## Review Procedure

### Phase 1: Collect Change Diffs

```bash
# List of changed files
git diff --name-only HEAD

# Get change contents
git diff HEAD
```

### Phase 2: Gemini CLI Review (External Model Perspective)

Execute Gemini CLI review on changed Dart files:

```bash
git diff HEAD -- "*.dart" | gemini -p "
Please review the following code changes.

## Review Points (Check All)

### 1. Code Quality
- Readability (is it easy to understand?)
- Naming (appropriate variable/function names)
- Structure (proper separation of concerns)

### 2. Bugs & Errors
- Null safety
- Edge cases
- Exception handling
- Memory leaks

### 3. Design Patterns
- Architecture consistency
- Appropriate dependencies
- Duplicate code

## Output Format
- Critical issues: [file:line] [description and fix suggestion]
- Minor issues: [file:line] [description]
- No issues: 'LGTM'
"
```

### Phase 3: Claude Subagent Review (Different Context Perspective)

Launch a review agent in a separate context using Task tool:

```
subagent_type: general-purpose

Prompt example:
---
Please review the following code changes.

## Changed Files
[Result of git diff --name-only HEAD]

## Change Contents
[Result of git diff HEAD]

## Review Points (Check All)

### Common Points
1. Code quality (readability, naming, structure)
2. Bugs & errors (null safety, edge cases, exception handling, memory leaks)
3. Design patterns (architecture consistency, dependencies, duplicate code)

### Project-Specific Points
4. Naming conventions (files: snake_case, classes: PascalCase, variables/functions: camelCase)
5. Architecture patterns (features/*/data/models/, repositories/, providers/, ui/)
6. Flutter-specific (Semantics support, Riverpod AsyncNotifier usage)

## Output Format
- Critical issues: [file:line] [description and fix suggestion]
- Minor issues: [file:line] [description]
- No issues: 'LGTM'
---
```

### Phase 4: Result Integration & Comparison

Integrate both review results and make judgment:

| Judgment | Condition | Action |
|----------|-----------|--------|
| PASS | Both LGTM | Task can be completed |
| MINOR | Only minor issues | Show warning, then task can be completed |
| FAIL | Critical issues found | Add fix tasks, re-review required |

### Phase 5: Feedback Loop

If FAIL judgment:
1. Fix the problem areas
2. Re-execute Phase 1-4
3. Repeat until PASS

## Review Point Checklist

### Code Quality

- [ ] Functions follow single responsibility principle
- [ ] Appropriate error handling exists
- [ ] Comments are minimal and clear
- [ ] Magic numbers are defined as constants

### Bugs & Errors

- [ ] Safe handling of nullable types
- [ ] Error handling for async operations
- [ ] Proper resource cleanup (dispose)
- [ ] Consideration of boundary values and edge cases

### Design Patterns

- [ ] Follows project structure
- [ ] Utilizes existing utilities/helpers
- [ ] No duplicate code
- [ ] Design is testable

### Project-Specific

- [ ] File names: snake_case
- [ ] Class names: PascalCase
- [ ] Variables/functions: camelCase
- [ ] Semantics support (for E2E testing)
- [ ] Appropriate use of Riverpod AsyncNotifier

## Output Template

```markdown
## Self Review Result

### Gemini Review (External Model)
[Output from Gemini]

### Claude Subagent Review (Different Context)
[Output from subagent]

### Comparison Analysis
- Common issues: [Issues identified by both]
- Gemini-only issues: [Issues found only by Gemini]
- Subagent-only issues: [Issues found only by subagent]

### Judgment: [PASS/MINOR/FAIL]

#### Issues (if applicable)
- [ ] [file:line] [description]

#### Next Action
- [Complete task / Fix required]
```

## Adjustment by Change Size

If running full dual review for all tasks takes too long:

```bash
# Determine by number of changed lines
git diff --stat HEAD | tail -1
```

| Change Size | Lines (approx) | Review Method |
|-------------|----------------|---------------|
| Small | ~30 lines | Gemini CLI only (lightweight) |
| Medium | 31-100 lines | Dual review |
| Large | 100+ lines | Dual review + detailed analysis |
