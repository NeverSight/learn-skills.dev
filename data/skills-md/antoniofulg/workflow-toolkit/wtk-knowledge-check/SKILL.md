---
name: wtk-knowledge-check
description: Check `knowledge/` for source drift, naming, conformance, and harvested gaps. Use when verifying a knowledge bundle.
---

# Knowledge Check

Run the bundled read-only checker from the consuming project root:

```bash
bun .agents/skills/wtk-knowledge-check/scripts/cli.ts [project-root]
```

The checker reports knowledge findings and exits non-zero only for errors. Read the project's
`knowledge/AGENTS.md` before editing knowledge; this skill owns checking, while that policy owns
the bundle's frontmatter and write boundaries.
