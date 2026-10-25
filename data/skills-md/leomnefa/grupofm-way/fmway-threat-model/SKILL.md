---
name: fmway-threat-model
version: 1.0.0
description: Usar para construir un modelo de amenazas chico y acotado sobre el trabajo actual o sobre código nuevo — una feature, un servicio, una API o los cambios de la rama actual. Descompone el sistema en activos, puntos de entrada y fronteras de confianza, enumera amenazas con STRIDE y registra mitigaciones y riesgo residual en un informe trazable con un diagrama de flujo de datos. Se invoca por separado para modelar un componente, o desde otro flujo (fmway-dev después del PRD o el plan, fmway-bugs para una corrección con impacto de seguridad) para exponer amenazas antes de escribir o entregar el código. Especialmente importante para superficies externas nuevas, flujos de autenticación, pagos o datos personales, y cambios en las fronteras de confianza.
---

# Proceso de modelado de amenazas

Flujo guiado por gates para producir un **modelo de amenazas chico y acotado** del trabajo actual —una
feature planificada, un módulo, una API o los cambios de la rama actual— con una pasada liviana de
STRIDE sobre los flujos de datos y las fronteras de confianza del sistema. El objetivo es un modelo
práctico y trazable que impulse mitigaciones, no un artefacto corporativo exhaustivo. La salida vive
en `docs/security/threat-models/{slug}/THREAT-MODEL.md`.

Dos modos de invocación:

- **Autónomo (modelar un componente o un cambio):** rama propia `assess/threat-{slug}` → PR a
  `develop`.
- **Embebido en otro flujo:** escribe en la **rama o worktree de quien llama**; el modelo viaja con el
  PR de ese flujo. Sin rama ni PR separados. Ejemplos: `fmway-dev` corriendo un modelo de amenazas
  justo después del PLAN en el Gate 2 (para que las mitigaciones se conviertan en tareas del plan);
  `fmway-bugs` modelando una corrección con impacto de seguridad.

Es un **flujo de evaluación**. Igual que `fmway-docs`, **no** mantiene un `.ways/state.json`.
Identifica amenazas y propone mitigaciones; implementar una mitigación es una tarea del flujo que
llama o un ítem posterior de `fmway-dev` o `fmway-bugs`.

Mantenelo **chico.** Escalá el modelo al cambio: un endpoint nuevo necesita un diagrama de flujo de
datos y un puñado de amenazas, no un documento de 40 páginas. La profundidad sigue al riesgo.

---

## Fase 0 — Alcance y descomposición

**Objetivo:** entender la porción del sistema lo suficiente como para razonar sobre amenazas. Solo
lectura.

### Relevamiento inicial

1. Confirmá el **objetivo**: una feature planificada (desde su PRD o PLAN), un módulo o servicio, una
   API, o **el diff de la rama actual** (código nuevo).
2. Leé primero el contexto relevante: el PRD y el PLAN (si estás embebido en desarrollo), la
   documentación en `docs/architecture/`, cualquier modelo de amenazas previo, la sección de seguridad
   del `CLAUDE.md` y un `VALIDATION.md` si existe (ver `fmway-security`).

### Descomponer el objetivo

Identificá, anclado en el código o el diseño:

- **Activos** — qué vale la pena proteger (datos personales, credenciales, datos de pago, tokens,
  movimiento de dinero, integridad de registros, disponibilidad de un flujo).
- **Actores** — quién interactúa (usuarios finales, administradores, llamadores anónimos, servicios
  internos, terceros) y su nivel de privilegio.
- **Puntos de entrada** — rutas, endpoints, consumidores de mensajes, subida de archivos, CLI, tareas
  programadas.
- **Fronteras de confianza** — dónde los datos cruzan un cambio de privilegio o de propiedad
  (internet→servicio, servicio→base de datos, servicio→tercero, inquilino→inquilino).
- **Flujos de datos** — cómo se mueven los datos entre actores, procesos y almacenamientos a través de
  esas fronteras.

### Criterios de salida de la Fase 0

Antes del Gate 1, Claude tiene que poder enunciar:
- el objetivo y qué porción del sistema cubre
- los activos y actores clave
- los puntos de entrada y las fronteras de confianza en alcance
- los flujos de datos principales que cruzan esas fronteras
- qué áreas no están claras y van a quedar como preguntas abiertas en lugar de asumirse

No deduzcas un control ni una frontera por un nombre. Si el diseño no deja claro un flujo, es una
pregunta abierta, no un supuesto.

---

## Gate 1 — Alcance y descomposición

Proponé el alcance del modelo y la descomposición, a la escala del cambio:

```markdown
## Modelo de amenazas propuesto

- **Objetivo:** {feature X | módulo | API | diff de la rama actual}
- **Activos:** {qué estamos protegiendo}
- **Actores:** {quiénes, con su nivel de privilegio}
- **Puntos de entrada:** {rutas / consumidores / tareas en alcance}
- **Fronteras de confianza:** {los cruces a modelar}
- **Método:** STRIDE por elemento del flujo de datos
- **Fuera de alcance:** {lo que este modelo no va a cubrir}
- **Preguntas abiertas:** {lo ambiguo}
```

- Preguntá: **"Este es el alcance y la descomposición del modelo de amenazas para {objetivo}.
  Confirmalo antes de que enumere amenazas."**
- **Frená. No enumeres amenazas hasta que el usuario confirme el alcance y la descomposición.**

---

## Configuración del aislamiento (solo en modo autónomo)

Si corrés **embebido en otro flujo**, salteálo: escribí en la rama o worktree existente.

Si corrés **por separado**, preguntale al usuario cómo quiere aislar el trabajo antes de escribir:

> ¿Querés que trabaje en una rama nueva del checkout actual, o que cree un worktree de git aparte?

Usá la respuesta tal cual. Frená después de preguntar; no crees ni rama ni worktree hasta que el
usuario elija.

Si el checkout actual tiene cambios sin commitear, frená y preguntá antes de cambiar de rama o crear
un worktree.

### Opción A — Rama en el checkout actual

```bash
git switch develop && git pull --ff-only && git switch -c assess/threat-{slug}
```

### Opción B — Worktree aparte

Creá worktrees únicamente bajo `.worktrees/`. No le pidas una ruta al usuario.

```bash
git fetch origin develop && mkdir -p .worktrees && git worktree add .worktrees/assess-threat-{slug} -b assess/threat-{slug} origin/develop
```

`{slug}` es el objetivo en kebab-case (por ejemplo `pago-por-link`, `api-exportar-contactos`). Toda la
salida se escribe dentro de la ubicación de trabajo elegida.

---

## Fase 2 — Enumerar amenazas (STRIDE)

**Objetivo:** producir `THREAT-MODEL.md` — un diagrama de flujo de datos más una pasada STRIDE por
cada elemento y frontera, anclada en el diseño real.

### Reglas del modelado (no negociables)

- **STRIDE por elemento.** Para cada flujo, proceso, almacenamiento o frontera, considerá suplantación
  (Spoofing), manipulación (Tampering), repudio (Repudiation), divulgación de información (Information
  disclosure), denegación de servicio (Denial of service) y elevación de privilegios (Elevation of
  privilege). Registrá las que aplican de verdad; no rellenes con filas que no aplican.
- **Trazable.** Cada amenaza referencia el elemento o flujo al que apunta y, cuando existe, el punto de
  código o diseño (`ruta:línea`, ruta HTTP, frontera). Cada mitigación ya existente cita dónde vive;
  cada mitigación propuesta es concreta.
- **Calificá el riesgo.** Cada amenaza recibe probabilidad × impacto (o un riesgo bajo/medio/alto). Eso
  es lo que ordena las mitigaciones.
- **Sin invención.** Si no está claro si una mitigación existe, marcá el estado de la amenaza como
  `Sin verificar` y sumá una pregunta abierta; nunca asumas que la defensa está puesta.
- **El riesgo residual es explícito.** Enunciá qué queda después de las mitigaciones propuestas y qué se
  acepta.

### Estructura de THREAT-MODEL.md

```markdown
# Modelo de amenazas — {objetivo}

## Alcance
- Objetivo: {feature | módulo | API | diff de rama}
- Fecha: {AAAA-MM-DD}
- Método: STRIDE
- Activos / actores / fronteras de confianza: {resumen corto del Gate 1}

## Diagrama de flujo de datos
{DFD en Mermaid: actores, procesos, almacenamientos y las fronteras de confianza como cruces etiquetados}

## Amenazas (STRIDE)
| # | Elemento / flujo | STRIDE | Amenaza | Probabilidad | Impacto | Riesgo | Mitigación existente | Mitigación propuesta | Estado |
|---|------------------|--------|---------|--------------|---------|--------|----------------------|----------------------|--------|
| 1 | POST /login | S | Credential stuffing por login sin límite de intentos | Alta | Alto | Alto | ninguna | Límite de tasa + bloqueo + opción de MFA | Abierta |
| 2 | servicio→base de datos | T | Inyección SQL por consulta sin parametrizar | Media | Alto | Alto | consultas parametrizadas `src/db/q.ts:20` | — | Mitigada |
| 3 | lectura de pedido | E | IDOR — sin chequeo de propiedad | Media | Alto | Alto | ninguna | Exigir autorización al acceder al registro | Abierta |

Estado: Mitigada / Abierta / Aceptada / Sin verificar.

## Mitigaciones priorizadas
Ordenadas por riesgo; cada una atada al número de su amenaza. (Se convierten en tareas del plan o en
ítems de seguimiento.)

## Riesgo residual
Qué queda después de las mitigaciones propuestas, y qué se acepta explícitamente (y quién lo acepta).

## Preguntas abiertas / a verificar
- …
```

**Validá el DFD de Mermaid contra el parser antes de cerrar**: un diagrama que no renderiza es peor que
ninguno. Mantenelo legible; partilo si queda sobrecargado.

---

## Fase 3 — Mitigaciones y riesgo residual

- **Priorizá** las amenazas abiertas por riesgo en la lista de mitigaciones, cada una atada al número de
  su amenaza.
- **Traspasá** las mitigaciones explícitamente — este flujo no las implementa:
  - si estás embebido en `fmway-dev`, cada mitigación abierta de riesgo alto o medio tiene que
    convertirse en una **tarea del PLAN** antes de empezar a codear
  - si no, enrutala a un ítem posterior de `fmway-dev`, `fmway-bugs` o `fmway-vuln`, según corresponda
- **Enunciá el riesgo residual** con claridad, para que el usuario pueda aceptarlo sabiendo qué acepta.

---

## Gate 2 — Revisión

Cuando el modelo está escrito:

- Entregá la ruta, las amenazas de riesgo alto, las mitigaciones priorizadas, el riesgo residual y las
  **Preguntas abiertas / a verificar**.
- Decí: **"Modelo de amenazas listo en `docs/security/threat-models/{slug}/THREAT-MODEL.md`. Dejé
  listadas las amenazas de riesgo alto y las mitigaciones propuestas. Revisalo."**
- **Frená. Esperá la revisión del usuario antes de seguir.**

Si corrés **embebido**, el control vuelve al flujo que llamó, en su propio gate: el modelo se revisa
ahí, sus mitigaciones se integran al plan de ese flujo y viaja con su PR. El paso de PR autónomo se
saltea.

---

## Fase 4 — PR (solo en modo autónomo)

Sugerí invocar `fmway-pr` para pushear `assess/threat-{slug}` y abrir el PR. No pushees ni ejecutes
`gh pr create` vos.

```
Título: assess(threat-model): {objetivo}
```

El cuerpo del PR tiene que incluir:
- **Alcance:** objetivo, activos, actores, fronteras de confianza.
- **Resumen:** amenazas de riesgo alto y su estado.
- **Mitigaciones:** la lista priorizada y a dónde se enruta cada una.
- **Riesgo residual:** qué queda y qué se acepta.
- **Preguntas abiertas:** ítems sin resolver que necesitan definición del equipo.

Una vez abierto, compartí la URL. **Frená. No mergees hasta que el usuario apruebe.**

---

## Referencia rápida — gates

| Gate | Disparador | Qué decir | Bloquea hasta |
|------|-----------|-----------|---------------|
| 1 | Alcance y descomposición propuestos | "Este es el alcance del modelo para {objetivo}. Confirmalo." | El usuario confirma |
| 2 | Modelo escrito | "Modelo listo en `docs/security/threat-models/{slug}/THREAT-MODEL.md`. Revisalo." | Revisión del usuario |
| 3 | (autónomo) Revisado | Sugerir `fmway-pr` para el PR `assess/threat-{slug} → develop`; compartir la URL | El usuario aprueba el PR |

---

## Qué se produce

```
docs/security/threat-models/{slug}/
  THREAT-MODEL.md   # DFD + tabla STRIDE + mitigaciones priorizadas + riesgo residual
```

---

## Qué NO hacer

- No enumeres amenazas antes de que el Gate 1 confirme el alcance y la descomposición.
- No rellenes la tabla STRIDE con filas que no aplican: registrá las amenazas que aplican de verdad.
- No asumas que una mitigación está puesta: si no está claro, marcá `Sin verificar` y sumá una pregunta
  abierta.
- No dejes amenazas ni mitigaciones sin trazabilidad: cada una referencia su elemento o flujo y, cuando
  existe, el punto de código o diseño.
- No implementes mitigaciones acá: modelá, priorizá y dejá que el flujo que llama o un ítem posterior
  cargue el cambio.
- No cierres un DFD de Mermaid que falla al renderizar.
- No dejes que el modelo se infle: escalalo al cambio; la profundidad sigue al riesgo.
- No abras un PR separado cuando corrés embebido en otro flujo: el modelo viaja con el PR de quien llamó.
- No escribas directamente en `develop` o `main` en modo autónomo — usá `assess/threat-{slug}`.
