---
name: dogfood
description: Run systematic, evidence-backed exploratory QA on a live web app — navigate its pages, exercise interactive elements, capture console errors and screenshots, then produce a categorized bug report. Use when the user wants to find bugs in a web application before shipping, wants a QA pass on a deployed app or PR preview, or asks to "dogfood" a URL.
---

# Dogfood Skill

Systematic exploratory QA of a web application: navigate it, interact with it, capture evidence of anything broken, and produce a structured bug report with screenshots and console errors attached.

This skill drives a real headless Chromium instance through a small bundled Node script (`scripts/browser-driver.mjs`). One browser session stays alive across the whole pass, so pages, cookies, and console history persist. It needs only the four core tools every harness has — **Read, Write, Edit, Bash** — plus Node. No harness-specific browser tool is required.

See also: [USE_CASES.md](USE_CASES.md) for trigger phrases and a worked example, [references/local-app-setup.md](references/local-app-setup.md) for safely standing up a local target first, and the [top-level skills index](../USE_CASES.md). This skill is also called internally by `app-design`'s Mode A Test phase — see [app-design/SKILL.md](../app-design/SKILL.md). The [accessibility-audit](../accessibility-audit/SKILL.md) skill reuses this driver and its `axe` command (documented in the driver reference below).

## Setup: paths & shell state (READ THIS FIRST)

Two facts about how commands run, and how this skill deals with them:

1. **Each Bash command may run in a fresh shell.** On stock pi, shell variables and `export`s do **not** carry over from one Bash call to the next. So this skill does **not** rely on a variable set in an earlier step. Instead:
   - The **output directory is a fixed relative path, `./dogfood-output`** — the working directory (your project root) is stable between calls, so this same relative path always resolves to the same place. Every command below uses it literally.
   - The **one value that must be absolute is this skill's own directory** (where `browser-driver.mjs` lives). Each Bash block that needs it sets `D=` on its first line. **You must fill in `D` with the real absolute path** (see step 2). Do not leave the placeholder.

2. **Find this skill's directory once, and reuse that exact string as `D`.** You loaded this `SKILL.md` from a path — its containing directory is the value. If you need to find it programmatically, check pi's standard skill locations (this is unambiguous and fast):
   ```bash
   for d in "$HOME/.pi/agent/skills/dogfood" "$HOME/.agents/skills/dogfood" ".pi/skills/dogfood" ".agents/skills/dogfood" ./dogfood; do
     [ -f "$d/scripts/browser-driver.mjs" ] && printf 'D=%s\n' "$(cd "$d" && pwd)" && break
   done
   ```
   Run that, read the `D=/absolute/path` line it prints, and use that literal path as `D` in every block below.

## Prerequisites

One-time setup (installs the Node Playwright package and a Chromium binary). Replace `D=...` with your real path:

```bash
D="/absolute/path/to/dogfood"          # ← this skill's directory (from Setup step 2)
( cd "$D/scripts" && npm install && npx playwright install chromium )
```

Notes:
- If a Chromium binary is already installed (some environments pre-provision one and set `PLAYWRIGHT_BROWSERS_PATH`), the driver auto-detects it and `npx playwright install` is a harmless no-op.
- The driver needs Node 18+. Check `node --version` if `launch` fails.

## Inputs

1. **Target URL** — the entry point. If the user didn't give one, don't just ask open-endedly — offer concrete options:
   - Check `package.json` for a `dev`/`start` script and try its declared port first, or probe common local dev ports and use the first that responds:
     ```bash
     for u in http://localhost:3000 http://localhost:5173 http://localhost:8080 http://localhost:4200 http://localhost:5000 http://127.0.0.1:8000; do
       curl -sf -o /dev/null "$u" && echo "responds: $u" && break
     done
     ```
   - If none respond, ask the user to pick **(a)** a local dev server on another port, **(b)** a staging/preview URL, or **(c)** a public URL — and paste it.
2. **Scope** — what to focus on. If not given, default to **full site** from `/`, and say so explicitly.
3. **Output directory** — fixed at `./dogfood-output` for this skill (see Setup). No variable to set.

## Workflow

Five phases. If your harness has a task/todo list, track each phase on it.

### Phase 1: Plan

1. Create the output layout:
   ```bash
   mkdir -p ./dogfood-output/screenshots ./dogfood-output/.browser
   : > ./dogfood-output/issues.jsonl        # findings file: one JSON object per line
   ```
   Layout: `./dogfood-output/screenshots/` (evidence), `issues.jsonl` (findings, append as you go), `report.md` (written in Phase 5).
2. Confirm the testing scope (from Inputs).
3. Sketch a rough sitemap: landing/home, nav links (header/footer/sidebar), key flows (sign up, login, search, checkout), forms, edge cases (empty states, error pages, 404s).
4. **Start the browser in the background** and leave it running until Phase 5. Launch is a long-lived process (it blocks until `close`), so start it *detached* and then poll its log for `READY`:
   ```bash
   D="/absolute/path/to/dogfood"          # ← this skill's directory
   nohup node "$D/scripts/browser-driver.mjs" launch --state-dir ./dogfood-output/.browser \
     > ./dogfood-output/.browser/launch.log 2>&1 &
   ```
   Then confirm it came up (separate command; safe to repeat):
   ```bash
   for i in $(seq 1 20); do
     grep -q READY ./dogfood-output/.browser/launch.log 2>/dev/null && { echo "browser up"; break; }
     sleep 0.5
   done
   cat ./dogfood-output/.browser/launch.log
   ```
   If you never see `READY`, read `launch.log` — it holds the error (usually a missing Chromium or Node < 18).

### Phase 2: Explore

For each page/feature, in order. **Every block below re-sets `D`** because variables don't carry between calls — fill in your real path each time.

1. **Navigate:**
   ```bash
   D="/absolute/path/to/dogfood"
   node "$D/scripts/browser-driver.mjs" navigate --state-dir ./dogfood-output/.browser --url "https://example.com/page"
   ```
2. **Snapshot the accessibility tree** (text structure — labels, roles, headings):
   ```bash
   D="/absolute/path/to/dogfood"
   node "$D/scripts/browser-driver.mjs" snapshot --state-dir ./dogfood-output/.browser
   ```
3. **Check the console** and clear it for the next step — do this after *every* navigation and interaction; silent JS errors are high-value findings:
   ```bash
   D="/absolute/path/to/dogfood"
   node "$D/scripts/browser-driver.mjs" console --state-dir ./dogfood-output/.browser --clear true
   ```
4. **Annotate interactive elements** and inspect:
   ```bash
   D="/absolute/path/to/dogfood"
   node "$D/scripts/browser-driver.mjs" annotate --state-dir ./dogfood-output/.browser --path ./dogfood-output/screenshots/page-1.png
   ```
   This overlays numbered `[N]` badges, saves the screenshot, and writes `refs.json` mapping each number to a CSS selector.
   - **If your harness can view images:** open the PNG and assess layout, visual bugs, accessibility.
   - **If it cannot:** rely on the `snapshot` from step 2 (text). Note in the report that visual-only issues weren't assessed.
   - ⚠️ **`--ref N` numbers are only valid until the next `annotate` or `navigate`.** After you re-annotate or change pages, the numbering is regenerated — don't reuse an old `--ref`. When acting across several steps, prefer `--selector "<css>"` (stable) over `--ref`.
5. **Test interactive elements** (refs are from the *most recent* annotate):
   ```bash
   D="/absolute/path/to/dogfood"
   node "$D/scripts/browser-driver.mjs" click  --state-dir ./dogfood-output/.browser --ref 3
   node "$D/scripts/browser-driver.mjs" type   --state-dir ./dogfood-output/.browser --ref 5 --text "test input"
   node "$D/scripts/browser-driver.mjs" press  --state-dir ./dogfood-output/.browser --key Tab
   node "$D/scripts/browser-driver.mjs" press  --state-dir ./dogfood-output/.browser --key Enter
   node "$D/scripts/browser-driver.mjs" scroll --state-dir ./dogfood-output/.browser --direction down
   node "$D/scripts/browser-driver.mjs" back   --state-dir ./dogfood-output/.browser
   ```
   You can pass `--selector "<css>"` instead of `--ref`. Cover keyboard navigation, form validation with invalid inputs, and empty submissions.
6. **After each interaction**, re-check: run `console` again; re-run `annotate`/`snapshot` and compare; ask "did the expected thing happen?" If not, it's a finding.

### Phase 3: Collect Evidence

For every issue found:

1. Capture a screenshot:
   ```bash
   D="/absolute/path/to/dogfood"
   node "$D/scripts/browser-driver.mjs" screenshot --state-dir ./dogfood-output/.browser --path ./dogfood-output/screenshots/issue-1.png
   ```
2. Append **one line** to `issues.jsonl` — one complete JSON object per line (JSONL). Appending a line can't corrupt earlier findings, unlike editing one big JSON array:
   ```bash
   cat >> ./dogfood-output/issues.jsonl <<'EOF'
   {"url":"https://example.com/page","steps":["click Login","submit empty"],"expected":"validation error","actual":"500 page","console":"TypeError: ...","screenshot":"screenshots/issue-1.png","severity":"High","category":"Functional"}
   EOF
   ```
   Keep the whole object on one physical line. After writing, sanity-check every line is valid JSON:
   ```bash
   while IFS= read -r line; do printf '%s' "$line" | python3 -c "import sys,json; json.loads(sys.stdin.read())" || echo "BAD LINE: $line"; done < ./dogfood-output/issues.jsonl
   ```
3. Classify **severity** (Critical / High / Medium / Low) and **category** (Functional / Visual / Accessibility / Console / UX / Content) using the taxonomy — read `<D>/references/issue-taxonomy.md` with the Read tool.

### Phase 4: Categorize

1. Read `./dogfood-output/issues.jsonl` back (each line is one finding).
2. De-duplicate — merge lines that are the same bug in different places.
3. Assign each a final severity and category.
4. Sort by severity: Critical, then High, Medium, Low.
5. Count issues by severity and by category (for the summary table).

### Phase 5: Report

1. Write `./dogfood-output/report.md` using the template — read `<D>/templates/dogfood-report-template.md` first. Fill in: executive summary, per-issue sections (link screenshots as relative markdown images, e.g. `![](screenshots/issue-1.png)`), the summary table, and testing notes (what was tested, what wasn't, blockers — including "visual issues not assessed" if the harness couldn't view images).
2. Shut down the browser:
   ```bash
   D="/absolute/path/to/dogfood"
   node "$D/scripts/browser-driver.mjs" close --state-dir ./dogfood-output/.browser
   ```
3. Tell the user the exact paths (`./dogfood-output/report.md` and the Critical/High screenshots). If your harness has a file-delivery capability, use it to surface them; otherwise the paths are enough.

## Driver Command Reference

| Command | Purpose |
|---------|---------|
| `launch` | Start the persistent headless browser (run detached; blocks until `close`) |
| `close` | Signal the running browser to shut down |
| `navigate --url <url>` | Go to a URL |
| `snapshot` | Dump the accessibility tree as JSON |
| `screenshot [--path <file>] [--fullpage true]` | Plain screenshot, no annotation |
| `annotate [--path <file>]` | Screenshot with numbered element badges + `refs.json` for `--ref` lookups |
| `click --ref <N> \| --selector <css>` | Click an element |
| `type --ref <N> \| --selector <css> --text <str>` | Fill a field |
| `press --key <key>` | Press a keyboard key |
| `scroll [--direction up\|down]` | Scroll the page |
| `back` | Go back in browser history |
| `console [--clear true]` | Read (and optionally clear) captured console/page errors |
| `axe [--tags <comma-list>]` | Run an automated axe-core scan of the current page; defaults to `wcag2a,wcag2aa,wcag21aa,wcag22aa` tags. Used by the `accessibility-audit` skill; also useful for a quick a11y sanity check mid-dogfood-run. |

All commands take `--state-dir ./dogfood-output/.browser` — the same directory passed to `launch`.

## Tips

- **Check the console after navigating and after significant interactions.** Silent JS errors are high value.
- **Use `annotate`** when you need to click precisely or reason about positions — `snapshot` gives structure but not layout.
- **Test valid and invalid inputs** — form-validation bugs are common.
- **Scroll long pages** — below-the-fold content may render wrong.
- **Test navigation flows end-to-end.**
- **Edge cases:** empty states, very long text, special characters, rapid clicking.
- **Always run `close` when done** — it's the only thing that stops the background browser process.
