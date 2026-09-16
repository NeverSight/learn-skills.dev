---
name: workdir
description: Use when an agent needs the configured Tariboy workdir path for a command or file outside its current directory.
---

# Workdir

Only a literal `workdir: /absolute/path` runtime line in the current prompt
defines the configured path. A harness working directory, current directory,
Git, or environment variable does not. If the line is absent, request the path
and stop.

Resolve workdir-relative commands to absolute paths. For a Tariboy script
operation, respond with the resolved absolute path and: "Use the `scripts`
skill for this operation."
