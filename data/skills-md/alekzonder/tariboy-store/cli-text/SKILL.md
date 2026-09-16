---
name: cli-text
description: Use when passing comments, context, messages, status, Markdown, generated text, or other data to CLI commands, including commands assembled in JavaScript.
---

# CLI Text

Keep text as data through every parser. Check the receiving command's help;
use only documented arguments and input modes.

| Available interface | Pass text with |
| --- | --- |
| Structured tool or process argv API | A string field or one argv element, without a shell |
| CLI file/stdin input | A tool-written file or quoted heredoc; e.g. `gh pr create --body-file PATH` |
| Shell and positional/flag value only | Quoted heredoc into a variable, then one quoted argument |

Use the owning skill's storage rules first (Markdown, one-line status, context
scope). This skill handles transport, not authorization or formatting policy.
Use `--` for leading-hyphen positional text only if the CLI documents it.
Shell quoting does not disable option parsing.

## Bash text argument

Choose a delimiter absent from every complete payload line; place both delimiter
lines at column 1. Never interpolate payload into an unquoted heredoc.

```bash
CLI_TEXT=$(cat <<'CLI_TEXT_84_END'
O'Reilly: `literal` $(literal) $HOME \path — Привет
CLI_TEXT_84_END
)
note-cli set "$CLI_TEXT"
```

Command substitution removes ALL trailing newlines. This recipe is suitable
only when that matches the requested text. If exact trailing newlines matter,
use file/stdin when supported, or append a sentinel inside the substitution
and remove only that sentinel afterward. Empty text is one argument: `""`.
NUL cannot be represented in argv or Bash variables; use documented binary
file/stdin input or report that the interface cannot carry it.

## Codex JavaScript → Bash

This complete snippet assumes `body` is an existing string and `note-cli set`
accepts one text argument. It preserves empty text and exact trailing newlines.
It needs no Node APIs, encoder or filesystem in the JavaScript isolate.

```javascript
if (body.includes("\0")) throw new Error("CLI argv cannot contain NUL");
let delimiter = "CLI_TEXT_END";
const lines = body.split("\n");
while (lines.includes(delimiter)) delimiter += "_";
const cmd = "CLI_TEXT=$(cat <<'" + delimiter + "'\n" + body +
  "\n" + delimiter + "\nprintf .\n)\n" +
  'CLI_TEXT=${CLI_TEXT%.}\nCLI_TEXT=${CLI_TEXT%?}\n' +
  'note-cli set "$CLI_TEXT"';
const result = await tools.exec_command({cmd});
if (result.exit_code !== 0) throw new Error("Text write did not finish successfully");
```

The sentinel preserves the heredoc's trailing newlines; the second removal
removes exactly the ONE newline added before the closing delimiter. Wait for
any running tool process before checking its exit status. After a successful
write, use the documented read API when available and compare saved text with
the intended value (allow only documented storage normalization). Verify before
retrying an uncertain write to avoid duplicate comments or messages.

## Common mistakes

`JSON.stringify` serializes JSON; it does **not** quote for a shell. Backticks
and `$()` still execute inside shell double quotes. Never use `eval`, rebuild
a command from text, or hand-roll Base64 to repair quoting. Treat generated,
user, and log text alike. Check each actual parser boundary, including remote
shells; avoid an extra shell when a direct argv API exists.
