---
name: accessibility-diff
description: "Regression check — diff a live page's web accessibility (a11y) violations against a baseline. By default it compares your uncommitted changes (stash-based); pass `--branch [<name>]` to compare against a branch. Reports the new WCAG violations introduced, the ones fixed, and the count of pre-existing ones. Use it for 'did my change break accessibility', 'what a11y issues did this PR add', or as a CI gate. For a full scan of one page use `accessibility-scan`; for a whole site use `accessibility-audit`."
argument-hint: "[--branch [<name>]] [target|url]"
allowed-tools: Bash, Read, Glob, Grep, Skill, Task
---

Default branch: !`git symbolic-ref refs/remotes/origin/HEAD --short 2>/dev/null | sed 's|.*/||' || echo main`

Report only what changed. Locate; don't fix.

Shared grounding and honesty conventions: [`../shared/methodology.md`](../shared/methodology.md).

Parse `$ARGUMENTS`: if `--branch <name>` is present, remove it and use branch mode (no value means the default branch above). The rest is the target: a URL, a config target name, or empty for the default target from `accesslint.config.json`. If it's empty and there's no config, ask for a URL.

## 1. Audit

```bash
PORT=$(npx -y @accesslint/chrome@latest ensure | node -e 'process.stdin.on("data",d=>process.stdout.write(""+JSON.parse(d).port))')
```

Stash mode (default; uncommitted changes). Tell the user first: _"Running in diff mode — stashing your changes to capture a baseline, then restoring. Your working tree will be fully restored."_ If `git stash push` fails, warn and exit.

```bash
git stash push -u -m "accesslint-diff-baseline"
npx -y @accesslint/cli@latest scan <target> --port "$PORT" --snapshot accesslint-diff --snapshot-dir /tmp --update-snapshot
git stash pop && sleep 2
npx -y @accesslint/cli@latest scan <target> --port "$PORT" --snapshot accesslint-diff --snapshot-dir /tmp --format json
```

Branch mode (`--branch <name>`). Tell the user first: _"Diffing against `<name>` — checking out that branch to capture a baseline, then restoring. Your working tree will be fully restored."_ Branch switching triggers a rebuild but not a browser reload, so the CLI opens a fresh tab each run to read the current build. Use `--wait-for "<selector>"` to hold the audit until the rebuild is ready; without it, warn that a slow build may give a stale baseline.

```bash
git diff --quiet && git diff --cached --quiet || git stash push -u -m "accesslint-diff-branch"
git checkout <branch>
npx -y @accesslint/cli@latest scan <target> --port "$PORT" --snapshot accesslint-diff --snapshot-dir /tmp --update-snapshot [--wait-for "<selector>"]
git checkout - && git stash pop 2>/dev/null
npx -y @accesslint/cli@latest scan <target> --port "$PORT" --snapshot accesslint-diff --snapshot-dir /tmp --format json [--wait-for "<selector>"]
```

Pass `--selector` and `--include-aaa` to both runs.

## 2. Report

```
Accessibility diff — http://localhost:3000/ vs main (94 rules, live DOM)
2 new · 1 fixed · 4 pre-existing hidden

New — Critical
- color-contrast — 2.1:1 (needs 4.5:1), #bbb on #fff
    where: main > p.subtitle   fix: darken to #767676
Fixed
- img-alt — <img src="old.jpg"> (no longer present)
```

For each new violation: where (selector verbatim, plus `file:line (symbol)` if `source` is present; don't fabricate), evidence, and fix (mechanical change or `NEEDS HUMAN`).

Don't edit. For fixes, apply the mechanical ones and re-run `accesslint:accessibility-diff` to verify; for bulk work hand off to `accesslint:accessibility-fix`.

## 3. Tear down

```bash
npx -y @accesslint/chrome@latest stop --all  # skip if ensure reported "managed":false
```

## Notes

- `ensure` determines the port; don't hardcode 9222.
- CLI exit 2 means a bad URL or target, or the page never loaded; check the dev server.
- A target name resolves the same in both runs only if `accesslint.config.json` is unchanged across the stash or checkout. If your changes touch the config, pass an explicit URL.
- Stash mode: `sleep 2` covers most HMR cases; if the baseline looks identical to current, add `--wait-for "<selector>"`.
- Branch mode: no HMR; the CLI opens a fresh tab each run, and `--wait-for` is the rebuild gate.
- Large DOM changes between runs cause selector drift; re-run `accesslint:accessibility-scan` for the full picture.
