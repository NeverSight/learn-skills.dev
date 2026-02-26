---
name: detect-product
description: Product reality extraction with evidence-backed features, monetization, and metrics. Use when analyzing product capabilities.
allowed-tools: Read, Glob, Grep, Write($JAAN_OUTPUTS_DIR/**), Edit(jaan-to/config/settings.yaml), Edit($JAAN_CONTEXT_DIR/**)
argument-hint: "[repo] [--full]"
context: fork
license: MIT
compatibility: Designed for Claude Code with jaan-to plugin. Partial standalone support for analysis mode.
---

# detect-product

> Evidence-based product reality extraction: features, monetization, instrumentation, and constraints.

## Context Files

- `$JAAN_LEARN_DIR/jaan-to-detect-product.learn.md` - Past lessons (loaded in Pre-Execution)
- `$JAAN_CONTEXT_DIR/tech.md` - Tech stack (for framework-aware scanning)
- `$JAAN_TEMPLATES_DIR/jaan-to-detect-product.template.md` - Output template
- `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md` - Language resolution protocol

**Output path**: `$JAAN_OUTPUTS_DIR/detect/product/` — flat files, overwritten each run (no IDs).

## Input

**Arguments**: $ARGUMENTS — parsed in Step 0.0. Repository path and mode determined there.

---

## Pre-Execution Protocol
**MANDATORY** — Read and execute ALL steps in: `${CLAUDE_PLUGIN_ROOT}/docs/extending/pre-execution-protocol.md`
Skill name: `detect-product`
Execute: Step 0 (Init Guard) → A (Load Lessons) → B (Resolve Template) → C (Offer Template Seeding)

### Language Settings
Read and apply language protocol: `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md`
Override field for this skill: `language_detect-product`

---

## Standards Reference

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-shared-reference.md` for Evidence Format (SARIF), Evidence ID Generation, Confidence Levels, Frontmatter Schema, Platform Detection, Document Structure, and Codebase Content Safety.

**This skill's namespace**: `E-PRD-*` (e.g., E-PRD-001, E-PRD-WEB-001)
**Tool name in frontmatter**: `detect-product`

**Cross-platform linking**: Use `related_evidence` field to link findings of the same feature across different platforms (see Step 0 for examples).

### Feature Evidence Linking — 3-Layer Model

"Feature exists" requires evidence across up to 3 layers:

| Layer | What | Example |
|-------|------|---------|
| **Surface** | Route, page, or screen | `/pricing` route, `PricingPage.tsx` |
| **Copy** | User-facing text | "Upgrade to Pro", pricing table copy |
| **Code path** | Business logic | `checkSubscription()`, Stripe API call |

**Confidence mapping**:
- All 3 layers found -> **Confirmed**
- 2/3 layers -> **Firm**
- 1 layer + heuristics -> **Tentative**
- Inferred only -> **Uncertain**

---

# PHASE 1: Detection (Read-Only)

## Step 0.0: Parse Arguments

**Arguments**: $ARGUMENTS

| Argument | Effect |
|----------|--------|
| (none) | **Light mode** (default): Surface + business logic scan, single summary file |
| `[repo]` | Scan specified repo (applies to both modes) |
| `--full` | **Full mode**: All detection steps, 7 output files (current behavior) |

**Mode determination:**
- If `$ARGUMENTS` contains `--full` as a standalone token → set `run_depth = "full"`
- Otherwise → set `run_depth = "light"`

Strip `--full` token from arguments. Set `repo_path` to remaining arguments (or current working directory if empty).

## Thinking Mode

**If `run_depth == "full"`:** ultrathink
**If `run_depth == "light"`:** megathink

Use extended reasoning for:
- Feature evidence linking across 3 layers
- Monetization model inference
- Instrumentation taxonomy analysis
- Constraint and risk assessment

## Step 0: Detect Platforms

**Purpose**: Auto-detect platform structure for multi-platform product feature tracking.

Use **Glob** and **Bash** to identify platform folders (same as detect-dev - see detect-dev Step 0 for full patterns and disambiguation rules).

### Platform Detection

1. **Check for monorepo markers**: `pnpm-workspace.yaml`, `lerna.json`, `nx.json`, `turbo.json`
2. **List top-level directories**: Exclude `node_modules`, `.git`, build outputs
3. **Match against platform patterns**: Apply disambiguation rules
4. **Handle detection results**:
   - No platforms → Single-platform: `platforms = [{ name: 'all', path: '.' }]`
   - Platforms detected → Multi-platform: Ask user to select all or specific platforms

### Product Detection Applicability

**Product detection is FULLY applicable to ALL platform types** (web, mobile, backend, cli, etc.)

| Platform Type | Product Analysis Scope |
|---------------|------------------------|
| web, mobile, androidtv, ios, android, desktop | Full feature detection (UI + business logic) |
| backend, api, services | Full feature detection (API endpoints, business logic, data models) |
| cli, cmd | Full feature detection (commands, flags, help text) |

### Cross-Platform Feature Linking

When the same feature appears across multiple platforms, use `related_evidence` field to link findings:

**Example: User Authentication across Web + Mobile**

```yaml
# In web/product/features.md:
evidence:
  id: E-PRD-WEB-015
  type: feature
  related_evidence: [E-PRD-MOBILE-023, E-PRD-BACKEND-042]
  description: "User authentication feature with OAuth support"
  layers:
    surface: "web/src/pages/login.tsx"
    copy: "Sign in with Google"
    code_path: "web/src/auth/oauth.ts"
  confidence: 1.0  # Confirmed (all 3 layers)

# In mobile/product/features.md:
evidence:
  id: E-PRD-MOBILE-023
  type: feature
  related_evidence: [E-PRD-WEB-015, E-PRD-BACKEND-042]
  description: "User authentication feature with OAuth support"
  layers:
    surface: "mobile/screens/LoginScreen.tsx"
    copy: "Sign in with Google"
    code_path: "mobile/services/auth.ts"
  confidence: 1.0  # Confirmed (all 3 layers)

# In backend/product/features.md:
evidence:
  id: E-PRD-BACKEND-042
  type: feature
  related_evidence: [E-PRD-WEB-015, E-PRD-MOBILE-023]
  description: "OAuth authentication API endpoints"
  layers:
    surface: "POST /api/auth/oauth"
    code_path: "backend/routes/auth.ts"
  confidence: 0.90  # Firm (2/3 layers - no UI copy in backend)
```

**Rationale**:
- Preserves traceability: each platform's findings stay in its own output file
- Enables detect-pack to identify cross-platform features in merged reports
- Allows confidence comparison across platforms (e.g., web has full 3-layer evidence, backend has 2-layer)

### Analysis Loop

For each platform in platforms:
1. Set `current_platform = platform.name`
2. Set `base_path = platform.path`
3. Run detection steps per `run_depth`:
   - **If `run_depth == "full"`:** Run Steps 1-5 scoped to `base_path`
   - **If `run_depth == "light"`:** Run Steps 1 and 3 only scoped to `base_path` (skip Steps 2, 4, 5)
4. When feature is detected, check if it's already detected in another platform:
   - Search across other platforms' findings for matching feature by name/description
   - If match found, add cross-platform links via `related_evidence`
5. Use platform-specific output paths in Step 7

**Note**: If single-platform mode (`platform.name == 'all'`), output paths have NO suffix. If multi-platform mode, output paths include `-{platform}` suffix.

## Step 1: Scan Routes and Screens (Surface Layer)

Identify all user-facing surfaces:

### Route Detection
- Glob: `**/pages/**/*.{tsx,jsx,vue}` — file-based routing (Next.js, Nuxt)
- Glob: `**/app/**/page.{tsx,jsx,ts,js}` — Next.js app router
- Grep for route definitions: `<Route`, `useRoutes`, `createBrowserRouter`
- Grep for API routes: `app.get(`, `router.post(`, `@Get(`, `@Post(`

### Screen/Page Inventory
For each route/page, extract:
- Route path
- Page/component name
- Public vs authenticated (look for auth guards, middleware)
- Feature domain (billing, settings, dashboard, etc.)

**If `run_depth == "light"`:** Skip Step 2. Proceed to Step 3 (Scan Business Logic).

## Step 2: Scan User-Facing Copy (Copy Layer)

Extract product-relevant text:

### Value Proposition Signals
- Grep: `**/landing*`, `**/home*`, `**/marketing*` for taglines and value statements
- Grep for hero sections: `<Hero`, `hero-section`, `landing-hero`
- Extract: headlines, subheadlines, CTA button text

### Pricing Copy
- Glob: `**/pricing.*`, `**/tiers.*`, `**/plans.*`
- Grep for pricing patterns: `\$\d+`, `/month`, `/year`, `per seat`, `upgrade`, `downgrade`
- Grep for tier names: `free`, `starter`, `pro`, `enterprise`, `premium`, `basic`

### Feature Descriptions
- Grep for feature lists: `features`, `capabilities`, `benefits`
- Extract feature names and descriptions from marketing/product pages

## Step 3: Scan Business Logic (Code Path Layer)

### Monetization / Billing
- Grep for Stripe: `stripe.subscriptions`, `stripe.invoices`, `stripe.checkout`, `stripe.prices`
- Grep for PayPal: `paypal`, `braintree`
- Grep for custom billing: `checkSubscription()`, `requiresPremium`, `userTier`, `planId`
- Grep for entitlement gates: `canAccess`, `hasFeature`, `isAllowed`, `checkPermission`
- Grep for usage limits: `rateLimited`, `usageCount`, `quota`, `limit`

### Entitlement Enforcement
- Grep for tier checks: `user.plan`, `user.tier`, `subscription.status`
- Grep for feature flags as gates: `isFeatureEnabled`, `featureToggle`
- Grep for middleware/guards: `requiresAuth`, `requiresPlan`, `checkEntitlement`

Distinguish "pricing copy" (what the product claims) from "enforcement" (what the code actually enforces). Gates must be proven by code locations; absence = "absence" evidence item.

**If `run_depth == "light"`:** Skip Steps 4-5. Proceed directly to Step 6 (Present Detection Summary).

**Note**: In light mode, features are capped at Tentative confidence (1 of 3 evidence layers from surface scan only). Cross-platform `related_evidence` linking works but is degraded (no copy-layer features).

## Step 4: Scan Instrumentation / Analytics

### Analytics SDKs
- Grep: `gtag('event'` — Google Analytics 4
- Grep: `mixpanel.track` — Mixpanel
- Grep: `analytics.track` — Segment
- Grep: `posthog.capture` — PostHog
- Grep: `amplitude.track` — Amplitude
- Grep: `plausible` — Plausible Analytics

### Feature Flags
- Grep: `unleash.isEnabled` — Unleash
- Grep: `launchdarkly.variation`, `ldClient` — LaunchDarkly
- Grep: `splitio`, `getTreatment` — Split.io
- Grep: `flagsmith` — Flagsmith
- Grep: `FEATURE_`, `FF_` — custom feature flag patterns

### Event Taxonomy
For each analytics call found, extract:
- Event name
- Properties/parameters
- Location (file:line)

Assess taxonomy consistency: naming convention, property standardization, coverage gaps.

## Step 5: Scan Product Constraints

### Technical Constraints
- Grep for rate limiting: `rateLimit`, `throttle`, `rateLimiter`
- Grep for file size limits: `maxFileSize`, `MAX_UPLOAD`, `fileSizeLimit`
- Grep for user limits: `maxUsers`, `seatLimit`, `teamSize`

### Business Rules
- Grep for trial/expiration: `trialEnd`, `expiresAt`, `gracePeriod`
- Grep for geo-restrictions: `allowedCountries`, `blockedRegions`, `geoRestrict`
- Grep for compliance: `GDPR`, `CCPA`, `HIPAA`, `SOC2`, `PCI`

### Risk Signals
- Features with routes but no tests
- Pricing copy without enforcement code
- Analytics events without consistent naming
- Entitlement checks with hardcoded values

---

# HARD STOP — Detection Summary & User Approval

## Step 6: Present Detection Summary

**If `run_depth == "light"`:**

```
PRODUCT DETECTION COMPLETE (Light Mode)
-----------------------------------------

PLATFORM: {platform_name or 'all'}

FEATURES DETECTED: {n}
  Tentative (surface-layer): {n}
  Cross-platform:            {n} features linked via related_evidence

MONETIZATION
  Model:        {free|freemium|subscription|usage-based|one-time|none detected}
  Tiers:        {tier names or "none detected"}
  Enforcement:  {n} code gates found    [Confidence: {level}]

SEVERITY SUMMARY
  Critical: {n}  |  High: {n}  |  Medium: {n}  |  Low: {n}  |  Info: {n}

OVERALL SCORE: {score}/10

OUTPUT FILE (1):
  $JAAN_OUTPUTS_DIR/detect/product/summary{-platform}.md

Note: Features at Tentative confidence (surface layer only).
Run with --full for copy layer, instrumentation audit, constraint analysis,
and 3-layer evidence linking (7 output files).
```

> "Proceed with writing summary to $JAAN_OUTPUTS_DIR/detect/product/? [y/n]"

**If `run_depth == "full"`:**

```
PRODUCT DETECTION COMPLETE
---------------------------

PLATFORM: {platform_name or 'all'}

FEATURES DETECTED: {n}
  Confirmed (3-layer): {n}
  Firm (2-layer):      {n}
  Tentative (1-layer): {n}
  Inferred:            {n}
  Cross-platform:      {n} features linked via related_evidence

MONETIZATION
  Model:        {free|freemium|subscription|usage-based|one-time|none detected}
  Tiers:        {tier names or "none detected"}
  Enforcement:  {n} code gates found    [Confidence: {level}]

INSTRUMENTATION
  Analytics:    {tool names or "none detected"}
  Feature flags: {tool names or "none detected"}
  Events:       {n} tracked events

SEVERITY SUMMARY
  Critical: {n}  |  High: {n}  |  Medium: {n}  |  Low: {n}  |  Info: {n}

OVERALL SCORE: {score}/10

OUTPUT FILES (7):
  $JAAN_OUTPUTS_DIR/detect/product/overview{-platform}.md       - Product overview
  $JAAN_OUTPUTS_DIR/detect/product/features{-platform}.md       - Feature inventory
  $JAAN_OUTPUTS_DIR/detect/product/value-prop{-platform}.md     - Value proposition signals
  $JAAN_OUTPUTS_DIR/detect/product/monetization{-platform}.md   - Monetization model
  $JAAN_OUTPUTS_DIR/detect/product/entitlements{-platform}.md   - Entitlement enforcement
  $JAAN_OUTPUTS_DIR/detect/product/metrics{-platform}.md        - Instrumentation reality
  $JAAN_OUTPUTS_DIR/detect/product/constraints{-platform}.md    - Constraints and risks

Note: {-platform} suffix only if multi-platform mode (e.g., -web, -backend). Single-platform mode has no suffix.
```

> "Proceed with writing 7 output files to $JAAN_OUTPUTS_DIR/detect/product/? [y/n]"

**Do NOT proceed to Phase 2 without explicit approval.**

---

# PHASE 2: Write Output Files

## Step 7: Write to $JAAN_OUTPUTS_DIR/detect/product/

Create directory `$JAAN_OUTPUTS_DIR/detect/product/` if it does not exist.

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-shared-reference.md` sections "Output Path Logic" and "Stale File Cleanup" for platform-specific suffix convention and run_depth cleanup rules.

### If `run_depth == "light"`: Write Single Summary File

Write one file: `$JAAN_OUTPUTS_DIR/detect/product/summary{suffix}.md`

Contents:
1. Universal YAML frontmatter with `platform` field, `findings_summary`, and `overall_score`
2. **Executive Summary** — BLUF of product findings
3. **Feature Inventory** — routes/screens with auth classification, Tentative confidence (from Step 1)
4. **Monetization + Entitlement Summary** — billing integrations, tier detection, code gates (from Step 3)
5. **Top Findings** — up to 5 highest-severity findings with evidence blocks
6. **Note**: "Features at Tentative confidence (surface layer only). Run with `--full` for copy layer analysis, instrumentation audit, feature flag detection, constraint analysis, and 3-layer evidence linking."

### If `run_depth == "full"`: Write 7 Output Files

Write 7 output files:

| File | Content |
|------|---------|
| `$JAAN_OUTPUTS_DIR/detect/product/overview{suffix}.md` | Product overview with feature summary |
| `$JAAN_OUTPUTS_DIR/detect/product/features{suffix}.md` | Feature inventory with 3-layer evidence + `related_evidence` for cross-platform features |
| `$JAAN_OUTPUTS_DIR/detect/product/value-prop{suffix}.md` | Value proposition signals from copy |
| `$JAAN_OUTPUTS_DIR/detect/product/monetization{suffix}.md` | Monetization model with evidence |
| `$JAAN_OUTPUTS_DIR/detect/product/entitlements{suffix}.md` | Entitlement enforcement mapping |
| `$JAAN_OUTPUTS_DIR/detect/product/metrics{suffix}.md` | Instrumentation reality (analytics, flags, events) |
| `$JAAN_OUTPUTS_DIR/detect/product/constraints{suffix}.md` | Technical/business constraints and risks |

**Note**: `{suffix}` is empty for single-platform mode, or `-{platform}` for multi-platform mode.

Each file MUST include:
1. Universal YAML frontmatter with `platform` field and findings_summary/overall_score
2. Executive Summary
3. Scope and Methodology
4. Findings with evidence blocks (using E-PRD-{PLATFORM}-NNN or E-PRD-NNN IDs)
   - For cross-platform features, include `related_evidence` field linking to same feature in other platforms
5. Recommendations

---

## Step 7a: Seed Reconciliation

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/seed-reconciliation-reference.md` for comparison rules, discrepancy format, and auto-update protocol.

1. Read domain-relevant seed files: `$JAAN_CONTEXT_DIR/tech.md`, `$JAAN_CONTEXT_DIR/integrations.md`
2. Compare detection results against seed content (feature references, analytics tools, external integrations, monetization providers)
3. If discrepancies found:
   - Display discrepancy table to user
   - Offer auto-updates for non-destructive changes: `[y/n]`
   - Suggest `/jaan-to:learn-add` commands for patterns worth documenting
4. If no discrepancies: display "Seed files are aligned with detection results."

---

## Step 8: Capture Feedback

> "Any feedback on the product detection? [y/n]"

If yes:
- Run `/jaan-to:learn-add detect-product "{feedback}"`

---

## Skill Alignment

- Two-phase workflow with HARD STOP for human approval
- Evidence-based findings with confidence scoring
- Fork-isolated execution (`context: fork`)
- Output to standardized `$JAAN_OUTPUTS_DIR` path

## Definition of Done

**If `run_depth == "light"`:**

- [ ] Single summary file written to `$JAAN_OUTPUTS_DIR/detect/product/summary{suffix}.md`
- [ ] Universal YAML frontmatter with `overall_score`
- [ ] Feature inventory at Tentative confidence with evidence blocks
- [ ] Monetization + entitlement summary included
- [ ] "--full" upsell note included
- [ ] User approved output

**If `run_depth == "full"`:**

- [ ] All 7 output files written to `$JAAN_OUTPUTS_DIR/detect/product/`
- [ ] Universal YAML frontmatter with `platform` field in every file
- [ ] Every finding has evidence block with correct ID format (E-PRD-NNN for single-platform, E-PRD-{PLATFORM}-NNN for multi-platform)
- [ ] Feature evidence uses 3-layer model with confidence mapping
- [ ] Cross-platform features linked via `related_evidence` field (if multi-platform)
- [ ] Monetization distinguishes "copy" from "enforcement"
- [ ] Absence evidence used where appropriate (not claims without evidence)
- [ ] Instrumentation taxonomy consistency assessed
- [ ] Confidence scores assigned to all findings
- [ ] Output filenames match platform suffix convention (no suffix for single-platform, -{platform} suffix for multi-platform)
- [ ] User approved output
- [ ] Seed reconciliation check performed (discrepancies reported or alignment confirmed)
