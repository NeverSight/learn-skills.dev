---
name: json-diff
description: Semantic diff between two JSON documents reported by JSON path — added, removed, changed with old/new values, recursing nested objects and comparing arrays positionally. Use when `diff` on JSON is useless (key reordering, formatting noise), for config drift checks, API response comparison, or CI gates on expected output.
when_to_use: Comparing configs across environments, golden-file API tests, verifying a migration produced exactly the intended changes. NOT a schema validator; it compares two concrete documents, not a document against a schema.
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [json, diff, config, testing, ci-gate]
---

# JSON Diff

`diff` on JSON is useless — one reordered key and everything flags. This
parses both documents and reports what actually changed, by path.

## Commands

```bash
python3 scripts/json_diff.py old.json new.json
python3 scripts/json_diff.py a.json b.json --json
python3 scripts/json_diff.py expected.json actual.json --max-changes 0
curl -s api/v1/config | python3 scripts/json_diff.py - prod-config.json
```

## Output

```
~ port: 8080 -> 9090
+ db.ssl: true
- legacy_mode: false
~ tags: array[2] -> array[3]
```

Paths use dot notation for objects (`db.host`) and brackets for arrays
(`items[2]`). `--max-changes N` makes it a CI gate: exit 1 when the count
exceeds N (use 0 for "must be identical").

## Pairs with

`env-gate` (config completeness), `api-tester` (fetch the JSON this diffs),
`verification-before-completion` (the discipline that makes you run it).
