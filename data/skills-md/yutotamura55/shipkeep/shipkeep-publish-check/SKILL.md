---
name: shipkeep-publish-check
description: Use before making a Git repository public, or when reviewing a repository that is already public, to find secrets and personal data anywhere in its history and to check the files and settings that publishing needs (license, README, SECURITY.md, .env handling, and GitHub secret scanning, vulnerability reporting, Dependabot alerts, and Actions token permissions).
---

# Check a repository before publishing it

Making a repository public publishes every commit on every branch and tag, not
only the current files. This skill scans that history (local branches and tags,
plus the branches already on the `origin` remote) and reports, check by check,
what is ready and what must be fixed first.

The skill only reads. Do not change the repository, commit, rewrite history,
push, or change GitHub settings while running it. Fixing is a separate step that
the user decides on after reading the report.

## Never reveal what you find

The point of the check is to keep secrets and personal data private. Treat
every value you find as confidential, including in this conversation and in the
output of the commands you run:

- Never print, quote, or paste a secret, an email address, a local user name, a
  local path, or a denylist term. Not even part of one.
- Refer to a finding by its kind and location: commit, file, and line. When a
  path holds confidential text, the scan hides it; keep it hidden.
- Do not open the files or commits behind a finding (for example with
  `git show`): that prints the values into the command output. Judge from the
  `context` field instead, which is the line with the values masked.
- Do not copy `context` lines into the report. Masking is best effort (see
  Limits), so describe what a line shows instead ("an AWS access key ID
  assigned to `key`").

## Steps

1. **Pick the repository.** Use the path the user gave, or the current
   repository; a subdirectory scans the whole repository. The scan reads
   commits only, because that is what a push publishes. If there is
   uncommitted work, tell the user it is not checked; committing it is their
   choice, not part of this skill.
2. **Find the denylist, if any.** A denylist is a plain text file (UTF-8)
   outside the repository with one private term per line, such as client or
   product names that must not be published. Lines starting with `#` are
   comments. Use the file the user names, or `~/.config/shipkeep/denylist.txt`
   when it exists. Never ask the user to type the terms into the conversation.
3. **Run the scan** with Python 3.10 or newer and Git. `gh` is optional: when it
   is installed and signed in, the scan also reads the GitHub settings.

   ```bash
   python3 <this skill's directory>/scripts/scan.py <repository> [--denylist <file>]
   ```

   The script prints one JSON document. It holds kinds, locations, and masked
   lines only, never a secret, an address, a path, or a denylist term, so the
   user can safely share it. With `--format result` it prints the same facts
   in the common shipkeep result format (`references/result.schema.json`),
   which the Issue converter and other shipkeep skills read; use it when the
   result will be filed or kept, and the default shape when you only read it. Exit code 2 means the path is not a Git repository,
   Git is missing or failed, the repository is a partial clone (reading its
   history could fetch objects into it; scan a full clone instead), or the
   denylist cannot be read; report the message and stop.
4. **Judge the findings** from their `context`. Mark a finding as a false
   positive only when the masked line shows the value is not real, for example
   a placeholder variable or an obvious dummy. Being in a test, a fixture, or
   documentation is not enough: real credentials are often committed there.
   When you cannot tell, keep it as a finding and say it needs the user's
   check. Keep false positives in the report, marked as such, with the reason.
5. **Report** in the user's language, using the format below.

## Report format

Start with one line that states:

- how many checks need fixing, taken from `counts.fail` in the scan output
  rather than counted by hand; if you marked every finding of a failed check as
  a false positive, say so and give both numbers;
- how many checks could not be verified (`counts.unknown`), when any. Never
  call the repository ready while a check is unknown.

Then a table with one row per check, in the order of the scan output.

| Status in the JSON | Write it as |
| --- | --- |
| `pass` | Ready |
| `fail` | Needs fixing |
| `unknown` | Cannot verify, with what the user should check by hand |
| `not_applicable` | Not applicable, with the reason |

Under the table, list each finding of each failed check with its kind,
location, and your judgment. Then give the fixes, most urgent first.

## What each check means and how to fix it

| Check | What it looks for | How to fix |
| --- | --- | --- |
| `history_coverage` | Whether the local copy holds the whole history: not a shallow clone, and fetching every branch of `origin` | Run `git fetch --unshallow`, or fetch all branches, then scan again. Until then, treat passing history checks as unconfirmed |
| `commit_identity` | Commits whose author or committer address is not a GitHub noreply address | Set the noreply address in Git, then rewrite the history with `git filter-repo --mailmap` |
| `history_secrets` | Added lines that look like private keys or API tokens, including lines a later commit deleted and lines a merge added | **Revoke and replace the credential first**: removing it from history does not make a leaked key safe. Then remove it with `git filter-repo` |
| `history_personal_data` | Personal email addresses and local home paths in added lines and commit messages. Not counted as personal data: GitHub noreply addresses, `noreply`/`no-reply` mailboxes, the `git@` mailbox of clone URLs, example domains, asset names such as `logo@2x.png`, and the exact service addresses listed in `SERVICE_ADDRESSES` in `scan.py` (Dependabot's sign-off). A trailer name such as `[bot]` is not enough on its own. Every address is still masked in `context` | Edit the files and rewrite the history, or accept it if the user decides the data may be public |
| `denylist` | Denylist terms in added lines, file names, commit messages, and branch or tag names | Same as personal data; rename the branch or tag |
| `sensitive_files` | Files that should never be committed (`.env`, `.dev.vars`, key stores, Terraform state), even if deleted later | Remove them from the history, and replace any credential they held |
| `env_files` | For each local env file a project uses (`.env`, or `.dev.vars` in a Cloudflare Workers project): an ignore rule and an example file next to it | Add the ignore rule and an example file with empty values |
| `license` | A license file at the top level of HEAD | Choose a license with the user; without one, others may not reuse the code |
| `readme` | A non-empty README at the top level of HEAD | Write what the project is and how to use it |
| `github_settings` | GitHub secret scanning and push protection on the `origin` repository | Turn them on in the repository's Settings → Advanced Security (called Code security in older GitHub pages) |
| `security_policy` | A non-empty `SECURITY.md` at the top level, in `.github/`, or in `docs/` of HEAD, where GitHub looks for it | Write how to report a vulnerability, for example through GitHub's private reporting, without a personal email address |
| `private_reporting` | GitHub private vulnerability reporting on the `origin` repository. Not applicable while the repository is private, because GitHub offers it only for public repositories | Turn it on in Settings → Advanced Security right after making the repository public |
| `dependabot_alerts` | GitHub Dependabot alerts on the `origin` repository | Turn them on in Settings → Advanced Security |
| `workflow_token` | Whether the default `GITHUB_TOKEN` of GitHub Actions can only read, and cannot approve pull requests. Once public, pull requests from strangers run workflows | In Settings → Actions → General → Workflow permissions, choose "Read repository contents and packages permissions" and clear "Allow GitHub Actions to create and approve pull requests" |

Rewriting history changes commit hashes. Tell the user that it needs a force
push, that open pull requests and forks keep the old commits, and that GitHub
support must be asked to purge cached views of a leaked secret. Leave these
operations to the user.

## Limits

State these limits in the report when they matter:

- Secret detection uses built-in patterns for common key formats. It does not
  find every kind of secret, such as passwords in custom formats.
- `context` masks detected values, email addresses, local paths, denylist
  terms, values after `=` or `:`, quoted text, and long key-like text. A short
  value in another form can still show, which is why the report describes
  lines instead of quoting them.
- `env_files` notices a `.env` file only when one is committed, an example
  exists, or the code loads it explicitly (for example with `dotenv`).
  Frameworks that load `.env` on their own, such as Vite, Next.js, and Nuxt,
  are not detected.
- Files with binary extensions (images, archives, fonts) are not searched.
- The scan does not see uncommitted files, stashes, remotes other than
  `origin`, or settings outside GitHub.
- `private_reporting`, `dependabot_alerts`, and `workflow_token` need admin
  access to the repository. Without it, GitHub hides the settings, so they are
  reported as unknown rather than off.
