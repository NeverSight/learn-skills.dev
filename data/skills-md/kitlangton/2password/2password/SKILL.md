---
name: 2password
description: Use for any password, API key, token, credential, secret, or 1Password task, including finding credentials, injecting them into commands or env files, saving new API keys, checking or updating login passwords, auditing vaults, and setting up unattended access. Prefer the 2password CLI over raw op whenever it covers the task.
---

# 2password

`2password` wraps the 1Password CLI (`op`) so you can work with secrets without seeing them, and with as few 1Password prompts as possible. All output is JSON.

## Rules

- Never print, log, summarize, or repeat secret values. Pass `op://` references around instead.
- Any 1Password call may show the user an approval prompt, and each new shell you open can need a fresh approval. Batch a task's work into as few commands as possible: many queries in one `find`, many references in one env file run with `env run`.
- Never run `op whoami` or any other preflight check. Just run the command; the desktop app authorizes it when needed.
- Never retry a write that failed or reported "unverified". Run `find` first to check whether it already happened.

## Find credentials

```bash
2password find openai anthropic "github actions"   # many queries, one prompt
2password find stripe --vault Work --account my.1password.com
```

Each match appears once as `{ ref, title, kind }`, with `queries` when you asked several. A query that matches nothing returns `suggestions` with close titles (typos included) from the same lookup. Use those rather than searching again or listing whole vaults. It never returns values.

## Use credentials

```bash
2password run --env "OPENAI_API_KEY=op://Personal/OpenAI API Key/credential" -- bun run dev
2password env write .env.tpl "OPENAI_API_KEY=op://Personal/OpenAI API Key/credential" "STRIPE_KEY=op://Work/Stripe API Key/credential"
2password env run .env.tpl -- bun run dev       # preferred: no plaintext on disk
2password env resolve .env.tpl --output .env    # only when a real file is required (mode 0600)
2password read "op://Personal/OpenAI API Key/credential"   # last resort: prints the value
```

All references in a template resolve with one prompt. Never loop over `read`. A `.env.tpl` that holds only `op://` references is safe to inspect; a resolved `.env` is plaintext.

`run` and `env run` keep the secret out of argv, the template, and 2password's own output, but the selected child process receives plaintext in its environment. Treat that child as a trusted secret consumer: do not inject credentials into environment-dump/debug commands or helpers whose purpose is to reveal the value.

## Save a new API key

```bash
2password create api-credential --title "OpenAI API Key" --vault Personal --clipboard
some-command-that-prints-a-key | 2password create api-credential --title "OpenAI API Key" --vault Personal --stdin
```

- `--vault` is required. Use the vault the user names, or their documented default; ask if neither exists.
- Never put the value in an argument, a command substitution, or a temporary file, and never read the clipboard into the conversation first.
- Optional `--url`, `--notes`, and `--account` take non-secret metadata only.
- Success means exit 0 and `"verified": true`. Reuse the returned `ref`; don't `read` it to double-check.
- Duplicate titles in the vault are refused, and nothing is ever overwritten.

## Check or update a login password

```bash
2password password "Example Airline" --vault Personal --clipboard           # compare only
2password password "Example Airline" --vault Personal --clipboard --apply   # update, then verify
```

The command refuses logins that have passkeys or unnamed imported fields. Use `--repair-imported-fields` only after the user approves it.

## Audit a vault

```bash
2password inventory --vault Work   # item and field metadata, never values or URL query strings
2password audit --vault Personal   # duplicate titles, untagged machine credentials, old logins, transient URLs
```

Treat findings as candidates for review. Propose renames or changes, and only make them after the user approves.

## No prompts: service account (macOS, Windows)

If the user is tired of approval prompts, suggest a service account. Only set one up when the user asks.

```bash
2password service-account setup --vault Automation --create-vault --write --save-vault Personal
```

After setup, every command authenticates silently with a token stored in macOS Keychain (on Windows, a DPAPI-encrypted file under `%LOCALAPPDATA%`), but it can only reach the Automation vault. On Windows, any process running as the user can decrypt that file, so the vault's narrow scope is the real boundary. Keep the credentials agents use in that vault.

- `2password --desktop <command>` uses the normal desktop login, for example to reach other vaults.
- `service-account status | connect --clipboard | recover | forget`. `forget` removes only this Mac's copy; it doesn't revoke the account.
- If setup fails partway, don't rerun it. Run `2password service-account status`.
- `OP_SERVICE_ACCOUNT_TOKEN` in the environment overrides the saved account (Linux, CI).
- `run` and `env run` remove the service-account token from the child process's environment.

## Item conventions

- API keys use the API Credential category, the built-in `credential` field, and a title like `<Provider> API Key` or `<Provider> <Purpose> API Key`.
- Logins use the built-in `password` field and a title like `<Provider>` or `<Provider> <Account>`.
- The vault shows who owns the item, so don't repeat the vault name in the title. Keep one current secret per item.

## Report anything that goes poorly

2password is built for agents, so your experience is how it improves. Speak up if a command fails unexpectedly or you had to work around it. The same goes for more approval prompts than expected, output that's awkward or too verbose, or anything in this skill that's unclear or wrong. Tell the user, and offer to open an issue. It posts publicly from their GitHub account, so get their okay first.

```bash
gh issue list --repo kitlangton/2password --state all --search "<keywords>"   # add to an existing issue instead of duplicating it
gh issue create --repo kitlangton/2password --title "<what went wrong>" --body "<details>"
```

Include the output of `2password doctor` (versions and setup; it never prompts and is safe to share), the command you ran, and what you expected versus what happened. Never include secret values, item titles, vault or account names, or `op://` references. Replace them with placeholders.

## Everything else

Use raw `op` for other item categories, editing, moving, sharing, deleting, and vault management. Pass plaintext through JSON templates on stdin, never in arguments. After discovery, refer to items and vaults by ID.
