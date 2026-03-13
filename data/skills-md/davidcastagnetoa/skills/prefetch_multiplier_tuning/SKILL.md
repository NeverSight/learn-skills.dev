---
name: prefetch_multiplier_tuning
description: Ajuste del prefetch multiplier de Celery workers para optimizar throughput vs latencia en tareas KYC
type: Algorithm
priority: Recomendada
mode: Self-hosted
---

# prefetch_multiplier_tuning

Ajuste fino del prefetch multiplier de los workers Celery para equilibrar throughput y latencia segun el tipo de tarea del pipeline de verificacion de identidad. Las tareas GPU-bound (face_match, liveness) requieren configuracion diferente a las CPU-bound (OCR, doc_processing) para evitar cuellos de botella y maximizar la utilizacion de recursos.

## When to use

Usa esta skill cuando trabajes con el **worker_pool_agent** y necesites optimizar el rendimiento de los workers Celery en el pipeline KYC. Aplica cuando observes alta latencia en tareas GPU-bound, subutilizacion de workers CPU-bound, o desbalance de carga entre colas de verificacion.

## Instructions

1. Identificar y clasificar las tareas del pipeline por tipo de recurso consumido:
   ```python
   # backend/modules/worker_pool/task_classification.py
   TASK_RESOURCE_MAP = {
       "face_match": "gpu_bound",        # ArcFace inference
       "liveness_detection": "gpu_bound", # Anti-spoofing model
       "ocr_extraction": "cpu_bound",     # PaddleOCR / EasyOCR
       "doc_processing": "cpu_bound",     # OpenCV processing
       "antifraud_analysis": "cpu_bound", # ELA, metadata analysis
       "decision_engine": "io_bound",     # DB queries, scoring
   }
   ```

2. Configurar prefetch multiplier diferenciado por tipo de worker:
   ```python
   # backend/modules/worker_pool/celery_config.py
   # GPU-bound workers: prefetch=1 para evitar acaparar tareas mientras GPU esta ocupada
   GPU_WORKER_CONFIG = {
       "worker_prefetch_multiplier": 1,
       "task_acks_late": True,
       "worker_concurrency": 1,  # Una tarea GPU a la vez
   }

   # CPU-bound workers: prefetch=4 para mantener pipeline lleno
   CPU_WORKER_CONFIG = {
       "worker_prefetch_multiplier": 4,
       "task_acks_late": True,
       "worker_concurrency": 4,  # Multiples tareas CPU en paralelo
   }

   # IO-bound workers: prefetch=8 para alto throughput
   IO_WORKER_CONFIG = {
       "worker_prefetch_multiplier": 8,
       "task_acks_late": False,
       "worker_concurrency": 8,
   }
   ```

3. Crear scripts de lanzamiento de workers con configuracion especifica por cola:
   ```bash
   # GPU workers - face_match y liveness
   celery -A worker_pool worker \
       --queues=face_match,liveness \
       --concurrency=1 \
       --prefetch-multiplier=1 \
       --hostname=gpu-worker@%h

   # CPU workers - OCR y document processing
   celery -A worker_pool worker \
       --queues=ocr,doc_processing,antifraud \
       --concurrency=4 \
       --prefetch-multiplier=4 \
       --hostname=cpu-worker@%h
   ```

4. Implementar metricas para medir el impacto del prefetch multiplier:
   ```python
   # backend/modules/worker_pool/metrics.py
   from prometheus_client import Histogram, Gauge

   task_wait_time = Histogram(
       "kyc_task_wait_seconds",
       "Tiempo de espera en cola antes de ejecucion",
       ["task_name", "worker_type"],
   )
   prefetch_utilization = Gauge(
       "kyc_prefetch_utilization",
       "Ratio de tareas prefetched vs ejecutadas",
       ["worker_type"],
   )
   ```

5. Implementar ajuste dinamico del prefetch multiplier basado en carga:
   ```python
   # backend/modules/worker_pool/dynamic_prefetch.py
   from celery.signals import worker_ready
   import psutil

   @worker_ready.connect
   def adjust_prefetch(sender, **kwargs):
       cpu_percent = psutil.cpu_percent(interval=1)
       current_multiplier = sender.app.conf.worker_prefetch_multiplier

       if cpu_percent > 85 and current_multiplier > 1:
           sender.app.conf.worker_prefetch_multiplier = max(1, current_multiplier - 1)
       elif cpu_percent < 40 and current_multiplier < 8:
           sender.app.conf.worker_prefetch_multiplier = current_multiplier + 1
   ```

6. Configurar task_acks_late junto con el prefetch para garantizar que tareas KYC no se pierdan:
   ```python
   # Combinacion critica para tareas de verificacion
   app.conf.update(
       task_acks_late=True,           # ACK solo despues de completar
       task_reject_on_worker_lost=True,  # Reencolar si worker muere
       worker_prefetch_multiplier=1,  # Default conservador
   )
   ```

7. Crear tests de carga para validar la configuracion de prefetch:
   ```python
   # backend/tests/test_prefetch_tuning.py
   def test_gpu_worker_no_starvation():
       """Verificar que GPU workers no acaparan tareas."""
       results = []
       for _ in range(10):
           r = face_match_task.delay(test_session_id)
           results.append(r)
       wait_times = [r.result["wait_time"] for r in results]
       assert max(wait_times) < 8.0  # Dentro del SLA de 8 segundos
   ```

## Notes

- Un prefetch_multiplier=1 es obligatorio para tareas GPU-bound del pipeline KYC (face_match, liveness); valores mayores causan que un worker acapare tareas mientras la GPU esta ocupada, aumentando la latencia global.
- Siempre combinar prefetch_multiplier con task_acks_late=True para tareas criticas de verificacion; esto evita perder tareas si un worker muere durante el procesamiento biometrico.
- Revisar periodicamente las metricas de wait_time por cola para detectar desajustes; el objetivo es mantener el tiempo total de verificacion por debajo de 8 segundos segun los SLA del sistema.
