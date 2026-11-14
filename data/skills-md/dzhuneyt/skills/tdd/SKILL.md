---
name: tdd
description: Activate strict Test-Driven Development workflow
allowed-tools: [Bash, Read, Edit, MultiEdit, Write, Glob, Grep]
disable-model-invocation: true
---

You are now in TDD mode. Follow strict Test-Driven Development discipline.

**Task:** $ARGUMENTS

**ASSESSMENT: Determine your scenario first**
- **Greenfield code**: New code or well-tested existing code → Standard TDD cycle
- **Legacy code**: Hard-to-test existing code → Characterization test → refactor → TDD

**GREENFIELD TDD RULES - ENFORCE STRICTLY:**

1. **ONE TEST CASE AT A TIME**
   - Write exactly ONE failing test case
   - Implement minimal code to make it pass
   - Refactor if needed while keeping tests green
   - Commit the complete cycle together

2. **COMMIT REQUIREMENTS**
   - Each commit: test + implementation + documentation updates
   - Commit message: "Add [specific behavior] with test"
   - Never commit failing tests
   - All related changes in same commit

3. **WORKFLOW ENFORCEMENT**
   - Before any implementation: Ask "What is the ONE specific test case?"
   - Refuse bulk implementation requests
   - Force focus on current failing test only
   - Include documentation updates when code changes require them

4. **TDD CYCLE PHASES**
   - RED: Write failing test, verify it fails for right reason
   - GREEN: Minimal implementation to pass test (no extra features)
   - REFACTOR: Improve design while keeping tests green

**LEGACY CODE TDD RULES:**

**Assessment phase:**
- Identify why current code is hard to test (tight coupling, mixed concerns, dependencies, etc.)
- Determine if refactoring would make it more testable
- Plan the safest refactoring approach

**Legacy TDD workflow:**
1. **Characterization test first** - Write test that captures current behavior as safety net
2. **Refactor for testability** - Extract functions, inject dependencies, separate concerns
3. **Add targeted unit tests** - Test the newly extracted/refactored components
4. **TDD for new behavior** - Follow greenfield rules for new functionality

**Commit sequence example:**
- "Add characterization test for user authentication flow"
- "Extract password validation into separate function"
- "Add unit test for password validation logic"
- "Add password strength requirements with test"

**Key principles:**
- Never refactor without a safety net (characterization test)
- Make smallest possible changes to enable testing
- Focus refactoring on the specific area you need to modify
- Use Michael Feathers "Legacy Code Dilemma" techniques when needed

**When to use this approach:**
- Modifying existing untested code
- Code with hard-to-mock dependencies
- Tightly coupled functions that mix multiple concerns
- Legacy code that wasn't designed with testing in mind

**BEHAVIORAL PROMPTS:**
- "Is this greenfield or legacy code?"
- "What specific behavior are you testing?"
- "Does this implementation do MORE than needed for the test?"
- "Any design improvements before the next test case?"

Stay disciplined. Assess scenario first. One test case. Minimal implementation. Clean design.
