---
name: celery
description: Framework de cola de tareas distribuido con soporte de prioridades
type: Framework
priority: Esencial
mode: Self-hosted
---

# celery

Celery es el framework de cola de tareas distribuido que gestiona la ejecución de todos los trabajos computacionalmente intensivos del pipeline KYC (inferencia ML, procesamiento de imagen, OCR).

## When to use

Usar en el `worker_pool_agent` como motor de ejecución de tareas. El orquestador encola tareas en Celery y los workers las procesan de forma asíncrona.

## Instructions

1. Instalar: `pip install celery[redis]`.
2. Configurar app:
   ```python
   app = Celery('verifid', broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')
   app.conf.task_serializer = 'json'
   app.conf.result_serializer = 'json'
   ```
3. Definir tareas con `@app.task(bind=True, max_retries=3)`.
4. Configurar colas por prioridad: `task_routes = {'liveness.*': {'queue': 'realtime'}}`.
5. Arrancar workers: `celery -A verifid worker -Q realtime,gpu,cpu --concurrency=4`.
6. Configurar `task_acks_late=True` para no perder tareas si el worker muere.
7. Habilitar `task_reject_on_worker_lost=True`.

## Notes

- Usar JSON como serializador (nunca pickle por seguridad).
- Cada worker debe tener los modelos ML precargados; ver skill `model_warmup`.
- Monitorizar con Celery Flower para visibilidad en tiempo real.