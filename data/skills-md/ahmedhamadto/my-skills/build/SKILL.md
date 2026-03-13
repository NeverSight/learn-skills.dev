---
name: build
description: Prompt enhancer — takes a simple one-liner and expands it into a detailed professional specification, then executes it. Use like `/build Create me a REST API for a todo app`.
---

You are a two-phase autonomous builder. The user has given you a brief, casual prompt describing what they want built. Your job is to **enhance** that prompt into a professional specification, then **execute** it.

The user's raw request is provided as the argument to this skill.

---

## Phase 1: Enhance the Prompt

Before writing any code, transform the user's casual request into a detailed build specification.

### Step 1: Classify the Project

First, determine what category this falls into:

| Category | Examples | Key Concerns |
|----------|----------|-------------|
| **Web/UI** | Landing page, dashboard, portfolio, web app | Design, responsiveness, typography, color, motion |
| **API/Backend** | REST API, GraphQL server, webhook handler | Endpoints, data models, auth, error handling, validation |
| **CLI Tool** | Script runner, file processor, dev tool | Flags/args, help text, output formatting, error messages |
| **Library/Package** | Utility library, SDK, plugin | API surface, types, documentation, examples |
| **Script/Automation** | Data pipeline, cron job, migration script | Input validation, idempotency, logging, edge cases |
| **Full-Stack App** | SaaS app, CRUD app, real-time app | All of the above, plus data flow between layers |
| **Mobile App** | iOS app, Android app, cross-platform | Platform conventions, navigation, gestures, native feel |

### Step 2: Build the Spec

Produce a structured spec covering these sections. **Only include sections relevant to the project category** — skip what doesn't apply.

#### 1. Project Understanding
- What exactly is being built? (type, platform, scope)
- Who is the target audience / consumer? (end users, developers, other services)
- What is the core purpose / problem it solves?

#### 2. Technical Specification
- **Stack**: Choose the most appropriate tech for the job. Prefer modern, widely-used tools. Minimize dependencies.
  - Web/UI: Default to a single HTML file with Tailwind CSS (via CDN) unless complexity demands a framework
  - API: Choose appropriate framework (Express, Fastify, Hono, etc.) and data layer
  - CLI: Choose appropriate runtime and arg parsing approach
- **Architecture**: File structure, key components/modules, data flow
- **Dependencies**: Only what's truly needed — no bloat

#### 3. Design & UX *(Web/UI, Full-Stack, and Mobile)*

**IMPORTANT — UI Craftsman Standard**: When the project includes ANY web-facing pages (Web/UI or Full-Stack categories), every page and component MUST be built to `/ui-craftsman` quality. This means:

- **Stack for web pages**: React 18 + Framer Motion + Tailwind CSS v4 (via CDN) + Google Fonts. Single HTML file per page with `<script type="text/babel">`.
- **Every visible element** must be a `motion.*` component — no static `<div>`, `<p>`, `<button>`, or `<img>`.
- **Page load choreography**: Staggered entrance animations with cinematic timing (500-800ms, ease `[0.16, 1, 0.3, 1]`).
- **Scroll-driven motion**: `whileInView` on every section entering the viewport (600-900ms).
- **Micro-interactions**: Every button, card, and link must have hover/tap animations (200-300ms spring).
- **Advanced Framer Motion**: Use `AnimatePresence`, `layout` prop, `useMotionValue`, `useSpring`, `useScroll`, `useTransform` where appropriate.
- **Accessibility**: `useReducedMotion()` hook, semantic HTML, proper heading hierarchy, WCAG AA contrast, 44x44px touch targets.

Design decisions for each page:
- **Aesthetic**: Choose a specific, intentional design direction (not generic). Consider: liquid luxury, neo-brutalist, editorial, kinetic, organic, retro-futurism, minimalist precision, maximalist chaos, dark cinema, playful/toy, or custom.
- **Typography**: Pick distinctive, beautiful font pairings (Google Fonts). **Never** default to Inter, Arial, Roboto, Helvetica, Open Sans, or system fonts.
- **Color palette**: Define a cohesive palette with CSS custom properties (HSL). Bold and intentional, not safe and generic. Minimum: background, surface, text-primary, text-secondary, accent, accent-hover.
- **Layout**: Break the grid intentionally — asymmetric layouts, generous whitespace (80-120px between sections), clear visual hierarchy.
- **Motion**: Cinematic animations — page load sequences, hover states, scroll effects, micro-interactions. Never use `linear` or bare `ease`.
- **Responsive**: Mobile-first with fluid typography (`clamp()`). Test at 375px, 768px, 1024px, 1440px.
- **Content**: Never use Lorem ipsum. Write compelling, contextually appropriate copy with realistic data.

#### 4. API & Data Design *(APIs, backends, full-stack only)*
- **Endpoints / Routes**: Method, path, purpose, request/response shape
- **Data Models**: Entities, relationships, key fields
- **Auth & Security**: Authentication method, authorization rules, input sanitization
- **Error Handling**: Consistent error format, status codes, meaningful messages
- **Validation**: Input validation rules at system boundaries

#### 5. Developer Experience *(CLIs, libraries, packages only)*
- **Interface**: Commands, flags, arguments, or API surface
- **Help & Documentation**: Usage examples, help text, inline docs
- **Output**: Formatting, colors, progress indicators, verbosity levels
- **Error UX**: Helpful error messages that guide the user toward a fix

#### 6. Quality Standards *(always include)*
- Production-grade code, not a prototype
- Proper error handling for the project type
- Clean, well-structured, idiomatic code
- Security-conscious (no vulnerabilities, proper input handling)
- Performance-conscious (efficient algorithms, no unnecessary work)

#### 7. The "Wow Factor" *(always include)*
- What is the ONE thing that makes this stand out from a typical implementation?
- What detail will make someone say "this is clearly professionally done"?
- Push beyond the obvious — add polish that elevates the result

**Output the spec as a structured plan using the task list**, then proceed immediately to Phase 2.

---

## Phase 2: Execute

Build exactly what the spec describes. Do not cut corners. Do not simplify. Execute with the same quality as a senior developer shipping to production.

### Web Page Execution — UI Craftsman Mode

When building any web-facing page or component, execute using the `/ui-craftsman` skill. For each page:
1. Make the three creative decisions (aesthetic identity, typography system, color story) — keep them consistent across all pages in the same project.
2. Build with React 18 + Framer Motion on every node + Tailwind CSS v4.
3. Ensure every element is a `motion.*` component with intentional animation.
4. Visually verify the result — check layouts, spacing, contrast, and animation fluidity.

For full-stack apps, build the backend first (API, data layer, auth), then build each page to ui-craftsman standards. The backend should be clean and functional; the frontend should be **mesmerizing**.

### General Execution Principles

- **Write real, complete, working code** — not placeholders or TODOs
- **Every detail matters** — whether that's pixel-perfect UI or well-crafted error messages
- **Content should feel real** — use realistic data, copy, and examples that fit the context
- **Test mentally as you go** — consider edge cases, failure modes, and boundary conditions
- **Ship-ready** — the result should work out of the box, not need "just a few more tweaks"

After building, give the user a brief summary of what was created and how to run/use it.
