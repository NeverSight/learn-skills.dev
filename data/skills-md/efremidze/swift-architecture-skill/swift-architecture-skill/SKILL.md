---
name: swift-architecture-skill
description: Agent Skill for Swift architecture design and implementation patterns, with architecture-specific playbooks and review checklists. Use when designing new features, refactoring existing modules, reviewing pull requests, or debugging maintainability issues in SwiftUI/UIKit projects and you need concrete guidance for MVVM, MVI, TCA, Clean Architecture, VIPER, or Reactive patterns.
---

# Swift Architecture Skill

## Overview

Use this skill to pick the best Swift architecture playbook for SwiftUI/UIKit codebases and apply it to the user’s task.

## Workflow

### Step 1: Analyze the Request Context

Before selecting an architecture, capture:
- task type (new feature, refactor, PR review, debugging)
- UI stack (SwiftUI, UIKit, or mixed)
- scope (single screen, multi-screen, app-wide)
- existing conventions to preserve

### Step 2: Select the Architecture

If the user explicitly names an architecture, treat it as the initial candidate and run a fit check before committing:
- validate against UI stack fit (SwiftUI/UIKit/mixed), state complexity, effect orchestration needs, team familiarity, and existing codebase conventions
- if it fits, proceed with the requested architecture
- if it mismatches key constraints, explicitly explain the mismatch and recommend the closest-fit alternative from `references/selection-guide.md`
- if the user still insists on a mismatched architecture, proceed with a risk-mitigated plan and state the risks up front

When no architecture is named, load `references/selection-guide.md` and infer the best fit from stated constraints (state complexity, team familiarity, testing goals, effect orchestration needs, and framework preferences). Explain the recommendation briefly.

Architecture reference mapping:
- MVVM → `references/mvvm.md`
- MVI → `references/mvi.md`
- TCA → `references/tca.md`
- Clean Architecture → `references/clean-architecture.md`
- VIPER → `references/viper.md`
- Reactive → `references/reactive.md`

### Step 3: Analyze Existing Codebase (When Applicable)

When code already exists:
- detect current architecture and DI style
- note concurrency model (async/await, Combine, GCD, mixed)
- align recommendations to local conventions

### Step 4: Produce Concrete Deliverables

Read the selected architecture reference and convert its guidance into deliverables tailored to the user's request:

- **File and module structure**: directory layout with file names specific to the feature
- **State and dependency boundaries**: concrete types, protocols, and injection points
- **Async strategy**: cancellation, actor isolation, and error paths
- **Testing strategy**: what to test, how to stub dependencies, and example test structure
- **Migration path** (for refactors): incremental steps to move from current to target architecture
- **UI stack adaptation**: where SwiftUI and UIKit guidance should differ for the chosen architecture

### Step 5: Validate with Checklist

End with the architecture-specific PR review checklist from the reference file, adapted to the user's feature.

## Output Requirements

- Keep recommendations scoped to the requested feature or review task.
- Prefer protocol-based dependency injection and explicit state modeling.
- Flag anti-patterns found in existing code and provide direct fixes.
- Include cancellation and error handling in all async flows.
- For explicit architecture requests, include a short fit result (`fit` or `mismatch`) with 1-2 reasons.
- For mismatch cases, include one closest-fit alternative and why it better matches the stated constraints.
- When writing code, include only the patterns relevant to the task — do not dump entire playbooks.
- Treat reference snippets as illustrative by default; add full compile scaffolding only if the user asks for runnable code.
- Ask only minimum blocking questions; otherwise proceed with explicit assumptions stated up front.
- When reviewing PRs, use the architecture-specific checklist and call out specific violations with line-level fixes.
