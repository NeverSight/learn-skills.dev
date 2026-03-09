---
name: section-11
description: Evidence-based endurance cycling coaching protocol (v11.13). Use when analyzing training data, reviewing sessions, generating pre/post-workout reports, planning workouts, answering training questions, or giving cycling coaching advice. Always read or fetch athlete JSON data before responding to any training question.
---

# Section 11 — AI Coaching Protocol

## File Locations

Data files (`latest.json`, `history.json`, `DOSSIER.md`, `section11/`) live in the athlete's **data directory** — typically `~/training-data/`. HEARTBEAT.md lives in the **agent workspace** — the directory the agent runs from (e.g., `~/clawd/`). These may or may not be the same directory.

## First Use Setup

On first use:

1. **Check for DOSSIER.md** in the data directory
   - If found, use it
   - If not found, check `section11/DOSSIER_TEMPLATE.md`
   - If not found, fetch from: https://raw.githubusercontent.com/CrankAddict/section-11/main/DOSSIER_TEMPLATE.md
   - Ask the athlete to fill in their data (zones, goals, schedule, etc.)
   - Save as DOSSIER.md in the data directory root

2. **Set up JSON data source**
   - **Local setup (recommended):** Athlete runs sync.py on a timer, producing `latest.json` and `history.json` in the data directory. See `examples/json-local-sync/SETUP.md` for the full local pipeline.
   - **GitHub setup:** Athlete creates a private GitHub repo for training data with automated sync. Save raw URLs in DOSSIER.md under "Data Source".
   - `latest.json` — current 7-day snapshot + 28-day derived metrics
   - `history.json` — longitudinal data (daily 90d, weekly 180d, monthly 3y)
   - See: https://github.com/CrankAddict/section-11#2-set-up-your-data-mirror-optional-but-recommended

3. **Configure heartbeat settings** (optional, OpenClaw)
   - Check for `HEARTBEAT.md` in the agent workspace
   - If not found, check `section11/examples/agentic/openclaw/HEARTBEAT_TEMPLATE.md`
   - If not found, fetch from: https://raw.githubusercontent.com/CrankAddict/section-11/main/examples/agentic/openclaw/HEARTBEAT_TEMPLATE.md
   - Ask athlete for their specific values (location, timezone, riding hours, weather thresholds, notification hours)
   - Save as HEARTBEAT.md in the agent workspace

Do not proceed with coaching until dossier and data source are complete.

## Protocol

Load the coaching protocol using this precedence:

1. Check `./SECTION_11.md` (data directory root)
2. If not found, check `section11/SECTION_11.md`
3. If not found, fetch from: https://raw.githubusercontent.com/CrankAddict/section-11/main/SECTION_11.md

If both root and `section11/` copies exist, prefer the root copy.

**Current version:** 11.13

## External Sources

All external files referenced by this skill (`sync.py`, `SECTION_11.md`, templates, setup guides) are maintained in the open-source [CrankAddict/section-11](https://github.com/CrankAddict/section-11) repository and can be inspected there.

## Data Hierarchy

1. JSON data (always read latest.json first, then history.json for longitudinal context)
2. Protocol rules (SECTION_11.md)
3. Athlete dossier (DOSSIER.md)
4. Heartbeat config (HEARTBEAT.md)

## Required Actions

- Read or fetch latest.json before any training question. Check data directory first, then fall back to dossier-specified URLs.
- Read or fetch history.json when trend analysis, phase context, or longitudinal comparison is needed. Same precedence.
- No virtual math on pre-computed metrics — use values from the JSON for CTL, ATL, TSB, ACWR, RI, zones, etc. Custom analysis from raw data is fine when pre-computed values don't cover the question.
- Follow Section 11 C validation checklist before generating recommendations
- Cite frameworks per protocol (checklist item #10)

## Write Capabilities

If `push.py` is available (`section11/examples/agentic/push.py` or in the data repo), the skill can manage the athlete's Intervals.icu calendar and training data:
- **push** — write planned workouts to calendar
- **list** — show planned workouts for a date range
- **move** — reschedule a workout to a different date
- **delete** — remove a workout from the calendar
- **set-threshold** — update sport-specific thresholds (FTP, indoor FTP, LTHR, max HR, threshold pace). Only after validated test results, never from estimates
- **annotate** — add notes to completed activities (description by default, `--chat` for messages panel) or planned workouts (`NOTE:` prepended to description)

All write operations default to preview mode — nothing is written without `--confirm`. Execution via local CLI or GitHub Actions dispatch. See `examples/agentic/README.md` for full usage, workout syntax, and template ID mappings.

Only available on platforms that can execute code or trigger GitHub Actions (OpenClaw, Claude Code, Cowork, etc.). Web chat users cannot use this.

## Report Templates

Use standardized report formats. Load templates using this precedence:

1. Check data directory `reports/` directory
2. If not found, check `section11/examples/reports/`
3. If not found, fetch from: https://raw.githubusercontent.com/CrankAddict/section-11/main/examples/reports/

Templates:
- **Pre-workout:** Readiness assessment, Go/Modify/Skip recommendation — `PRE_WORKOUT_REPORT_TEMPLATE.md`
- **Post-workout:** Session metrics, plan compliance, weekly totals — `POST_WORKOUT_REPORT_TEMPLATE.md`
- **Weekly:** Week summary, compliance, phase context — `WEEKLY_REPORT_TEMPLATE.md`
- **Block:** Mesocycle review, phase progression — `BLOCK_REPORT_TEMPLATE.md`
- **Brevity rule:** Brief when metrics are normal. Detailed when thresholds are breached or athlete asks "why."

## Heartbeat Operation

On each heartbeat, follow the checks and scheduling rules defined in your HEARTBEAT.md:
- Daily: training/wellness observations (from latest.json), weather (only if conditions are good)
- Weekly: background analysis (use history.json for trend comparison)
- Self-schedule next heartbeat with randomized timing within notification hours

## Security & Privacy

**Data ownership & storage**
All training data is stored where the user chooses: on their own device or in a Git repository they control. This project does not run any backend service, cloud storage, or third-party infrastructure. Nothing is uploaded anywhere unless the user explicitly configures it.

The skill reads from: user-configured JSON data sources and DOSSIER.md in the data directory, and HEARTBEAT.md in the agent workspace. It writes to: DOSSIER.md in the data directory and HEARTBEAT.md in the agent workspace (during first-use setup only).

**Anonymization**
`sync.py` (maintained in the source repository) anonymizes raw training data. The skill does not perform anonymization itself. Only aggregated and derived metrics (CTL, ATL, TSB, zone distributions, power/HR summaries) are used by the AI coach.

**Network behavior**
When running locally (files in the data directory), no network requests are needed for protocol, templates, or data. When files are not available locally, the skill performs simple HTTP GET requests to fetch them from configured sources.

It does **not** send API keys, LLM chat histories, or any user data to external URLs. All fetched content comes from sources the user has explicitly configured.

**Recommended setup: local files**
The safest and simplest setup is fully local: sync.py on a timer, all files on your device. See `examples/json-local-sync/SETUP.md` for the complete local pipeline. If you use GitHub, use a **private repository**. See `examples/json-auto-sync/SETUP.md` for automated sync setup.

**Protocol and template URLs**
The GitHub URLs are fallbacks for when local files aren't available. The risk model is standard open-source supply-chain.

**Heartbeat / automation**
The heartbeat mechanism is fully opt-in. It is not enabled by default and nothing runs automatically unless the user explicitly configures it. When enabled, it performs a narrow set of actions: read training data, run analysis, write updated summaries/plans to the user's chosen location.

**Private repositories & agent access**
Section 11 does not implement GitHub authentication. It reads files from whatever locations the runtime environment can already access:
- Running locally: reads from your filesystem
- Running in an agent (OpenClaw, Claude Cowork, etc.) with GitHub access configured: can read/write repos that the agent's token/SSH key allows

Access is entirely governed by credentials the user has already configured in their environment.
