---
name: record-tui
description: |
  Use when recording terminal demos, creating GIFs of CLI apps, writing VHS tape files,
  or generating demo recordings for TUI applications. Use when asked to "record a demo",
  "create a GIF of my CLI", "write a VHS tape", "make a terminal recording",
  "generate a demo for my TUI", or "set up VHS for CI".
license: MIT
metadata:
  author: Antonin Januska
  version: "1.1.0"
  argument-hint: <app-command> [output-format]
tags: [vhs, recording, tui, demo, gif, terminal, cli, charmbracelet]
---

# Record TUI - Terminal Demo Recording with VHS

## Overview

Record polished terminal demos using [Charmbracelet VHS](https://github.com/charmbracelet/vhs). VHS turns `.tape` scripts into GIFs, MP4s, and WebMs — reproducible, version-controlled, and CI-friendly.

**Core principle:** Write tape files as code, not as screen captures. Every demo should be reproducible from a single `.tape` file.

## When to Use

**Use this skill when:**
- Recording a demo GIF for a README or docs
- Creating video walkthroughs of CLI/TUI applications
- Setting up automated demo recording in CI/CD
- Writing `.tape` files for VHS
- Troubleshooting VHS output quality (choppy GIFs, wrong dimensions, timing issues)

**Avoid when:**
- Recording non-terminal content (use screen capture tools instead)
- One-off manual recordings where reproducibility doesn't matter (use `asciinema`)
- The app has no terminal interface

## Prerequisites

**VHS requires two dependencies:**

```bash
# macOS
brew install charmbracelet/tap/vhs ffmpeg ttyd

# Debian/Ubuntu
sudo apt install ffmpeg && sudo snap install ttyd --classic
go install github.com/charmbracelet/vhs@latest
```

**Verify:** `vhs --version && ffmpeg -version && ttyd --version`

## Phase 1: Plan the Recording

Before writing a tape file, answer these questions:

1. **What are you recording?** — The exact command to launch the app
2. **What interactions to show?** — Key presses, navigation, typing sequences
3. **What's the target format?** — GIF (README), MP4 (docs site), WebM (web)
4. **What dimensions?** — Match your app's ideal viewport

**Recommended dimensions by use case:**

| Use Case | Width | Height | FontSize |
|----------|-------|--------|----------|
| README GIF | 1200 | 600 | 20 |
| Docs/tutorial | 1400 | 800 | 18 |
| Social media | 1200 | 630 | 22 |
| Full TUI app | 1600 | 900 | 16 |
| Compact CLI demo | 800 | 400 | 20 |

## Phase 2: Write the Tape File

### Tape File Structure

Every tape file follows this order:

```tape
# 1. Output declaration
Output demo.gif

# 2. Requirements (optional)
Require my-app

# 3. Settings (MUST come before commands)
Set Shell "bash"
Set FontSize 20
Set Width 1200
Set Height 600
Set Theme "Catppuccin Frappe"
Set WindowBar Colorful
Set Padding 20
Set TypingSpeed 75ms

# 4. Hidden setup (optional)
Hide
Type "export TERM=xterm-256color"
Enter
Sleep 500ms
Ctrl+L
Show

# 5. Visible interactions
Type "my-app --demo"
Sleep 500ms
Enter
Sleep 2s

# 6. App interactions
Down Down Down
Enter
Sleep 1s
Type "hello world"
Enter
Sleep 3s

# 7. Hidden cleanup (optional)
Hide
Ctrl+c
Sleep 500ms
```

### Essential Commands

| Command | Example | Purpose |
|---------|---------|---------|
| `Output` | `Output demo.gif` | Set output (gif/mp4/webm/ascii) |
| `Set` | `Set FontSize 20` | Configure settings |
| `Type` | `Type "hello"` | Emulate typing |
| `Type@Nms` | `Type@100ms "slow"` | Type at specific speed |
| `Enter`/`Tab`/`Space` | `Enter` | Key presses |
| `Up`/`Down`/`Left`/`Right` | `Down 3` | Navigation (with repeat) |
| `Ctrl+key` | `Ctrl+c` | Modifier combos |
| `Sleep` | `Sleep 2s` | Pause (ms or s) |
| `Wait+Screen` | `Wait+Screen /ready/` | Wait for screen content |
| `Hide`/`Show` | `Hide` | Control recording visibility |
| `Screenshot` | `Screenshot step1.png` | Capture current frame |
| `Env` | `Env TERM "xterm-256color"` | Set env variable |
| `Source` | `Source setup.tape` | Include another tape |
| `Require` | `Require node` | Fail if not in PATH |

For complete command details, settings, and timing guidelines, see **[Command Reference](./reference/COMMAND-REFERENCE.md)**.

## Phase 3: Smart Tape Generation

When asked to generate a tape file for a specific app, follow this process:

### Step 1: Analyze the App

Read the app's code or help output to understand:
- How it launches (command, flags, arguments)
- Key interactions (what keys it responds to)
- Visual states worth showing (menus, forms, results)

### Step 2: Generate the Tape

Build the tape file showing the app's key features:

```bash
# Generate and preview
vhs validate demo.tape    # Check syntax
vhs demo.tape             # Record
```

### Step 3: Iterate

Run the tape, review the output, adjust timing and interactions.

**Useful iteration commands:**
```bash
# Quick preview without saving
vhs demo.tape --output /dev/null

# Test specific section — use Source to split tapes
vhs section-test.tape
```

### Available Templates

Use these as starting points — copy and customize:

- **Basic CLI Demo** — Simple command + output recording
- **Interactive TUI Demo** — Navigation, forms, keyboard interaction
- **Build-and-Run Demo** — Hidden compilation, visible app usage
- **Multi-Panel TUI** — Complex apps like lazygit, k9s
- **CI Golden File** — ASCII output for regression testing
- **Composable Tapes** — DRY settings with `Source`

For complete copy-paste templates, see **[Templates](./reference/TEMPLATES.md)**.

## Phase 4: Optimize Output

### GIF Optimization

GIFs can get large. Reduce size with:

```tape
Set Framerate 15          # Lower framerate (default 30)
Set PlaybackSpeed 1.5     # Speed up slow parts
Set Width 800             # Smaller dimensions
```

**Post-processing with gifsicle (optional):**
```bash
gifsicle -O3 --lossy=80 demo.gif -o demo-optimized.gif
```

**Target sizes:**
- README GIF: < 5 MB (GitHub renders inline)
- Docs GIF: < 10 MB
- If over 10 MB, consider MP4 or WebM instead

### Timing Tips

- `Sleep 500ms` after typing a command — lets the viewer read it
- `Sleep 2-3s` after Enter — lets the viewer see the output
- `Sleep 3-5s` on the final frame — prevents abrupt loop restart
- `Set LoopOffset 60%` — smoother GIF looping
- Use `Type@100ms` for important text the viewer should follow
- Use `Type@30ms` for boilerplate the viewer doesn't need to read

## Phase 5: CI/CD Integration

### GitHub Actions

```yaml
name: Record Demo
on:
  push:
    branches: [main]
    paths:
      - "demo.tape"
      - "src/**"

jobs:
  record:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Record demo
        uses: charmbracelet/vhs-action@v2
        with:
          path: "demo.tape"

      - name: Commit updated GIF
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "docs: update demo recording"
          file_pattern: "*.gif"
```

### Golden File Testing

Use ASCII output to detect visual regressions:

```tape
Output demo.ascii
# ... your interactions ...
```

```bash
# In CI: compare against committed golden file
vhs demo.tape
diff demo.ascii demo.ascii.golden
```

## Examples

### Good: Well-Structured Tape File

<Good>

```tape
# Clear output declaration
Output demo.gif

# Explicit dependency
Require gum

# All settings grouped at top
Set Shell "bash"
Set FontSize 20
Set Width 1200
Set Height 600
Set Theme "Catppuccin Frappe"
Set WindowBar Colorful
Set TypingSpeed 75ms
Set Padding 20

# Hidden setup — always Ctrl+L before Show to clear the screen
Hide
Type "export GLAMOUR_STYLE=dark"
Enter
Sleep 500ms
Ctrl+L
Show

# Deliberate pacing — viewer can follow
Type "gum choose 'Option A' 'Option B' 'Option C'"
Sleep 500ms
Enter
Sleep 1s

# Navigate with visible pauses
Down
Sleep 300ms
Down
Sleep 300ms
Enter
Sleep 2s

# Generous final pause for loop
Sleep 3s
```

</Good>

### Bad: Common Mistakes

<Bad>

```tape
# Missing Output declaration — VHS won't know where to save

# Settings scattered throughout (will error or be ignored)
Type "my-app"
Set FontSize 20
Enter
Set Theme "Dracula"

# No Sleep after Enter — output flashes by
Type "my-app run"
Enter
Type "my-app status"
Enter

# No final Sleep — GIF loops abruptly

# No Require — silently fails if app missing
```

</Bad>

### Bad: TUI Recording Anti-Patterns

<Bad>

```tape
Output demo.gif
Set Width 600
Set Height 300
# Too small — TUI elements will be cramped and unreadable

Type "lazygit"
Enter
# No Sleep — app hasn't loaded yet, next keys arrive too early

Tab Tab Tab Tab Tab
# Rapid-fire navigation — viewer can't follow what's happening

Type "c"
Type "feat: add feature"
Enter
# No pauses between actions — looks like a blur
```

</Bad>

For a complete well-structured TUI example (lazygit, k9s), see **[Templates](./reference/TEMPLATES.md)**.

## Troubleshooting

### Problem: GIF is choppy or laggy

**Cause:** Framerate too high for GIF format, or file too large for viewer.

**Solution:**
```tape
Set Framerate 15            # Lower from default 30
Set PlaybackSpeed 1.0       # Don't speed up
```
If still choppy, reduce dimensions or switch to MP4.

### Problem: TUI doesn't render correctly

**Cause:** Missing TERM variable, wrong shell, or app needs specific setup.

**Solution:**
```tape
Hide
Env TERM "xterm-256color"
Type "stty rows 50 cols 120"
Enter
Sleep 500ms
Ctrl+L
Show
```

### Problem: Keys arrive before app is ready

**Cause:** No Sleep after launching the app — VHS sends keystrokes immediately.

**Solution:** Always add `Sleep 1-3s` after launching a TUI app:
```tape
Type "my-tui"
Enter
Sleep 2s          # Wait for app to initialize
Down              # Now safe to interact
```

For apps with variable startup time, use `Wait`:
```tape
Type "my-tui"
Enter
Wait+Screen /ready/    # Wait until "ready" appears on screen
Down
```

### Problem: VHS command not found

**Cause:** Missing VHS, ffmpeg, or ttyd.

**Solution:**
```bash
# macOS
brew install charmbracelet/tap/vhs ffmpeg ttyd

# Verify all three
vhs --version && ffmpeg -version && ttyd --version
```

### Problem: GIF too large for GitHub

**Cause:** High resolution, long recording, or high framerate.

**Solution:**
1. Reduce dimensions: `Set Width 800` / `Set Height 400`
2. Lower framerate: `Set Framerate 15`
3. Speed up slow sections: `Set PlaybackSpeed 1.5`
4. Post-process: `gifsicle -O3 --lossy=80 demo.gif -o demo-small.gif`
5. If still too large, use MP4 and embed with `<video>` tag

## Integration

**This skill pairs with:**
- **build-tui** — Record demos of TUIs you build
- **git-worktree** — Test recordings across branches
- **track-session** — Track recording iteration progress

**Useful alongside:**
- [Charmbracelet VHS](https://github.com/charmbracelet/vhs) — The recording tool
- [VHS GitHub Action](https://github.com/charmbracelet/vhs-action) — CI integration
- [gifsicle](https://www.lcdf.org/gifsicle/) — GIF optimization

## Quick Reference

```bash
vhs validate demo.tape            # Check syntax
vhs demo.tape                     # Record
vhs demo.tape --output custom.gif # Custom output path
vhs themes                        # List available themes
vhs new demo.tape                 # Create tape from template
```

**Key commands cheat sheet:**

| Command | Purpose |
|---------|---------|
| `Output file.gif` | Set output file and format |
| `Require app` | Fail if dependency missing |
| `Set Key Value` | Configure terminal settings |
| `Type "text"` | Emulate typing |
| `Type@100ms "text"` | Type at specific speed |
| `Enter` / `Tab` / `Space` | Key presses |
| `Up` / `Down` / `Left` / `Right` | Navigation |
| `Ctrl+c` | Modifier key combos |
| `Sleep 2s` | Pause execution |
| `Wait+Screen /regex/` | Wait for screen content |
| `Hide` / `Show` | Control recording visibility |
| `Screenshot file.png` | Capture current frame |
| `Env VAR "val"` | Set environment variable |
| `Source other.tape` | Include another tape file |

## Deep Reference

For detailed guides, load these files when needed:

- **[Command Reference](./reference/COMMAND-REFERENCE.md)** — All VHS commands, settings, timing guidelines
- **[Templates](./reference/TEMPLATES.md)** — Copy-paste tape file templates for common scenarios

*Only load these when specifically needed to save context.*

## References

- [Charmbracelet VHS](https://github.com/charmbracelet/vhs) — Official repository
- [VHS README](https://github.com/charmbracelet/vhs/blob/main/README.md) — Full documentation
- [VHS GitHub Action](https://github.com/charmbracelet/vhs-action) — CI/CD integration
- [VHS Examples](https://github.com/charmbracelet/vhs/tree/main/examples) — Official tape examples
- [VHS Themes](https://github.com/charmbracelet/vhs/blob/main/THEMES.md) — Available color themes
