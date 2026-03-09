---
name: engram-docs-alignment
description: >
  Documentation alignment rules for Engram.
  Trigger: Any code or workflow change that affects user or contributor behavior.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

Use this skill when:
- Changing APIs, setup flows, or plugin behavior
- Updating CLI commands or examples
- Writing contributor guidance

---

## Alignment Rules

1. Docs must describe current behavior, not intended behavior.
2. Update docs in the same PR as the code change.
3. Validate examples before publishing.
4. Remove references to deprecated files, endpoints, or scripts.

---

## Verification

- [ ] Endpoint names match server routes
- [ ] Script names match repository paths
- [ ] Command examples execute as documented
- [ ] Cross-agent notes are still accurate
