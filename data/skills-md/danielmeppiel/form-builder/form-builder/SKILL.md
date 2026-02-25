---
name: form-builder
description: Build accessible forms with React Hook Form + Zod
license: MIT
metadata:
  author: danielmeppiel
  version: "1.0.0"
compatibility: React 18+, TypeScript 5+
---

# Form Builder

Build accessible, type-safe forms in React.

## When to Use

Activate when user asks to:
- Create any form (contact, signup, login, checkout, etc.)
- Add form validation
- Handle form submission

## Stack

- **React Hook Form** — form state, minimal re-renders
- **Zod** — schema validation
- **@hookform/resolvers** — connects them

## Examples

- [Contact form](examples/contact-form.tsx) — full implementation
- [Newsletter signup](examples/newsletter-signup.tsx) — minimal implementation

## Install

```bash
npm install react-hook-form @hookform/resolvers zod
```
