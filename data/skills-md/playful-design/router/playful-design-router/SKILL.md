---
name: playful-design-router
description: Routes interface and design work to the right installed design skill (Emil Kowalski's design-engineering and animation skills, Benji Taylor's stageshow, Vercel's web-design-guidelines, Stewdio's blank-page and Raphael Salaja's userinterface collection). Use at the start of any UI, visual design, motion, copy, layout, mockup or front-end polish task, when reviewing or shipping interface changes, or whenever it is unclear which design skill applies.
---

# Playful Design Router

One skill that knows the others. Read the request, decide which design skills apply, and use them in a sensible order. Curated by Playful Design (playfuldesign.app/skills).

## 1. See what is installed

Before routing, check which of these skills are present. Look in `.claude/skills/`, `.agents/skills/` and `.cursor/skills/` in the project, and the same folders under `~/`. Only route to skills that exist. If a skill would clearly help but is missing, say so once and give its install command from the table at the end. Do not install anything without asking.

## 2. Always on (standards)

Apply these to every interface change. They do not need to be named:

- `scope`: change exactly what was asked, keep what worked, finish every item.
- `restraint`: ship the smallest thing that does the job; delete what nobody asked for.
- `reuse`: the project's own components first, then a maintained library, then a native feature.
- `copy`: short, plain interface labels.
- `defaults`: house defaults for focus, forms, loading, dialogs, scroll edges and type.
- `color`: contrast held to exact ratios, colour through role tokens, a real dark palette.
- `motion` or `emil-design-eng`: what animates, easing, durations, springs and reduced motion. If both are installed, use `emil-design-eng` for animation decisions and `motion` for house numbers.

The project's own conventions (its CLAUDE.md, AGENTS.md, design tokens or style guide) win over any of these. When rules conflict, say which one you followed.

## 3. Route by intent

| The request is about | Use |
| --- | --- |
| Finding references or inspiration before designing | `gather` |
| Turning a one-line motion or animation idea into a full prompt | `blank-page` |
| Copying or recreating a named site, screen or component | `match` |
| Fake or mocked product UI, hero or feature-card illustrations, bento grids, cursor or product demo animations | `stageshow` |
| Building a new animation or transition on the web | `animate` (then `animation-performance` if it is heavy) |
| Animation in React Native or Expo | `animate-expo` |
| Gestures, springs, sheets, materials, Apple-style feel | `apple-design` |
| "Make it feel more alive" or "what should animate?" | `find-animation-opportunities` |
| "It feels slow" or "too much animation" | `remove-animations` |
| A plan to fix motion across a whole app | `improve-animations` |
| Naming a motion effect so it can be asked for precisely | `animation-vocabulary` |
| A web app that should feel native on phones | `mobile-native` |
| Stress-testing a screen with worst-case data | `break-ui` |
| Choosing a UI library (charts, OTP, toasts, command menus) | suggest `/pick-ui-library` |
| Sonner toasts | `ask-sonner` |
| Swift code | `write-swift` |
| Choosing between directions ("try a few", "show options") | suggest `/prototype` (Raphael's builds labelled variants on one page; Emil's puts them behind a live picker; only one can be installed because they share a name) |
| Seeing every state and variant of real components | suggest `/lab` |
| A mascot or character made from an object | suggest `/avatar` |
| Missing icons that should match an existing set | `icons` |
| A daily batch of small interaction experiments | suggest `/sketchbook` |
| Understanding an existing animation or interaction | suggest `/deconstruct` |
| Long-form writing: posts, case studies, design notes | `prose` |
| Reviewing UI code for accessibility, focus, forms, motion and performance | `web-design-guidelines` |
| A strict review of motion code | suggest `/review-animations` |
| Checking a change actually works in the running app | `verify` |
| Responsive layout, overflow, clipping, zoomed text | `viewports` |
| Pixel alignment, spacing and radii that are slightly off | suggest `/alignment` |
| Keyboard access and focus order | suggest `/keyboard` |
| Jank, dropped frames, slow input | `animation-performance`, or suggest `/frames` for a measured trace |
| A correction the user keeps repeating | `rule` |
| "Review everything" or an end-of-task design pass | suggest `/audit` |
| Committing, merging and releasing | suggest `/ship`, only when the user asks to ship |
| A Grok Bots portfolio page | suggest `/bots` |

Skills marked "suggest" only run when the user calls them by name (`disable-model-invocation`). Name the command and what it will do; do not try to run it yourself.

## 4. Order of work

For anything bigger than a one-line fix:

1. **Before building:** `gather` or `match` if references matter; offer `/prototype` when the direction is open.
2. **While building:** the always-on standards, `stageshow` for faux UI and marketing visuals, and `animate` or `animate-expo` for new motion.
3. **Before saying done:** `verify` in the running app, `viewports` for layout changes, `break-ui` for data-heavy screens, and `web-design-guidelines` on the changed UI files. Offer `/alignment`, `/keyboard` or `/frames` when the change touches those areas.
4. **After:** `rule` if a correction came up twice. `/ship` only on request.

Keep it proportional. A copy tweak needs `scope` and `copy`, not the whole pipeline.

## 5. Report the route

In one short line, say which skills you used, for example: "Used stageshow for the hero mock, checked with verify and viewports."

## Install commands

| Skill | Install |
| --- | --- |
| Everything (this router and every skill below) | `npx skills add playful-design/router` |
| This router only | `npx skills add playful-design/router --skill playful-design-router` |
| stageshow (Benji Taylor) | `npx skills add benjitaylor/skills --skill stageshow` |
| Emil Kowalski's collection | `npx skills add emilkowalski/skills` |
| One of Emil's | `npx skills add emilkowalski/skills --skill <name>` |
| web-design-guidelines (Vercel) | `npx skills add vercel-labs/agent-skills --skill web-design-guidelines` |
| blank-page (Stewdio) | `npx skills add StewdioAI/blank-page` |
| Raphael Salaja's collection | `npx skills add raphaelsalaja/skills` |
| One skill from it | `npx skills add raphaelsalaja/skills --skill <name>` |

Credit for each skill belongs to its author. This router only points the way.
