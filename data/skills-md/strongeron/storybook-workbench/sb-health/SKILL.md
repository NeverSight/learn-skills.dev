---
name: sb-health
description: "Check design-system health for a React+Vite app — raw hex, undefined/unused tokens, scale gaps, DESIGN.md drift, and (opt-in) property→token-family misuse. Use for 'is my design system healthy', 'find raw colors', 'check tokens', or a mixed design system."
compatibility: "Requires bash and python3; reads sb-inventory's project-inventory.json for unused-token (run sb-inventory first); Node.js + stylelint optional for the stylelint pass; property→token-family is opt-in via a designer-owned design-system/lint/colors.json."
allowed-tools: Bash Read Glob Grep Write
license: MIT
metadata:
  author: strongeron
  version: '2.3.0'
  bundle: storybook-workbench
  vendor:
    scripts: [validate-design-system.sh, check-property-tokens.py, scaffold-wrapper.sh]
    wrappers: [DesignSystemHealth]
    references: [colors.schema.json, colors.example.json]
---

# sb-health — design-system health gate

The browser can't shell out, so the script runs the checks and writes JSON the wrapper renders.
`design-system-health.json` is a **rendered** output (Health Docs + DesignSystemHealth/TokenMatrix), so
`refresh-usage.sh` re-runs this check with the other rendered extractors — see `CONTEXT.md` §STORAGE MAP.

## Run it

```bash
SKILL=${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}
CORE=${CLAUDE_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}
"$SKILL/scripts/validate-design-system.sh"       # → .storybook/design-system-health.json
# --emit-prompt  also outputs an LLM sub-agent prompt for semantic checks
#                (naming drift, semantic-vs-presentational, scale clarity)
"$CORE/scripts/scaffold-wrapper.sh" DesignSystemHealth   # → .storybook/wrappers/ (+ icons.tsx)

# Opt-in property→token-family check (off until a designer authors the rules file):
"$SKILL/scripts/check-property-tokens.py" --init   # scaffold design-system/lint/colors.json (+ schema)
```

## What it checks

- **raw-color** — hex/rgba/hsl literals in components (should be tokens). When the literal's value EQUALS
  an existing token's resolved value (e.g. `#005596` on a tile whose siblings use `bg-secondary` →
  `--secondary` resolves to `#005596`), the fix is to **adopt that exact token**, not invent a new one —
  the finding names the matching token when it can resolve one, so the fix is "replace with `--x`", not "add a token".
- **undefined-token** — components reference `--foo` that's not declared
- **scale-gap** — spacing/type scale has unexpected jumps
- **unused-token** — declared but never referenced (var, Tailwind utility, or custom `@utility`).
  Read from sb-inventory's single source (`.storybook/project-inventory.json` → `tokens.map`),
  not re-scanned here, so health, inventory, and the token views never disagree. Run `sb-inventory`
  first; if the file is absent this check is skipped.
- **design-md** — a `DESIGN.md` (Google Labs YAML-tokens-plus-markdown, an increasingly common way to
  brief agents on a visual identity) is a **claim, not ground truth** — like `AGENTS.md` it drifts as
  the code changes, or was wrong from the start. The script finds it and cross-checks the colors it
  *claims* against the colors the code's CSS tokens actually *declare*, emitting `design-md-drift` for
  each claimed color the code doesn't define. Treat a present `DESIGN.md` as untrusted until reconciled.
- **property-token-family** *(opt-in)* — a *valid, declared* token used on the **wrong property family**
  (e.g. `color: var(--color-container)` — a container token used as text color). raw-color catches "no
  token at all"; undefined-token catches "token doesn't exist"; this catches "real token, wrong slot."
  Off until a designer authors `design-system/lint/colors.json` (see below), so the zero-config default
  is preserved. Findings are `warning`/`info` only — an opt-in never flips a green CI build red.
- runs `stylelint` if configured

Report `summary` (errors/warnings/info counts) and the top findings. The `DesignSystemHealth`
wrapper renders severity with the shared icon set (no emoji).

The JSON it writes (shape — read these fields, don't re-derive). Each finding is
`{kind, severity, message, file?, line?, fix?}`; `summary` rolls up the counts:

```jsonc
{
  "findings": [
    { "kind": "raw-color",       "severity": "error",   "file": "Button.tsx", "line": 42, "message": "#3b82f6 literal", "fix": "use --color-primary" },
    { "kind": "undefined-token", "severity": "error",   "file": "Card.tsx",   "line": 11, "message": "--surface-2 not declared" },
    { "kind": "design-md-drift", "severity": "warning", "message": "DESIGN.md claims #1e90ff; no token declares it" },
    { "kind": "unused-token",    "severity": "info",    "message": "--legacy-accent declared, never referenced" },
    { "kind": "scale-gap",       "severity": "info",    "message": "spacing jumps 16px → 48px" },
    { "kind": "property-token-family", "severity": "warning", "file": "Card.css", "line": 3, "message": "background uses --color-content — not allowed for 'background*' (expects --color-container / --color-canvas)", "fix": "Use one of --color-container, --color-canvas, or remap with /* color-lint-alias: … */" }
  ],
  "summary": { "total": 6, "errors": 2, "warnings": 2, "info": 2, "checksRun": ["raw-color", "undefined-token", "..."] }
}
```

### Property→token-family rules (opt-in, designer-owned)

The which-token-family-belongs-on-which-property logic is **design intent**, so it lives in a
designer-editable rules file — not in the script. The designer owns the rules; the dev owns the linter.
Scaffold it once (writes the file **and** a JSON Schema so it's self-documenting in any editor):

```bash
"$SKILL/scripts/check-property-tokens.py" --init    # → design-system/lint/colors.json (+ colors.schema.json)
```

```jsonc
// design-system/lint/colors.json — owned by the designer
{
  "$schema": "./colors.schema.json",
  "propertyTokens": {
    "color":       ["--color-content"],                                   // exact property
    "background*": ["--color-container", "--color-canvas", "--color-backdrop"], // family (trailing *)
    "box-shadow":  ["--color-border", "--color-shadow"],
    "border*":     ["--color-border"]                                     // values are token PREFIXES
  }
}
```

Only properties listed are governed (opt in one property at a time). Escape hatches, in order of
preference — both are read from your source files:

```css
/* color-lint-alias: --color-theme --color-container */  /* file-level prefix remap: a token is
                                                            semantically right but lives in the "wrong"
                                                            family — treat this prefix as that one */
color: var(--color-theme-fg); /* color-lint-ignore */    /* per-line suppression — counted, and the
                                                            report nudges a refactor past 10. The number
                                                            growing is the signal: mute fast, fix slowly. */
```

The rules file is itself a **claim, not ground truth** (same stance as `DESIGN.md`): if a rule allows a
token-prefix that *no declared token matches*, the script emits `property-rules-drift` so a stale config
can't silently pass — or silently mis-flag.

**Triage order — severity is the verdict, not the count:** fix `error` first (raw-color → map to an
existing token; undefined-token → declare it or fix the typo), *reconcile* `warning` (design-md-drift
→ hand to `design-md`; property-token-family → swap to an allowed token, or if the token is genuinely
right add a `color-lint-alias`; property-rules-drift → fix the rules file), and **report `info` as-is**
(unused-token / scale-gap / property-lint-suppressions are signals to verify, never auto-fixes — see
Never below). A repo with 0 errors and 20 info findings is *healthy*.

## Never (and the non-obvious why)

- **NEVER delete an `unused-token` on sight** — it is `info`, not `error`. A static scan can't see a
  token consumed by a Tailwind utility (`bg-[--brand]`), a runtime `var()` built by string concat, or
  a sibling app in the monorepo. "Unused" means "I didn't find a reference," not "safe to remove."
- **NEVER treat `scale-gap` as a failure to fix** — it's `info`. Real scales have intentional jumps (a
  display size far above body); "smoothing" them invents tokens nobody asked for and breaks the rhythm
  a designer chose.
- **NEVER trust `DESIGN.md` as ground truth** — it's a *claim*, like `AGENTS.md`/`CLAUDE.md`, and drifts.
  Reconcile against `design-md-drift` first; an un-reconciled DESIGN.md will confidently lie about colors
  the code doesn't define.
- **NEVER "fix" a `raw-color` by inventing a new token** — map it to an *existing* token. A fresh token
  per literal just relocates the mess into the token layer (more undefined-token noise next run).
- **NEVER hand-recompute this JSON by re-grepping** — the browser can't shell out, so the script is the
  single source; cite its fields. Re-deriving by eye is how the counts drift from what the wrapper renders.

## When to defer

For **extraction** (turning a messy codebase into tokens + components), this skill only *measures*.
To actually extract, run `/ds-runbook` → `/ds-audit` → `/ds-token-extract` → `/ds-component-extract`,
then come back here to verify health and to `sb-stories` for capture.

For a **`DESIGN.md`** that drifted (or to author/regenerate one *from* the code's real tokens), hand
off to the **`design-md`** skill — it composes, extracts, and deep-audits the Google Labs DESIGN.md
format. `sb-health` only flags the drift; `design-md` reconciles or rewrites the brief.

## Next

If health is poor and the project is in transition, fix tokens (or route to ds-* skills) before
authoring stories. Otherwise append a finding and continue to `sb-stories`.
