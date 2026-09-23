---
name: invoke-agent
description: Busca en el workspace actual de herdr un agente ya despierto para el rol pedido (PM, BA, UX, ARCH); si no hay ninguno, crea un pane nuevo, levanta un agente Claude en él y le carga ese rol. Use when the user runs /invoke-agent, asks to hand off work to another agent/role, spawn a new agent, or bring a PM/BA/UX/Architect into a herdr session.
type: skill
tags: [agentes, roles, herdr, multi-agente]
---

# Invoke Agent — Invocar un rol en herdr

## Goal

Conseguir que un agente con el rol pedido (PM, BA o UX) esté disponible y con el playbook
cargado, dentro del **workspace de herdr actual** — reusando uno ya despierto si existe, o
creando uno nuevo con el comando más simple disponible si no. Para cargar un rol en la sesión
donde se está ejecutando ahora mismo, sin tocar herdr, usar `init-agent` en su lugar.

## Roles disponibles

Los mismos que `init-agent`: `PM`, `BA`, `UX`, `ARCH` (`references/PLAYBOOK-<ROL>.md`). Convención
de nombre de agente en herdr: el rol en minúscula (`pm`, `ba`, `ux`, `arch`).

## Input

Un parámetro de rol (`PM`, `BA`, `UX` o `ARCH`), case-insensitive. Ejemplo: `/invoke-agent BA`.

Si no se especifica, o no matchea ninguno de los cuatro, preguntar cuál rol invocar y esperar
respuesta. No asumir un rol por defecto.

## Workflow

1. **Determinar el workspace actual.** Leer la variable de entorno `HERDR_WORKSPACE_ID` (si no
   está disponible en el entorno, resolverla con `herdr pane get $HERDR_PANE_ID`).
2. **Listar los panes del workspace actual:** `herdr pane list --workspace <workspace_id>`.
3. **Listar los agentes vivos:** `herdr agent list`.
4. **Cruzar ambos listados.** Buscar un agente cuyo `pane_id` esté entre los panes del workspace
   actual (paso 2) y cuyo nombre coincida con la convención del rol pedido (`pm`/`ba`/`ux`/`arch`). Un
   agente despierto con el rol correcto pero en **otro** workspace no cuenta — se ignora.
   - **Si existe** en el workspace actual → es el destinatario. Ir al paso 6.
   - **Si no existe** en el workspace actual → ir al paso 5.
5. **Crear un agente nuevo en el workspace actual**, con el comando más simple disponible (no
   crear un workspace nuevo si ya hay uno activo):
   1. Si el nombre del rol (`pm`/`ba`/`ux`/`arch`) ya está tomado por un agente vivo en otro workspace
      (visible en el listado del paso 3), elegir un nombre libre agregando un sufijo numérico
      (`ba-2`, `ba-3`, ...) — herdr exige nombres únicos entre agentes vivos, sin importar el
      workspace.
   2. `herdr pane split --current --direction right --focus` → capturar el `pane_id` devuelto.
   3. `herdr agent start <nombre-resuelto> --kind claude --pane <pane_id>`.
6. **Entregarle el rol y el trabajo** al agente (nuevo o reusado):
   1. `herdr agent prompt <target> "/init-agent <ROL>"` — para que se cargue el playbook a sí
      mismo en lugar de pegarlo por texto.
   2. Un segundo `herdr agent prompt <target> "<encargo concreto>"` (agregar `--wait --until idle`
      si se necesita confirmar que lo procesó) con la tarea real: dónde está el insumo (PRD, HU,
      etc.), contexto mínimo del proyecto y cualquier punto abierto relevante.
7. Confirmar al usuario, en una línea, si se reusó un agente existente o se creó uno nuevo, y su
   `pane_id`/nombre.

## Notas

- Depende de que `init-agent` esté instalado en el mismo entorno del agente invocado. Si no lo
  está, pegar el contenido completo del playbook correspondiente en el primer
  `herdr agent prompt` en su lugar.
- Nunca reusar un agente del rol pedido si está despierto en otro workspace, aunque esté idle.
- Si `herdr agent start` falla por nombre ya ocupado (ej. un agente muerto no liberó el nombre a
  tiempo), diagnosticar con `herdr agent list`/`herdr agent get` antes de reintentar a ciegas con
  otro nombre.
