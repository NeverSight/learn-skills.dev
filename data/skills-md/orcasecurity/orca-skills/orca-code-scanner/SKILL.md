---
name: "orca-code-scanner"
description: "Scan the code you just changed with the Orca CLI (secrets, vulnerable or malicious dependencies, IaC, Dockerfiles, images, SAST), then triage and fix real findings. Run once as the closing step of a coding task, or when asked to scan changes. Not for live cloud posture. Also use when asked \"is this secure\" or to scan an image before pushing, or when secrets, CVEs, malicious packages, IaC misconfig, or licenses come up while coding. Not for non-security code review or Orca platform/CLI troubleshooting. Runs without being asked; skip only if the developer says not to scan."
allowed-tools:
  - Bash(orca-cli *)
  - Bash(printenv ORCA_SECURITY_PROJECT_KEY)
  - Bash(git status)
  - Bash(git status *)
  - Bash(git diff)
  - Bash(git diff *)
  - Read
  - Grep
  - Glob
---

# Orca Code Scanner

When you finish a coding task, scan what you changed with the Orca CLI, triage,
and fix the real issues before it ships — secrets, dependencies (SCA: vulns,
license, malicious), IaC, container images, and SAST. You run `orca-cli`
yourself (no wrapper); it works the same on macOS, Linux, and Windows.

Scope is what the task **produces**: source, manifests/lockfiles, IaC,
Dockerfiles, and the images you build. Scanning **live cloud posture** (a
deployed account or running environment) is a separate Orca workflow — out of
scope here.

## Setup

Needs the **Orca CLI, authenticated** (part of Orca Shift Left). Don't check
anything up front: run the first scan and react to how it fails.

**Running on your own** (closing step, nobody asked for a scan) — never install
or log in:
- `orca-cli` not found: say once per session "Orca code scan skipped: orca-cli
  not installed (https://docs.orcasecurity.io/docs/orca-cli-installation)" and
  stop. Don't offer an install.
- `not authenticated`: say "Orca code scan skipped: not logged in — run
  `orca-cli auth login`" and stop. Don't start the login yourself.

**Asked to scan** (the developer requested it):
- `orca-cli` not found: offer to install; with approval run
  `curl -sfL https://raw.githubusercontent.com/orcasecurity/orca-cli/main/install.sh | sh -s -- -b "$HOME/.local/bin"`
  (Windows PowerShell: `New-Item -ItemType Directory -Force "$HOME\.local\bin" | Out-Null; iwr https://github.com/orcasecurity/orca-cli/raw/main/install.ps1 -OutFile $env:TEMP\install.ps1; & $env:TEMP\install.ps1 -binDir "$HOME\.local\bin"`
  — if it fails, follow https://docs.orcasecurity.io/docs/orca-cli-installation#for-windows-machines).
  If `orca-cli` is still not found, tell the developer to add `~/.local/bin` to
  PATH — don't call it by full path. If they decline, say so and stop.
- `not authenticated`: run `orca-cli auth login` (opens a browser). If the
  browser cannot open from your shell, give the developer the exact command to
  run in another terminal and wait for them.

Never read or print `ORCA_SECURITY_API_TOKEN`; if it is set, the CLI uses it on
its own (the better option in CI and sandboxed agents such as Codex).

**Network:** every scan needs Orca Cloud. In a sandbox with network off (Codex's
default), request network approval before the first scan. A network or sandbox
error is not an auth failure — don't run login for it; say the scan couldn't
reach Orca.

**Sandboxed agents (Codex):** scans also write outside the workspace — the CLI's
saved login (macOS: `~/Library/Application Support/orca`) and the SAST engine's
log (`~/.opengrep`). If a scan fails with `operation not permitted` on one of
these, stop and don't retry (a blocked login refresh can log the developer out
of `orca-cli`). Tell the developer to add this to `~/.codex/config.toml` once,
with full paths (use the folders the error names), then restart Codex:

```toml
[sandbox_workspace_write]
network_access = true
writable_roots = ["/Users/<you>/Library/Application Support/orca", "/Users/<you>/.opengrep"]
```

Pass the project whose **policy** applies as `-p <key>` — use the value of
`printenv ORCA_SECURITY_PROJECT_KEY` (run it alone, not chained with other
commands, so it stays pre-approved), else `-p default`. Each scan type needs its policy
attached; if one isn't, `orca-cli` errors for it — run the rest and note what you
couldn't.

## What to scan

Only what you changed **this task** (from `git status`/`git diff` plus your own
record), current content — not the whole repo or git history, and not after every
edit. Run once as the closing step (or on request). Choose scans by what each
changed file *is*, reasoning about its role rather than matching a fixed
extension list.

## Scans

Write each scan as one plain command with `-p <key>` typed literally. No shell
variables, loops, or functions (zsh does not word-split `$P`, which breaks the
project key). Never pipe scan output through `tail`, `head`, or `grep`; read all
of it. Always pass `--timeout 180s --skip-scan-log` (shown below): without the
timeout the CLI hangs at "policy decision" if the Orca backend never answers;
`--skip-scan-log` keeps these local scans out of the tenant's scan logs (you
still get every finding and the policy result). On a timeout, report that scan
as "did not complete" and continue with the rest.

- **Secrets** — every changed file, including IaC, Dockerfiles, and manifests,
  not just source. `--path` takes ONE path, not a comma list. One changed file:
  `orca-cli -p <key> --timeout 180s --skip-scan-log secrets scan --path <file> --disable-git-scan`.
  More than one: run that once with `--path .` instead, and report only findings
  in files you changed.
- **SCA** — a manifest/lockfile changed; scan the project dir (works from the
  manifest/lockfile, no install): `orca-cli -p <key> --timeout 180s --skip-scan-log sca scan --path <dir>`.
  Covers vulns+license+malicious by default. It reads the *resolved lockfile*, so
  if a dependency changed, update the lockfile first (npm/pnpm/poetry/… — detect
  it), else note the result may be partial. If license/malicious aren't in the
  policy, retry with `--security-checks vulns` and say what you skipped.
- **IaC** — Terraform/CloudFormation/K8s/Helm/Dockerfile changed:
  `orca-cli -p <key> --timeout 180s --skip-scan-log iac scan --path a.tf,b.yaml` (`--path` is comma-separated).
- **Container images** — you built or changed an image:
  `orca-cli -p <key> --timeout 180s --skip-scan-log image scan <ref>` (or `<file>.tar --tar-archive`). Catches
  OS/app CVEs + secrets in the built layers, complementing the Dockerfile IaC
  scan. The image must be built or pullable; if not, say so.
- **SAST** — first-party source changed:
  `orca-cli -p <key> --timeout 180s --skip-scan-log sast scan --path a.py,b.ts` (comma-separated).

## Triage and fix

Detection is pattern-based, so read the output directly and **triage before
fixing**. Read every finding before deciding; never report one you have not read.

- Fix the real CRITICAL/HIGH/MEDIUM you safely can — pin a vulnerable dep, move a
  secret to an env var / secrets manager and change the code to read it from
  there (if the value is unused you may delete the line, but say so and tell the
  developer to rotate it), tighten an over-permissive IaC setting; explain each
  fix. A **malicious or typosquat** package is removed and replaced
  with the legitimate one (name it), never "patched".
- A **hard-coded secret** always moves out of the code, whatever its priority.
  Orca may rate it INFO when the value tests invalid; that only lowers how
  urgently it needs rotating, not whether it stays in the code.
- Likely **false positives**: don't force a fix — list them with your reasoning
  and let the developer decide.
- **Never** suppress, ignore, weaken, or downgrade a finding just to pass —
  accepting a risk is the developer's call, not yours.
- Rescan once to confirm (at most one more pass, don't loop). Close with a short
  summary: which scans ran, which you skipped and why, what you fixed, what's
  open. All clean? Say so in a line. This skill is **advisory** — it never blocks
  committing or pushing.
