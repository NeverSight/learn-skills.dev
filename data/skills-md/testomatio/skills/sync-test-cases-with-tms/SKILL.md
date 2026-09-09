---
name: sync-test-cases-with-tms
description: Synchronize test scenarios and cases between a local project and Testomat.io. Use this skill whenever the user wants to pull/export/download tests from Testomat.io; or push/import/sync new or updated test cases back to the TMS in corresponding `*.test.md` format. Supports custom directories, markdown test format and advanced import/export workflows.
inputs:
  testDir:
    description: "Target directory for pulled tests"
    required: false
license: MIT
metadata:
  author: Testomat.io
  version: 1.0.0
---

# Sync Test Cases with TMS

Sync Markdown test cases (`*.test.md`) between the local project and Testomat.io.

Use when the user wants to:
- Pull/export/download tests from Testomat.io to local Markdown files.
- Push/upload/import local Markdown tests to Testomat.io.
- Bulk edit: pull cases -> edit locally -> push back to TMS.

## Setup

- Check for the `TESTOMATIO` token: skill input -> `.env` in project root -> ask the user.
- Save the token to `.env`: `TESTOMATIO=tstmt_xxxxx`.
- If the user has no key: get it in Testomat.io under **Settings → Project → Project Reporting API key** (`https://app.testomat.io/projects/<project-id>/settings/project`).

## Running the CLI

- Run `check-tests` via `npx`. Do not install it as a project dependency.
- **The first `check-tests` call in the session must be `npx check-tests@latest …`** to resolve the latest version. All later calls in the same session use plain `npx check-tests …`.
- **Use only options documented here, in [TESTOMATIO_CLI.md](./references/TESTOMATIO_CLI.md), or listed by `npx check-tests --help`. Do not invent options** (e.g. `--pattern`, `--force`).

## Pull

Downloads test scenarios from Testomat.io and saves them as local Markdown files.

Directory selection — if the `testDir` input is provided or the user passes `-d <path>`, use that path. Otherwise:
- Workspace is empty or for manual tests only: pull to root.
- End-to-end testing project: pull to the `manual-tests` directory.
- Any other case: pull to `.testeiya/manual-tests` (ensure `.testeiya/` exists and is gitignored).

Cache-folder rules:
- Default pull target is the gitignored cache `.testeiya/manual-tests/`. Add `.testeiya/` to the project `.gitignore` if it is not there yet.
- **Pulled cases must never land in a tracked folder** (`manual-tests/`, etc.) — that pollutes the repo.
- Being gitignored does not block editing the files or pushing them back.
- If the repo already keeps its `*.test.md` files in a tracked folder, don't pull — work with them in place, or pass `-d <that folder>` for an in-place refresh.
- This matches `scan-automation-project`, which pulls the *code* into `.testeiya/code/` when it runs inside a manual-tests repo.

```bash
npx check-tests pull -d .testeiya/manual-tests
```

- To pull only specific suites (user names a suite or gives suite IDs): `npx check-tests pull --suite-ids "@S12345678,@S87654321"`.
- More pull options: [TESTOMATIO_CLI.md](./references/TESTOMATIO_CLI.md).

## Push

Uploads local Markdown tests to Testomat.io.

Pre-push file filtering — push only test case files, never project docs or requirements:
- Include files matching `*.test.md`, or Markdown files with valid `<!-- test ... -->` blocks.
- Ignore all other Markdown (`README.md`, `CHANGELOG.md`, documentation).
- If test cases live alongside other files, copy or move the test files into `.testeiya/manual-tests/` first.

Pre-push validation:
1. At least one `*.test.md` file exists.
2. Each file contains a valid test block:

```md
<!-- test
priority: ...
creator: ...
tags: ...
labels: ...
-->
# ... (test case title)

... (test case description)
```

```bash
# Specific files (preferred when known)
npx check-tests push --files login.test.md checkout.test.md

# Testeiya cache folder
npx check-tests push -d .testeiya/manual-tests
```

- **When the files to push are known** (e.g. just produced by `qa-write-test-cases` / `improve-test-cases`), **pass them explicitly via `--files`** (alias `-f`). Without `--files` the CLI falls back to the default glob `**/*.test.md`, which may pick up unrelated files.
- Quote glob patterns. Paths resolve relative to `--dir`.
- Use `-d` when `.testeiya` or `manual-tests` directories exist.
- **Push only the test cases directory** (e.g. `.testeiya/manual-tests`, not `.testeiya/`).
- More push options and examples: [TESTOMATIO_CLI.md](./references/TESTOMATIO_CLI.md).

## Summary Output

After syncing, print a short log-style summary:

```
Sync Complete:
- Action: pull/push
- Directory: <path>
- Tests synced: 15
- Status: Success
```
