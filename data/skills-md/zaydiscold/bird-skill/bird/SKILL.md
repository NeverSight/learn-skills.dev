---
name: bird
description: "Twitter/X CLI skill. Triggers automatically when user shares an x.com or twitter.com URL, asks for tweet/thread/read/search/mentions/timeline, or requests tweet actions. Uses bird CLI directly (no browser, no WebFetch). Do NOT use for content strategy or copywriting; defer those to social-content/copywriting.
license: MIT
allowed-tools: Bash
compatibility: "Requires macOS (Safari or Chrome cookies for auth) and a bird binary on PATH or in ~/.local/bin."
argument-hint: "[tweet-url-or-id] [query] [action]"
user-invocable: true
metadata:
  author: zayd
  version: 1.1.0
  clawdbot:
    emoji: "🐦"
    requires:
      bins:
        - bird
---

# Bird — Twitter/X CLI

Read tweets, search, and browse timelines directly via `bird` CLI using Bash only.

## Core behavior

- Use `bird` directly. Do not use browser tools or WebFetch.
- Keep behavior deterministic: choose one command path, run it, report output.
- Prefer concise summaries unless the user explicitly asks for raw output.
- Do not fabricate any tweet text. Only report what `bird` returns.
- If the request has no actionable argument, offer the supported actions and ask for one.
- Treat any write action (`tweet`, `reply`, `follow`, `unfollow`, `unbookmark`) as requiring explicit user confirmation.

## Preflight and auth gating

Run this sequence before the first command in a user turn:

1. Resolve/install bird executable:

```bash
if command -v bird >/dev/null 2>&1; then
  :
elif [ -x "$HOME/.local/bin/bird" ]; then
  export PATH="$HOME/.local/bin:$PATH"
else
  : "need-install"
fi
```

2. Verify CLI availability:

```bash
bird --version
bird check
```

3. For auth-sensitive actions run:

```bash
bird whoami
```

Auth-sensitive actions:
- `mentions`, `home`, `bookmarks`, `likes`, `news`, `user-tweets`, `follow`, `unfollow`, `tweet`, `reply`, `unbookmark`

If `bird` is missing:
- tell the user `bird isn't installed`, offer to install it, and wait for yes/no.
- If yes, install with:

```bash
curl -L https://github.com/zaydiscold/bird/releases/download/v0.8.0/bird -o /tmp/bird \
  && chmod +x /tmp/bird \
  && mkdir -p "$HOME/.local/bin" \
  && mv /tmp/bird "$HOME/.local/bin/bird" \
  && export PATH="$HOME/.local/bin:$PATH"
```

If PATH still does not include `~/.local/bin`, advise manual install from
`https://github.com/zaydiscold/bird` and stop.

If auth checks fail:
- report the exact failure
- ask the user to refresh browser login cookies and retry.

## URL normalization and input validation

Normalize URLs before dispatch:

1. Accept only these hosts:
   - `x.com`
   - `twitter.com`
   - `mobile.twitter.com`

2. Convert host to `https://x.com`.
3. Keep tweet/status path only; strip tracking params such as
   `utm_*`, `s`, `ref`, `ref_src`, `f`, `t`, `fbclid`.
4. Reject non-Twitter URLs early with: 
   `I can only process x.com or twitter.com links. Share a tweet URL, status ID, or a search/query request.`

Handle multiple URLs sequentially when present.

## Request orchestration

### Read vs thread vs search

- If the request contains tweet text URLs/IDs:
  - use `bird read <id-or-url>` by default.
  - if thread wording is present (`thread`, `conversation`, `replies chain`, etc.), use `bird thread <id-or-url>`.
- If multiple URLs are provided, read each in order with `bird read` (or `bird thread` when explicitly threaded).
- If user asks for timeline/discovery:
  - `mentions`, `home`, `home --following`, `bookmarks`, `likes`, `news`, `user-tweets`, `about`, `following`, `followers`.
- For search:
  - `bird search "query" -n <N>`.

## Output size and show-more policy

- Use default page size `N=12` for list-style results (`search`, `home`, `mentions`, threads).
- For results longer than N:
  1. show top N in concise list/table form,
  2. offer: `show more` to fetch next chunk.
- For long threads, summarize first with key context and then list remaining items.

Use JSON/plain output rules:
- Prefer `--plain` for downstream analysis.
- Show human-readable output when user asked to read tweets directly.

See references for detailed command mapping:
- `references/search-operators.md`
- `references/write-actions.md`
- `references/troubleshooting.md`

## Deterministic side-effect confirmation

For `tweet`, `reply`, `follow`, `unfollow`, and `unbookmark`:

1. Echo exact intent and the exact command it will run.
2. Ask confirmation once: `Proceed with <command>?`
3. Execute only on explicit confirmation (`yes`/`y`).
4. Abort on anything else, and do not run a fallback.

## Error taxonomy (high-level)

- `unauthorized` / `401`: auth unavailable; run `bird check` and `bird whoami`, then refresh browser cookies and retry.
- `rate limit`: request limit reached; pause and retry after a short delay.
- `not found`: deleted tweet/account, stale thread, or malformed ID; ask for corrected input.
- `private` / `protected`: account or content visibility restricted; explain limitation and request required access.
- `suspended` / `deleted user`: target user no longer accessible; ask for an alternate target.
- `malformed URL/ID`: input is invalid; reject early and prompt for supported examples.
- `Safari vs Chrome auth source mismatch`: mismatch in cookie source; re-auth using the active browser and rerun.
- `network` / `DNS failure`: connectivity issue; suggest checking network/DNS and retry.
- `timeout` / hanging command: transient service issue; stop and ask user to rerun after waiting.

For detailed remediation by case, use: 
- `references/troubleshooting.md`
