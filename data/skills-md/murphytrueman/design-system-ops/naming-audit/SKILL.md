---
name: naming-audit
description: "Audit a design system's naming conventions across components, tokens, and patterns. Trigger when someone says: naming conventions, audit component names, are my names consistent, naming problems, naming review, inconsistent names, fix our naming, review naming, or anything about the quality or consistency of names in a design system."
references:
  - ../../knowledge-notes/output-discipline.md
---

# Naming audit

A skill for auditing naming conventions across a design system's components, tokens, and patterns. Produces a violation report with specific examples, ambiguity flags, and rename suggestions with rationale.

## Context

Naming is the primary interface between a design system and its consumers. A name is the first piece of information a designer or developer gets about what a component does, what a token means, or how a pattern behaves. Good names are predictable: consumers can guess what a name refers to before they look it up. Bad names require lookup, then clarification, then occasionally a conversation to confirm what was meant.

Naming problems accumulate. A single ambiguous component name is an inconvenience. Twenty ambiguous names spread across a library, with some following one convention and others following three others, is a system that new team members cannot navigate and experienced team members cannot trust.

This audit covers naming for components, tokens, and any documented patterns. It does not mandate a specific naming convention — it assesses whether the naming is consistent, unambiguous, and fit for its purpose.

## Step 0: Identify what you're looking at

Before auditing names, determine what kind of shared UI this is. The library type changes how strict the consistency expectations should be and what recommendations are proportionate.

**Classify from codebase signals:**

- **Design system** — Full audit applies. Naming conventions should be documented, consistent, and enforced. Recommend creating a decision record for any undocumented conventions.
- **Component library** — Naming consistency matters, but the recommendation to "create a decision record" should be scaled down to "write down the convention you're already following, even if it's just a comment in the README." A 5-component library does not need a formal governance artefact.
- **Pattern library** — Naming conventions often follow the documentation tool's conventions (Fractal's folder numbering, Storybook's story hierarchy). Audit against the tool's conventions as well as internal consistency. Pattern names tend to describe what the pattern shows rather than what it does — flag this only if it creates confusion, not as a blanket violation.
- **Utility collection** — Naming is the primary interface. Every utility name needs to be unambiguous and predictable because there's no documentation site to fall back on. The audit should be strict on clarity and lenient on formal convention — a utility called `clamp-width` is better than one called `u-cw` even if the latter follows a prefix convention.

**Include the classification in the report header** as "Library type: [Design system / Component library / Pattern library / Utility collection]" and calibrate recommendation weight accordingly.

---

## Step 1: Gather the name inventory

Ask for or confirm:
- Component names (full list)
- Token names (full list, or the semantic and component tiers if the primitive tier is large)
- Pattern names (if documented)
- Any existing naming convention documentation

If naming convention documentation exists, assess against it. If it does not, derive the implicit conventions from the existing names and note where they are inconsistent with each other.

**Small-system note (fewer than 5 components):** A naming audit on a system this size is more of a naming workshop than a compliance audit. The consistency check (Step 2) becomes trivial — with 1–4 components, either every name follows the same convention or the inconsistencies are immediately visible. Focus the audit on purpose clarity and ambiguity flags rather than pattern detection. The primary output should be a naming decision record (use the `decision-record` skill) establishing the convention now, while the system is small enough to rename without migration cost.

## Step 1b: Naming decision worksheet

If no naming convention documentation exists, use this worksheet to establish conventions before auditing against them. This prevents the audit from flagging inconsistencies without a reference point.

**Component naming:**
- Casing convention: [PascalCase / camelCase / kebab-case]
- Specificity direction: [general-to-specific (ButtonPrimary) / category-first (NavigationPrimary)]
- Abbreviation policy: [no abbreviations / approved list: ...]
- Prefix/suffix rules: [category prefixes? state suffixes? size suffixes?]

**Token naming:**
- Tier separator: [dot / dash / slash]
- Semantic pattern: [category.role.state / category.role.modifier]
- State naming: [default/hover/active/disabled / rest/hover/pressed/disabled]

**Document this as a decision record.** Use the `decision-record` skill to capture the naming conventions as a formal record. This creates a reference point for future audits and prevents the conventions from being lost when team members change.

## Step 2: Assess component naming

### Consistency check

Are component names following a consistent convention? Identify which conventions are in use:
- Casing: PascalCase, camelCase, kebab-case, or mixed
- Specificity pattern: general-to-specific (`ButtonPrimary`) or category-first (`NavigationPrimary`)
- Abbreviation policy: are abbreviations used, and are they consistent (`Btn` vs `Button`, `Nav` vs `Navigation`)

Flag any component whose name does not follow the dominant convention. Note whether the inconsistency is a naming decision (this component is intentionally named differently) or an oversight.

### Purpose clarity check

A component name should communicate what the component does without requiring context.

Flag names that:
- Are generic to the point of meaninglessness: `Box`, `Container`, `Wrapper`, `Layout`, `Base`
- Describe visual treatment rather than function: `BlueCard`, `LargeText`, `RoundedButton`
- Use internal team jargon: names that would not be understood by someone new to the organisation
- Are ambiguous between similar components: `Modal` and `Dialog` in the same system, `Tooltip` and `Popover` without clear distinction

For each flagged name: describe the ambiguity and suggest a rename. The rename suggestion should follow the system's established convention and improve rather than just change.

### Suffix and prefix conventions

If the system uses suffixes or prefixes to indicate category, variant, or role, are they applied consistently?

Common patterns to check:
- Size suffixes: `ButtonSm`, `ButtonMd`, `ButtonLg` — are sizes applied consistently across components?
- State suffixes: `-active`, `-disabled`, `-loading` — are state names consistent across components?
- Category prefixes: `Form-`, `Nav-`, `Data-` — are prefixes applied to all relevant components?

Flag any component that should have a prefix or suffix based on the system's conventions but does not.

## Step 3: Assess token naming

Token naming has additional criteria beyond general consistency. See the token-architecture knowledge note for the full three-tier model.

### Semantic token naming

Semantic tokens must describe intent, not appearance. Flag any semantic token that:
- Uses a colour name: `color.semantic.blue`, `color.secondary.green`
- Uses a visual descriptor: `color.light`, `spacing.large`, `font.bold`
- Is ambiguous between multiple potential uses: `color.accent`, `color.highlight`, `color.important`

For each flagged token: propose a rename that encodes intent rather than appearance.

### Tier consistency check

Are tokens within each tier named consistently with each other?

- Primitive tier: do all primitives follow the same pattern? (`color.blue.500` and `color.red.500` not `color.blue-500` and `color.red500`)
- Semantic tier: do semantic tokens follow a consistent category.role.state pattern?
- Component tier: do component tokens follow a consistent component.property.state pattern?

Flag any token that breaks from the dominant pattern within its tier.

### Cross-tier collision check

Are any token names used at multiple tiers with different meanings? This is rare but creates genuine confusion when it occurs. A semantic token named the same as a primitive it does not reference, or a component token named identically to a semantic token it does not correspond to, is a naming error.

## Step 4: Produce the naming audit report

Open with a headline sentence. Example: "Your component naming is consistent but your token naming has three competing conventions — here's where the friction is."

---

### Naming audit report

**Date:** [date]
**Scope:** [components / tokens / patterns / all]
**Convention documentation:** [exists and used as reference / does not exist — conventions derived from inventory]

---

#### Summary

One paragraph. What is the overall naming quality? Is the inconsistency concentrated (a specific era of the system, a specific team's contributions) or distributed? What is the most important finding? Be direct — if naming is a mess, say so plainly.

---

#### Convention inventory

What naming conventions are currently in use? List the dominant conventions and any divergent conventions found. This section tells the team what they are actually doing, which is the baseline for any improvement.

---

#### Findings

**Component naming violations**

| ID | Component name | Issue | Rename suggestion | Priority |
|---|---|---|---|---|
| NA-01 | [name] | [specific issue] | [suggested name] | 🟠/🟡/⚪ |

**Token naming violations**

| ID | Token name | Issue | Rename suggestion | Priority |
|---|---|---|---|---|
| NA-[n] | [token name] | [specific issue] | [suggested name] | 🟠/🟡/⚪ |

**Priority key:** 🟠 High (ambiguity creates real misuse risk) · 🟡 Medium (inconsistent but not misleading) · ⚪ Low (minor, low impact)

---

#### Recommendations

**If convention documentation does not exist:**
Create it before making naming changes. Without documentation, rename decisions will be made without a stable reference point, and the same inconsistencies will accumulate again.

**Sequencing renames:**
Renaming components and tokens is a breaking change. Recommendations:
1. Fix new additions first — apply the correct conventions going forward
2. Rename in order of severity: high-priority violations before medium and low
3. Use the deprecation process for component renames — the old name should be deprecated with a migration path, not removed immediately
4. Token renames should follow the same process as any other breaking change — see the `change-communication` skill

**Connection to decision-record:** Every naming convention established or changed during this audit should be documented as a decision record using the `decision-record` skill. The naming convention is the most frequently referenced governance decision in any design system — it deserves a formal record.

---

## Closing note (include in every report)

End the report with:

> **A note on context:** This audit checks naming patterns against common conventions — it does not know why a name was chosen. Some inconsistencies may be deliberate distinctions. If any finding flags a naming choice your team made intentionally, let me know — I'll learn your conventions and skip those patterns in future runs. The goal is to catch accidental inconsistency, not to override deliberate decisions.

---

## Quality checks

- Every violation has a specific rename suggestion with rationale, not just a flag
- Rename suggestions follow the system's established conventions — they improve the naming while maintaining consistency
- The convention inventory section describes what the system is actually doing, not what it should be doing
- Severity ratings reflect real impact: a misleading name is high priority, a minor casing inconsistency is low
- The recommendations section addresses sequencing — naming changes are breaking changes and should be treated accordingly
- The closing note about intentional deviations is present
