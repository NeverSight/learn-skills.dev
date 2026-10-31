---
name: coding-wrapped
description: Creates or refreshes a private local Coding Wrapped website from Claude Code and Codex session history. Use for Coding Wrapped, coding-agent fun facts, AI-coding behavior insights, a personal localhost coding dashboard, new insight cards, or an export of an existing Wrapped. Scans locally, excludes raw transcripts from generated state, and produces one language with aggregate metrics, a Coding Overview, and four-at-a-time illustrated insights.
---

# Coding Wrapped

Turn local coding-agent history into a private localhost site. Make the default
flow short: infer the language, scan standard local sources, generate the site,
open it, and explain the controls.

## Product contract

1. **Local first** — Read local session files and write state only to the user's
   machine. Bind the site to `127.0.0.1`.
2. **Facts before stories** — Derive every claim from aggregate metrics. Never
   invent a number because it makes a better card.
3. **Fun before judgment** — Lead with recognizable habits and memorable
   moments. Give light suggestions, never scores, rankings, or diagnoses.
4. **One language** — Infer Chinese or English from the invoking prompt and
   generate the whole experience in that language.
5. **Four distinct scenes** — Generate insights four at a time. Their pixel-art
   illustrations must use different compositions, not four variations of a
   person, a hub, and connecting lines.

This is not a raw transcript viewer, employee-monitoring tool, productivity
score, or cloud analytics service.

## Runtime

Require Python 3.9+ and a local web browser. The bundled scripts make no
outbound network requests and need no separate API key; copy and illustration
generation use the active agent when available. Keep the workflow
platform-neutral. Do not require a Codex-only or Claude-only tool.

## First-run decisions

1. Infer `zh` or `en` from the user's current prompt. Do not ask for a language
   choice unless the prompt is genuinely ambiguous.
2. Reuse the saved display name when `config.json` exists. Otherwise infer a
   suitable short name; ask only if no reasonable name is available.
3. Treat an explicit request to scan or generate Coding Wrapped as authorization
   to read the standard local Claude Code and Codex session directories. If the
   user only asks what the Skill does, ask before scanning.
4. Do not ask about themes, metrics, layout, or data sources during normal
   onboarding. Use the defaults and report which sources were found.
5. Use one interface language. Do not expose a language toggle. A later request
   to change language is a regeneration request.
6. Do not present an implementation plan during the normal first run. Build the
   site, show it, then let the user react to something concrete.

## Run the workflow

Set `SKILL_DIR` to this Skill folder. Use a custom `CODING_WRAPPED_HOME` only
when the user requests one; otherwise state lives in `~/.coding-wrapped/`.

### 1. Scan local history

Run:

```bash
python3 "$SKILL_DIR/scripts/build_metrics.py" \
  --display-name "<name>" \
  --locale "<zh-or-en>"
```

This creates `7d`, `30d`, and `all` aggregate snapshots. It may read:

- `~/.claude/projects/**/*.jsonl`
- `~/.codex/sessions/**/*.jsonl`

Never copy raw transcript text into the generated site. Read
[references/privacy-policy.md](references/privacy-policy.md) before changing the
scanner or sending any scan-derived payload to a model.

### 2. Generate the Coding Overview

Run the brief command:

```bash
python3 "$SKILL_DIR/scripts/generate_overview.py" brief \
  --output /tmp/coding-wrapped-overview-brief.json
```

Read the brief. Write one overview in its requested locale with no score or
ranking and up to three sourced recommendations. Keep the summary to two
sentences: select two or three representative facts instead of replaying every
metric, then state the behavior they reveal. Aim for roughly two desktop lines
(45–75 Chinese characters or 18–34 English words). Save the result as:

Choose recommendations only from the brief's
`tip_context.candidate_practices`; each entry already carries its localized
action and sources, so do not load the full catalog. Open
[references/coding-best-practices.md](references/coding-best-practices.md) only
to check one practice's sourcing. Match the practice to an observed behavior
signal and use its localized action as the factual basis. Do not invent a
generic recommendation when no candidate fits.

```json
{
  "copy": {
    "<locale>": {
      "eyebrow": "...",
      "title": "...",
      "summary": "...",
      "recommendations": [
        {
          "id": "...",
          "practice_id": "an-allow-listed-practice-id",
          "title": "...",
          "body": "..."
        }
      ]
    }
  }
}
```

Persist it:

```bash
python3 "$SKILL_DIR/scripts/generate_overview.py" persist \
  --input /tmp/coding-wrapped-overview.json
```

### 3. Generate exactly four insights

Run:

```bash
python3 "$SKILL_DIR/scripts/generate_insights.py" brief \
  --output /tmp/coding-wrapped-insight-brief.json
```

Read [references/insight-writing.md](references/insight-writing.md) and
[references/visual-system.md](references/visual-system.md). Take each Light
Tip from the brief's `tip_context.candidate_practices`, as for the Overview.
Choose the four most personal and visually expressive
findings, not merely the four largest values. Use exactly one allow-listed
`tip_practice_id` per insight; persistence derives its source links from the
catalog. A tip must match an observed aggregate behavior signal.

When an image-generation tool is available:

1. Use the `cw-pixel-diorama-v1` contract and required prompt prefix from
   `references/visual-system.md`.
2. Resolve the matching theme reference under
   `$SKILL_DIR/assets/frontend-template/assets/` and attach it as an actual
   image reference. If the tool accepts multiple references, also attach
   `agent-orchestra-warm.png` to anchor the shared rendering language.
3. Create exactly four 1536 × 1024 PNG illustrations with four different
   compositions.
4. Run the reference comparison and six-point visual QA gate before
   persistence. Regenerate a drifting image; do not accept it merely because
   it is pixel art.
5. Pass each approved absolute PNG path as `image_source`.

When no image-generation tool is available (Claude Code has none built in),
omit `image_source`; the persistence script uses the bundled illustration for
each card's theme. Do not block
the site on image generation.

Write a batch matching the requested locale and persist it:

```bash
python3 "$SKILL_DIR/scripts/generate_insights.py" persist \
  --input /tmp/coding-wrapped-insights.json
```

Every batch must contain exactly four insights. The first real batch replaces
the demo seed; later batches append and survive page refreshes.

### 4. Serve and open the site

Run the server as a persistent process:

```bash
python3 "$SKILL_DIR/scripts/serve_site.py" --open
```

Default URL: `http://127.0.0.1:4173/`.

Use the local browser to confirm:

- the configured name and language appear;
- the Overview loads;
- four generated insights load;
- factual metric cards load;
- generated images resolve;
- the Insight deck changes cards with mouse drag and touch swipe while vertical
  page scrolling still works;
- the Dashboard scrolls vertically at `1280 × 720`, `1440 × 900`, and
  `1024 × 768`, without an unexpected horizontal scrollbar;
- export-card routes remain fixed-size and do not shift;
- no raw prompt, code, project name, or local path is visible.

### 5. Hand off a tiny manual

After generation, give the user the URL and explain only these controls:

- **Scan data** refreshes factual aggregates and does not regenerate insights.
- **Generate insights** copies a request to paste back into the agent. The
  agent writes four new insights (1–3 minutes, uses model allowance), and the
  open Dashboard picks them up when it regains focus.
- **Insight deck** supports click, arrow keys, mouse drag, and horizontal swipe.
- **Customize** chooses which factual metric blocks are shown.
- **Export** creates a portable local archive:

```bash
python3 "$SKILL_DIR/scripts/export_wrapped.py"
```

End with: raw conversations stay out of the website; only aggregates, generated
copy, approved source links, and generated illustrations are saved.

## Refresh rules

- Refresh facts whenever requested; this is deterministic and model-free.
- Do not regenerate the Coding Overview more than weekly unless the user asks.
- Auto-refresh the Overview only after it is at least seven days old and there
  are at least three new sessions or twenty new messages.
- Generate new insights only after explicit user action. Warn only that it uses
  model allowance and usually takes 1–3 minutes.
- Generate four, never one.

## Recovery

- If one source directory is missing, continue with the other and report the
  reduced coverage.
- If both are missing, explain the expected default paths and stop before
  generating claims.
- If image generation fails, use the fallback illustrations.
- If port `4173` is busy, choose another local port and report the exact URL.
- Preserve existing state on every retry; writes are atomic.
