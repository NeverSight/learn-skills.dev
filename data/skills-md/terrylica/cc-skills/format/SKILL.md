---
name: format
description: Reference for asciinema v3 .cast NDJSON format. TRIGGERS - cast format, asciicast spec, event codes.
allowed-tools: Read, AskUserQuestion, Bash
argument-hint: "[header|events|parsing|all] [-f file] [--live]"
model: haiku
---

# /asciinema-tools:format

Display reference documentation for the asciinema v3 .cast format.

## Arguments

| Argument     | Description                     |
| ------------ | ------------------------------- |
| `header`     | Show header field specification |
| `events`     | Show event codes deep-dive      |
| `parsing`    | Show jq/bash parsing examples   |
| `all`        | Show complete format reference  |
| `-f, --file` | Use specific .cast for examples |
| `--live`     | Run parsing examples on file    |

## Execution

Invoke the `asciinema-cast-format` skill with user-selected section.

### Skip Logic

- If section provided -> skip Phase 1 (section selection)
- If `-f` provided with `parsing` -> skip Phase 2 (example file)

### Workflow

1. **Selection**: AskUserQuestion for section
2. **Example**: AskUserQuestion for example file (if parsing)
3. **Display**: Show requested documentation

## Examples

```bash
# Show header format
/asciinema-tools:format header

# Show event codes
/asciinema-tools:format events

# Parse specific file with live examples
/asciinema-tools:format parsing -f session.cast --live
```

## Troubleshooting

| Issue          | Cause           | Solution                                     |
| -------------- | --------------- | -------------------------------------------- |
| File not found | Invalid path    | Use absolute path or ensure file exists      |
| Parse error    | Invalid NDJSON  | Check file is valid asciinema v3 format      |
| No output      | Missing section | Specify one of: header, events, parsing, all |
