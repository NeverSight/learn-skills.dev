---
name: review-git-workdir
description: Review Git working directory.
---

Do the code review of the current state of the git working directory. Use `git status` command to see changed files.

- Ignore code generation artifacts like protobuf generated files, and similar.
- Ignore files with `.gensum` file extension.
- Pay attention to any left out debug statements, code that's left commented out, unused code, and any other potential issues.
