---
name: jmeter-jtl-performance-dashboard
description: Analyze a JMeter .jtl (CSV) result file and generate a performance test dashboard — summary tables, time-series and per-sampler charts (PNG), SLA validation, observations, recommendations, and downloadable HTML/Markdown/CSV report files. Use when asked to analyze JMeter results, build a performance report/dashboard, check load-test SLAs, or turn a .jtl file into charts.
---

# jmeter-jtl-performance-dashboard

Turns a JMeter `.jtl` result file (CSV format) into a full performance report:
an **interactive HTML dashboard** (Plotly), a Markdown report, three CSVs, and
seven PNG charts. Parsing and stats use **pandas**; the dashboard uses
**Plotly** (interactive: hover, zoom, legend toggle, PNG export) and **matplotlib**
(Agg backend) produces the static PNGs kept for backward compatibility and the
Markdown report — no display / no JMeter listeners needed. If Plotly is not
installed the dashboard gracefully falls back to the PNGs. Large files are read
in chunks. Sensitive fields (URL, tokens, cookies, auth headers, request/response
bodies) are **never** written to any output.

The dashboard is client-ready: 12 KPI cards with status colours, an SLA
compliance matrix (target · actual · status · variance, fails first) with an
overall PASS/FAIL/NOT EVALUATED badge, key-findings and priority recommendation
cards, interactive trend / dual-axis users-vs-throughput / error / P95-vs-error
scatter / distribution box-plot / degradation heatmap charts, a
searchable-sortable sampler table, TOC nav, Print-to-PDF + HTML/CSV export, and a
Data Quality section. It also has a read-only-by-default **Edit Report** mode
(client-side only): an ✎ Edit Report button enables inline editing of titles,
metadata, SLA targets, and narrative text, with an Override-metrics toggle
(audit-tracked) for KPI/SLA actuals, localStorage persistence, and an
"Export edited HTML" that writes a separate file without touching the original.

The driver is a single script: **`.claude/skills/jmeter-jtl-performance-dashboard/analyze_jtl.py`**.
All commands below were run and verified on Windows 11, Python 3.12.10, pandas
3.0.3, matplotlib 3.11.0, plotly 6.9.0. Paths are relative to the repo root (`D:\SeleniumRepo`).

## Prerequisites

Needs Python 3.9+ with pandas, matplotlib, and plotly (all in
`requirements.txt`). If Python is missing on Windows
(only the Microsoft Store alias stub is present), install it per-user — no admin:

```powershell
winget install --id Python.Python.3.12 --scope user --silent --accept-source-agreements --accept-package-agreements
```

Then create a virtual environment and install deps (one time). Use the full
interpreter path if `python` still resolves to the Store stub:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .claude\skills\jmeter-jtl-performance-dashboard\requirements.txt
```

## Run (agent path — this is the one to use)

Invoke the driver with the `.jtl` path. This is exactly the verified command:

```powershell
.\.venv\Scripts\python.exe .claude\skills\jmeter-jtl-performance-dashboard\analyze_jtl.py path\to\results.jtl --test-name "Shop Peak Test" --env "Staging" --build "v2.4.1" --bucket 1min --sla-p95 2000 --sla-error-rate 1 --sla-avg 800
```

It prints a 6-step progress log and a summary line, then writes everything to
`reports/jmeter-jtl-performance-dashboard/`. Open `performance_dashboard.html`
to view the report. Exit code is `0` on success even when SLAs fail (SLA
failures are listed in the output and marked `FAIL` in the report), `2` for a
missing file, `3` if no valid rows survive parsing.

**Options** (all optional except the `.jtl` path):

| Flag | Meaning | Default |
|---|---|---|
| `--out DIR` | Output directory | `reports/jmeter-jtl-performance-dashboard` |
| `--bucket SIZE` | Time-series bucket: `30s`, `1min`, `5min` | `1min` |
| `--delimiter` | Force `,` or `tab` | auto-detected |
| `--test-name` / `--env` / `--build` / `--duration` | Report metadata labels | `—` |
| `--sla-avg MS` | Max average response time (ms) | not checked |
| `--sla-p90 MS` / `--sla-p95 MS` | Max P90 / P95 (ms) | not checked |
| `--sla-error-rate PCT` | Max error rate (%) | not checked |
| `--sla-throughput RPS` | Min throughput (req/s) | not checked |
| `--sla-users N` | Target concurrent users | not checked |

Simplest form (no SLA, defaults):

```powershell
.\.venv\Scripts\python.exe .claude\skills\jmeter-jtl-performance-dashboard\analyze_jtl.py path\to\results.jtl
```

Different bucket size (verified):

```powershell
.\.venv\Scripts\python.exe .claude\skills\jmeter-jtl-performance-dashboard\analyze_jtl.py path\to\results.jtl --out reports\run2 --bucket 30s
```

Tab-delimited JTL (verified):

```powershell
.\.venv\Scripts\python.exe .claude\skills\jmeter-jtl-performance-dashboard\analyze_jtl.py path\to\results.jtl --delimiter tab
```

## Output files (in `reports/jmeter-jtl-performance-dashboard/`)

```
performance_dashboard.html          # interactive dashboard — Plotly embedded self-contained (KPI cards, SLA matrix, findings, recommendations, charts, sampler table, data quality)
performance_report.md               # same content as Markdown
performance_summary.csv             # one-row overall summary
sampler_metrics.csv                 # per-sampler metrics table
time_series_metrics.csv             # per-bucket avg/p90/p95/throughput/error%/users
charts/response_time_trend.png      # Avg / P90 / P95 over time
charts/active_users.png             # concurrency (skipped if no allThreads column)
charts/throughput.png               # requests/sec over time
charts/error_rate.png               # error % over time (error periods shaded)
charts/sampler_average_response_time.png   # bar, highest→lowest
charts/sampler_p95_response_time.png       # bar, highest→lowest
charts/sampler_error_percentage.png        # bar, red ≥5%, amber >0%
```

## Gotchas (learned while building this)

- **`python` on Windows may be a Store alias stub** that errors with "Python was
  not found." Always call the venv interpreter by path
  (`.\.venv\Scripts\python.exe`), not bare `python`.
- **The JTL must have a header row.** JMeter writes headers only when
  `jmeter.save.saveservice.print_field_names=true`. Without it the script can't
  find `timeStamp`/`elapsed` and exits with a clear error. Only `timeStamp` and
  `elapsed` are strictly required; everything else degrades gracefully.
- **No `allThreads` column → no active-users chart.** The script skips that one
  chart and blanks the peak/avg-users fields instead of crashing. The HTML only
  embeds charts that actually exist, so there is never a broken image.
- **`allThreads` is per-JVM.** In a distributed test each load generator reports
  its own thread count, so "concurrent users" is per-generator unless you merge
  JTLs first.
- **`timeStamp` unit is auto-detected** (epoch ms with 13 digits vs epoch
  seconds with 10). `elapsed`/`Latency` are treated as milliseconds (JMeter
  spec); if the values look like seconds the script converts and notes it.
- **Bar charts show the top 25 samplers** by the sorted metric. With more labels
  than that, the rest are omitted from the *chart* (all still appear in the CSV
  and the sampler table).
- **Security is enforced at write time**, not just by omission: `URL` is never
  loaded, and `failureMessage` is redacted (Bearer tokens, `cookie=`,
  `token=`, long opaque strings → `[REDACTED]`) and truncated. Verified: a
  planted `Bearer …SECRET…` token and the request URL do **not** appear in any
  output file.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Python was not found` / Store popup | Install via the winget line above, then use `.\.venv\Scripts\python.exe` (full path), not `python`. |
| `JTL is missing required columns 'timeStamp' and/or 'elapsed'` | The file has no header row. Re-run JMeter with `print_field_names=true`, or add the header manually. |
| `ERROR: file not found` (exit 2) | Check the `.jtl` path; quote it if it contains spaces. |
| `no valid rows after parsing` (exit 3) | Every row had an unparseable `timeStamp`/`elapsed` — likely a wrong `--delimiter`; try `--delimiter tab`. |
| Charts look empty / one PNG missing | `active_users.png` is intentionally absent when the JTL has no `allThreads` column. |
| Wrong columns split into one | Delimiter mis-detected; force it with `--delimiter ,` or `--delimiter tab`. |

## Verifying a change to the driver

Regenerate the seeded sample JTL and re-run — this is the exact smoke test used
during development. `gen_sample_jtl.py` ships next to the driver in this skill:

```powershell
.\.venv\Scripts\python.exe .claude\skills\jmeter-jtl-performance-dashboard\gen_sample_jtl.py sample_results.jtl
.\.venv\Scripts\python.exe .claude\skills\jmeter-jtl-performance-dashboard\analyze_jtl.py sample_results.jtl --sla-p95 2000 --sla-error-rate 1
```

Expected on the seeded sample: 50,872 rows, ~4.98% errors, Avg ~1137 ms, P95
~3330 ms, and three SLA `FAIL` rows.
