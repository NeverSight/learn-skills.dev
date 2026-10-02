---
name: studio-mode-operator
description: Activate this skill when users need help with OBS Studio Mode's preview/program workflow — staging scene changes privately, rehearsing transitions, and committing them to the live output. Triggers include "enable studio mode", "preview the next scene", "rehearse a transition", "promote preview to program", "what's queued on preview", or "switch my transition to fade". This skill focuses on the two-scene discipline (program = what viewers see, preview = what's being prepared) rather than general streaming setup.
---

# Studio Mode Operator

Expert guidance for OBS Studio Mode, the two-scene preview/program workflow
used by broadcast operators to stage changes before putting them on air.

## When to Use This Skill

Activate **studio-mode-operator** when users request help with:

- **Entering and exiting studio mode**
  - "Enable studio mode"
  - "Turn on preview/program"
  - "I want to rehearse transitions"
  - "Disable studio mode, I'm done directing"

- **Preview-side staging**
  - "What's on preview right now?"
  - "Queue up the Gaming scene on preview"
  - "Preview the BRB scene without switching"

- **Transitions between preview and program**
  - "Cut to preview" (immediate)
  - "Fade to preview over 500ms"
  - "What transition is active?"
  - "Change my default transition to Slide"

- **Transition rehearsal**
  - "Show me how the transition will look before I fire it"
  - "Practice the segment change"

- **Troubleshooting studio mode**
  - "The transition button isn't doing anything"
  - "My preview scene reverted"

Prefer `streaming-assistant` for end-to-end stream sessions that only
incidentally touch studio mode; reach for this skill when the user's
primary focus is the preview/program discipline itself.

## Core Responsibilities

1. **Enforce the two-scene mental model** — always name both program
   (live) and preview (staging) when reporting state.
2. **Never clobber program without asking.** In studio mode, a scene
   switch via `set_scene` bypasses the preview and goes straight to air,
   which is almost always the wrong thing. Route through preview +
   transition instead.
3. **Choose the right transition** — hard cut for reactive news-style
   flow, fade for emotional beats, slide/wipe for segment boundaries.
4. **Reconnect state on ambiguity** — studio mode can be toggled from
   the OBS UI without our tools knowing; always verify with
   `get_studio_mode_enabled` at the start of a session.

## Available Tools

### Studio Mode Control
- `get_studio_mode_enabled` - Check whether studio mode is active
- `toggle_studio_mode` - Enable/disable studio mode

### Preview Scene
- `get_preview_scene` - Get the name of the scene currently on preview
- `set_preview_scene` - Put a scene on preview (no-op on program)

### Program (Live) Scene
- `get_current_scene` / `list_scenes` - Inspect program and available scenes
- `set_current_scene` - Puts a scene DIRECTLY on program; avoid in
  studio mode unless the user explicitly wants to skip the transition

### Transitions
- `list_transitions` - Available transition types (Cut, Fade, Slide, etc.)
- `get_current_transition` - Which transition is default
- `set_current_transition` - Change the default transition + duration
- `trigger_transition` - Execute the current transition (preview -> program)

### Contextual
- `get_obs_status` - Sanity-check OBS is connected

## Core Workflow: Preview → Program

This is the canonical loop studio-mode operators run on every scene change:

```
1. User indicates what they want live ("Switch to Gaming")

2. Confirm studio mode is on:
   - get_studio_mode_enabled
   - If false, ask: "Studio mode is off — do you want to enable it and
     rehearse, or just cut directly?"

3. Stage on preview:
   - set_preview_scene with the target scene
   - get_preview_scene to confirm
   - Report: "Gaming is queued on preview; program still shows BRB"

4. Confirm the transition type is appropriate:
   - get_current_transition
   - If the user said "fade", set_current_transition to "Fade" first

5. Commit to program:
   - trigger_transition
   - The preview scene becomes the new program; program becomes preview

6. Verify:
   - get_current_scene (now Gaming)
   - get_preview_scene (now BRB — swapped)
```

## Transition Selection Guide

| Situation | Transition | Notes |
|---|---|---|
| Breaking news / reactive cut | `Cut` | Zero-duration, most responsive |
| Segment boundary, same tone | `Fade` | 300-500ms feels natural |
| Topic change, different tone | `Fade` + longer (800ms) | Gives viewer a mental beat |
| Structured show transitions | `Slide` / `Swipe` | Signals segment change strongly |
| Intentional "jarring" moment | `Stinger` | Requires a configured stinger media source |

Always prefer the transition the user specifies by name. If ambiguous
("make it smoother"), increase duration on the current transition
before switching to a fancier one.

## Example Workflows

### Example 1: Simple Scene Change via Preview

```
User: "Go to Gaming"

1. get_studio_mode_enabled → true
2. list_scenes → confirm "Gaming" exists
3. set_preview_scene("Gaming")
4. Report: "Gaming queued on preview. Trigger transition when ready?"
5. User confirms
6. trigger_transition
7. Report: "On air with Gaming"
```

### Example 2: Enabling Studio Mode Mid-Session

```
User: "Enable studio mode and stage the BRB scene"

1. get_studio_mode_enabled → false
2. toggle_studio_mode
3. get_studio_mode_enabled → true (verify)
4. At this point preview mirrors program — inform the user
5. set_preview_scene("BRB")
6. Report: "Studio mode on. BRB on preview, Gaming still on program.
   Ready to transition."
```

### Example 3: Rehearsing a Fade

```
User: "Show me how a 1-second fade to Intermission looks before I commit"

1. get_current_transition → {name: "Cut", duration: 0}
2. set_current_transition("Fade", duration_ms: 1000)
3. set_preview_scene("Intermission")
4. Report: "Fade set to 1s, Intermission on preview. Hit trigger to
   rehearse — the actual program won't change until you do."
5. User says: "OK, now do it"
6. trigger_transition
7. Confirm new program
```

### Example 4: Emergency Direct Cut

```
User: "Just cut to Emergency scene NOW — something on-camera"

1. Skip preview staging (user signalled urgency)
2. set_current_scene("Emergency")
3. Report: "Emergency scene LIVE. Note: we bypassed preview because
   you said NOW — let me know when you want to go back to the
   preview/program flow."
```

This is the ONE time `set_current_scene` is preferable in studio mode.
Prompt operators to acknowledge they're intentionally skipping preview.

## Common Pitfalls

### Program and Preview Appear Identical
- **Cause**: Studio mode was just enabled, or a transition just fired.
  Preview mirrors program at that moment.
- **Fix**: Normal state. `set_preview_scene` to diverge them.

### `trigger_transition` Does Nothing
- **Cause**: Studio mode is disabled — there's no preview to promote.
- **Fix**: `get_studio_mode_enabled`. If false, either enable it or
  use `set_current_scene` for direct cuts.

### Transition Is Instant Despite Setting Duration
- **Cause**: The current transition is `Cut`, which ignores duration.
- **Fix**: `set_current_transition` to Fade/Slide/etc., THEN duration
  applies.

### Scene Disappeared from Preview After OBS Restart
- **Cause**: Preview state is not persisted across OBS restarts.
- **Fix**: Re-stage with `set_preview_scene` after reconnecting.

## Best Practices

1. **Name both scenes in every status report.** "Program: Gaming,
   Preview: BRB" is unambiguous; "On Gaming" is not.
2. **Confirm transition type before firing on novel scene changes.**
   The transition set last night may not match today's intent.
3. **Use long fades sparingly on live content.** 500ms is the sweet
   spot — longer makes pacing drag unless it's deliberate.
4. **For scheduled transitions (start-of-stream bumper, etc.)**,
   prefer automation rules (see `streaming-assistant`) over manual
   trigger_transition calls.

## Integration with Other Skills

- **streaming-assistant** - Handles the whole stream lifecycle; defer
  to it for pre-stream checklists. This skill owns only the
  preview/program loop once streaming is live.
- **preset-manager** - Scene presets are compatible with studio mode;
  apply on preview, then trigger_transition to put the preset on air.
- **scene-designer** - Layout changes happen to scenes. When you
  modify program while studio mode is on, preview and program can
  diverge in content — re-run the transition to converge them.

## OBS Version Notes

- **`get_preview_scene` / `set_preview_scene`** require studio mode to
  be enabled. If studio mode is off, these tools will return an error
  — treat that as a signal to toggle studio mode first rather than a
  hard failure.
- **OBS 30 multi-canvas (Sprint 1.0 / FB-42):** studio mode applies to
  the main canvas only. Additional canvases (vertical output, etc.)
  don't participate in the preview/program flow; they're driven
  directly.
