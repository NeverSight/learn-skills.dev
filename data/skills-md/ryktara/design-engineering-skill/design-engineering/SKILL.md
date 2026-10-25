---
name: design-engineering
description: Context-first UI/UX design engineering for real codebases across web, mobile, desktop (WinUI/WPF/Avalonia), Android TV / tvOS / IPTV, and kiosks. Use when creating or redesigning screens, pages, components, or design systems; auditing or refactoring existing UI; fixing responsive, accessibility, typography, colour, spacing, motion, or DPAD/remote-focus problems; making multiple brands structurally distinct; or implementing a screenshot. Inspects the project first, derives navigation/layout/density before visual style, and verifies by rendering. Not for backend, database, infrastructure, or non-visual bugs.
---

# Design Engineering

Purpose: understand product, users, environment, input modality, platform, constraints, and the existing implementation; derive a design direction from those signals; implement it in the project's own conventions; verify by rendering. Visual style is decided last, never first.

All commands below use `${CLAUDE_SKILL_DIR}` (this directory). Scripts are Python 3 stdlib only; on Windows use `python`, elsewhere `python3` if needed.

## 1. Classify the task

Pick the mode(s) that fit; scale effort to the size of the change (a one-line CSS fix does not need the full loop).

| Mode | Typical request | Load |
|---|---|---|
| create | new screen / page / component / flow | design-reasoning, platform file, stack file |
| design-system | tokens, type scale, colour roles, theming, dark mode | color, typography, layout-density, motion |
| audit / review | "what's wrong", review against criteria | review-rubric, accessibility, anti-generic |
| refactor / polish | improve without breaking; "looks unprofessional/generic" | anti-generic, layout-density, typography |
| accessibility | WCAG, screen readers, keyboard, focus, contrast | accessibility (+ platform file) |
| responsive | breakpoints, overflow, window sizes, orientation | responsive |
| brand | several brands / white-label / distinct identities | brand-differentiation |
| reconstruct | screenshot or reference image → code | screenshot-reconstruction |

Build the requirements contract when the request is more than a one-line fix; it is the single source of task/platform/input/constraint signals for every later step and reports what is MISSING:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/advise.py" requirements "<request>" [--project .design-inspect.json] [--pretty] [--explain]
```

Exit codes: 0 CONFIDENT, 3 PARTIAL, 4 AMBIGUOUS (conflicting platforms or contradictory instructions such as "keep the navigation but redesign the information architecture": resolve before designing), 5 ABSTAIN (out of scope).

The contract also reports `scope` (task domain: UI_DESIGN / UI_INTERACTION / UI_ACCESSIBILITY / UI_IMPLEMENTATION versus FRONTEND_RUNTIME / BACKEND / DATA / INFRASTRUCTURE / BUILD_TOOLING, with `in_scope`, a reason and the nearest supported UI task), `mode_evidence` (why the modes were chosen: existing-UI language, problem statement, explicit fix or build verb), and `change_budget`: **low** (polish, audit, review, accessibility: keep the system), **moderate** (refactor, fixes after a diagnosis, additions inside an existing app), **high** (redesign, brand), **greenfield** (new product). A UI-adjacent technical prompt ("why does my component re-render") is out of scope even if the skill was activated; say so and hand back the technical part. A technical cause with a user-visible symptom ("scrolling freezes", "screen reader announces the wrong count") is in scope for its UX side.

## 2. Inspect the project before deciding anything

Never redesign from assumptions when the repository can answer. For any work inside an existing codebase:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/inspect_project.py" <project-root> --out .design-inspect.json
```

It reports (KNOWN vs INFERRED) the stack, platforms, UI libraries, CSS architecture, tokens/theme files, fonts, icons, routing, component directories, breakpoints, accessibility and focus/DPAD handling, tests, i18n, product hints, and the **design context** already present: navigation topology (left rail, top bar, bottom tabs, menu bar, TV rails, hub-and-spoke…), theme polarity (light-first, dark-first, dual-theme with its default), surface language (bordered-flat, elevated, flat-tonal), radius language, spacing base, typography family and features, component library. Each carries KNOWN / INFERRED / UNKNOWN with the evidence; regex detection never proves UX semantics, so read the shell/theme files it points at and correct it when it is wrong. Then read the files it points at (theme/tokens, the component directory, one representative screen). Existing conventions win: reuse → extend → compose → new primitive, in that order. Never install a UI framework to build one screen. Delete `.design-inspect.json` when done unless the user wants it kept.

Ledger every decision input as **KNOWN** (observed in repo or request), **INFERRED** (reasonable from evidence), or **MISSING** (ask only if it materially changes the result and cannot be derived). Do not invent brand guidelines, users, devices, or design-system rules.

## 3. Get the guidance bundle, then the direction

For any task beyond a one-line fix, fetch the guidance bundle. It derives the task's **concerns** (REQUIRED / RECOMMENDED / OPTIONAL: structure, navigation, component, interaction, accessibility, content, data-display, adaptive, states, feedback, performance, privacy, environment, brand, motion, anti-pattern) from the requirements, then selects the smallest set of records that covers them: **core** (what to build) plus **guardrails** (rules and anti-patterns that must hold). Bundles are 5–8 records; every item says which concern and concept it was selected for.

```bash
python "${CLAUDE_SKILL_DIR}/scripts/advise.py" guidance "<request>" --project .design-inspect.json [--explain] [--json]
```

The bundle is chosen to cover the **expected concepts** derived from the requirements (required / recommended concept ids with reasons, e.g. `table.inline_edit` requires keyboard navigation, visible focus and validation), not only broad concerns; each record shows `covers: …`. Read `metrics.uncovered_required_concerns` and `uncovered required concepts`: those are the things the knowledge base could not back for this context, so decide them from the references and say so. `coverage_per_1k_tokens` and `contaminated` show whether the bundle is compact and on-task. `status: PARTIAL` means exactly that. Guardrails are not optional; a guardrail you cannot honour needs a stated reason.

For substantial create / redesign / design-system / brand work, also get the visual direction (it consumes the same bundle for its guardrails):

```bash
python "${CLAUDE_SKILL_DIR}/scripts/advise.py" direction "<request>" --project .design-inspect.json [--brand NAME] [--out brand-a.json]
```

Output: the KNOWN/INFERRED/MISSING ledger, one choice per slot (navigation, layout, density, surface, cards, typography, colour, motion, focus, CTA, imagery, icons, metadata) with the signals that selected it, a **compatibility table** (per slot: preserved / changed / new, with the reason), the change budget, preservation metrics, the bundle's core guidance, its guardrails grouped (interaction, accessibility, platform, states, feedback, privacy/environment, anti-patterns), and a design fingerprint. For an existing application the direction preserves the detected navigation, theme polarity, typography and surface language by default; a slot changes only when the change budget allows it, when an accessibility or platform requirement forces it (stated in the reason), or when the request asks for a redesign or a brand. `validation.violations` lists any unjustified structural change. Add `--explain` to see alternatives and rejected options. Treat it as evidence, not a verdict: reconcile every slot with what the repository already does.

For a focused lookup or to debug why something was or was not selected (`search` is the raw ranked list without concern coverage):

```bash
python "${CLAUDE_SKILL_DIR}/scripts/advise.py" search "<question>" [-k 5] [--kind rule|pattern|component|chart|antipattern|direction] [--project .design-inspect.json] [--explain]
python "${CLAUDE_SKILL_DIR}/scripts/advise.py" show <record-id>
```

Retrieval consumes the requirements contract: TV requests never return hover/pointer patterns, "no cards" / "no rails" exclude those patterns, "do not change navigation" preserves the navigation slot, environment-specific rules (outdoor, shared device, offline) appear only with evidence, and problem statements ("users keep missing…", "looks cramped") are treated as audit/polish work on existing UI, not as a request to build something new. `status: ABSTAIN` or an empty result means no verified match; say so and fall back to the references rather than presenting a guess as knowledge. Statuses describe observable coverage (CONFIDENT = every required concern covered and platform known; PARTIAL = something required is uncovered or the platform is only inferred), not a probability of being right. A direction with `validation.violations` must not be used as-is.

Decision order (do not skip ahead): task and user → environment and input → density and navigation → layout and components → states → then typography, colour, surfaces, motion. See [references/design-reasoning.md](references/design-reasoning.md).

## 4. Load only what the task needs

Read the relevant file(s); each is self-contained and one level deep.

- Reasoning and craft: [design-reasoning.md](references/design-reasoning.md), [anti-generic.md](references/anti-generic.md), [layout-density.md](references/layout-density.md), [typography.md](references/typography.md), [color.md](references/color.md), [motion.md](references/motion.md), [components.md](references/components.md), [data-viz.md](references/data-viz.md), [performance.md](references/performance.md)
- Constraints and checks: [accessibility.md](references/accessibility.md), [responsive.md](references/responsive.md), [review-rubric.md](references/review-rubric.md), [verification.md](references/verification.md)
- Special modes: [brand-differentiation.md](references/brand-differentiation.md), [screenshot-reconstruction.md](references/screenshot-reconstruction.md)
- Platforms (always load the one that applies): [web](platforms/web.md), [mobile](platforms/mobile.md), [tv](platforms/tv.md), [desktop](platforms/desktop.md), [kiosk](platforms/kiosk.md)
- Stacks (load the detected one): [react](stacks/react.md), [nextjs](stacks/nextjs.md), [vue](stacks/vue.md), [nuxt](stacks/nuxt.md), [svelte](stacks/svelte.md), [angular](stacks/angular.md), [astro](stacks/astro.md), [html-css](stacks/html-css.md), [tailwind](stacks/tailwind.md), [shadcn](stacks/shadcn.md), [compose](stacks/compose.md), [compose-tv](stacks/compose-tv.md), [swiftui](stacks/swiftui.md), [flutter](stacks/flutter.md), [react-native](stacks/react-native.md), [winui](stacks/winui.md), [wpf](stacks/wpf.md), [avalonia](stacks/avalonia.md)

A TV screen is not an enlarged desktop layout; a phone screen is not a shrunk one. When the platform is TV, kiosk, or desktop-native, the platform file overrides generic web habits.

## 5. Deterministic checks (use them instead of estimating)

```bash
python "${CLAUDE_SKILL_DIR}/scripts/tokens.py" contrast "#1B1F24" "#F7F8FA"        # WCAG ratio + pass/fail
python "${CLAUDE_SKILL_DIR}/scripts/tokens.py" validate tokens.json --platform web|mobile|desktop|tv
python "${CLAUDE_SKILL_DIR}/scripts/tokens.py" scale --platform tv --base 24 --ratio 1.25
python "${CLAUDE_SKILL_DIR}/scripts/tokens.py" init > tokens.json                   # semantic-role skeleton
python "${CLAUDE_SKILL_DIR}/scripts/fingerprint.py" compare brand-a.json brand-b.json   # brand structure check
python "${CLAUDE_SKILL_DIR}/scripts/validate_skill.py"                             # after editing this skill
```

Tokens are semantic roles (`color.bg.canvas`, `color.text.primary`, `color.action.primary-hover`, `color.focus.ring`, `color.feedback.error`…), validated per theme for contrast, state completeness, and role sanity. Never quote a contrast ratio you did not compute.

## 6. Implement

- Build in the project's stack and component model; wire new values through its token/theme layer, not inline hex.
- Every substantial screen: purpose, primary action, information hierarchy (one focal point), navigation, secondary information, density, empty/loading/error/partial states, hover/focus/pressed/selected states for the input model, responsive or adaptive behaviour, accessibility semantics, visual identity. Enumerate states before coding.
- Accessibility is a constraint during design, not a checklist after: contrast, target size, keyboard/DPAD operability, visible focus, labels, reduced motion, text scaling.
- Justify each visual device (gradient, glass, card, pill, icon, shadow, animation) by function or by the brand system; the anti-generic reference lists what to remove by default.
- Do not break routes, state, API contracts, playback, auth, persistence, test ids, accessibility semantics, or existing input modes. Keep UI changes separate from unrelated backend edits.
- Charts: pick the form from the analytical question ([data-viz.md](references/data-viz.md)); a chart with no question is decoration.

## 7. Verify by rendering, then report

Compilation is not visual success. When a browser, emulator, simulator, screenshot tool, or computer-use is available: run the app, capture the representative viewports/devices (use the project's breakpoints; TV at its design frame; desktop at a small and a large window), look at the images, and check overflow/clipping, hierarchy, alignment, contrast, empty and loading states, focus visibility by tabbing or DPAD-ing through, and reduced motion. Fix what you see and re-capture. Details: [verification.md](references/verification.md) and [responsive.md](references/responsive.md).

For reviews, score against [review-rubric.md](references/review-rubric.md) and report defects with evidence (screenshot, measured ratio, element), not impressions.

Close with the material changes, the ledger of assumptions (INFERRED/MISSING), and anything left unverified because a tool was unavailable.

## Scope notes

- Skip this skill for backend logic, databases, infrastructure, build tooling, and non-visual bugs. If a request mixes both, use it only for the UI part.
- If other design skills are active (a project design system file such as DESIGN.md, a brand guideline, or a stack-specific design skill), the project's own files are the source of truth; this skill supplies reasoning, checks, and platform intelligence around them.
- Maintenance, installation, and usage examples: [docs/USAGE.md](docs/USAGE.md), [docs/MAINTENANCE.md](docs/MAINTENANCE.md), [docs/INSTALL.md](docs/INSTALL.md). Evaluations: `python "${CLAUDE_SKILL_DIR}/evals/run_evals.py"`.
