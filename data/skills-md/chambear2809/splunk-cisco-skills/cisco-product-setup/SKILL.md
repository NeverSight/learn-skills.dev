---
name: cisco-product-setup
description: "Use when the user asks to set up Splunk for a Cisco product such as ACI, Nexus 9000, Duo, Meraki,
  ThousandEyes, ASA, or FTD, including choosing the dedicated ASA syslog TA versus Cisco Security Cloud
  API or eStreamer collection. Resolve a Cisco product name from the SCAN catalog and route installation,
  configuration, and validation through the correct existing setup skill."
compatibility: "Splunk Cloud Platform 10.5.2605: delegated. Compatibility is determined by the canonical replacement or selected child skill; this compatibility alias or router does not own a runtime or package."
metadata:
  splunk_cloud_10_5: "delegated"
  compatibility_verified: "2026-08-20"
---

# Cisco Product Setup

## Prerequisites

| Tool or access | Purpose | Verify |
|---|---|---|
| Bash and Python 3 | Run bundled setup and validation helpers | `bash --version && python3 --version` |
| Required product/platform access | Inspect or configure the selected target | Complete the documented preflight |
| Credential files for live modes | Keep secrets out of chat | Verify paths only |

## Workflow Overview

```text
┌───────────┐   ┌───────────────┐   ┌───────────────┐   ┌─────────────────┐
│ Preflight │ → │ Render/review │ → │ Apply/handoff │ → │ Validate evidence │
└───────────┘   └───────────────┘   └───────────────┘   └─────────────────┘
```

## When to Activate

- Set up Splunk for a Cisco product such as ACI, Nexus 9000, Duo, Meraki, ThousandEyes, ASA, or FTD, including
  choosing the dedicated ASA syslog TA versus Cisco Security Cloud API or eStreamer collection.
- Preview and review the cisco product setup workflow before any live apply phase.
- Diagnose failed prerequisites, generated assets, configuration, or validation evidence.

## Scope

Follow the documented read-only or render-first path whenever it is available.
This skill does not imply permission to mutate live systems. Require explicit
apply flags, protected credentials, and operator review for state changes.

## Examples

Inspect the supported setup modes before selecting one:

```bash
bash skills/cisco-product-setup/scripts/setup.sh --help
```

Expected output: usage, supported modes, and required arguments are displayed
without changing the target environment.

Inspect validation modes before running completion checks:

```bash
bash skills/cisco-product-setup/scripts/validate.sh --help
```

Expected output: offline, live, and completion options are displayed when the
skill supports them; help exits without mutation.

## Troubleshooting

| Issue | Cause | Resolution |
|---|---|---|
| Preflight fails | A required tool or access path is missing | Resolve it before rendering or applying |
| Rendered assets are incomplete | Required non-secret inputs are absent | Complete intake and render again |
| Apply is blocked | Review, credentials, or explicit acceptance is missing | Use the documented handoff |
| Validation is incomplete | Live evidence is unavailable | Record the gap and keep completion open |

## Shared add-on completion gate

When the selected product resolves to a Splunk TA, add-on, or dashboard
companion, the delegated child must satisfy the
[shared completion gate](../shared/ta_completion_gate.md). Package delivery
alone is never successful product onboarding.

Provides one product-aware entrypoint for Cisco setup requests.

## What It Does

- Resolves a product name, alias, or keyword against the pinned normalized SCAN
  public-catalog fixture.
- Classifies the product as `automated`, `partial`, `manual_gap`,
  `no_plans_available`, `unsupported_legacy`, or `unsupported_roadmap`.
- For automated products, delegates to the existing family skill already in
  this repo.
- For partial products, returns a concrete collector or app-install handoff
  path without claiming full product automation.
- For CUCM, Expressway, Meeting Server, and Meeting Management, delegates only
  render/validate planning to `cisco-collaboration-setup`; all four remain
  `partial`. BroadWorks and RoomOS collaboration hardware retain
  `unsupported_roadmap` through a non-executable `gap_handoff` to the same
  evidence router.
- For ASA and FTD, treats the collection path as part of product identity:
  syslog or `Splunk_TA_cisco-asa` intent routes to `cisco-asa-ta-setup`, while
  API and eStreamer intent routes to `cisco-security-cloud-setup`. Bare ASA/FTD
  requests return both choices instead of selecting an owner silently.
- Uses the relevant family `template.example` file to show which non-secret
  values are required before configuration.

## Primary Commands

List products:

```bash
bash skills/cisco-product-setup/scripts/resolve_product.sh --list-products
```

Preview a product route:

```bash
bash skills/cisco-product-setup/scripts/setup.sh \
  --product "Cisco ACI" \
  --dry-run
```

Run the default workflow:

```bash
bash skills/cisco-product-setup/scripts/setup.sh \
  --product "Cisco ACI" \
  --set name ACI_PROD \
  --set hostname apic1.example.local,apic2.example.local \
  --set username splunk-api \
  --secret-file password /tmp/aci_password
```

## Agent Behavior

The agent must never ask for secrets in chat. Use the routed family skill's
secret-file pattern instead.

For non-secret intake, prefer the family `template.example` that the dry-run
output lists for the resolved product.

## Product Coverage

- Automated products use the existing Cisco family skills already in this repo.
- Partial products list the backed collector or handoff workflow and succeed
  in `--dry-run` previews, but do not perform live configuration through this
  router.
- Active products without a local route return `manual_gap`.
- Products with no verified local route return `no_plans_available`.
- Deprecated and retired products return `unsupported_legacy`.
- Roadmap products return `unsupported_roadmap`.

## Catalog Files

- `catalog_overrides.json` defines local routing overrides.
- `scan_source.json` records the public SCAN catalog timestamp, minimum app
  version, raw source SHA-256, and normalized fixture SHA-256.
- `scan_products.fixture.json` is the sanitized, package-free source fixture
  consumed by clean-clone builds.
- `scan_sourcetype_reconciliation.json` binds the current SCAN version to every
  reviewed sourcetype delta, the previous and current complete-set hashes, a
  snapshot of every unchanged product, canonical owner skills, and downstream
  evidence. This makes omitted product changes and incomplete per-product
  deltas fail closed.
- `catalog.json` is the generated runtime catalog.
- `scripts/build_catalog.py --check` verifies that `catalog.json` matches the
  pinned fixture and overrides, including both provenance checksums and the
  sourcetype reconciliation contract.
- `scripts/build_catalog.py --write` regenerates `catalog.json` after editing
  `catalog_overrides.json`.
- `scripts/build_catalog.py --refresh-source --write` fetches the public SCAN
  `products.conf` and refreshes the fixture and manifest. When the source
  version changes, catalog generation intentionally stops until
  `scan_sourcetype_reconciliation.json` and its downstream evidence are
  reviewed; rerun `--write` after that review.
- `scripts/build_catalog.py --check-live-source` is the networked drift check;
  it is scheduled separately from pull-request gating.
- `--scan-package PATH` produces one-off comparison output from a reviewed
  vendor package but cannot overwrite the pinned generated catalog.
  Without a mode flag the script prints the catalog to stdout.

## Completion Validation

The router's validation phase, including `--validate-only`, invokes actionable
Cisco child validators with `--completion`. Consequently the full router does
not report onboarding complete when account/input, event-flow, or shipped
dashboard evidence is missing. Run a child `validate.sh` without that flag when
only a warning-oriented diagnostic inventory is desired.
