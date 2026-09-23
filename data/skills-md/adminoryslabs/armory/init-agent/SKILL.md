---
name: init-agent
description: Carga en la sesión actual el playbook de un rol de equipo ágil aumentado por IA (PM, BA, UX, ARCH) y adopta ese rol para el resto de la conversación, sin crear ni invocar ningún agente nuevo. Use when the user runs /init-agent, or asks to become/act as a specific team role (PM, BA, UX, Architect) in the current session.
type: skill
tags: [agentes, roles, playbook, herdr]
---

# Init Agent — Cargar un rol en la sesión actual

## Goal

Adoptar, en la sesión ya abierta, el rol de un agente de equipo (Product Manager, Business
Analyst, Diseñador/UX o Arquitecto de Software) leyendo su playbook y operando bajo ese rol de
ahí en adelante. Esta skill no toca herdr ni crea paneles — para eso está `invoke-agent`.

## Roles disponibles

| Rol | Playbook |
|---|---|
| `PM` | `references/PLAYBOOK-PM.md` |
| `BA` | `references/PLAYBOOK-BA.md` |
| `UX` | `references/PLAYBOOK-UX.md` |
| `ARCH` | `references/PLAYBOOK-ARCH.md` |

## Input

Un parámetro de rol (`PM`, `BA`, `UX` o `ARCH`), case-insensitive. Ejemplo: `/init-agent PM`.

Si no se especifica, o el valor no matchea ninguno de los cuatro, preguntar explícitamente cuál de
los cuatro roles cargar y esperar la respuesta antes de continuar. No asumir un rol por defecto.

## Workflow

1. Resolver el rol pedido al playbook correspondiente en `references/`.
2. Leer el playbook completo.
3. Adoptar el Rol, Proceso, Plantilla y Checklist del playbook como la identidad operativa de
   esta sesión a partir de este momento — no como un documento de referencia pasivo, sino como
   las reglas que rigen cada respuesta siguiente.
4. Confirmar al usuario, en una línea, qué rol quedó cargado y cuál es su entrada esperada (para
   que sepa qué pasarle a continuación).

## Notas

- El playbook cargado no se reescribe ni se resume: se aplica tal cual vive en `references/`.
- Si en algún momento se necesita traer a OTRO rol a colaborar dentro de una sesión de herdr
  (en un pane nuevo o reusando uno ya despierto), esa es tarea de `invoke-agent`, no de esta
  skill.
