---
name: NEON-SOUL
version: 0.4.3
description: Automated soul synthesis for AI agents. Extracts identity from memory and session logs, promotes recurring patterns to axioms (N>=3), generates SOUL.md with full provenance tracking. Bundled processing engine — no manual Q&A needed.
homepage: https://liveneon.ai
user-invocable: true
emoji: "\U0001F52E"
metadata:
  openclaw:
    config:
      stateDirs:
        - memory/
        - .neon-soul/
      readPaths:
        - ~/.openclaw/agents/main/sessions/
      writePaths:
        - SOUL.md
        - .neon-soul/backups/
    requires:
      node: ">=22.0.0"
      services:
        - name: ollama
          url: http://localhost:11434
          optional: false
tags:
  - soul
  - soul-synthesis
  - identity
  - self-learning
  - memory
  - provenance
  - compression
  - agent-soul
  - soul-document
  - ai-agent
---

# NEON-SOUL

Automated soul synthesis for AI agents. Reads memory files and session logs, finds recurring patterns, generates SOUL.md with provenance tracking. No questionnaires, no templates — identity emerges from real conversations.

**Requirements:** Node.js 22+, Ollama running locally (`ollama serve`).

---

## Commands

### `/neon-soul synthesize`

Run the bundled processing engine. This is a single exec command:

```
exec node {baseDir}/scripts/neon-soul.mjs synthesize
```

Synthesis is **incremental by default** — only new/changed memory files and sessions are processed. Existing signals are preserved and merged with new ones. Results from previous runs are cached (generalization, principle matching, axiom notation, tension detection) so unchanged data is never re-processed. If nothing changed since the last run, synthesis skips automatically.

The script auto-detects Ollama, reads memory files and session logs, extracts signals, promotes axioms, and generates SOUL.md. It outputs JSON.

**Reporting results:** Don't dump raw JSON. Present a brief, conversational summary:
- If new axioms emerged or counts changed: highlight what grew (e.g. "3 new signals crystallized into axioms — your soul is deepening")
- If nothing changed: a short one-liner is fine (e.g. "Soul is stable, no new patterns detected")
- If it failed: explain clearly what went wrong and suggest a fix
- Include key numbers naturally (axiom count, signal count) but don't list every field
- Keep the tone reflective and warm — this is about the user's identity evolving, not a build log

**Options:**
- `--reset` — Clear all synthesis data and caches, re-extract from scratch
- `--force` — Run even if no new sources detected
- `--dry-run` — Preview changes without writing
- `--include-soul` — Include existing SOUL.md as input (for bootstrapping from hand-crafted files)
- `--memory-path <path>` — Custom memory directory path
- `--output-path <path>` — Custom SOUL.md output path
- `--time-budget <minutes>` — Time budget for synthesis (default: 20). Adaptively limits session extraction based on observed LLM speed to ensure synthesis completes within budget
- `--verbose` — Show detailed progress

**Examples:**
```
exec node {baseDir}/scripts/neon-soul.mjs synthesize
exec node {baseDir}/scripts/neon-soul.mjs synthesize --reset
exec node {baseDir}/scripts/neon-soul.mjs synthesize --force
exec node {baseDir}/scripts/neon-soul.mjs synthesize --dry-run
```

**If Ollama is not running**, the script prints an error. Tell the user to start Ollama: `ollama serve`

---

### `/neon-soul status`

Show current soul state. Read the following files and report:

1. Read `.neon-soul/state.json` for last synthesis timestamp
2. Read `.neon-soul/synthesis-data.json` for signal/principle/axiom counts
3. Count files in `memory/` modified since last synthesis
4. Report dimension coverage (7 SoulCraft dimensions)

**Options:** `--verbose`, `--workspace <path>`

---

### `/neon-soul rollback`

Restore previous SOUL.md from backup.

1. List backups in `.neon-soul/backups/`
2. With `--force`: restore most recent backup
3. With `--backup <timestamp> --force`: restore specific backup
4. With `--list`: show available backups without restoring

---

### `/neon-soul audit`

Explore provenance across all axioms.

1. Read `.neon-soul/synthesis-data.json`
2. With `--list`: show all axioms with IDs and descriptions
3. With `--stats`: show statistics by tier and dimension
4. With `<axiom-id>`: show full provenance tree (axiom -> principles -> signals -> source files)

---

### `/neon-soul trace <axiom-id>`

Quick single-axiom provenance lookup.

1. Read `.neon-soul/synthesis-data.json`
2. Find the axiom matching `<axiom-id>`
3. Show: axiom text, contributing principles, source signal file:line references

---

## Scheduled Synthesis

Set up cron to run synthesis automatically. Incremental processing and multi-layer caching mean it only does real work when new memory or sessions exist — cached runs complete in seconds.

**Recommended:** Every 60 minutes, isolated session, 30-minute timeout.

**OpenClaw cron example:**
```
openclaw cron add \
  --name "neon-soul-synthesis" \
  --every 60m \
  --timeout 1800 \
  --isolated \
  --message "Run neon-soul synthesis: exec node {baseDir}/scripts/neon-soul.mjs synthesize --memory-path <memory-path> --output-path <output-path>. Share a brief, warm summary of what changed — highlight any new patterns, axioms, or growth. If nothing changed, just a calm one-liner."
```

**Or run manually:** `/neon-soul synthesize`

**Why cron over heartbeat:**
- Synthesis is a standalone task — no conversational context needed
- Runs in isolation from the main session
- Incremental by default — cached runs complete in seconds when nothing changed
- Adaptive time budget prevents runaway execution

---

## Data Locations

| What | Path |
|------|------|
| Memory files | `memory/` (diary, preferences, reflections) |
| Session logs | `~/.openclaw/agents/main/sessions/*.jsonl` |
| Soul output | `SOUL.md` |
| State | `.neon-soul/state.json` |
| Backups | `.neon-soul/backups/` |
| Synthesis data | `.neon-soul/synthesis-data.json` |
| Caches | `.neon-soul/generalization-cache.json`, `compression-cache.json`, `tension-cache.json` |

---

## Privacy

NEON-SOUL processes personal memory files to synthesize identity. Your data stays on your machine.

**What NEON-SOUL does NOT do:**
- Send data to any service beyond your configured LLM (Ollama, local by default)
- Store data anywhere except your local workspace
- Transmit to third-party analytics, logging, or tracking services
- Make network requests independent of your agent

**Before running synthesis:**
1. Review what's in your `memory/` directory
2. Remove any secrets, credentials, or sensitive files
3. Use `--dry-run` to preview what will be processed

---

## Troubleshooting

**Ollama not running:** `curl http://localhost:11434/api/tags` to check. Start with `ollama serve`.

**Bullet lists instead of prose:** When prose generation fails, NEON-SOUL falls back to bullet lists. Usually means Ollama timed out or the model isn't loaded. Run synthesis again.

**Stale results after model change:** Caches are keyed by model ID. Switching models automatically invalidates cached results. Use `--reset` if you want a clean start.
