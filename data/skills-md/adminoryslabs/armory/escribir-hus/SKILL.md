---
name: escribir-hus
description: Convierte un PRD en Historias de Usuario que un desarrollador - humano o agente - pueda construir sin adivinar - una HU por funcionalidad del alcance, formato Como/Quiero/Para con al menos dos escenarios Gherkin, conflictos del PRD documentados en vez de resueltos en silencio y puntos abiertos como preguntas exactas al negocio. Use when the BA role receives a PRD, or when asked to write, draft or split user stories from a PRD, in any domain.
type: skill
tags: [ba, hu, historias-de-usuario, gherkin, prd]
---

# Escribir HUs

## Goal

Traducir un PRD en Historias de Usuario accionables, sin importar el dominio del proyecto (salud,
fintech, retail o cualquier otro): cada HU tiene que poder construirse sin que nadie adivine lo
que el PRD no dice.

## Input

- **PRD** con 5 secciones (el formato es constante; el dominio varía y nunca se asume):
  1. Problema
  2. Objetivo
  3. Alcance (Incluye / No incluye)
  4. Supuestos y Puntos Abiertos
  5. Criterios de éxito
- **Si el sistema ya existe y fue contextualizado:** `docs/contexto/GLOSARIO.md` y
  `docs/contexto/CAPACIDADES.md`. Las HUs usan los términos del glosario y no duplican
  capacidades que el sistema ya tiene.

Si el PRD no trae alguna sección, adaptarse sin cambiar el proceso (por ejemplo, extraer el
objetivo del Problema) y dejarlo dicho.

## Workflow

1. **Leer las 5 secciones completas antes de escribir nada.** El Alcance marca los límites; los
   Puntos Abiertos marcan lo que todavía no está decidido.
2. **Identificar las funcionalidades claras del Alcance.** Cada una se convierte en una HU: no
   combinar varias en una HU gigante ni fragmentar de más creando HUs artificiales para sub-pasos
   de una misma acción.
3. **Detectar conflictos entre secciones antes de resolverlos.** Si el Alcance, el Objetivo y los
   Criterios de éxito no dicen lo mismo, no se decide en silencio: se documenta el conflicto y se
   construye solo lo mínimo necesario para cumplir el criterio, dejando explícito que falta
   confirmación de negocio.
4. **Redactar cada HU** con `assets/hu-template.md`: Historia (Como/Quiero/Para) + al menos 2
   escenarios Gherkin (camino feliz + 1 caso borde).
5. **Reglas de negocio transversales** (por ejemplo, un Criterio de éxito que aplica a varias
   funcionalidades) se validan como escenario borde dentro de cada HU afectada, no como una HU
   aparte.
6. **Ningún dato no confirmado por el PRD se asume por conveniencia.** Se declara como Punto
   Abierto con la pregunta exacta que se le haría al negocio.
7. **Nada de lo marcado "No incluye" se agrega**, aunque parezca una mejora obvia.
8. **Los Puntos Abiertos se reparten solo en las HUs donde aplican literalmente**, no se copian
   todos en todas las HUs por defecto.
9. **Un archivo Markdown por HU**, guardado en la carpeta del proyecto.

## Quality gate

- [ ] Leí las 5 secciones del PRD (no solo el Alcance)
- [ ] Cada HU corresponde a una funcionalidad clara del Alcance: ni combinada ni fragmentada de más
- [ ] Cada HU tiene mínimo 2 escenarios Gherkin (camino feliz + caso borde)
- [ ] Ningún dato asumido aparece redactado como si ya estuviera decidido
- [ ] Nada de la lista "No incluye" se coló como funcionalidad
- [ ] Cada Punto Abierto trae la pregunta exacta al negocio, no una suposición disfrazada
- [ ] Los conflictos entre secciones del PRD quedaron documentados, no resueltos en silencio
- [ ] Si el sistema estaba contextualizado: usé los términos del glosario y no dupliqué capacidades
- [ ] Un archivo Markdown por HU, guardado en la carpeta del proyecto

## References

- `assets/hu-template.md` — plantilla de HU.
- `references/ejemplos-aplicados.md` — casos resueltos en proyectos anteriores (conflictos de
  alcance, puntos abiertos, elementos fuera de alcance propuestos por otro agente).
