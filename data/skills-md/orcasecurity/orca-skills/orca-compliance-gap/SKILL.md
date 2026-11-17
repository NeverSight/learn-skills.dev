---
name: orca-compliance-gap
description: Deep-dive compliance gap analysis for any framework — failing controls ranked by impact, quick wins, account breakdown, and remediation plan. Use when user asks about compliance gaps, failures, or status (e.g., "compliance gaps", "PCI DSS status", "where are we failing", "SOC 2 compliance", "quick wins").
trigger: When user asks about compliance gaps, framework scores, failing controls, compliance posture, "how's our PCI compliance", "what's failing in SOC 2", "compliance gap analysis", "show me compliance issues", or framework-specific questions (e.g., "CIS benchmark gaps", "NIST failures")
---

# Orca Compliance Gap Skill

Answers the question: **"Where are we failing, what's the fastest path to improve, and who owns the worst gaps?"**

Given a compliance framework (or all frameworks), analyzes failing controls ranked by blast radius, identifies quick wins (single-fix controls), breaks down gaps by account/business unit, and generates a prioritized remediation plan.

## Usage

```
/orca-compliance-gap
/orca-compliance-gap PCI DSS
/orca-compliance-gap CIS AWS
/orca-compliance-gap SOC 2
```

Or natural language:
- "how's our PCI compliance?"
- "what's failing in CIS AWS?"
- "compliance gap analysis"
- "show me our worst compliance gaps"
- "which framework needs the most work?"
- "quick wins for SOC 2"

## Processing Logic

### Step 1: Determine Scope

Parse user input to determine:
- **Specific framework**: "PCI DSS" → filter to that framework
- **All frameworks**: no argument → show overview of all, then drill into worst
- **Account-specific**: "compliance in account 123456789012" → filter by account

### Step 2: Gather Data (run ALL in parallel)

**Query 1: All enabled frameworks with current scores**
```
get_enabled_compliance_frameworks:
  (no filters)
```

**Query 2: Compliance trend over time**
```
get_compliance_trend_over_time:
  filters:
    datetime_filter: 30
```

**Query 3: Compliance by account**
```
get_compliance_analysis_by_account_or_business_unit:
  group_by: "accounts"
```

**Query 4: Compliance by business unit**
```
get_compliance_analysis_by_account_or_business_unit:
  group_by: "business_units"
```

### Step 3: Deep-Dive into Target Framework(s)

For the target framework (or the worst-scoring one if user said "all"), run Queries 5-8 in parallel. Query 6 depends on Query 5 (it needs the `rule_id`s), so run it after Query 5 returns.

**Query 5: Failing control tests**
```
get_compliance_framework_control_tests:
  framework_id: <id>
  filters:
    status: "fail"
```

**Query 6: Compliant + non-compliant assets per failing control** (runs after Query 5)
Scope to the top N failing controls (default N=5) to keep response sizes manageable. The `rule_id` comes from Query 5's `tests[].rule_id`.
```
get_control_test_assets:
  framework_id: <id>
  rule_id: <tests[].rule_id from Query 5>   # one call per top-N failing control
```
Returns `{ non_compliant_assets: [...], compliant_assets: [...] }` — both arrays, so true pass/fail ratios are computable per control, not just a failure count.

**Query 7: Framework stats**
```
get_compliance_framework_stats_for_asset:
  framework_id: <id>
```

**Query 8: Assets with most failures**
```
get_framework_assets_with_failed_controls_count:
  framework_id: <id>
```

**Query 9: Per-framework account breakdown**
```
get_compliance_analysis_by_account_or_business_unit:
  group_by: "accounts"
  framework_ids: ["<framework_id>"]
```

### Step 4: Analyze and Rank

#### Quick Win Detection

A "quick win" is a failing control where:
- Few assets are affected — use the actual `non_compliant_assets.length` from Query 6 (`get_control_test_assets`), not a guess (treat < 5 as low)
- The fix is a single configuration change (not architectural)
- Fixing it passes the control completely (no partial pass)
- The control appears in multiple frameworks (high ROI)

#### Impact Ranking

Rank failing controls by:
1. **Cross-framework impact** — for the top failing assets returned by Query 6 (`get_control_test_assets`), call `get_related_compliance_frameworks_for_asset` with the asset's `group_unique_id` as `asset_unique_id`. A control/asset participating in more frameworks gets priority.
   - **HARD RULE: before counting frameworks per asset, filter `result[]` to entries where `active === true`.** The `result` array includes frameworks with `active: false` (frameworks that could apply to this asset type but aren't enabled in the tenant). Counting them inflates cross-framework impact with frameworks the customer hasn't enabled.
2. **Asset count** — controls failing on many assets = systematic issue
3. **Severity** — critical/high controls before medium/low
4. **Fix complexity** — simple config changes before architectural changes

#### Account Responsibility

Map failing controls to accounts to identify:
- Which account drags the score down most
- Which account has the most unique failures
- Cross-account patterns (same control failing everywhere)

### Step 5: Generate Remediation Plan

Build a prioritized remediation plan:

**Phase 1: Quick Wins (days)**
- Single-config fixes affecting multiple frameworks
- Expected score improvement per fix

**Phase 2: Systematic Fixes (weeks)**
- Controls failing across many assets (same root cause)
- Requires policy change or automation

**Phase 3: Architectural Changes (months)**
- Deep structural gaps requiring design changes
- Network segmentation, encryption-at-rest, etc.

## Proactive Remediation Behavior

**CRITICAL: Never leave the user with just data. After EVERY output layer, suggest the next action and offer to generate remediation code.**

After the dashboard and after every drill-down section:
1. **Suggest what to do next** — identify the highest-ROI fix and recommend it
2. **Offer remediation format selection** — always ask: "I can generate the fix. What format do you prefer?"
3. **Supported formats**: Terraform, CloudFormation, Ansible, CLI commands (aws/az/gcloud), step-by-step instructions, Pulumi, ARM/Bicep
4. **Auto-suggest quick wins** — proactively say "The quickest score improvement is fixing X. Want me to generate the code?"

When the user selects a format:
- Generate the remediation code for the selected control(s) immediately
- Write it to a file: `compliance-fix-<control-id>.<ext>` (e.g., `.tf`, `.yml`, `.sh`)
- Include verification commands
- Show projected score improvement after applying
- Suggest the next control to fix

**Format mapping:**
| User says | Extension | Template |
|-----------|-----------|----------|
| Terraform | `.tf` | HCL with provider + resource blocks |
| CloudFormation | `.cfn.yaml` | YAML template with Parameters/Resources |
| Ansible | `.yml` | Playbook with tasks |
| CLI | `.sh` | Shell script with cloud CLI commands |
| Instructions | inline | Numbered step-by-step console walkthrough |
| Pulumi | `.ts` | TypeScript Pulumi program |
| ARM/Bicep | `.bicep` | Bicep template |

## Output Format

### Layer 1: Dashboard

```
═══════════════════════════════════════════════════════════════════
COMPLIANCE GAP ANALYSIS — <framework or "All Frameworks">
<date> | <account scope>
═══════════════════════════════════════════════════════════════════

POSTURE: <overall assessment — 1 line>

┌─────────────────────────────────────────────────────────────────┐
│  FRAMEWORKS     <N> enabled                                     │
│  AVG SCORE      <X>%                                            │
│  WORST          <framework> at <X>%                             │
│  BEST           <framework> at <X>%                             │
│  TREND (30d)    <improving / stable / degrading>                │
│  QUICK WINS     <N> controls fixable with single changes        │
│  WORST ACCOUNT  <account> — <X>% avg score                     │
└─────────────────────────────────────────────────────────────────┘

FRAMEWORK SCORES:
  Framework                    Score    Trend    Status
  ─────────────────────────────────────────────────────────
  <framework>                  <X>%     ↓ -N%    ⚠ DROPPED
  <framework>                  <X>%     → 0%     ✓ STABLE
  <framework>                  <X>%     ↑ +N%    ✓ IMPROVING
  ...

# Show the next line ONLY when fewer than 3 frameworks are enabled.
# Source from get_recommended_compliance_frameworks_to_enable.
Recommended additional frameworks (from connected providers <connected_providers>): <top 3 display_names>

TOP FAILING CONTROLS (highest impact):
  [1] <control name> — failing on <N> assets, affects <M> frameworks
  [2] <control name> — failing on <N> assets, affects <M> frameworks
  [3] <control name> — failing on <N> assets, affects <M> frameworks

RECOMMENDED ACTION:
  The fastest score improvement: fix <top control> — affects
  <N> assets across <M> frameworks. I can generate the fix now.

  What format? terraform | cloudformation | ansible | cli |
  instructions | pulumi | arm/bicep

═══════════════════════════════════════════════════════════════════
Or drill down: controls | quick wins | accounts | trends |
remediation plan | <framework name> | full
═══════════════════════════════════════════════════════════════════
```

### Layer 2: Drill-Down Sections

#### "controls" — All Failing Controls

```
───────────────────────────────────────────────────────────────────
FAILING CONTROLS — <framework>
Score: <X>% (<P> pass, <F> fail of <T> total)
───────────────────────────────────────────────────────────────────

CRITICAL CONTROLS FAILING:
  <control-id>  <control name>
                Assets failing: <N> | Frameworks: <list>
                Fix: <1-line remediation summary>
                Failing assets (from get_control_test_assets):
                  - <name> (<type>) — <ui_url>
                  - <name> (<type>) — <ui_url>
                  ...

  <control-id>  <control name>
                ...

HIGH CONTROLS FAILING:
  ...

MEDIUM CONTROLS FAILING:
  ...

(Rendering the real failing assets — name, type, ui_url — per control is what lets
generated remediation code target actual resource IDs instead of a generic template.)

FIX NOW:
  Pick any control and I'll generate the remediation code.
  Choose format: terraform | cloudformation | ansible | cli |
  instructions | pulumi | arm/bicep

───────────────────────────────────────────────────────────────────
```

#### "quick wins" — Fastest Path to Improvement

```
───────────────────────────────────────────────────────────────────
QUICK WINS — Highest ROI Fixes
───────────────────────────────────────────────────────────────────

  [1] <control name>
      Fix: <specific action>
      Impact: passes control in these active frameworks: <active framework
              display_names from get_related_compliance_frameworks_for_asset,
              filtered to active === true>
      Failing assets (from get_control_test_assets):
        - <name> (<type>) — <ui_url>
        - ...
      Score boost: ~<X>% across <frameworks>
      Effort: LOW (single config change)

  [2] <control name>
      ...

  [3] <control name>
      ...

ESTIMATED TOTAL IMPROVEMENT:
  Fixing all <N> quick wins → +<X>% average score improvement

LET'S DO IT:
  I'll generate fixes for all quick wins in one batch.
  Choose format: terraform | cloudformation | ansible | cli |
  instructions | pulumi | arm/bicep

───────────────────────────────────────────────────────────────────
```

#### "accounts" — Account Breakdown

```
───────────────────────────────────────────────────────────────────
COMPLIANCE BY ACCOUNT
───────────────────────────────────────────────────────────────────

  Account                   Avg Score    Worst Framework    Failures
  ──────────────────────────────────────────────────────────────────
  <account-1>               <X>%         <framework> <Y>%   <N>
  <account-2>               <X>%         <framework> <Y>%   <N>
  ...

WORST ACCOUNT DEEP DIVE — <account>:
  Framework          Score    Gap from Target
  ──────────────────────────────────────────
  <framework>        <X>%     -<Y>% from 90%
  ...

  Top failures in this account:
    <control> — <N> assets
    ...

───────────────────────────────────────────────────────────────────
```

#### "trends" — Score History

```
───────────────────────────────────────────────────────────────────
COMPLIANCE TRENDS — Last 30 Days
───────────────────────────────────────────────────────────────────

  Date        Avg Score    Direction    Notable Changes
  ──────────────────────────────────────────────────────
  Apr 17      <X>%         ─            <note>
  Apr 10      <X>%         ↓ -N%        <note>
  Apr 03      <X>%         → 0%         <note>
  Mar 27      <X>%         ↑ +N%        <note>

FRAMEWORKS THAT DROPPED:
  <framework>: <from>% → <to>% (<reason if detectable>)

FRAMEWORKS THAT IMPROVED:
  <framework>: <from>% → <to>% (<what was fixed>)

───────────────────────────────────────────────────────────────────
```

#### "remediation plan" — Prioritized Fix Plan

```
───────────────────────────────────────────────────────────────────
REMEDIATION PLAN — Path to <target>% Compliance
───────────────────────────────────────────────────────────────────

PHASE 1: QUICK WINS (this week)
  Expected improvement: +<X>%
  [ ] <fix 1> — <N> assets, <M> frameworks
  [ ] <fix 2> — <N> assets, <M> frameworks
  [ ] <fix 3> — ...

PHASE 2: SYSTEMATIC FIXES (this month)
  Expected improvement: +<X>%
  [ ] <fix pattern> — <N> assets across <M> accounts
  [ ] <fix pattern> — ...

PHASE 3: ARCHITECTURAL (this quarter)
  Expected improvement: +<X>%
  [ ] <change> — requires <team/resource>
  [ ] <change> — ...

PROJECTED SCORES AFTER EACH PHASE:
  Framework         Current  Phase 1  Phase 2  Phase 3
  ─────────────────────────────────────────────────────
  <framework>       <X>%     <Y>%     <Z>%     <W>%
  ...

START NOW:
  Tell me which phase to start with and your preferred format.
  I'll generate implementation code for each fix in that phase.

  Format: terraform | cloudformation | ansible | cli |
  instructions | pulumi | arm/bicep

───────────────────────────────────────────────────────────────────
```

#### "<framework name>" — Single Framework Deep Dive

Show controls, account breakdown, and remediation plan for just that framework.

#### "full" — Everything Expanded

Show all sections in order.

## Edge Cases

### No Compliance Frameworks Enabled

Call `get_recommended_compliance_frameworks_to_enable` (no params) and render the tenant-aware
recommendations from its response: `frameworks[].display_name` and `connected_providers`.
```
⚠ No compliance frameworks enabled in Orca.

To get started, enable frameworks in:
  Orca Console → Compliance → Framework Settings

Recommended for your connected providers (<connected_providers>):
  • <frameworks[0].display_name>
  • <frameworks[1].display_name>
  • <frameworks[2].display_name>
  ...
```
If the tool returns an empty `frameworks` list, fall back to one line: "No tenant-specific recommendations available — enable a CIS Benchmark for your cloud provider to start."

### Framework Not Found
```
⚠ Framework "<input>" not found.

Available frameworks:
  <list of enabled frameworks>

Try: /orca-compliance-gap <exact framework name>
```

### Perfect Score
```
✅ <framework> — 100% compliant!

All <N> controls passing across <M> assets.
Last failure resolved: <date>

Recommendation: Set up alerts for score regression.
```

## MCP Tools Used

### Primary Tools

| Tool | Purpose | Parameter |
|------|---------|-----------|
| `get_enabled_compliance_frameworks` | All framework scores | optional `filters` |
| `get_compliance_trend_over_time` | Score history | `filters.datetime_filter` (7/14/30) |
| `get_compliance_analysis_by_account_or_business_unit` | Account/BU breakdown | `group_by` ("accounts" or "business_units") |
| `get_compliance_framework_control_tests` | Failing controls per framework | `framework_id`, optional `filters` |
| `get_compliance_framework_stats_for_asset` | Per-framework detailed stats | `framework_id` |
| `get_framework_assets_with_failed_controls_count` | Worst assets per framework | `framework_id` |
| `get_control_test_assets` | Compliant + non-compliant assets for one control test | `framework_id`, `rule_id` |
| `get_related_compliance_frameworks_for_asset` | All frameworks an asset participates in (active + inactive) | `asset_unique_id` (= `group_unique_id` from `get_control_test_assets`) |
| `get_compliance_analysis_by_account_or_business_unit` | Per-account score per framework (heatmap replacement) | `group_by: "accounts"`, `framework_ids: ["<id>"]` |

### Secondary Tools

| Tool | Purpose | When |
|------|---------|------|
| `get_control_test_alerts` | Alerts for a specific control | "controls" drill-down |
| `get_recommended_compliance_frameworks_to_enable` | Tenant-aware framework recommendations | empty-state edge case + sparse-coverage dashboard hint |
| `discovery_search` | Find assets related to a control failure | When investigating specific gaps |

### Parameter Notes

- `framework_id` comes from `get_enabled_compliance_frameworks` response
- `filters` object can contain: `datetime_filter`, `providers`, `accounts`, `framework_ids`, `business_units`
- `datetime_filter` values: 7, 14, 30 (days)
- `group_by` is an enum: `"accounts"` or `"business_units"`
- `framework_ids` on `get_compliance_analysis_by_account_or_business_unit` is **top-level, NOT under `filters`** — nesting it under `filters` is silently ignored or fails
- `rule_id` (e.g. `rcad0b53623`) is the second key needed for `get_control_test_assets`, sourced from `get_compliance_framework_control_tests` → `tests[].rule_id`
- `asset_unique_id` (e.g. `CodeRepository_<acct>_<resource>` or `vm_<acct>_<resource>`) for `get_related_compliance_frameworks_for_asset` is sourced from `get_control_test_assets` → `*_assets[].group_unique_id`
- `get_related_compliance_frameworks_for_asset` returns inactive frameworks too — filter `active: true` before counting

## Implementation Notes

1. **Parallelize all initial queries** — frameworks, trends, and account breakdown are independent.
2. **Cross-framework impact** is the key ranking metric — a control that fails in 5 frameworks is 5x more impactful to fix.
3. **Quick wins** should have estimated score improvements — calculate from (controls_fixed / total_controls) per framework.
4. **Account ownership** matters — the user needs to know WHO to assign the work to.
5. **Link to other skills** — suggest `/orca-alert-triage` for individual alert deep-dives from failing controls, `/orca-impact-analysis` for fix impact.
6. **Compliance tools are the most complete** in the Orca MCP — leverage all of them.
7. **Avoid the redundant account round-trip** — `get_enabled_compliance_frameworks` already returns `top_accounts` and `stats.accounts.data` (per-account pass/fail counts across the framework). Only call `get_compliance_analysis_by_account_or_business_unit` when you need the per-account *score* per framework (e.g. the heatmap replacement in Query 9); otherwise prefer the inline data.

### Response sizes are large — always scope first

Every compliance tool can return tens to hundreds of KB. Without scoping, the skill will hit context limits before it can rank or render. Default scoping rules:

- `get_compliance_framework_control_tests`: pass `filters.providers` and/or `filters.assets_categories` whenever the user query implies a scope (e.g. "PCI on AWS" → `providers: ["aws"]`).
- `get_control_test_assets`: call only on the top-N failing controls (default N=5), never on every failing control by default.
- `get_related_compliance_frameworks_for_asset`: call only on the top-N failing assets per control (default N=3), and de-duplicate by `group_unique_id` across controls.
- `get_enabled_compliance_frameworks`: when answering a single-framework question, pass `filters.framework_ids: ["<id>"]` instead of fetching all.
