---
name: sdlc-setup-wiki
description: Create, upgrade or connect a project wiki for the sdlc-skills - a git repository that holds a project's knowledge bundle in wiki/ and a copy of the checking tool in .wiki-llm/ - and add an application to it. Use when the user wants to start a project wiki, set up or initialise the wiki repository, connect the current folder to an existing wiki, upgrade or repair the wiki's tool copy after updating the skills, add a new application to the wiki, or when another sdlc-skills skill says the wiki is older than the skills, was edited by hand, cannot be found from this folder, or has no such application.
---

# Set up a wiki repository

A wiki repository is a project's own git repository. It holds the knowledge
bundle in `wiki/` and a copy of the tool and schema in `.wiki-llm/`, so people,
skills and CI check the wiki with the same rules.

This skill does four things:
- it creates a wiki repository, or brings its tool copy up to this skill's
  release;
- it links the **workspace** (the folder the user started you in) to the wiki
  repository, by writing a note into the workspace's `AGENTS.md` and
  `CLAUDE.md`, so other sdlc-skills find the wiki without asking;
- it adds an application to the wiki when the user asks;
- it never adds any other concept; other skills do that.

## The tool

This skill carries its own copy of the tool: `wiki-llm/tools/wiki_llm.py` in
the folder that holds this `SKILL.md`. Use its absolute path for every command
below, and remember the workspace:

```bash
TOOL="python3 <folder of this SKILL.md>/wiki-llm/tools/wiki_llm.py"
RELEASE="$(cat <folder of this SKILL.md>/RELEASE)"
WORKSPACE="$(pwd)"
```

Every draft this skill finishes is stamped `--by "sdlc-setup-wiki/$RELEASE"`.

Every command prints JSON. Exit 0 is success. Exit 1 is a failed check or a
refusal: read `error`, `message` or `validate.errors`. Exit 2 is a usage or
environment problem: show `error` to the user and stop, unless a step below
says otherwise.

## 1. Find out what to do

1. Get the wiki repository's path from the user, unless they already gave it
   or, when they ask to add an application, the workspace note between
   `<!-- sdlc-skills:start -->` and `<!-- sdlc-skills:end -->` names it. For example
   `../shop-wiki`. A path relative to the workspace is fine. Call it `WIKI`.
   The folder may not exist yet.
2. Note whether the workspace **is** the wiki repository:
   `[ "$(cd "$WIKI" 2>/dev/null && pwd -P)" = "$(pwd -P)" ]`. Call this case
   SELF.
3. Run `$TOOL copy check "$WIKI"` and act on the result:

| Result | Do |
|---|---|
| exit 2 with "no tool copy found" | **Create** (section 2) |
| `status` `edited` or `older` | **Upgrade** (section 3) |
| `status` `current`, and the user asked to add an application | **Add an application** (section 4a) |
| `status` `current` | **Link only** (section 4) |
| `status` `newer` | The wiki was set up by a newer release. Tell the user to update their installed sdlc-skills, then run this skill again. Stop |

To add an application to a wiki that is not `current`, upgrade it first; once
the upgrade's pull request is merged, run this skill again to add it.

A draft starts from the remote's default branch, else a local `main`, else
`master`. If `draft start` reports "no default branch", tell the user the
repository needs one of these, and stop.

## 2. Create

1. Ask the user for:
   - the Application key: lower-case words joined by `-`, for example `shop`;
   - the Application title, for example `Shop Platform`;
   - the owner team, for example `payments`.
2. Show what will be written, and ask for approval:
   - in `WIKI`: `README.md` with the checks to run by hand or in CI (kept if
     one exists), `.gitignore` lines `.worktrees/` and `__pycache__/`,
     `.wiki-llm/` (the tool copy), `wiki/index.md` and `wiki/<app>/overview.md`;
   - the workspace note in each `AGENTS.md` and `CLAUDE.md` of the workspace,
     or a new `AGENTS.md` when neither exists.

   Also say how the wiki is saved: as the first commit on `main` when `WIKI` is
   new, not a git repository, or has no commits; otherwise on a draft branch
   `wiki/setup` for a pull request.
3. On approval, pick the case.

   **New folder, no git repository, or a repository with no commits.**

   ```bash
   mkdir -p "$WIKI" && cd "$WIKI"
   git rev-parse --git-dir >/dev/null 2>&1 || git init
   git symbolic-ref HEAD refs/heads/main
   $TOOL init . --app <key> --title "<title>" --owner-team <team>
   ```

   `init` must report `ok: true`. In the SELF case, run `$TOOL link . .` now,
   so the note is part of the first commit. Then:

   ```bash
   git add -A
   git commit -m "Set up the <title> wiki"
   cd "$WORKSPACE"
   ```

   Report the commit, and that the user can push `main` to a new remote. Then,
   unless SELF, go to section 5.

   **A repository with commits.** Write the skeleton into a draft:

   ```bash
   cd "$WIKI"
   $TOOL draft start setup
   $TOOL init .worktrees/setup --app <key> --title "<title>" --owner-team <team>
   ```

   In the SELF case, run `$TOOL link .worktrees/setup .worktrees/setup`. Then
   run `cd .worktrees/setup` and
   `$TOOL draft finish --by "sdlc-setup-wiki/$RELEASE"`, and go to section 6.

## 3. Upgrade

1. Show the user `copy.release_version` and `source.release_version` from
   `copy check`, and whether the Schema version changes
   (`copy.schema_version` and `source.schema_version`). When `status` is
   `edited`, list `added`, `missing` and `changed`: those hand edits will be
   replaced. Unless SELF, also say which workspace files get the note.
2. Ask for approval. On approval, with `<version>` the value of
   `source.release_version`:

   ```bash
   cd "$WIKI"
   $TOOL draft start setup-<version>
   $TOOL copy install .worktrees/setup-<version>
   ```

   If `draft start` refuses because the branch exists, an earlier upgrade
   left it. If its pull request was merged or closed, run
   `$TOOL draft discard setup-<version> --remote` and start again. If it is
   still open, tell the user to finish that pull request first, and stop.
3. In the SELF case, run `$TOOL link .worktrees/setup-<version> .worktrees/setup-<version>`.
4. Run `cd .worktrees/setup-<version>`. When the Schema version changes, run
   `$TOOL migrate`. If it reports that no migration is available, tell the user
   the wiki cannot be upgraded with this release. Then run
   `cd "$WIKI" && $TOOL draft discard setup-<version>` and stop.
5. Run `$TOOL draft finish --by "sdlc-setup-wiki/$RELEASE"`, then go to
   section 6.

## 4. Link only

The wiki is up to date. Tell the user, and say which workspace files get the
note. On approval:

- **Not SELF.** Go to section 5.
- **SELF.** The note belongs in the wiki repository, so it goes through a
  draft:

  ```bash
  $TOOL draft start link
  $TOOL link .worktrees/link .worktrees/link
  ```

  If `written` is empty, the note is already there. Run
  `$TOOL draft discard link`, report "already linked", and stop. Otherwise
  run `cd .worktrees/link` and
  `$TOOL draft finish --by "sdlc-setup-wiki/$RELEASE"`, then go to
  section 6.

## 4a. Add an application

1. Ask the user for what they have not given:
   - the Application key: lower-case words joined by `-`, for example
     `billing`; it must not be a folder in `$WIKI/wiki/` already;
   - the Application title, for example `Billing`;
   - the owner team, for example `finance`.

   If the key the user wants is already a folder in `$WIKI/wiki/`, say that
   the application exists, offer a different key, and start nothing until
   they give one.
2. Show what will be written: `wiki/<key>/overview.md` and the indexes the
   tool updates, on a draft branch `wiki/app-<key>` for a pull request. Ask for
   approval.
3. On approval:

   ```bash
   cd "$WIKI"
   $TOOL draft start app-<key>
   cd .worktrees/app-<key>
   $TOOL app add --key <key> --title "<title>" --owner-team <team>
   $TOOL draft finish --by "sdlc-setup-wiki/$RELEASE"
   ```

   If `app add` refuses because the application exists, run
   `cd "$WIKI" && $TOOL draft discard app-<key>`, tell the user, and stop.
   Otherwise go to section 6, with the commit message
   `Add the <title> application`.

## 5. Link the workspace

```bash
cd "$WORKSPACE"
$TOOL link "$WORKSPACE" "$WIKI"
```

Report the files in `written` (or that the note was already there), and any
`warnings`. If the workspace is a git repository, tell the user the note is an
ordinary change there: they commit it if teammates should share it.

## 6. Change-set gate

1. If `draft finish` is not `ok`, show `missing_logs` and `validate.errors`.
   A new tool version can report problems the old one did not. Do not fix
   wiki content in this skill. Tell the user what failed, run
   `$TOOL draft discard <key>` from `WIKI`, and stop.
2. Run `$TOOL draft diff` and show the user the change set:
   - list the files;
   - say that `.wiki-llm/` files are the tool copy, written by the tool;
   - say that `AGENTS.md` and `CLAUDE.md` hold the workspace note.

   Propose a commit message such as `Set up the <title> wiki`,
   `Upgrade the wiki tool to <version>`, `Link the wiki to its workspace` or
   `Add the <title> application`.
3. On approval, run `$TOOL draft commit -m "<message>"; cd "$WORKSPACE"` as
   one command: `draft commit` removes the worktree you are in, so judge it by
   the JSON it prints, not by an error about the current directory.
   - Report the branch, and that the user opens the pull request; the change
     reaches the wiki when it is merged.
   - If there is no remote, say that the branch has to be pushed first.
   - Unless SELF, or this run only added an application, go to section 5.
4. On rejection, run `$TOOL draft discard <key>` from `WIKI`.

## Rules

- Change nothing before the user approves what will be written.
- Never edit files in `.wiki-llm/` by hand; `copy install` replaces the whole
  folder.
- Never write the workspace note by hand; `link` replaces it in place.
- Never open a pull request or call a hosting service; the user does that.
- Never push to `main` of a repository that already has commits.
