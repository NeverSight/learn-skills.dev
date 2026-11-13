---
name: feature-implementation-planner
description: Clarify and structure the requirement first, then generate an implementation plan for the requirement; Use this skill when user submits a requirement to add new functionalities.
---

<when-to-use-this-skill>
- User submits a requirement to add new functionalities.
</when-to-use-this-skill>

<capabilities>

The capabilities section describes additional capabilities that you can refer to.

<defining-requirement>
- Gather relevant information from the codebase, knowledge base, and user input to clearly define the software requirement.
- Identify and clarify any ambiguous terms or implicit assumptions to ensure proper understanding.
- Ask questions to the user to refine and narrow down the focus of the software requirement as needed.
- Present a structured summary of the requirement to the user and request confirmation or refinements.
</defining-requirement>

<adapting-tdd-approach>
- Recognize when the full TDD cycle may be adapted or streamlined based on the implementation type:
  - **Simple features** (small UI additions, basic form fields): May consolidate test and implementation steps when logic is straightforward
  - **Pure presentational components**: Focus on rendering and prop validation tests with minimal logic testing
  - **Type-only additions** (adding new types/interfaces without behavior): Focus on type-checking validation rather than test-first approach
  - **Configuration changes** (adding constants, config options): Minimal testing may suffice if changes don't affect behavior
  - **Complex business logic**: Always follow full TDD cycle for safety and clarity
- When adapting the approach, always ensure existing tests pass before and after changes
- Document the rationale for adapting the TDD approach in the plan
</adapting-tdd-approach>

<implementation-planning>
- **Validate Baseline**: Run existing tests, linting, and type-checking to ensure the codebase is in a clean state before implementation begins.
- Break down high-level software requirements into specific, independently testable functionalities.
- Map out dependencies between functionalities to establish an efficient implementation sequence.
- **Consolidate Steps**: Group related functionalities together when they share context or can be tested together, reducing the total step count while maintaining clarity.
- Create a detailed step-by-step implementation plan for the functionalities following the TDD approach. For each functionality, the steps should include:
  - **Write Focused Tests**: Create precise unit tests for a single functionality, task or requirement, ensuring coverage of all possible scenarios, edge cases, and invalid inputs.  
  - **Confirm Test Failure**: Execute the tests to verify they fail initially, confirming their validity before implementation begins.  
  - **Implement Minimal Code**: Write the simplest code required to pass the tests, avoiding over-engineering or adding features not directly related to the current test cases.  
  - **Verify Implementation**: Re-run the tests to confirm that the implemented code passes all test cases successfully. Debug and refine as necessary.  
  - **Refactor**: Improve the code’s structure, readability, and performance while maintaining functionality, ensuring no tests break during the process.  
  - **Validate Refactoring**: Run the tests again after refactoring to ensure the updated code still passes all test cases without introducing regressions.
  - **Clean Up Unused Code**: Remove any obsolete or redundant code that is no longer needed after implementation.
  - **Clean Up Tests**: Update or remove tests that are no longer relevant, ensuring the test suite remains accurate and effective.
  - **Verify Cleanup**: Re-run all tests to ensure that the cleanup process has not introduced any regressions or issues.
  - **Validate Linting, Formatting and Type Checking**: Run linting, formatting and type checking tools to ensure code quality and adherence to coding standards.
- Ensure the total number of steps in the plan is manageable and does not exceed 20 steps.
- Summarize the complete plan to the user. For example:
  """
  To implement the requirement of [requirement summary], the plan is as follows:
  - Step 1: Validate Baseline (run existing tests, lint, type-check)
  - Step 2: Write Focused Tests for functionality A
  - Step 3: Confirm Test Failure for functionality A
  - Step 4: Implement Minimal Code for functionality A
  - Step 5: Verify Implementation for functionality A
  - Step 6: Refactor code related to functionality A
  - Step 7: Validate Refactoring for functionality A
  - Step 8: Clean Up Unused Code for functionality A
  - Step 9: Clean Up Tests for functionality A
  - Step 10: Verify Cleanup for functionality A
  - Step 11: Validate Linting, Formatting and Type Checking for functionality A
  - Step 12: Write Focused Tests for functionality B
  - Step 13: Confirm Test Failure for functionality B
  - Step 14: Implement Minimal Code for functionality B
  - Step 15: Verify Implementation for functionality B
  - Step 16: Refactor code related to functionality B
  - Step 17: Validate Refactoring for functionality B
  - Step 18: Clean Up Unused Code for functionality B
  - Step 19: Clean Up Tests for functionality B
  - Step 20: Verify Cleanup for functionality B
  - Step 21: Validate Linting, Formatting and Type Checking for functionality B
  - ...
  I will apply **plan-executor** skill to implement the requirement step by step as outlined.
  """
</implementation-planning>


<implementation-planning-examples>

When you need specific examples to understand how to apply the implementation planning approach, load the relevant example file from the examples folder:

- **Adding a New Export Feature**: When implementing a new feature that involves both backend logic and UI components, read `examples/adding-new-export-feature.md`
- **Simple UI Enhancement**: When implementing straightforward UI improvements without complex business logic, read `examples/simple-ui-enhancement.md`
- **Complex Business Logic**: When implementing sophisticated algorithms or complex business rules requiring rigorous testing, read `examples/complex-business-logic.md`

Only load example files when they are directly relevant to the current implementation task to minimize context size.

</implementation-planning-examples>

</capabilities>

<rules>

The rules section outlines decision criteria that determine which capabilities to apply based on the current context and user inputs.

<rule> If the user submits a requirement, apply the **defining-requirement** capability to clarify and structure it. </rule>
<rule> After defining the requirement, apply the **adapting-tdd-approach** capability to evaluate whether to adapt TDD approach based on the implementation type and complexity. </rule>
<rule> Apply the **implementation-planning** capability to generate a detailed implementation plan, incorporating baseline validation and step consolidation strategies. </rule>
</rules>