---
name: interactive-bug
description: Diagnosticar y corregir bugs con preguntas adaptativas usando `question` (multiple choice + respuesta libre). Usar cuando el usuario reporta que algo no funciona, hay errores en UI/API/datos o comportamiento inesperado, especialmente con poco contexto inicial.
---

# Interactive Bug Fixer

Objetivo: obtener contexto suficiente para resolver el bug en un solo intento, con minimo ida y vuelta.

## Protocolo operativo

1) Clasificar rapido el bug
- UI/UX
- API/backend
- Datos/estado
- Infra/config

2) Ejecutar ronda 1 de preguntas (OBLIGATORIO con `question`)
- Hacer 2-4 preguntas en un unico llamado a `question`
- Mezclar preguntas cerradas (opciones) y abiertas (texto libre)
- Priorizar preguntas de alto valor diagnostico

3) Confirmar entendimiento en 3 bullets
- Problema observado
- Comportamiento esperado
- Hipotesis inicial

4) Pedir confirmacion corta
- "¿Este resumen representa bien el problema?"
- Si no, hacer una segunda ronda breve (maximo 2 preguntas)

5) Investigar y corregir
- Leer codigo relevante
- Encontrar causa raiz
- Aplicar fix minimo y seguro

## Diseno de preguntas

- Usar opciones cuando hay respuestas previsibles.
- Usar abiertas cuando falta detalle especifico.
- No repetir informacion que el usuario ya dio.
- Recordar: `question` ya incluye opcion de escribir respuesta propia (no agregar "Otro").

## Plantillas por tipo

### UI/UX
- Cerrada: "¿Donde ocurre?" (header, modal, tabla, formulario, otro)
- Abierta: "¿Que deberia pasar y que pasa realmente?"
- Cerrada: "¿Ves errores en consola?" (si/no/no se)

### API/backend
- Cerrada: "¿Como falla?" (timeout, 4xx/5xx, respuesta invalida, intermitente)
- Abierta: "Pega status/mensaje/stack trace"
- Cerrada: "¿Antes funcionaba?" (si/no/no se)

### Datos/estado
- Cerrada: "¿Que falla?" (no guarda, guarda mal, no lee, inconsistente)
- Abierta: "Da un ejemplo concreto de dato afectado"
- Cerrada: "¿Pasa siempre o con ciertos casos?"

## Reglas duras

1. Usar `question` para preguntar, no texto plano.
2. Maximo 4 preguntas por ronda y 2 rondas totales.
3. Incluir al menos 1 pregunta abierta si faltan datos criticos.
4. Si hay contexto suficiente, saltar preguntas y pasar a investigacion.
5. Arreglar con cambio minimo; no refactorizar sin necesidad.

## Salida minima esperada

Antes de editar:
- Causa raiz probable
- Archivos a tocar
- Estrategia de fix (1-3 lineas)

Despues de editar:
- Explicar fix en lenguaje simple
- Indicar por que el cambio resuelve el bug
