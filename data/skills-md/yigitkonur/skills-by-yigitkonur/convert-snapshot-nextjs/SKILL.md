---
name: convert-snapshot-nextjs
description: Use skill if you are converting saved HTML snapshots into buildable Next.js pages with self-hosted assets and extracted styles.
---

# Snapshot to Next.js

Convert saved HTML snapshots into grounded Next.js App Router builds. Treat the snapshot as source code, not inspiration: extract first, rebuild from extracted values, then prove the rebuilt page matches.

## Use this skill when

- Input is a saved snapshot: `.html` + companion `_files/` folders, SingleFile export, or an unpacked offline site capture.
- The user wants to rebuild, recreate, convert, clone, scaffold, or extract a saved site into Next.js.
- Fidelity matters more than speed or creative redesign.

## Do not use this skill when

- The only source is a live URL, screenshot, PDF export, Figma design, or loose design idea.
- The task is general Next.js UI coding with no offline snapshot to parse.
- The goal is a redesign, simplification, or "same vibe" rewrite instead of faithful reconstruction.

## Setup

| Key | Value |
|---|---|
| **Output location** | `{page}-nextjs/` sibling to snapshot dir |
| **Naming** | kebab-case everywhere (files, CSS classes, variables) |
| **Minified CSS warning** | Snapshot CSS may be minified (no trailing `;` before `}`). All grep patterns in references use `[^;}]+` to handle this — do not simplify to `[^;]+`. |

## Start with these decisions

| Situation | Action |
|---|---|
| `.html` + `_files/` folders present | Primary mode. Extract from external CSS, JS, and assets. |
| `.html` with inline `<style>` blocks but no `_files/` | SingleFile fallback. Extract from inline styles and document any reduced confidence. |
| `package.json` + source repo but no saved snapshot | Fallback mode only. Read source directly, but keep the same grounding rules. |
| Request says "extract", "document", "design system", or "tokens" | Stop at Waves 0–2 unless the user explicitly asks for a build. |
| Request says "rebuild", "recreate", "convert", "clone", or "pixel-perfect" | Run Waves 0–4. |
| Snapshot is very large or spans many page types | Group pages by type, finish each wave completely, then expand scope. |
| Request is ambiguous | Default to extraction-first (Waves 0–2). Do not assume a full rebuild. |

Read `references/input-output-spec.md` for full input detection, output trees, and ambiguity handling.

## Operating contract

1. **Extract before build.** No Wave N+1 starts until all Wave N signals exist. Read `references/wave-pipeline.md`.
2. **Parse, don't guess.** Every value must trace to snapshot CSS, HTML, or documented behavior. Read `references/principles-and-rules.md`.
3. **Build from extracted values only.** `tokens.ts`, `tailwind.config.ts`, `globals.css`, and components must trace to Wave 0/1 extraction; mark incomplete values `UNVERIFIED` instead of substituting Tailwind defaults.
4. **Self-host everything.** Fonts, images, icons, and other assets must end up local. No CDN fonts. No remote image URLs.
5. **Write signals last.** `done.signal` and `foundation-ready.signal` are written only after verification passes.
6. **If something cannot be grounded, mark it `UNVERIFIED`.** Honest gaps are allowed. Invented values are not.

## Do this / not that

| Do this | Not that |
|---|---|
| Use CSS Module prefixes, semantic tags, and real selector boundaries to identify sections | Infer sections from generic `<div>` nesting alone |
| Search across all `_files/*.css` together and deduplicate shared files | Read minified CSS by eye or treat each hashed CSS file as an isolated system |
| Carry exact source values through Wave 0 → Wave 4 | Round, normalize, or replace values because they look "close enough" |
| Download remote assets during Wave 0 and map them to local paths | Leave Google Fonts or CDN assets in the final build |
| Implement only documented hover, focus, animation, and responsive behavior | Invent motion, states, or breakpoint behavior not found in source |
| Keep the build dependency set limited to the scaffold rules in `references/system-template.md` | Add UI, icon, animation, or font packages for convenience |

## Required sequence

| Phase | Goal | Required reference | Primary outputs | Gate |
|---|---|---|---|---|
| Wave 0 | Per-page exploration and deobfuscation | `references/foundations-agent.md` | `wave0/{page}/exploration.md`, `deobfuscated.css`, `behavior-spec.md`, `assets/` | `wave0/{page}/done.signal` |
| Wave 1 | Unified design soul by page type | `references/sections-agent.md` | `wave1/{group}/design-soul.md`, `token-values.json`, `responsive-map.md` | `wave1/{group}/done.signal` |
| Wave 2 | Self-contained page build briefs | `references/section-template.md` | `wave2/{page}/agent-brief.md` | `wave2/{page}/done.signal` |
| Wave 3 | Next.js scaffold and design-system foundation | `references/system-template.md` | `nextjs-project/`, `wave3/foundation-brief.md`, `traceability-matrix.md` | `wave3/foundation-ready.signal` |
| Wave 4 | Page builds and fidelity checks | `references/wave-pipeline.md` + `references/quality-checklist.md` | route files, page components, copied public assets | final verification passes |

If the user only asked for extraction or documentation, stop after the appropriate wave instead of pushing to build.

## Asset and style handling rules

- Extract CSS custom properties, `@font-face`, `@media`, `@keyframes`, and transition values before touching the build.
- Treat Wave 1 `token-values.json` as the source of truth for tokens; Wave 3 only re-expresses those exact values in `tokens.ts`, Tailwind config, and `globals.css`.
- Copy fonts to `public/assets/fonts/`, images to `public/assets/images/...`, and icons to `public/assets/icons/` or inline them only when the source uses inline SVG.
- Preserve exact typography, spacing, gradients, shadows, radii, z-index, and breakpoint values.
- Preserve responsive behavior from real source media queries; do not substitute Tailwind defaults if the snapshot uses different breakpoints.
- Preserve extracted interaction behavior, but only if it can be grounded from CSS or documented JS behavior specs.
- For inline `style=""` attributes or JS-driven states, extract the base CSS and the trigger separately; do not freeze computed runtime values into guessed static styles.

## Recovery rules

- **Missing `_files/` folder:** treat as SingleFile mode if inline CSS exists; otherwise full reconstruction may be blocked.
- **Missing assets or remote-only assets:** download them during extraction and record original → local path mapping.
- **Missing fonts:** Check `<link>` tags for Google Fonts / Typekit URLs. Download font files to `public/assets/fonts/` and create `@font-face` declarations. If URL is unreachable, substitute with a system font stack and add `/* TODO: replace with original font */`.
- **External JS (analytics, chat widgets):** Do NOT embed third-party scripts. Add a `{/* TODO: re-add [service] script */}` comment in `layout.tsx`.
- **Missing CSS or JS evidence for a value or behavior:** mark it `UNVERIFIED` and avoid inventing the implementation.
- **Incomplete snapshot:** continue extraction where possible, but do not claim a pixel-perfect rebuild if core layout, type, or asset data is missing.
- **Shared headers, footers, or components across pages:** deduplicate them intentionally; note page-specific overrides rather than re-documenting the whole component each time.

## CLI-verifiable acceptance criteria

Every conversion must pass these checks before declaring success:

```bash
# Type-check passes
npx tsc --noEmit

# Production build succeeds
npm run build

# No UNVERIFIED comments remain
grep -r 'UNVERIFIED' app/ components/ lib/ styles/ && echo "FAIL: unverified values" || echo "PASS"

# No external URLs leak into components
grep -rE 'https?://' components/ | grep -v '// original:' && echo "FAIL: external URLs" || echo "PASS"
```

## Verification before claiming completion

- **After extraction (before Wave 3):** run the grounding test and cross-reference checks from `references/quality-checklist.md`.
- **Before `foundation-ready.signal`:** verify extracted CSS custom properties and shared tokens are accounted for, allowed dependency set, self-hosted fonts/assets, traceability matrix, and clean TypeScript/build checks.
- **Before final completion:** compare source vs build at 1280px, 768px, and 375px; confirm zero external network requests; run clean install/build verification.
- If any verification fails, fix it before writing the completion signal or calling the build done.

## Reference map

| Need | Read |
|---|---|
| Input detection, output trees, ambiguous requests | `references/input-output-spec.md` |
| Hard rules: grounding, section identification, zero invention | `references/principles-and-rules.md` |
| Wave 0 extraction method | `references/foundations-agent.md` |
| Wave 1 design-soul extraction | `references/sections-agent.md` |
| Wave 2 build-brief format | `references/section-template.md` |
| Wave 3 scaffold, token wiring, allowed deps | `references/system-template.md` |
| Full wave orchestration and gates | `references/wave-pipeline.md` |
| Acceptance criteria, fidelity tests, and failure modes | `references/quality-checklist.md` |
| Section-type and anatomy heuristics | `references/website-patterns.md` |

Read only the references needed for the current wave. Keep the top-level skill focused on decisions, sequencing, and guardrails; keep implementation detail in the reference files.
