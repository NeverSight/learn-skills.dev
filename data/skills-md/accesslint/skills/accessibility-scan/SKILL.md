---
name: accessibility-scan
description: "One page, automated tier — run the web accessibility (a11y) rule engine against a live page and locate every violation it can detect mechanically. Pass a URL, a config target name (e.g. `accesslint:accessibility-scan dev`), or nothing to use the default target from `accesslint.config.json`. Ensures a debuggable Chrome, runs the @accesslint/core engine over CDP, and returns a worklist of live-DOM WCAG 2.2 violations, each grounded to its DOM selector and source `file:line`. Locates; doesn't edit. Use it for 'is this page accessible', 'check a11y on this URL', 'find contrast and alt-text issues', or to verify a UI change. For hands-on keyboard and screen-reader checks use `accessibility-inspect`; for a whole site or product use `accessibility-audit`; to diff against uncommitted changes or a branch use `accessibility-diff`."
argument-hint: "[target|url]"
allowed-tools: Bash, Read, Glob, Grep, Skill, Task
---

Audit a live page and report each violation and where it is. Locate; don't fix.

Shared grounding and honesty conventions: [`../shared/methodology.md`](../shared/methodology.md).

`$ARGUMENTS` is a URL, a config target name (`dev`, `storybook`, …), or empty to audit the default target from `accesslint.config.json`. If it's empty and no config exists, ask for a URL or suggest `npx @accesslint/cli init`.

## 1. Audit

```bash
PORT=$(npx -y @accesslint/chrome@latest ensure | node -e 'process.stdin.on("data",d=>process.stdout.write(""+JSON.parse(d).port))')
npx -y @accesslint/cli@latest scan <target> --port "$PORT" --format json
```

`<target>` is the URL or config target name from `$ARGUMENTS`. Omit it (don't pass `""`) to audit the config's default target. Add flags as needed: `--selector`, `--wait-for "<selector>"`, `--include-aaa`, `--disable <rules>`, or pin them per-target in `accesslint.config.json`.

## 2. Report

Counts by impact, then one entry per violation:

- where: selector verbatim, plus `file:line (symbol)` if `source` is present. Don't fabricate. If no violation has `source`, note "source mapping unavailable; located by selector only".
- evidence: contrast ratio, missing attribute, empty name.
- fix: mechanical change, or `NEEDS HUMAN`.

Don't edit. For fixes, apply the mechanical ones and re-run to verify; for bulk work hand off to `accesslint:accessibility-fix`.

## 3. Tear down

```bash
npx -y @accesslint/chrome@latest stop --all  # skip if ensure reported "managed":false
```

## Notes

- `ensure` determines the port; don't hardcode 9222.
- CLI exit 2 means a bad URL or target, or the page never loaded; check the dev server. An unknown target name makes the CLI list the available targets from `accesslint.config.json`.
