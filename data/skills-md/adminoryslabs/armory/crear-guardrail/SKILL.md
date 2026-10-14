---
name: crear-guardrail
description: Crea un guardrail o hook en el agente de programación que se está usando (Claude Code, OpenCode, Codex, Antigravity u otro) - detecta qué agente es, consulta su documentación oficial vigente sobre hooks y permisos, propone el guardrail, espera aprobación, lo configura de forma nativa y lo prueba provocando el evento. Use when the user asks to create, add, or configure a guardrail, hook, permission rule, or automatic block/check for their coding agent.
type: skill
tags: [harness, guardrails, hooks, permisos, agnostico]
---

# Crear guardrail

## Goal

Convertir una **regla** ("nadie hace push a main") en un **límite real** del entorno, configurado
de forma nativa en el agente que se está usando. La skill no trae recetas por agente: trae el
**procedimiento** para que el agente aprenda a configurarse a sí mismo con su documentación
vigente.

## Input

- **La regla a hacer cumplir**, en lenguaje natural. Ejemplos de guardrails transversales:
  - bloquear `git push` a la rama principal y `git push --force`;
  - bloquear comandos destructivos sobre el sistema de archivos fuera del proyecto;
  - pedir confirmación antes de cualquier deploy o escritura contra un servicio remoto;
  - impedir la lectura o escritura de archivos de secretos (`.env` y similares).
- Opcional: si debe aplicar a nivel de proyecto (todo el equipo) o de usuario.

Si la regla no es clara (qué acción, qué excepción), preguntar antes de seguir.

## Workflow

1. **Detectar qué agente está corriendo** esta sesión (por su propia identidad, variables de
   entorno o archivos de configuración presentes en el proyecto). Decirlo al usuario en una línea.

2. **Consultar la documentación oficial vigente** de ese agente sobre hooks, permisos o
   políticas. Usar `references/puntos-de-partida.md` solo como punto de partida: **si la
   documentación actual difiere, gana la documentación actual**. Si el agente no tiene acceso a
   la web, decirlo y pedir al usuario el enlace o el fragmento de documentación.

3. **Elegir el mecanismo más simple que haga cumplir la regla:**
   - si el agente tiene **permisos declarativos** (allow/deny/ask) que alcanzan, usar eso;
   - si no alcanza, usar un **hook** sobre el evento correspondiente (ej. antes de ejecutar un
     comando);
   - si el agente no ofrece ningún mecanismo, decirlo explícitamente y proponer la alternativa
     menos frágil (y dejar la regla también escrita en `AGENTS.md`).

4. **Proponer el guardrail al usuario antes de escribir nada:**
   - qué evento lo dispara;
   - qué bloquea, pide confirmar o ejecuta;
   - en qué archivo de configuración queda y con qué alcance (proyecto / usuario);
   - qué podría bloquear por error (falsos positivos).
   **Esperar aprobación explícita.**

5. **Configurarlo** en el archivo nativo del agente, sin borrar configuración existente.

6. **Probarlo provocando el evento** de forma segura (ej. un `git push` a main en una rama de
   prueba o en modo simulación) y mostrar al usuario que el guardrail actuó. Si no actuó, se
   corrige antes de darlo por terminado.

7. **Registrarlo** en `AGENTS.md`, sección `## Guardrails`: la regla, el mecanismo, el archivo
   donde vive y cómo se probó. Así el resto del equipo (humano o agente) sabe que existe.

## Constraints

- No se instala nada que el usuario no haya aprobado.
- No se desactivan guardrails existentes para crear uno nuevo.
- Un guardrail que no se probó no se da por creado.
- Si el agente no permite hacer cumplir la regla, se dice: la regla queda como regla escrita, no
  como falso guardrail.
