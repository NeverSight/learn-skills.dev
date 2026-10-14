---
name: preparar-sprint0
description: Prepara el Sprint 0 (walking skeleton) de un proyecto a partir de su Tech Design y ADRs - clasifica los ADRs en transversales y de historia, define el mapa de propiedad de rutas por rol, escribe la Definition of Done del esqueleto y propone un plan, y se detiene para aprobación humana. Use when the LEAD (or the user) needs to prepare, plan, or initialize the Sprint 0 / walking skeleton of a project before any user story is built.
type: skill
tags: [lead, sprint0, walking-skeleton, dod, adrs]
---

# Preparar Sprint 0

## Goal

Convertir *"inicializa el proyecto"* en una unidad de trabajo **acotada y verificable**: el
esqueleto mínimo que funciona de punta a punta, sin lógica de negocio. El resultado es un único
documento, `SPRINT0.md`, que leen por igual el TESTER y el DEV.

**Esta skill no construye nada.** Prepara, propone y se detiene.

## Input

- `TECH-DESIGN.md` y `adrs/` — **obligatorios**. Si faltan, detenerse y pedirlos.
- `AGENTS.md` y/o `CLAUDE.md` del proyecto — si existen, se leen y luego se actualizan (paso 5).
- HUs — **no se leen para construir**. Solo se consultan para saber a qué historia pertenece cada
  ADR de historia.

## Workflow

1. **Leer el Tech Design y todos los ADRs.**

2. **Clasificar cada ADR** en una de tres categorías, con una línea de justificación:
   - **Transversal** — se necesita para que el proyecto exista (stack, estructura, estilo de API,
     ORM, manejo de estado general). **Aplica en el Sprint 0.**
   - **De historia** — resuelve una funcionalidad concreta. **No aplica en el Sprint 0**; se anota
     a qué HU(s) pertenece.
   - **Mixto / a discutir** — parte es transversal y parte es de historia. Se explica qué parte
     aplica ahora y se marca para que el humano lo confirme.
   Pregunta guía: *"¿Esto lo necesito para que el proyecto exista, o para una funcionalidad
   concreta?"*

3. **Definir el mapa de propiedad de rutas** según el stack real del proyecto (no según un stack
   asumido):
   - **TESTER** — las rutas donde viven las pruebas según la convención del framework de pruebas
     elegido (y sus fixtures o datos de prueba).
   - **DEV** — el código de la aplicación, su configuración, migraciones y el manifiesto de
     dependencias.
   - **Solo LEAD / humano** — los archivos del harness: `AGENTS.md`, `CLAUDE.md`, carpetas de
     skills y de configuración de agentes, `SPRINT0.md`, contratos.
   Si una ruta no encaja claramente, se marca como pregunta para el humano.

4. **Escribir la Definition of Done del esqueleto.** Cada punto debe ser **verificable** y decir
   **cómo** se verifica (prueba o comando). Mínimo:
   - la aplicación arranca en local;
   - se conecta a sus dependencias principales (ej. base de datos), si los ADRs transversales las
     incluyen;
   - existe un punto de verificación de salud (ej. una ruta o comando de health) con nombre exacto;
   - el runner de pruebas está instalado, configurado y se ejecuta;
   - respeta los ADRs transversales;
   - **cero lógica de negocio**.
   Los nombres exactos (rutas, comandos) se escriben en la DoD: son el contrato mínimo que permite
   a TESTER y DEV trabajar sin verse.

5. **Escribir el plan** usando `assets/sprint0-template.md`: qué crea el DEV, qué crea el TESTER,
   y **qué NO se crea** (todo lo que pertenece a ADRs de historia).

6. **Guardar `SPRINT0.md`** en la raíz del proyecto y **agregar el mapa de propiedad de rutas** a
   `AGENTS.md` (y a `CLAUDE.md` si también existe), en una sección `## Propiedad de rutas`.

7. **Detenerse.** Presentar al humano: la clasificación de ADRs, el mapa de rutas, la DoD y el
   plan, más la lista de preguntas abiertas. **No invocar a nadie ni crear archivos de
   aplicación.** Si el humano pide cambios, se ajusta `SPRINT0.md` y se vuelve a presentar.

## Constraints

- No se implementa ningún ADR de historia, aunque parezca trivial.
- No se elige un stack que los ADRs no fijan: si falta una decisión, es una pregunta.
- Un punto de la DoD que no se puede verificar no entra en la DoD.
- No se publica nada (ni push a main, ni deploy).
