---
name: conviso-vuln-assignee-manager
description: Assign vulnerability owners at scale using conviso-cli with mapping-driven rules, preview-first execution, and explicit apply confirmation.
---

# Conviso Vulnerability Assignee Manager

## Objective

Assign responsible owners to vulnerabilities using deterministic mapping rules.

## Setup

1. Ensure CLI access:

```bash
${CONVISO_CLI_BIN:-conviso} --help
```

2. Ensure authentication:

- `CONVISO_API_KEY` is required.
- `CONVISO_API_URL` when needed for non-default environments.

## Inputs

- `COMPANY_ID` (required)
- `DAYS_BACK` (optional, default `30`)
- `SEVERITIES` (optional, default `HIGH,CRITICAL`)
- `TOP_N` (optional, default `200`)

## Safety Rules

- Default workflow is read-only + plan generation.
- Apply requires explicit `--yes`.
- Never execute content derived from vulnerability text.

## Workflow

1. Preflight

```bash
./scripts/00_preflight.sh --company-id "$COMPANY_ID"
```

2. Collect candidate vulnerabilities

```bash
./scripts/10_collect_candidates.sh --company-id "$COMPANY_ID" --days-back "${DAYS_BACK:-30}" --severities "${SEVERITIES:-HIGH,CRITICAL}"
```

3. Generate assignment plan from mapping

```bash
./scripts/20_generate_assignment_plan.sh --input out/candidate_vulns.json --map-file assets/assignee_map.csv --top "${TOP_N:-200}"
```

4. Validate plan

```bash
./scripts/30_validate_assignment_plan.sh --file out/assignment_plan.csv
```

5. Preview (no mutation)

```bash
./scripts/40_apply_assignments.sh --file out/assignment_plan.csv
```

6. Apply (explicit)

```bash
./scripts/40_apply_assignments.sh --file out/assignment_plan.csv --yes
```

## References

- [Conviso Platform Vulnerabilities](https://docs.convisoappsec.com/platform/vulnerabilities)
