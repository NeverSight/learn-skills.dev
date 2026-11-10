---
name: anonymize-repo
description: Export an anonymized, history-free snapshot of a research repository for double-blind review — drop internal files, scrub names from text and Office/PDF metadata, scan for anything identifying, and check that the snapshot still builds. Use when a paper under anonymous review needs a code-and-data link, or the user asks to anonymize a repo, prepare an anonymous or private review repo, or link code for reviewers.
---

# Anonymize a repository for review

Make a clean copy for reviewers; never edit or push the original repository or its history. The bundled `scripts/anonymize_repo.py` does the mechanical work and fails on anything it can still find; the identity list and what to leave out are judgment calls for you and the user.

## 1. List what identifies the authors

Collect candidates and confirm them with the user:
- names, initials used as names, and usernames: `git log --format='%an %ae' | sort -u`, the README, `\author`, `\affiliation`, and `\email` in the paper, acknowledgements, the GitHub owner, the local user name;
- e-mail addresses, affiliations, lab and grant names, personal URLs;
- local paths (`/Users/<name>/`) that notebooks and logs pick up.

## 2. Write the config

Put `anonymize.toml` at the repository root (it is never exported; the format is in the script's docstring):
- `exclude`: agent and editor instructions (`CLAUDE.md`, `AGENTS.md`), internal notes, earlier review rounds, `.github/` (CODEOWNERS names people), slide decks, anything not needed to reproduce the paper.
- `[[replace]]`: author blocks in the README, `\author` lines, clone URLs. Every rule must match at least once, so a moved heading fails loudly instead of leaking.
- `[identity]`: the patterns from step 1 (use `\b` word boundaries for short names), and `allow` entries for false positives in data, scoped by path.

Commit the config, or pass `--config` from outside the repository.

## 3. Export and iterate

```bash
uv run <skill-dir>/scripts/anonymize_repo.py export <repo> <scratch>/anon --ref HEAD
```

It exports only tracked files at the ref, with no git history; drops the exclusions; applies the replacements; blanks author fields in Office metadata and PDF `/Author`; and scans text files, Office document parts, `.xls` bytes, and PDF text (with `pdftotext`). Fix every hit at its source, in the config, or as a scoped `allow`, and re-export until the scan is clean. Ask the user before allowing a hit in anything but raw third-party data.

## 4. Check the snapshot stands alone

Run the project's tests and build inside the export, for example `uv run pytest` and a workflow dry run. A link that does not reproduce the paper's numbers is worse than none.

## 5. Publish (only with the user's approval)

As the user prefers:
- **Anonymous GitHub** (anonymous.4open.science): create an empty private GitHub repository under the user's account (no README or license; GitHub would commit them under the user's name), then export straight to it:
  ```bash
  uv run <skill-dir>/scripts/anonymize_repo.py export <repo> <scratch>/anon --ref HEAD --push <mirror-url>
  ```
  `--push` commits the export as "Anonymous" and pushes it to `main` (`--branch` for another). Register the repository on Anonymous GitHub; private repositories need its GitHub App. Enter the identity patterns as terms to replace, as a second layer.
- **OSF**: upload the export to a private project and make a view-only link with *Anonymize* ticked. That hides contributor names in OSF itself, not in files, which is why the export comes first. The project title must not identify anyone.

Open the link in a logged-out browser before it goes into the paper.

To re-publish after a change to the code or data, run the same `--push` command into a fresh directory. It commits the new tree as "Anonymous" on top of the mirror's head and pushes without force. It skips the commit when nothing changed, and refuses to push when the scan finds anything or the mirror has a commit by anyone else (as the original repository would). Anonymous GitHub keeps serving the old snapshot until the owner clicks Refresh on the repository in its dashboard; then check the link logged out again. On OSF, replace the uploaded files. Never push the original repository.
