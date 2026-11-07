---
name: hinge
description: Control the hinge (fold) angle of a foldable iPhone Simulator such as iPhone Duo. Use when you need to fold, unfold, half-open, or animate the fold of a running simulator, read its current hinge angle, or test how an app reacts to hinge and display changes.
---

# hinge

Set and read the hinge angle of a booted foldable iPhone Simulator from the command line. It posts the same HID event as the hidden hinge slider in Xcode's Device Hub (hold Option).

Run the bundled script at `scripts/hinge`, relative to this skill's directory. If `hinge` is on `PATH`, you can use that instead.

## Commands

```bash
scripts/hinge 120                # set angle: 0 = closed, 180 = flat
scripts/hinge open               # 180°
scripts/hinge close              # 0°
scripts/hinge half               # 90°
scripts/hinge sweep 180 0 2      # animate from 180° to 0° over 2 seconds
scripts/hinge get                # print current angle, e.g. 130.0
scripts/hinge -d "iPhone Duo" 90 # target a simulator by name or UDID (default: booted)
```

## Workflow

1. Make sure a foldable simulator is booted: `xcrun simctl list devices booted`.
2. Set the angle, then wait about half a second for the system to settle before you take a screenshot or read the UI.
3. Check the result with `scripts/hinge get`.
4. Screenshots: `xcrun simctl io booted screenshot out.png`. For the outer display, add `--display=1`.

## Notes

- Simulator only. It does not work on physical devices.
- The first run compiles a tiny helper with Xcode's clang, caching it under `~/.cache/hinge`. It takes a few seconds.
- `get` takes about 1–2 seconds because it samples `devicectl device motion hinge-angle`.
- A `sweep` runs at 60 Hz in one process. For a smooth animation, use it instead of many `set` calls.
- This uses a private, undocumented protocol. It was verified with Xcode 27.1 and iOS 27.1 and may break in other versions. If `set` succeeds but `get` doesn't change, report that the protocol has likely changed.
