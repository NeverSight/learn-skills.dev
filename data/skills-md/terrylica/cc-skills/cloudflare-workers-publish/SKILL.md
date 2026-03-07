---
name: cloudflare-workers-publish
description: Deploy static HTML files to Cloudflare Workers with 1Password credential management. TRIGGERS - Cloudflare Workers deploy, publish static site, wrangler deploy, static hosting, cloudflare publish, CF Workers, HTML hosting, workers.dev, static assets deploy
disable-model-invocation: true
allowed-tools: Read, Bash, Grep, Write, Edit, Glob, AskUserQuestion
---

# Cloudflare Workers Publish

Deploy static HTML files (Bokeh charts, dashboards, reports) to Cloudflare Workers with Static Assets, using 1Password for credential management.

**Scope**: Static-only deployments on workers.dev. No dynamic Workers, no R2 object storage.

**Prerequisite**: 1Password CLI (`brew install 1password-cli`) + Node.js (`npx wrangler`)

---

## When to Use This Skill

- Publishing HTML files to a public URL (too large for GitHub)
- Setting up a new Cloudflare Workers static site
- Troubleshooting a failed Cloudflare deploy
- Rotating Cloudflare API tokens in 1Password

**Do NOT use for**: Dynamic Workers (JavaScript/TypeScript logic), Cloudflare Pages (deprecated April 2025 - CFW-01), R2 object storage, or custom domains (advanced setup not covered).

---

## Architecture

```
Local project/
├── results/published/              # Deploy root (contains wrangler.toml)
│   ├── wrangler.toml               # Workers config (name + assets)
│   ├── index.html                  # Auto-generated directory listing
│   └── gen800/                     # Subdirectories with HTML files
│       └── XRPUSDT_750/
│           └── equity_plot.html    # 13MB Bokeh chart
└── scripts/
    └── publish_findings.sh         # Deploy script (3 phases)

Credential flow:

1Password (Claude Automation vault)
   ├── account_id (TEXT)      →  CLOUDFLARE_ACCOUNT_ID env var
   └── credential (CONCEALED) →  CLOUDFLARE_API_TOKEN env var
                                       ↓
                                 npx wrangler deploy
                                       ↓
                                 https://{name}.{slug}.workers.dev/
```

---

## TodoWrite Task Templates

### Template A - New Static Site (First-Time Setup)

```
1. [Preflight] Verify Node.js and 1Password CLI installed
2. [Preflight] Create Cloudflare API token (Workers Scripts Edit permission)
3. [Execute] Pre-provision 1Password item in Claude Automation vault (biometric)
4. [Execute] Store token + account ID in 1Password item fields
5. [Execute] Create publish directory with wrangler.toml (3 fields only)
6. [Execute] Create deploy script from skill template (parameterize 4 vars)
7. [Execute] Create mise task wrapper in .mise/tasks/publish.toml
8. [Execute] Add .wrangler/ to .gitignore
9. [Execute] Add LFS tracking for large HTML files in .gitattributes
10. [Verify] Enable workers.dev subdomain in Cloudflare dashboard
11. [Verify] Run first deploy and verify URL in browser (NOT curl)
12. [Verify] Document the workers.dev URL in project docs
```

### Template B - Add Files to Existing Published Site

```
1. [Preflight] Verify files are real content, not LFS pointers (head -1)
2. [Execute] Copy HTML files to published/{generation}/{symbol_threshold}/
3. [Execute] Run deploy script (index.html auto-regenerates)
4. [Verify] Verify new files appear at workers.dev URL in browser
```

### Template C - New Worker (New Subdomain/Project)

```
1. [Preflight] Choose worker name ({name}.{slug}.workers.dev)
2. [Execute] Create 1Password item OR reuse existing Cloudflare credentials
3. [Execute] Create wrangler.toml with chosen name and today's date
4. [Execute] Create parameterized deploy script from skill template
5. [Execute] Create mise task wrapper
6. [Verify] Deploy and discover actual workers.dev URL via wrangler output
```

### Template D - Rotate Cloudflare API Token

```
1. [Execute] Create new API token in Cloudflare dashboard (Workers Scripts Edit)
2. [Execute] Update 1Password item credential field (biometric required)
3. [Verify] Run deploy script to verify new token works
4. [Execute] Revoke old token in Cloudflare dashboard
```

### Template E - Troubleshoot Failed Deploy

```
1. Is wrangler.toml in current directory? (CFW-10)
2. Are credentials populated? Print first 8 chars of account ID
3. Is --reveal present for CONCEALED fields? (CFW-03)
4. Is workers.dev subdomain registered in CF dashboard? (CFW-07)
5. Does token have Workers Scripts Edit permission? (CFW-11)
6. Are HTML files real content or LFS pointers? head -1 file (CFW-12)
7. SSL handshake error? Verify in browser, not curl (CFW-08)
8. Is npx wrangler installed? npx wrangler --version
```

---

## Workflow: First-Time Setup

### Phase 1: Create Cloudflare API Token

1. Go to <https://dash.cloudflare.com/profile/api-tokens>
2. Click **Create Token** > **Custom token**
3. Set permissions: **Account** > **Workers Scripts** > **Edit** (CFW-11)
4. Account Resources: **Include** > your account
5. Copy the token (shown only once)

### Phase 2: Provision 1Password Credentials

**CRITICAL (CFW-02)**: 1Password service accounts can only READ items. They CANNOT CREATE new items. Create the item manually first.

See [1Password setup guide](./references/onep-credential-setup.md) for step-by-step instructions.

After provisioning, the item should have:

| Field        | Type      | `--reveal` | Content            |
| ------------ | --------- | ---------- | ------------------ |
| `account_id` | TEXT      | No         | Cloudflare acct ID |
| `credential` | CONCEALED | **YES**    | API token          |

### Phase 3: Create wrangler.toml

See [wrangler setup guide](./references/wrangler-setup.md).

```toml
# Minimal Workers Static Assets config (CFW-09)
name = "my-project-name"
compatibility_date = "2026-02-18"

[assets]
directory = "."
```

### Phase 4: Create Deploy Script

Copy the bundled template and edit the 4 config variables:

```bash
cp "$(skill-path)/scripts/publish_static.sh" scripts/publish_myproject.sh
# Edit: PUBLISH_DIR, OP_ITEM_ID, SITE_TITLE, PROJECT_URL
```

Or reference the working implementation: `rangebar-patterns/scripts/publish_findings.sh`

### Phase 5: Create mise Task

```toml
# .mise/tasks/publish.toml (CFW-13: bash in .sh file, not inline TOML)
["publish:site"]
description = "Deploy published files to Cloudflare Workers (static)"
run = "bash scripts/publish_myproject.sh"
```

Add to `.mise.toml` `[task_config] includes`:

```toml
[task_config]
includes = [
    ".mise/tasks/publish.toml",
]
```

### Phase 6: Git Hygiene

**.gitignore**:

```
# Wrangler temp files (Cloudflare Workers deploy)
.wrangler/
results/published/.wrangler/
```

**.gitattributes** (for large HTML files):

```
results/published/**/*.html filter=lfs diff=lfs merge=lfs -text
```

### Phase 7: Enable workers.dev Subdomain (CFW-07)

First-time Cloudflare accounts must enable the workers.dev route:

1. Go to <https://dash.cloudflare.com> > **Workers & Pages**
2. Enable workers.dev subdomain

**The subdomain is NOT predictable** (CFW-06). Discover yours after deploy:

```bash
npx wrangler whoami
```

### Phase 8: Deploy and Verify

```bash
mise run publish:site
```

**Verify in BROWSER, not curl** (CFW-08). macOS LibreSSL can fail TLS handshake with Cloudflare but browsers handle it fine.

---

## Anti-Patterns Summary

Full details with code examples: [references/anti-patterns.md](./references/anti-patterns.md)

| ID     | Severity | Gotcha                                   | Fix                                           |
| ------ | -------- | ---------------------------------------- | --------------------------------------------- |
| CFW-01 | HIGH     | Cloudflare Pages deprecated (April 2025) | Use Workers with Static Assets                |
| CFW-02 | HIGH     | 1P service account creating items        | Pre-provision via biometric/web UI            |
| CFW-03 | HIGH     | Missing `--reveal` for CONCEALED fields  | Always pass `--reveal` for API tokens         |
| CFW-04 | MEDIUM   | SC2155 `export VAR=$(cmd)`               | Split: `VAR=$(cmd)` then `export VAR`         |
| CFW-05 | LOW      | Bash 4+ `${var^^}` on macOS              | Use `tr '[:lower:]' '[:upper:]'`              |
| CFW-06 | MEDIUM   | Assuming workers.dev URL format          | Run `npx wrangler whoami` to discover slug    |
| CFW-07 | HIGH     | workers.dev subdomain not registered     | Enable in Cloudflare dashboard first          |
| CFW-08 | LOW      | curl SSL/TLS handshake failure on macOS  | Verify in browser instead                     |
| CFW-09 | MEDIUM   | Overcomplicating wrangler.toml           | Only `name`, `compatibility_date`, `[assets]` |
| CFW-10 | HIGH     | Running wrangler from wrong directory    | Always `cd` to directory with wrangler.toml   |
| CFW-11 | MEDIUM   | Excessive token permissions              | Workers Scripts Edit (Account) only           |
| CFW-12 | HIGH     | Deploying LFS pointers instead of files  | Run `git lfs pull` before deploy              |
| CFW-13 | MEDIUM   | Tera template conflict in mise TOML      | Complex bash in standalone `.sh` files        |
| CFW-14 | MEDIUM   | Pipe subshell data loss in while-read    | Use `< <(find ...)` process substitution      |
| CFW-15 | LOW      | No directory listing page                | Auto-generate index.html before each deploy   |

---

## Reference Implementation

The working production deployment lives in `rangebar-patterns`:

| File                              | Purpose                    |
| --------------------------------- | -------------------------- |
| `results/published/wrangler.toml` | Minimal Workers config     |
| `scripts/publish_findings.sh`     | 3-phase deploy script      |
| `.mise/tasks/publish.toml`        | mise task wrapper          |
| `.gitignore` (`.wrangler/`)       | Ignore wrangler temp files |
| `.gitattributes`                  | LFS tracking for HTML      |

**Live URL**: `https://rangebar-findings.terry-301.workers.dev/`

---

## Post-Change Checklist

After modifying this skill:

1. [ ] Anti-patterns table matches [references/anti-patterns.md](./references/anti-patterns.md)
2. [ ] All bash examples use `set -euo pipefail`
3. [ ] No hardcoded 1Password item IDs (parameterized)
4. [ ] No hardcoded workers.dev slugs (discovered at runtime)
5. [ ] Template script passes `bash -n` syntax check
6. [ ] All internal links use relative paths (`./references/...`)
7. [ ] Link validator passes
8. [ ] Skill validator passes
9. [ ] Append changes to [references/evolution-log.md](./references/evolution-log.md)

---

## Troubleshooting

| Issue                          | Cause                                 | Solution                                                      |
| ------------------------------ | ------------------------------------- | ------------------------------------------------------------- |
| `op item get` returns masked   | Missing `--reveal` flag (CFW-03)      | Add `--reveal` for CONCEALED fields                           |
| `op item create` fails         | Service account can't create (CFW-02) | Use biometric `op` or web UI to create item first             |
| wrangler: config not found     | Not in correct directory (CFW-10)     | `cd` to directory containing wrangler.toml before deploy      |
| SSL handshake failure          | macOS LibreSSL (CFW-08)               | Verify in browser; ignore curl errors                         |
| 403 on workers.dev URL         | Subdomain not enabled (CFW-07)        | Enable in Cloudflare dashboard > Workers & Pages              |
| Deploy succeeds, files missing | LFS pointers deployed (CFW-12)        | Run `git lfs pull` before deploy                              |
| `${var^^}` syntax error        | Bash 3 on macOS (CFW-05)              | Use `tr '[:lower:]' '[:upper:]'`                              |
| mise TOML parse error          | Tera template conflict (CFW-13)       | Move complex bash to standalone `.sh` file                    |
| Empty index.html               | No `gen*/*.html` files found          | Check file paths match `find . -path './gen*/*.html'` pattern |
| Token permission denied        | Wrong token scope (CFW-11)            | Recreate with Account > Workers Scripts > Edit permission     |
