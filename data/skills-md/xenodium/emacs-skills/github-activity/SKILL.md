---
name: github-activity
description: 'This skill should be used when the user invokes "/github-activity" to analyze a GitHub project''s recent activity (PRs and issues) and produce a succinct, chart-backed health report.'
tools: Bash
disable-model-invocation: true
---

# Analyze GitHub project activity

Produce a **succinct** report on a GitHub project's activity — throughput, backlog burn-rate, and responsiveness — backed by matplotlib charts. The bundled `analyze.py` does the fetching, windowing, and plotting; your job is to run it and turn its JSON summary into a short, insightful report.

## How to run

1. **Resolve the target repo** (`owner/name`), in this order:
   - An argument the user passed to `/github-activity` (e.g. `/github-activity xenodium/agent-shell`).
   - Otherwise, infer from the current directory's `origin` remote:
     ```sh
     gh repo view --json nameWithOwner -q .nameWithOwner
     ```
   - If neither works, ask the user which repo.
2. **Resolve the window.** Default is the last **6 months**. Honor any user phrasing ("last 3 months", "this year") via `--months N`.
3. **Query the Emacs foreground color** once (reuse if already known this session):
   ```sh
   emacsclient --eval '(face-foreground (quote default))'
   ```
   Returns a hex like `"#eeffff"`. Pass it as `--fg`.
4. **Run the analyzer** (it shells out to `gh`, computes metrics, writes charts, prints a JSON summary):
   ```sh
   uv run --with matplotlib "$CLAUDE_PLUGIN_ROOT/skills/github-activity/analyze.py" \
     --repo owner/name --months 6 --fg "#eeffff" --outdir /tmp
   ```
   If `$CLAUDE_PLUGIN_ROOT` is unset, use the skill's own directory path.
5. **Read the JSON** printed on stdout and **write the report** (structure below), embedding each returned chart path as a markdown image on its own line:
   ```
   ![throughput](/tmp/agent-ghactivity-throughput-XXXX.png)
   ```

## Report structure (keep it tight)

Order the report **bottom-line-up-front**: lead with the takeaway, then the evidence, and keep each chart directly next to the prose that interprets it. A skimmer should get the whole story from the TL;DR alone; everything below it is drill-down.

- **TL;DR** — 2–3 bullets at the very top: the verdict on how active/healthy the project is, the one or two numbers that prove it, and the implication (e.g. "issues need a triage pass"). This is the report for anyone who reads only the top.
- **Snapshot table** — metrics as rows, PRs and Issues as the two columns, numeric columns right-aligned. Put the window in a **caption line above** the table (not as a row — it applies to both columns and would leave blank cells). One metric per row:

  **Activity — last N months (FROM → TO)**

  | Metric | PRs | Issues |
  |---|--:|--:|
  | Opened | … | … |
  | Closed | … | … |
  | Net (opened − closed) | … | … |
  | Open now | … | … |
  | Median days to close | … | … |
  | p90 days to close | … | … |

  Emphasis: **bold at most one or two cells** — the value(s) that justify the headline (typically the concerning one: a large `p90`, a positive/growing `net`, or a high `open now`). Do not bold routinely, do not bold both the good and bad value, and don't use color or emoji (they don't render in terminal tables).
- **Throughput** — the chart, **immediately followed by 1–2 bullets that read it** (don't defer interpretation to a separate block). Draw from:
  - Is intake steady or spiking? Is closing keeping up (net trend)?
  - Are PRs healthier than issues (or vice versa)?
  - Steady drip vs lumpy cleanup bursts (look at `busiest_weeks`).
- **Backlog** — include only if it adds signal (a clear growth/decline trend); skip if flat. When included, put the chart with a single bullet noting the trend.
- **Most-wanted open issues** (optional) — the top entries from `top_open_issues` (open issues by 👍 reactions — a demand signal). List up to 3 as `[#N](url) — title (👍 R, C comments)`. Skip if the list is empty (no issue has reactions). This is distinct from `oldest_open`: reactions show *demand*, age shows *staleness*.
- **Next steps** (optional, ≤3 bullets) — only when the data motivates a concrete action, and each must be **specific**: cite the actual items from `oldest_open_issues` / `oldest_open_prs` / `top_open_issues` as linked references (e.g. "Triage or close [#142](url) — open 156 days"; "[#511](url) has 8 👍 and 9 comments — high demand, still open"). Prefer high-demand items over merely old ones when prioritizing. Point at real signals (a growing `net`, an aging `p90`). Skip this section entirely when the project is healthy; never emit generic filler like "keep triaging issues" or "review PRs promptly". A bad actionable is worse than none.

Prefer concrete numbers over adjectives. Do not dump the raw JSON. Do not restate every weekly value — summarize the shape. Don't repeat the TL;DR verbatim lower down — the bullets under each chart should add detail, not echo.

**Always link issue/PR references.** Every time you mention a PR or issue anywhere in the report (TL;DR, bullets, tables, next steps), render it as a markdown link `[#N](url)` using the `url` field the analyzer provides for that item (`oldest_open_*` and `top_open_issues` each carry a `url`). Never leave a bare `#N`.

## Rules

- Charts follow the `matplotlib` skill conventions: transparent background, Emacs FG color for text/spines/ticks, dark opaque legend box (`facecolor='#1a1a2e'`, `labelcolor=FG`), hidden top/right spines, subtle grid. `analyze.py` already does this — pass the real `--fg`.
- Timestamped filenames (the script handles this). Never overwrite a fixed name.
- The final (current) week is partial; the script hatches it and flags `partial: true` — never compare it head-to-head with full weeks. Say "in-progress" when referencing it.
- If the repo has very little activity in the window (few PRs/issues), say so plainly and skip charts that would be noise.
- Requires `gh` (authenticated) and `uv`. If `gh` errors on auth or a missing repo, surface that instead of guessing.
