---
name: build-and-ship
description: Builds a project and Ship it to the target environment
---

# Build and Ship

This skill is a step of feature development. 
This skill builds a codebase, makes sure that all tests pass and ship it to the target environment. 

---

## The Workflow

You **must always strictly** follow this workflow when building and shipping a feature:

1. Build the project 
2. Run the tests. If tests fail, understand the problem and go back to Phase 2. 
3. Clean up task files and update feature documentation (see below). **Commit and push** after that. 
4. Depending on whether you are shipping a *Feature* or a *Fix*: 
  - If shipping a *Feature*: update the Feature markdown file with an "Implemented" badge: `![Status](https://img.shields.io/badge/status-implemented-brightgreen?style=flat-square)`. This is **IMPORTANT**. Also update the `README.md` file in the `docs/features` folder, that contains the map of all features (index).
  - If shipping a *Fix*: update any Feature markdown file to which this fix is linked by closing any Open Point that was pointing at this fix. Make sure the Feature document is up-to-date with this fix. *Note that you will find any linked Feature in the GitHub issue that the Fix is solving*.
5. Open a Pull Request. **Always** open a PR when you are done.
6. Link the Github issue to the PR 

**Expected Output:**
The PR you have created.

## Acceptance Criteria

- [ ] The project builds
- [ ] The project's tests all pass
- [ ] Feature markdown files are updated with resolved open questions and non-obvious API/domain decisions
- [ ] A PR has been open 
- [ ] The GitHub issue has been linked to the PR so that when the PR is merged by the user, the issue automatically closes
- [ ] If shipping a *Feature*: the Feature markdown file has been updated with the "Implemented" badge

**Red Flags:**
Any of these behaviour or sentences are a **BIG** problem and mean that something is going wrong. Stop and rethinking what you should be doing. 
- Please proceed with the full implementation as planned. Do not wait for confirmation — implement all files now
- You are re-implementing a whole feature from its spec when a change record indicated only a delta needed to be applied.
- You applied the additions and modifications from a change record but **skipped the removals**.