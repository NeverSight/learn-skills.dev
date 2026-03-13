---
name: create-plan
description: Create a detailed development plan and GitHub issues for a project. Use when the user wants to plan a new feature or fix, create GitHub issues for backlogs or bugs, or draft a comprehensive development plan with task breakdowns, dependencies, and testing strategies. Plans are written in Traditional Chinese with English code examples.
metadata:
  original-prompt: create-plan.prompt.md
  plan-language: 正體中文
  restriction: All issue and PR operations are limited to repositories owned by jim60105 only.
---

# Create Plan

Create a detailed development plan and corresponding GitHub issues.

**We are at planning stage so don't start to implement anything!**
**Planning Stage is to create a detailed development plan and #issue_write on GitHub**

> This time, the work requires greater accuracy. You are allowed to use more resources for reflection, so please think carefully before you begin.

## Steps

0. **Research**: Conduct deep research on the project and the issue. Search for relevant information in the codebase; find related issues and comments. Run commands like `git log` or `git diff` to understand project history. #askQuestions clarifying questions if needed. If #askQuestions or #ask_user is not available, you should keep on without asking questions.

1. **Plan Creation**: Based on research, create a detailed development plan including:
   - Breakdown of tasks and subtasks
   - Dependencies between tasks
   - Potential challenges and mitigation strategies
   - Testing and validation strategies

2. **Review Plan**: Review the plan for comprehensiveness and feasibility. Challenge yourself to think of edge cases and potential pitfalls.

3. **Issue Creation**: Create a new GitHub issue for each backlog item or bug report. You may have several solutions, but only write THE BEST ONE. Write issue descriptions in 正體中文, but use English for example code comments and CLI responses. The plan should be very detailed (try your best!) because I will assign these tasks to newbies in the future. Please write documentation that enables anyone to complete the work successfully. However, do not mention 'newbies' in the document, as I do not want to undermine the employee's confidence. Please write that enables anyone to complete the work successfully.

4. **Prompt User**: Show the issue number and link, and ask if any changes are needed. Edit the issue description if requested.

***All issue and PR operations are limited to repositories owned by jim60105 only.***
