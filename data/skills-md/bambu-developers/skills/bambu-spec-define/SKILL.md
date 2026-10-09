---
name: bambu-spec-define
description: Crea, revisa y gestiona el ciclo de vida de specs (`SPEC NN`) para un feature antes de que se escriba una sola línea de código — la fase deliberadamente lenta de un flujo de spec-driven design. Hace preguntas socráticas para llenar cada sección de `templates/SPEC.template.md` (contexto, goals, non-goals, dependencias, requisitos funcionales, interfaces y contratos, requisitos no funcionales, edge cases, criterios de aceptación, riesgos, preguntas abiertas), asigna el número `NN` secuencial, valida las referencias `Depends on:`, y controla las transiciones de estado Draft → In review → Approved → Implemented → Obsolete (o sus equivalentes en español — Borrador → En revisión → Aprobado → Implementado → Obsoleto). Usa este skill cuando el usuario pida "escribamos el spec de...", "necesito un spec para...", "let's spec out...", "write a spec for...", "manda este spec a revisión", "apruebo el SPEC 04", "approve SPEC 04", "¿qué dice el SPEC 02?", "este spec quedó obsoleto", o mencione `specs/SPEC-NN` explícitamente. Nunca escribe código de aplicación ni empieza una implementación — eso es trabajo de **bambu-spec-implement**, que solo arranca una vez que el spec correspondiente llegue a Approved.
---

# Spec-driven design — definición del spec

> "A spec is not decorative documentation. It is the contract that drives later execution. If the spec is vague, the code will improvise. That is why this flow is deliberately slow during the definition phase and fast during the writing phase."

Este skill cubre la mitad **lenta** de ese flujo: producir, revisar y aprobar el contrato escrito antes de que nadie escriba código. La mitad rápida — ejecutar ese contrato — es **bambu-spec-implement**, que se niega a arrancar si el spec no está Approved.

## Cuándo usar este skill

- "Escribamos el spec de...", "necesito un spec para...", "let's spec out...", "write a spec for X".
- "Manda este spec a revisión", "send this spec to review".
- "Apruebo el SPEC 04", "approve SPEC 04".
- "¿Qué dice el SPEC 02?", "muéstrame el SPEC 03".
- "Este spec ya quedó obsoleto, lo reemplazó el SPEC 09".
- El usuario menciona `specs/SPEC-NN` o un número de spec explícito.

No lo uses para escribir o modificar código de aplicación — ese es el límite duro de este skill. Tampoco lo uses para documentación de referencia general (eso es `bambu-readme-generator` u otros docs); un spec es un contrato de una sola iniciativa, no documentación descriptiva del repo.

## Flujo de trabajo

### Paso 0 — Ubicar el directorio de specs

```bash
test -d docs/specs && echo docs/specs || echo specs
```

Si `docs/specs/` ya existe en el repo, úsalo. Si no, `specs/` en la raíz es el default — detecta, no asumas. Si ninguno existe todavía (primer spec del repo), crea `specs/` en la raíz.

### Paso 1 — Spec nuevo o continuación

Si el usuario referencia un `SPEC NN` existente (por número, título o archivo), ábrelo y continúa desde ahí — el resto de los pasos aplica igual a "llenar lo que falta" que a "escribir desde cero". Si no hay referencia, es un spec nuevo: sigue al Paso 2.

### Paso 2 — Asignar número y nombre de archivo

Escanea `<specs-dir>/*.md` buscando el `NN` más alto en **todos** los estados, incluyendo Obsolete, y asigna `max + 1`. Los números no se reciclan ni siquiera si el spec llega a Obsolete.

Nombre de archivo: `<specs-dir>/SPEC-NN-slug-del-titulo.md` (kebab-case, derivado del título).

Si detectas que ya existe un archivo con el mismo `NN` (colisión por ramas paralelas que se mergearon por separado), ofrece una operación de renumeración atómica: renombra el archivo más reciente al siguiente número libre, corrige su propio header `# SPEC NN`, y actualiza cualquier línea `Depends on:` de otros specs que apuntara al número viejo.

### Paso 3 — El Objective primero

Antes de tocar cualquier otra sección, escribe el **Objective**: una sola oración, legible en 5 segundos, que describa qué se va a construir. Si no cabe en una oración sin "y" ni ", además", el feature es demasiado grande — detente y propón dividirlo en dos o más specs que se referencien entre sí vía `Depends on:`.

### Paso 4 — Llenar el cuerpo, sección por sección

Usa `templates/SPEC.template.md` como esqueleto y `templates/section-recipes.md` como guía — cada placeholder tiene ahí una receta socrática (preguntas a hacer, no heurísticas de detección de código: el spec normalmente precede al código, así que no hay nada que autodescubrir). Ve sección por sección, en orden, y no avances a la siguiente hasta que la actual sea concreta — presiona contra respuestas vagas de una palabra.

| Sección | Clase | Si no aplica |
|---|---|---|
| Context | MANDATORY | — (siempre tiene contenido real) |
| Goals | MANDATORY | — |
| Non-goals | MANDATORY | — (una lista vacía es señal de alerta, no de limpieza) |
| Dependencies | OPTIONAL | Omite la sección entera si `Depends on:` del header está vacío y no hay dependencia externa |
| Functional requirements | MANDATORY | — |
| Interfaces & contracts | MANDATORY | `N/A — <razón>` si de verdad no expone nada |
| Non-functional requirements | OPTIONAL | Omite si no hay ninguna cifra o restricción más allá de lo que el repo ya garantiza |
| Edge cases | MANDATORY | — |
| Acceptance criteria | MANDATORY | — |
| Risks | OPTIONAL | Omite solo si el cambio es trivial y totalmente reversible; dilo explícitamente al omitir |
| Open questions | OPTIONAL | Omite una vez resueltas; mientras no esté vacía, bloquea el paso a Approved |

Una sección MANDATORY sin contenido aplicable se escribe como `N/A — <razón en una línea>`, nunca se deja el encabezado vacío. Una sección OPTIONAL que no aplica se omite por completo (encabezado y placeholder).

### Paso 5 — Validar antes de escribir

- Ninguna sección MANDATORY quedó con `{{...}}` sin sustituir.
- Cada entrada de `Depends on:` resuelve a un archivo de spec que existe.
- Si alguna dependencia está Obsolete, adviértelo explícitamente.
- No hay colisión de número `NN` sin resolver (ver Paso 2).

### Paso 6 — Guardar

Escribe `<specs-dir>/SPEC-NN-slug.md` con `Status: Draft` (o su valor actual si es continuación de un spec existente).

### Paso 7 — Transiciones de estado

Los estados válidos son **Draft, In review, Approved, Implemented, Obsolete** (o sus equivalentes en español: Borrador, En revisión, Aprobado, Implementado, Obsoleto — acéptalos como entrada del usuario, pero **normaliza siempre al token canónico en inglés al escribir el archivo**, para que `bambu-spec-implement` pueda parsear el Status sin importar en qué idioma ocurrió la conversación).

| Transición | Dispara con | Antes de aplicarla, verifica |
|---|---|---|
| (nuevo) → Draft | Se empieza un spec nuevo | Nada — un Draft puede estar incompleto, es el estado de trabajo. |
| Draft → In review | Instrucción explícita del usuario ("manda a revisión") | Toda sección MANDATORY está presente y sin placeholders sin sustituir. Open Questions puede seguir teniendo items — la revisión es donde se resuelven. |
| In review → Approved | Instrucción explícita del usuario **nombrando el spec** ("apruebo el SPEC 04") — nunca te auto-apruebes | (a) MANDATORY sigue completo; (b) `## Open questions` está ausente o vacía; (c) `## Acceptance criteria` es un checklist no vacío; (d) cada spec en `Depends on:` está, a su vez, Approved o Implemented (nunca Draft/In review/Obsolete). Si algo falla, niégate a cambiar el Status y reporta cuál condición no se cumple. |
| Approved → Implemented | Lo dispara **bambu-spec-implement** al terminar, no este skill por iniciativa propia | Agrega una referencia de una línea (PR o commit) junto al cambio de Status. Es la única escritura permitida sobre un spec ya Approved. |
| cualquiera (menos Implemented) → Obsolete | Instrucción explícita del usuario — feature cancelado, reemplazado, o enfoque abandonado | Anota la razón en la misma línea de Status (`> **Status:** Obsolete — superseded by SPEC 09`). **Nunca borres el archivo** — otros specs pueden referenciarlo en su `Depends on:`. |
| Approved → vuelve a In review | Se edita el contenido sustantivo de un spec ya Approved | Regresa el Status automáticamente a `In review` en cuanto cambia una sección MANDATORY/OPTIONAL — una aprobación no sobrevive a un cambio de contrato. |
| Implemented → (nunca se edita en el lugar) | Se descubre un hueco después de implementado | No toques las secciones sustantivas de un spec Implemented. Si hace falta algo, es un spec **nuevo** que depende de o reemplaza al anterior — la historia de lo que realmente se construyó se mantiene intacta. |

### Paso 8 — Reporte

Confirma al usuario: ruta del archivo, Status resultante, qué secciones OPTIONAL se omitieron y por qué, y si quedan Open Questions pendientes que bloquean el paso a Approved.

## Reglas duras

- **Nunca** escribas un Objective de dos oraciones — divide el feature en specs separados conectados por `Depends on:`.
- **Nunca** rellenes una sección OPTIONAL con relleno genérico en vez de omitirla cuando su regla de omisión aplica.
- **Nunca** resuelvas en silencio algo que debería ir a Open Questions — eso es exactamente la decisión silenciosa que esta sección existe para evitar.
- **Nunca** muevas un spec a Approved mientras Open Questions no esté vacía, o mientras alguna dependencia en `Depends on:` no esté a su vez Approved/Implemented.
- **Nunca** te auto-apruebes — Approved requiere instrucción explícita del usuario nombrando el spec.
- **Nunca** edites las secciones sustantivas de un spec Implemented — escribe un spec nuevo en su lugar.
- **Nunca** borres un archivo de spec — márcalo Obsolete con la razón en la propia línea de Status.
- **Nunca** escribas código de aplicación — ese es el trabajo de **bambu-spec-implement**, una vez que el spec esté Approved.

## Files

- `templates/SPEC.template.md` — esqueleto del spec con `{{placeholders}}`, header fijo + 11 secciones de cuerpo.
- `templates/section-recipes.md` — receta socrática por placeholder (qué preguntar, cuándo omitir la sección).
