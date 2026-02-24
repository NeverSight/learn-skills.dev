---
name: jb-beansloop
description: Beans-driven Ralp loop for beans-enabled repos. Use either to work on one bean on user request or to work on all beans in a repo.
skill_author: bjesuiter@gmail.com
private: true
---

# JB Beans Loop

Use this skill to run a beans-driven Ralph-style loop when working in a beans-enabled repo and running an anthropic model.

## Scope and Activation

Use this skill only when BOTH are true:
- The repo is beans-enabled (`.beans.yml` exists)
- `beans` cli exists

Ignore this skill when:
- `.beans.yml` is missing.
- `beans` cli is missing.

If a user request conflicts with beans usage (for example: asks to skip bean creation), ask for confirmation before proceeding.

## Next Issue Mode (Automatic)

When you need a new issue to work on select the next most important bean via the beans skill and based on your own judgement.

This mode should run unattended for as long as possible (overnight-friendly). If a bean is blocked, select another unblocked bean instead of stopping. Only stop when all remaining beans are either completed or blocked.

Query for actionable beans (exclude completed, scrapped, and draft).

```bash
beans query '{ beans(filter: { excludeStatus: ["completed", "scrapped", "draft"], isBlocked: false }) { id title status type priority } }'
```

Evaluate the "most important" bean based on the following criteria:
1. Dependency between beans (you cannot work on a bean that depends on another bean that is not completed)
2. Priority (critical, high, normal, low, deferred)
3. Urgency (time-sensitive or bug)
4. Recency (most recently updated)
5. Tiebreaker: highest priority, then most recent updatedAt

After you found an issue to work on, mark it as `in-progress` and start working on it until the acceptance criteria are met.
If you can't finish the current bean because you encounter an unresolveable issue, mark the current bean as `blocked` and link the follow-up bug/ticket. 

## Next Issue Mode (Manual)

If the user says: 
- `next issue`
- `next bean`
- `next beans`
- `next ticket`
trigger the "Next Issue Mode (Automatic)" but DON'T run a loop in this case!

Rules: 
- ONLY work on that one issue to completion
- Ask the user to review changes and finish.
- Do not commit automatically. 
- If the user approves, 
  use the `committer` skill to commit and push.

## Default Ralp-Loop Prompt

- Start by using Next Issue Mode to select the next bean.
- Work on ONLY one bean at a time.
- Track all work in beans. Never use todo lists.
- Keep the loop unattended as long as possible; avoid unnecessary prompts.
- If you discover new work, create a new bean instead of expanding scope.
- If you can't finish the current bean 
  because you encounter an unresolveable issue, 
  mark it as `blocked` and link the follow-up bug. 
  Then run "Next Issue Mode (Automatic)" again.
- Update bean checklists as you complete each item.
- When the bean is complete, run "Pre-Completion Verification" then mark it done in beans.

## Pre-Completion Verification

Before marking any bean as completed, ensure the app still works:

1. **Build**: Run the build command if the project has one (`npm run build`, `bun run build`, etc.)
2. **Lint/Typecheck**: Run linting and type checking (`npm run lint`, `tsc --noEmit`, etc.)
3. **Tests**: Run the test suite if available (`npm run test`, `bun run test`, etc.)
4. **Manual Verification**: Visually or functionally verify your changes work as expected
5. **GitHub Actions** (after commit/push): Check the pipeline for errors

**If any step fails:** 
- Find and fix the issue before marking the bean complete
- Do NOT mark the bean complete with broken code
- If you cannot resolve the issue, mark the bean as blocked and create a follow-up bug

Note on statuses: beans only supports status values listed in the repo config (draft, todo, in-progress, completed, scrapped). Use tags or a short note in the bean body for labels like `blocked`, `broken`, or `ai verified` unless your repo defines those as valid statuses.

## Browser Integration Test Loop

Use the `jb-browser-testing` skill for all browser verification.

- Start by using "Next Issue Mode (Automatic)" to select the next "done" bean for testing.
- Test every bean marked as done, acting like a user would.
- Confirm the correct browser tab before testing (match port number and page heading).
- If the test succeeds:
  - Record the result in the bean body.
  - Mark the bean as `ai verified at <timestamp>`.
- If the test fails:
  - Create a new bug bean describing the failure.
  - Mark the original bean as `broken` and link the follow-up bug.
- Stop when every "done" bean is either `ai verified` or `broken`.

Recommended result format in the bean body:

```md
## AI Verification
- Result: passed | failed
- Timestamp: <timestamp>
- Notes: <short summary>
```

## Beans CLI Quick Reference

```bash
# Get active beans
beans query '{ beans(filter: { excludeStatus: ["completed", "scrapped", "draft"] }) { id title status type priority } }'

# Read a bean
beans query '{ bean(id: "<id>") { title status type body } }'

# Create a bean
beans create "Title" -t task -d "Description" -s todo

# Update status
beans update <id> --status completed
```
