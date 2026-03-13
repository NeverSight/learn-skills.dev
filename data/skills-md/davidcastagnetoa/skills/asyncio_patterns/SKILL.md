---
name: asyncio_patterns
description: Patrones de concurrencia async para ejecutar agentes en paralelo dentro del pipeline KYC
type: Library
priority: Esencial
mode: Self-hosted
---

# asyncio_patterns

asyncio y asyncio.gather permiten ejecutar simultáneamente los agentes independientes del pipeline reduciendo el tiempo total en ~50%.

## When to use

Usar en el orchestrator_agent cada vez que dos o más agentes puedan ejecutarse en paralelo.

## Instructions

1. Identificar fases paralelas: liveness + doc_capture; OCR + face_match.
2. Envolver cada llamada de agente como corrutina async.
3. Usar `await asyncio.gather(task_a, task_b, return_exceptions=True)`.
4. Gestionar `return_exceptions=True`: el fallo de un agente no cancela los demás.
5. Aplicar `asyncio.wait_for(coro, timeout=N)` a cada tarea para respetar SLO de 8 segundos.
6. Propagar `session_id` con `contextvars.ContextVar` a través de todas las corrutinas.

## Notes

- El GIL no afecta a I/O-bound async, pero sí a CPU-bound. Las tareas CPU-bound deben ejecutarse en ProcessPoolExecutor o delegarse a Celery workers.
- asyncio.gather no garantiza orden de resultados; indexar por posición o usar diccionario.