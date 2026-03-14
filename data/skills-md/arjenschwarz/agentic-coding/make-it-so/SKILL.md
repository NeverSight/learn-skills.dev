---
name: make-it-so
description: 4. Make it so (implement all tasks)
---

### 4. Make it so (implement all tasks)

Implement all the remaining tasks from the spec.

**Constraints:**

**Task Retrieval:**
- The model MUST use the rune skill to retrieve the next tasks to work on
- Use `rune next --phase --format json` to get the next incomplete phase to work on.

**Task Execution:**
- The model MUST read all files referenced in the front_matter_references and any additional references included in the task
- The selected tasks MUST be added to the internal TODO list for tracking and implemented in the order specified
- The model MUST implement all of the selected tasks, including all subtasks
- Once a subtask or task is completed, use the rune skill to mark it complete (e.g., `rune complete 1.1`)
- Use tools and skills as appropriate while implementing the task. For example, if you need to know the capabilities of a library, use context7, and if you want to verify your code is efficient, use the efficiency-optimizer skill

**Review**
- Once a phase is completely implemented, use the design-critic skill to look over the implemented work and verify that it's correct. Issues detected should be fixed or updated in the decision log.

**Commit**
- After the review, the code needs to be committed using the below process.

1. Run all formatting and test commands.
2. Use the command line to get an overview of the staged git changes. If no changes are staged, stage all files. If running the formatting resulted in unstaged changes to files, stage these as well. DO NOT revert code changes unless specifically asked to do so.
3. Create a concise, well-documented summary of the changes in the format as defined at keepachangelog.com, excluding any changes to the changelog file itself. Use proper formatting and be specific about the changes. Ignore the marking of tasks as complete.
4. Read the CHANGELOG.md file, if the file does not exist, create it.
5. Verify if the summary is already present in the changelog, if not add it to the top of the file.
6. Add the changelog to staged commits
7. Verify the current git branch using the git command.
8. Extract any ticket numbers from the branch, check for the below options based on what is likely.
    a. Extract the JIRA ticket number from the branch. The ticket number will be in the format ABC-123 and will be the combination of 3-5 letters or numbers, a -, and 1-5 numbers. This will be at the start of the branch name, possibly preceeded by something like feature/ or hotfix/.
    b. Check for a pure number, this would likely reflect a GitHub Issue.
9. If a ticket number was found, use this as the commit message prefix, otherwise use [feat] / [bug] / [doc] as appropriate based on any prefixes in the branchname and/or the code changes
10. Summarise the changes into a multi-line detailed commit message, prefixed with the commit message prefix and :. Do NOT include any co-authored-by information in the commit message.
11. Commit the code

**Compact**
- After the commit, run `/compact` with instructions that preserve only the `/make-it-so` skill context
- Use this exact format: `/compact Continuing /make-it-so - implement the next phase. Current progress: [brief summary of completed phase]`
- After compaction completes, immediately continue executing `/make-it-so` to implement the next phase
