---
name: experience-lwc-legacy-migrate
description: "Migrate legacy Salesforce UI stacks onto modern LWC — Aura → LWC conversion completeness verification and Lightning Out Beta → Lightning Out 2.0 host-page migration. TRIGGER on \"verify Aura to LWC migration completeness\", \"migrate Lightning Out Beta to LO 2.0\", \"upgrade $Lightning.use() to <lightning-out-application>\", \"replace hardcoded LO tokens with OAuth PKCE\", \"write an LO 2.0 host page\", or an external Lightning Out page that stopped rendering; also `.cmp`/`.js-meta.xml` files alongside LWC. DO NOT TRIGGER for the initial Aura-to-LWC conversion (use experience-aura-lwc-migrate), a React-to-LWC migration, or building a new LWC (use experience-lwc-design-generate)."
metadata:
  version: "1.0"
  domains: ["Experience"]
  relatedSkills:
    - "experience-aura-lwc-migrate"
    - "experience-lwc-design-generate"
  cliTools:
    - tool: ["python3"]
      semver: ">=3.8"
---
<!-- adk-managed-skill -->

# Migrating Legacy LWC Stacks

Two distinct migration workflows live here because users in the middle of
migrating Aura components are often also migrating Lightning Out host pages
— they benefit from one skill that knows both.

| Migration                          | Use when                                               | Reference                                                                                              |
|------------------------------------|--------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| Aura → LWC completeness check      | An Aura component was converted, verify nothing is lost | [aura-to-lwc-completeness-checklist.md](references/aura-to-lwc-completeness-checklist.md)              |
| Lightning Out Beta → LO 2.0        | Migrating an external host page off `lightning.out.js`  | [lightning-out-beta-to-2-migration.md](references/lightning-out-beta-to-2-migration.md)                |

## When to Use This Skill

- User has already converted an Aura component to LWC and wants a structured
  completeness check.
- User has a non-Salesforce host page that embeds Salesforce LWC via
  Lightning Out Beta and needs to move to LO 2.0.
- User is upgrading `$Lightning.use()` / `$Lightning.createComponent()` calls
  to the `<lightning-out-application>` web component pattern.
- User needs to replace a hardcoded LO auth token with OAuth PKCE + front-door
  flow.

If the user wants to build a brand-new LO 2.0 host page from scratch (no Beta
code to migrate), the LO 2.0 system reference inside this skill is still the
right source of truth — point them at it directly.

## Prerequisites

- Access to the source (Aura component files or Beta host page).
- For LO 2.0 migration: ability to create an External Client App (ECA) in
  Salesforce Setup (Consumer Key required) and optionally a Lightning Out 2.0
  App (18-char App ID).
- For Aura migration: access to the LWC conversion, including any `__tests__`
  (Jest) and `__utam__` (UTAM) folders if they exist.


## Workflow A — Aura → LWC Completeness Check

Goal: rate an already-done Aura-to-LWC conversion across 12 dimensions and
produce actionable recommendations.

### Step A1 — Identify the component

Ask the user for the component name (e.g. `accountTile`). Locate the Aura
source (`{componentName}.cmp`, controller, helper, CSS) and the LWC output
(`{componentName}.html`, `.js`, `.css`, `.js-meta.xml`).

### Step A2 — Run the checklist

Follow [aura-to-lwc-completeness-checklist.md](references/aura-to-lwc-completeness-checklist.md)
verbatim:

- Score the conversion on all 12 metrics (Functional Parity, Event Handling,
  Data Binding & State, UI/UX Parity, Extensibility & Modularity, Error
  Handling, Localization, Security & Access Control, Performance, Salesforce
  Best Practices, Jest Test Coverage, UTAM Page Objects).
- Use the six-rating scale: Excellent / Good / Satisfactory / Limited / Poor
  / Missing.
- Present the output as a list (not a table), per the reference.

### Step A3 — Summarize + recommend

End with an overall confidence statement and a prioritized list of specific,
actionable recommendations (what to fix, in what order).


## Workflow B — Lightning Out Beta → LO 2.0

Goal: transform a Lightning Out Beta host page into a Lightning Out 2.0 host
page while leaving the customer's HTML structure, styling, and business logic
intact.

### Step B1 — Read the LO 2.0 mental model

Internalize the architecture *before* editing code:
[lightning-out-2-system-reference.md](references/lightning-out-2-system-reference.md).

Key takeaway: LO 2.0 is not a library upgrade. It runs the LWC inside an
iframe with a closed shadow DOM — host-page JS cannot touch the LWC and
vice versa, and host-page CSS does not cascade in.

### Step B2 — Identify Beta patterns

Use Phase 1 of the migration guide to locate:

- **Pattern A** — Script tag loading `lightning.out.js` (extract the domain).
- **Pattern B** — Config variables (endpoint, Aura app, component, token).
- **Pattern C** — `$Lightning.use(...)` call.
- **Pattern D** — `$Lightning.createComponent(...)` call.
- **Pattern E** — DOM target element referenced by the 3rd arg of Pattern D.

See [lightning-out-beta-to-2-migration.md § Phase 1](references/lightning-out-beta-to-2-migration.md).

### Step B3 — Apply transformations

The script-tag URL, the component tag name, and the attribute names are
**deterministic** conversions — derive them with the helper script so they are
exact every time (namespace preserved, camelCase → kebab-case, Beta host →
versioned LO 2.0 library URL):

```bash
python3 scripts/convert-lo-names.py \
  --component c:myComponent \
  --attributes recordId,ownerId \
  --my-domain https://<DOMAIN>.lightning.force.com
```

It prints the `<c-...>` tag, the kebab-case attributes, and the versioned LO
2.0 library URL. Then work through Phase 2 of the guide:

1. **Script tag** — use the `library-url` the script prints; add `async`.
2. **Component name / attributes** — use the `component-tag` and kebab-case
   attributes the script prints.
3. **Component tag** — add the `<c-...>` tag directly in HTML at the target
   location (a judgement call — place it where the Beta render target was).
4. **Replace the `$Lightning` block** — delete it entirely and start from
   [assets/lo20-host-page-template.html](assets/lo20-host-page-template.html),
   filling in the config constants; it already includes the helper functions,
   `mountLo20(frontdoorUrl, orgUrl)`, `boot()`, and the OAuth listeners.

### Step B4 — Six non-negotiable rules

These rules cause silent runtime failures if violated, and every one is a
deterministic code-structure check. Enforce them with the validator script
rather than by eye — run it against the migrated page and fix every FAIL:

```bash
python3 scripts/validate-lo20-page.py <migrated-page.html>
```

It prints a PASS/FAIL line per rule (plus the LO 2.0 library and Beta-removal
checks) and exits non-zero if any rule fails. The six rules it enforces:

1. `customElements.whenDefined(...)` must receive a **literal string**, not
   the `components` variable.
2. `mountLo20(frontdoorUrl, orgUrl)` must accept two parameters.
3. Call `clearCachedResult()` before every `mountLo20(...)`.
4. Always pass both parameters when calling `mountLo20(...)`, even if
   `orgUrl` is undefined.
5. Wrap all initialization in `boot()` and call `boot()` at the end.
6. The component tag has **no inline `display:none`** — control visibility
   via the loading indicator.

### Step B5 — Salesforce setup

- **External Client App (ECA)** — Setup → App Manager → New Connected App →
  External Client App. Enable OAuth with PKCE. Copy the Consumer Key.
- **Lightning Out 2.0 App** — apply this decision before continuing:

  | Condition | Action |
  |---|---|
  | Host page sets `app-id="..."` | Setup → Lightning Out → New LO App; copy the 18-character App ID into the host page's `app-id` attribute |
  | Host page embeds LWC directly (no `app-id`) | Skip the LO App entirely |
- Helper files the migration assumes exist alongside the host page:
  `frontdoor-url.html` (OAuth callback) and `utils/LightningOutAuth.js`
  (PKCE implementation).

### Step B6 — Run the LO 2.0 verification checklist

First run `python3 scripts/validate-lo20-page.py <migrated-page.html>` to clear
the mechanical checks, then walk the remaining manual items in the full
post-migration checklist — cover every item before declaring the migration
done. See the "Verification Checklist" section at the end of
[lightning-out-beta-to-2-migration.md](references/lightning-out-beta-to-2-migration.md).


## Verification Checklist (high level)

For Aura → LWC:
- [ ] All 12 completeness metrics rated with a justification.
- [ ] Output in list form (not table), per the reference.
- [ ] Overall confidence statement present.
- [ ] Concrete, prioritized recommendations listed.

For LO Beta → LO 2.0:
- [ ] Script tag uses `.my.salesforce.com/lightning/lightning.out.latest/index.iife.prod.js` with `async`.
- [ ] No references to `$Lightning.use` / `$Lightning.createComponent` remain.
- [ ] Component name is kebab-case; attributes are kebab-case.
- [ ] `mountLo20(frontdoorUrl, orgUrl)` takes two parameters.
- [ ] `customElements.whenDefined(...)` uses a literal string.
- [ ] All initialization wrapped in `boot()` and `boot()` is called once.
- [ ] OAuth PKCE flow replaces hardcoded token; postMessage, BroadcastChannel,
      and storage listeners all present and defensively coded.
- [ ] Component tag has no inline `display:none`.


## Troubleshooting

- **LO 2.0 mount hangs** — custom element not registered. Verify the library
  script tag URL and that the `app-id` / `frontdoor-url` values are correct.
- **Component renders empty** — attributes probably still in camelCase. LO 2.0
  reads HTML attributes which must be kebab-case.
- **OAuth callback never fires** — one of postMessage / BroadcastChannel /
  storage listeners was dropped. LO 2.0 needs all three.
- **Aura checklist scored "Missing" on UTAM or Jest** — may be acceptable if
  the team has an alternative test strategy; flag in recommendations rather
  than block.
