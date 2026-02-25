---
name: license-checker
description: Audits node_modules for package licenses. Uses bash to resolve SPDX IDs without reading file contents into context. LLM inference is a last resort for a small residual set.
author: DigitalSpeed
---

# License Checker

Scan all packages in `node_modules` and produce a license compliance report. **Never read raw file contents into context** — use bash to pattern-match first; only buffer the irreducible unknown set.

## 1. Execution Workflow

**Step 1 — Bulk resolve (single bash call, handles scoped packages, zero file reads in context):**
```bash
SPDX='MIT|ISC|BSD-[0-9]+-Clause|Apache-2\.0|GPL-[23]\.0(-only|-or-later)?|LGPL-[23]\.0|AGPL-3\.0|MPL-2\.0|Unlicense|CC0-1\.0|CDDL-1\.[01]|EPL-[12]\.0|EUPL-1\.[12]'

find node_modules -mindepth 2 -maxdepth 3 -name 'package.json' \
  ! -path '*/.bin/*' ! -path '*/node_modules/*/node_modules/*' | while read pjson; do
  dir=$(dirname "$pjson")
  row=$(jq -r '[.name, .version, (.license // (.licenses | if type=="array" then map(.type//"") | join(" OR ") else (.//"") end) // ""), (.repository.url // .repository // "")] | @tsv' "$pjson" 2>/dev/null)
  lic=$(printf '%s' "$row" | cut -f3)
  if [ -z "$lic" ]; then
    lfile=$(find "$dir" -maxdepth 1 \( -iname 'license*' -o -iname 'licence*' -o -iname 'copying*' \) 2>/dev/null | head -1)
    match=$(grep -iom1 -E "$SPDX" "$lfile" 2>/dev/null | head -1)
    if [ -n "$match" ]; then
      printf '%s\t%s*\tgrep\n' "$(printf '%s' "$row" | cut -f1-2,4)" "$match"
    else
      printf '%s\tUNKNOWN\t—\n' "$(printf '%s' "$row" | cut -f1-2,4)"
    fi
  else
    printf '%s\tpackage.json\n' "$row"
  fi
done
```
Output is TSV: `name  version  license  repository`. Rows where license is `UNKNOWN` proceed to step 2.

**Step 2 — LLM inference for residual unknowns only:**
For each `UNKNOWN` package, read the first **500 chars** of its license file (or README if absent). Apply:
```
SPDX ID only. Append * if inferred from file (not package.json). Text:
[500-char buffer]
```

**Step 3 — Render report** using the format in §2.

## 2. Output Format

Tree format sorted alphabetically by `name@version`. An `*` suffix on a license means it was inferred from a file, not `package.json`.

```
├─ lodash@4.17.21
│  ├─ repository: https://github.com/lodash/lodash
│  └─ licenses: MIT
├─ some-lib@1.2.0
│  ├─ repository: https://github.com/some/lib
│  └─ licenses: GPL-3.0*
└─ ghost-pkg@1.0.0
   └─ licenses: UNKNOWN
```

Omit the `repository` line if the field is empty. Use `├─` for all entries except the last, which uses `└─`. Sub-fields always use `│  ├─` / `│  └─` (or `   ├─` / `   └─` under a `└─` parent).

Summary line after the tree:
```
Scanned: N  |  Confirmed: N  |  Inferred (*): N  |  Unknown: N
⚠️  Copyleft: [packages with GPL / LGPL / AGPL / MPL / EUPL licenses]
```
