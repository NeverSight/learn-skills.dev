---
name: textual-ui-developer
description: Develop and debug the MassGen Textual TUI with deterministic replay, snapshot regression tests, and targeted runtime checks.
---

# Textual UI Developer

Use this skill to improve the MassGen Textual UI while minimizing flaky reproduction and API cost.

## Use This Skill When

- You need to debug timeline rendering or ordering issues.
- You need to verify layout/styling changes in the real Textual shell.
- You need to update or add TUI regression tests (snapshot/golden/transcript).
- You need to reproduce UI behavior from `events.jsonl` deterministically.

## Default Strategy

Prefer deterministic workflows before live model runs:

1. Reproduce from recorded/synthetic events (`events.jsonl`) with no API calls.
2. Confirm behavior in the real shell using `--tui-real`.
3. Encode findings into tests (unit, transcript golden, snapshot).
4. Use live `massgen --display textual` or `--textual-serve` only when needed.

## Quick Commands

```bash
# Full frontend/TUI test suite
uv run pytest massgen/tests/frontend -q

# Timeline transcript goldens
uv run pytest massgen/tests/frontend/test_timeline_transcript_golden.py -q
UPDATE_GOLDENS=1 uv run pytest massgen/tests/frontend/test_timeline_transcript_golden.py -q

# Snapshot scaffold tests
uv run pytest massgen/tests/frontend/test_timeline_snapshot_scaffold.py -q
uv run pytest massgen/tests/frontend/test_timeline_snapshot_scaffold.py --snapshot-update -q
uv run pytest massgen/tests/frontend/test_timeline_snapshot_scaffold.py -q --snapshot-report snapshot_report.html
uv run python scripts/render_snapshot_svgs.py --real-tui-only

# Event replay (no API cost)
uv run python scripts/dump_timeline_from_events.py /path/to/events.jsonl [agent_id]
uv run python scripts/dump_timeline_from_events.py --tui /path/to/events.jsonl [agent_id]
uv run python scripts/dump_timeline_from_events.py --tui-real /path/to/events.jsonl [agent_id]

# Example synthetic fixture
uv run python scripts/dump_timeline_from_events.py --tui-real massgen/tests/frontend/fixtures/synthetic_tui_events.jsonl agent_a
```

## Workflow

### 1) Reproduce with Event Replay (No API Cost)

Start with transcript replay to verify timeline semantics quickly:

```bash
uv run python scripts/dump_timeline_from_events.py /path/to/events.jsonl agent_a
```

Then inspect visually:

```bash
# Lightweight timeline-focused view
uv run python scripts/dump_timeline_from_events.py --tui /path/to/events.jsonl agent_a

# Full runtime TextualApp shell
uv run python scripts/dump_timeline_from_events.py --tui-real /path/to/events.jsonl agent_a
```

Optional speed control for real replay:

```bash
MASSGEN_TUI_REPLAY_SPEED=8 uv run python scripts/dump_timeline_from_events.py --tui-real /path/to/events.jsonl agent_a
```

Exit replay with `q`.

### 2) Convert Findings into Tests

Pick the narrowest layer that captures the bug:

- Unit logic: `test_tool_batch_tracker.py`, `test_content_processor.py`, helpers.
- Transcript/golden behavior: `test_timeline_transcript_golden.py` + `massgen/tests/frontend/golden/`.
- Widget/shell snapshots: `test_timeline_snapshot_scaffold.py` + `massgen/tests/frontend/__snapshots__/`.
- Replay script behavior: `test_dump_timeline_from_events_script.py`.

### Final Presentation Focus Loop

When iterating specifically on final-answer visualization:

1. Validate header semantics in unit tests (winner line, tie-break markers, vote line formatting) in `test_timeline_section_widget.py`.
2. Regenerate only final-presentation snapshots if intended UI changed:
   - `uv run pytest massgen/tests/frontend/test_timeline_snapshot_scaffold.py --snapshot-update -q`
3. Verify runtime shell appearance with no API cost:
   - `uv run python scripts/dump_timeline_from_events.py --tui-real massgen/tests/frontend/fixtures/synthetic_tui_events.jsonl agent_a`
4. Run full frontend suite before finalizing:
   - `uv run pytest massgen/tests/frontend -q`

### 3) Snapshot Workflow

If snapshot tests mismatch:

1. Open `snapshot_report.html`.
2. Check `Show difference` toggle interpretation:
   - ON = blend-diff overlay (can look purple/black).
   - OFF = raw current vs historical snapshots.
3. If change is intentional, regenerate with `--snapshot-update`.
4. Re-run the frontend suite to confirm stability.

### 3.1) Mandatory Screenshot Review

For visual/UI tasks, do not rely on test pass/fail alone. You must read screenshots directly before finalizing:

1. Review the snapshot images in `snapshot_report.html` (current vs historical).
2. Keep `Show difference` OFF first to verify raw rendering; then optionally use ON for pixel-level drift.
3. If screenshots are provided in chat/task context, inspect those images directly and compare against expected runtime appearance.
4. If your viewer cannot open `.svg`, render via browser engine:
   - `npx playwright screenshot "file:///ABS/PATH/to/snapshot.svg" /tmp/snapshot.png`
   - Batch all (or real-TUI-only): `uv run python scripts/render_snapshot_svgs.py [--real-tui-only]`
   - Prefer this over ImageMagick conversion for Textual snapshots to avoid false artifacts.
5. Call out any mismatch between rendered snapshots and expected real TUI look, even if tests pass.
6. Only conclude "visual change verified" after explicit screenshot review.

### 4) Optional Live Visual Validation

Use live runs only after deterministic checks pass:

```bash
# Native terminal TUI
uv run massgen --display textual

# Browser-hosted Textual
uv run massgen --textual-serve
```

## Key Files

- `scripts/dump_timeline_from_events.py`: text replay, `--tui`, and `--tui-real` modes.
- `massgen/frontend/displays/textual_terminal_display.py`: `TextualApp`, shell layout, runtime event routing.
- `massgen/frontend/displays/tui_event_pipeline.py`: timeline event adapter and filtering logic.
- `massgen/frontend/displays/timeline_event_recorder.py`: deterministic text transcript recorder.
- `massgen/tests/frontend/test_timeline_snapshot_scaffold.py`: snapshot scaffold (widget + real shell states).
- `massgen/tests/frontend/test_timeline_transcript_golden.py`: transcript golden regressions.
- `docs/modules/testing.md`: canonical testing commands and parity notes.

## Done Criteria

A TUI change is complete when:

1. Relevant deterministic tests were added or updated first.
2. `uv run pytest massgen/tests/frontend -q` passes.
3. Snapshot/golden updates are intentional and reviewed.
4. `--tui-real` replay confirms expected real-shell behavior for the target scenario.
