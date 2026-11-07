---
name: sota-secrets-management
description: >-
  State-of-the-art secrets management for building and auditing software. Use
  whenever a task involves creating, storing, injecting, rotating, or scanning
  for credentials — or reviewing code/infrastructure for secret leaks and
  misuse. BUILD mode: implementing secrets handling; AUDIT mode: sweeping a
  repo for leaked, hardcoded, or mishandled secrets. Trigger keywords: secret,
  secrets management, credential, API key, token, password, private key,
  signing key, JWT secret, TLS key, SSH key, database password, connection
  string, .env, dotenv, environment variable, Vault, OpenBao, AWS Secrets
  Manager, GCP Secret Manager, Azure Key Vault, KMS, envelope encryption,
  SOPS, age, sealed-secrets, external-secrets, workload identity, OIDC
  federation, SPIFFE, SPIRE, IAM role, GitHub Actions OIDC, short-lived
  credential, rotation, revocation, key expiry, gitleaks, trufflehog, secret
  scanning, leaked key, hardcoded secret, committed secret, git history purge,
  honeytoken, pre-commit hook, kid rotation.
---

# SOTA Secrets Management

## Purpose

Eliminate static secrets where possible; where not possible, make every secret short-lived,
narrowly scoped, runtime-injected, auditable, and rotatable without downtime. This skill covers
the full lifecycle (generation → distribution → storage → use → rotation → revocation → expiry),
storage backends, application handling patterns, leak detection, incident remediation, and
per-credential-type rules. It serves two workflows: **BUILD** (write correct secrets handling
into new or existing code) and **AUDIT** (sweep a repo for secret issues and report findings).

The hierarchy of preference, always:

1. **No secret at all** — workload identity / OIDC federation / cloud IAM roles.
2. **Short-lived, auto-issued secret** — Vault dynamic creds, STS tokens, SPIRE SVIDs.
3. **Long-lived secret in a managed backend** — secret manager + rotation + audit log.
4. **Encrypted secret in the repo** — SOPS+age / sealed-secrets, GitOps only.
5. **Plaintext secret anywhere** — never acceptable.

When you write or review code, push the design as far up this hierarchy as the platform allows,
and document why if you stop below level 2.

## BUILD mode

Use when implementing anything that consumes or manages a credential.

1. **Classify the credential.** Type (DB cred, API key, signing key, TLS key, …) determines the
   rules — read [`rules/05-credential-types.md`](rules/05-credential-types.md) for the matching section before writing code.
2. **Try to eliminate it.** Cloud-to-cloud or CI-to-cloud calls should use workload identity
   (OIDC, IAM roles, SPIFFE) — see [`rules/01-lifecycle-and-workload-identity.md`](rules/01-lifecycle-and-workload-identity.md). Only fall back
   to a stored secret when no federation path exists (e.g., third-party SaaS API key).
3. **Pick the storage backend** per environment using the decision table in
   [`rules/02-storage-backends.md`](rules/02-storage-backends.md). Never invent a custom encrypted store.
4. **Wire injection at runtime** — file mount or env var populated by the platform, fetched via
   SDK with caching/TTL, never baked into images or code. Patterns and good/bad pairs in
   [`rules/03-application-patterns.md`](rules/03-application-patterns.md).
5. **Design rotation before shipping.** Every secret needs: an owner, a rotation procedure that
   works with zero downtime (dual-secret / kid overlap), an expiry or rotation interval, and a
   revocation path. If you cannot answer "how do we rotate this at 3am during an incident,"
   the design is not done.
6. **Add guardrails:** pre-commit scanning config, CI secret-scan gate, `.gitignore` entries for
   `.env*` and key files, log-scrubbing for the new secret's shape
   ([`rules/04-detection-and-remediation.md`](rules/04-detection-and-remediation.md)).
7. **Self-review against the Audit checklist** at the end of every rules file you used.

## AUDIT mode

**Coverage:** every `rules/` file's Audit checklist applies in AUDIT mode. Mark one *not applicable* only with its reason in the report — never skip a file because the thing it checks for is absent, since that absence may be the finding.

Use when asked to find secret leaks/misuse in an existing repo.

### Sweep procedure

1. **Tooling pass (absent? ask the operator to install it, router principle 6):** run `gitleaks git --redact .` and/or
   `trufflehog filesystem .` (and `git log` history scan when the repo has history). Treat tool
   output as candidates, not verdicts — verify each hit.
2. **Manual grep pass** for what tools miss. Sweep at minimum:
   - High-entropy strings and known prefixes: `AKIA`, `ASIA`, `ghp_`, `gho_`, `ghs_`, `ghu_`,
     `ghr_`, `github_pat_`, `xoxb-`, `xoxp-`, `sk-`, `sk_live_`, `rk_live_`, `AIza`, `ya29.`,
     `glpat-`, `npm_`, `dop_v1_`, `shpat_`, `eyJhbGciOi` (inline JWTs), `-----BEGIN ([A-Z0-9]+ )*PRIVATE KEY( BLOCK)?-----` (ERE; [rules/04](rules/04-detection-and-remediation.md) §6 has the tested command).
   - Assignment patterns: `(password|passwd|pwd|secret|token|api[_-]?key|auth)\s*[:=]\s*['"][^'"]{6,}`.
   - Connection strings with embedded creds: `://[^/:@\s]+:[^@\s]+@` (postgres, mysql, mongodb,
     amqp, redis URLs).
   - Files: `.env*` tracked in git, `*.pem`, `*.p12`, `*.pfx`, `*.key`, `*.jks`, `*.keystore`,
     `id_rsa*`, `credentials.json`, `serviceaccount*.json`, `kubeconfig`, `.npmrc`/`.pypirc`
     with tokens, `terraform.tfstate` (state files contain plaintext secrets).
3. **History pass:** `git log --all -m -p` / `gitleaks git --log-opts="--all -m"` for secrets removed
   from HEAD (without `-m`, merge commits show no diff: rules/04 §1)
   but live in history. A secret deleted in a later commit is **still leaked** — severity is
   unchanged.
4. **Handling pass (misuse, not just leaks):** secrets in log statements, error messages,
   exception payloads, crash/telemetry dumps, URLs/query strings, CLI args (visible in `ps`),
   Dockerfile `ENV`/`ARG`, docker-compose `environment:` literals, Kubernetes manifests with
   stringData/base64 secrets committed, CI YAML with inline values, debug endpoints dumping
   config, world-readable key files, missing rotation/expiry on long-lived tokens, overly broad
   token scopes.
5. **Verify and triage** each finding: is the value real (test-shaped? placeholder? entropy?),
   is it currently valid, what blast radius. Never call a credential live by invoking it against
   production without explicit permission; judge from context.

### Severity conventions

| Severity | Definition | Examples |
|---|---|---|
| **Critical** | Valid (or must-assume-valid) secret exposed to anyone with repo/log access | Live cloud key in code or git history; DB password in a public image; private signing key committed |
| **High** | Secret exposed in a narrower channel, or handling that will leak under normal operation | Secret logged at info level; cred in CLI args; `.env` with real values tracked in private repo; token in URL; tfstate with secrets in VCS |
| **Medium** | Weak lifecycle or weak protection of an otherwise contained secret | No rotation for years; long-lived token where OIDC is available; overly broad scope; secret in env var where platform supports file mounts; world-readable key file; weak generation (low entropy) |
| **Low** | Hygiene gaps with no current exposure | Missing pre-commit/CI scanning; `.env.example` containing realistic-looking values; no `.gitignore` for key files; missing audit logging on secret access |

Confirmed-fake placeholders (`changeme`, `xxx`, `<YOUR_KEY>`, obvious test fixtures) are not
findings, but note them as Low if they are realistic enough to mask real leaks in scans.

### Finding format

Report every finding as:

```
[SEVERITY] path/to/file.py:123 — RULE-ID short title
  Evidence: the offending line, with the secret value REDACTED (show prefix + length only)
  Why: one sentence of impact
  Fix: concrete remediation (rotate first, then remove; target pattern to adopt)
  Effort: trivial | small | medium | large
```

Order findings Critical → Low. End the audit with: counts per severity, whether git history is
affected (if so, remediation must include rotation + history purge per
[`rules/04-detection-and-remediation.md`](rules/04-detection-and-remediation.md)), and the top 3 systemic fixes. **Never reproduce a
discovered secret in full in your report** — redact to first 4 chars + length.

## Rules index

| File | Read this when... |
|---|---|
| [`rules/01-lifecycle-and-workload-identity.md`](rules/01-lifecycle-and-workload-identity.md) | Generating secrets (entropy/length), setting rotation/expiry/revocation policy, replacing static secrets with OIDC federation, SPIFFE/SPIRE, cloud IAM roles, GitHub Actions OIDC |
| [`rules/02-storage-backends.md`](rules/02-storage-backends.md) | Choosing where a secret lives: Vault/OpenBao, AWS/GCP/Azure secret managers, SOPS+age, sealed-secrets/external-secrets in Kubernetes, env vars vs file mounts (no cross-deployment shared mounts), in-memory handling and zeroization, consumer-key end-to-end encryption (§8) |
| [`rules/03-application-patterns.md`](rules/03-application-patterns.md) | Writing app code that consumes secrets: config layering, runtime injection, caching/TTL, keeping secrets out of code/VCS/logs/errors/URLs/argv/crash dumps, per-env separation, least-privilege scoping, access audit logging; **never-persist-raw (§2.1)** — text whose producer you do not control is stored as a digest plus a structural skeleton, because shape redaction is an enumeration |
| [`rules/04-detection-and-remediation.md`](rules/04-detection-and-remediation.md) | Setting up gitleaks/trufflehog, pre-commit hooks, CI gates; responding to a leak (rotate-first, purge history, assume compromised); honeytokens; running an AUDIT sweep; **agent session transcripts as a credential store (§7)** — inventorying and scoping the scan of `~/.claude/projects/**`, and why a tool that sweeps it is a secret-processing tool |
| [`rules/05-credential-types.md`](rules/05-credential-types.md) | Handling a specific credential class: DB creds, API keys, signing keys, TLS private keys, SSH keys, JWT secrets and kid rotation, data keys vs KMS envelope encryption, .env discipline |

## Top-10 non-negotiables

1. **A leaked secret is rotated first, scrubbed second.** History rewriting without rotation is
   theater — assume every secret that ever touched git, logs, or a ticket is compromised.
2. **No secrets in source code or VCS, ever** — including "temporarily," tests against real
   services, example files with live values, and committed `.env` files.
3. **Prefer no secret to a managed secret:** if OIDC federation / IAM roles / SPIFFE can replace
   a static credential (CI→cloud, service→cloud, pod→service), use it. Static keys for cloud
   access from CI are a defect, not a choice.
4. **Every secret has an expiry or rotation interval and a documented zero-downtime rotation
   procedure** (dual-secret overlap, JWT `kid`, DB dual users). Unrotatable = misdesigned.
5. **Generate secrets with a CSPRNG, ≥256 bits of entropy** for opaque tokens (≥32 random bytes
   before encoding); never derive from timestamps, UUIDv4-as-secret, or human-chosen strings.
6. **Secrets never appear in:** logs, error messages, exception payloads, crash dumps, URLs or
   query strings, CLI arguments, `ps` output, Dockerfile layers, image env, shell history, or
   telemetry. Scrub at the logger and wrap in redacting types.
7. **Inject at runtime, never at build time.** Images, artifacts, and bundles are
   secret-free; the platform (orchestrator, secret-manager SDK, CSI driver) supplies values
   when the process starts — file mounts preferred over env vars where supported.
8. **Least privilege and per-environment separation:** one credential per consumer per
   environment, scoped to the minimum actions/resources; dev/staging/prod never share secrets
   and prod values are unreadable from non-prod.
9. **Application data encryption uses KMS envelope encryption** (encrypt data with a data key,
   wrap the data key with a KMS key); never hardcode or hand-manage raw encryption keys.
10. **Scanning is mandatory and layered:** pre-commit (gitleaks/trufflehog) on every developer
    machine, a blocking CI gate, and periodic full-history scans. Detection without a leak
    runbook is incomplete — keep the rotate→revoke→purge→monitor runbook current.
