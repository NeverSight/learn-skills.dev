---
name: token-saver
description: Automatically delegates routine coding tasks to free AI models (GLM, GitHub Copilot, and others) via OpenCode MCP, preserving Claude's context window and rate limits for complex reasoning. Use when generating boilerplate, CRUD operations, simple refactoring, test scaffolding, documentation, type definitions, or any well-defined low-judgment task. Triggers automatically when Claude recognizes routine patterns.
---

# Token Saver

Offload routine tasks to free models. Save Claude for complex reasoning.

## Automatic Delegation Rules

**DELEGATE** (routine, well-defined):
- Boilerplate code generation
- TypeScript/Python interfaces and types
- CRUD operations and database models
- Simple data validation (Zod schemas, validators)
- Test scaffolding and fixtures
- Code formatting and style cleanup
- Docstrings and inline comments
- README sections and documentation
- Repetitive refactoring (early returns, destructuring)
- Form field mappings
- Standard API endpoint scaffolding

**KEEP IN CLAUDE** (requires judgment):
- Architectural decisions
- Security-sensitive code
- Complex business logic
- Error handling strategy
- Performance optimization
- Code review and analysis
- Debugging and root cause analysis
- Domain-specific logic requiring context
- Anything touching auth, payments, PII

## How to Delegate

1. **Identify routine task** — Match against delegation rules above
2. **Gather context** — Read relevant files if needed
3. **Invoke OpenCode** — Use configured free model
4. **Validate output** — Check for correctness before using
5. **Apply or return** — Write to file or pass back to conversation

### Invocation Pattern

```bash
# Basic invocation
opencode run --model <model-name> "<prompt>"

# With file context
opencode run --model <model-name> "$(cat src/types.ts)" "<prompt>"

# Recommended free models
opencode run --model glm/glm-4 "<prompt>"
opencode run --model github-copilot/gpt-4.1 "<prompt>"
```

### Example Delegations

**Generate TypeScript interface:**
```bash
opencode run --model glm/glm-4 "Generate TypeScript interface for a User with id, email, name, createdAt, updatedAt fields"
```

**Create Zod schema:**
```bash
opencode run --model glm/glm-4 "Create Zod validation schema for email, password (min 8 chars), and optional phone number"
```

**Refactor to early returns:**
```bash
opencode run --model github-copilot/gpt-4.1 "Refactor this function to use early returns: $(cat src/utils/validate.ts)"
```

**Generate test fixtures:**
```bash
opencode run --model glm/glm-4 "Generate 5 test fixtures for User objects with realistic fake data"
```

## Model Selection

Choose model based on task:

| Task Type | Recommended Model | Why |
|-----------|------------------|-----|
| TypeScript/JS | github-copilot/gpt-4.1 | Strong TS inference |
| Python | glm/glm-4 | Good Python patterns |
| Documentation | glm/glm-4 | Natural language strength |
| General boilerplate | Any free model | All handle well |

See [model-capabilities.md](references/model-capabilities.md) for detailed comparison.

## Configuration

Requires OpenCode MCP server. See [mcp-config-template.json](references/mcp-config-template.json) for setup.

## Fallback Chain

If primary model fails:
1. Try next model in configured list
2. If all fail, escalate back to Claude
3. Log failure for debugging

## Validation Checklist

Before using delegated output:
- [ ] Syntax is correct (no obvious errors)
- [ ] Types are accurate (if TypeScript)
- [ ] Follows project conventions
- [ ] No security issues introduced
- [ ] Imports are correct

## When NOT to Delegate

Stop and keep in Claude if task involves:
- Decisions about *what* to build (not just *how*)
- Security boundaries or auth logic
- Complex conditional logic
- Domain-specific business rules
- Code that touches sensitive data
- Anything you'd want a senior engineer to review
