---
name: play
description: Play .cast recordings in iTerm2 with speed controls. TRIGGERS - play recording, asciinema play, view cast.
allowed-tools: Bash, AskUserQuestion, Glob
argument-hint: "[file] [-s speed] [-i idle-limit] [-l loop] [-r resize] [-m markers]"
model: haiku
---

# /asciinema-tools:play

Play terminal recordings in a dedicated iTerm2 window.

## Arguments

| Argument                | Description                      |
| ----------------------- | -------------------------------- |
| `file`                  | Path to .cast file               |
| `-s, --speed`           | Playback speed (e.g., `-s 6`)    |
| `-i, --idle-time-limit` | Max idle time in seconds         |
| `-l, --loop`            | Loop playback                    |
| `-r, --resize`          | Match terminal to recording size |
| `-m, --markers`         | Pause on markers                 |

## Execution

Invoke the `asciinema-player` skill with user-selected options.

### Skip Logic

- If `file` provided -> skip Phase 1 (file selection)
- If `-s` provided -> skip Phase 2 (speed selection)
- If any of `-i/-l/-r/-m` provided -> skip Phase 3 (options)

### Workflow

1. **Preflight**: Check iTerm2 and asciinema
2. **Discovery**: Find .cast files
3. **Selection**: AskUserQuestion for file
4. **Speed**: AskUserQuestion for playback speed
5. **Options**: AskUserQuestion for additional options
6. **Launch**: Open iTerm2 via AppleScript

## Examples

```bash
# Play recording at normal speed
/asciinema-tools:play session.cast

# Play at 6x speed
/asciinema-tools:play session.cast -s 6

# Play with idle time limit and looping
/asciinema-tools:play session.cast -i 2 -l
```

## Troubleshooting

| Issue               | Cause             | Solution                               |
| ------------------- | ----------------- | -------------------------------------- |
| iTerm2 not found    | Not installed     | `brew install --cask iterm2`           |
| Window not opening  | AppleScript issue | Grant iTerm2 accessibility permissions |
| Playback stuttering | Large file        | Use `-i 1` to cap idle time            |
