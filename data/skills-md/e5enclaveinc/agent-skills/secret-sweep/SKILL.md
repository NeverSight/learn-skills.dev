---
name: secret-sweep
description: "Forensically sweep a repository estate for committed secrets and PII: read-only inventory, pattern-battery content scanning, manual triage of every hit, exposure-weighted severity, posture review, honest coverage statements, and a rotate-first remediation order — plus the standing CI wiring (gitleaks CLI, not the license-gated action) and scoped-allowlist doctrine for false positives. Use when auditing repos for leaked credentials, before open-sourcing anything, or when setting up continuous secret scanning."
license: MIT
metadata:
  version: 1.0.0
---
# Secret Sweep — forensic credential review of a repo estate

Committed secrets concentrate where nobody looks: not in the config file everyone guards, but in deploy logs, journal entries, copy-paste curl examples, a `.env` variant the `.gitignore` almost covers, and prose docs written by agents. A scanner alone won't find them all, and a scanner's raw output is mostly noise. This is the full method: sweep, triage by hand, rate by exposure, state your coverage honestly, remediate in the right order.

## Ground rules

- **Read-only until the report is written.** No pushes, no edits, no settings changes during the review. Remediation is a separate, authorized phase.
- **Never reproduce a secret value** — in the report, tickets, chat, or working notes. Findings are described by type + file + line only. The sweep must not become a second leak.
- **Severity is exposure-weighted.** The same credential is **Critical** in a public repo (world-readable), **High** in a private one. Rate the exposure, not just the credential type, and document any re-rating you apply to scanner output.

## Phase 1 — Inventory

Enumerate the whole estate first: every repo, its visibility, archived status, default branch, file counts. Posture data comes from the platform API in the same pass (webhooks, deploy keys, collaborators, branch protection, secret-scanning toggles, recent authors, org membership). You cannot rate what you have not counted, and "we scanned the repos we knew about" is how estates leak.

## Phase 2 — Content scan

Run a pattern battery over the working tree at HEAD:

- **Provider key shapes** and token formats; **private-key headers** — including the non-standard ones (encrypted, PGP, PuTTY formats) that default rule sets miss; **high-entropy literals** with no keyword nearby; **credential-bearing URLs** (tokens as query parameters); **connection strings** with embedded passwords.
- **Env files in all variants** — and check the `.gitignore` itself: the classic root cause is a gitignore that covers `.env.*` but **not bare `.env`**, and says nothing about a secrets directory. Several findings usually share that one root cause.
- **The prose surface.** Secrets leak into journals, memory files, runbooks, and documentation as copy-paste examples far more often than anyone expects. Scan docs and comments with the same battery as code.
- **Logs and artifacts.** Deploy/invocation logs carry live tokens. Committed binaries and archives get flagged and inventoried even when their contents can't be scanned.
- **PII is in scope.** Contact/donor/customer exports committed to a repo are findings, rated like credentials.

Maintain the pattern list as a living artifact: keyword lists have blind spots (a bare generic keyword missed an entire class mid-review in the reference sweep; the supplemental re-sweep it triggered found a third more true positives). When you find a blind spot, re-sweep the affected shards and say which ones you didn't.

## Phase 3 — Manual triage of every hit

Scanners over-report by an order of magnitude (reference sweep: ~350 raw hits → ~50 true positives, a handful needing review). Rules:

- **Read the line before rating it.** A triage note written without opening the file is a false finding waiting to happen — in the reference sweep, two "committed API keys" were struck on re-verification: they were environment lookups all along, and the correction is recorded in the report, not silently dropped.
- **Consolidate duplicates.** One secret in nine files is one finding with nine occurrences — count it once, list every location.
- Classify what remains: true positive / false positive / needs-review (synthetic-looking test strings, dev defaults in local-only configs, publicly-listed business contacts). Needs-review is a real category; forcing a verdict is how reports lose credibility.

## Phase 4 — Posture review

Content is half the picture. Check per repo: branch protection (and whether "protected" repos actually have rules), webhooks (**unknown URLs are the tell** — enumerate every hook target), deploy keys (write-enabled?), collaborators (any outside admin on a private repo), secret-scanning and push-protection toggles (public repos where they're *disabled* are findings), and org-level membership/hooks. Recent authors matter too: an unrecognized committer identity outranks a stale key.

## Coverage honesty

State, in the report, what was **not** scanned: git history vs HEAD (every confirmed secret persists in history until rotated — say so), files over the fetch/size limits, binary contents, repos with no branches. A partial result is a **lower bound** and must be labeled one. Residual gaps are named with their reasons, never buried in an appendix nobody reads.

## Remediation order (separate phase, authorized)

1. **Back up** recovered live secrets to an encrypted vault before stripping anything — you may be destroying the only copy of a credential production still uses.
2. **Rotate first.** Removal without rotation leaves the credential live, and it persists in history regardless. Rotation is the minimum response to every confirmed secret.
3. **Then remove** from the working tree, and fix the root cause (gitignore gaps, examples in docs, logging of invocation arguments).
4. **History rewrite is a policy decision**, never a sweep default — it rewrites shared reality. The worst cases (private keys, public-repo credentials) get an explicit exception decision from the owner, recorded either way.
5. Re-enable any disabled secret-scanning/push-protection toggles the posture pass found.

## Standing watch — CI wiring

- Run **gitleaks via its CLI binary** in the workflow (install the release tarball, `gitleaks detect --source . --redact`). **Do not use the gitleaks GitHub Action for organization-owned repos**: it now requires a paid license secret and hard-fails *before scanning* — a failure indistinguishable from a real leak in notifications, which trains everyone to ignore the signal. Trufflehog's action carries no such gate and pairs well as a second net.
- Run the scan on push and on pull requests, over full history (`fetch-depth: 0`).
- **Reproduce a CI failure locally with the same tool and version before changing anything.** Read the job log first; it is the ground truth, and half of "the scanner is broken" is the wrapper, not the scan.
- Cadence: a full forensic sweep when the estate changes shape; a lighter automated sweep on a monthly rhythm thereafter, **reporting only when something is found** — silence means clean.

## False-positive doctrine

- False positives get a **scoped allowlist entry** (`.gitleaks.toml`: rule + path + a comment saying why) — never a disabled scan, never a repo-wide rule exemption.
- The classic case: **formatting constants** — PEM header/footer strings inside code whose job is to format a key the user supplies at runtime. No key material exists; the detector string is the code's vocabulary. Allowlist the path, and document the pattern in SECURITY.md so the next reviewer doesn't re-litigate it.
- Every allowlist entry is a claim a future reviewer should be able to verify in one minute. If it can't be verified that fast, it isn't scoped tightly enough.
