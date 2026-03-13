---
name: create-local-plan
description: Create a detailed development plan stored locally in `.github/plans/`. Use when the user wants to plan a new feature, create a local backlog or bug plan, or draft a detailed development plan without creating GitHub issues. Plans are written in Traditional Chinese with English code examples.
metadata:
  original-prompt: create-local-plan.prompt.md
  plan-language: 正體中文
---

# Create Local Plan

Create a detailed development plan stored locally in the `.github/plans/` directory.

**We are at planning stage so don't start to implement anything!**

> This time, the work requires greater accuracy. You are allowed to use more resources for reflection, so please ultrathink carefully before you begin.

## Steps

0. **Research**: Conduct deep research on the project and the plan. Search for relevant information in the codebase, run commands like `git log` or `git diff` to understand the project history.

1. **Plan Creation**: Create a development plan in `.github/plans/backlogs` or `.github/plans/bugs`. Write the plan description in 正體中文, but use English for example code comments and CLI responses. The plan should be very detailed (try your best!) because I will assign these tasks to newbies in the future. Please write documentation that enables anyone to complete the work successfully. However, do not mention 'newbies' in the document, as I do not want to undermine the employee's confidence. Please write that enables anyone to complete the work successfully.

2. **Prompt User**: Show the plan details and ask if any changes are needed. If so, edit the plan description accordingly.
