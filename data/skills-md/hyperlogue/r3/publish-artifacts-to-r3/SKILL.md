---
name: publish-artifacts-to-r3
description: Publish HTML pages, documents, files, or code changes to r3 for human review, and respond to feedback on existing r3 artifacts. Use when the user asks to use r3 or supplies an r3 artifact or feedback command.
---

Run `r3 guide` once per session to get instructions for publishing artifacts and
responding to feedback. This tries the executable on `PATH`; if it succeeds,
use that executable for subsequent commands.

If `r3` is unavailable, run the latest published release with npm:

```sh
npx --yes @hyperlogue/r3@latest guide
```

With Bun:

```sh
bunx --bun @hyperlogue/r3@latest guide
```

On NixOS, use the Nix flake:

```sh
nix run github:hyperlogue/r3#r3 -- guide
```

Follow the executable's guide for publication and the feedback workflow. Before
preparing an artifact kind for the first time in a session, read its preparation
guide using the `guide html`, `guide files`, or `guide diff` subcommand.
Use `--help` for command details.

Share the returned artifact URL. When responding to feedback, publish changes as
a new version under the same artifact ID and reply to its threads. This keeps the
comments and version history together.
