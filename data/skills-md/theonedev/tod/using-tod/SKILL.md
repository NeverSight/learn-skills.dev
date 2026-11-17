---
name: using-tod
description: Query and operate on OneDev issues, pull requests, builds, and projects with tod. Use for general OneDev tasks outside the specialized workflows.
---

# Use the tod CLI

Use `tod` configured with `server-url` and `access-token`. Run `tod --help`
to find commands and `tod <command> --help` for arguments and flags.
API commands generally print the server response. Code-comment commands use
the `id` from `tod pr get-code-comments`.

## Project and reference context

- `tod` infers the current project from Git remotes. Use `--working-dir`
  to select a different local directory, or a qualified reference to select
  a server project. `123` and `#123` require a current project. Use
  `myproject#123` or `PROJ-123` otherwise. Reuse qualified references from
  API responses in later commands and handoffs, especially after switching
  checkouts. Qualify references in global queries such as
  `fixed in pull request "myproject#42"`.
- Issue, PR, and build lists use `--project`, then the current project,
  then all accessible projects. Outside a checkout, specify `--project`
  for issue creation and branch/tag builds. For PR creation and its
  requirement queries, supply `--source-project` and `--source-branch`.
- Checkout and current-reference commands, `tod project current`,
  `tod remote`, top-level `tod get-commit-message-requirement`,
  `tod build check-spec`, and `tod build run --local` need a local
  repository. Local builds infer the project from the checkout and reject
  `--project`. For API-only work, use qualified references and explicit
  project flags directly.
- `tod issue create-branch` accepts a qualified reference without a
  checkout. `tod issue checkout` requires the issue project's repository and
  can create the server branch even without `--for-write`.
- Use `tod issue current-reference` or `tod pr current-reference` for the
  current checkout. Ask for the reference if the command cannot resolve it.

## Build reports

- `tod build get-code-problems <build> "<report>" <severity>` returns findings
  at or above the supplied threshold. Use `CRITICAL`, `HIGH`, `MEDIUM`, or `LOW`.
- `tod build get-unit-test-report <build> "<report>"` returns report data.
  Add `--artifact <artifact-path> > <output-file>` to save a named report artifact.

## Markdown input

Pass exact Markdown from a temporary file outside the repository. For
stdin, pass `-` to the matching flag, for example
`tod issue add-comment myproject#123 --file -` with a quoted heredoc.
File input replaces the corresponding inline argument or flag. Omit both
when optional text is absent.

| Flag | Commands |
| --- | --- |
| `--description-file <path>` | `issue create`, `issue edit`, `pr create`, `pr edit` |
| `--comment-file <path>` | `issue change-state`, `issue log-work`, `pr discard` |
| `--note-file <path>` | `code-comment resolve`, `code-comment unresolve` |
| `--summary-file <path>` | `pr approve`, `pr request-changes` |
| `--file <path>` | `issue add-comment`, `pr add-comment`, `pr add-code-comment`, `code-comment add-reply` |

For line-anchored PR comments, use `--on-file <path>` and
`--from-line <line>`. In authored Markdown, use OneDev references such as
`PR #42`, `issue team/app#7`, and `build APP-9`. A reference without an
entity type means an issue.

Download and inspect each linked image or file in issue and PR descriptions
and comments. Use `tod download <original-url> <output-file>` with the URL as
written, then open the downloaded file to understand its contents.

## State-changing commands

Get confirmation for changes the user has yet to authorize. This includes
writes, reviews, merges, build runs, and issue checkout when it can create
a branch. Read-only queries can run directly.
