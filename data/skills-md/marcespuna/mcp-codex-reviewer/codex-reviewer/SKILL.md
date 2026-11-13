---
name: codex-reviewer
description: Enables Codex-powered plan and implementation reviews. Activates when using /deep-task or when enhanced review workflow is needed for thorough, AI-validated development.
---

# Codex-Enhanced Review Workflow

This skill enables a collaborative AI review process using OpenAI Codex to validate plans and implementations.

## When Active

- User invokes `/deep-task` command
- User explicitly requests Codex review
- Working on complex tasks that benefit from external AI validation

## Codex Capabilities

Codex operates with **READ-ONLY filesystem access**:
- **CAN** read any file in the working directory and subdirectories
- **CAN** explore imports, dependencies, and related modules
- **CAN** examine tests, configs, and documentation
- **CANNOT** write, modify, or execute any files

This means Codex can provide deeply context-aware reviews by actually reading the codebase, not just the snippets you provide. Always give it comprehensive file paths so it can understand the full picture.

## Review Focus Areas

Codex reviews are optimized for systems-level and embedded development, focusing on:

1. **Code Reusability** - Leveraging existing modules, extracting common patterns, modular design
2. **Dead Code Prevention** - Identifying unused code paths, unreachable branches, unused imports/variables
3. **Maintainability & Testability** - Clean structure, isolated components, proper abstractions, unit testability
4. **Code Footprint** - Binary size impact, memory usage, suitability for resource-constrained environments
5. **Optimizations** - CPU cycles, memory allocations, stack usage, loop efficiency, data structure choices

## Workflow Overview

### Phase 1: Planning with Codex Review

1. **Switch to plan mode** (encouraged but not enforced)
   - Analyze the user's request thoroughly
   - Explore the codebase to understand context

2. **Gather context and clarifications**
   - Ask clarifying questions to understand requirements
   - Identify relevant files and existing patterns
   - Note constraints or dependencies

3. **Draft implementation plan**
   - Create a detailed, step-by-step plan
   - List all files to be modified/created
   - Identify potential risks or edge cases

4. **Request Codex review** (REQUIRED before presenting plan)

   **IMPORTANT**: Codex has READ-ONLY filesystem access. It will read the files you provide to understand the codebase context. Provide comprehensive file paths!

   Call `mcp__mcp-codex__codex_plan_review` with:
   ```
   - user_prompt: The original user request
   - clarifications: Summary of Q&A with user
   - relevant_files: Array of file paths - BE THOROUGH:
     * Files that will be modified
     * Files that import/depend on modified files
     * Similar existing implementations for pattern reference
     * Test files for the affected modules
     * Config files that might be relevant
   - plan: Your drafted implementation plan
   ```

   Codex will read these files and explore related code to provide context-aware feedback.

5. **Evaluate Codex feedback critically**
   - Review each finding - verify it's actually correct
   - Don't blindly accept all suggestions
   - Use your judgment on what's valid

6. **Handle Codex questions**
   - If Codex raises questions you can't answer, ask the user
   - Incorporate user clarifications into the plan

7. **Update plan if findings are valid**
   - Address legitimate concerns
   - Document why you're not incorporating certain suggestions

8. **Present refined plan to user**
   - Include feature branch creation as first step (if git repo)
   - Summarize what Codex feedback was incorporated

### Phase 2: Implementation with Review

1. **Create feature branch first** (if in git repository)
   ```bash
   # Check if in git repo
   git rev-parse --git-dir

   # Create and checkout feature branch
   git checkout -b feature/<task-slug>
   ```

2. **Implement the approved plan**
   - Follow the plan step by step
   - Track progress with todo list
   - Commit logical units of work

3. **Request implementation review** (REQUIRED before declaring completion)

   **IMPORTANT**: Codex has READ-ONLY filesystem access. It will read the changed files and related code to verify the implementation. Provide complete context!

   Call `mcp__mcp-codex__codex_implementation_review` with:
   ```
   - user_prompt: The original user request
   - plan: The approved implementation plan
   - clarifications: All clarifications gathered
   - diff: Output of `git diff` from branch point
   - changed_files: Array of modified file paths - BE THOROUGH:
     * All files that were modified
     * New files that were created
     * Test files (new and modified)
     * Config files if changed
   ```

   Codex will read the full files (not just diff), check related modules, and verify against existing patterns.

4. **Evaluate Codex feedback critically**
   - Verify each finding is actually correct
   - Prioritize critical issues over suggestions
   - Use judgment on what needs immediate fixing

5. **If critical fixes are needed**
   - Switch to plan mode
   - Propose a fix plan to the user
   - Wait for user approval
   - Implement fixes

6. **Present final results**
   - Summarize what was implemented
   - Note any deviations from plan and why
   - Include summary of Codex review
   - Suggest next steps (PR creation, testing, etc.)

## Tool Reference

### codex_plan_review

Reviews an implementation plan before user approval.

```
mcp__mcp-codex__codex_plan_review
├── user_prompt (required): Original user request
├── clarifications: Q&A summary with user
├── relevant_files: ["path/to/file1", "path/to/file2"]
└── plan (required): The implementation plan to review
```

**Returns:**
- `approved`: boolean
- `summary`: Brief assessment
- `feedback`: Detailed feedback
- `suggestions`: Array of specific suggestions
- `concerns`: Array of potential issues
- `questions`: Questions needing user clarification

### codex_implementation_review

Reviews completed code against the approved plan.

```
mcp__mcp-codex__codex_implementation_review
├── user_prompt (required): Original user request
├── plan (required): The approved plan
├── clarifications: All clarifications gathered
├── diff: Git diff of changes
└── changed_files: ["path/to/modified/file"]
```

**Returns:**
- `approved`: boolean
- `summary`: Brief assessment
- `plan_adherence`: How well implementation follows plan
- `quality_notes`: Code quality observations
- `issues`: Array of issues with severity/file/description
- `positive_notes`: Things done well

## Critical Behavior

1. **Always evaluate Codex findings before acting**
   - Codex can make mistakes
   - Verify suggestions make sense for this codebase
   - Don't blindly accept all recommendations

2. **Don't skip reviews**
   - Plan review is REQUIRED before presenting plan to user
   - Implementation review is REQUIRED before declaring completion
   - If review fails (timeout, error), inform user and offer to proceed

3. **Ask for clarification when needed**
   - If Codex raises questions you can't answer, ask the user
   - Don't make assumptions about user intent

4. **Feature branch is mandatory**
   - Always create `feature/<task-slug>` before making changes
   - This enables clean diffs for implementation review

## Example Flow

```
User: Add a circular buffer for UART RX handling

Claude Code:
1. Enters plan mode
2. Asks: "What buffer size? Does it need to be thread-safe for ISR access?"
3. User: "256 bytes, yes it's filled from ISR"
4. Reads: src/drivers/uart.c, src/utils/ring_buffer.h, src/hal/*
5. Drafts plan reusing existing ring_buffer module with volatile qualifiers
6. Calls codex_plan_review
7. Codex suggests: "Existing ring_buffer uses malloc - consider static allocation for ISR safety"
8. Evaluates: Valid concern, updates plan to use statically allocated buffer
9. Adds step 1: "Create branch feature/uart-rx-buffer"
10. Presents refined plan to user
11. User approves
12. Creates branch, implements with todo tracking
13. Calls codex_implementation_review
14. Codex: "Approved. Notes: good use of volatile, memory barrier might be needed on ARM"
15. Evaluates: Valid point, adds memory barrier for portability
16. Presents completion summary to user
```

## Handling Review Failures

If Codex review fails (timeout, connection error):
1. Inform the user about the failure
2. Offer options:
   - Retry the review
   - Proceed without review (user accepts risk)
   - Cancel and investigate
3. Document that review was skipped if proceeding
