---
name: celery_redis
description: Cola de tareas distribuida para despachar trabajo computacionalmente intensivo a workers
type: Framework
priority: Esencial
mode: Self-hosted
---

# celery_redis

Celery con Redis gestiona la ejecución asíncrona de tareas pesadas del pipeline (inferencia ML, OCR, face match) fuera del event loop principal de FastAPI.

## When to use

Usar para todas las tareas que requieren GPU o CPU significativo: liveness inference, OCR, face_match, deepfake detection.

## Instructions

1. Instalar: `pip install celery[redis] redis`
2. Configurar: `CELERY_BROKER_URL = "redis://localhost:6379/0"`
3. Result backend: `CELERY_RESULT_BACKEND = "redis://localhost:6379/1"`
4. Definir colas por prioridad: `realtime`, `gpu`, `cpu`, `async`.
5. Asignar cada tarea ML: `@app.task(queue='gpu')`.
6. Arrancar workers: `celery worker -Q gpu --concurrency=2 -P solo`.
7. Usar `chord` para pipelines donde la decisión espera todos los resultados.
8. Configurar `task_soft_time_limit` y `task_time_limit`.
9. Activar `task_acks_late=True` para reintento automático.

## Notes

- RabbitMQ es alternativa con mejor soporte de dead-letter queues.
- Celery Flower para monitorización: `pip install flower`.
- Redis Sentinel para HA del broker.