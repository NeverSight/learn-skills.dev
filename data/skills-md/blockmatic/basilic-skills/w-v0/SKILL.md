---
name: w-v0
description: Draft a Next.js and shadcn v0.dev prompt from the current file and wait for OPEN, EDIT, or CANCEL.
disable-model-invocation: true
---

Produce a v0 prompt from the current file, selection, and stack. Do not open v0 until the user replies OPEN.

1. Draft a concise prompt: App Router, TypeScript, Tailwind, shadcn, server components by default, accessible HTML, mobile-first, no secrets or repo-internal paths.
2. Show the prompt and wait for OPEN, EDIT:, or CANCEL.
3. On EDIT:, revise and wait again. On CANCEL, stop. On OPEN, URL-encode and open `https://w-v0.dev?chat={prompt}`. Reply only that v0 opened; do not dump the URL if it contains the full prompt.
4. Docs: `/w-docs` if behavior or commands changed.
