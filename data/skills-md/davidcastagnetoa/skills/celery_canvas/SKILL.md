---
name: celery_canvas
description: Composición de workflows complejos con dependencias paralelas y secuenciales usando Celery Canvas
type: Framework
priority: Esencial
mode: Self-hosted
---

# celery_canvas

Celery Canvas (chord, group, chain) permite componer pipelines de tareas con ejecución paralela y secuencial, respetando las dependencias entre agentes del pipeline KYC.

## When to use

Usar para modelar el pipeline KYC completo en Celery: fases paralelas (liveness + doc processing) y fases secuenciales (face match → antifraud → decision).

## Instructions

1. `group`: ejecutar tareas en paralelo sin dependencias entre ellas.
   ```python
   job = group(liveness_task.s(frames), doc_processing_task.s(doc_image))
   ```
2. `chord`: ejecutar grupo en paralelo y callback cuando todas terminan.
   ```python
   chord(group(liveness_task.s(), ocr_task.s()))(face_match_task.s())
   ```
3. `chain`: ejecutar tareas en secuencia, pasando resultado de una a la siguiente.
   ```python
   pipeline = chain(preprocess.s() | face_match.s() | antifraud.s() | decision.s())
   ```
4. Combinar: usar `chord` para la fase paralela y `chain` para la secuencia posterior.
5. Manejar fallos parciales con `link_error` callbacks.

## Notes

- Los `chord` usan Redis para sincronizar resultados; asegurar que Redis tiene suficiente memoria.
- En producción, limitar la profundidad de anidamiento de Canvas para evitar overhead.