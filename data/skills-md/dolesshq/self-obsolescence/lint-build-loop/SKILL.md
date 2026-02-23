---
name: lint-build-loop
description: Run `npm run lint && npm run build` in a loop, fixing errors until both succeed. Use when the user asks to iterate on lint/build failures.
metadata:
  short-description: Loop lint + build
---

# Lint + Build Loop

## Goal

Repeatedly run `npm run lint && npm run build`, fix any errors that appear, and rerun until both commands succeed.

## Workflow

1. **Confirm working directory**
   - Run in the project root that contains the `package.json` the user intends.
   - If multiple roots exist, ask the user to choose.

2. **Run the loop**
   - Execute `npm run lint && npm run build`.
   - If it fails, read the error output, fix the underlying issues, and rerun the same command.
   - Continue until the command exits successfully.

3. **Failure handling**
   - If the same error repeats after fixes, pause and ask the user for guidance.
   - If a fix is ambiguous or risky, explain the tradeoff and ask before proceeding.

4. **Reporting**
   - Summarize the fixes made and confirm the final successful run.
   - Provide the exact command used and the directory it was run in.
