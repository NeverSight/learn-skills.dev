---
name: connect-tool
description: Connect any tool (Notion, Stripe, ClickFunnels...) to every agent by installing its official CLI, or writing a one-file Python CLI over its API, then a global skill. Use for "connect-tool notion", "connect X", "make a CLI for X", "use my X API key".
argument-hint: "<tool name, e.g. notion or clickfunnels>"
---

Give the user's agents a new tool they can use from any folder, as a `<tool>-cli` skill. Talk to the user in their language, one short question at a time, no jargon.

If you got this skill from a link instead of a local folder, install nothing else from the repo: download a file it links only when a step needs it, with `curl -fsSL https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/connect-tool/<path> -o <scratch>/<file>` (for example `scripts/cli_template.py`), and read another skill it names only when you reach it, from `https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/<skill-name>/SKILL.md`.

1. Confirm the tool (fix typos: "mtoin" is Notion). If `~/.agents/skills/<tool>-cli/` exists, read it and ask before changing it.
2. Look for a CLI published by the vendor itself (their docs, domain, or GitHub org); check `command -v` in case it is installed. Official CLI found: steps 3a. None: steps 3b. Never install a third-party package without the user's yes.
3a. Install with the documented method, preferring `brew` on macOS, then the vendor's `npm i -g` / `pipx` / `uv tool install`, then their own install script. Ask before `sudo`. Check `<cli> --version`; if not found, fix the shell PATH and say so in one line. Log in with the CLI's browser login when it has one; if it needs a key, the user adds `export <VAR>=...` to `~/.zshrc` themselves. Read `<cli> --help` and the main subcommands' `--help`.
3b. Read the official API docs: base URL, auth header, extra values like a subdomain or workspace id, and the endpoints behind the 5 to 10 things the user will really ask. Copy [scripts/cli_template.py](scripts/cli_template.py) to `~/.agents/skills/<tool>-cli/scripts/<tool>.py` and fill the constants, `auth_headers`, `SETTINGS`, and `COMMANDS` with confirmed endpoints only (`check` is a cheap read, stdlib only). Tell the user where to create the key, with the narrowest permissions that fit, and to run `python3 ~/.agents/skills/<tool>-cli/scripts/<tool>.py login` in their terminal (hidden input). If they paste the key in the chat instead, pipe it straight in with `printf '%s' '<key>' | python3 .../<tool>.py login --<setting> <value>`, never repeat it, never write it anywhere else.
4. Prove it works: one read-only command, then one real read (list a few items). Fix until both work.
5. Write `~/.agents/skills/<tool>-cli/SKILL.md`, under 30 lines, with only commands you ran or saw in `--help` or the docs. `<run>` is `<cli>` or `python3 ~/.agents/skills/<tool>-cli/scripts/<tool>.py`:

```markdown
---
name: <tool>-cli
description: <Tool> from the terminal: <main resources>. Use when the user asks to <4-6 real tasks in their words>.
---

Run `<run> <command>`; check `--help` before a command you have not used. Auth: <login command or VAR, where the key comes from>.

- <Task>: `<command> [args]`
- ...

Read before writing. Ask before anything that deletes, publishes, sends, or spends money. Docs: <url>.
```

6. Link it for Claude Code: if `~/.claude/skills` is not already a link to `~/.agents/skills`, run `mkdir -p ~/.claude/skills && ln -s ~/.agents/skills/<tool>-cli ~/.claude/skills/<tool>-cli`.

Finish with three lines: what is connected (CLI and account), that a new session shows `/<tool>-cli`, and one thing to try now.
