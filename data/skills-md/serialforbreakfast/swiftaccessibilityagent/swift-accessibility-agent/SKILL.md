---
name: swift-accessibility-agent
description: Use this skill when reviewing or updating SwiftUI, UIKit, tvOS, macOS, or visionOS UI for accessibility. It selects platform-specific guidance, preserves accessibility semantics, and outputs citations plus verification steps.
---

# Swift Accessibility Agent

## Use This Skill For

- Accessibility review of Apple-platform UI.
- Accessibility-aware implementation updates.
- Platform/framework-specific guidance selection.

## Task Workflows

### Review Existing Accessibility Implementation

1. Identify the changed UI surface and platform/framework.
2. Load one backlog file for that surface.
3. Load one or two matching guideline files.
4. Output findings with guideline IDs, citation IDs, and verification steps.

### Improve Existing UI Accessibility

1. Load the matching backlog and current guideline file(s).
2. Propose concrete semantic fixes (label/value/hint/role/actions).
3. Include rationale tied to Tier-1 citations.
4. Provide verification plan (Inspector + manual flow; optional XCUITest hook).

### Implement New Accessible UI

1. Select guideline topics before implementation.
2. Prefer native controls and explicit semantics.
3. Include interop ownership notes for mixed stacks.
4. Return implementation plus verification expectations.

## Internal Routing (As Needed)

Load these only when task scope is ambiguous or multi-platform:

1. `references/manifests/security-policy.json`
2. `references/manifests/axes.json`
3. `references/manifests/core.json`
4. `references/manifests/routes.json`

## Then Select

- Platform: `ios`, `tvos`, `macos`, `visionos`
- Framework: `swiftui`, `uikit`, `appkit`, or mixed interop
- Task type: implement, review, triage, or guideline authoring

## Load Only What Is Needed

After route selection, load only:

1. One platform backlog:
   - `references/swiftui/guidelines/topic-backlog.md`
   - `references/uikit/guidelines/topic-backlog.md`
   - `references/tvos/guidelines/topic-backlog.md`
   - `references/macos/guidelines/topic-backlog.md`
   - `references/visionos/guidelines/topic-backlog.md`
2. One or two topic guideline files tied to the task.
3. Required testing docs:
   - `references/testing/inspector-audit-checklist.md`
   - `references/testing/manual-test-scripts.md` (or platform equivalent)
   - `references/testing/xcuitest-hooks.md` when automation is relevant
4. Core references only when needed:
   - `references/core/sources/registry.md`
   - `references/core/taxonomy/semantics-checklist.md`
   - `references/core/templates/guideline-template.md`

## Operating Rules

1. Treat Tier-1 Apple sources as platform truth.
2. Keep semantics explicit for interactive UI:
   - label
   - value
   - hint
   - role/traits
   - actions
3. Prefer native controls and document interop ownership when mixed frameworks are used.
4. Keep guidance testable with concrete verification steps.

## Output Requirements

For review tasks:

- Findings or confirmations tied to guideline IDs.
- Rationale with citation IDs.
- Verification steps (Inspector + manual flow; optional XCUITest hook).

For implementation tasks:

- Concrete code or content changes.
- Why the change aligns with selected guideline(s).
- Verification plan with expected outcomes.
