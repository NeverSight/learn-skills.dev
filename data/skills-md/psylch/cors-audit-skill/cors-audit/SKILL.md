---
name: cors-audit
description: "This skill performs a comprehensive CORS (Cross-Origin Resource Sharing) audit on web projects. It should be used when diagnosing CORS errors, setting up CORS for new projects, reviewing CORS configuration after deployment issues, or validating that CORS is handled correctly across all layers (gateway, backend, frontend). Covers standard frontend-backend setups, micro-app architectures (Qiankun, single-spa), and multi-origin dynamic-origin scenarios."
---

# CORS Audit

Perform a systematic CORS configuration audit across all layers of a web project. Identify misconfigurations, redundant headers, and security issues before they cause production problems.

## Language

**Match user's language**: Respond in the same language the user uses.

## Bundled Resources

- `scripts/validate_cors.py` — Automated CORS validator (Python stdlib, no dependencies)
- `references/cors_checklist.md` — Detailed per-item audit checklist with pass/fail criteria
- `references/architecture_patterns.md` — CORS strategy for each architecture type with configuration examples
- `references/script_reference.md` — Full script subcommands, options, and usage examples

## When to Use

- CORS errors appear in browser console after deployment or configuration changes
- Setting up a new project with cross-origin API calls
- Reviewing existing CORS setup for correctness and security
- Migrating from direct API access to gateway-proxied architecture
- Embedding micro-apps (Qiankun, single-spa, Module Federation) into a host application

## Preflight

Before starting, run the preflight check:

```bash
python scripts/validate_cors.py preflight
```

**Check-Fix table:**

| Check | Fix |
|-------|-----|
| Python < 3.7 | Install Python 3.7+ (`brew install python3` / `apt install python3`) |
| Python not found | Install Python (`brew install python3` / `apt install python3` / `winget install Python.Python.3`) |

## Degradation Strategy

When live endpoints are unreachable (network failures, firewall, VPN required):

| Situation | Strategy |
|-----------|----------|
| Live endpoint unreachable | **Skip** Phases 3/5 live validation; rely on static config analysis only |
| Some endpoints reachable, some not | Validate reachable endpoints; report unreachable ones as "skipped — not reachable" |
| No network access at all | Run static-only audit (Phases 1, 2, 4 config review); note that live validation was skipped in the report |

Always inform the user which validations were skipped and why. Static config analysis alone can still catch the majority of CORS issues (duplicate headers, wildcard+credentials, missing OPTIONS handlers).

## How It Works

Print this checklist at the start and update it as each phase completes:

```
Progress:
- [ ] Phase 1: Architecture Discovery
- [ ] Phase 2: Config Collection & Static Validation
- [ ] Phase 3: Single-Layer Rule Verification
- [ ] Phase 4: Best Practices Validation
- [ ] Phase 5: Environment-Specific Validation
- [ ] Phase 6: Report Findings
```

### Phase 1: Architecture Discovery

Determine the project's architecture type before examining configuration:

1. **Identify all network layers** between browser and backend (reverse proxy, API gateway, backend framework, CDN/edge)
2. **Classify the architecture** — reference `references/architecture_patterns.md`:
   - Same-origin / Simple cross-origin / Gateway-proxied / Micro-app embedded / Multi-consumer API
3. **Map all request flows** — trace Origin header from browser to backend, noting proxy hops and credential requirements

### Phase 2: Config Collection & Static Validation

Collect CORS config from every layer. For each, document: where headers are set, `Allow-Origin` value, `Allow-Credentials` flag, OPTIONS handling.

| Layer | What to check |
|-------|---------------|
| Gateway/Proxy | Config file (Caddyfile, nginx.conf) — CORS headers, OPTIONS handling |
| Backend | CORS middleware config — origin lists, regex patterns, credential flags |
| Frontend | API base URL — same-origin, relative path, or cross-origin absolute URL? |
| Environment vars | Different CORS settings per environment (dev/staging/production)? |

Run static validation on each config file found:

```bash
python scripts/validate_cors.py validate --config path/to/Caddyfile
```

### Phase 3: Apply the Single-Layer Rule

**The #1 CORS best practice: CORS headers must be set by exactly ONE layer.** Duplicate headers are the most common CORS bug.

1. **Count CORS-setting layers** — flag if more than one
2. **Choose the authoritative layer** (gateway-proxied -> gateway; no gateway -> backend; CDN/edge -> edge)
3. **Verify non-authoritative layers are silent**
4. **If dual layers unavoidable**, strip upstream headers (Caddy: `header_down -Access-Control-Allow-Origin`; Nginx: `proxy_hide_header`)

**Verify on live endpoints** (most reliable — catches headers from any layer):

```bash
python scripts/validate_cors.py validate --url https://your-api.com/health --origin https://your-frontend.com
```

### Phase 4: Validate Against Best Practices

Reference `references/cors_checklist.md` for the full per-item checklist. Key areas:

- **Origin policy**: No `*` with credentials; prefer specific origins in production; dynamic reflection for multiple origins
- **Preflight**: OPTIONS returns 204 with all CORS headers; include `Max-Age`
- **Credentials**: `Allow-Credentials: true` requires specific origin (not `*`)
- **Headers/Methods**: `Allow-Headers` and `Allow-Methods` must cover all frontend usage

### Phase 5: Environment-Specific Validation

- **Dev**: Backend CORS enabled, frontend points to localhost, wildcards acceptable
- **Production**: Backend CORS disabled if gateway handles it, explicit origins only
- **Micro-app**: Origin = host domain; gateway must allow host domain; API URL must be absolute

Run live validation on production endpoints — see `references/script_reference.md` for batch and micro-app testing examples.

### Phase 6: Report Findings

Produce a summary table and classify issues:

- **Critical**: Duplicate CORS headers, `*` with credentials, missing CORS entirely
- **Warning**: Wildcards in production, missing `Max-Age`, overly broad `Allow-Headers`
- **Info**: Simplification and consistency suggestions

Generate a JSON report: see `references/script_reference.md` for output format options (`--format`, `--output`, `--limit`).

Exit codes reflect script execution status, not audit severity. Finding severity is in the JSON `summary` field.

## Common Pitfalls Quick Reference

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| "multiple values `*, https://x.com`" | Two layers both add Origin header | Apply single-layer rule (Phase 3) |
| "No Access-Control-Allow-Origin header" | CORS not configured for this origin | Add origin to allowlist |
| Preflight blocked by CORS | OPTIONS not handled | Add OPTIONS handler returning 204 |
| Request to `localhost` from production | Frontend API URL not set for prod | Set API base URL to gateway domain |
| 404 on API when embedded as micro-app | Relative path resolves to host domain | Use absolute URL to gateway |
| Works standalone, fails when embedded | Origin is host domain, not app domain | Allow host domain in CORS config |
| Server-to-server calls unaffected | CORS is browser-only | Investigate auth/network issues instead |
