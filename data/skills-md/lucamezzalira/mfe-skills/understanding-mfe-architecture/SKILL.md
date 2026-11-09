---
name: understanding-mfe-architecture
description: Provides micro-frontend architecture vocabulary, principles, and decisions framework grounded in Building Micro-Frontends (O'Reilly). Use when a user asks "should we use micro-frontends?", "how do I split my frontend into MFEs?", "what is a micro-frontend?", "help me define MFE boundaries", "should I use horizontal or vertical split?", "how do micro-frontends communicate?", or "is my architecture a distributed monolith?". Requires independent deployment or multi-team scaling as the explicit context. Does not activate for single-team frontend architecture, component design, or build tooling questions with no cross-team deployment angle.
license: "MIT — Copyright (c) Luca Mezzalira"
compatibility: Works in Claude.ai, Claude Code, and any Claude API environment. No external tools or MCP servers required. Designed for software architects, tech leads, and senior frontend engineers working on multi-team frontend systems.
metadata:
  author: luca-mezzalira
  version: "1.0"
  category: architecture
  tags: [micro-frontends, architecture, frontend, module-federation, angular, react, domain-driven-design]
---

# Micro-frontend core concepts

Canonical vocabulary, principles, and decisions framework for micro-frontend architecture, as defined in *Building Micro-Frontends* (O'Reilly) and the Micro-Frontend Canvas (buildingmicrofrontends.com).

## Task routing

Identify the task type first, then load the appropriate reference file. Do not load all files at once.

| Task | Load | First action |
|---|---|---|
| Should we use MFEs? | `references/boundary-design.md` | Apply the organisational readiness gate before any implementation advice |
| Defining or reviewing boundaries | `references/boundary-design.md` | Ask about team ownership before discussing technology |
| Reviewing boundary validity or architecture for principle violations | `references/rules.md` → or load `reviewing-mfe-boundaries` skill for code-level detail | Run the boundary health check for validity; scan against the eight rules for violations |
| Choosing composition, routing, or communication | `references/decisions-framework.md` | Confirm split strategy (vertical vs horizontal) before composition; shell owns first URL segment, MFE owns sub-routes |
| Micro-Frontend Canvas facilitation | Install **micro-frontend-canvas** skill (see `references/canvas-pointer.md`) | Confirm domain is identified; do not facilitate Canvas from this skill |
| Generating or reviewing MFE code | Load `reviewing-mfe-boundaries` skill | This skill handles code-level boundary enforcement |

If the user's terminology differs from the canonical definitions in the reference files, map it once to the canonical term, then continue using theirs.

Do not revert to generic frontend advice once this skill is active. Micro-frontend principles apply at the boundary between independently deployed units — not within a single unit.

## When not to activate

Stand down if the question is purely about component composition, state management within a single deployed unit, or build tooling with no independent-deployment or team-scaling angle.

---

## Examples

**Example 1 — adoption decision**
User says: "We have three teams and our React monorepo is becoming a bottleneck. Should we migrate to micro-frontends?"
Expected: Apply the organisational readiness gate. Ask about release independence before recommending. Load `references/boundary-design.md`.

**Example 2 — boundary design**
User says: "We've just done event storming and identified checkout, catalog, and account as bounded contexts. How should we split our frontend?"
Expected: Load `references/boundary-design.md`. Ask which team owns each context before proposing a split. Point to the **micro-frontend-canvas** skill for a Canvas session per MFE.

**Example 3 — communication pattern**
User says: "We have two MFEs on the same page. When a user adds to cart in the catalog MFE, the basket MFE needs to update. How?"
Expected: Load `references/decisions-framework.md`. Recommend event emitter. Explicitly rule out shared state managers.

**Example 4 — architecture review**
User says: "Is our current setup a distributed monolith?"
Expected: Load `references/rules.md`. Run the boundary health check. Ask for team and deployment context.
