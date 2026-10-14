---
name: audit-agent-context
description: Audita si AGENTS.md y/o CLAUDE.md del repo actual siguen reflejando la realidad del proyecto (estructura, comandos, convenciones, alcance) y reporta discrepancias sin editarlos. Usar cuando el usuario ejecute /audit-agent-context, pida verificar o actualizar la documentación de contexto para agentes, o sospeche que AGENTS.md/CLAUDE.md quedó desactualizado.
type: skill
tags: [agentes, documentacion, auditoria, agents-md, claude-md]
---

# Audit Agent Context — Auditar AGENTS.md / CLAUDE.md contra la realidad del repo

## Goal

Detectar y reportar — **nunca corregir en automático** — discrepancias entre lo que declaran
`AGENTS.md` y/o `CLAUDE.md` del proyecto y el estado real del repositorio: estructura de
carpetas, comandos, stack, convenciones de nombres, alcance declarado y reglas de coordinación
multi-agente. La skill entrega un reporte clasificado; las ediciones las decide y aplica el
usuario en un paso posterior y explícito.

## Cuándo se dispara

- El usuario ejecuta `/audit-agent-context`.
- Pide cosas como "revisá si el AGENTS.md sigue siendo verdad", "actualizá el contexto de
  agentes", "¿el CLAUDE.md quedó desactualizado?", o equivalentes.

## Input

Ninguno obligatorio. Opcionalmente, una ruta de proyecto distinta al cwd (por ejemplo si se
está auditando un subproyecto o un worktree).

## Workflow

1. **Resolver alcance.**
   - Raíz de proyecto: `git rev-parse --show-toplevel` (si falla, usar el cwd).
   - Localizar todos los `AGENTS.md` y `CLAUDE.md` relevantes: raíz del repo, cwd si es
     distinto, y cualquiera anidado en subcarpetas de trabajo declaradas. No asumir que solo hay
     uno de cada uno — puede haber pares en más de un nivel.

2. **Extraer afirmaciones verificables** de cada archivo encontrado, sin reescribirlas. Buscar
   específicamente:
   - Rutas y nombres de archivo/carpeta mencionados (¿existen? ¿siguen ahí?).
   - Comandos citados (build, lint, test, `gentle-ai ...`, `herdr ...`, etc.) — ¿el
     binario/script referenciado existe o es invocable?
   - Afirmaciones negativas ("no hay código", "no hay package.json", "no hay tests") — ¿siguen
     siendo ciertas?
   - Convenciones de nombres/estructura declaradas (ej. `HU-0X-<slug>.md`,
     `PLAYBOOK-<ROL>.md`) — ¿los archivos reales las cumplen?
   - Alcance declarado (qué carpetas cubre ese AGENTS.md/CLAUDE.md) vs. la ubicación real del
     archivo en el árbol.
   - Reglas de coordinación multi-agente (rutas de playbooks, nombres de skills, comandos de
     invocación).

3. **Verificar cada afirmación contra el repo real.**
   - Usar Glob/Grep/Read para estructura y contenido; `git ls-files` / `git status` para lo
     trackeado vs. lo sin trackear.
   - Si el repo tiene código y hay CodeGraph disponible, preferirlo para preguntas de
     arquitectura real antes de un grep amplio (regla ya vigente a nivel global para preguntas
     estructurales).
   - Para comandos, verificar que el binario/skill exista (`.claude/skills`, `.agents/skills`,
     scripts de `package.json`, etc.) — no ejecutar comandos con efectos secundarios solo para
     "probar" que funcionan.

4. **Clasificar cada afirmación** para el reporte final:
   - ✅ **Vigente** — coincide con la realidad.
   - ⚠️ **Desactualizada** — contradice el estado real (citar evidencia: qué dice el archivo vs.
     qué se encontró).
   - ❓ **No verificable automáticamente** — requiere confirmación humana (ej. decisiones de
     negocio o de alcance futuro).
   - 🆕 **No documentada** — el repo tiene algo (carpeta, convención, skill, playbook) que ningún
     AGENTS.md/CLAUDE.md menciona.

5. **Entregar el reporte** agrupado por archivo auditado (si hay más de uno). Cada ítem incluye:
   afirmación textual citada, evidencia encontrada y clasificación. Cerrar con una lista de
   cambios sugeridos, redactados como propuestas puntuales (no aplicadas), para que el usuario
   decida cuáles llevar al archivo.

## Reglas no negociables

- **Nunca editar `AGENTS.md`/`CLAUDE.md` dentro de esta skill.** Aplicar las correcciones es un
  paso posterior y explícito, fuera del alcance de esta auditoría.
- **Nunca asumir intención no confirmada.** Si una afirmación es ambigua o depende de una
  decisión de negocio/equipo, se marca ❓, no se resuelve por conjetura.
- Si el proyecto auditado tiene sus propias reglas de dominio (por ejemplo, "Puntos Abiertos" o
  "Alcance — No incluye" como en este mismo test-project), esta skill se somete a esas reglas
  también: no inventa alcance ni resuelve conflictos en silencio.
- Si no se encuentra ningún `AGENTS.md` ni `CLAUDE.md` en el alcance resuelto, reportarlo
  explícitamente — no es un fallo silencioso.

## Notas

- Esta skill es de solo lectura sobre el repo: no escribe archivos ni hace commits.
- Los pasos 2–4 son genéricos, no hardcodeados a la estructura de `test-project`: sirve para
  auditar el contexto de agentes de cualquier repo donde se invoque.
