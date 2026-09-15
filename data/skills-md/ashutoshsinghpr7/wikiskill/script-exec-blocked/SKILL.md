---
name: script-exec-blocked
description: "Sandbox approval policy blocks execute_code and python3 -c; use read_file/write_file + manual transforms instead of retrying both runners."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [sandbox, execution, approval, file-tools]
    homepage: https://github.com/ashutoshsinghpr7/wikiskill
---

# Script Execution Blocked in Sandbox

## Problem

`execute_code` and `python3 -c` fail with "BLOCKED … single-query mode (-q)
runs without a user present to approve it". Plain terminal commands (grep,
ls, file, xxd) and file tools (read_file, write_file) still work.

## Fix

- Do NOT retry both runners back-to-back: a real task burned two turns on
  `python3 -c` then `execute_code` before falling back.
- Compute small transforms manually from the files you read; write the
  deliverable with write_file; verify by re-reading it.
- Keep parsing/sorting simple enough to verify by hand.

## Evidence

- Hit in 3/4 analyzed traces; all three recovered this way; the one failure
  was a spec-interpretation bug, not a tooling problem.
