---
name: codebase-design-axes
description: "Companion to codebase-design for variant axes. Use when adding a variant to an existing set — a second scenario, state, mode, tier, provider, or parser branch — when a spec enumerates states, or when a change is about to touch the same concept in more than one file. Gives the forcing rule codebase-design lacks: every variant axis gets one owner module, and the second variant is the design deadline."
---

# Codebase Design: Variant Axes

The dual of a `codebase-design` principle. That skill's seam rule is restraint: **one adapter means a hypothetical seam; two adapters means a real one** — don't build abstraction before something varies. This skill is the forcing direction: **the moment something varies, the owner module is mandatory.** Restraint without forcing produces sprawl one compliant-looking diff at a time.

Uses the `codebase-design` vocabulary — **module**, **interface**, **seam**, **depth**, **leverage**, **locality**. Load that skill for definitions.

## Glossary

**Variant axis** — a concept whose values enumerate: states, scenarios, modes, tiers, providers, formats, channels. If you can say "we support N of them and will add an (N+1)th," it's an axis.

**Owner module (registry)** — the single module that owns an axis. Everything the codebase knows about the axis's values is derivable from it.

**Touchpoint** — a place a consumer varies with the axis (a route param, a catalog row, a config entry, a switch branch, a fixture flag).

**Shallow-by-diffusion** — the failure mode: the axis has no module, so its de-facto interface is the union of its touchpoints, each with nothing behind it. Interface as complex as the implementation — shallowness, produced upstream of any module you could point at.

## The rule

**Every variant axis gets one owner module, and the second variant is the design deadline.**

- The first instance inline is fine — that's the hypothetical-seam rule working as intended.
- The moment the first sibling appears ("ready" grows "importing"), the axis is real. Build the registry **before adding the sibling**, not after five of them.
- Adding a variant after that touches **one registry row** (plus pinned test expectations). Nothing else.

## Why axes sprawl (mechanism, not carelessness)

1. **Nobody owns the axis.** It's a concept with no module, so every touchpoint edit looks locally compliant. No single diff is wrong; the sum is.
2. **Framework gravity.** Frameworks hand you mechanism-shaped files (`page.tsx`, `routes.ts`, handlers, config), so diffs land in mechanism files. Concept-shaped modules never emerge from file conventions — they have to be asked for.
3. **Existing code out-prompts guidance.** Five hand-maintained rows in a consumer file is a stronger instruction than any skill or doc: the next author adds a sixth row in six places. Treat "N touchpoints already exist" as evidence of a missing module, never as the pattern to extend.

## The shape (axis as data)

- **Rows, not branches.** An `as const` row table; unions derived via `(typeof rows)[number]`. The type system then enforces single ownership — you physically can't add a variant without a row, and no consumer can hold a stale hand-typed union.
- **The owner module is framework-free.** No React, no framework route types, no DOM. That's what makes the interface the test surface — one pure test file can prove every consumer's contract.
- **The framework layer stays thin adapters.** Entry points parse and pass; controllers derive the view model; views render it. If an adapter component needs substantial tests of its own, the module behind it isn't deep enough yet.
- **One tracer test through the interface, exercising real consumers,** with a few pinned wire-format literals as the anti-tautology anchor — instead of N mechanism tests that each pin the sprawl in place and turn later consolidation into a fight with your own suite.

## The procedure

Before writing implementation code for anything touching a variant axis:

1. **Name the axis** and the one module that owns it (a domain noun, not a mechanism noun).
2. **Show the interface** — ≤6 caller-facing entries, as signatures.
3. **State the next-variant delta.** The answer must be "one row."
4. **Checkpoint: stop for review before implementing.** It's signatures — the review is cheap; the sprawl it prevents is not.
5. **Proof** is one pure contract test through the interface exercising the real consumers.

The delta criterion is mechanically checkable after the fact: `git diff --stat` for variant N+1 should show the registry file, its test, and nothing else in product code.

## Failure signals

Any of these means stop and route through the rule before continuing:

- A new variant touches more than one product file.
- A hand-typed union restates registry contents anywhere.
- The same discriminant string gains a new `switch`/`if` branch in more than one file.
- Mechanism tests pin per-touchpoint literals for values the registry should own.

## The ask (delegation template)

When commissioning work on an axis, this paragraph is the whole contract:

> Before writing code: name the variant axis and the one module that owns it. Show me the public interface (≤6 caller-facing functions) and state what adding the _next_ variant touches — the answer must be "one row". Stop for my review before implementing. Proof is one pure contract test through that interface exercising the real consumers. Non-goals: no generic framework, this axis only.

The two load-bearing parts are the **checkpoint** (interface review before implementation) and the **delta criterion** in acceptance ("next variant = one row").

## Adjacent skills

- **`codebase-design`** — vocabulary, deep/shallow, seam discipline. Design-time companion; this skill decides _when_ a module must exist, that one decides _what makes it good_.
- **`design-an-interface` / DESIGN-IT-TWICE** — when the owner module's interface deserves competing designs.
- **`improve-codebase-architecture`** — the rescue mode: scanning an existing codebase for axes that already sprawled. If you're reaching for it on an axis younger than a month, this skill fired too late.
- Repos may pin a local reference shape and enforcement gate (e.g. a registry exemplar named in the repo's own agent docs, plus a review gate asserting the next-variant delta). Keep repo-specific exemplar names there, not here.
