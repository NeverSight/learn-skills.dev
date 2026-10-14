---
name: secret-scanner
description: "Static secret/token scanning for codebases and git repos: detects leaked credentials (AWS, GitHub, OpenAI, Anthropic, Stripe, Google, Slack, private keys, JWTs) using gitleaks v8.30.1 pattern table + Shannon entropy gating + allowlist noise filters. Stdlib-only Python script with JSON/Markdown/text reports, redaction, CI exit-code gate."
license: MIT
metadata:
  author: best
  version: "1.0.0"
  compatibility: "Requires Python 3 stdlib only. Optional: git for --git mode."
when_to_use: "Use when scanning code/git repos for leaked secrets: 'secret scanner', 'scan for tokens', 'find leaked keys', 'detect credentials', 'secret detection'. Example: 'scan my repo for leaked API keys' or 'check this directory for secrets before I push'."
---

# Secret Scanner — leaked credential detection

Load this skill when you need to **scan a codebase, directory, or git repo for
leaked secrets/tokens/keys** (before publishing a repo, before a release, or
during security review).

The scanner is **static and offline by design**: patterns come from the
[gitleaks v8.30.3 default config](https://github.com/gitleaks/gitleaks), the
canonical open-source secret-detection rule set, and detection uses the same
Shannon-entropy gating semantics as gitleaks. No network calls are made — a
format match is reported as **potential**, not verified.

---

## The scanner script

`scripts/secret_scanner.py` — pure Python 3 stdlib (no dependencies).

| Source | Command |
|---|---|
| File | `python3 secret_scanner.py --path path/to/file` |
| Directory (recursive) | `python3 secret_scanner.py --path path/to/dir` |
| Git repo (tracked files) | `secret_scanner.py --git /path/to/repo` |
| stdin (blob) | `cat file | secret_scanner.py` |

### Detected pattern families (19 rules)

Critical: AWS Access Key ID (`AKIA`/`ASIA`/`ABIA`/`A3T…`) & secret key,
GitHub PAT classic/fine-grained/refresh tokens, OpenAI (`sk-*T3BlbkFJ*`),
Anthropic (`sk-ant-api03-…AA`), Stripe (`sk_live_`/`rk_live_`),
Google API key (`AIza…`), private keys (PEM/OpenSSH/PGP blocks).
High: Slack app/bot/user tokens and webhooks, Perplexity (`pplx-…`).
Medium: JWT, generic keyword-anchored API keys.

### False-positive suppression (allowlists)

- **Placeholders**: `$VAR`, `${VAR}`, `{{ }}`, `%VAR%`, `true/false/null`,
  `****`, `EXAMPLE`, `xxxx`, `your-`, `placeholder`, `TODO` — never reported
- **Noise paths**: `node_modules/`, `vendor/`, `.git/`, lockfiles
  (`package-lock.json`, `go.sum`, `poetry.lock`, …), minified JS, binaries,
  images, fonts
- **Entropy gate**: every entropy-sensitive rule skips values whose Shannon
  entropy ≤ rule minimum (gitleaks semantics)

### Capabilities

- `--json` / `--markdown` / text (default) report formats
- `--redact N` — mask secrets in output (keeps first N chars; CI-safe)
- `--max-mb N` — skip huge files (default 10 MB)
- `--exit-code` — exit 1 when findings present (CI gate), else 0

---

## Usage example (typical)

```bash
# Full directory scan, JSON report for CI
python3 secret_scanner.py --path ./my-repo --json --redact 8 --exit-code

# Scann only tracked files of a repo
python3 secret_scanner.py --git /Users/me/projects/lovii_demo

# Markdown human-readable report
python3 secret_scanner.py --path ./app --markdown > scan-report.md
```

## Interpretation guidance

- **Critical + live risk** (AWS/GitHub/OpenAI/Anthropic/etc.) → rotate the
  credential **first**, then scrub history. Assume a committed secret is
  compromised (forks, cache, CI logs, bots).
- **Medium (generic/JWT)** → verify context before alarming; check whether the
  value appears in tests/fixtures/docs.
- **Allowlisted but suspicious** → check if `.env.example` contains a real key
  instead of a `YOUR_KEY` placeholder.
- Only the operator can confirm whether a secret is still live — offline
  heuristic check (token length/grammar, `EXAMPLE` suffix) is automatic.

## Canonical patterns

Full deep dive with upstream sources in `references/canonical-patterns.md`.
Key canons:

- **gitleaks rule table** (v8.30.3 `config/gitleaks.toml`) — the canonical regex
  set; entropy per-rule minimums
- **Shannon entropy gating** — `detect/utils.go#L117-L134`; skip when
  `entropy <= rule.Entropy` (strictly greater)
- **Global & path allowlists** — placeholders + lockfiles + binaries
- **SkillSpector two-stage model** — static → heuristic/human triage, baseline
  suppression for re-scans
- **Remediation order** — rotate first, scrub second (gitleaks/TruffleHog
  guidance; `git filter-repo`/BFG for history)

## Files

- `SKILL.md` — this file
- `skill.json` — manifest
- `scripts/secret_scanner.py` — the stdlib scanner (pattern table + entropy +
  allowlists)
- `references/canonical-patterns.md` — gitleaks/Detect-secrets/TruffleHog/
  SkillSpector deep dive with per-rule regexes and sources

## Canonical analogues

Full source depth — in `references/canonical-patterns.md`. Backbone:

<table>
<tr><th>Analog</th><th>What we borrow</th></tr>
<tr><td>gitleaks (GitHub, MIT)</td><td>Pattern table, entropy thresholds, global/path allowlists, redaction, exit-code CI model</td></tr>
<tr><td>TruffleHog v3</td><td>Typed-detector philosophy; `verified` vs `unverified` framing (we stay offline)</td></tr>
<tr><td>Yelp detect-secrets</td><td>Quoted-string scanning to cut noise; keyword-anchored entropy</td></tr>
<tr><td>NVIDIA SkillSpector</td><td>Two-stage analysis; severity scoring; false-positive baseline/suppression</td></tr>
</table>

## Installation

```bash
# For opencode
cp -r skills/secret-scanner ~/.config/opencode/skills/

# For other agents
# Copy the skill folder to your skills directory; requires Python 3.
```

---

> **Security note**: this tool finds *potential* secrets. It never comments
> them out, does not attempt to "verify" them online, and never rewrites
> source files. Operators must rotate real secrets and scrub history
> manually — see `references/canonical-patterns.md` → Remediation workflow.

## Boundaries

- Do not use as a complete dependency or architectural security review; use `security-review`.
