---
name: better
description: Improve and implement interfaces across accessibility, layout, writing, typography, colors, and UI polish. Mandatory after building or changing any screen. Use when interface work finishes or a screen or flow must be better, clearer, or more polished; audit only when explicitly requested.
user-invocable: true
---

Improve one resolved screen, flow, feature, or product interface. Default to implementation: inspect, identify the concrete fixes, apply them, and verify the result in the same task. Use the domain guides for design principles and checks; this entrypoint owns workflow, authorization, severity, and reporting.

This is the required last pass for any interface work: run it after building or changing a screen, even when nobody asks. Treat `/better` (`$better` in Codex), "better this UI", and "make this smarter" as requests to implement. Do not stop after findings, propose work instead of doing it, or ask whether to proceed. Ask only for essential missing information that cannot be resolved from context; continue independent work while waiting. Honor explicit "audit", "review only", "read-only", "plan only", or "no edits" requests as non-mutating boundaries.

For an explicit review of a branch, PR, commit range, or uncommitted changes, review only the interface those changes touch, without editing. A version-control reference in an improvement request identifies the implementation scope; it does not turn the request into a read-only review or require another invocation.

State the scope briefly. Inspect one complete flow at a time; continue through the requested scope rather than silently dropping work. Cover empty, loading, error, and narrow-width states where they exist. Keep a concrete finding list as implementation scope; apply all actionable in-scope fixes, not only HIGH findings. Cap reported findings at 15, not the work performed.

Identify the stack, tokens, viewports, and preview command. Read project interface docs (`CONTRIBUTING.md`, `AGENTS.md`, design-system, Storybook). A documented convention does not retire a finding; report a shared-token cause once against that source.

Load the available guides in this order, identify the fixes, then implement:

1. `references/accessibility/guide.md`
2. `references/layout/guide.md`
3. `references/writing/guide.md`
4. `references/typography/guide.md`
5. `references/colors/guide.md`
6. `references/ui/guide.md`
7. `references/design-system-rules.md` for product screens (lists, settings, modals, detail pages) and the screenshot loop.

Take principles, references, and verification checks from each guide. This file owns severity, ranking, cap, and format. A missing guide is `Not reviewed` with its path; do not recreate its rules. Assign an overlapping issue to the owner of the underlying rule and report it once.

Cite `path/to/file:line` and show the current implementation. Do not report a code finding from appearance alone or a visual finding from source alone when runtime decides the result. Run the project's safe checks; a check you cannot run is `Not verified`.

Contrast standard is WCAG 2.2 AA everywhere, and it overrides any other threshold in the guides: 4.5:1 for body text, 3:1 for large text (≥24px, or ≥18.5px bold) and for UI components, icons and focus indicators. Measure each rendered pair with `node <skill-dir>/scripts/contrast.mjs <fg> <bg>` (hex, rgb, hsl or oklch; `<skill-dir>` is this skill's folder) and report the measured ratio, never an estimate. A failing pair is fixed by changing lightness, keeping the hue, then remeasured.

`HIGH` blocks a task, misleads, hides content, risks data loss, or is a confirmed trigger: unnamed control, missing focus, pointer-only path, ignored `prefers-reduced-motion`, clip at 320px or 200% zoom, failing contrast, color-only meaning, unconfirmed destructive action, unreachable truncated content, undisclosed overflow, error with no recovery, semantic color used against its meaning, motion-only state. `MEDIUM` harms comprehension, efficiency, adaptability, or consistency. `LOW` is isolated polish. Rank triggers first, then reach. Prefer delete → platform → existing token → correct value → add. One root cause is one row. Never pad to reach the cap.

Implement with existing components and tokens, preserve unrelated work, and re-verify after changes. When a browser is available, finish with the screenshot loop from `references/design-system-rules.md`: capture light and dark, compare side by side with the reference, review bluntly with vision, fix and repeat until no structural issue remains. Distinguish verified behavior from untested states and unrelated check failures. An implementation request does not itself authorize deployment, sending messages, or other external operations.

For implementation, return a concise account of what changed, checks and remaining blockers, with a rendered preview when available. Do not offer to implement work that is already in scope. Use `references/review-format.md` for explicit review-only requests or when a detailed review is requested alongside implementation. Finish when the requested fixes and feasible verification are complete, or explain the concrete blocker.
