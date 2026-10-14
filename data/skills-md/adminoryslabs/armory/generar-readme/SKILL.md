---
name: generar-readme
description: Genera un README.md pensado para que un evaluador externo entienda y corra el proyecto en minutos — quickstart real en 3 comandos (install, config, run), diagrama de arquitectura y stack, decisiones clave enlazadas a las ADRs, demo link/video, y resumen ejecutivo del problema resuelto y los aprendizajes. Use when the user asks to generate, write, or improve a README aimed at an evaluator, demo day, hackathon, or project submission.
---

# Evaluator README Generator

## Goal

Most READMEs are written for a teammate who already has context. This one is written for someone
who has never seen the project and has a few minutes to decide if it works and what it's about —
an evaluator, a judge, a reviewer. Every section exists to answer a specific question that person
will actually ask, in the order they'll ask it: what is this, can I run it, how is it built, why
was it built this way, does it actually work.

The primary outcome is a file written to disk: `README.md` at the project root.

## Non-negotiable rule

Every command and every claim in the README must be verified against the real project — its actual
package manager scripts, its actual entry points, its actual environment variables. Never invent a
command that looks plausible for the stack; check it. A quickstart that doesn't run is worse than
no quickstart, because it's the first thing an evaluator tries.

## Required Input

- The project's own files: manifest (`package.json`, `pyproject.toml`, `requirements.txt`,
  `Cargo.toml`, etc.), any existing `.env.example`, `docker-compose.yml`, entry scripts.
- `PRD.md`, if present — used for the executive summary's problem statement. If absent, ask the
  user for the problem in one or two sentences instead of inventing one.
- `TECH-DESIGN.md` and `adrs/*.md`, if present — used for the architecture section and the key
  decisions list. If absent, derive the architecture description directly from the repo's actual
  structure/services, and omit the "Decisiones clave" section rather than inventing decisions.
- Demo link or a ~3 min video — **ask the user for this**, don't fabricate a URL. If not available
  yet, the section says so explicitly instead of a placeholder link.
- Learnings for the executive summary — **ask the user directly**; this is a reflection only they
  can give. Do not fill it with generic filler like "aprendimos a trabajar en equipo."

## Workflow

### 1. Discover the real project

Read the manifest to determine the stack and the actual install/build/run scripts. Check for
`.env.example`/`.env.sample`. If none exists, grep the code for how it actually reads configuration
(`process.env.*`, `os.environ.*`, `os.Getenv`, config loaders) and generate a real
`.env.example` from that — never guess variable names.

### 2. Nail the 3-command quickstart

Determine, concretely, for this project:

1. **Install** — the real dependency-install command.
2. **Config** — copy/fill `.env.example` (or generate it per step 1 if missing).
3. **Run** — the real command that starts the project, dev or prod as appropriate.

If the project genuinely needs more than three steps (a DB migration, a seed command), say so
honestly and list the real steps — don't force a false "3 commands" claim to satisfy the format.
Keep it as tight as the project truly allows, no tighter.

### 3. Architecture and stack

Build a short diagram (a compact Mermaid diagram or a clear textual one, whichever the project's
complexity actually warrants) from real component boundaries: from `TECH-DESIGN.md` if available,
otherwise from the repo's actual folders/services/deployables. Pair it with a stack table by layer
(frontend / backend / data / infra) using the versions actually pinned in the manifest, not generic
names.

### 4. Key decisions

If `adrs/*.md` exist, list each with one line summarizing its `Decisión` and a direct relative link
(`adrs/000X-slug.md`). If no ADRs exist, omit this section entirely rather than writing a fake
"decisiones clave" with no substance.

### 5. Demo and executive summary

Ask for the demo link/video if not already provided. Write the executive summary from `PRD.md`'s
`Problema` and `Usuario objetivo` sections if available; otherwise ask the user directly for a
one-paragraph problem statement. Ask the user for real learnings — do not invent them.

### 6. Write the file

Assemble `README.md` using `assets/readme-template.md`. If a `README.md` already exists, ask
whether to overwrite it or merge the new sections into the existing structure — don't silently
replace content the user may have hand-written.

## README.md Sections, In Order

See `assets/readme-template.md` for the full template.

- Título + pitch de una línea
- Resumen ejecutivo (problema, para quién, aprendizajes)
- Demo (link / video ~3 min)
- Quickstart (Install, Config, Run — comandos reales)
- Arquitectura (diagrama + tabla de stack)
- Decisiones clave (enlaces a ADRs) — solo si existen ADRs
- Estructura del repo (opcional, solo si aporta algo que el árbol de carpetas no explica solo)

## Quality Gate

Before returning, silently check:

- Every command in Quickstart was verified against a real script or entry point in the project —
  none invented from "what a project like this usually runs."
- `.env.example` either already existed or was generated from real env-var reads in the code.
- No fabricated demo URL — if not provided, the section explicitly says "pendiente" instead of a
  placeholder link.
- Learnings and the problem statement (when no PRD exists) came from the user, not generic filler.
- The architecture section reflects the actual components found in the repo, not a generic
  three-tier template applied by default.
- "Decisiones clave" only appears if real ADRs exist to link to.

## References

- `assets/readme-template.md` — the exact structure `README.md` must follow.
