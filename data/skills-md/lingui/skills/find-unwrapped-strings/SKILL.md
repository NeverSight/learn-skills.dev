---
name: find-unwrapped-strings
description: Audit a Lingui project for hardcoded user-facing strings that were never wrapped in macros. Use when asked to find untranslated, unwrapped, or hardcoded strings, to check i18n coverage, to audit what an i18n setup or migration missed, or when text renders in the source language after everything was supposedly translated.
---

# Find Unwrapped Strings

## When to run this

- After a Lingui setup or a migration onto Lingui — both wrap what they touch, and neither proves the rest of the codebase was touched.
- When the report is "the build is green and the catalogs are full, but this screen still shows English in every locale."
- As a periodic coverage audit on a project where i18n is already established.

The misses are systematic, not random. Strings in JSX get wrapped because they look like UI; what survives is display copy that doesn't — inside data modules (`export const products = [{ name: "AeroPress Go" }]`), message maps in toast and error helpers, labels in config objects.

**The scan is over-inclusive by design.** Precision comes from judging each hit against the skip-list, never from tuning the scanner until it goes quiet. A quiet scanner is indistinguishable from a clean codebase, and only one of those is worth having.

Judge by role, never by language. The scanner flags string literals structurally and the skip-list decides which are user-facing — what natural language a string appears to be written in is not an input to that decision, and working it out is pure overhead.

## Step 1 — Ensure the guardrail

Install `eslint-plugin-lingui` and enable `no-unlocalized-strings` at `warn` with the tuned options from [references/eslint-config.md](references/eslint-config.md):

```bash
npm install --save-dev eslint-plugin-lingui
```

Take the current release — it's a lint-only dev dependency, so there's nothing a pinned range protects.

**This install is permanent.** The audit is a one-time sweep; the rule is what stops the next regression. An audit that finds 30 strings and leaves no guardrail behind buys a few weeks.

Enable the rule explicitly. The plugin's `recommended` and `flat/recommended` presets do **not** include it, so extending a preset is not coverage — the reference has the detail.

If the user declines a new dev dependency, there is a one-shot mode — write the tuned config outside the repo and point ESLint at it, leaving the project untouched:

```bash
npx eslint -c /tmp/lingui-audit.config.js --no-config-lookup 'src/**/*.{ts,tsx}' --format json
```

Offer that only after they decline, and say what it costs: the audit works, but nothing prevents the next unwrapped string and the next audit starts from zero. Recommend the install.

Either way, this step is done once a scan runs and the rule reports.

## Step 2 — Scan

```bash
npx eslint 'src/**/*.{ts,tsx}' --format json > /tmp/lingui-scan.json
```

Filter to `ruleId === "lingui/no-unlocalized-strings"` and reduce to `file:line` plus the offending source line — the reference has the `jq` recipe. That list is the worklist; work it top to bottom.

Keep the rule's options in the config file and run the CLI with no rule flags. An options-bearing `--rule` replaces the configured options rather than merging, roughly doubling the hit list with class names and log arguments — and the longer list reads as *more* thorough, so its garbage gets "fixed" by wrapping identifiers. The reference has the measurements.

When a scan comes back clean on a codebase you have reason to suspect, check the glob before believing it: a `files` pattern of `src/**/*.ts` never lints `.tsx`, and the run still exits 0.

## Step 3 — Judge each hit

Every hit gets a **disposition** — wrapped, or skipped with a recorded reason. No hit leaves this step without one.

The skip-list lives in the **lingui-best-practices** skill, section "Don't Wrap Non-UI Strings" — the authority on what stays unwrapped. Read it there before dispositioning. If it's out of reach, the role test below carries the judgment.

Dispositions turn on the string's **role**, not its shape. `"Best seller"` in a data module is a badge a shopper reads — wrap it. `"aero-press-go"` in the same object is a URL segment — skip it. Two questions settle the ambiguous ones:

- Could a translator change this without breaking anything? (`"DRAFT"` as a status value: no.)
- If this rendered in Japanese, would that be correct or a bug? (A `sku` in Japanese is a bug.)

When the line alone can't answer, read the consuming site. A string's role lives where it's used, not where it's defined.

## Step 4 — Fix in bounded batches

Wrap per the macro decision tree in **lingui-best-practices**. The cases this audit turns up most:

- JSX content → `Trans`
- A string inside a component (attribute, `alert`, function argument) → `useLingui()` + `` t`…` ``
- **A string outside any component** — data module, module-level map, config object → `msg` descriptor from `@lingui/core/macro`, resolved at the consuming site.

That last case is what this audit exists for, and it's the one that gets fixed wrongly. `t` at module scope resolves once, at import time, against whatever locale happened to be active, and then never changes. Define with `msg`, resolve where it renders:

```ts
// src/data/products.ts — definition
import { msg } from "@lingui/core/macro";

export const products = [
  { sku: "sku-1001", slug: "aero-press-go", name: msg`AeroPress Go` },
];
```

```tsx
// consuming component — resolution
const { t } = useLingui();
<h2>{t(products[0].name)}</h2>;
```

The field's type changes from `string` to `MessageDescriptor`, so TypeScript points at every consuming site — follow it. In non-React code with no render moment, `i18n._(descriptor)` resolves at call time, which is what a toast helper wants.

Add translator comments as you wrap, per **enhanced-message-context**: data-module labels and one-word badges are its must-comment cases, arriving with no surrounding UI to infer meaning from.

Then, once per round:

```bash
npx lingui extract --clean
npx lingui compile
```

and re-scan from Step 2.

**Bounds: at most 2 fix rounds, or ~40 files.** On hitting either, stop and report. A human can rerun the audit; a human cannot review a 200-file diff.

## Step 5 — Terminate

Stop when one of these is true, and say which:

1. **The scan is clean.**
2. **A round wrapped zero new strings** — every remaining hit is a confirmed false positive. Grow the rule's configured ignores from those specific cases, per the reference's discipline, so the guardrail stays quiet while still reporting everything else. Severity stays at `warn`, the rule stays enabled, and hits get ignores rather than `eslint-disable` comments.
3. **The bound is exhausted** (2 rounds / ~40 files).

## Step 6 — Report

Every hit from every scan lands in one of three buckets, stated with `file:line`:

- **Wrapped** — what changed, and which macro.
- **Skipped** — with the skip-list reason (`slug`, `enum value`, `log output`).
- **Residual** — still open, reviewed or not, listed individually so the next run starts here.

Report the guardrail state too: severity, and which ignores you added with the evidence that earned each.

Account for every hit before claiming the audit is finished. "I wrapped 16 strings" is not a result; "wrapped 16, skipped 16 as identifiers and log output, 0 residual, rule left at `warn`" is. Unreported residuals are the one outcome this skill exists to prevent — the misses were invisible in the first place precisely because nobody wrote them down.

## Invoked by another workflow?

An orchestrator (a setup skill, a TMS-connection skill) may supply scope (`src/features/checkout` only, or the files a migration touched), extra skip-list entries from a project rules file (brand names, product codes), or known misses ("an earlier pass missed the data layer").

Honor all three. The pipeline and the reporting contract don't change: scope narrows what you scan, never what you report. Findings outside the given scope are reported as out-of-scope, not omitted.

## Related skills

- **lingui-best-practices** — owns the skip-list and the macro decision tree that Steps 3 and 4 run on.
- **enhanced-message-context** — translator comments for the short, context-free labels this audit surfaces.
