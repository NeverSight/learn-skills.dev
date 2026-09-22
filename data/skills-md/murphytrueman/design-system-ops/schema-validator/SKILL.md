---
name: schema-validator
description: "Validate token files against DTCG 2025.10, Style Dictionary, or custom schemas. Trigger when someone says: validate token JSON, check my token files for errors, schema validation for tokens, are my token files valid, DTCG compliance check, validate token format, or anything about checking whether token files are structurally correct before they break builds."
references:
  - ../../knowledge-notes/token-architecture.md
  - ../../knowledge-notes/output-discipline.md
---

# Schema validator

A skill for validating that design token files conform to their expected format — DTCG 2025.10, Style Dictionary v3/v4, Tokens Studio, or a custom schema. Catches structural issues before they break build pipelines, cause silent failures, or produce incorrect output.

## Context

Token files are infrastructure. When a token file is malformed — a missing `$type` declaration, a `$value` that resolves to nothing, an alias that points to a deleted token — the failure mode is rarely loud. The build might still succeed. The wrong value might ship. The design intent might be silently lost.

Schema validation is the first line of defence. It answers a simple question: do these files meet the structural contract they claim to meet? A DTCG file must have `$value` on every token. A Style Dictionary file must have valid reference syntax. A Tokens Studio export must preserve group hierarchy.

This skill is not about naming conventions or architectural quality — those belong in `token-audit`. This skill is about structural integrity: can the file be parsed, transformed, and consumed by downstream tools without error?

## Boundaries

This skill validates token file structure only. It does not assess naming quality (use `naming-audit`), token architecture health (use `token-audit`), or token usage in code (use `token-compliance`). If the token source format is not recognisable as DTCG, Style Dictionary, Tokens Studio, or a declared custom schema, ask the user to identify the format before proceeding. If no token files are provided or accessible, there is nothing to validate — stop and confirm the file location with the user.

---

## Configuration

Check for `.ds-ops-config.yml` in the project root. If present, load:
- `system.token_format` — pre-selects the primary format to validate against (dtcg, style-dictionary-v3, style-dictionary-v4, tokens-studio, custom)
- `integrations.style_dictionary` — if enabled, use Style Dictionary's built-in validation as a cross-check
- `severity.schema_*` — overrides for finding severity (e.g. `schema_missing_type: critical`)

## Auto-pull integrations

**Style Dictionary v4** (`integrations.style_dictionary.enabled: true`):
- Run `npx style-dictionary build --config [path] --dry-run` to get Style Dictionary's own validation errors
- Cross-reference Style Dictionary errors with this skill's findings for completeness

If no config exists, proceed with defaults.

---

## Step 1: Identify files and target format

Ask for or confirm:

1. **Path to token files** — directory or specific files to validate
2. **Target format** — which specification to validate against:
   - **DTCG 2025.10** (W3C Design Token Community Group specification)
   - **Style Dictionary v3** (legacy JSON with `value` property)
   - **Style Dictionary v4** (JSON with DTCG alignment, `$value` property)
   - **Tokens Studio** (Figma Tokens plugin export format)
   - **Custom** — if custom, ask for the schema or describe the expected structure
3. **Strictness level** — strict (every violation is an error) or lenient (warnings for non-critical issues)

If the token files contain format indicators (e.g., `$type` fields suggest DTCG), auto-detect the format and confirm with the user.

## Step 2: Parse and inventory

For each file in the provided path:

1. **Attempt to parse** — JSON, YAML, JS module, or CSS custom properties
2. **Record parse status** — parsed successfully, failed with error, or empty file
3. **Count tokens** — total token definitions found
4. **Identify format signals** — which format the file appears to use (based on property names, structure)

Produce the file inventory:

| File | Format detected | Tokens | Parse status |
|------|----------------|--------|-------------|
| colors.json | DTCG 2025.10 | 47 | ✓ Parsed |
| spacing.json | Style Dictionary v3 | 12 | ✓ Parsed |
| broken.json | Unknown | 0 | ✗ Parse error: unexpected token at line 23 |

## Step 3: Validate against target format

For each successfully parsed file, run format-specific validation:

### DTCG 2025.10 checks

1. **$value required** — every leaf token must have a `$value` property
2. **$type present** — every token must declare `$type` (or inherit from a parent group's `$type`)
3. **$type values valid** — must be one of: color, dimension, fontFamily, fontWeight, duration, cubicBezier, number, strokeStyle, border, transition, shadow, gradient, typography, fontStyle
4. **$description optional but typed** — if present, must be a string
5. **Alias syntax correct** — aliases must use `{group.token}` syntax with curly braces
6. **Alias targets exist** — every alias must resolve to a real token (no broken references)
7. **No circular aliases** — alias chain must terminate at a concrete value
8. **Composite token structure** — composite types (border, shadow, typography, transition, gradient) must have correct sub-properties
9. **Color values valid** — hex, RGB, HSL, or named colour that resolves correctly
10. **Dimension values valid** — number + unit (px, rem, em, etc.)
11. **Group $type inheritance** — if a group declares `$type`, all children without their own `$type` inherit it
12. **No `$` prefix on non-spec properties** — custom properties should not start with `$` to avoid confusion with spec properties
13. **Extensions namespace** — custom metadata should live under `$extensions` if present

### Style Dictionary v3 checks

1. **`value` required** — every leaf token must have a `value` property (not `$value`)
2. **Reference syntax** — aliases use `{group.token.value}` with `.value` suffix
3. **Reference resolution** — all references resolve to existing tokens
4. **Category-Type-Item (CTI)** — if using CTI convention, validate hierarchy consistency
5. **No reserved property collisions** — `value`, `original`, `name`, `comment`, `themeable`, `attributes` are reserved

### Style Dictionary v4 checks

All DTCG checks above, plus:
1. **DTCG alignment** — v4 uses `$value` and `$type` (not legacy `value`)
2. **Preprocessor compatibility** — if preprocessors are configured, validate custom property shapes
3. **Platform-specific overrides** — if present, validate they follow the platform config schema

### Tokens Studio checks

1. **Group hierarchy preserved** — nested groups maintain parent-child relationships
2. **Token types valid** — type field matches Tokens Studio's type system (color, borderRadius, sizing, spacing, opacity, borderWidth, boxShadow, fontFamilies, fontWeights, lineHeights, fontSizes, letterSpacing, paragraphSpacing, textDecoration, textCase, composition, other)
3. **Math expressions valid** — if tokens use math expressions (`{size.base} * 2`), validate syntax
4. **Reference syntax** — uses `{group.token}` without `.value` suffix
5. **Set structure** — if multi-set, validate set names and token assignments
6. **Theme configuration** — if themes are defined, validate theme-to-set mappings

## Step 4: Cross-format consistency

If files use multiple formats (common during migration):

1. **Identify format boundaries** — which files are which format
2. **Flag inconsistencies** — same token in two formats with different values
3. **Migration readiness** — if migrating from v3 to DTCG, how many files still need conversion

## Step 5: Produce the validation report

Structure the report as:

```
# Token Schema Validation Report

## Summary
- Files scanned: X
- Files valid: Y
- Files with errors: Z
- Target format: [DTCG 2025.10 / Style Dictionary v3 / etc.]
- Strictness: [strict / lenient]

## File Inventory
[Table from Step 2]

## Validation Results

### ✓ Valid Files
[List each valid file with token count]

### ✗ Files with Errors

#### [filename.json]
| # | Check | Status | Detail | Fix |
|---|-------|--------|--------|-----|
| SV-01 | $type required | ❌ FAIL | 3 tokens missing $type: `color.brand.accent`, `spacing.page.gutter`, `font.body.size` | Add `$type: "color"`, `$type: "dimension"`, `$type: "fontFamily"` respectively |
| SV-02 | Alias resolution | ❌ FAIL | `{color.legacy.blue}` referenced by `color.semantic.info` does not exist | Either create `color.legacy.blue` or update the reference to `{color.primitive.blue.500}` |

### ⚠️ Warnings
[Non-critical issues: missing $description, custom $ properties, etc.]

## Format Compliance Score
- DTCG 2025.10: X% compliant (Y/Z checks pass)
- [If migrating] Legacy tokens remaining: N files, M tokens

## Recommendations
[Prioritised list of fixes, grouped by: parse errors first, then broken references, then missing declarations]
```

## Step 6: Produce machine-readable output (optional)

If the user requests it or if the output will feed into another tool:

```json
{
  "format": "dtcg-2025.10",
  "files_scanned": 12,
  "files_valid": 10,
  "files_invalid": 2,
  "findings": [
    {
      "id": "SV-01",
      "file": "colors.json",
      "token": "color.brand.accent",
      "check": "$type_required",
      "status": "FAIL",
      "fix": "Add $type: \"color\""
    }
  ]
}
```

---

## Quality checks

Before delivering the report, verify:

1. **Every file in the path was scanned** — no files skipped without explanation
2. **Parse errors include line numbers or error positions** — not just "invalid JSON"
3. **Fix suggestions are specific and copy-pasteable** — not "add the missing type" but "add `$type: \"color\"` to token `color.brand.accent`
4. **Compliance summary denominator matches total applicable checks** — if a check doesn't apply (e.g., no composite tokens), it's excluded from the count
5. **Alias chains are fully traced** — broken reference errors identify the full chain, not just the immediate reference
6. **Cross-format issues are flagged** — if the same token exists in two files with different formats, this is noted
7. **Findings reference specific token names and file paths** — never "some tokens are missing types"

## Small-system note

For systems with fewer than 5 token files: run the same validation but present results as a single-page summary rather than a per-file breakdown. Include the specific fix for every single issue rather than grouping by pattern.
