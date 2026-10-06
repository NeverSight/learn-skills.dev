---
name: quota-interpretation
description: "Rules and algorithms for quota interpretation, pace calculation, runway derivation, selection signals, and output tier rendering (TOON, JSON, TUI) in quota-axi."
user-invocable: false
---

# Quota Interpretation, Pace & Output Models

This document specifies the mathematics and presentation rules for quota interpretation, runway derivation, pace calculations, and output format tiering in quota-axi.

---

## Quota Availability & Bound Conflicts

Implemented in `src/interpretation.ts`:

- **Effective Availability**: Analyzes provider windows across all scopes (`all_models`, product scopes, model scopes).
- **Bound Conflict Detection**:
  - `availability()` accepts an optional own-windows argument.
  - When every window metered strictly for a scope reports remaining allowance, but an inherited account-wide window reports zero, quota-axi publishes `effectiveAvailability[].boundConflict` and reports the scope status as `unknown` rather than asserting `exhausted_now` or `effective 0`.
  - Used for Codex model windows (`additional_rate_limits`/`rateLimitsByLimitId`). Other providers keep their account bounds unless empirical proof of non-enforcement exists.

---

## Pace & Runway Calculations

Implemented in `src/pace.ts`:

- **Cycle-Average Pace**: Every projection assumes cycle-average consumption across the active window. There is no `projectionBasis` field anywhere in the API model.
- **Reserve Percentage Points (`reservePercentPoints`)**:
  - Quantifies how usage tracks against elapsed window time.
  - Positive values indicate usage is tracking behind the elapsed time clock (headroom remaining).
  - Negative values indicate usage is running ahead of the reset clock (burn rate higher than cycle average).
- **Effective Usable Runway**: Aggregates all authoritative bounds to determine time until exhaustion, preserving uncertainty if any binding window lacks timing metadata. Runway is dynamic and never cached.
- **Selection Signal (`effectiveAvailability[].selection`)**:
  - Computed purely from reported figures via `summarizeEffectiveSelection` in `src/pace.ts`.
  - Published field name is centralized in `SELECTION_SCALAR_KEY` in `src/types.ts`.
  - If any bounding window lacks usable pace data, the whole scope is deemed unmeasurable (no scalar published, `unmeasurableWindowIds` listed). A not-yet-triggered zero-use window (no `resetsAt` plus zero usage) is fully available and is excluded from the weighted mean instead of blocking; when every bounding window is untriggered the scope publishes no scalar and reports `unknown` with no `unmeasurableWindowIds`.
  - **Data only**: quota-axi never routes, recommends, or ranks winners.

---

## Output Formats & Tier Splitting

### 1. Default TOON Report (`src/render.ts`)

Structured into three concise decision blocks:

1. `quota[]`: One fully populated row per measurable scope.
2. `exhaustion[]`: Sparse block for finite-runway scopes, joined on `provider` + `scope`.
3. `attention[]`: Sparse block capturing every non-nominal condition (degraded sources, warnings, unmeasurable scopes, soft expiry).

**Core Invariants**:

- Every requested provider must appear in `quota[]` or `attention[]`, except providers with positive evidence of absence, which default TOON omits and counts in a single help line; `--full` and an explicit `--provider` name them.
- `quota[]` rows preserve provider declaration order and are **never metric-sorted**.
- `spendPriority` renders literal `unknown`, never `0`. An unknown or stale scope receives no `quota[]` row; any finite runway is preserved in `attention[]`.

### 2. JSON Tier Splitting (`--json` vs `--full`)

- `--json`: Normalized quota model with derivation inputs demoted to `--full`.
- `--full`: Includes account identities, diagnostic logs, and per-source attempts.
- **Demotion Rule**: Demote at renderer serialization time only (`quotaJsonReport` in `src/render.ts`). The in-memory model retains all fields so `--tui` and `--full` have full context.

### 3. Human Terminal Interface (`--tui`)

- Pure card renderer in `src/tui.ts`; interactive live loop in `src/tui-live.ts`.
- **Viewport Management**: `renderQuotaTui` is height-independent. `src/tui-viewport.ts` (`scrollFrame`) windows the output to fit terminal dimensions, clipping oversized lines and providing scroll affordances without terminal overflow.
- **Humanized Presentation**:
  - `through_reset` renders as `on pace ✓`.
  - Pace is visualized via bar fill and `┃` marker (no multiple chip or legend).
  - Projected exhaustion displays as relative countdown (`empty in Nd Nh`).
  - Headline bar uses the binding window's own label (`week`, `session`, `credits`).

### 4. CLI Fast Path

- Bare `-v`, `-V`, or `--version` routes through `axi-sdk-js/fast-path` and the leaf `src/version.ts`.
- Dynamically imports `src/cli.js` so provider dependencies and network graph never load on version checks.
