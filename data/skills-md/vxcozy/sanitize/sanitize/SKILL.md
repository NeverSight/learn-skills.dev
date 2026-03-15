---
name: sanitize
description: "Run a 12-point security audit on a git repo — checks for private keys, API tokens, .env files, config files with secrets, plaintext passwords, RPC URLs with embedded keys, wallet addresses, console.log leaks, .gitignore gaps, and test files with real credentials."
license: MIT
compatibility: Requires git
metadata:
  author: vxcozy
  version: "1.0"
allowed-tools: Bash(grep:*) Bash(git:*) Read Glob Grep
---

Run a comprehensive 12-point security sanitization audit on the current repository. This checks for secrets, credentials, and sensitive data that should never be committed.

## Checks

For each repository in the project, scan all tracked and staged files:

1. **Full file audit** — Run `git status` to list all modified/untracked files. Review what's about to be committed.
2. **Private keys / mnemonics** — Grep for 64-char hex strings (`0x` + 64 hex), `BEGIN PRIVATE KEY`, `mnemonic =`, `seed phrase`
3. **API keys / tokens / secrets** — Grep for `sk-*`, `AKIA*`, `ghp_*`, `glpat-*`, `xox[bpsa]-*`, Bearer tokens, `api_key=`, `api_secret=`
4. **`.env` files** — Check if any `.env*` files (except `.env.example`) are tracked by git with `git ls-files '*.env*'`
5. **`.mcp.json`** — Check if `.mcp.json` is tracked (often contains plaintext private keys)
6. **`config.json` / config files** — Check tracked `config.json`, `settings.json`, `credentials.*` files for secret-like values (private_key, secret, password, token)
7. **Plaintext passwords** — Grep for `password=`, `passwd=`, `pwd=` with literal (non-env-var) values
8. **RPC URLs with embedded keys** — Grep for Infura/Alchemy/QuickNode/Moralis URLs containing inline API keys
9. **Real wallet addresses** — Flag Ethereum addresses (`0x` + 40 hex) in non-test source files for manual review. Ignore dummy addresses (0x0000..., 0xaAaA..., 0xdead..., 0xbeef...)
10. **`console.log` leaking data** — Grep for console.log/debug/info statements referencing key/secret/token/password/mnemonic/credential
11. **`.gitignore` coverage** — Verify `.gitignore` includes: `.env`, `.env.local`, `.mcp.json`, `config.json`, `.claude/`, `node_modules`
12. **Test files with real credentials** — Scan `.test.*` / `.spec.*` files for production API keys or tokens (sk-*, AKIA*, ghp_*)

## Pre-commit hook

This skill includes a bash pre-commit hook (`scripts/pre-commit-sanitize`) that runs the same 12 checks automatically on every `git commit`. Install it with:

```bash
./scripts/install-hooks.sh /path/to/your/repo
```

## Output

Report each check as **PASS**, **WARN**, or **FAIL** with specific file:line references for any findings. Summarize at the end with total pass/warn/fail counts.

## Rules

- Dummy/test addresses (0xaAaA..., 0xdead..., 0x0000...) are OK — don't flag
- `.env.example` with placeholders is OK
- Variable names and type definitions mentioning "key" or "secret" are OK — only flag actual literal values
- Focus on `git diff` and staged content when possible, not entire file history
- If the repository has a pre-commit hook installed, note that and still run the full audit independently
