---
name: cowsay
description: Generates an ASCII cow saying custom text. Use when the user wants "cowsay", "cow say", or a cow to say something.
allowed-tools:
  - Bash(uvx cowsay:*)
  - Bash(bash */cowsay.sh:*)
---

# cowsay

Run the Python `cowsay` package to show an ASCII cow (or other character) saying the user's custom text.

## When to use

- User asks for a cow to say something (e.g. "make a cow say hello", "cowsay hello world").
- User provides custom text they want displayed in cowsay style.

## Instructions

1. **Get the text** – Use the exact phrase or sentence the user wants the cow to say. If they didn’t specify, ask or use a short default (e.g. "Hello!").
2. **Run cowsay** – Execute the script (uses `uvx cowsay` so no install or local-dir conflict):
   - `bash /mnt/skills/user/cowsay/scripts/cowsay.sh "user's text here"`
   - Escape or quote the text so spaces and special characters are preserved.
3. **Show the result** – Present the command output to the user as the cow’s speech bubble.

## Usage

```bash
bash /mnt/skills/user/cowsay/scripts/cowsay.sh "Your message here"
```

Requires [uv](https://docs.astral.sh/uv/) (or run `uvx cowsay "Your message here"` directly).

**Arguments:**

- Message text – The line the cow should say (default: use the text the user provided or ask).

**Examples:**

- `bash /mnt/skills/user/cowsay/scripts/cowsay.sh "Hello, world!"`
- `bash /mnt/skills/user/cowsay/scripts/cowsay.sh "Ship it!"`

## Output

The tool prints an ASCII-art cow with the given text in a speech bubble. Example:

```
 _____________
< Hello world! >
 -------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

## Present results to user

Show the cowsay output in a code block (e.g. preformatted text) so the cow art is aligned correctly.

## Troubleshooting

- **`uvx: command not found`** – Install [uv](https://docs.astral.sh/uv/), then `uvx cowsay` will work.
- **Broken layout** – Use a fixed-width font when displaying the output.
- **Special characters** – Keep the message in quotes so the shell doesn’t split or interpret it.
