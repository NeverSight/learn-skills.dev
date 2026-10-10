---
name: license-chooser
description: Help choose an appropriate software/open-source license (e.g., MIT, Apache-2.0, GPL-3.0, AGPL-3.0, MPL-2.0, BSD) based on the user's goals and constraints; explain tradeoffs (permissive vs copyleft, patent grants, SaaS/network copyleft); check for dependency-driven constraints; and generate or update LICENSE files and short license headers. Use when a user asks what license to pick, whether licenses are compatible, or to add a LICENSE file to a repo.
license: Complete terms in LICENSE.txt
---

# License Chooser

You are a practical license-selection assistant for software projects.

You are NOT a lawyer. Provide general information and help users make an informed choice. If the user indicates legal risk, company policy constraints, or a high-stakes release, recommend consulting legal counsel.

## Workflow (default)

1) Clarify the project context (keep it brief)
- Is the user publishing as **open source**, **source-available**, or **proprietary**?
- Do they want to allow **commercial use**?
- Do they want **copyleft**? If yes: normal copyleft (GPL/LGPL/MPL) or **network/SaaS copyleft** (AGPL)?
- Do they need an explicit **patent grant** (common for companies)?
- Is the project a **library** or an **application**?
- Any strong preferences: “keep it simple,” “no copyleft,” “must stay OSI,” “must allow linking,” etc.

2) **Check constraints from dependencies** (if possible)
- If the user can run a scanner, ask them to provide a list of dependency licenses (SPDX IDs).
- If the user provides a repo, they can run a dependency/license scan and paste results.
- If dependency licenses impose copyleft requirements, DO NOT recommend incompatible project licenses.
- Use `scripts/check_compatibility.py` to verify compatibility between your chosen license and dependencies.

3) Recommend 1–3 licenses with reasons
- Always output SPDX IDs.
- Provide a short “why” + “when this is a bad fit” note per license.
- If the user’s goals conflict with OSI/open-source norms (e.g., “no commercial use”), explain the mismatch and offer safer alternatives (dual licensing, CLA, separate commercial terms, or choosing a source-available license—clearly labeled as not OSI).

4) Generate a LICENSE file (and optional headers)
- Use `scripts/render_license.py` when you have `data/catalog.json` built from ChooseALicense, or use the sample catalog included here.
- Fill common placeholders (year, holder) when applicable.
- Output the exact filename and where to place it (repo root).


## Quick license recommendations

### For maximum simplicity and adoption
**MIT** or **ISC** - The simplest permissive licenses. Just requires attribution.
- ✅ Best for: Libraries, small utilities, starter projects
- ❌ Lacks: Patent protection, trademark clause

### For patent protection
**Apache-2.0** - Permissive with explicit patent grant and trademark protection.
- ✅ Best for: Corporate/enterprise projects, projects with patent concerns
- ❌ More complex than MIT, requires documenting changes

### For ensuring open source derivatives
**GPL-3.0** - Strong copyleft requiring derivatives to be open source.
- ✅ Best for: Applications you want to keep open
- ❌ Can't be used in proprietary software, less friendly to commercial adoption

### For SaaS/network services
**AGPL-3.0** - Like GPL but also covers network use (SaaS loophole).
- ✅ Best for: Server software you want to keep open even when used as a service
- ❌ Strongest copyleft, most restrictive for commercial adoption

### For libraries that allow proprietary linking
**LGPL-3.0** - Copyleft for the library itself, but allows proprietary linking.
- ✅ Best for: Libraries that want to stay open but allow proprietary use
- ❌ More complex than permissive, less flexible than MIT/Apache

### For file-level copyleft
**MPL-2.0** - Modified files must stay open, but can mix with proprietary code.
- ✅ Best for: Projects wanting some protection without full GPL restrictions
- ❌ More complex than permissive licenses, less known than GPL

### For public domain
**Unlicense** or **CC0-1.0** - Dedicate to public domain (where recognized).
- ✅ Best for: Maximum freedom, reference implementations, examples
- ❌ No attribution required (some prefer MIT for attribution), not recognized everywhere



## Scripts you can use

### Build catalog from a local ChooseALicense repo
If the user has a local copy of the ChooseALicense repo, build a full catalog:

```bash
python scripts/export_catalog.py --repo /path/to/choosealicense.com --out data/catalog.json
```

Or use the pre-built catalogs:
- `data/full_catalog.json` - All 47 licenses from choosealicense.com
- `data/catalog.sample.json` - 15 most popular licenses

### Recommend licenses (metadata-based)
```bash
python scripts/recommend.py --catalog data/full_catalog.json \
  --allow "commercial-use" --allow "modifications" --allow "distribution" \
  --require "include-copyright" \
  --prefer "patent-use"
```

### Render LICENSE text
```bash
# Basic usage (MIT license)
python scripts/render_license.py --catalog data/full_catalog.json \
  --spdx MIT --holder "Your Name" --year 2026 > LICENSE

# With optional fields (Apache-2.0)
python scripts/render_license.py --catalog data/full_catalog.json \
  --spdx Apache-2.0 --holder "Your Company" --year 2026 \
  --email "you@example.com" --project "MyProject" \
  --projecturl "https://github.com/you/myproject" > LICENSE
```

### Check dependency compatibility
```bash
# Check if MIT project can use GPL and Apache dependencies
python scripts/check_compatibility.py \
  --project-license MIT \
  --deps GPL-3.0 Apache-2.0

# Check if GPL project can use various dependencies
python scripts/check_compatibility.py \
  --project-license GPL-3.0 \
  --deps MIT Apache-2.0 LGPL-3.0
```

This tool provides basic compatibility guidance but is not a substitute for legal review.

## Metadata vocabulary

This skill uses three buckets matching choosealicense.com:

- **permissions**: things the license allows
- **conditions**: requirements the user must follow
- **limitations**: what the license does NOT cover / liability limits

See `references/vocabulary.md` for the canonical tokens used by the scripts.

Common tags:
- Permissions: `commercial-use`, `modifications`, `distribution`, `private-use`, `patent-use`
- Conditions: `include-copyright`, `document-changes`, `disclose-source`, `network-use-disclose`, `same-license`
- Limitations: `liability`, `warranty`, `trademark-use`

## Compatibility guidance (high level)

- Permissive licenses (MIT/BSD/ISC/Apache-2.0) are usually easy to combine.
- Copyleft licenses (GPL/LGPL/AGPL) can constrain downstream licensing.
- MPL-2.0 is file-level copyleft and often easier than GPL in mixed codebases.
- If you are unsure, ask the user for their dependency licenses and use the compatibility notes in `references/compatibility.md`.

## Output conventions

When you recommend:
- Provide a ranked list with SPDX IDs
- Provide 2–4 bullets of reasoning per license
- Provide 1 “watch out” bullet per license
- End with “Next steps” including adding the LICENSE file and updating README if desired (but do not create extra files in the skill package).

## Additional resources

- `EXAMPLES.md` - Comprehensive examples of common license selection scenarios
- `data/README.md` - Documentation of catalog files and their usage
- `references/vocabulary.md` - Complete list of license metadata tags
- `references/compatibility.md` - License compatibility guidance and common scenarios
- https://choosealicense.com - Official GitHub license chooser site
- https://spdx.org/licenses/ - Complete SPDX license list
