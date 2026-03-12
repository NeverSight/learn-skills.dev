---
name: dead_letter_queue
description: Cola de mensajes fallidos para capturar y reprocesar tareas KYC que exceden reintentos maximos
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# dead_letter_queue

Cola de mensajes fallidos (DLQ) para capturar tareas del pipeline KYC que exceden el numero maximo de reintentos, como inferencia facial fallida, OCR timeout o errores de liveness detection. Permite analisis post-mortem de fallos recurrentes y re-procesamiento manual o automatizado de tareas recuperables.

## When to use

Usa esta skill cuando trabajes con el **worker_pool_agent** y necesites implementar o configurar el manejo de tareas fallidas en el pipeline de verificacion de identidad. Aplica cuando tareas criticas (face_match, OCR, liveness) fallan repetidamente y necesitas capturarlas en lugar de perderlas.

## Instructions

1. Definir la configuracion de reintentos maximos por tipo de tarea en la configuracion de Celery:
   ```python
   # backend/modules/worker_pool/celery_config.py
   TASK_MAX_RETRIES = {
       "face_match": 3,
       "ocr_extraction": 5,
       "liveness_detection": 3,
       "doc_processing": 4,
   }
   ```

2. Crear el modelo de base de datos para almacenar tareas en la DLQ:
   ```python
   # backend/modules/worker_pool/models/dead_letter.py
   class DeadLetterEntry(Base):
       __tablename__ = "dead_letter_queue"
       id = Column(UUID, primary_key=True, default=uuid4)
       task_name = Column(String, nullable=False)
       task_id = Column(String, unique=True, nullable=False)
       args = Column(JSON)
       kwargs = Column(JSON)
       exception = Column(Text)
       traceback = Column(Text)
       retry_count = Column(Integer)
       created_at = Column(DateTime, default=datetime.utcnow)
       status = Column(String, default="pending")  # pending, reprocessed, discarded
   ```

3. Implementar el handler de task_failure que envia tareas agotadas a la DLQ:
   ```python
   from celery.signals import task_failure

   @task_failure.connect
   def handle_task_failure(sender, task_id, exception, args, kwargs, traceback, einfo, **kw):
       if sender.request.retries >= TASK_MAX_RETRIES.get(sender.name, 3):
           DeadLetterEntry.create(
               task_name=sender.name,
               task_id=task_id,
               args=args,
               kwargs=kwargs,
               exception=str(exception),
               traceback=str(einfo),
               retry_count=sender.request.retries,
           )
   ```

4. Crear endpoint API para consultar y gestionar la DLQ:
   ```python
   # backend/api/routes/dead_letter.py
   @router.get("/dlq/entries")
   async def list_dlq_entries(status: str = "pending", limit: int = 50):
       return await DeadLetterEntry.filter(status=status).limit(limit).all()

   @router.post("/dlq/entries/{entry_id}/reprocess")
   async def reprocess_entry(entry_id: UUID):
       entry = await DeadLetterEntry.get(id=entry_id)
       celery_app.send_task(entry.task_name, args=entry.args, kwargs=entry.kwargs)
       entry.status = "reprocessed"
       await entry.save()
   ```

5. Implementar un job periodico que analice patrones de fallo en la DLQ:
   ```python
   @celery_app.task(name="dlq_analysis")
   def analyze_dlq_patterns():
       recent = DeadLetterEntry.filter(
           created_at__gte=datetime.utcnow() - timedelta(hours=1)
       ).all()
       failure_counts = Counter(e.task_name for e in recent)
       for task_name, count in failure_counts.items():
           if count > ALERT_THRESHOLD:
               send_alert(f"DLQ: {task_name} tiene {count} fallos en la ultima hora")
   ```

6. Configurar alertas y metricas de la DLQ para monitoreo:
   ```python
   DLQ_METRICS = {
       "dlq_entries_total": Counter("dlq_entries_total", "Total DLQ entries", ["task_name"]),
       "dlq_reprocessed_total": Counter("dlq_reprocessed_total", "Reprocessed entries", ["task_name"]),
   }
   ```

7. Implementar politica de retencion para limpiar entradas antiguas de la DLQ:
   ```python
   @celery_app.task(name="dlq_cleanup")
   def cleanup_old_entries(retention_days: int = 30):
       cutoff = datetime.utcnow() - timedelta(days=retention_days)
       DeadLetterEntry.filter(created_at__lt=cutoff, status="discarded").delete()
   ```

## Notes

- Las entradas de la DLQ deben anonimizar datos biometricos y personales segun GDPR/LOPD; almacenar solo referencias de sesion, nunca imagenes ni embeddings faciales.
- El re-procesamiento manual desde la DLQ debe pasar por las mismas validaciones antifraude que el flujo original para evitar bypass de seguridad.
- Monitorear el crecimiento de la DLQ como indicador de salud del sistema: un incremento sostenido indica problemas sistemicos en el pipeline que requieren atencion inmediata.
