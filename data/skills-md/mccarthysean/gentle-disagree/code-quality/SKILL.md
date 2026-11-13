---
name: code-quality
description: Maintain code quality with Ruff for Python and ESLint/TypeScript for frontend. Run linters, fix issues, and ensure consistent formatting. Use when linting code, fixing style issues, or preparing to commit.
allowed-tools: [Bash, Read, Edit]
---

# Code Quality Skill

## Purpose
Maintain code quality and consistent formatting for the Gentle Disagree project.

## When to Use This Skill
- Before committing code
- Fixing linting errors
- Formatting code
- Code review preparation
- CI/CD failures

## Python (Backend)

### Ruff Linting
```bash
cd /home/sean/git_wsl/gentle-disagree/backend

# Check for issues
uv run ruff check .

# Auto-fix issues
uv run ruff check --fix .

# Format code
uv run ruff format .

# Check formatting without changes
uv run ruff format --check .

# Full lint and format
uv run ruff check --fix . && uv run ruff format .
```

### Python Best Practices
- Use type hints for function parameters and returns
- Follow PEP 8 style guidelines
- Use `from None` or `from err` when re-raising exceptions (B904)
- Remove unused variables (F841)
- Keep functions small and focused

### Example
```python
# ✅ Good - proper exception chaining
try:
    response = await client.post(url, json=data)
except httpx.TimeoutException:
    raise HTTPException(status_code=504, detail="Timeout") from None
except httpx.HTTPError as e:
    raise HTTPException(status_code=502, detail=str(e)) from e

# ❌ Bad - missing exception chaining
except httpx.TimeoutException:
    raise HTTPException(status_code=504, detail="Timeout")
```

## TypeScript (Frontend)

### TypeScript Build
```bash
cd /home/sean/git_wsl/gentle-disagree/frontend

# Quick type check
bun run typecheck

# Full build (includes all checks)
bun run build
```

### ESLint
```bash
cd /home/sean/git_wsl/gentle-disagree/frontend

# Check for issues
bun run lint

# Auto-fix issues (if configured)
bunx eslint . --fix
```

### TypeScript Best Practices
- Never use `any` or `unknown` types
- Use nullish coalescing (`??`) not OR (`||`)
- Use `const` over `let` when value doesn't change
- Avoid calling setState synchronously in useEffect
- Use lazy state initialization for synchronous data

### Example - State Initialization
```typescript
// ✅ Good - lazy initialization
const [sessions, setSessions] = useState<Session[]>(() => getSessions());

// ❌ Bad - useEffect with setState
const [sessions, setSessions] = useState<Session[]>([]);
useEffect(() => {
  setSessions(getSessions());  // Causes cascading renders
}, []);
```

### Example - Unused Variables
```typescript
// ✅ Good - no variable if not used
} catch {
  setError("Something went wrong");
}

// ❌ Bad - unused error variable
} catch (error) {
  setError("Something went wrong");
}
```

## Pre-Commit Checklist

### Full Quality Check
```bash
# Backend
cd /home/sean/git_wsl/gentle-disagree/backend
uv run ruff check --fix .
uv run ruff format .

# Frontend
cd /home/sean/git_wsl/gentle-disagree/frontend
bun run lint
bun run typecheck
bun run build
```

### Quick Check (CI simulation)
```bash
# Backend
cd /home/sean/git_wsl/gentle-disagree/backend
uv run ruff check .
uv run ruff format --check .

# Frontend
cd /home/sean/git_wsl/gentle-disagree/frontend
bun run lint
bun run build
```

## Common Issues

### Python

#### Exception Chaining (B904)
When re-raising exceptions in except blocks:
```python
# Always use 'from None' or 'from err'
except SomeError:
    raise NewError("message") from None  # Suppresses original traceback
except SomeError as e:
    raise NewError("message") from e  # Preserves exception chain
```

#### Unused Variables (F841)
```python
# ❌ Bad
except Exception as e:  # 'e' never used
    return default_value

# ✅ Good
except Exception:
    return default_value
```

### TypeScript

#### React Hooks - setState in useEffect
This is a React 19 lint rule. For synchronous data (like localStorage):
```typescript
// Use lazy initialization instead of useEffect
const [data, setData] = useState(() => loadFromStorage());
```

#### Null/Undefined Handling
```typescript
// ❌ Using || can cause issues with falsy values
const value = data.count || 0;  // Returns 0 if count is 0

// ✅ Use nullish coalescing
const value = data.count ?? 0;  // Only returns 0 if null/undefined
```

## Integration
This skill automatically activates when:
- Running linters
- Fixing code style issues
- Preparing to commit code
- CI/CD check failures
- Code review
