---
name: "3"
description: "Standard execution timebox for moderately involved tasks. Use when the user invokes /3 and target completion within 13 minutes with implementation, testing, and nearby regression checks."
---

# /3 — Standard

Treat this as a moderately involved task and complete it end to end.

## Timebox

Target completion in under 13 minutes. Maintain the same high quality expected at every execution level.

## Behavior

- Inspect all directly relevant code and dependencies.
- Identify the likely root cause before making structural fixes.
- Implement a complete solution rather than a temporary patch.
- Preserve existing architecture unless changing it is clearly justified.
- Test the main flow plus important edge cases.
- Check nearby functionality likely to be affected.
- Use available tools efficiently and in parallel when possible.
- Avoid excessive research, commentary, and unrelated refactoring.
- Resolve ordinary implementation decisions independently.

Spend most of the time building and validating, not explaining. Finish once the requested behavior is implemented and verified.
