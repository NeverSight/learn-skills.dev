---
name: ux-audit
description: Suite roll-up — fan out to the default UX auditors (usability, accessibility, cuj) against one target, with web performance available opt-in, normalize all findings into the shared .ux/audits contract, and produce one combined go/no-go roll-up. Use for "full UX audit", "audit everything", "ux-audit".
---

# UX Audit — suite roll-up

Run the auditor suite against one target and merge the results. By default this fans out to
usability, accessibility, and cuj; web performance is opt-in (add `--only web-performance` or
`--all`). This is the fan-out the
[report contract](../usability-audit/references/report-contract.md) was built for: every
auditor writes the same schema into `.ux/audits/`, so their reports are comparable and can be
rolled up into a single verdict.

Two native auditors plus two wrapped from **[web-quality-skills](https://github.com/addyosmani/web-quality-skills)**
(the same-author companion to `agent-skills`, a coherent suite of web-quality checks):

| Auditor | Source | Frameworks | Report `auditor` |
|---------|--------|------------|------------------|
| Usability | native `skills/usability-audit` | Nielsen / Shneiderman / AI / NPCIS | `usability` |
| Accessibility | wrap `web-quality-skills:accessibility` | WCAG 2.2 | `accessibility` |
| Web performance | wrap `web-quality-skills:performance` (+ `core-web-vitals`) **(opt-in — excluded from the default bundle; add via `--only web-performance` or `--all`)** | Core Web Vitals | `web-performance` |
| Critical user journeys | native `skills/audit-cuj` **(conditional — needs `.ux/cujs/`)** | the host's own CUJ files | `cuj` |

> Extensible: `web-quality-skills` also ships `seo` and `best-practices`; add them as
> future suite members the same way (register their frameworks in
> [`scripts/validate_report.py`](../../scripts/validate_report.py)).

---

## Inputs

- `target` — a URL (preferred; a11y and web-perf need a render) or a repo path. Omit to
  infer from the running dev server / repo.
- `--scope` — narrow to a flow or area, shared by all auditors.
- `--only <list>` — run a subset, e.g. `--only usability,accessibility`. Default (no
  `--only`): usability, accessibility, and cuj — **web performance is excluded (opt-in)**.
  Naming `web-performance` in `--only` runs it.
- `--all` — run every available auditor, **including web performance**. If both `--only` and
  `--all` are given, `--only` wins (the explicit subset is honored; `--all` is ignored).
- `--mode` — passed through to auditors that support it (usability).

## Workflow

1. **Discover available auditors.** Usability is always available (native). For
   accessibility and web performance, check whether the wrapping skills
   (`web-quality-skills:accessibility`, `web-quality-skills:performance`) are installed.
   **Web performance is also opt-in**: even when installed, it runs only when named in
   `--only` or when `--all` is passed — it is *excluded from the default bundle* (its
   metrics are typically dev-mode / localhost lab numbers, not production Core Web Vitals).
   When it is not opted into, record it as skipped with the reason `"web performance is
   opt-in; run with --only web-performance or --all"`, exactly as the CUJ skip is disclosed.
   The CUJ auditor (`audit-cuj`) is native but **conditional**: it runs only when the host
   has authored journeys — `.ux/cujs/` exists and is non-empty. **Skip any auditor that is
   unavailable — a wrapped skill not installed, `.ux/cujs/` absent/empty, or web performance
   not opted into — and record it as skipped with a note giving the reason** in the roll-up
   (for CUJ: `"no CUJs authored; run /ux-spec"`). A missing, skipped, or opt-in-not-requested
   auditor must never read as a clean pass. Honor `--only` and `--all`.

2. **Auth pre-flight — once, before any auditor runs.** *Applies only when this run will
   actually drive a browser:* `target` is a URL (or a reachable running app) **and** the
   resolved mode is live or hybrid. A repo-path target, or `--mode static`, has no page to
   navigate and no session to establish — skip this step entirely and record nothing. Do not
   start a dev server or open a browser just to run the probe; that is the ask-first
   boundary below, and a static run is not owed a browser.

   Otherwise: navigate to `target` (honoring `--scope`) and check for a login wall. If one
   stands there, run the **auth handoff** now:
   [`auth-handoff.md`](../usability-audit/references/auth-handoff.md) — observe the wall
   verbatim, ask once, the **user** signs in, re-observe to confirm the session holds.

   **Before the fan-out, not inside it.** Every auditor shares this browser session, so a
   lazy handoff would interrupt the user partway through a multi-auditor run — after minutes
   of work — and could ask more than once as each auditor hit the same wall independently.
   One probe, one interruption, before any auditor starts.

   | Outcome | Then |
   |---|---|
   | Not applicable (repo-path target, or static mode) | Proceed. Nothing to record. |
   | No wall | Proceed. Nothing to record. |
   | Handoff succeeded | Proceed. **Every** auditor inherits the session, native and wrapped alike. |
   | Declined | Proceed **unauthenticated** — do not skip the run. Auditors cover what is reachable and disclose the gated screens as coverage gaps. |
   | No attended browser surface | Same as declined, with cause `handoff unavailable — no attended browser surface`. **Not** a decline; nobody was asked. |

   **Disclose it in the roll-up.** Carry the outcome into the roll-up summary as an
   `Access:` line, so a go/no-go verdict is never read as covering the whole product when it
   covered only the public half. Record the **rung, never the account**.

   **A note on the wrapped auditors.** `web-quality-skills:accessibility` and
   `:performance` inherit the session but do not know this suite's capture rules, so their
   own artifacts may carry account data. That is why the artifact posture
   ([`auth-handoff.md`](../usability-audit/references/auth-handoff.md) §6) recommends ignoring
   `.ux/audits/` **wholesale** rather than assets-only, and why the recommendation is made
   here — at auth time, before any auditor writes anything.

3. **Fan out.** Run each selected auditor against the same `target`/`--scope`:
   - **Usability** — invoke the native `usability-audit` skill; it already writes a
     contract report.
   - **Accessibility** — invoke `web-quality-skills:accessibility`; capture its WCAG
     findings.
   - **Web performance** *(only when opted in via `--only web-performance` or `--all`)* —
     invoke `web-quality-skills:performance` (and `core-web-vitals`); capture its findings,
     respecting its metric-honesty rule (unmeasured = potential, never fabricated).
   - **Critical user journeys** — invoke the native `audit-cuj` skill; it replays the
     host's `.ux/cujs/` and already writes a contract report. It honors its own
     static-vs-live honesty rule (a static run cannot produce a verified pass).

4. **Normalize into the shared contract.** For each wrapped auditor, write a
   contract-conforming report at `.ux/audits/<auditor>-<YYYYMMDD>-<HHMMSS>.md` — same
   frontmatter schema, body layout, and appendix. **Map each tool's severity onto the
   0–4 scale**:
   - **Accessibility (WCAG):** blocker on a core flow / Level A name-role-value failure →
     3–4; Level AA (e.g. 1.4.3 contrast) → 3; minor/AAA or edge → 2; cosmetic → 1.
   - **Web performance:** a Core Web Vital in the "poor" band (measured) → 3; "needs
     improvement" → 2; a structural anti-pattern with only *potential* impact → 1–2,
     labeled potential per the metric-honesty rule.
   - **Omit severity 0** (non-problems), same as usability.
   Set `auditor` and `frameworks` per the table above; carry the tool's evidence
   (screenshots, `file:line`, measured metrics) into the Evidence field.
   The **native** auditors (usability, `cuj`) already emit contract reports — no external
   remapping. **CUJ carries one exception the roll-up must respect: `total: 0` is a *pass*
   (every journey verified clean), not "found nothing".** Read the CUJ report's
   executive-summary counts and `frameworks` list to tell a clean pass from a run that
   verified nothing (`frameworks: [cuj-contract]` alone signals the latter), and never
   fold a *skipped* CUJ run into the passed column.

5. **Append the index.** Add one `.ux/audits/index.md` row per auditor run (append-only),
   exactly as a single-auditor run does.

6. **Write the roll-up.** Create `.ux/audits/rollup-<YYYYMMDD>-<HHMMSS>.md`: a per-auditor
   severity table, the auditors that ran vs. were skipped (with reasons — including a
   CUJ run skipped for want of `.ux/cujs/`, and web performance skipped when not opted into,
   with its opt-in reason), a merged top-issues list ordered by severity across all
   auditors, and an overall **go/no-go verdict** (e.g. no-go if any sev4, or any auditor
   reports a sev3 blocker — a CUJ sev4 is a blocked journey and forces no-go). A skipped CUJ
   run, or a web-performance run not opted into, is disclosed, never scored as a pass. Link
   to each individual report.

7. **Self-check.** Validate every report and the index with
   [`scripts/validate_report.py`](../../scripts/validate_report.py), and confirm the safety
   invariant with [`scripts/audit_safety.py`](../../scripts/audit_safety.py) `<host-repo>`.
   It checks **both halves** of the invariant (SPEC §5.2) and exits 0 only if both
   hold: nothing changed outside `.ux/audits/`, **and** the writes you just made inside it
   were observed — it prints them. Exit 1 with *"no writes were observed"* means the run
   produced nothing; that is a real failure for an auditor, not a formality, and it is the
   only signal you get once `.ux/audits/` is gitignored and `git status` has gone quiet.

8. **Render the HTML companions.** Generate a self-contained HTML view for every member
   report, the roll-up dashboard (with its go/no-go verdict and per-auditor matrix linking to
   each member's `.html`), and the index landing page:

   ```
   python3 scripts/render_report_html.py .ux/audits/*.md
   python3 scripts/render_report_html.py --index .ux/audits/index.md
   ```

   Each `.html` is a derived view of its Markdown, written under `.ux/audits/` — the safety
   invariant holds. (Also available on demand via `/ux-review`.)

## Boundaries

- **Findings only.** No auditor in the roll-up edits host application code.
- **Never write outside `.ux/audits/`** in the host repo — the suite-wide safety invariant.
- **Ask first** before starting a dev server, navigating a browser, or installing anything
  (including a missing wrapped skill — offer, don't auto-install).
- **Never fabricate**, and honor each wrapped auditor's own honesty rules (usability's
  render-vs-source; web performance's metric-honesty).

## Exit criteria (done when)

- Each selected, available auditor produced a contract-valid report under `.ux/audits/`,
  with one appended index row apiece.
- A `rollup-<timestamp>.md` exists with the per-auditor table, skipped auditors (with
  reasons), merged issues, and a go/no-go verdict.
- Every report validates; `audit_safety.py` exits 0 on **both** halves: nothing changed
  outside `.ux/audits/`, **and** the reports this run wrote inside it were observed.
