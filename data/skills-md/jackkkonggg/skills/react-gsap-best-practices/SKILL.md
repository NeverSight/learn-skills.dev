---
name: react-gsap-best-practices
description: Use when building, reviewing, or refactoring React components that use GSAP or @gsap/react (useGSAP, contextSafe, dependency-driven updates, ScrollTrigger integration, and SSR-safe setup) to enforce production-safe animation patterns.
---

# React GSAP Best Practices

Apply these rules when working on React codebases that use GSAP.

## Rule loading order

1. Read `rules/react-gsap-setup.md`.
2. Read `rules/react-gsap-lifecycle.md`.
3. Read `rules/react-gsap-scrolltrigger.md`.
4. Read `rules/react-gsap-ssr-strictmode.md`.
5. Use `AGENTS.md` as a compact summary plus pointer.

## Enforcement policy

- Use recommendation-first language for style and performance guidance.
- Use strict language (`must` / `must not`) only for lifecycle correctness, memory safety, and accessibility constraints.
- Prefer official React and GSAP docs when resolving conflicts; update these rules when docs change.
