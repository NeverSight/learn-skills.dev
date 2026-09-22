---
name: governance-encoder
description: "Convert governance policies into machine-executable JSON constraint files that AI agents and CI pipelines validate against automatically. This produces rule engine files in .ai/governance/, NOT narrative decision records or documentation. Trigger when someone says: encode governance rules, governance as code, automate governance, rule engine, machine-executable constraints, enforce rules automatically, constraint definitions, or anything about converting human-readable policies into structured rules that tools check programmatically. Do NOT trigger for documenting why a decision was made or recording the reasoning behind a choice — use decision-record for those."
references:
  - ../../knowledge-notes/component-governance.md
  - ../../knowledge-notes/design-to-code-contract.md
  - ../../knowledge-notes/human-oversight-framework.md
  - ../../knowledge-notes/agent-orchestration-guide.md
---

# Governance encoder

A skill for converting design system governance policies — the rules about how the system should be used, contributed to, and evolved — from human-readable documentation into machine-executable constraint definitions that AI agents validate against in real time.

## Context

Most design system governance lives in documents that humans read and (sometimes) follow. Contribution guidelines in a wiki. Naming conventions in a README. Token usage rules in a Slack thread from eighteen months ago. These rules are enforced by review — a senior team member spots a violation during a PR review or a design crit and asks for a correction.

This enforcement model breaks down at scale, and it breaks down entirely with AI agents. An agent generating a component cannot read a wiki page and decide to follow the naming convention. It cannot recall a Slack conversation about token usage. It needs rules expressed as structured data with explicit conditions, constraints, and consequences that it can evaluate programmatically.

Governance encoding is the process of taking every governance rule that currently lives in a human-readable document and expressing it as a machine-checkable constraint. The output is not a better document — it is a rule engine that agents (and CI pipelines and linters) consume directly.

The distinction between governance documentation and governance encoding:
- **Documentation** says: "Components should follow our naming convention."
- **Encoding** says: `{ "rule": "component_naming", "pattern": "^[A-Z][a-zA-Z]+$", "scope": "component_export_name", "severity": "error", "message": "Component names must be PascalCase with no special characters" }`

Both are necessary. Documentation explains the intent. Encoding enforces the constraint.

---

## Configuration

Before producing output, check for a `.ds-ops-config.yml` file in the project root. If present, load:
- `governance.rule_format` — output format preference (JSON or YAML, default: JSON)
- `governance.severity_model` — custom severity levels (default: error/warning/info)
- `governance.categories` — override default rule categories
- `system.framework` — framework-specific rules (React, Vue, Svelte)
- `system.tokens` — identifies token files for token governance rules
- `integrations.*` — enables auto-pull for existing governance context

## Auto-pull integrations

If integrations are configured in `.ds-ops-config.yml`, pull data automatically:

**GitHub** (`integrations.github.enabled: true`):
- Pull CONTRIBUTING.md, PR templates, and issue templates for existing governance documentation
- Scan ESLint/Stylelint configs for existing code-level rules that overlap with governance
- Pull branch protection rules and CI configuration for release governance context

**Figma MCP** (`integrations.figma.enabled: true`):
- Read library publishing rules and component organisation structure
- Extract naming patterns from existing component names
- Identify variant naming conventions

If an integration fails, log it and proceed with manual input.

---

## Step 1: Inventory existing governance rules

Before encoding, catalogue what governance rules already exist and where they live.

Scan for governance sources:
- Contribution guidelines (CONTRIBUTING.md, wiki pages)
- Code style guides (ESLint configs, Prettier configs, Stylelint configs)
- Design guidelines (Figma file organisation rules, naming conventions)
- Release processes (CHANGELOG conventions, versioning rules)
- Token usage rules (documentation, code comments, linter configs)
- PR review checklists
- Decision records

For each rule found, classify:

| Rule | Source | Currently enforced by | Machine-encodable? |
|---|---|---|---|
| Component names must be PascalCase | CONTRIBUTING.md | PR review | Yes — regex pattern |
| Props must have TypeScript types | ESLint config | CI pipeline | Yes — already encoded |
| New components need design review | Wiki | Manual process | Partially — gate check |
| Tokens must use semantic tier | Style guide | PR review | Yes — import pattern |

Ask for or confirm:
- Are there governance rules that exist only in team knowledge (not documented anywhere)?
- Are there rules that are documented but not enforced (aspirational rules)?
- Are there rules that are currently enforced by linters that should be promoted to governance rules?
- What severity model does the team use? (Default: error blocks merge, warning flags for review, info provides guidance)

---

## Step 2: Define the rule schema

Every governance rule follows the same schema, regardless of what it governs:

```json
{
  "id": "GOV-001",
  "category": "naming",
  "rule": "component_export_name",
  "description": "Component export names must be PascalCase",
  "intent": "Consistent naming enables predictable imports and tooling integration",
  "scope": {
    "applies_to": "component_files",
    "file_pattern": "src/components/**/*.{tsx,vue,svelte}"
  },
  "constraint": {
    "type": "pattern",
    "pattern": "^[A-Z][a-zA-Z]+$",
    "target": "default_export_name"
  },
  "severity": "error",
  "enforcement": {
    "automated": true,
    "tool": "eslint",
    "rule_ref": "naming-convention"
  },
  "exceptions": {
    "allowed": true,
    "requires": "decision_record",
    "examples": ["hOTP (legacy naming, migration planned)"]
  },
  "references": {
    "governance_doc": "CONTRIBUTING.md#naming-conventions",
    "decision_record": null
  }
}
```

### Schema fields

**Required fields:**
- `id` — unique identifier for the rule (GOV-NNN format)
- `category` — rule category (naming, structure, tokens, accessibility, contribution, release, documentation)
- `rule` — machine-readable rule name
- `description` — human-readable description of what the rule requires
- `intent` — why this rule exists (the reasoning, not just the constraint)
- `scope` — where the rule applies
- `constraint` — the actual check definition
- `severity` — error (blocks), warning (flags), info (suggests)

**Optional fields:**
- `enforcement` — how the rule is currently enforced (automated tool, manual review, unenforced)
- `exceptions` — whether exceptions are allowed and what they require
- `references` — links to governance documentation and decision records

### Constraint types

Different rules require different constraint structures:

**Pattern constraint** — validates against a regex:
```json
{ "type": "pattern", "pattern": "^[A-Z][a-zA-Z]+$", "target": "export_name" }
```

**Presence constraint** — requires something to exist:
```json
{ "type": "presence", "target": "prop_types", "requires": ["type", "default", "description"] }
```

**Relationship constraint** — validates a relationship between elements:
```json
{ "type": "relationship", "source": "semantic_token", "target": "component_style", "rule": "no_primitive_tokens_in_components" }
```

**Threshold constraint** — validates against a numeric boundary:
```json
{ "type": "threshold", "target": "bundle_size_gzip", "max": 10240, "unit": "bytes" }
```

**Gate constraint** — requires a process step to be completed:
```json
{ "type": "gate", "requires": ["design_review_approved", "accessibility_audit_passed", "documentation_complete"], "before": "publish_to_npm" }
```

**Enumeration constraint** — validates against a set of allowed values:
```json
{ "type": "enumeration", "target": "component_status", "values": ["alpha", "beta", "stable", "deprecated"] }
```

---

## Step 3: Encode rules by category

### Naming rules

Rules that govern how things are named in the system:

- Component export names (PascalCase, no prefixes/suffixes unless system convention)
- Prop names (camelCase, consistent verb patterns for booleans: `is`, `has`, `show`)
- Token names (tier hierarchy, separator conventions, domain prefixes)
- File names (component file naming, test file naming, story file naming)
- CSS class names or variable names (if applicable)
- Event handler names (on + verb pattern)

### Structure rules

Rules that govern how things are organised:

- Component file structure (co-located tests, stories, styles)
- Directory organisation (by category, by feature, flat)
- Export patterns (barrel files, named exports, default exports)
- Dependency rules (which categories can depend on which — atoms cannot import organisms)
- Component composition limits (maximum nesting depth, prohibited parent-child combinations)

### Token rules

Rules that govern how design tokens are used:

- Semantic tokens required in component styles (no primitive tokens in component code)
- Token tier discipline (components reference semantic tier, semantic references primitive tier)
- No hardcoded values where tokens exist (raw hex, raw pixel values)
- Token naming must follow the system's naming convention
- New tokens require documentation before use

### Accessibility rules

Rules that govern accessibility compliance:

- All interactive components must have keyboard support
- All images must have alt text (or be explicitly decorative)
- Colour contrast must meet the system's minimum ratio
- Focus management must be explicit for overlays and modals
- ARIA attributes must follow the component's accessibility contract
- Reduced motion must be respected for all animations

### Contribution rules

Rules that govern how new work enters the system:

- New components require a design spec before development
- New components require an accessibility audit before release
- API changes require a decision record
- Breaking changes require a migration guide
- All components must reach documentation threshold before beta status

### Release rules

Rules that govern how the system is published:

- Changelog entry required for every release
- Semver rules (what constitutes major, minor, patch)
- Release approval gates (who must approve, what must pass)
- Deprecation notice period (how far in advance)
- Canary release requirements for major versions

### Documentation rules

Rules that govern documentation quality:

- Every component must have a description (minimum: purpose section)
- Every prop must have a type and description
- Every component must have at least one usage example
- Anti-patterns must be documented for all stable components
- Accessibility documentation must include keyboard and screen reader behaviour

---

## Step 4: Encode the exception framework

Not every rule applies in every situation. The exception framework defines how teams request, document, and track governance exceptions:

```json
{
  "exception_framework": {
    "levels": [
      {
        "level": "auto_approved",
        "description": "Exceptions that are pre-approved for specific contexts",
        "examples": ["Prototype/experiment branches exempt from documentation rules"],
        "requires": "nothing — automatically granted based on context detection",
        "expires": "When the context ends (branch merged or deleted)"
      },
      {
        "level": "team_approved",
        "description": "Exceptions approved by the component team lead",
        "examples": ["Temporary naming deviation during a migration"],
        "requires": "Decision record with rationale and expiry date",
        "expires": "On the specified date or when the migration completes"
      },
      {
        "level": "governance_approved",
        "description": "Exceptions approved by the design system governance group",
        "examples": ["Permanent deviation from token architecture for a specific product"],
        "requires": "Formal decision record with business justification",
        "expires": "When the governance group revokes or the justification no longer applies"
      }
    ],
    "tracking": {
      "format": "exception_record",
      "fields": ["rule_id", "level", "approved_by", "rationale", "scope", "expires", "status"],
      "review_cadence": "Quarterly review of all active exceptions"
    }
  }
}
```

---

## Step 5: Generate the rule engine output

### File structure

```
.ai/governance/
  rules/
    naming.json
    structure.json
    tokens.json
    accessibility.json
    contribution.json
    release.json
    documentation.json
  exceptions/
    active-exceptions.json
  governance-manifest.json
  enforcement-guide.md
```

### Governance manifest

```json
{
  "version": "1.0",
  "generated": "[date]",
  "system": "[design system name]",
  "total_rules": 42,
  "by_category": {
    "naming": 8,
    "structure": 6,
    "tokens": 7,
    "accessibility": 6,
    "contribution": 5,
    "release": 5,
    "documentation": 5
  },
  "by_severity": {
    "error": 15,
    "warning": 18,
    "info": 9
  },
  "enforcement_coverage": {
    "automated": "60%",
    "manual_review": "30%",
    "unenforced": "10%"
  },
  "active_exceptions": 3
}
```

### Enforcement guide

Generate an `enforcement-guide.md` that documents how each rule category maps to enforcement tooling:

```markdown
# Governance enforcement guide

## Automated enforcement

Rules that are enforced automatically through CI/CD and linters.
For each rule: the tool that enforces it, how to configure it,
and what happens when it triggers.

## Review-based enforcement

Rules that are enforced through PR review and design review.
For each rule: what reviewers should check, the review checklist item,
and escalation path for disputes.

## Agent enforcement

Rules that AI agents should check before producing output.
For each rule: the constraint definition the agent loads,
how the agent validates its output, and what the agent does
when a constraint is violated (block, warn, or note).

## Gap analysis

Rules that are documented but not yet enforced by any mechanism.
For each rule: the recommended enforcement path and estimated
effort to implement.
```

---

## Step 6: Map rules to agent behaviour

For each rule, define how AI agents should use it:

**Pre-generation check** — the agent checks the rule before producing output:
- Token rules: the agent only uses semantic tokens, never primitives
- Naming rules: the agent names generated components following the convention
- Composition rules: the agent respects parent-child constraints

**Post-generation validation** — the agent checks its own output against rules:
- Structure rules: generated files follow the expected structure
- Documentation rules: generated components include required documentation sections
- Accessibility rules: generated components include required ARIA attributes

**Gate enforcement** — the agent blocks actions that require process steps:
- Contribution rules: the agent flags that a design review is required
- Release rules: the agent verifies that all pre-release gates are met

Produce a mapping table:

| Rule ID | Agent phase | Agent action on violation |
|---|---|---|
| GOV-001 | Pre-generation | Use correct naming pattern |
| GOV-012 | Post-generation | Replace primitive token with semantic equivalent |
| GOV-025 | Gate | Block and report: "Design review required before this component can be published" |

---

## Recommend to the user

- Start by encoding the rules that are violated most frequently — these have the highest return on investment
- Every encoded rule should include `intent` — agents that understand why a rule exists can make better judgments in ambiguous situations
- Run the rule engine in "audit mode" first (report violations, do not block) to calibrate severity levels before switching to enforcement mode
- Review the exception framework quarterly — stale exceptions that were never resolved are governance debt
- Pair every `error` severity rule with automated enforcement. A rule that blocks but is not automated creates friction without reliability.
- Commit the governance rules alongside the codebase and update them as part of governance changes

---

## Quality checks

- Every rule has a unique ID that does not collide with existing rules
- Every rule has both a `description` (what) and an `intent` (why)
- Constraint definitions are precise enough that two independent implementations would produce the same validation result
- Severity levels are calibrated: `error` rules represent genuine risks, not preferences
- The exception framework exists and includes a review cadence — exceptions without expiry dates accumulate indefinitely
- Agent behaviour mapping covers all rules, not just the automated subset
- The enforcement guide distinguishes between rules that are enforced today and rules that should be enforced (aspiration vs reality)
- Rule categories are comprehensive — no governance rule that the team actually follows is missing from the encoded set
