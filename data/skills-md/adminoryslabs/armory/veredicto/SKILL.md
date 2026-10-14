---
name: veredicto
description: Dicta el veredicto de una unidad de trabajo cuando el TESTER y el DEV ya entregaron - corre las pruebas del TESTER contra el código del DEV, verifica punto por punto la Definition of Done con evidencia, comprueba que cada rol tocó solo sus rutas y decide a quién se devuelve cada rojo. Use when the LEAD has received both deliveries (ENTREGA TESTER and ENTREGA DEV) for a unit of work, or when asked to verify, judge, or give the verdict on a team delivery.
type: skill
tags: [lead, veredicto, verificacion, evidencia]
---

# Veredicto (v1)

## Goal

Responder con evidencia **"¿esta unidad de trabajo cumple su spec?"**. El veredicto no es una
opinión: cada punto lleva un comando, una prueba o un `archivo:línea` que lo respalda, o queda
`NO VERIFICADO`.

## Input

- El documento de trabajo (`SPRINT0.md`) — la spec contra la que se juzga.
- Los informes de `ENTREGA TESTER` y `ENTREGA DEV`.
- El mapa de propiedad de rutas en `AGENTS.md`.
- La rama de trabajo y su punto de partida (`git merge-base` contra la rama principal).

Si falta cualquiera de las dos entregas, **no se dicta veredicto**: se espera.

## Workflow

1. **Verificar la propiedad de rutas.** Listar qué archivos tocó cada commit del ciclo:
   `git log <base>..HEAD --name-only --format="%s"`. Agrupar por prefijo (`[TESTER]` / `[DEV]`)
   y comparar contra el mapa de `AGENTS.md`. Cada archivo fuera de las rutas del rol es un
   **hallazgo**, aunque las pruebas pasen. Un commit sin prefijo también es un hallazgo.

2. **Correr las pruebas del TESTER** contra el código del DEV, con el comando que indica el
   informe del TESTER. Guardar la salida.

3. **Verificar cada punto de la DoD**, en orden:
   - **🟢** — hay evidencia de que se cumple (prueba en verde, comando con salida esperada, o
     `archivo:línea`).
   - **🔴** — hay evidencia de que no se cumple.
   - **NO VERIFICADO** — no hay forma de comprobarlo con lo disponible. Nunca se pone en verde
     "por inspección" ni por lo que dice un informe.

4. **Para cada 🔴, decidir a quién se devuelve** según la evidencia:
   - la prueba es coherente con la spec y el código no la cumple → **DEV**;
   - la prueba exige algo que la spec no dice, o lo contrario a la spec → **TESTER**;
   - la spec admite más de una lectura → **humano** (no corrige ningún agente).
   Devolver con el punto exacto, la evidencia y la cita de la spec.

5. **Contar vueltas.** Si el mismo desacuerdo ya volvió dos veces, no se devuelve una tercera: se
   escala al humano.

6. **Escribir el veredicto** en `informes/VEREDICTO-<unidad>.md`:
   - tabla de la DoD con resultado y evidencia;
   - hallazgos de propiedad de rutas;
   - devoluciones hechas (a quién, por qué, vuelta N);
   - lista de `NO VERIFICADO` para decisión humana.

7. **Si todo está en verde** (o los `NO VERIFICADO` fueron aceptados por el humano), el LEAD abre
   el PR con el veredicto en la descripción.

## Constraints

- No se modifica código ni pruebas para "hacer pasar" el veredicto.
- No se confía en lo que dicen los informes: se verifica.
- No se publica nada (ni push a main, ni merge).
