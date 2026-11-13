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

<bug-fixing-planning>
- Break down the identified bug root cause into specific, independently testable issues.
- Map out dependencies between issues to establish an efficient bug-fixing sequence.
- Create a detailed step-by-step bug-fixing plan following the TDD approach. For each issue, the steps should include:
  - **Write Focused Tests**: Create precise unit tests targeting the specific bug issue, ensuring comprehensive coverage of all scenarios, edge cases, and invalid inputs.
  - **Confirm Test Failure**: Execute the tests to verify they fail initially, validating that the tests correctly identify the current code behavior before fixing begins.
  - **Fix Code**: Modify the minimum amount of code necessary to pass the tests while addressing the bug, avoiding over-engineering or introducing unrelated changes.
  - **Verify Fix**: Re-run all tests to confirm the fix works successfully. Debug and refine as necessary to ensure correctness.
  - **Validate Linting, Formatting and Type Checking**: Run linting, formatting and type checking tools to ensure code quality and adherence to coding standards.
- Ensure the total number of steps in the plan is manageable and does not exceed 20 steps.
- Summarize the complete plan to the user. For example:
  """
  To fix the bug of [bug summary], the plan is as follows:
  - Step 1: Write Focused Tests for issue A
  - Step 2: Confirm Test Failure for issue A
  - Step 3: Fix Code for issue A
  - Step 4: Verify Fix for issue A
  - Step 5: Validate Linting, Formatting and Type Checking for issue A
  - Step 6: Write Focused Tests for issue B
  - Step 7: Confirm Test Failure for issue B
  - Step 8: Fix Code for issue B
  - Step 9: Verify Fix for issue B
  - Step 10: Validate Linting, Formatting and Type Checking for issue B
  - ...
  """
</bug-fixing-planning>
</capabilities>

<rules>

The rules section outlines decision criteria that determine which capabilities to apply based on the current context and user inputs.

<rule> If the user reports a bug, apply the **identifying-bug-root-cause** capability to identify the root cause of the bug. </rule>
<rule> After identifying the root cause of the bug, apply the **bug-fixing-planning** capability to generate a bug-fixing plan. </rule>
</rules>