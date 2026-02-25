---
name: implement-feature-complete
description: |
  Manages complete feature implementation lifecycle through 10 stages: planning, TDD, naming,
  DRY, implementation, refactor, integration testing, E2E testing, real usage validation,
  and production monitoring. Use when implementing new features, significant changes,
  or onboarding to project workflow. Ensures Clean Architecture, fail-fast principles,
  ServiceResult pattern, and quality gates. Triggers on "implement feature X", "add functionality Y",
  "complete workflow for Z", "end-to-end implementation", or "production-ready feature".
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Edit
  - MultiEdit
  - Write
---

Works with Clean Architecture projects, Python codebases, TDD workflows, and quality gates.
# Complete Feature Implementation

## Quick Start

Orchestrate the complete lifecycle of implementing a feature following project standards. This meta-skill ensures no step is forgotten, all quality gates pass, and the feature is production-ready.

**Most common use case:**
```
User: "Add ability to search code by file type"

→ Follow 10-stage workflow (TDD, naming, DRY, implementation, refactor, testing)
→ Use checklist template to track progress
→ Validate at each stage before proceeding
→ Feature is production-ready with unit/integration/E2E tests + monitoring

Result: Fully tested feature in 2-3 hours
```

## When to Use This Skill

Use when:
- **Implementing new features** - "Add ability to X"
- **Significant changes** - Multi-layer modifications affecting domain/application/infrastructure
- **Onboarding to project** - Learning the complete feature workflow
- **Quality-critical work** - Features requiring full test coverage and monitoring
- **Production deployments** - Changes that must be production-ready

**Trigger phrases:** "Implement feature X", "Add functionality for Y", "Complete workflow for Z", "End-to-end implementation"

## What This Skill Does

Orchestrates complete feature implementation through 10 stages:

1. **Planning & Location** - Determine Clean Architecture layer placement
2. **TDD - Red** - Write comprehensive failing tests first
3. **Consistent Naming** - Follow project conventions
4. **Extract Common (DRY)** - Centralize shared logic
5. **Implementation - Green** - Minimum code to pass tests
6. **Refactor - Clean** - Quality gates enforcement
7. **Integration Testing** - Test with real dependencies (Neo4j, file system)
8. **E2E Testing** - Test through MCP interface
9. **Real Usage Validation** - Manual testing in Claude Code
10. **Production Monitoring** - Verify OTEL traces and production readiness

## 10-Stage Workflow

### Stage 1: Planning & Location (5-10 min)

**Determine architectural placement:**
1. Identify Clean Architecture layer (domain/application/infrastructure/interface)
2. Locate existing similar features for consistency
3. Plan dependencies and interfaces
4. Identify required tests (unit, integration, E2E)

**Key decisions:**
- Domain layer (value objects, entities) vs Application layer (use cases)
- Repository pattern needed?
- ServiceResult pattern for error handling
- Dependencies to inject

**Exit criteria:** Clear plan documented, layers identified, test strategy defined

### Stage 2: TDD - Red (Write Failing Test) (10-15 min)

**Write comprehensive failing tests BEFORE implementation:**
1. Unit tests for business logic (domain/application)
2. Constructor validation tests
3. Edge case tests (empty inputs, invalid states)
4. Error handling tests (ServiceResult failures)

**Template usage:**
```python
# Use test-implement-constructor-validation skill
# Use setup-pytest-fixtures for factory patterns
```

**Exit criteria:** All tests written, all tests failing (red), coverage plan complete

### Stage 3: Consistent Naming (5 min)

**Follow project conventions:**
1. Review existing code for naming patterns
2. Match verb conventions (find, search, get, create, update, delete)
3. Align with project vocabulary (e.g., "code" not "file", "repository" not "repo")
4. Check abbreviations match project style

**Exit criteria:** Naming consistent with existing codebase, no new patterns introduced

### Stage 4: Extract Common (DRY Principle) (10 min)

**Identify and centralize shared logic:**
1. Search for similar implementations: `Grep` for existing patterns
2. Extract to shared utilities if used 3+ times
3. Refactor existing code to use new shared logic
4. Update tests to cover shared utilities

**Exit criteria:** No duplicate logic, shared code extracted, all tests still failing (red)

### Stage 5: Implementation - Green (Make Test Pass) (20-30 min)

**Minimal implementation to pass tests:**
1. Implement domain layer (value objects, entities)
2. Implement application layer (use cases, handlers)
3. Implement infrastructure layer (repositories, external adapters)
4. Use ServiceResult pattern for error handling
5. Inject dependencies properly

**Key patterns:**
- Use Protocol for interfaces (domain layer)
- Concrete implementation in infrastructure
- Fail-fast validation (no try/except for imports, validation)
- Type hints everywhere

**Exit criteria:** All tests passing (green), no shortcuts, minimal code

### Stage 6: Refactor - Clean (Quality Gates) (10-15 min)

**Enforce quality standards:**
```bash
# Run quality gates
pytest tests/
mypy src/
ruff check src/
```

**Fix issues:**
1. Type errors (mypy)
2. Linting issues (ruff)
3. Test failures
4. Code duplication
5. Missing docstrings

**Exit criteria:** All quality gates passing, code clean, tests green

### Stage 7: Integration Testing (Real Dependencies) (15-20 min)

**Test with real Neo4j and file system:**
1. Create integration tests in `tests/integration/`
2. Use real Neo4j database (test fixtures)
3. Test real file system operations
4. Verify end-to-end data flow

**Template:**
```python
# tests/integration/test_feature_integration.py
@pytest.mark.integration
async def test_feature_with_real_neo4j(neo4j_container):
    # Test with real database
    pass
```

**Exit criteria:** Integration tests passing, real dependencies work correctly

### Stage 8: E2E Testing (MCP Interface) (15-20 min)

**Test through actual MCP tool interface:**
1. Create E2E test in `tests/e2e/`
2. Test through MCP tool call (as Claude Code would use it)
3. Verify JSON schema validation
4. Test error scenarios

**Template:**
```python
# tests/e2e/test_feature_mcp.py
async def test_feature_via_mcp_tool(mcp_server):
    result = await mcp_server.call_tool("tool_name", {"param": "value"})
    assert result.success
```

**Exit criteria:** E2E tests passing, MCP interface validated

### Stage 9: Real Usage Validation (Manual Testing) (10-15 min)

**Test in Claude Code environment:**
1. Start MCP server: `python -m src.project_watch_mcp`
2. Use feature in Claude Code conversation
3. Monitor logs: `tail -f logs/project-watch-mcp.log`
4. Verify OTEL traces show expected spans
5. Test error scenarios manually

**Validation checklist:**
- Feature works as expected
- Logs show proper trace spans
- Errors handled gracefully
- Performance acceptable

**Exit criteria:** Feature works in real Claude Code session, logs clean, traces visible

### Stage 10: Production Monitoring (OTEL Traces) (5-10 min)

**Verify production readiness:**
1. Check OTEL traces include all spans
2. Verify error handling traces (ServiceResult.failure paths)
3. Confirm performance metrics logged
4. Validate trace context propagation

**Use observe-analyze-logs skill for trace analysis**

**Exit criteria:** All traces present, error paths traced, production-ready

## Usage Examples

### Example 1: Search by File Type Feature

**Request:** "Add ability to search code by file type (.py, .ts, etc.)"

**Workflow:**
1. **Planning:** Application layer (SearchByFileTypeHandler), infrastructure (Neo4j query)
2. **TDD:** Write failing tests for handler, repository, validation
3. **Naming:** "search_by_file_type" (matches existing "search_code")
4. **DRY:** Reuse existing file extension parsing logic
5. **Implementation:** Handler + repository method + Neo4j query
6. **Refactor:** Pass quality gates (mypy, ruff, pytest)
7. **Integration:** Test with real Neo4j database
8. **E2E:** Test via MCP tool call
9. **Real Usage:** Test in Claude Code, monitor logs
10. **Monitoring:** Verify OTEL traces complete

**Result:** Production-ready feature in 2 hours

### Example 2: Add Repository Method

**Request:** "Add method to get file metadata by path"

**Workflow:** Same 10 stages, focused on repository layer
- Stage 1: Infrastructure layer (repository method)
- Stage 2: Write failing repository tests
- Stage 5: Implement Cypher query
- Stage 7: Integration test with real Neo4j

**Result:** Tested repository method in 1 hour

## Expected Outcomes

### Successful Feature Implementation

**Indicators:**
- All 10 stages completed
- All tests passing (unit, integration, E2E)
- Quality gates green (mypy, ruff, pytest)
- Feature works in Claude Code
- OTEL traces visible in logs
- No regressions introduced

**Deliverables:**
- Production-ready feature
- Comprehensive test coverage (80%+)
- Clean code (no type errors, no linting issues)
- Integration with existing system
- Monitoring and observability

### Stage Failure Example

**If quality gates fail at Stage 6:**
```
❌ Stage 6 Failed: Quality Gates

Issues:
- mypy: 3 type errors in src/application/handlers/search_by_file_type.py
- ruff: 2 linting issues (unused imports, line length)
- pytest: 1 test failure (edge case not handled)

Next steps:
1. Fix type errors (add type hints)
2. Fix linting (remove imports, break lines)
3. Fix test failure (handle empty file type list)
4. Re-run quality gates
5. Proceed to Stage 7 when green
```

## Requirements

**Tools needed:**
- pytest (unit tests)
- mypy (type checking)
- ruff (linting)
- Neo4j (integration tests)
- MCP server (E2E tests)

**Knowledge needed:**
- Clean Architecture (layer boundaries)
- TDD workflow (red-green-refactor)
- ServiceResult pattern (error handling)
- Dependency injection (Container pattern)
- OTEL tracing (observability)

**Project files:**
- `ARCHITECTURE.md` - Clean Architecture reference
- `tests/conftest.py` - Pytest fixtures
- `src/container.py` - DI container

## Troubleshooting

### Issue: Quality gates failing at Stage 6

**Symptom:** mypy/ruff/pytest errors prevent progression

**Diagnosis:**
```bash
# Check specific errors
mypy src/
ruff check src/
pytest tests/ -v
```

**Solutions:**
- **Type errors:** Add missing type hints, fix return types
- **Linting:** Fix imports, line length, unused variables
- **Test failures:** Fix edge cases, update test expectations

### Issue: Integration tests failing at Stage 7

**Symptom:** Tests pass with mocks, fail with real Neo4j

**Diagnosis:** Data model mismatch or query issues

**Solutions:**
- Verify Neo4j schema matches expectations
- Check Cypher query syntax
- Validate test fixtures create correct data
- Use `neo4j_container` fixture correctly

### Issue: E2E tests failing at Stage 8

**Symptom:** MCP tool call fails or returns unexpected results

**Diagnosis:** Interface contract mismatch

**Solutions:**
- Verify tool schema matches implementation
- Check input validation (Pydantic models)
- Validate tool registration in MCP server
- Test tool directly with `mcp-cli`

### Issue: Feature doesn't work in Claude Code (Stage 9)

**Symptom:** Manual testing fails, logs show errors

**Diagnosis:** Use `analyze-logs` skill to investigate traces

**Solutions:**
- Check logs for error traces
- Verify MCP server started correctly
- Validate Claude Code can reach server
- Test with simpler inputs first

## Supporting Files

- **[references/stage-guide.md](references/stage-guide.md)** - Detailed guidance for each stage:
  - Stage-specific anti-patterns and red flags
  - Detailed troubleshooting for each stage
  - Code templates and examples
  - Quality gate details (mypy, ruff, pytest configurations)
  - Integration and E2E test patterns
  - OTEL trace validation techniques

- **[references/workflow-checklist.md](references/workflow-checklist.md)** - Copy-paste checklist:
  - 10-stage checklist with exit criteria
  - Quality gate commands
  - Manual testing checklist
  - Production readiness validation

## Red Flags to Avoid

1. **Skipping TDD** - Writing implementation before tests leads to poor test coverage
2. **Skipping quality gates** - Type errors and linting issues compound over time
3. **Mock-only testing** - Integration and E2E tests catch real-world issues
4. **No manual testing** - Automated tests don't catch UX issues
5. **Missing OTEL traces** - Production issues are hard to debug without traces
6. **Inconsistent naming** - Makes codebase harder to navigate
7. **Copy-paste code** - Violates DRY, creates maintenance burden
8. **Partial implementation** - "Working on my machine" doesn't mean production-ready
9. **Ignoring stage failures** - Each stage builds on previous, failures cascade
10. **No monitoring** - Can't validate production behavior without traces

---

**Key principle:** Each stage builds on the previous. Don't skip stages or shortcuts will compound into production issues.

**Remember:** 2-3 hours for complete feature is faster than debugging production issues for days.
