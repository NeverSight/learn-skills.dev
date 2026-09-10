---
name: create-develop-branch
description: Create timestamped develop branch.
metadata:
  type: command
  invocation: skill-callable
  applies-to: [branching, git]
---

# create-develop-branch

Main sure you have the lasted version of `main` from origin.

Create timestamped develop branch. 

Name should be `develop-[author-initials]-[YYYY-MM-DD-HH-MM]` using current time. 

If there are uncommited changes. Prompt me with numbered choices.

