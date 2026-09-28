---
name: design-catalogue
description: |
  Catalogue navigator for design-agent-skills. Lists available design skill stubs,
  matches user intent to the right stub, and routes to install and invoke.
  Use when the user wants to browse or find the right design skill.
triggers:
  - "what design skills"
  - "find a design skill"
  - "browse design skills"
  - "which skill for design"
  - "design skill for"
  - "show me design skills"
  - "what skills do you have"
das:
  category: meta
  type: navigator
  catalogue: true
---

# design-catalogue

Meta-skill for this catalogue. Activate when the user wants to browse, discover, or find
the right design skill — not when they've already named one.

## When to use

Activate when the user:
- Asks what design skills exist ("what skills do you have?", "show me design skills")
- Describes a problem but names no skill ("I want premium UI", "make it not look generic")
- Asks which skill fits a task ("what should I use for animations?", "which for good taste?")

Do **not** activate if the user already named a specific skill — route directly to that stub.

## How to respond

1. Present the relevant section of the catalogue index below
2. Recommend the best match with a one-line reason
3. Show the stub's install command for the match
4. Ask if they want to install and invoke it

> For `type:package` and `type:platform` stubs: show the `npx skills add` or per-agent
> install command from the stub. These must not be curl'd directly.

## Domain fast-path

When the user's intent is clearly within one domain, route directly to that domain catalogue
instead of scrolling the full index below:

| Domain | Route to | When |
|--------|----------|------|
| Motion, 3D, shaders, generative art | `motion-catalogue` | GSAP, Framer Motion, Three.js, Lottie, p5.js, shaders, video |
| Figma, design-to-code, tokens, platform suites | `figma-catalogue` | Figma skills, Stitch, design tokens, Anthropic/Vercel/Expo suites |
| Accessibility, WCAG, web performance | `accessibility-catalogue` | a11y audit, WCAG 2.2, Core Web Vitals, React quality |
| UI craft, visual design, brand, mobile | `design-engineering-catalogue` | Taste, color, typography, iOS/Android, brand identity |
| Slides, diagrams, data viz, PM, design review, copy | `content-catalogue` | Presentations, wireframes, charts, UX strategy, PM frameworks, UX writing, copywriting, user research |

## Catalogue index

### Design Engineering (opinionated UI taste)

| Skill | Best for |
|-------|----------|
| [`taste-skill`](../taste-skill/SKILL.md) | Premium, non-generic UI — variance, motion, density dials |
| [`impeccable`](../impeccable/SKILL.md) | 23 commands, Chrome extension, Live Mode browser iteration |
| [`emilkowalski-skill`](../emilkowalski-skill/SKILL.md) | Animation decision framework, easing curves, interaction principles |
| [`make-interfaces-better`](../make-interfaces-better/SKILL.md) | Polish: micro-interactions, typography details, visual refinement |
| [`ui-craft`](../ui-craft/SKILL.md) | 18 slash commands, anti-slop CLI, 3 style variants — deepest design engineering skill |
| [`frontend-design`](../frontend-design/SKILL.md) | 8 aesthetic anchors (Brutalist, Nordic, Cyberpunk…) with locked CSS tokens per theme |
| [`huashu-design`](../huashu-design/SKILL.md) | Magazine-grade typography, CSS Grid, animated prototypes, MP4 export |
| [`brand-design-md`](../brand-design-md/SKILL.md) | Fetches exact tokens for 62 world-class brands (Stripe, Linear, Apple…) at runtime |
| [`ai-graphic-design-skill`](../ai-graphic-design-skill/SKILL.md) | Maps 15 AI tools to design scenarios + 2025-26 Creative Director roadmap |
| [`logo-designer-skill`](../logo-designer-skill/SKILL.md) | Brand interview → 3-5 SVG concepts → PNG export 16px–2048px |
| [`distinctive-frontend`](../distinctive-frontend/SKILL.md) | 4 themed design systems (Cyberpunk, Brutalist, Vaporwave, Nordic) with staggered animations |
| [`design-for-ai`](../design-for-ai/SKILL.md) | CHECKER (7-category audit) + APPLIER (6-phase creation) dual-mode plugin |
| [`styleseed`](../styleseed/SKILL.md) | 69 design rules, 60+ brand skins (Toss, Stripe, Linear, Vercel…), 13 slash commands |
| [`awesome-design-skills`](../awesome-design-skills/SKILL.md) | 67-style aesthetic registry: glassmorphism, brutalism, bento, editorial, riso… |
| [`interaction-design`](../interaction-design/SKILL.md) | IxD principles, component states, micro-interactions, affordances, task flows — Norman + Tognazzini |
| [`format-storybook`](../format-storybook/SKILL.md) | Storybook story structure, template composition, controls, Chromatic, CSF patterns |
| [`localization-design`](../localization-design/SKILL.md) | RTL mirroring, per-language text expansion, non-Latin type, cultural color/icon traps |
| [`design-system-governance`](../design-system-governance/SKILL.md) | Ownership models, contribution lifecycle, semver contract, deprecation policy |

### Motion & Animation

| Skill | Best for |
|-------|----------|
| [`design-motion-principles`](../design-motion-principles/SKILL.md) | UI motion design: build components with purposeful motion or audit for AI-slop patterns — Emil Kowalski, Jakub Krehel, Jhey Tompkins lenses |
| [`algorithmic-art`](../algorithmic-art/SKILL.md) | Generative art with p5.js, flow fields, particle systems |
| [`shader-dev`](../shader-dev/SKILL.md) | GLSL shaders: ray marching, fluid simulation, WebGL effects |
| [`p5js-hermes`](../p5js-hermes/SKILL.md) | p5.js creative coding: noise, particles, GLSL, audio-reactive |
| [`remotion`](../remotion/SKILL.md) | Programmatic video with React |
| [`motion-design-skill`](../motion-design-skill/SKILL.md) | Official LottieFiles: timing, easing, choreography, Disney 12 principles for UI |
| [`gsap-skills`](../gsap-skills/SKILL.md) | Official GSAP: 8 skills — core, timeline, ScrollTrigger, Flip, Draggable, SplitText |
| [`framer-motion-skills`](../framer-motion-skills/SKILL.md) | 6 Framer Motion skills: core, Next.js, variants, scroll, gestures, layout |
| [`animate-skill`](../animate-skill/SKILL.md) | Emil-inspired Next.js/React patterns: hover, toast, text reveal, modals |
| [`animate-css-skill`](../animate-css-skill/SKILL.md) | Animate.css v4 + scroll triggers + RTL + prefers-reduced-motion |
| [`css-animation-skill`](../css-animation-skill/SKILL.md) | Scrapes live app design language, interviews, produces standalone animation file |
| [`wiggle-claude-skill`](../wiggle-claude-skill/SKILL.md) | Animates SVG logos → Lottie JSON → GIF + MP4 |
| [`claudedesignskills`](../claudedesignskills/SKILL.md) | 22-skill bundle: Three.js, GSAP, R3F, Framer, Babylon, A-Frame, PixiJS, Rive, Lottie |
| [`hyperframes`](../hyperframes/SKILL.md) | "Write HTML → render video": GSAP/CSS/Lottie/Three.js + TTS media (HeyGen) |

### Interaction & Polish

| Skill | Best for |
|-------|----------|
| [`taste-design-stitch`](../taste-design-stitch/SKILL.md) | Aesthetic judgment for Google Stitch output |
| [`design-lab`](../design-lab/SKILL.md) | Interactive design exploration, variant generation |
| [`interface-design-dammyjay`](../interface-design-dammyjay/SKILL.md) | Dashboards, admin panels, SaaS information-dense UI |
| [`bencium-ux-designer`](../bencium-ux-designer/SKILL.md) | Distinctive, production-grade frontend |
| [`neo-user-journey`](../neo-user-journey/SKILL.md) | UX journey mapping + Playwright testing + 50+ patterns + Nielsen scoring |
| [`simota-agent-skills`](../simota-agent-skills/SKILL.md) | 15 design sub-skills: Vision, Frame (Figma bridge), Pixel, Clay, Ink, Sketch |
| [`design-auditor`](../design-auditor/SKILL.md) | 19-category audit: typography, dark mode, RTL, dark patterns; 0-100 score |
| [`search-ux`](../search-ux/SKILL.md) | Search input, autocomplete, ranking, faceted filters, zero-results, search analytics |
| [`interfaces-that-feel`](../interfaces-that-feel/SKILL.md) | Emotional design: felt-state → physical analogue → motion/copy/spacing changes |
| [`information-architecture-and-navigation`](../information-architecture-and-navigation/SKILL.md) | Polar-bear IA: organization/labeling/nav/search, taxonomy, wayfinding, findability |

### Visual, Components & Color

| Skill | Best for |
|-------|----------|
| [`color-expert`](../color-expert/SKILL.md) | OKLCH/OKLAB color science, palette generation, contrast |
| [`baseline-ui`](../baseline-ui/SKILL.md) | Animation durations, typography scale, Tailwind anti-patterns |
| [`shadcn-ui`](../shadcn-ui/SKILL.md) | shadcn/ui component workflow |
| [`ui-ux-pro-max`](../ui-ux-pro-max/SKILL.md) | 50+ styles, 97 palettes, 9 tech stacks |
| [`platform-design-skills`](../platform-design-skills/SKILL.md) | 300+ HIG/MD3/WCAG rules for cross-platform |
| [`apple-hig-skills`](../apple-hig-skills/SKILL.md) | Apple HIG: iOS, macOS, visionOS, watchOS, tvOS |
| [`hig-doctor`](../hig-doctor/SKILL.md) | Diagnose and fix Apple HIG violations |
| [`swiftui-patterns`](../swiftui-patterns/SKILL.md) | SwiftUI view and component best practices |
| [`ink-google`](../ink-google/SKILL.md) | Ink-style editorial design for artifacts |
| [`design-tokens-skill`](../design-tokens-skill/SKILL.md) | W3C DTCG token spec: OKLCH, references/aliasing, Terrazzo, Figma exports |
| [`google-fonts-skill`](../google-fonts-skill/SKILL.md) | 1,923 Google Fonts with mood tags + 73 pairings + CSS vars + Tailwind config |
| [`mobile-app-design`](../mobile-app-design/SKILL.md) | iOS HIG + Android MD3 + RN best practices — 26K words |
| [`mobile-app-ui-design`](../mobile-app-ui-design/SKILL.md) | Professional mobile UI: intentional, smooth, alive interfaces |
| [`sleek-design-mobile-apps`](../sleek-design-mobile-apps/SKILL.md) | Sleek platform: design screens, projects, assets via natural language (account req.) |
| [`liquid-glass-skill`](../liquid-glass-skill/SKILL.md) | iOS 26 Liquid Glass: .glassEffect(), GlassEffectContainer, migration patterns |
| [`swiftui-claude-skills`](../swiftui-claude-skills/SKILL.md) | WWDC 2025 verified SwiftUI, iOS 26.4 RC, Xcode 26 |
| [`swiftui-design-skill`](../swiftui-design-skill/SKILL.md) | SwiftUI visual design craft — anti-AI-slop, typography, color, brand |
| [`material-3-skill`](../material-3-skill/SKILL.md) | Material Design 3 / Material You: dynamic color, tonal surfaces, 30+ components (Compose + Flutter) |

### Accessibility & Quality

| Skill | Best for |
|-------|----------|
| [`fixing-accessibility`](../fixing-accessibility/SKILL.md) | ARIA, keyboard nav, focus management, contrast fixes |
| [`fixing-motion-performance`](../fixing-motion-performance/SKILL.md) | Layout thrashing, compositor, scroll-linked animation |
| [`wcag-audit-patterns`](../wcag-audit-patterns/SKILL.md) | WCAG 2.2 audits with remediation |
| [`addyosmani-quality`](../addyosmani-quality/SKILL.md) | 6-skill suite: a11y, Lighthouse, CWV, perf, SEO, best practices |
| [`cloudflare-web-perf`](../cloudflare-web-perf/SKILL.md) | Core Web Vitals: LCP, INP, CLS fixes |
| [`react-doctor`](../react-doctor/SKILL.md) | React security, performance, correctness scoring |
| [`mastepanoski-skills`](../mastepanoski-skills/SKILL.md) | 6 audits: ux-rethink, Nielsen, WCAG POUR, Don Norman, cognitive walkthrough |
| [`wcag-ai-skill`](../wcag-ai-skill/SKILL.md) | WCAG 2.2 full workflow: design → frontend → QA → conformance docs |
| [`accessibility-agents`](../accessibility-agents/SKILL.md) | 25 specialist a11y agents: web code, Office/PDF docs, markdown auditors |
| [`dark-pattern-audit`](../dark-pattern-audit/SKILL.md) | Static audit of codebase + copy for deceptive dark patterns — confidence-graded, source-located |

### Design Review & Creative Direction

| Skill | Best for |
|-------|----------|
| [`creative-director`](../creative-director/SKILL.md) | 20+ ideation methods, Cannes/D&AD evaluation |
| [`design-brief`](../design-brief/SKILL.md) | Structured design briefs from loose requirements |
| [`design-consultation`](../design-consultation/SKILL.md) | Complete design system from scratch |
| [`design-review-garrytan`](../design-review-garrytan/SKILL.md) | Visual audit + atomic fix commits |
| [`plan-design-review`](../plan-design-review/SKILL.md) | Scored critique (0–10) with AI slop detection |
| [`design-html`](../design-html/SKILL.md) | Implement designs as production HTML/CSS |
| [`digidai-pm`](../digidai-pm/SKILL.md) | Senior PM: 30+ frameworks, SaaS metrics |
| [`ux-ui-mastery`](../ux-ui-mastery/SKILL.md) | 19 skills: cognitive psych, spatial UX, ambient UI, iOS 26, WCAG 3.0 |
| [`designer-skills`](../designer-skills/SKILL.md) | 91 skills, 28 commands: design research, systems, ux-strategy, critique |
| [`design-with-claude`](../design-with-claude/SKILL.md) | Deterministic WCAG/token audit + design slash commands: dashboards, b2b SaaS, healthcare UX, onboarding |
| [`ux-designer-skill`](../ux-designer-skill/SKILL.md) | Synthesizes 19 authoritative UX sources (NNG, Laws of UX) — 2026 best practices |
| [`wondelai-skills`](../wondelai-skills/SKILL.md) | Book-derived: Refactoring UI, Design of Everyday Things, Sprint, Lean UX |
| [`design-impact-reporting`](../design-impact-reporting/SKILL.md) | Design ROI: user→product→business metrics, scorecard / before-after / A-B / portfolio |
| [`design-debt-audit`](../design-debt-audit/SKILL.md) | Design-debt taxonomy + audit process + Severity×Frequency/Effort scoring + register |
| [`design-negotiation`](../design-negotiation/SKILL.md) | Advocacy scripts: timeline / scope / stakeholder override / headcount, evidence-based |
| [`service-blueprint`](../service-blueprint/SKILL.md) | NN/g service blueprints: 5 swim lanes, lines of visibility, JSON schema + render pipeline |

### Design Research

| Skill | Best for |
|-------|----------|
| [`user-research-cookiy`](../user-research-cookiy/SKILL.md) | End-to-end user research: study planning, AI-moderated interviews, survey design, transcript synthesis, research reports |
| [`software-ux-research`](../software-ux-research/SKILL.md) | Research ops: survey design, repository management, usability testing (ISO 9241), JTBD |

### Figma & Design-to-Code

| Skill | Best for |
|-------|----------|
| [`figma-official-skills`](../figma-official-skills/SKILL.md) | 7 official Figma skills: implement, generate, library, code-connect |
| [`openai-skills`](../openai-skills/SKILL.md) | OpenAI's 9 skills: Figma + frontend + slides + imagegen |
| [`google-stitch-skills`](../google-stitch-skills/SKILL.md) | 6 Stitch skills: design-md, react-components, shadcn, loop |
| [`extract-design-md`](../extract-design-md/SKILL.md) | Extract Stitch output into DESIGN.md format |
| [`claude2figma`](../claude2figma/SKILL.md) | 4 skills enforcing token compliance: colors/fonts/spacing bind to Figma variables |
| [`work-with-design-systems`](../work-with-design-systems/SKILL.md) | Inspect (WCAG audit) + Build (6-phase with variable bindings) dual-mode |
| [`figma-variables-tokens-generator`](../figma-variables-tokens-generator/SKILL.md) | Questionnaire → W3C token ZIP + Figma plugin for import |
| [`figma-skill`](../figma-skill/SKILL.md) | Figma API + Community resources → design tokens → 7 frameworks |
| [`extract-design-system`](../extract-design-system/SKILL.md) | Reverse-engineers tokens from any live website → tokens.json + tokens.css |

### Official Platform Suites

| Skill | Best for |
|-------|----------|
| [`anthropics-skills`](../anthropics-skills/SKILL.md) | 6 Anthropic skills: frontend-design, artifacts, canvas, theme, brand, pptx |
| [`vercel-skills`](../vercel-skills/SKILL.md) | 4 Vercel skills: web-design-guidelines, components, React best practices |
| [`microsoft-skills`](../microsoft-skills/SKILL.md) | 2 Microsoft skills: design review, dark-theme React |
| [`software-mansion-skills`](../software-mansion-skills/SKILL.md) | Official Software Mansion: RN animations, gestures, SVG, on-device AI |
| [`callstack-agent-skills`](../callstack-agent-skills/SKILL.md) | Official Callstack: RN best practices, profiling, Turbo Modules, upgrade |
| [`expo-skills`](../expo-skills/SKILL.md) | Official Expo: Expo SDK, EAS Build/Submit, Expo Router |

### Diagrams & Wireframing

| Skill | Best for |
|-------|----------|
| [`excalidraw-diagram`](../excalidraw-diagram/SKILL.md) | Excalidraw with visual validation loop (3.2k stars) |
| [`hand-drawn-diagrams`](../hand-drawn-diagrams/SKILL.md) | Quick hand-drawn sketch diagrams |
| [`excalidraw-agents365`](../excalidraw-agents365/SKILL.md) | Excalidraw tuned for coding agent workflows |
| [`wireframer`](../wireframer/SKILL.md) | Low-fidelity wireframes, structure-first |
| [`softaworks-agent-toolkit`](../softaworks-agent-toolkit/SKILL.md) | 40+ skills: mermaid, excalidraw, draw-io, C4, marp |
| [`nimbalyst-skills`](../nimbalyst-skills/SKILL.md) | Excalidraw with MCP tools, mockups, data models |
| [`wireframe-skill`](../wireframe-skill/SKILL.md) | NL → wireframe JSON + interactive HTML with drag/drop, undo/redo |
| [`claude-wireframe-skill`](../claude-wireframe-skill/SKILL.md) | 5 UX approaches as interactive prototypes — B&W first then color variants |

### Data Visualization & Charts

| Skill | Best for |
|-------|----------|
| [`antvis-chart-skills`](../antvis-chart-skills/SKILL.md) | 7 AntV skills: 26+ chart types, 98.2% accuracy |
| [`markdown-viewer-skills`](../markdown-viewer-skills/SKILL.md) | 14 skills: Vega, PlantUML, JSON Canvas, infographics |
| [`d3js-skill`](../d3js-skill/SKILL.md) | D3.js: data binding, scales, transitions, interactive charts |
| [`data-viz-agent`](../data-viz-agent/SKILL.md) | Multi-library agent: D3/Chart.js/Plotly/Matplotlib |
| [`claud3`](../claud3/SKILL.md) | D3 v7 + Tufte principles: 80+ chart types, dark theme, annotations |
| [`data-analysis-skill`](../data-analysis-skill/SKILL.md) | Multi-expert parallel analysis → HTML reports + PowerPoint export |

### 3D, Creative & Media

| Skill | Best for |
|-------|----------|
| [`cloudai-threejs`](../cloudai-threejs/SKILL.md) | Three.js 3D scenes, animations, WebGL |
| [`fal-ai-skills`](../fal-ai-skills/SKILL.md) | fal.ai image/video and 3D model generation |
| [`composio-artifacts`](../composio-artifacts/SKILL.md) | Artifacts connected to GitHub/Slack/Linear via Composio |
| [`webgpu-claude-skill`](../webgpu-claude-skill/SKILL.md) | Three.js TSL, node materials, GPU compute, WGSL — r183+ |
| [`threejs-ecs-ts`](../threejs-ecs-ts/SKILL.md) | Three.js + Entity Component Systems + TypeScript |
| [`threejs-claude-skill-package`](../threejs-claude-skill-package/SKILL.md) | 24 skills: WebGL, WebGPU, R3F, physics, IFC/BIM architecture |
| [`generative-media-skills`](../generative-media-skills/SKILL.md) | 41 workflows: Midjourney v7, Flux Kontext, Kling 3.0, Veo3, Suno audio |
| [`open-design`](../open-design/SKILL.md) | 31 skills + 71 brand design systems — local-first Claude Design alternative |
| [`superdesign-skill`](../superdesign-skill/SKILL.md) | Infinite-canvas ideation: brand extraction, design drafts, IDE-native |

### Presentations

| Skill | Best for |
|-------|----------|
| [`nanobanan-ppt`](../nanobanan-ppt/SKILL.md) | AI-powered PPT with document analysis and image generation |
| [`guizang-ppt`](../guizang-ppt/SKILL.md) | Structured PowerPoint from outline (no API deps) |
| [`frontend-slides`](../frontend-slides/SKILL.md) | Animation-rich HTML presentations |
| [`revealjs-skill`](../revealjs-skill/SKILL.md) | Reveal.js: themes, Chart.js, speaker notes, PDF export |
| [`marp-slides`](../marp-slides/SKILL.md) | MARP + 22 example decks, SVG charts, dashboard components |
| [`slidev-skill`](../slidev-skill/SKILL.md) | Official Slidev: developer presentations in Markdown with Vue + animations |
| [`cc-slidev`](../cc-slidev/SKILL.md) | Slidev plugin with evidence-based design guardrails for tech talks |
| [`marp-slide-quality`](../marp-slide-quality/SKILL.md) | SlideGauge scoring: overflow, contrast, density checks before render |

### Product & PM

| Skill | Best for |
|-------|----------|
| [`deanpeters-pm-skills`](../deanpeters-pm-skills/SKILL.md) | 9 skills: journey maps, OST, story mapping, PRD |
| [`phuryn-pm-skills`](../phuryn-pm-skills/SKILL.md) | 65 skills / 8 plugins: discovery, strategy, execution, market research, data analytics, GTM, growth |
| [`coreyhaines-marketing`](../coreyhaines-marketing/SKILL.md) | 3 CRO skills: onboarding, page, signup flow |
| [`pm-skills`](../pm-skills/SKILL.md) | 55 skills: Triple Diamond, 26 phases, Design Sprint, Foundation Sprint |
| [`claude-pm-skills`](../claude-pm-skills/SKILL.md) | Product thinking, discovery, prioritization, launch |
| [`design-sprint`](../design-sprint/SKILL.md) | Research codebase → design feature → decompose into parent + sub-issues with dependencies |
| [`product-position`](../product-position/SKILL.md) | B2B SaaS positioning: messaging hierarchy, competitive framing, strategic narrative — Dunford + JTBD frameworks |
| [`lenny-skills`](../lenny-skills/SKILL.md) | 86 PM skills: behavioral product design, surveys, user interviews, design reviews, onboarding, growth loops (945 ★) |
| [`assimovt-productskills`](../assimovt-productskills/SKILL.md) | 16 skills: roadmaps, North Star metrics, A/B experiments, competitor analysis, strategy docs, Shape Up scoping |
| [`chadboyda-gtm`](../chadboyda-gtm/SKILL.md) | 18 go-to-market skills: positioning/ICP, pricing, sales motion, outbound, launches, GTM metrics |

### Content Design & Copy

| Skill | Best for |
|-------|----------|
| [`ux-writing-skill`](../ux-writing-skill/SKILL.md) | Microcopy, button labels, error messages, empty states, form copy, a11y writing |
| [`copywriting-skill`](../copywriting-skill/SKILL.md) | Landing pages, product copy, email sequences, headlines, tone-of-voice (5 sub-skills) |
| [`humanize-text`](../humanize-text/SKILL.md) | Score + rewrite text across 7 AI-pattern dimensions; works on raw text, Figma URLs, screenshots |
| [`content-strategy`](../content-strategy/SKILL.md) | Content audit, content model, voice/tone, governance, content hierarchy |

### Email Design

| Skill | Best for |
|-------|----------|
| [`email-html-mjml`](../email-html-mjml/SKILL.md) | MJML 4.x → cross-client HTML email, WCAG 2.1 AA, Outlook-safe |

### TUI & Terminal Design

| Skill | Best for |
|-------|----------|
| [`tui-design-skill`](../tui-design-skill/SKILL.md) | Terminal UI design: Bubble Tea (Go), Ratatui (Rust), Textual (Python), Ink (TS) |
| [`textual-tui-skill`](../textual-tui-skill/SKILL.md) | Textual (Python) deep-dive: 40+ widgets, TCSS, reactive, workers, Pilot testing |

---

## Routing guide

| User says | Route to |
|-----------|----------|
| "good taste", "anti slop", "premium UI", "not generic" | `taste-skill` or `ui-craft` |
| "design variance", "motion intensity", "visual density" | `taste-skill` |
| "no Inter font", "no 3-column cards", "no centered hero" | `taste-skill` or `ui-craft` |
| "anti-slop detector", "33 rules", "ui-craft", "18 slash commands" | `ui-craft` |
| "polish", "micro-interactions", "make it feel better" | `make-interfaces-better` |
| "animation principles", "easing curves" | `emilkowalski-skill` |
| "GLSL", "ray march", "WebGL shader" | `shader-dev` |
| "generative art", "p5.js", "particle system" | `algorithmic-art` or `p5js-hermes` |
| "Three.js", "3D scene", "WebGL 3D" | `cloudai-threejs` |
| "Figma to code", "implement Figma" | `figma-official-skills` |
| "Stitch", "DESIGN.md", "stitch loop" | `google-stitch-skills` |
| "color palette", "OKLCH", "color science" | `color-expert` |
| "WCAG", "accessibility audit", "contrast" | `fixing-accessibility` or `addyosmani-quality` |
| "Core Web Vitals", "LCP", "CLS" | `cloudflare-web-perf` or `addyosmani-quality` |
| "React performance", "React audit" | `react-doctor` |
| "design review", "visual audit", "AI slop" | `plan-design-review` |
| "design system", "build from scratch" | `design-consultation` |
| "Apple HIG", "iOS design", "visionOS" | `apple-hig-skills` |
| "HIG compliance", "fix HIG" | `hig-doctor` |
| "mermaid", "C4 diagram", "draw.io" | `softaworks-agent-toolkit` |
| "excalidraw" | `excalidraw-diagram` |
| "wireframe", "lo-fi", "layout skeleton" | `wireframer` |
| "D3", "chart", "data visualization" | `d3js-skill` or `antvis-chart-skills` |
| "customer journey", "user story", "PRD" | `deanpeters-pm-skills` or `phuryn-pm-skills` |
| "CRO", "conversion", "onboarding" | `coreyhaines-marketing` |
| "PowerPoint", "slides", "presentation" | `guizang-ppt` or `nanobanan-ppt` |
| "HTML presentation", "animated slides" | `frontend-slides` |
| "shadcn", "shadcn component" | `shadcn-ui` |
| "platform design", "cross-platform rules" | `platform-design-skills` |
| "creative strategy", "campaign concept", "SCAMPER" | `creative-director` |
| "design brief", "requirements spec" | `design-brief` |
| "motion principles", "purposeful motion", "motion audit", "AI slop motion", "hover state design", "micro-interaction design", "Emil Kowalski motion", "Jhey Tompkins" | `design-motion-principles` |
| "GSAP", "ScrollTrigger", "GreenSock" | `gsap-skills` |
| "Framer Motion", "framer animation", "layout animation" | `framer-motion-skills` |
| "Lottie", "motion principles", "Disney principles" | `motion-design-skill` |
| "SVG logo animation", "wiggle", "logo GIF" | `wiggle-claude-skill` |
| "Animate.css", "bounce", "fadeIn" | `animate-css-skill` |
| "Babylon.js", "A-Frame", "PixiJS", "Rive" | `claudedesignskills` |
| "HTML to video", "render video", "HeyGen" | `hyperframes` |
| "Reveal.js", "revealjs presentation" | `revealjs-skill` |
| "Marp", "MARP slides" | `marp-slides` |
| "Slidev", "developer slides Vue" | `slidev-skill` |
| "Marp quality", "slide overflow check" | `marp-slide-quality` |
| "design tokens", "DTCG", "W3C tokens", "Terrazzo" | `design-tokens-skill` |
| "Google Fonts", "font pairing", "typography scale" | `google-fonts-skill` |
| "mobile app design", "touch targets", "thumb zones" | `mobile-app-design` |
| "iOS 26", "Liquid Glass", "glassEffect" | `liquid-glass-skill` |
| "SwiftUI iOS 26", "WWDC 2025 SwiftUI" | `swiftui-claude-skills` |
| "SwiftUI design", "SwiftUI visual design", "iOS visual design" | `swiftui-design-skill` |
| "WCAG 2.2 guidance", "conformance docs" | `wcag-ai-skill` |
| "25 a11y agents", "PDF accessibility", "document a11y" | `accessibility-agents` |
| "Don Norman audit", "cognitive walkthrough", "ux-rethink" | `mastepanoski-skills` |
| "91 design skills", "design ops", "visual critique" | `designer-skills` |
| "audit my design system", "healthcare UX", "b2b SaaS UX" | `design-with-claude` |
| "UX principles", "Laws of UX", "usability guidelines" | `ux-designer-skill` |
| "Refactoring UI", "Design Sprint book", "Lean UX" | `wondelai-skills` |
| "user journey", "journey mapping", "Playwright UX" | `neo-user-journey` |
| "design score", "19-category audit", "dark patterns audit" | `design-auditor` |
| "Figma token compliance", "Figma variables enforcement" | `claude2figma` |
| "extract tokens website", "reverse-engineer CSS" | `extract-design-system` |
| "Figma design system build", "variable bindings" | `work-with-design-systems` |
| "React Native animations", "Reanimated", "Gesture Handler" | `software-mansion-skills` |
| "Expo", "EAS Build", "Expo Router" | `expo-skills` |
| "React Native profiling", "Turbo Modules", "brownfield" | `callstack-agent-skills` |
| "D3 Tufte", "80 chart types", "dark chart" | `claud3` |
| "parallel data analysis", "data to PowerPoint" | `data-analysis-skill` |
| "WebGPU", "TSL Three.js", "GPU compute" | `webgpu-claude-skill` |
| "Three.js ECS", "entity component 3D" | `threejs-ecs-ts` |
| "Three.js BIM", "IFC architecture", "AEC 3D" | `threejs-claude-skill-package` |
| "Midjourney workflow", "Kling", "Veo3", "Flux Kontext" | `generative-media-skills` |
| "infinite canvas design", "SuperDesign" | `superdesign-skill` |
| "open-design platform", "31 design skills local" | `open-design` |
| "Triple Diamond PM", "55 PM skills", "Design Sprint method" | `pm-skills` |
| "MJML", "HTML email", "Outlook-safe email" | `email-html-mjml` |
| "terminal UI", "TUI", "Bubble Tea", "Ratatui", "Textual" | `tui-design-skill` |
| "brand tokens Stripe", "62 brands" | `brand-design-md` |
| "aesthetic anchor", "Brutalist CSS", "Nordic design" | `frontend-design` |
| "logo SVG", "brand interview", "logo PNG" | `logo-designer-skill` |
| "AI Midjourney design", "AI Creative Director" | `ai-graphic-design-skill` |
| "button label", "error message copy", "empty state", "microcopy" | `ux-writing-skill` |
| "landing page copy", "product copy", "tone of voice", "headline" | `copywriting-skill` |
| "remove AI patterns", "de-slop", "AI writing", "humanize text" | `humanize-text` |
| "Material Design 3", "Material You", "MD3", "Jetpack Compose design" | `material-3-skill` |
| "brand skin", "design token engine", "styleseed" | `styleseed` |
| "design aesthetic", "glassmorphism", "brutalism style", "claymorphism" | `awesome-design-skills` |
| "Textual TUI", "Textual Python", "Textual widget", "TCSS" | `textual-tui-skill` |
| "interaction design", "component states", "affordance", "micro-interaction timing" | `interaction-design` |
| "Storybook", "Storybook story", "CSF", "Chromatic visual regression" | `format-storybook` |
| "user research", "user interview", "research synthesis", "usability study" | `user-research-cookiy` |
| "feature design sprint", "design to issues", "decompose feature" | `design-sprint` |
| "product positioning", "messaging hierarchy", "value proposition", "competitive framing" | `product-position` |
| "behavioral product design", "designing surveys", "running design reviews", "growth loops" | `lenny-skills` |
| "roadmap planning", "North Star metric", "experiment design", "competitor analysis", "Shape Up" | `assimovt-productskills` |
| "go-to-market skills", "GTM operator", "sales motion", "AI SDR", "pricing strategy" | `chadboyda-gtm` |
| "dark patterns", "deceptive design", "manipulative UI", "hidden fees code" | `dark-pattern-audit` |

## No match

If intent doesn't match any stub:
- Say so directly: "No stub in this catalogue covers [X] yet."
- Suggest checking the repo for new additions
- Offer to help build a stub if they have an upstream skill in mind
