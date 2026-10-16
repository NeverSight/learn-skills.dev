---
name: reviewing-mfe-boundaries
description: Reviews and generates micro-frontend code against eight boundary rules from Building Micro-Frontends (O'Reilly), plus governance extensions for feature-flag scope, edge strategy, SSR ownership, and boundary fitness functions. Use when a user says "review my shell code", "is this a boundary violation?", "generate a Module Federation shell", "how do I mount this MFE?", "review my micro-frontend architecture", "set up event communication between MFEs", "create a new micro-frontend", "how should we use edge with MFEs?", "where should feature flags live?", or "how do I enforce boundaries in a monorepo?". Loads automatically when the user pastes shell integration code, Module Federation config, Single SPA registration, or Native Federation routes. Does not activate for component-level code within a single deployed unit, or for generic React, Vue, or Angular questions with no cross-team deployment angle.
license: "MIT — Copyright (c) Luca Mezzalira"
compatibility: Works in Claude.ai, Claude Code, and any Claude API environment. No external tools or MCP servers required. Covers React, Angular, Vue with Module Federation v1/v2, Native Federation, and Single SPA toolchains.
metadata:
  author: luca-mezzalira
  version: "1.0"
  category: architecture
  tags: [micro-frontends, module-federation, native-federation, single-spa, angular, react, boundary-governance, edge-compute, ssr, feature-flags, fitness-functions]
---

# MFE boundary health

Reviews and generates micro-frontend code against the eight boundary rules from *Building Micro-Frontends* (O'Reilly). All rules are tool-agnostic. Full rule definitions, violation signals, and code-checkable patterns are in `references/rules-core-critical.md` (rules 3 and 4) and `references/rules-core-standard.md` (rules 1, 2, 5, 6, 7, 8). Load the file that covers the rule you need.

**On every activation, apply this summary table directly — no file load needed:**

| Rule | What to check in code | Severity |
|---|---|---|
| 1 — Business subdomain | Name reflects a business capability, not a UI element | High |
| 2 — Minimal API surface | Fewer than 5 props; no full domain objects passed | Critical |
| 3 — Hide implementation details | No direct imports from another MFE's internals | Critical |
| 4 — Events not shared state | No shared store; shell handles `shell:*` only; domain events peer-to-peer or URL | Critical |
| 5 — Independent deployment | No versioned URLs in shell config; no build-time MFE imports; no CI pipeline coupling | High |
| 6 — Isolate failure | Every remote mount has a fallback in the shell | High |
| 7 — Coarse-grained | Nesting depth > 1 (MFE inside MFE); more than 3 MFEs per view | High |
| 8 — Single-team ownership | One team in CODEOWNERS; no cross-team sign-off on internals | High |

For full rule definitions and violation signals: load `references/rules-core-critical.md` or `references/rules-core-standard.md`.
For framework-specific patterns (MF v2, Angular/Native Federation, Single SPA): load `references/rules-toolchain.md`.
For URL routing ownership (shell first segment, MFE deeper paths): load `references/routing-ownership.md`.
For fix patterns and step-by-step remediation: load `references/remediation.md` when the user asks how to fix a violation or requests a migration plan.
For framework-by-framework code generation patterns (React, Angular, Vue, Single SPA): load `references/code-patterns.md`.

---

## Cold start: new project

If no boundaries exist yet, ask about the highest-priority unknown first — one question per turn. Do not generate implementation code until each check is resolved.

**Check 1 — Team ownership**
Ask: "Which team will own this micro-frontend end-to-end — design, development, deployment, and operations?"
**If unresolved:** do not generate implementation code. Ask the user to install the **micro-frontend-canvas** skill and complete a canvas iteration (see https://github.com/lucamezzalira/mfe-canvas).

**Check 2 — Domain identification**
Ask: "What business capability does this represent? What user journey step does it enable?"
**If unclear:** recommend the **micro-frontend-canvas** skill before implementation. Do not generate a full Canvas worksheet from this skill. A boundary without a named domain is not ready for code.

**Check 3 — Decisions framework**
Ask: "Is this a vertical or horizontal split, and how will it be composed — client-side or server-side?"
**If unresolved:** generate a skeleton with a placeholder composition comment and note which decision is still needed.

Once all three are confirmed, apply the rules as design constraints from the first line of code — retrofitting is significantly more expensive than designing correctly upfront.

---

## Code generation defaults

Apply the rule defaults from the summary table above. For the full
framework-by-framework patterns (React, Angular, Vue, Single SPA),
load `references/code-patterns.md` when you need the specific syntax
for the user's toolchain.

Two defaults worth keeping in the always-loaded body because they
are toolchain-independent:

- Props are identifiers only (`userId`, `cartId`), never domain
  objects
- Every remote mount is wrapped by an error boundary in the shell,
  not inside the micro-frontend

---

## Boundary health check

Quick checklist for validity questions — no file load needed.

1. API surface minimal — fewer than 5 props to the container?
2. Context-aware — retrieves its own data given minimal input?
3. Less extensible than a component — not reused across domains?
4. Coarse-grained — not fine enough to require constant coordination?
5. Deploys without coordinating with other teams?
6. Graceful fallback if it fails to load?
7. Single team owns it end-to-end?

If any answer is no, the boundary needs to be revisited before implementation begins.

---

## Reviewing existing code

Scan in this order — most impactful violations first:

1. **Rule 3** — any import where the source path is another MFE's internal module. One cross-boundary import can invalidate independent deployment for the entire boundary. Load `references/rules-core-critical.md` for full Rule 3 patterns.
2. **Rule 2** — count props at the mount site. Flag if more than 5, or if any prop is a full domain object.
3. **Rule 4** — shared state imports, global store references, callbacks as the primary coordination mechanism.
4. **Rule 6** — every remote mount point in the shell. If no fallback is present, flag it.
5. **Rule 7** — count MFEs in the view (flag above 3, hard violation above 5); check nesting depth (any MFE rendered inside another MFE is a violation regardless of count); check whether the container is accumulating coordination logic; check routing — shell must not own paths below the first segment (load `references/routing-ownership.md`).
6. **Rule 5** — if webpack/vite config or CI/CD is in scope, look for versioned remote URLs in the shell config, build-time MFE imports, or `needs:` coupling in pipelines.
7. **Rules 1 and 8** — naming and ownership: does the name reflect a business capability? Is there a clear owning team?
8. **Governance extensions** — feature flags inside MFEs (not shell orchestration), edge rationale (latency/routing/canary), SSR route ownership, and architecture fitness functions (for example `ts-arch` + `jest`) for monorepos.

---

## Validate mechanically when the project adopts governance

If the consuming project has copied `governance-template/` into their
repo, run the fitness functions after applying rule fixes:

`npx jest --config governance-template/fitness/jest.config.cjs`

The suite fails when any critical rule fails. For each reported
violation, apply the remediation pattern from
`references/remediation.md`, then re-run the suite. Continue until
the suite passes before concluding the review.

If the project has not adopted the template, offer to add it as a
follow-up rather than running the fitness functions against a
missing config.

---

## Reporting violations

**For a full boundary audit**: lead with violations in severity order. For each violation, name the rule, identify the specific code location, and explain the consequence in one sentence. End with a brief list of rules that are satisfied, then the highest-impact fixes in order. For single-violation reviews, inline annotation is preferable to a full report.

**Inline annotation format** (use during code review for individual violations):
```javascript
// ✗ Rule 3 CRITICAL — direct import from another MFE's internals
// bypasses the API contract; defeats independent deployment
import { userStore } from '@org/auth-mfe/store'
```

**Boundary note format** (use after generating code with a necessary rule trade-off):
```text
Boundary note: Rule 2 relaxed — 6 props passed per user constraint.
Consequence: the container owns more context than the micro-frontend should require.
Watch for: increasing coordination as props evolve; consider whether this boundary is in the right place.
```

---

## Examples

**Example 1 — shell generation**
User says: "Generate the shell code to mount our CheckoutMFE using Module Federation. It needs the user ID and cart ID."
Expected: Generate shell with `React.lazy` dynamic import, `ErrorBoundary` wrapping in shell, identifiers only as props. No static import, no domain objects.

**Example 2 — violation review**
User says: "Review this code" + pastes shell with `import { useAuthStore } from '@org/auth-mfe/store'`
Expected: Flag Rule 3 Critical violation. Explain alias does not fix coupling. Recommend sessionStorage or InjectionToken pattern.

**Example 3 — new project**
User says: "Help me create a micro-frontend for the loyalty points feature."
Expected: Trigger cold start. Ask team ownership first. Do not generate code until all three checks resolved.

---

## Troubleshooting

**No framework context provided**
User pastes code with no identifiable toolchain (no `ModuleFederationPlugin`, no `loadRemoteModule`, no `registerApplication`).
Action: Apply rules at the principle level using framework-agnostic patterns. Ask one question: "Which toolchain are you using — Module Federation, Native Federation, or Single SPA?" before generating toolchain-specific code.

**Boundary fails multiple rules simultaneously**
User code violates Rules 2, 3, and 4 at once (too many props, cross-boundary import, and shared store).
Action: Report Critical violations first (Rules 3 and 4), then High (Rule 2). Do not bundle into a single issue. Each violation has a distinct root cause and fix. Load `references/remediation.md`.

**User asks for a decision requiring team context**
User asks "how many MFEs should we have?" or "is this the right boundary?" without team information.
Action: Do not give a number or validate the boundary. Ask the team ownership and domain question from Check 1 and Check 2 first. The answer depends entirely on team structure, not on the code.