---
name: claude-code-workflow
description: Claude Code AI-assisted development workflow. Activate when discussing Claude Code usage, AI-assisted coding, prompting strategies, or Claude Code-specific patterns.
location: user
---

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

# Claude Code Workflow

Guidelines for effective AI-assisted development with Claude Code.

## Task Value Matrix

| Value | Task Type | Example |
|-------|-----------|---------|
| High | Boilerplate generation | CRUD endpoints, test scaffolding |
| High | Refactoring | Extract function, rename across files |
| High | Documentation | Docstrings, README updates |
| Medium | Bug investigation | Error analysis, log interpretation |
| Medium | Code review | Pattern suggestions, security review |
| Low | Novel architecture | Requires deep domain knowledge |
| Low | Ambiguous requirements | Needs human clarification |

---

## Workflow Patterns

### Explore-Plan-Code-Commit (EPCC)

The RECOMMENDED workflow for most development tasks:

1. **Explore**: Use Glob, Grep, Read to understand existing code
   - MUST understand context before making changes
   - SHOULD identify related files and dependencies
   - MAY use subagents for parallel exploration

2. **Plan**: Outline changes before implementation
   - SHOULD create TodoWrite items for multi-step tasks
   - MUST validate plan covers edge cases

3. **Code**: Implement changes incrementally
   - MUST run tests after each significant change
   - SHOULD use Edit over Write for existing files
   - SHALL NOT introduce breaking changes without tests

4. **Commit**: Create logical, atomic commits
   - MUST follow semantic commit conventions
   - SHALL NOT commit secrets or credentials

### Test-Driven Development with AI

```
1. Write failing test → 2. Implement minimum to pass → 3. Refactor → 4. Repeat
```
- MUST run tests between each step
- SHOULD use targeted test execution during development

### Spike-Then-Implement

For uncertain implementations: Create throwaway spike, validate, delete, implement properly with tests.

---

## Context Management

### Efficient Prompting

**MUST:** Provide specific file paths, include error messages verbatim, state expected vs actual behavior

**SHOULD:** Reference previous context, specify output format, include constraints upfront

**SHOULD NOT:** Repeat information in context, include unnecessary background, ask multiple unrelated questions

### Conversation Structure

```
[Initial Context] → [Specific Task] → [Iterative Refinement]
```
- SHOULD front-load critical information
- MUST NOT bury important constraints at end of message

### Context Window Optimization

- SHOULD use subagents for isolated subtasks
- MUST NOT paste entire files when snippets suffice

---

## Subagent vs Direct Tool Usage

### Use Subagents (Task tool) When:
- Parallel independent operations (multiple searches, test runs)
- Isolated subtasks not needing main conversation context
- Complex multi-step work (refactoring across many files)
- Risk isolation (exploratory changes that might fail)

### Use Direct Tools When:
- Sequential dependencies (each step depends on previous)
- Context continuity needed (building on recent conversation)
- Simple operations (single file read/edit)
- Immediate feedback required (interactive debugging)

| Scenario | Recommendation |
|----------|----------------|
| Search 5+ files for pattern | Subagent |
| Edit single file | Direct |
| Run tests + fix failures | Subagent |
| Explore unfamiliar codebase | Subagent |
| Implement planned changes | Direct |

---

## Model Selection

### Opus (Complex Reasoning)
SHOULD use for: Architecture decisions, complex debugging, multi-file refactoring, novel problem solving, security-sensitive code review

### Sonnet (Standard Tasks)
RECOMMENDED for: Routine code changes, test writing, documentation, code review, bug fixes with clear scope

### Haiku (Quick Operations)
MAY use for: Simple queries, syntax checking, format conversions, quick lookups, commit message generation

```
IF deep reasoning OR high-stakes: USE Opus
ELSE IF routine development: USE Sonnet
ELSE IF simple/quick: USE Haiku
```

---

## Quality Assurance

### Automated Validation

**MUST:** Test execution after changes, linting/formatting, type checking, security scanning

**SHOULD:** Coverage thresholds, performance benchmarks, integration tests

### Human Review Checkpoints

**REQUIRED:** Security-sensitive changes, production deployments, architecture modifications, public API changes

**RECOMMENDED:** Complex business logic, performance-critical code, external integrations

---

## Prompt Engineering for Code Tasks

### Specificity Patterns

**Effective:** "Refactor UserService in src/services/user.py to use dependency injection for database connection"

**Ineffective:** "Clean up the user code"

### Constraint Specification

MUST specify: Language/framework versions, performance requirements, backward compatibility, error handling

### Prompt Templates

**Bug Fix:**
```
File: [path] | Error: [exact message]
Expected: [behavior] | Actual: [behavior]
Relevant code: [snippet]
```

**Feature:**
```
Goal: [one sentence]
Criteria: [list] | Location: [file] | Constraints: [limits]
```

---

## Session Context Management

### Integration with Context Files

**CURRENT.md** - Active task state (SHOULD update when switching tasks, MUST reflect current focus)

**STATUS.md** - Project progress (SHOULD update at session end, MUST include blockers/next steps)

### Session Lifecycle

```
[Start] → [Load CURRENT.md] → [Work + TodoWrite] → [End] → [Update STATUS.md]
```

### Context Preservation
- MUST save context before long breaks
- SHOULD use /snapshot for complex multi-session work
- MAY use /pickup to resume efficiently

---

## Skill Activation Optimization

### Triggering Skills Efficiently
- MUST use specific keywords in descriptions
- SHOULD include file patterns for automatic activation
- MAY use manual invocation for specialized skills

### Skill Composition

Skills SHOULD be: Single-purpose, composable, self-contained

Skills MUST NOT: Conflict with others, duplicate core rules, exceed context budget

| Pattern | Trigger |
|---------|---------|
| File-based | `*.py`, `Dockerfile`, `package.json` |
| Directory-based | `.claude/`, `tests/`, `src/` |
| Content-based | Keywords in conversation |
| Command-based | `/skill-name` invocation |

---

## Anti-Patterns to Avoid

### Conversation Anti-Patterns
| Anti-Pattern | Better Approach |
|--------------|-----------------|
| Context dumping | Provide focused, relevant context |
| Vague requests | Specific, measurable goals |
| Premature optimization | MVP first, optimize with data |
| Ignoring errors | Address errors immediately |

### Tool Usage Anti-Patterns
| Anti-Pattern | Better Approach |
|--------------|-----------------|
| Bash for file ops | Use Read/Edit/Write tools |
| Write over Edit | Prefer Edit for existing files |
| Single-threaded search | Parallel subagent searches |
| Skipping Read | Always Read before Edit |

### Workflow Anti-Patterns
| Anti-Pattern | Better Approach |
|--------------|-----------------|
| Coding without tests | TDD or test-after minimum |
| Giant commits | Atomic, logical commits |
| Ignoring TodoWrite | Update status in real-time |

### Prompting Anti-Patterns
| Anti-Pattern | Better Approach |
|--------------|-----------------|
| "Make it better" | Define specific improvements |
| Assuming knowledge | Provide relevant background |
| Ignoring constraints | State constraints upfront |

---

## Quick Reference

### Effective Session
1. Start with clear goal
2. Load context (CURRENT.md)
3. Use EPCC workflow
4. Update TodoWrite in real-time
5. Run tests frequently
6. Save context before ending

### Model Selection
- **Opus**: Architecture, security, complex bugs
- **Sonnet**: Daily development, tests, docs
- **Haiku**: Quick queries, formatting

### Tool Selection
- **Read**: View file content
- **Edit**: Modify existing files
- **Write**: Create new files (rare)
- **Glob**: Find files by pattern
- **Grep**: Search file contents
- **Task**: Parallel/isolated work
- **Bash**: System operations only
