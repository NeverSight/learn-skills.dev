---
name: version-bump-advisor
description: "Recommend the correct semver bump with reasoning and a generated changelog entry. Trigger when someone says: what version bump, is this a breaking change, semver recommendation, should this be major or minor, version this release, changelog entry, what kind of release is this, or anything about versioning a design system release."
references:
  - ../../knowledge-notes/component-governance.md
  - ../../knowledge-notes/design-to-code-contract.md
---

# Version Bump Advisor

## Context

Design system versioning is a persistent source of team friction. Breaking changes are called minor because they "just affect two components." Minor improvements trigger unnecessary major bumps because someone worries about change. And the reasoning is never written down, so every release prompts the same debate.

This skill removes the subjectivity by applying a consistent classification framework to every change, then generating a changelog entry and reasoning that the team can trust. When the next release ships, there's a record of why it was a major and what consumers need to change.

## Steps

### 1. Accept and Classify Input

Accept input in any form: git diff output, PR description, a list of changes in natural language, or direct conversation about planned changes.

For each change, classify it into exactly one category:

- **Breaking (→ major):** removed prop/component/token, renamed API surface, changed default behaviour, changed type signature, removed CSS custom property, changed token value that consumers depend on, removed variant or variant option, removed CSS class or changed its selector specificity
- **Minor (→ minor):** new prop, new component, new token, new variant, added optional parameter, new CSS custom property, expanded type union, new variant option, added optional CSS class without removing existing classes
- **Patch (→ patch):** bug fix (fix for unintended behaviour), documentation update, internal refactor with no API change, dependency update, performance improvement with no API change

Be strict about classifications. Misclassifying a breaking change as a patch or minor is worse than over-bumping. If you are unsure, err toward breaking.

### 2. Determine the Semver Bump

The highest-severity change wins. If there is one breaking change and five patches, the bump is major. If there are five minors and zero breaking changes, the bump is minor.

Document the change count by type (X breaking, Y minors, Z patches) so the team sees the composition of the release. Example: "This release includes 1 breaking change, 3 new features (minors), and 2 bug fixes (patches). Bump: major."

### 3. Flag Edge Cases

Design systems have scenarios that don't fit standard semver cleanly. Identify and resolve them:

- **Breaking changes disguised as fixes:** A change labeled "bug fix" but that actually changes component behaviour (e.g., "fixed Button to now require an onClick handler"). This is breaking, not a patch. Reclassify.

- **Pre-1.0 rules:** If the version is 0.x.x, semver says breaking changes increment minor (0.4.0 → 0.5.0), not major. Do not jump to 1.0 unless explicitly planned. Apply this rule.

- **Deprecation-only releases:** A release that deprecates a prop but does not remove it is minor (deprecation is additive). The removal is breaking and happens in a later major bump. Example: "@deprecated Use newProp instead" on oldProp in v2.4.0 is minor; removing oldProp in v3.0.0 is major.

- **Peer dependency changes:** Changes to peer dependencies (e.g., "now requires React 18+", "drops support for Node 14") are often breaking and frequently miscategorised as patches. Reclassify if necessary.

- **CSS specificity changes:** A change that keeps class names but increases specificity (e.g., `.button` becomes `.button-group .button`) can be breaking even if the API surface didn't change. It breaks overrides. Treat as breaking if consumers rely on specificity.

- **Token value changes:** If a token value changes (e.g., color-primary from #0047AB to #0052CC) and consumers snapshot values in their own code rather than always referencing the token, this is breaking. Advise consumers to always reference tokens, not values, but treat as breaking if value changes.

Document which edge cases apply to this release, even if the answer is "none apply."

### 4. Generate Changelog Entry

Produce a changelog entry in markdown format, organised by category. This should be copy-paste-ready for CHANGELOG.md:

```
## [X.Y.Z] - YYYY-MM-DD

### Breaking Changes
- **ComponentName:** Removed prop `oldProp`. Use `newProp` instead. [migration: change `oldProp={value}` to `newProp={value}`]
- **TokenName:** Value changed from `#0047AB` to `#0052CC`. Update refs if you snapshot values.

### Features
- **ComponentName:** Added new variant `outline`. Use `variant="outline"` on Button.
- **TokenName:** New token `color-secondary-light` for lighter secondary backgrounds.

### Fixes
- **ComponentName:** Fixed Button to correctly apply icon spacing in all variants.
- **TokenName:** Fixed opacity value for `color-disabled` to meet WCAG contrast ratio.

### Internal
- Refactored token build pipeline for 30% faster compilation.
- Updated development dependencies.

### Deprecations
- **ComponentName:** Prop `oldSize` is deprecated. Use `size` instead. Deprecation removal planned for v4.0.0.
```

Keep descriptions to one line per item. Use [migration: ...] notation for breaking changes to highlight what consumers must change.

### 5. Generate Migration Notes for Breaking Changes

For every breaking change, include migration guidance. Format:

```
**Migration: ComponentName prop change**

Before (v2.x):
```jsx
<Button oldProp="value" />
```

After (v3.0):
```jsx
<Button newProp="value" />
```

Rationale: oldProp was confusing because it only applied in certain states. newProp is clearer and works in all states.
```

Do not assume users understand why the change was necessary. Explain the reason; it builds confidence that the change was deliberate.

### 6. Generate Decision Record Snippet (for major bumps only)

If the bump is major, offer to generate a decision record snippet in the format of the decision-record skill. Provide a template that the team can fill in:

```
## Decision: Version X.Y.Z (Major Release)

**Date:** YYYY-MM-DD
**Bump reason:** [1 sentence]
**Breaking changes:** [numbered list]
**Impact:** [who is affected, how many consumers]
**Rollout plan:** [immediate, phased, beta period, etc.]
**Communication:** [how will consumers learn about this]
```

Do not write the full decision record — that is the decision-record skill's job. Provide the skeleton so the team has a prompt.

## Quality Checks

1. **Breaking changes correctly identified even when described as "fixes" or "improvements."** Read the change carefully. If behaviour changes, default changes, type signature changes, or something is removed, it is breaking. Do not trust the PR author's classification.

2. **Pre-1.0 semver rules applied if version is 0.x.x.** If bumping from 0.4.0 and there is a breaking change, the new version is 0.5.0, not 1.0.0 (unless the team explicitly plans the v1 release).

3. **Changelog entry can be copy-pasted into a CHANGELOG.md without editing.** It should be complete, properly formatted, and ready to go. No "[FILL IN DESCRIPTION]" placeholders. Every breaking change has a migration note.

4. **Migration notes included for every breaking change.** Before/after code examples, one per breaking change. Explain the rationale so consumers understand why the change happened.

5. **Edge cases section addressed, even if none apply.** At the end of the recommendation, include a section: "Edge cases: [none identified]" or "Edge cases: breaking change disguised as fix (reclassified), deprecation-only release (minor bump applied)." Show your work.

## Small-System Note

For releases with fewer than 5 changes, the classification and changelog output are the same. The structure doesn't change; the volume is lower. Still apply all quality checks — a small release with a breaking change is still major.
