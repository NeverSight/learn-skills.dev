---
name: qa-sprint-report-by-testomatio
description: Generate a QA Sprint Progress Summary Report from Testomat.io TMS data. Use when the user wants to produce a structured end-of-sprint report covering test design coverage, execution results, defect trends, and quality signals. The skill reads data via Testomat.io MCP tools, maps it to the report sections, and outputs an `.html` file by default (or `.md` if explicitly requested).
license: MIT
metadata:
  author: Testomat.io
  version: 1.0.0
---

# QA Sprint Report by Testomat.io

## When to Use

- End of sprint — produce a shareable QA report for stakeholders.
- Sprint review — need a structured view of what was tested, passed, failed, blocked.
- Mid-sprint status — capture current execution progress.
- The user mentions "sprint report", "QA summary", "sprint progress", or similar.

## How to Identify the Sprint

The user may identify the sprint in one of these ways (in priority order):

1. **Milestone name or ID** — e.g. "Sprint 42", "Sprint 2024.3" — use `milestones_list(type="Sprint")` to find it.
2. **Run group title** — e.g. "Sprint 42 Run" — use `rungroups_list` / `rungroups_get`.
3. **Direct run ID or run title** — use `runs_get` or `runs_list`.
4. **Plan title or ID** — use `plans_list` / `plans_get`.
5. **No identifier provided** — ask the user to specify the sprint milestone, run group, or run.

> If the user provides only a sprint name like "Sprint 42", always resolve it to a concrete milestone/rungroup/run first. Do not assume the title directly maps to an ID.

## Rules

- **Do not fabricate data.** If MCP does not return a value, use `[None]` or hide the section. Never invent numbers or statuses.
- **Resolve sprint first.** Never assume a sprint name maps directly to a run ID without verification.
- **Hide unavailable sections.** If analytics (Section 8) is not available, omit it entirely rather than leaving placeholder text.
- **One blank line between actions.** In any generated code or CLI snippets.
- **Use TQL for filtering.** Always prefer `tql` filters over client-side filtering when calling `runs_list`, `tests_list`, `testruns_list`.
- **HTML is the default output.** Generate `.html` first; only offer `.md` if the user explicitly asks for it or their initial prompt includes a request to save as `.md`.

---

# MCP Tools Mapping

Each report section maps to specific MCP tools. See the full section structure and metrics in the template:

- [qa-sprint-report.md](./references/qa-sprint-report.md) — section layout with fill-in placeholders

### Quick Commands

| Action | MCP Tool | Key Parameters |
|--------|----------|----------------|
| Find sprint milestone | `milestones_list` | `type="Sprint"`, `status="active"` |
| List runs for sprint | `runs_list` | `tql`: `milestone == '{id}'` |
| Get run details | `runs_get` | `run_id` |
| Get test results | `testruns_list` | `run_id`, `filter_status` |
| Get suite tests | `tests_list` | `suite_id`, `per_page=100` |
| Check analytics availability | `system_ping` | (Enterprise flag in response) |
| Get test health analytics | `analytics_tests` | `kind`, `days`, `from`, `to` |
| Get stats analytics | `analytics_stats` | `kind`, `from`, `to` |

---

# Workflow

### Step 1: Resolve Sprint Identity

Ask the user if no sprint identifier is provided. Try to resolve:

```
1. milestones_list(type="Sprint") — find milestone matching sprint name
2. rungroups_list — find rungroup with sprint title
3. runs_list(tql="title % 'Sprint N'") — find runs by title
```

### Step 2: Gather Sprint Metadata & Time Range

Collect for the report header:

- `milestones_get(milestone_id)` or `rungroups_get(rungroup_id)` for sprint title/dates.
- Ask user for QA Lead name if not in TMS.

**Critical: Extract Sprint Time Range**

Resolve the sprint time range in this priority order:

1. **User-provided** — If the user specified a time range in their original prompt, use it.
2. **Milestone/Rungroup dates** — Extract `start_date` / `due_date` from `milestones_get` or `rungroups_get`.
3. **Run timestamps** — If milestone/rungroup has no dates, derive from earliest `created_at` and latest `finished_at` across the sprint's runs (`runs_get`).
4. **Manual input** — If no time range can be determined from TMS, ask the user to specify the sprint period manually.

The time range is required for:
- `analytics_tests(kind="...", from="YYYY-MM-DD", to="YYYY-MM-DD")`
- `analytics_stats(kind="...", from="YYYY-MM-DD", to="YYYY-MM-DD")`
- Filtering runs by sprint period

### Step 3: Collect Run Data

1. `runs_list(tql="milestone == '{id}'")` — all runs for the sprint milestone
2. For each run, call `runs_get` to get status, counts, environments
3. `testruns_list(run_id, filter_status)` — get passed/failed/skipped per run

### Step 4: Build Report Sections

Iterate sections 1–9 of the template, populating each with MCP data. Apply rules:

- If a metric is not available → use `[None]` in the cell
- If an entire section has no data → hide the section (do not show placeholder text)
- Section 8 (Analytics) → check `system_ping` response for Enterprise capability; if not available, hide

### Step 5: Write Output File

Write the filled report to:
```
{user-specified-path}/QA_Sprint_Progress_Report_{SprintName}_{YYYY-MM-DD}.html
```

If no path specified, save to current working directory.

### Step 6: Offer Markdown Export

After writing the `.html` file, ask the user if they also want to export the report as a `.md` file:

```
❓ The report has been saved to `{path}`.
Would you like to also export it as a `.md` file?

1. ✏️ Yes, save as `.md` in the same location
2. 👍 No, keep the `.html` only
```

**If user picks option 1:**
1. Convert the HTML content to Markdown format.
1. Generate ".md" markdown format report using template from the references - [qa-sprint-report.md](./references/qa-sprint-report.md).
2. Save as `QA_Sprint_Progress_Report_{SprintName}_{YYYY-MM-DD}.md` in the **same directory** as the HTML file.

**If user picks option 2:**
- Confirm the `.html` path and end the workflow.

## HTML Template Styling

When exporting to HTML, apply the following styles:

### Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--primary-color` | `#6366f1` | Headers, badges, links |
| `--primary-hover` | `#4f46e5` | Hover states |
| `--success-color` | `#10b981` | Passed/ready badges |
| `--danger-color` | `#ef4444` | Failed/blocked badges |
| `--warning-color` | `#f59e0b` | In-progress badges |
| `--info-color` | `#3b82f6` | Info badges |
| `--gray-50` to `--gray-900` | `#f9fafb` → `#111827` | Text hierarchy |

### Typography

- **Font Family:** Inter (Google Fonts) with fallback: `-apple-system, BlinkMacSystemFont, sans-serif`
- **Font Weights:** 300 (light), 400 (regular), 500 (medium), 600 (semibold), 700 (bold), 800 (extrabold)
- **Monospace:** `ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas` — for ticket IDs and code
- **Icons:** Font Awesome 6.4.0 (`fa-solid`)

### Status Badges

| Status | Background | Text Color |
|--------|------------|------------|
| `passed`, `ready` | `#d1fae5` | `#065f46` |
| `failed`, `blocked` | `#fee2e2` | `#991b1b` |
| `progress` | `#fef3c7` | `#92400e` |
| `info` | `#dbeafe` | `#1e40af` |

### Key Elements

| Element | Description |
|---------|-------------|
| `.main-container` | White glass card (`rgba(255,255,255,0.98)`) with `backdrop-filter: blur(20px)`, max-width 1300px, border-radius 20px |
| `.header` | Gradient background (`linear-gradient(135deg, #6366f1, #4f46e5)`), white text, flex layout |
| `.section-card` | White background, 1px border `--gray-200`, border-radius 12px, box-shadow |
| `.report-table` | Full-width, collapse borders, hover highlight on rows |
| `.meta-grid` | CSS Grid (`repeat(auto-fit, minmax(220px, 1fr))`), gap 20px |
| `.instruction-card` | Info box with left 5px border in `--primary-color`, background `#eef2ff` |
| `.tms-link` | Primary color link with hover underline |

### HTML Structure

```html
<div class="main-container">
  <header class="header">
    <div class="header-title">
      <h1>QA Sprint Progress Report</h1>
      <p><i class="fa-solid fa-cubes"></i> [Project Name]</p>
    </div>
    <div class="header-badge">
      <i class="fa-solid fa-calendar-days"></i> Sprint: [Sprint Number]
    </div>
  </header>

  <section class="instruction-section">
    <div class="instruction-card">
      <h5><i class="fa-solid fa-circle-info"></i> How to Use This Template</h5>
      <ul>...</ul>
    </div>
  </section>

  <main class="content-section">
    <div class="section-card">
      <div class="section-title"><i class="fa-solid fa-chart-pie"></i> 1. Sprint Summary Scorecard</div>
      <div class="meta-grid">...</div>
    </div>
    <!-- Repeat section-card for each section -->
  </main>
</div>
```

---

# Report Template Reference

| Section | Description |
|---------|-------------|
| [qa-sprint-report.md](./references/qa-sprint-report.md) | Full template with all sections, emoji, and fill-in placeholders |