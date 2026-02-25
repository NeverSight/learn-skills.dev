---
name: vue-doctor
description: Diagnose and fix Vue/Nuxt codebase health issues. Use when reviewing Vue code, fixing performance problems, auditing security, or improving code quality.
version: 1.0.0
---

# Vue Doctor

Scans your Vue/Nuxt codebase for security, performance, correctness, and architecture issues. Outputs a 0-100 score with actionable diagnostics.

## Usage

```bash
npx -y vue-doctor@latest . --verbose
```

## Workflow

1. Run the command above at the project root
2. Read every diagnostic with file paths and line numbers
3. Fix issues starting with errors (highest severity)
4. Re-run to verify the score improved

## Rules (30+)

- **Security**: v-html XSS risks, eval(), hardcoded secrets in client code
- **Composition API**: watch as computed, async watchEffect, reactive destructuring, ref in computed
- **Performance**: index as key, deep watch, expensive template expressions, method calls in v-for
- **Architecture**: prop mutation, missing emits declaration, giant components
- **Correctness**: v-if with v-for, this in setup, direct DOM manipulation, missing prop types
- **Nuxt**: window in SSR, missing SEO meta, process.env in client, server route error handling
- **Bundle Size**: barrel imports, full lodash, moment.js, heavy libraries
- **Accessibility**: missing prefers-reduced-motion for motion libraries
- **Dead Code**: unused files, exports, types

## Score

- **75+**: Great
- **50-74**: Needs work
- **0-49**: Critical
