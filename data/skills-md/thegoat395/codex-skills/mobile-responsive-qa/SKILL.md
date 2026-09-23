---
name: mobile-responsive-qa
description: "Verify phone/tablet input and navigation flows."
---

# Mobile Responsive QA

Use this skill to catch mobile problems that make otherwise premium sites feel rushed.

## Workflow

1. Inspect the affected surface, relevant project scripts, target URL and available inspection tooling; reuse existing context.
2. Read [Mobile Responsive QA Guide](references/mobile-responsive-qa-guide.md) before claiming the site is ready.
3. Inspect affected phone/tablet navigation and input states: menu focus, touch affordances, virtual-keyboard occlusion, sticky controls, orientation and overflow where relevant. Distinguish emulation from real-device evidence.
4. Fix issues when they are in scope; otherwise record exact evidence and remaining risk.
5. Summarize commands, URLs, screenshots/checks, changed files, and what was not tested.

## Scoped execution

Apply the [shared web contract](../website-operating-rules/references/scoped-web-contract.md) once when execution crosses phases; reuse it if already read. Load only the specialist guidance relevant to the requested surface and deliverable.

## Scope and evidence

Record width emulation separately from real touch/device/virtual-keyboard evidence. Use `$responsive-visual-polish-qa` for broad breakpoint composition; do not claim real-device certification from emulation.
