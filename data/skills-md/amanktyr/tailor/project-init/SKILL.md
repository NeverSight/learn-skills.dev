---
name: project-init
description: Guides project initialization, interactive product discovery, developer expertise assessment, stack selection matrix, and automated Architecture Decision Record (ADR) setup.
---

# Project Initialization Skill

Activate this skill when bootstrapping a new project from scratch, establishing architectural baselines, or executing `/init-project`.

> **Operational Directive:** *Never write code before establishing product scope, technical requirements, and developer expertise.*

---

## 1. Product Discovery Questionnaire

Before recommending or installing any framework, gather critical product invariants:

1. **Target Product & Core Value Proposition:** What is being built, what core problem does it solve, and who are the primary users?
2. **Platform & Modality:** Public SaaS, internal dashboard, mobile API, desktop application, or developer CLI?
3. **Scale & Traffic Expectations:** Prototype / MVP, internal team tool (<100 users), or high-throughput multi-tenant production system?
4. **Data Model & Concurrency:** Relational data (PostgreSQL/MySQL), document-based (MongoDB), key-value cache (Redis), or embedded (SQLite)?
5. **Deployment & Runtime Constraints:** Serverless (Vercel/Cloudflare Workers), containerized cluster (Docker/Kubernetes), single VPS, or static hosting?

---

## 2. Developer Expertise Matrix

Assess the developer's familiarity level (`Beginner`, `Intermediate`, `Advanced`, `Expert`):
- **Languages:** TypeScript, Python, Go, Rust, C#, PHP, Java
- **Frontend Frameworks:** Next.js (App Router), React (SPA), Vue / Nuxt, SvelteKit, Vanilla HTML/CSS
- **Backend Frameworks:** Express / Fastify, NestJS, Django / FastAPI, Go Gin / Echo, ASP.NET Core, Laravel
- **Databases & ORMs:** Prisma, Drizzle, TypeORM, SQLAlchemy, Django ORM, Entity Framework Core, Raw SQL

*Rule:* **Never recommend a complex, unfamiliar stack for an urgent MVP if a well-understood, robust alternative achieves the goal in half the time.**

---

## 3. Technology Stack Recommendation Matrix

| Project Archetype | Recommended Stack | Key Rationale |
| :--- | :--- | :--- |
| **Full-Stack SaaS / Web App** | Next.js (App Router) + TypeScript + Tailwind CSS + PostgreSQL + Prisma/Drizzle | Unified language, fast server-side rendering, robust ORM, rapid UI iterations |
| **High-Performance API Service** | Go (net/http + Gin) OR FastAPI (Python) + PostgreSQL + Redis | High concurrency, low memory footprint, strict typing, auto-generated OpenAPI |
| **Data Science / ML Backend** | Python + FastAPI + PyTorch / Scikit-learn + PostgreSQL + Celery/Redis | Native ML ecosystem support, async performance, robust data processing |
| **Enterprise Internal Tool** | Next.js + React + shadcn/ui + PostgreSQL + Supabase / Auth.js | Rapid scaffolding, enterprise UI primitives, integrated authentication |
| **Fast Developer CLI Tool** | Node.js (TypeScript + Commander + Picocolors) OR Rust (Clap) | Zero-config distribution via `npx`, fast startup, deterministic execution |
| **Micro-Service / Embedded** | Go OR Rust + SQLite / PostgreSQL | Zero runtime dependencies, single static binary, instant cold start |

---

## 4. Initialization Output & Memory Scaffolding

Upon stack confirmation, generate the baseline architecture:
1. Initialize `.ai/` memory directory with:
   - `INDEX.md`: Top-level memory index.
   - `CONSTITUTION.md`: Project non-negotiables, intensity mode, and coding standards.
   - `STACK.md`: Confirmed frameworks, runtimes, and dependencies.
   - `ARCHITECTURE.md`: High-level system topology and boundaries.
   - `DECISIONS.md`: Initial **ADR-001 (Technology Stack & Baseline Architecture)**.
2. Synchronize multi-agent adapter rules (`CLAUDE.md`, `.cursorrules`, `AGENTS.md`, `GEMINI.md`).
