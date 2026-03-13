---
name: docs-transloadit-robots
description: Offline lookup for Transloadit Robots and their parameter docs/examples via the `transloadit` CLI. Use to draft or validate `steps` JSON without guessing robot names/params.
---

# Search Robots (Offline)

```bash
npx -y @transloadit/node docs robots list --search import --limit 10 -j
```

Output shape:
- `docs robots list -j` prints a single JSON object: `{ robots: [{ name, title?, summary, category? }], nextCursor? }`

# Get Full Robot Docs (Offline)

Comma-separated:
```bash
npx -y @transloadit/node docs robots get /http/import,/image/resize -j
```

Output shape + error contract:
- `docs robots get -j` prints `{ robots: [...], notFound: string[] }`
- Exit code is `1` if `notFound` is non-empty, but JSON still includes partial results.

# Apply To Steps JSON

- Robot names map to: `steps.<stepName>.robot` (example: `"/image/resize"`)
- Param docs map to: `steps.<stepName>.<paramName>` keys.
