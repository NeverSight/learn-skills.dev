---
name: herdspace
description: Use herdspace to open projects in Herdr with hopen, add a project to a list, split a tab with a pane template, and check or update the setup. Use when a person asks to open, add, or arrange projects in Herdr, mentions hopen or herdspace, or asks to install or update herdspace.
license: MIT
metadata:
  source: "https://github.com/MussaCharles/herdspace"
---

# Use herdspace

herdspace has two parts. `hopen` opens the projects of a list in one Herdr session. `bootstrap.sh` sets up a machine. A list is a VS Code workspace file. Each list becomes one Herdr session with the name of the file.

If `hopen --version` fails, herdspace is not installed. Follow the agent install steps at `https://raw.githubusercontent.com/MussaCharles/herdspace/main/install.md`.

## Open projects

| The person wants to | Run |
|---------------------|-----|
| Open the projects of the list `work` | `hopen work --no-attach` |
| Open every list | `hopen --all` |
| See every list and its state | `hopen --list` |
| Open new projects with a template | `hopen work --template code --no-attach` |
| See every template | `hopen --templates` |

When you run `hopen` yourself, add `--no-attach`. You cannot use the session. Tell the person to attach in their own terminal:

```bash
hopen work
```

`hopen` is safe to run again. It starts a stopped session, adds only the folders that have no workspace, and closes nothing.

## Add a project to a list

1. Find the list file with `hopen --list`. A list is at `~/<name>.code-workspace` or `~/<name>/<name>.code-workspace`.
2. Before you change the file, ask the person.
3. Add one entry to `folders`, for example `{ "name": "api", "path": "./code/api" }`. The path is relative to the folder of the list file. Keep the comments and the other entries.
4. Run `hopen <name> --no-attach`. It adds a workspace only for the new folder.

## Split a tab with a template

`hopen --apply grid` splits the current tab with the `grid` template. It works only inside Herdr, in the tab to split. The templates are in `~/.config/hopen/templates`. Each line of a template file is one pane: `NAME FROM DIRECTION SIZE COMMAND`.

## Check or update the setup

On a server machine, a client machine, or one machine as both, `--check` reports what is done and what is missing. It changes nothing:

```bash
curl -fsSL https://github.com/MussaCharles/herdspace/releases/latest/download/bootstrap.sh | bash -s -- server --check
```

Use `client --server <name>` or `both` in place of `server`, for the role of the machine. If the person does not want the editor keys of herdspace, add `--keep-terminal-keys` to a client or `both` run. The setup saves the choice. To update, run the same command with no `--check`. Show the person the output of `--check` first, and ask before the run.

To update only `hopen`:

```bash
curl -fsSL https://github.com/MussaCharles/herdspace/releases/latest/download/install.sh | bash
```

## Rules

- Do not stop the Herdr server, and do not close a workspace, a tab, or a pane of the person.
- Before you change a list file or a template, ask the person.
- If a command asks for a password, stop. Give the command to the person to run in their own terminal.
- Do not print the contents of `~/.ssh` or of another secret file.
