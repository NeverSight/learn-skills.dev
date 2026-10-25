---
name: render-report
description: Render existing .ux/audits reports into self-contained, offline HTML pages — findings as cards, the captured screenshots as an interactive walk-through flipbook, plus the roll-up dashboard and an index landing page. Use for "render the report to HTML", "HTML view of the audit", "open the audit in a browser", "flipbook walkthrough", "make a shareable report page".
---

# Render report — a self-contained HTML view of an audit

Turn the Markdown reports under a host's `.ux/audits/` into **self-contained HTML** you can
open in a browser or share: findings as severity-badged cards, the live screenshots as an
interactive **walk-through flipbook**, the roll-up as a go/no-go **dashboard**, and an
`index.html` landing page. The transform is
[`scripts/render_report_html.py`](../../scripts/render_report_html.py).

**The Markdown report is the source of truth; the HTML is a derived view.** This skill never
edits a report's Markdown, the shared [report contract](../usability-audit/references/report-contract.md),
or any host application code — it only writes `.html` companions beside the `.md` files, under
`.ux/audits/`. Running it changes no finding, count, or verdict.

This is the on-demand path. The audit skills already render the HTML as their final step; use
this to (re)render reports that already exist — after pulling a branch, to refresh the view, or
to render an older run.

## Inputs

`$ARGUMENTS`:

- **`target`** — which reports to render. A single report (`.ux/audits/cuj-<ts>.md`), a glob
  (`.ux/audits/*.md`), or omitted to render **every** report in the host's `.ux/audits/`.
- **`--index`** — also (re)generate the `index.html` landing page from `index.md`. Implied when
  rendering the whole directory.

## Workflow

### 1. Locate the reports

Find the Markdown reports under the host's `.ux/audits/`. If the directory is absent or holds
no `*.md` reports, **stop and say so** — there is nothing to render; point the user at
`/usability-audit`, `/cuj-audit`, or `/ux-audit` to produce one first. Do not create reports
here; this skill only renders what already exists.

**Exit criteria:** a non-empty set of report paths, or a clean stop with the reason.

### 2. Render each report, and the index

Run the transform over the selected reports, then refresh the index:

```
python3 scripts/render_report_html.py .ux/audits/<report>.md   # or .ux/audits/*.md
python3 scripts/render_report_html.py --index .ux/audits/index.md
```

Each `<report>.md` yields `<report>.html` beside it; `rollup-*.md` renders as the dashboard;
`index.md` renders as the landing page. The output is **deterministic** — re-rendering an
unchanged report produces a byte-identical `.html`, so there is no diff churn.

**Exit criteria:** one `.html` per selected report plus `index.html`, each self-contained
(images inlined as `data:` URIs, no external references — it opens offline).

### 3. Report what was written, and confirm the footprint

List the `.html` files written and confirm every change is confined to `.ux/audits/`:

```
python3 scripts/audit_safety.py <host-repo>
```

This exits 0 only when **both** halves hold — nothing outside `.ux/audits/`, and the `.html`
files you just wrote observed inside it. A render that produced no files exits 1, which is
the correct answer: there was nothing to render or nothing got written.

**Exit criteria:** `audit_safety.py` exits 0 on **both** halves: nothing changed outside
`.ux/audits/`, **and** the `.html` files this run wrote inside it were observed and listed.

## Boundaries

- **Derived view only.** Never edit the report Markdown, the report contract, or host
  application code. The `.html` is generated *from* the `.md`; the Markdown stays canonical.
- **Never write outside `.ux/audits/`.** The `.html`, the dashboard, and `index.html` all live
  there, so the suite-wide safety invariant is unaffected.
- **Never fabricate.** Render what the report says; add no finding, count, image, or verdict
  the Markdown does not carry.

## Exit criteria (done when)

- Every selected report has a self-contained `.html` companion beside it, and `index.html` is
  refreshed; each opens offline with no external references.
- An absent/empty `.ux/audits/` stopped the run with a reason instead of inventing a report.
- `audit_safety.py` exits 0 on **both** halves: nothing changed outside `.ux/audits/`,
  **and** the writes this run made inside it were observed and listed. (`git status` alone is
  not the check — once `.ux/audits/` is gitignored it shows nothing, which a run that wrote
  nothing satisfies identically.)
