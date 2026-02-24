---
name: gitlab-create-merge-request
description: >
  Create a GitLab merge request using glab CLI with the first commit message
  as the title. Use when the user asks to open an MR for the current branch
  targeting main, or after completing work that needs review.
---

# Create Merge Request

Create a GitLab merge request for the current branch targeting `main`.

## Steps

1. Get the first commit message of the current branch (compared to main):

   ```bash
   git log main..HEAD --reverse --format="%s" | head -n 1
   ```

2. Create the MR using glab:
   ```bash
   glab mr create -t "<FIRST_COMMIT_MESSAGE>" -d "<SUMMARY_OF_WHAT_HAS_BEEN_DONE>" -b main --fill -y
   ```

## Notes

- Ensure the branch has been pushed before running this command
- The MR title will be the first commit message of the branch
