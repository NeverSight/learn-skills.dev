---
name: interactive-task
description: Aclarar y ejecutar tareas de desarrollo no-bug (agregar, cambiar, refactorizar, configurar, optimizar) con preguntas adaptativas via `question` (opciones + respuesta libre). Usar cuando el pedido llega incompleto o ambiguo y se necesita definir alcance rapido.
---

# Interactive Task Assistant

Objetivo: convertir pedidos vagos en una especificacion ejecutable con pocas preguntas y alta precision.

## Protocolo operativo

1) Clasificar la tarea
- NUEVO: agregar/crear/implementar
- CAMBIO: modificar/ajustar/reemplazar
- REFACTOR: limpiar/reorganizar/simplificar
- CONFIG: variables, entornos, settings
- MEJORA: optimizar UX/performance/confiabilidad

2) Ejecutar ronda 1 de preguntas (OBLIGATORIO con `question`)
- Hacer 2-4 preguntas en un unico llamado a `question`
- Mezclar cerradas (decision rapida) y abiertas (detalle puntual)
- Cubrir minimo: alcance, resultado esperado y restricciones

3) Confirmar especificacion corta
- "Lo que voy a hacer"
- "Lo que no voy a tocar"
- "Criterio de listo"

4) Pedir confirmacion
- "¿Te sirve este alcance?"
- Si no, hacer segunda ronda breve (maximo 2 preguntas)

5) Investigar y ejecutar
- Buscar patrones existentes en el repo
- Implementar con minima complejidad necesaria

## Diseno de preguntas

- Usar opciones cuando hay alternativas comunes.
- Usar abiertas cuando se necesite texto exacto, orden o reglas de negocio.
- No preguntar datos que ya esten en el pedido.
- Recordar: `question` ya permite respuesta libre (no agregar opcion "Otro").

## Preguntas base por tipo

### NUEVO
- Cerrada: "¿Donde debe aparecer?" (header/sidebar/pagina X/modal/otro)
- Abierta: "¿Como debe comportarse exactamente?"
- Cerrada: "¿Reusar patron existente o crear variante nueva?"

### CAMBIO
- Abierta: "¿Que comportamiento actual queres cambiar?"
- Abierta: "¿Como debe quedar?"
- Cerrada: "¿Afecta solo este modulo o varios?"

### REFACTOR
- Cerrada: "¿Objetivo principal?" (legibilidad, performance, mantenibilidad)
- Cerrada: "¿Restricciones?" (sin cambios funcionales, sin tocar API, etc)
- Abierta: "¿Hay una zona puntual del codigo que te preocupe?"

### CONFIG
- Cerrada: "¿Entorno?" (dev, staging, prod, todos)
- Abierta: "¿Que variables/ajustes exactos necesitas?"
- Cerrada: "¿Solo documentar o tambien aplicar cambios?"

### MEJORA
- Cerrada: "¿Que mejorar?" (UX, velocidad, estabilidad, DX)
- Abierta: "¿Como medimos que mejoro?"
- Cerrada: "¿Prioridad?" (rapido, balanceado, profundo)

## Reglas duras

1. Usar `question` para preguntar, no texto plano.
2. Maximo 4 preguntas por ronda y 2 rondas totales.
3. Incluir al menos 1 pregunta abierta si falta detalle clave.
4. Definir explicitamente alcance IN y OUT antes de ejecutar.
5. Elegir la solucion mas simple que cumpla el objetivo (sin sobre-ingenieria).

## Salida minima esperada

Antes de editar:
- Tipo de tarea detectado
- Alcance IN / OUT
- Archivos probables a tocar
- Criterio de listo

Despues de editar:
- Cambios realizados
- Como validar rapido que quedo bien
