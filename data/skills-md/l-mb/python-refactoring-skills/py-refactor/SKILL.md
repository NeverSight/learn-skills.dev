---
name: py-refactor
description: Orchestrate comprehensive Python refactoring - coordinates security, complexity, testing, code health, and modernization skills to systematically improve code quality.
status: stable
---

# Python Refactoring Orchestrator

Comprehensive refactoring workflow coordinating specialized skills to improve Python code quality.

## Overview

This skill orchestrates multiple focused skills to perform systematic refactoring:

| Skill | Purpose | Status |
|-------|---------|--------|
| `py-security` | Vulnerability detection and remediation | stable |
| `py-code-health` | Dead code and duplication removal | stable |
| `py-complexity` | Reduce cyclomatic/cognitive complexity | stable |
| `py-test-quality` | Coverage analysis and mutation testing | stable |
| `py-modernize` | Upgrade tooling and syntax | stable |
| `py-quality-setup` | Configure linters and type checkers | stable |
| `py-git-hooks` | Set up pre-commit hooks | stable |

## Refactoring Priorities

Follow this impact-based prioritization:

1. **Critical**: Security vulnerabilities (use `py-security`)
2. **High**: Code duplication, untested code (<80% coverage)
3. **Medium**: Complexity reduction, dead code removal
4. **Low**: Syntax modernization, style improvements

## Standard Refactoring Workflow

### Phase 1: Setup (if needed)

```
1. If quality tools not configured (pyproject.toml):
   → Invoke: py-quality-setup
   (also configures .claude/settings.local.json permissions for all tools)

2. Add analysis tools to [dependency-groups] dev in pyproject.toml:
   "radon", "vulture", "pylint", "bandit", "lizard",
   "pytest-cov", "mutmut", "wily", "ruff", "mypy", "basedpyright"

3. Install and activate:
   uv sync && source .venv/bin/activate
```

### Phase 2: Comprehensive Analysis

Run all automated scanners to get baseline:

```bash
mkdir -p reports

# Security
ruff check . --select S > reports/security.txt
bandit -r . -f json -o reports/security.json

# Code health
vulture . --min-confidence 80 > reports/dead_code.txt
pylint --disable=all --enable=duplicate-code --recursive=y . > reports/duplication.txt

# Complexity
radon cc . -n C -s > reports/complexity.txt
lizard -l python -w > reports/cognitive_complexity.txt
radon mi . -n B > reports/maintainability.txt

# Test quality
pytest --cov=. --cov-report=html --cov-report=term > reports/coverage.txt

# Initialize complexity tracking
wily build .
```

### Phase 3: Prioritized Remediation

**Step 1: Security (Critical)**
```
If security.txt shows issues:
→ Invoke: py-security
   - Fix SQL injection, hardcoded secrets, weak crypto
   - Verify: ruff check . --select S (clean)
   - Run tests to ensure no regressions
```

**Step 2: Test Quality (High - enables safe refactoring)**
```
If coverage < 80%:
→ Invoke: py-test-quality
   - Write tests for untested code
   - Run mutation testing to verify test quality
   - Target: ≥80% coverage, ≥75% mutation score
```

**Step 3: Code Health (High)**
```
If duplication.txt or dead_code.txt show issues:
→ Invoke: py-code-health
   - Remove dead code (vulture findings)
   - Consolidate duplicates (pylint findings)
   - Verify: Tests still pass, coverage maintained
```

**Step 4: Complexity Reduction (Medium)**
```
If complexity.txt shows C+ functions or maintainability < 65:
→ Invoke: py-complexity
   - Extract functions, simplify conditionals
   - Use guard clauses, lookup tables
   - Track improvement with wily
   - Verify: radon cc . -n C (clean)
```

**Step 5: Modernization (Optional)**
```
If project uses old patterns or pip:
→ Invoke: py-modernize
   - Migrate pip → uv
   - Upgrade syntax to Python 3.13+
   - Consolidate to pyproject.toml
   - Verify: Tests pass, type checking works
```

### Phase 4: Automation

```
Set up git hooks to prevent regressions:
→ Invoke: py-git-hooks
   - Pre-commit hooks run ruff, mypy, basedpyright
   - Optionally add security checks (bandit)
   - Test hook works correctly
```

### Phase 5: Final Validation

```bash
# Run complete validation suite
ruff check .
mypy . && basedpyright .
ruff check . --select S
radon cc . -n C
vulture . --min-confidence 80
pytest --cov=. --cov-fail-under=80

# Track overall improvement
wily diff HEAD~1
wily report .
```

## When NOT to Use This Skill

Don't use orchestrated refactoring when:

- **Single focused task**: Use specific skill directly (e.g., just py-security for CVE fix)
- **No tests exist**: Write tests first (py-test-quality), then refactor
- **Active development**: Coordinate with team to avoid merge conflicts
- **Production incident**: Fix incident first, refactor later

## Additional Resources

- **WORKFLOWS.md**: Quick workflows for specific scenarios (security sweep, complexity sprint, legacy modernization)
- **METRICS.md**: Success metrics, tool reference, Engineering Charter alignment
