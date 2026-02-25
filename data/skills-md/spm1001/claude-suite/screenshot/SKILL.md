---
name: screenshot
description: >
  Take screenshots to see what's on screen. Triggers on 'screenshot', 'grab a screenshot',
  'have a look', 'can you see', 'what does it look like', 'check the screen', 'did that work',
  'verify it worked', 'what happened'. AFTER uncertain CLI operations (backgrounded processes,
  nohup, visual changes), consider capturing to verify state. Captures windows or full screen
  to files. (user)
---

# Screenshotting

Take screenshots to see what's on screen. Captures persist as files (unlike browsermcp snapshots which only exist in context).

## Quick Reference

```bash
# Capture specific app window
~/.claude/skills/screenshot/scripts/look.py --app Ghostty

# Capture window by title match
~/.claude/skills/screenshot/scripts/look.py --app Chrome --title "LinkedIn"

# Capture full screen
~/.claude/skills/screenshot/scripts/look.py --screen

# List available windows
~/.claude/skills/screenshot/scripts/look.py --list

# List windows grouped by category
~/.claude/skills/screenshot/scripts/look.py --categories

# List only browser windows
~/.claude/skills/screenshot/scripts/look.py --category browsers

# Native resolution (skip resize)
~/.claude/skills/screenshot/scripts/look.py --app Safari --native
```

**Categories:** browsers, terminals, editors, communication, documents, media, other

## When to Use

**Reactive (user asks):**
- "Have a look at this"
- "Can you see what's on screen?"
- "What does it look like?"
- "Check the browser"

**Proactive (verify state):**
- After uncertain CLI operations (did it background?)
- When tool prompt state is unclear
- After browsermcp actions when snapshot isn't enough
- To verify visual changes actually happened

**Documentation:**
- Capture steps in a workflow
- Before/after comparisons
- Bug evidence with screenshots

## When NOT to Use

- Browser-only tasks where browsermcp snapshot suffices
- When you just need to describe what's visible
- High-frequency captures that would clutter the directory

## Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| Capture without purpose | Clutters context | Only screenshot when you need the visual |
| Skip --list first | Wrong window captured | List windows to find exact app/title |
| Native on large screens | Huge files, slow upload | Use default 1568px resize |

## Resolution Strategy

Default: 1568px max dimension (~1,600 tokens, optimal for API)

| Option | Tokens | Use case |
|--------|--------|----------|
| Default (1568px) | ~1,600 | Full detail, no resize penalty |
| `--max-size 735` | ~500 | Quick look, text readable |
| `--native` | varies | When original resolution needed |

**Why 1568px:** Images larger than this get resized server-side anyway. Pre-resizing avoids upload latency while getting the same visual fidelity.

## Output

**Ephemeral (no path):** Screenshots go to `/tmp/claude-screenshots/` — auto-cleaned by OS, won't clutter project directories:
```
/tmp/claude-screenshots/2025-12-15-143022-chrome.png
```

**Persistent (explicit path):** For documentation workflows, specify where screenshots should live:
```bash
look.py --app Chrome ./docs/step3.png
```

**Design rationale:** Quick looks are ephemeral by default. Documentation requires intentional placement. If a subagent is documenting, it should think about where artifacts belong.

## How It Works

1. **Window enumeration:** Uses macOS CGWindowList API (pure Quartz, no AppleScript)
2. **Capture:** Uses `screencapture -l<windowid>` for windows, `screencapture -x` for screen
3. **Resize:** Uses `sips --resampleHeightWidthMax` for efficient scaling

**Key capability:** Can capture windows even when covered or minimized.

## Limitations

**Scrollback:** Only captures visible viewport. If content scrolled off screen, it won't be in the screenshot. Workaround: increase window size or pipe output to file.

**Multiple monitors:** Untested. `--screen` with `-m` flag captures main monitor only.

**Window selection:** Takes first match when multiple windows match filters. No "frontmost" heuristic yet.

## Integration with browsermcp

browsermcp's `browser_screenshot` injects images directly into context but doesn't persist them as files. Use this skill when you need:
- Screenshots that persist beyond the conversation
- Captures of non-browser apps
- Captures of windows behind the browser
- Files to upload to Drive or include in docs

## Permissions

Requires **Screen Recording** permission in System Preferences > Privacy & Security.

If capture fails with "check Screen Recording permissions", the user needs to grant permission to the terminal app (Ghostty, Terminal, iTerm, etc.).
