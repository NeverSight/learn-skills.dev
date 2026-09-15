---
name: verify-output-readback
description: "After write_file, re-read the deliverable (or ls + hexdump/line-print) and re-check the last format clauses before finishing."
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [verification, deliverables, write_file, readback]
    homepage: https://github.com/ashutoshsinghpr7/wikiskill
---

# Verify Deliverable by Re-Reading

## What passing agents did

- After `write_file`, always re-read the deliverable (or `ls` + hexdump /
  line-print) to confirm exact content, line count, and absence of trailing
  blank lines before finishing.
- Re-checked the last format clauses (header? separator? case? final
  newline?) against the spec one more time.
- A `find-secret` run verified the payload was exactly `data.log` (8 bytes).

## When to use

Any task graded by exact-match output comparison — the readback is the
difference between a byte-exact pass and a silent 0.0.
