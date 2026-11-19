---
name: pr-description
description: Write a board pull request's title and description as AGENTS.md's "pr titles and descriptions" asks, with the evidence to show it working. Use whenever you open a PR in this repo or rewrite one's title or body.
---

# Write a PR's title and description

Follow "pr titles and descriptions" in AGENTS.md: the title, the four answers
(Users, Protocol / backends, Performance / I/O, Tests), and the rules after
them. This says how to get the evidence here.

## Evidence

- **CLI and output changes:** run the commands on a real board (`vb serve` in
  a scratch directory, or the verify-board skill) and paste what printed in a
  `text` block with the command line. Trim it; don't retype it. For a bug, the
  wrong output on `main`, then the right one on the branch.
- **UI changes** (the inspector, the docs site, Slack or GitHub rendering): a
  screenshot, or a short video for a flow. Add it to the PR on github.com, or
  attach it to the PR's board thread (`vb reply <root id> --attach <file>`) and
  say where it is.
- **What can't be shown** (a race, a refactor, a bump): the test that fails
  without the change, or the check you ran, in one line.
- **What a test fakes:** a platform's API (Slack, GitHub) is fine to fake, and
  the Tests line says so. A test that mocks board's own code tests the mock.
- **SDK samples:** copy the imports from the file the sample came from (the
  factory's `route.ts`, a test), every `@vercel/board/*` one, so the sample shows
  where each name lives.

## Example

Title: `feat(sync)!: resolve platform links and list a thread's copies`

````markdown
Go between a board message and its copies on Slack and GitHub.

- **Users:** `vb sync <id>` lists where a thread is synced; `vb read <link>` reads the thread a Slack or GitHub link names.
- **Protocol / backends:** breaking for custom backends: 2 new methods, `synced` and `linked`. The conformance kit's `sync` group checks both.
- **Performance / I/O:** `vb sync`: 3 board reads, plus 1 `chat.getPermalink` per Slack copy. `vb read <link>`: 1 lookup per sync entry of the link's platform, then the thread; no platform calls.
- **Tests:** the CLI as a subprocess against a board over HTTP, in-process boards on `local()` and `http()`, and the conformance kit. Slack's and GitHub's APIs are faked; nothing of board's is.

### Users

```text
$ vb sync 2
slack  C1:1727000000.123456  https://acme.slack.com/archives/C1/p1727000000123456

$ vb read https://acme.slack.com/archives/C1/p1727000000123456
#2  U_ADA · 0s
      checkout is down
```

A link the board didn't sync and one in a channel you can't read get the same
`error: Couldn't find that link's message on this board.`

```ts
import { board } from '@vercel/board'

const team = board()
await team.sync(id)     // { targets: [{ target, key, thread, message, url, undelivered }] }
await team.linked(url)  // the thread, as team.thread(id) answers it
```

### Protocol / backends

```ts
synced  GET /messages/:id/sync → SyncedView  // from sync's records
linked  GET /links?url=        → ThreadView  // never asks the platform

// SyncProvider, both optional, by the platform's own IDs:
locate(url): { thread, message | null } | null
url(thread, message): Promise<string | null>
```

- Custom backends implement `synced` and `linked`; `ChatSyncProvider` subclasses rename the protected `locate()` to `locationOf()`.

### Open

- A board without a provider for a platform can't read that platform's links.
````
