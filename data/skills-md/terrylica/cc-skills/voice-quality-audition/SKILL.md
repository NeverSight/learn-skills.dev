---
name: voice-quality-audition
description: Audition Kokoro TTS voices to compare quality and grade. TRIGGERS - audition voices, kokoro voices, voice comparison, tts voice, voice quality, compare voices.
allowed-tools: Read, Bash, Glob, AskUserQuestion
---

# Voice Quality Audition

Compare Kokoro TTS voice quality across all available voices. Runs `tts_kokoro_audition.sh` which plays a passage with each top voice. Each voice announces its name before reading the passage. Uses clipboard text or a default passage.

> **Platform**: macOS (Apple Silicon)

---

## When to Use This Skill

- Audition all available Kokoro voices to hear quality differences
- Compare specific voices side-by-side for a project
- Re-evaluate voice grades after a Kokoro engine upgrade
- Select a new default voice for TTS_VOICE_EN or TTS_VOICE_ZH
- Test how a particular passage sounds across multiple voices

---

## Requirements

- Kokoro TTS engine installed and healthy (`kokoro-install.sh --health`)
- Apple Silicon Mac with MLX Metal available
- `afplay` available (ships with macOS)
- Audition script at plugin `scripts/tts_kokoro_audition.sh`
- Shared library at plugin `scripts/lib/tts-common.sh`

---

## Voice Catalog

| Voice ID   | Name    | Grade   | Gender |
| ---------- | ------- | ------- | ------ |
| af_heart   | Heart   | A       | Female |
| af_bella   | Bella   | A-      | Female |
| af_nicole  | Nicole  | B-      | Female |
| af_aoede   | Aoede   | C+      | Female |
| af_kore    | Kore    | C+      | Female |
| af_sarah   | Sarah   | C+      | Female |
| am_adam    | Adam    | F+      | Male   |
| am_michael | Michael | unrated | Male   |
| am_echo    | Echo    | D       | Male   |
| am_puck    | Puck    | unrated | Male   |

**Current defaults** (configured in `~/.claude/automation/claude-telegram-sync/mise.toml`):

- English voice: `af_heart` (Grade A) via `TTS_VOICE_EN`
- Chinese voice: `zf_xiaobei` via `TTS_VOICE_ZH`
- macOS `say` fallback EN: `Samantha` via `TTS_VOICE_SAY_EN`
- macOS `say` fallback ZH: `Ting-Ting` via `TTS_VOICE_SAY_ZH`

See [Voice Catalog](./references/voice-catalog.md) for detailed characteristics and grade criteria.

---

## Workflow Phases

### Phase 1: Preflight

Verify Kokoro is installed and healthy:

```bash
kokoro-install.sh --health
```

All 6 checks must pass (venv, Python 3.13, mlx_audio importable, kokoro_common.py, tts_generate.py, version.json).

### Phase 2: Text Selection

The audition script reads from the macOS clipboard (`pbpaste`). If the clipboard is empty or not text, it falls back to a built-in passage about reading in a library.

To audition with custom text, copy the desired passage to the clipboard before running.

### Phase 3: Ask User — Full or Selective Audition

Use `AskUserQuestion` to determine scope:

- **Full audition** — Play all 10 voices sequentially (takes several minutes)
- **Select specific voices** — Run only a subset (e.g., top 3 female voices)

For a selective audition, edit the `VOICES` array in the script or pass voice IDs manually.

### Phase 4: Execute Audition

```bash
~/.local/bin/tts_kokoro_audition.sh
```

Or directly from the plugin source:

```bash
/path/to/plugins/tts-telegram-sync/scripts/tts_kokoro_audition.sh
```

The script acquires the TTS lock, plays each voice sequentially with a 1-second gap, then releases the lock on exit.

### Phase 5: Feedback

Use `AskUserQuestion` to collect the user's preference:

- Which voice sounded best?
- Any voices to eliminate from future consideration?
- Should we update grade assignments?

### Phase 6: Apply Configuration

Optionally update the default voice in mise.toml:

```toml
# ~/.claude/automation/claude-telegram-sync/mise.toml
[env]
TTS_VOICE_EN = "af_heart"   # Change to preferred voice ID
TTS_VOICE_ZH = "zf_xiaobei"
```

After changing mise.toml, restart the Telegram bot for the new voice to take effect.

---

## TodoWrite Task Templates

```
1. [Preflight] Verify Kokoro TTS is installed and healthy (kokoro-install.sh --health)
2. [Text] Check clipboard for passage, fall back to default if empty
3. [Select] Ask user: full audition (all 10 voices) or specific voices
4. [Audition] Run tts_kokoro_audition.sh and let user listen
5. [Feedback] Ask user which voice they prefer and collect grade feedback
6. [Apply] Optionally update TTS_VOICE_EN in mise.toml and restart bot
```

---

## Post-Change Checklist

- [ ] Kokoro health check passed before audition
- [ ] All selected voices played without errors
- [ ] User confirmed preferred voice
- [ ] mise.toml updated with new voice ID (if changed)
- [ ] Bot restarted after configuration change (if applicable)
- [ ] Voice catalog grades updated in reference doc (if re-graded)

---

## Troubleshooting

| Issue                           | Cause                              | Solution                                                                |
| ------------------------------- | ---------------------------------- | ----------------------------------------------------------------------- |
| No audio plays                  | Kokoro not installed               | Run `kokoro-install.sh --install` or use `full-stack-bootstrap` skill   |
| Audio cuts off mid-sentence     | TTS lock stolen by another process | Check for competing TTS processes: `pgrep -la afplay`                   |
| Voice sounds wrong              | Invalid voice ID in Kokoro model   | Verify voice ID exists in `VOICES` array; check Kokoro version          |
| Clipboard empty                 | No text copied                     | Script uses default passage automatically; no action needed             |
| "ERROR: Local Kokoro not found" | Venv or script missing             | Run `kokoro-install.sh --health` to diagnose; `--install` to fix        |
| FAILED for a specific voice     | Voice not available in model       | Voice may require a different Kokoro version; check model compatibility |
| Lock not released               | Script crashed without cleanup     | Remove stale lock: `rm -f /tmp/kokoro-tts.lock`                         |
| All voices sound identical      | Kokoro model not loaded properly   | Re-download model: `kokoro-install.sh --upgrade`                        |

---

## Reference Documentation

- [Voice Catalog](./references/voice-catalog.md) - Comprehensive voice listing with quality grades, characteristics, and selection guidance
- [Evolution Log](./references/evolution-log.md) - Change history for this skill
