---
name: py-test-quality
description: Measure and improve test coverage and test suite quality using code coverage and mutation testing. Ensures tests actually catch bugs.
status: stable
---

# Python Test Quality Analysis

Measure test coverage and verify test suite effectiveness using coverage analysis and mutation testing.

## Objectives

1. Measure code coverage comprehensively
2. Identify untested code paths
3. Verify test suite catches bugs (mutation testing)
4. Enable safe refactoring through high test coverage
5. Track coverage trends over time

## Required Tools

**Add to `[dependency-groups]` dev**: `"pytest"`, `"pytest-cov"`, `"mutmut"`, `"coverage"`
**Optional**: `"cosmic-ray"` (advanced mutation testing)

- **pytest-cov**: Code coverage measurement
- **mutmut**: Mutation testing - verifies tests catch bugs
- **cosmic-ray**: Advanced mutation testing (slower)

**Permissions**: Run py-quality-setup first to configure `.claude/settings.local.json` with all needed tool permissions.

## Coverage Analysis

### Measure Coverage

```bash
# Run tests with coverage
pytest --cov=. --cov-report=term-missing
pytest --cov=. --cov-report=html  # Generate HTML report
pytest --cov=. --cov-report=term --cov-report=html  # Both

# Coverage with specific targets
pytest --cov=src --cov=lib tests/
pytest --cov=mypackage --cov-branch  # Include branch coverage

# Fail if coverage below threshold
pytest --cov=. --cov-fail-under=80

# Show only uncovered lines
pytest --cov=. --cov-report=term-missing:skip-covered
```

### Configure Coverage

Add to `pyproject.toml` (see **py-quality-setup** for base configuration):

```toml
[tool.coverage.run]
source = ["src"]  # Adjust to your source directory
omit = [
    "*/tests/*",
    "*/test_*.py",
    "*/__pycache__/*",
    "*/venv/*",
    "*/.venv/*",
]
branch = true  # Enable branch coverage

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "@abstractmethod",
]

[tool.coverage.html]
directory = "htmlcov"
```

### Interpret Coverage Reports

```
Name                 Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------------
src/auth.py            45      5     12      2    87%   23-25, 67
src/database.py        89      0     18      0   100%
src/handlers.py       123     35     28     12    68%   45-78, 99-110
----------------------------------------------------------------
TOTAL                 257     40     58     14    82%
```

**Key metrics**:
- **Stmts**: Total statements
- **Miss**: Uncovered statements
- **Branch**: Total branches (if/else, etc.)
- **BrPart**: Partially covered branches (one path tested, not both)
- **Cover**: Coverage percentage
- **Missing**: Line numbers not covered

**Coverage targets**:
- **≥80%**: Minimum acceptable
- **≥90%**: Good coverage
- **100%**: Ideal (may not be practical for all code)

## Mutation Testing

Mutation testing verifies your tests actually catch bugs by introducing small changes (mutations) and checking if tests fail.

### Run Mutation Testing

```bash
# Using mutmut (easier, faster)
mutmut run                    # Run all mutations
mutmut run --paths-to-mutate=src/  # Specific directory
mutmut results                # Show summary
mutmut show <mutation-id>     # Show specific mutation
mutmut apply <mutation-id>    # Apply mutation to see code change

# Common workflow
mutmut run
mutmut results               # Shows: survived, killed, timeout
mutmut show 1                # Examine first surviving mutation
```

### Configure Mutmut

Add to `setup.cfg` or `pyproject.toml`:

```toml
[tool.mutmut]
paths_to_mutate = "src/"
backup = false
runner = "pytest -x --tb=short"
tests_dir = "tests/"
```

### Interpret Mutation Results

```
Legend for output:
🎉 Killed mutants: Tests caught the bug (good!)
⏰ Timeout: Mutation created infinite loop (acceptable)
🤔 Suspicious: Needs investigation
🙁 Survived: Bug not caught by tests (bad!)
```

**Mutation score**: `killed / (killed + survived) * 100%`

**Target mutation scores**:
- **≥75%**: Good test quality
- **≥85%**: Excellent test quality
- **100%**: Perfect (rarely achievable)

### Address Surviving Mutations

```bash
# 1. Identify surviving mutations
mutmut results

# 2. Show specific mutation
mutmut show 5

# Example output:
# src/auth.py:23
# -    if user.age >= 18:
# +    if user.age > 18:

# 3. Write test to kill this mutation
def test_user_exactly_18_is_adult():
    user = User(age=18)
    assert is_adult(user) is True  # This would fail with > instead of >=

# 4. Re-run mutmut
mutmut run

# 5. Verify mutation now killed
mutmut results
```

## Coverage-Guided Refactoring

**Golden rule**: Only refactor well-tested code. If coverage is low, write tests first.

### Workflow

```
1. Run: pytest --cov=. --cov-report=html --cov-fail-under=80
2. If coverage < 80%:
   a. Open htmlcov/index.html
   b. Identify modules with low coverage (red/yellow)
   c. Write tests to increase coverage to ≥80%
   d. Re-run coverage to verify
3. Run: mutmut run (optional but recommended)
4. If mutation score < 75%:
   a. Review surviving mutations
   b. Write tests to kill mutations
   c. Re-run mutmut
5. NOW safe to refactor:
   a. Apply refactoring patterns
   b. Re-run: pytest --cov=. (ensure coverage maintained)
   c. Re-run: mutmut run (ensure mutation score maintained)
```

## Integration with Refactoring

### Before Refactoring Checklist

```bash
# 1. Measure baseline coverage
pytest --cov=src/module_to_refactor.py --cov-report=term-missing

# 2. If coverage < 80%, write tests first
# ... write tests ...

# 3. Verify tests are effective
mutmut run --paths-to-mutate=src/module_to_refactor.py

# 4. Now proceed with refactoring
# ... refactor ...

# 5. Verify coverage maintained
pytest --cov=src/module_to_refactor.py --cov-fail-under=80

# 6. Verify tests still effective
mutmut run --paths-to-mutate=src/module_to_refactor.py
```

## CI/CD Integration

Add coverage enforcement to CI:

```yaml
# .github/workflows/test.yml
- name: Run tests with coverage
  run: |
    pytest --cov=. --cov-report=term --cov-report=xml --cov-fail-under=80

- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
```

## Verification Checklist

- [ ] `pytest --cov=. --cov-fail-under=80` passes
- [ ] Coverage report reviewed (`htmlcov/index.html`)
- [ ] Critical paths have test coverage
- [ ] Mutation testing run on critical modules (`mutmut run`)
- [ ] Mutation score ≥75% for critical code
- [ ] Coverage configuration in pyproject.toml

## Examples

**Example: Increase coverage before refactoring**
```
1. Run: pytest --cov=src/handlers.py --cov-report=html
2. Coverage: 55% (too low to refactor safely)
3. Open htmlcov/handlers_py.html
4. Lines 45-78 not covered (error handling paths)
5. Write tests for error cases:
   - test_handler_invalid_input()
   - test_handler_database_error()
   - test_handler_missing_params()
6. Re-run: pytest --cov=src/handlers.py
7. Coverage now: 85% (safe to refactor)
8. Proceed with complexity reduction refactoring
9. After refactoring: pytest --cov=src/handlers.py --cov-fail-under=85
10. Verify coverage maintained at 85%
```

**Example: Use mutation testing to improve tests**
```
1. Run: mutmut run --paths-to-mutate=src/auth.py
2. Results: 15 killed, 3 survived (83% mutation score)
3. Run: mutmut show 5
4. Mutation: Changed >= to > in age check
5. Realize: Missing boundary test for age exactly 18
6. Write: test_user_exactly_18_is_adult()
7. Run: mutmut run --paths-to-mutate=src/auth.py
8. Results: 16 killed, 2 survived (89% mutation score)
9. Repeat for remaining survivors
10. Final: 18 killed, 0 survived (100% mutation score)
```

**Example: Coverage-guided refactoring session**
```
1. Target: Refactor src/payment.py (complexity D, 150 lines)
2. Check coverage: pytest --cov=src/payment.py --cov-report=term-missing
3. Coverage: 92% (good! safe to refactor)
4. Check test quality: mutmut run --paths-to-mutate=src/payment.py
5. Mutation score: 78% (acceptable)
6. Proceed with refactoring:
   - Extract 4 smaller functions
   - Reduce complexity from D to A/B
7. After refactoring:
   - pytest --cov=src/payment.py --cov-fail-under=92 ✓
   - mutmut run --paths-to-mutate=src/payment.py
   - Mutation score: 80% (improved!)
8. Commit changes with confidence
```

**Example: Set up coverage tracking in CI**
```
1. Add to pyproject.toml:
   [tool.coverage.run]
   source = ["src"]
   branch = true

2. Create .github/workflows/test.yml:
   - pytest --cov=. --cov-fail-under=80

3. First run fails: Coverage 67%
4. Write tests to reach 80%
5. CI now passes
6. All future PRs must maintain 80% coverage
7. Consider increasing threshold as coverage improves
```

## Related Skills

- **Prerequisites**: py-quality-setup (configure pytest-cov in pyproject.toml)
- **Enables**: py-security, py-code-health, py-complexity (safe refactoring with test coverage)
- **Enforcement**: py-git-hooks (add coverage checks to CI)
