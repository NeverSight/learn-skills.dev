---
name: generar-prd-conversacional
description: "Trigger: PRD, product requirements, definir producto, idear proyecto, armar spec de producto. Genera un PRD sección por sección conversando con el usuario — profundiza con preguntas, presenta alternativas cuando hay decisión real, y solo escribe `PRD.md` cuando cada sección está validada."
license: Apache-2.0
metadata:
  author: "adminoryslabs"
  version: "1.0"
---

# PRD Generator (Conversational)

## Goal

Producir un `PRD.md` listo para alimentar diseño técnico o implementación, recorriendo **una
sección a la vez** junto al usuario. A diferencia de la skill `generar-prd` (light, una sola
pasada), esta skill:

- **Entrevista** antes de escribir cada sección — no asume, no rellena con placeholders.
- **Presenta alternativas con trade-offs** en las secciones donde hay una decisión real
  (cómo enmarcar el problema, cómo definir éxito, qué entra en alcance, etc.).
- **Marca supuestos** del agente con `<!-- REVISAR: ... -->` para que el humano los valide
  durante la revisión.
- Escribe `PRD.md` al final, después de que las 8 secciones estén validadas — no antes.

El output es un PRD que el usuario puede defender, no un draft opaco que tenga que reescribir.

## Activation Contract

Usar esta skill cuando el usuario pida **explícitamente** un PRD guiado, paso a paso, o cuando
arranque con frases como "armemos un PRD", "quiero definir bien este producto antes de
codear", "necesito un spec de producto conversado". Si el usuario solo quiere un draft rápido
para arrancar, usar la skill light `generar-prd`.

## Hard Rules

- Recorrer las 8 secciones en el orden del template. No saltear secciones, no reordenarlas.
- Antes de escribir cada sección, **esperar** la respuesta del usuario. Una sección escrita sin
  input del usuario es un failure mode de esta skill — equivale a volver al modo light.
- No inventar el problema, el usuario o el outcome. Si el usuario no los tiene claros, ayudar a
  descubrirlos con preguntas — nunca asumirlos.
- Marcar toda suposición del agente con `<!-- REVISAR: ... -->` inline. El PRD debe ser
  revisable, no presentable como terminado.
- Las alternativas deben ser **realmente viables** para el proyecto en cuestión — no opciones
  de手册 que descarten la decisión sin presentarla.
- Si el usuario cierra la conversación a mitad de flujo, guardar progreso parcial en
  `PRD.md` con las secciones validadas y el resto marcado como `<!-- PENDIENTE -->`.

## Decision Gates

| Situación | Acción |
|---|---|
| Usuario pide un draft rápido | Usar `generar-prd` (light), no esta skill |
| Usuario tiene idea pero no problema claro | Saltar a la sección Problema y ayudar a descubrirlo con preguntas, no avanzar a la siguiente |
| Usuario tiene todo claro y quiere ir rápido | Aceptar respuestas cortas — no obligar a expandir si la respuesta es suficiente |
| Sección con decisión real (problema, éxito, alcance) | Presentar 2-3 alternativas con trade-offs antes de aceptar la respuesta |
| Sección con captura (supuestos, casos borde) | 1-2 preguntas de profundización, sin alternativas |
| Usuario ya tiene un PRD y quiere revisarlo | No usar esta skill — pedirle que abra `PRD.md` existente y revisarlo juntos sección por sección |

## Workflow

Antes de empezar, confirmar que el usuario quiere el flujo conversacional. Si confirma, recorrer
las 8 secciones en orden, **una por turno**. Para cada sección:

1. **Abrir**: enunciar por qué importa esa sección en 1 línea, sin tutorial.
2. **Profundizar**: 1-3 preguntas concretas. Si la sección tiene decisión real, presentar
   2-3 alternativas con trade-offs antes de la pregunta. Ver guía en
   `references/secciones-guia.md`.
3. **Validar**: confirmar que entendiste (1 línea parafraseando) y preguntar si quiere
   ajustar antes de cerrar.
4. **Cerrar**: registrar la respuesta y avanzar a la siguiente sección. No acumular — el PRD
   se va construyendo en la cabeza del usuario a medida que avanza.

Las 8 secciones, en orden, con el tipo de interacción esperado:

| # | Sección | Tipo | Alternativas? |
|---|---|---|---|
| 1 | Problema | Decisión real (encuadre) | Sí |
| 2 | Usuario objetivo | Decisión real (segmento) | Sí |
| 3 | Objetivo / resultado esperado | Decisión real (outcome vs output) | Sí |
| 4 | Alcance | Decisión real (frontera) | Sí |
| 5 | No alcance | Captura con anti-patrones | No |
| 6 | Criterios de éxito | Decisión real (qué medir) | Sí |
| 7 | Casos borde | Captura | No |
| 8 | Supuestos y riesgos | Captura | No |

Cuando las 8 secciones estén validadas:

1. Ensamblar `PRD.md` usando `assets/prd-template.md` — copiar el template tal cual, sin
   modificar estructura ni títulos.
2. Llenar cada sección con la respuesta validada. Si quedó algún supuesto implícito del
   agente, marcarlo con `<!-- REVISAR: ... -->`.
3. Escribir a disco en `PRD.md` (root del proyecto), salvo que el usuario indique otra ruta.
4. Cerrar con un recordatorio: el PRD es un borrador estructurado — la revisión real
   (ambigüedades, números, bordes) sigue siendo del humano.

## Quality Gate

Antes de cerrar, verificar silenciosamente:

- Las 8 secciones están presentes. Ninguna vacía — al menos un bullet/idea aunque sea mínima.
- "No alcance" tiene al menos una exclusión **explícita** (no "todo lo no mencionado arriba").
- Los criterios de éxito son verificables, no adjetivos sin ancla medible.
- Toda suposición del agente está marcada con `<!-- REVISAR: ... -->`.
- Si se cerró antes de completar todas las secciones, las restantes están marcadas
  `<!-- PENDIENTE -->` en el archivo.

## References

- `assets/prd-template.md` — template literal, no modificar. Idéntico al de `generar-prd`.
- `references/secciones-guia.md` — guía de profundización por sección: preguntas concretas,
  alternativas con trade-offs, anti-patrones y ejemplos de respuestas buenas vs malas.
