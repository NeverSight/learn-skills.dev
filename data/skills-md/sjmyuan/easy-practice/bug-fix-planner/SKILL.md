---
name: bug-fix-planner
description: First, determine the root cause of the reported bug. Then, create a clear, step-by-step plan for the bug fixing. Use this skill whenever a user reports a bug.
---

<when-to-use-this-skill>
- User reports a bug.
</when-to-use-this-skill>

<capabilities>

The capabilities section describes additional capabilities that you can refer to.

<identifying-bug-root-cause>
- Gather relevant information from the codebase, knowledge base, test results and user input to clearly identify the bug.
- Analyze the information to identify patterns, inconsistencies, or anomalies that may indicate the root cause of the bug.
- Formulate hypotheses about potential causes and systematically test them through code inspection, debugging, or additional logging.
- Ask questions to the user to narrow down the possibilities until the most likely root cause is identified.
- Present the identified root cause and the reasoning process to the user and request confirmation or refinements.
</identifying-bug-root-cause>

<adapting-tdd-approach>
- Recognize when the full TDD cycle may be adapted or streamlined based on the bug complexity:
  - **Simple bugs** (typos, minor logic errors, incorrect constants): May consolidate test writing and fixing in fewer steps if existing tests provide adequate coverage
  - **Type-related bugs** (missing/incorrect TypeScript types): Focus on type-checking validation rather than test-first approach
  - **Configuration bugs** (incorrect environment settings, build config): Validate with build/run rather than unit tests
  - **Performance bugs**: Require performance tests and benchmarks in addition to functional tests
  - **Complex logic bugs**: Always follow full TDD cycle for safety and thorough validation
- When adapting the approach, always ensure existing tests pass before and after changes
- Document the rationale for adapting the TDD approach in the plan
</adapting-tdd-approach>

<bug-fixing-planning>
- **Validate Baseline**: Run existing tests, linting, and type-checking to ensure the codebase is in a clean state before bug fixing begins.
- Break down the identified bug root cause into specific, independently testable issues.
- Map out dependencies between issues to establish an efficient bug-fixing sequence.
- **Consolidate Steps**: Group related issues together when they share context or can be tested together, reducing the total step count while maintaining clarity.
- Create a detailed step-by-step bug-fixing plan following the TDD approach. For each issue, the steps should include:
  - **Write Focused Tests**: Create precise unit tests targeting the specific bug issue, ensuring comprehensive coverage of all scenarios, edge cases, and invalid inputs.
  - **Confirm Test Failure**: Execute the tests to verify they fail initially, validating that the tests correctly identify the current code behavior before fixing begins.
  - **Fix Code**: Modify the minimum amount of code necessary to pass the tests while addressing the bug, avoiding over-engineering or introducing unrelated changes.
  - **Verify Fix**: Re-run all tests to confirm the fix works successfully. Debug and refine as necessary to ensure correctness.
  - **Clean Up Unused Code**: Remove any obsolete or redundant code that is no longer needed after the bug fix.
  - **Clean Up Tests**: Update or remove tests that are no longer relevant due to the bug fix, ensuring the test suite remains accurate and effective.
  - **Verify Cleanup**: Re-run all tests to ensure that the cleanup process has not introduced any regressions or issues.
  - **Validate Linting, Formatting and Type Checking**: Run linting, formatting and type checking tools to ensure code quality and adherence to coding standards.
- Ensure the total number of steps in the plan is manageable and does not exceed 20 steps.
- Summarize the complete plan to the user. For example:
  """
  To fix the bug of [bug summary], the plan is as follows:
  - Step 1: Validate Baseline (run existing tests, lint, type-check)
  - Step 2: Write Focused Tests for issue A
  - Step 3: Confirm Test Failure for issue A
  - Step 4: Fix Code for issue A
  - Step 5: Verify Fix for issue A
  - Step 6: Clean Up Unused Code for issue A
  - Step 7: Clean Up Tests for issue A
  - Step 8: Verify Cleanup for issue A
  - Step 9: Validate Linting, Formatting and Type Checking for issue A
  - Step 10: Write Focused Tests for issue B
  - Step 11: Confirm Test Failure for issue B
  - Step 12: Fix Code for issue B
  - Step 13: Verify Fix for issue B
  - Step 14: Clean Up Unused Code for issue B
  - Step 15: Clean Up Tests for issue B
  - Step 16: Verify Cleanup for issue B
  - Step 17: Validate Linting, Formatting and Type Checking for issue B
  - ...
  I will apply **plan-executor** skill to fix the bug step by step as outlined.
  """
</bug-fixing-planning>

<bug-fixing-planning-examples>

When you need specific examples to understand how to apply the bug-fixing planning approach, load the relevant example file from the examples folder:

- **Simple Logic Bugs**: When fixing bugs related to incorrect logic, timing, or calculation errors, read `examples/simple-logic-bug.md`
- **Type-Related Bugs**: When fixing bugs related to TypeScript types, optional fields, or type safety issues, read `examples/type-related-bug.md`
- **Data Persistence Bugs**: When fixing bugs related to database operations, async handling, or data loss issues, read `examples/data-persistence-bug.md`

Only load example files when they are directly relevant to the current bug being fixed to minimize context size.

</bug-fixing-planning-examples>
</capabilities>

<rules>

The rules section outlines decision criteria that determine which capabilities to apply based on the current context and user inputs.

<rule> If the user reports a bug, apply the **identifying-bug-root-cause** capability to identify the root cause of the bug. </rule>
<rule> After identifying the root cause of the bug, apply the **adapting-tdd-approach** capability to evaluate whether to adapt TDD approach based on the bug complexity and type. </rule>
<rule> Apply the **bug-fixing-planning** capability to generate a detailed bug-fixing plan, incorporating baseline validation and step consolidation strategies. </rule>
<rule> Always validate the baseline state before starting bug fixes to ensure a clean starting point. </rule>
</rules>