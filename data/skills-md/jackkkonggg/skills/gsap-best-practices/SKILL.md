---
name: gsap-best-practices
description: Use when writing, reviewing, or refactoring GSAP animation code in JavaScript/TypeScript (tweens, timelines, ScrollTrigger, matchMedia, plugin usage, and performance tuning) to enforce production-safe animation patterns.
---

# GSAP Best Practices

Apply these rules when working on GSAP-powered animation codebases.

## Current platform note

- As of March 6, 2026, official GSAP docs state that all plugins, including former Club GSAP bonus plugins, are freely available in the public package. Use the standard `gsap` package and do not recommend legacy private-registry or paid-only installation flows. Prefer GSAP `3.13+` when this matters.

## Rule loading order

1. Read `rules/gsap-core.md`.
2. Read `rules/gsap-timelines.md`.
3. Read `rules/gsap-scrolltrigger.md`.
4. Read `rules/gsap-performance.md`.
5. Use `AGENTS.md` as a compact summary plus pointer.

## Enforcement policy

- Use recommendation-first language for style and performance guidance.
- Use strict language (`must` / `must not`) only for correctness, stability, and accessibility constraints.
- Prefer official GSAP docs when resolving conflicts; update these rules when docs change.
