---
name: symmetric-dogfooding
description: Bidirectional integration validation where two repositories validate each other before release. TRIGGERS - symmetric dogfooding, bidirectional testing, cross-repo validation, reciprocal testing, polyrepo integration.
allowed-tools: Read, Bash, Write, Edit, Grep, Glob
---

# Symmetric Dogfooding

Bidirectional integration validation pattern where two repositories each consume the other for testing, ensuring both sides work correctly together before downstream adoption.

## Pattern Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    SYMMETRIC DOGFOODING                         │
│                                                                 │
│        Repo A ◄─────── mutual validation ───────► Repo B        │
│                                                                 │
│   EXPORTS:                              EXPORTS:                │
│   - Library/API                         - Library/API           │
│   - Data structures                     - Data structures       │
│                                                                 │
│   VALIDATES WITH:                       VALIDATES WITH:         │
│   - Repo B real outputs                 - Repo A real outputs   │
│   - Production-like data                - Production-like data  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## When to Use This Skill

Use this skill when:

- Two repos have a producer/consumer relationship
- APIs evolve independently and need integration testing
- Data formats may drift between repos
- Both repos are actively developed

---

## TodoWrite Task Templates

### Template A: Setup Symmetric Dogfooding Between Two Repos

```
1. Identify integration surface (exports from A consumed by B and vice versa)
2. Document data formats, schemas, API signatures at boundary
3. Configure cross-repo dev dependencies in both repos
4. Pin versions explicitly (tags or SHAs, never main)
5. Create integration/ test directory in both repos
6. Write bidirectional validation tests (A validates with B outputs, B validates with A outputs)
7. Add validation tasks to mise.toml or Makefile
8. Document pre-release protocol in both CLAUDE.md files
9. Run full symmetric validation to verify setup
10. Verify against Symmetric Dogfooding Checklist below
```

### Template B: Pre-Release Validation

```
1. Run validate:symmetric task in releasing repo
2. Check if other repo has pending changes affecting integration
3. If yes, test against other repo's feature branch
4. Document any failures in validation log
5. Fix integration issues before release
6. Update version pins after successful validation
7. Coordinate if breaking changes require simultaneous release
8. Verify against Symmetric Dogfooding Checklist below
```

### Template C: Add New Integration Point

```
1. Identify new export/import being added
2. Update integration surface documentation
3. Add tests in both repos for new integration point
4. Run symmetric validation in both directions
5. Update version pins if needed
6. Verify against Symmetric Dogfooding Checklist below
```

### Symmetric Dogfooding Checklist

After ANY symmetric dogfooding work, verify:

- [ ] Both repos have integration tests that import the other
- [ ] Version pins are explicit (tags or commit SHAs)
- [ ] Pre-release checklist includes cross-repo validation
- [ ] Integration tests use real data (not mocks of the other repo)
- [ ] Breaking changes coordination documented
- [ ] Validation task runnable via single command

---

## Post-Change Checklist (Self-Maintenance)

After modifying THIS skill:

1. [ ] Templates cover common symmetric dogfooding scenarios
2. [ ] Checklist reflects current best practices
3. [ ] Example in references/ still accurate
4. [ ] Append changes to [evolution-log.md](./references/evolution-log.md)

---

## Implementation Guide

### Phase 1: Discovery and Mapping

**Identify the integration surface:**

- List all exports from Repo A consumed by Repo B
- List all exports from Repo B consumed by Repo A
- Document data formats, schemas, API signatures

**Map validation scenarios:**

- What real-world data from B can validate A outputs?
- What real-world data from A can validate B outputs?
- Identify edge cases that only appear in production usage

### Phase 2: Dependency Configuration

Configure cross-repo dev dependencies:

**Python (uv/pip):**

```toml
# Repo A pyproject.toml
[project.optional-dependencies]
validation = ["repo-b"]

[tool.uv.sources]
repo-b = { git = "https://github.com/org/repo-b", tag = "<tag>" }  # SSoT-OK
```

```toml
# Repo B pyproject.toml
[project.optional-dependencies]
validation = ["repo-a"]

[tool.uv.sources]
repo-a = { git = "https://github.com/org/repo-a", tag = "<tag>" }  # SSoT-OK
```

**Rust (Cargo):**

```toml
[dev-dependencies]
repo-b = { git = "https://github.com/org/repo-b", tag = "<tag>" }  # SSoT-OK
```

**Node.js:**

```json
{
  "devDependencies": {
    "repo-b": "github:org/repo-b#<tag>"
  }
}
```

**Critical**: Pin to tags or commit SHAs. Never use main/master branches.

### Phase 3: Test Infrastructure

**Directory structure in both repos:**

```
repo-a/
└── tests/
    ├── unit/              # Internal tests
    └── integration/       # Tests using repo-b real outputs
        └── test_with_repo_b.py

repo-b/
└── tests/
    ├── unit/              # Internal tests
    └── integration/       # Tests using repo-a real outputs
        └── test_with_repo_a.py
```

**Bidirectional validation test pattern:**

```python
# repo-a/tests/integration/test_with_repo_b.py
"""Validate Repo A outputs work correctly with Repo B inputs."""

def test_a_output_consumed_by_b():
    # Generate output using Repo A
    a_output = repo_a.generate_data()

    # Feed to Repo B - should work without errors
    b_result = repo_b.process(a_output)

    # Validate the round-trip
    assert b_result.is_valid()
```

### Phase 4: Task Automation

**mise.toml example:**

```toml
[tasks."validate:symmetric"]
description = "Validate against partner repo"
run = """
uv sync --extra validation
uv run pytest tests/integration/ -v
"""

[tasks."validate:pre-release"]
description = "Full validation before release"
depends = ["test:unit", "validate:symmetric"]
```

### Phase 5: Pre-Release Protocol

**Before releasing Repo A:**

1. Run `validate:symmetric` in Repo A (tests against current Repo B)
2. If Repo B has pending changes, test against Repo B branch too
3. Update version pins after successful validation

**Before releasing Repo B:**

1. Run `validate:symmetric` in Repo B (tests against current Repo A)
2. If Repo A has pending changes, test against Repo A branch too
3. Update version pins after successful validation

**Coordinating breaking changes:**

- If A needs to break compatibility, update B first
- If B needs to break compatibility, update A first
- Consider simultaneous releases for tightly coupled changes

---

## Anti-Patterns

| Anti-Pattern               | Problem                        | Solution                      |
| -------------------------- | ------------------------------ | ----------------------------- |
| One-direction only         | Misses half the bugs           | Always test both directions   |
| Using main branch          | Unstable, breaks randomly      | Pin to tags or SHAs           |
| Skipping for small changes | Small changes cause big breaks | Always run full validation    |
| Mocking partner repo       | Defeats the purpose            | Use real imports              |
| Ignoring version matrix    | Silent production failures     | Maintain compatibility matrix |

---

## References

- [example-setup.md](./references/example-setup.md) - Real-world trading-fitness/rangebar-py example
- [evolution-log.md](./references/evolution-log.md) - Skill change history

**External:**

- [Dogfooding (DevIQ)](https://deviq.com/practices/dogfooding/)
- [CDC Testing (Microsoft)](https://microsoft.github.io/code-with-engineering-playbook/automated-testing/cdc-testing/)

---

## Troubleshooting

| Issue                       | Cause                          | Solution                                         |
| --------------------------- | ------------------------------ | ------------------------------------------------ |
| Dependency resolution fails | Version pin outdated           | Update tag/SHA pin to latest stable version      |
| Tests pass locally fail CI  | Different partner repo version | Pin exact same version in both environments      |
| Breaking change not caught  | One-direction testing only     | Run validate:symmetric in BOTH repos             |
| Integration surface unclear | Undocumented exports           | Map all imports/exports before setting up tests  |
| Too many parts moving       | Uncoordinated releases         | Coordinate breaking changes, test branches first |
| Mock data hiding bugs       | Using stubs instead of real    | Always import real partner repo for integration  |
| Version matrix explosion    | Too many combinations          | Limit support to N-1 versions, document clearly  |
| Circular dependency         | Both repos require each other  | Use optional-dependencies for validation only    |
