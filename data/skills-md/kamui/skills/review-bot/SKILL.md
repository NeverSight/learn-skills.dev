---
name: review-bot
description: "Mint GitHub App installation tokens and resolve the reviewing identity a repository's tracker doc declares. Use when a publishing skill needs the login and review-token command for a reviewing app, or when a person invokes /review-bot to create, install, or check the app."
compatibility: Requires Python 3.9+ and openssl on macOS or Linux
---

# Review bot

Publishing skills can post reviews as a GitHub App, so a pull request's author is not reviewing their own work. This skill is the mechanism behind that: it holds the script that mints the app's short-lived installation token and reports the app's identity. The app itself is declared per repository, its private key is held per machine, and nothing here reads a config file or infers a repository from a remote.

## The Reviewing identity block

A repository declares its reviewing app in `docs/agents/issue-tracker.md`, in exactly this block, which every publishing skill reads:

```text
## Reviewing identity

- **Reviewing app**: <app name>
- **Client id**: <client id>
```

An optional third field, **Review-token command**, holds a literal shell command for a repository whose token comes from somewhere else (a bot account's PAT from a secret store, for instance). When it is present, the publisher uses it as-is and does not consult this skill.

## Where the key lives

The private key is the only per-machine item. `scripts/review_token.py` resolves it as `--key`, then `REVIEW_BOT_KEY`, then `~/.config/review-bot/<client id>.pem`, then `~/.config/review-bot/key.pem`, mode 600. Keying by client id lets one machine hold keys for the apps of two repositories. The key never lives in a repository or under the synced skills directory; anyone holding it can post as the app.

## Resolve

What a dependent calls. Inputs: the client id from the tracker doc and `<owner>/<repo>`, the pull request's **base** repository, never the checkout's remote (a fork checkout's remote is the fork).

1. If this skill is not among the installed skills, or the tracker doc gives no client id, return the matching `unavailable` line below.
2. Run `python3 scripts/review_token.py whoami --client-id <id> <owner>/<repo>` from this skill's root. Its stdout carries the identity; every failure reason is on stderr with exit 1 or 2.
3. On exit 0 return two lines:
   - `reviewer: <slug>`, the parenthesised slug from the `app:` line. That is the GraphQL form, the bare login without `[bot]`, which is what consumers read and what `finish-it` stores in its packet. Do not take it from the `graphql login:` line, which may carry the suffix.
   - `review-token command: <the whoami "review-token command:" line, verbatim>`. It reads `python3 <absolute path to scripts/review_token.py> token --client-id <id> <owner>/<repo>`, with the path shell-quoted by `shlex.quote` so it survives the `sh -c "$tok"` re-parse consumers give it. A consumer that embeds the command inside a single-quoted `sh -c '…'` quotes any single quote it carries the ordinary way, as its publication reference says, so a script path with a space or other metacharacter is safe in both forms only through that step. The absolute path is the installed skill's own, so no `PATH` entry is involved.
4. On a non-zero exit return `review-bot: unavailable (<reason>)`, with the reason taken from stderr and phrased as one of:
   - not among the installed skills
   - no client id in the tracker doc
   - key not found at `<path>`
   - key unreadable
   - signing failed (not an app private key)
   - app not installed on `<owner>/<repo>`
   - forge refused (`HTTP <status>: <message>`)
   - network or TLS failure

The dependent then falls back to the authenticated user, records the reason, and withholds gating. Resolution never stops a run.

Worked example, for a repository declaring client id `Iv1.example` and a skill installed at `~/.agents/skills/review-bot`:

```text
reviewer: reviewer
review-token command: python3 /home/me/.agents/skills/review-bot/scripts/review_token.py token --client-id Iv1.example acme/widgets
```

## Setup and check

What a person invokes as `/review-bot`. Walk `references/setup.md` with them: create the app with the permissions it lists, install it on every repository it will review, generate and download the key, and place it at the per-client-id path. Then run `python3 scripts/review_token.py whoami --client-id <id> <owner>/<repo>` against a repository they name and show its output: the app, both logins, the installation and its permissions, and the review-token command. On a non-zero exit, report stderr and the step of `references/setup.md` it points at (a 404 is an installation that does not cover that repository; an `openssl` refusal is a file that is not the app's private key).

End by printing the exact block to paste into that repository's `docs/agents/issue-tracker.md`, filled in from the `app:` line and the client id:

```text
## Reviewing identity

- **Reviewing app**: <app name>
- **Client id**: <client id>
```

## Script

`scripts/review_token.py` has two subcommands and no others; `GH_TOKEN=$(python3 scripts/review_token.py token …) gh …` is how an ad-hoc call runs as the app.

- `token --client-id <id> <owner>/<repo>` prints an installation token scoped to that one repository on stdout, and nothing else. Tokens cache under `~/.cache/review-bot/<client id>/<owner>/<repo>.json` (`REVIEW_BOT_CACHE_DIR` overrides the root), directories mode 700 and files mode 600, written through a `.part` rename, and are reused while more than five minutes remain; `REVIEW_BOT_NO_CACHE=1` always mints. A cache that cannot be written is a warning on stderr, and the minted token is still printed.
- `whoami --client-id <id> <owner>/<repo>` prints `app: <name> (<slug>)`, `rest login: <slug>[bot]`, `graphql login: <login>` read with the minted token through the GraphQL viewer query, `installation: <id> on <owner>/<repo>`, `permissions: …`, and `review-token command: …`. A cached token the probe refuses is dropped, with a warning on stderr, and minted again once.

Both take `--key <path>` (or `REVIEW_BOT_KEY`) and `--api <url>` (or `REVIEW_BOT_API`, default `https://api.github.com`; GitHub Enterprise passes `https://<host>/api/v3`, from which the GraphQL endpoint `<host>/api/graphql` is derived). The script warns on stderr when the key is group- or world-readable.

Exit codes: `0` success; `1` the forge answered and refused (not installed, HTTP 401/403/404, a minted token failing the probe); `2` no answer or no local input (key missing or unreadable, `openssl` absent or refusing the key, network or TLS failure), naming the failing command on stderr. A TLS verification failure names `Install Certificates.command` and `SSL_CERT_FILE`. Consumers test only non-zero and capture stdout as the token; the token never appears in the `argv` of anything the script runs.

`python3 scripts/test_review_token.py` drives the script against a throwaway key and a local fake forge.
