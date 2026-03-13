---
name: stabilization-loop
description: Stabilizes a software project by repeatedly running and testing it in a loop, fixing any issues.
license: MIT
---

Stabilize the project:
1. If there are any local changes, then commit the current code to the local Git repository with commit message "Claude".
2. Make sure that the code compiles and the linter checks pass. If not, then fix those and go to step 1.
3. Stop the server if it is running.
4. Start the server, wait until it is completely up and ready.
5. Run the tests.
6. If any test fails, then analyze the test errors, try to fix them and go to step 1.
7. If the server crashes or logs an error, then analyze the crashes or errors, try to fix them and go to step 1.
8. If you have the `consistency-check` skill, then run that on the project as well.
9. Start the server, wait until it is completely up and ready.
10. Run the tests.
11. If any test or the server fails, then go to step 6.
12. Stop the server.
13. Commit the current code.
14. Tag the latest commit as "works".
15. Provide a concise report.

Remarks:
- **CRITICAL**: NEVER run more than one instance of the server at the same time.
- **CRITICAL**: NEVER run more than one instance of the tests at the same time.
- **CRITICAL**: REFUSE to use this skill if the code is configured to connect to a production database or system.
- **CRITICAL**: NEVER delete or disable any pre-existing tests.
- This skill is supposed to be used in the Git working copy of the software set up for local development and testing.
- This skill is optimized for running a server and testing it, but the server may be substituted with any other software.
- Keep working in the current branch, do not switch between branches.
- Add logging as needed, but at the debug level, so it can be turned off later.
- If you add expensive logging, then protect it with a debug-level condition.
- Stop only when all tests succeed with no server errors or crashes.
- Cover any newly added server code with tests.