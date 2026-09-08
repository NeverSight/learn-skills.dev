---
name: browse-x
description: Read public X posts, threads, profiles, and search results. Use for X/Twitter links or research.
allowed-tools:
  - Bash(bun scripts/browse-x.ts *)
  - Bash(curl *x.pcstyle.dev*)
---

# browse x

public content through x.pcstyle.dev. no X login needed. run the helper from this skill's directory:

```bash
bun scripts/browse-x.ts "https://x.com/handle/status/123"
bun scripts/browse-x.ts profile handle
bun scripts/browse-x.ts search "from:handle release"
bun scripts/browse-x.ts followers handle
bun scripts/browse-x.ts following handle
```

## options

markdown by default. `--json` for structured output, `--full` for metadata, `--compact` for less. use `--cursor` with the returned cursor to continue. run `bun scripts/browse-x.ts --help` for thread, feed, and other options.

optional: `X_MD_API_KEY` sends a bearer key; `X_API_BASE` changes the host. never print the key. invalid or disabled keys return 401.

## limits

public and keyed requests have different quotas. on 429 (exit 3), wait for the printed `Retry-After`; don't loop retries. exit 2 means bad arguments, exit 1 means another error. private or deleted content may be unavailable. check `warnings`; don't invent missing replies, media, or pinned posts.
