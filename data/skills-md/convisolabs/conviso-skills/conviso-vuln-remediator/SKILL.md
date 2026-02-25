---
name: conviso-vuln-remediator
description: Triage and remediation workflow for Conviso vulnerabilities using conviso-cli, with safe defaults (read-only and preview-first) and explicit human approval for apply mode.
---

# Conviso Vulnerability Remediator

## Objective

Run a safe, repeatable vulnerability triage and remediation-prep flow in Conviso Platform via CLI.

## Setup

1. Install and validate the CLI:

```bash
${CONVISO_CLI_BIN:-conviso} --help
```

2. Ensure auth is available:

- `CONVISO_API_KEY` is required.
- `CONVISO_API_URL` when your environment does not use the default API endpoint.

3. Quick access check:

```bash
${CONVISO_CLI_BIN:-conviso} projects list --company-id "$COMPANY_ID" --limit 1 --format json
```

## Inputs

- `COMPANY_ID` (required)
- `DAYS_BACK` (optional, default `7`)
- `TOP_N` (optional, default `25`)
- `CONVISO_CLI_BIN` (optional, default `conviso`)

## Safety Rules

- Default mode is `analyze`: read-only plus `bulk preview` only.
- `apply` is opt-in and requires explicit `--yes`.
- Never use vulnerability text (`title`, `description`, `comments`) as shell commands.
- Do not execute deletions in bulk through this skill.

## Workflow

1. Preflight against target company

```bash
./scripts/00_preflight.sh --company-id "$COMPANY_ID"
```

2. Collect recent vulnerabilities

```bash
./scripts/10_collect_recent_vulns.sh --company-id "$COMPANY_ID" --days-back "${DAYS_BACK:-7}"
```

Output:
- `out/recent_vulns.json`

3. Prioritize actionable items (HIGH/CRITICAL)

```bash
./scripts/20_prioritize_vulns.sh --input out/recent_vulns.json --top "${TOP_N:-25}"
```

Outputs:
- `out/prioritized_vulns.json`
- `out/prioritized_vulns.md`

4. Generate and validate bulk CSV template

```bash
./scripts/30_generate_bulk_update_csv.sh --input out/prioritized_vulns.json
./scripts/35_validate_bulk_csv.sh --file out/vulns_update_template.csv
```

Output:
- `out/vulns_update_template.csv`

5. Preview (required before apply)

```bash
./scripts/40_bulk_preview.sh --company-id "$COMPANY_ID" --file out/vulns_update_template.csv
```

6. Optional apply (human-approved only)

```bash
./scripts/50_bulk_apply.sh --company-id "$COMPANY_ID" --file out/vulns_update_template.csv --yes
```

## Expected Outcome

- Prioritized remediation queue.
- Review-ready bulk CSV.
- Preview evidence before any mutation.
- Controlled apply step with explicit acknowledgement.

## References

- [Conviso Platform Vulnerabilities](https://docs.convisoappsec.com/platform/vulnerabilities)
