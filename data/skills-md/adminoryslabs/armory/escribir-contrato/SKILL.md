---
name: escribir-contrato
description: Escribe el contrato observable de una Historia de Usuario para que el TESTER y el DEV puedan trabajar al mismo tiempo sin verse - arma el paquete de contexto (HU + ADRs de historia + sección del Tech Design), define entrada, salida por caso, errores y nombres que no se negocian con el origen de cada línea, lista las decisiones que la HU no tomaba y se detiene para aprobación humana. Use when the LEAD takes a user story to build, or when asked to write, draft, or version the contract/spec of a user story.
type: skill
tags: [lead, contrato, spec, hu, caja-negra]
---

# Escribir contrato

## Goal

Producir el **único documento que leen el TESTER y el DEV**: lo que la HU tiene que hacer **vista
desde afuera**, con la precisión suficiente para que dos agentes que no se ven lleguen al mismo
resultado. El contrato fija lo observable; lo interno queda libre para el DEV.

**Esta skill no construye nada.** Escribe, pregunta y se detiene.

## Input

- **La HU** — desde Jira vía MCP si está conectado, o el archivo/enlace indicado. Si tiene puntos
  abiertos sin resolver, **detenerse**: se escalan antes de escribir el contrato.
- `TECH-DESIGN.md` — la sección y los criterios de aceptación que corresponden a esta HU.
- `adrs/` — **solo los ADRs de historia** de esta HU (y los transversales que condicionan su
  interfaz, ej. estilo de API).
- `AGENTS.md` — convenciones del proyecto.
- Contratos anteriores en `contratos/` — para no contradecir nombres ya fijados.

## Workflow

1. **Armar el paquete de contexto:** HU + ADRs que aplican + sección del TDD. Nada más. Listar
   qué entró al paquete y por qué.

2. **Identificar la interfaz observable** por la que se usa la funcionalidad (una ruta HTTP, una
   pantalla, un comando, un evento…). El contrato se escribe sobre esa interfaz.

3. **Por cada escenario Gherkin y cada criterio de aceptación del TDD**, derivar los casos:
   - **entrada** exacta (ruta, parámetros, formato);
   - **salida** exacta por caso (status, datos, texto visible, efecto persistente);
   - **errores** (qué entrada inválida produce qué respuesta).

4. **Fijar los nombres que no se negocian:** rutas, campos, mensajes visibles, formatos. Son los
   que el TESTER verificará textualmente.

5. **Anotar el origen de cada línea** (escenario Gherkin, criterio del TDD, ADR). Una línea sin
   origen es una **decisión nueva**: se marca `DECISIÓN PROPUESTA` y entra en la lista de
   preguntas para el humano. Nunca se presenta como si viniera de la HU.

6. **Declarar qué queda fuera del contrato** (todo lo interno: estructura, nombres de funciones,
   consultas) → libertad del DEV.

7. **Guardar** `contratos/CONTRATO-<HU>.md` con `assets/contrato-template.md`, versión `v1`.

8. **Detenerse.** Presentar el contrato y las preguntas al humano. No invocar a nadie.

## Versionado

Cuando durante el ciclo aparece un hueco (lo reporta el TESTER, el DEV o el veredicto):

1. se formula la pregunta al humano;
2. con la respuesta, se edita el contrato, se sube la versión (`v2`, `v3`…) y se agrega una fila
   al changelog (qué cambió, por qué, quién lo aprobó);
3. el LEAD avisa a TESTER y DEV de la nueva versión.

## Constraints

- No se completa con suposiciones lo que la HU no dice: se pregunta.
- No se describe implementación interna en el contrato.
- No se contradice un nombre fijado en un contrato anterior sin decirlo explícitamente.
- No se publica nada.
