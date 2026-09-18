---
name: w-form
description: Build a Next.js form using the app's existing mutation path, not a second stack.
disable-model-invocation: true
---

Implement a form in the current Next app. Follow `next-v16` and `shadcn-v3`. If the app already mutates through an API client (Fastify + TanStack Query), do not introduce Server Actions, `useFormStatus`, or `useOptimistic` for those flows.

1. Inspect how neighboring forms submit. Reuse that path.
2. Share one Zod schema for client UX and server validation.
3. Wire accessible labels, errors, pending, and empty/error/success states with existing UI primitives.
4. Run lint and exercise submit, validation failure, and keyboard path.
5. Docs: `/w-docs` if behavior or commands changed.
