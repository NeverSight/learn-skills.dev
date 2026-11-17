---
name: project-guidelines-example
description: "Example project-specific skill template based on a real production application."
origin: ECC
---

# Project Guidelines Skill (Example)

This is an example of a project-specific skill. Use this as a template for your own projects.

Based on a real production application: [Zenith](https://zenith.chat) - AI-powered customer discovery platform.

## When to Use

Reference this skill when working on the specific project it's designed for. Project skills contain:
- Architecture overview
- File structure
- Code patterns
- Testing requirements
- Deployment workflow

> This is a **template**. Keep your own project skill lean: describe structure and rules inline, and push full code samples to a `reference/` file (as this example does — see [reference/example-code.md](reference/example-code.md)).

---

## Architecture Overview

**Tech Stack:**
- **Frontend**: Next.js 15 (App Router), TypeScript, React
- **Backend**: FastAPI (Python), Pydantic models
- **Database**: Supabase (PostgreSQL)
- **AI**: Claude API with tool calling and structured output
- **Deployment**: Google Cloud Run
- **Testing**: Playwright (E2E), pytest (backend), React Testing Library

**Services:**
```
Frontend (Next.js + TypeScript + TailwindCSS)
        │
        ▼
Backend (FastAPI + Python 3.11 + Pydantic)
        │
   ┌────┼────┐
   ▼    ▼    ▼
Supabase  Claude  Redis
Database   API    Cache
```

---

## File Structure

```
project/
├── frontend/
│   └── src/
│       ├── app/              # Next.js app router pages (api/, (auth)/, workspace/)
│       ├── components/       # React components (ui/, forms/, layouts/)
│       ├── hooks/            # Custom React hooks
│       ├── lib/              # Utilities
│       ├── types/            # TypeScript definitions
│       └── config/           # Configuration
│
├── backend/
│   ├── routers/              # FastAPI route handlers
│   ├── models.py             # Pydantic models
│   ├── main.py               # FastAPI app entry
│   ├── auth_system.py        # Authentication
│   ├── database.py           # Database operations
│   ├── services/             # Business logic
│   └── tests/                # pytest tests
│
├── deploy/                   # Deployment configs
├── docs/                     # Documentation
└── scripts/                  # Utility scripts
```

---

## Code Patterns (Summary)

Document the canonical patterns your project uses. This example covers four; full code is in [reference/example-code.md](reference/example-code.md):

- **API Response Format (FastAPI)** — a generic `ApiResponse[T]` envelope with `ok()` / `fail()` constructors.
- **Frontend API Calls (TypeScript)** — a typed `fetchApi<T>()` wrapper returning the same envelope shape.
- **Claude AI Integration** — structured output via tool calling, parsing the `tool_use` block into a Pydantic model.
- **Custom Hooks (React)** — a `useApi<T>()` hook managing `data` / `loading` / `error` state.

---

## Testing Requirements

- **Backend**: `poetry run pytest tests/ --cov=.` — async fixtures with `httpx.AsyncClient`.
- **Frontend**: `npm run test` (unit), `npm run test:e2e` (Playwright) — React Testing Library.

> Full test commands and example test files: [reference/example-code.md](reference/example-code.md).

---

## Deployment Workflow

### Pre-Deployment Checklist

- [ ] All tests passing locally
- [ ] `npm run build` succeeds (frontend)
- [ ] `poetry run pytest` passes (backend)
- [ ] No hardcoded secrets
- [ ] Environment variables documented
- [ ] Database migrations ready

> Deployment commands (Cloud Run) and the full environment-variable list: [reference/example-code.md](reference/example-code.md).

---

## Critical Rules

1. **No emojis** in code, comments, or documentation
2. **Immutability** - never mutate objects or arrays
3. **TDD** - write tests before implementation
4. **80% coverage** minimum
5. **Many small files** - 200-400 lines typical, 800 max
6. **No console.log** in production code
7. **Proper error handling** with try/catch
8. **Input validation** with Pydantic/Zod

---

## Reference Files

- [reference/example-code.md](reference/example-code.md) — full code samples for the patterns above: API response envelope (FastAPI + TypeScript), Claude structured-output integration, React `useApi` hook, backend/frontend test commands and example test files, and deployment commands plus environment variables.

---

## Related Skills

- `coding-standards.md` - General coding best practices
- `backend-patterns.md` - API and database patterns
- `frontend-patterns.md` - React and Next.js patterns
- `tdd-workflow/` - Test-driven development methodology
