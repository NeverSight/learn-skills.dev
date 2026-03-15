---
name: github-gist
description: "Create, manage, and organize GitHub Gists using the gh CLI. Use this skill whenever a user wants to create a gist, share code snippets, manage existing gists, add files to a gist, list or search gists, edit gist content or descriptions, clone a gist, or delete a gist. Every gist created or modified must include a README.md documenting its purpose and contents."
---

# GitHub Gist Skill

Expert management of GitHub Gists via the `gh` CLI. All gists created through this skill include a `README.md` that documents the gist's purpose, content, and optional usage instructions.

## Core Rule: README.md is Mandatory

**Every gist must contain a `README.md` file.** When creating a new gist, always generate a `README.md` alongside any other files. When editing a gist that lacks a `README.md`, add one.

The README.md must include:
- **Description** — what the gist does or contains
- **Content summary** — what files are included and what each does
- **Usage** (optional, include when the gist contains runnable scripts or commands)

See `references/readme-template.md` for the standard template.

## Reference Files

| Reference | When to Load |
|-----------|--------------|
| `references/readme-template.md` | Before creating any gist — get the README.md template |
| `references/workflows.md` | For multi-step operations: create with multiple files, bulk edit, clone & modify |
| `references/search-and-manage.md` | For listing, filtering, viewing, or deleting gists |

## Quick Reference: Common Operations

### Create a new gist (single file)
```bash
# Always create README.md first, then create gist with both files
cat > /tmp/README.md << 'EOF'
# <gist title>

<description>

## Files

- `<filename>` — <what it does>

## Usage

<usage instructions if applicable>
EOF

gh gist create --public --desc "<description>" /tmp/README.md <your-file>
```

### Create a gist (multiple files)
```bash
gh gist create --public --desc "<description>" README.md file1.sh file2.py
```

### List gists
```bash
gh gist list                          # 10 most recent
gh gist list -L 50                    # 50 most recent
gh gist list --public                 # only public
gh gist list --secret                 # only secret
gh gist list --filter "pattern"       # filter by description/filename
gh gist list --filter "pattern" --include-content  # search file contents
```

### View a gist
```bash
gh gist view <id>                     # rendered view
gh gist view <id> --raw               # raw content
gh gist view <id> --files             # list filenames
gh gist view <id> --filename README.md
gh gist view <id> --web               # open in browser
```

### Edit a gist
```bash
gh gist edit <id>                         # interactive (opens editor)
gh gist edit <id> --filename <file>       # edit specific file
gh gist edit <id> --desc "new description"
gh gist edit <id> --add newfile.py        # add a file
gh gist edit <id> --remove oldfile.py     # remove a file
```

### Clone a gist locally
```bash
gh gist clone <id> [<directory>]
```

### Delete a gist
```bash
gh gist delete <id>
```

## Workflow: Creating a Gist

When a user asks to create a gist, follow these steps:

1. **Gather information** — determine the description, files involved, and whether it should be public or secret (default: secret)
2. **Generate README.md** — always write a `README.md` using the template in `references/readme-template.md`
3. **Assemble files** — write the actual script/content files if they don't already exist
4. **Create the gist** — use `gh gist create` with all files, including `README.md`
5. **Confirm and report** — show the user the gist URL

**Always load `references/readme-template.md` before writing the README.md.**

## Workflow: Adding Files to an Existing Gist

When adding files to a gist:
1. Check if a `README.md` exists: `gh gist view <id> --files`
2. If missing, create one with `gh gist edit <id> --add README.md`
3. Add the new file: `gh gist edit <id> --add <filename>`
4. Update the `README.md` to document the new file

## Determining Visibility

- **Secret** (default): private to owner, accessible by URL. Use when the content is personal or sensitive.
- **Public** (`--public`): listed publicly. Use when the intent is sharing with the community.

Ask the user if unclear. Default to secret.

## File Naming Convention

- Scripts: use the appropriate extension (`.sh`, `.py`, `.rb`, `.js`, etc.)
- Config snippets: use the actual config filename (e.g., `.zshrc`, `nginx.conf`)
- Documentation: always `README.md` (never `readme.txt` or `README.txt`)
- One-liners or reference cards: use `.md` format for readability

## Error Handling

| Error | Resolution |
|-------|-----------|
| `gh: not authenticated` | Run `gh auth login` |
| File not found | Verify path; use absolute paths in `/tmp/` for temp files |
| Gist ID not found | Run `gh gist list` to find the correct ID |
| Rate limited | Wait and retry; use `--limit` to reduce API calls |

---

> **Tip:** Use `gh gist view <id> --web` to open any gist in the browser for easy sharing.
