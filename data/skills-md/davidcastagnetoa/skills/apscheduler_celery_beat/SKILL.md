---
name: apscheduler_celery_beat
description: Eliminación automática programada de datos biométricos tras TTL y tareas de mantenimiento periódicas
type: Library
priority: Esencial
mode: Self-hosted
---

# apscheduler_celery_beat

Celery Beat actúa como scheduler distribuido para ejecutar tareas periódicas críticas: purga de datos biométricos expirados, rotación de logs, generación de reportes de métricas FAR/FRR y limpieza de sesiones huérfanas.

## When to use

Usar para toda tarea que deba ejecutarse en intervalo fijo o en horario programado. En particular, la purga de biometría es obligatoria por GDPR y debe ejecutarse aunque el sistema esté bajo carga.

## Instructions

1. Instalar: `pip install celery[redis] django-celery-beat` o `APScheduler` si no se usa Django.
2. Definir schedule en `backend/tasks/scheduler.py`:
   ```python
   from celery.schedules import crontab
   CELERYBEAT_SCHEDULE = {
       "purge-expired-sessions": {
           "task": "tasks.audit.purge_expired_biometric_data",
           "schedule": crontab(minute="*/15"),  # cada 15 minutos
       },
       "cleanup-orphan-minio-objects": {
           "task": "tasks.audit.cleanup_orphan_objects",
           "schedule": crontab(hour="*/1"),
       },
       "generate-far-frr-report": {
           "task": "tasks.metrics.generate_daily_report",
           "schedule": crontab(hour=0, minute=0),
       },
   }
   ```
3. Tarea de purga: consultar sesiones con `created_at < NOW() - INTERVAL '24 hours'` y `status = 'completed'`, eliminar objetos MinIO, nullificar referencias en PostgreSQL.
4. Arrancar beat: `celery -A backend.celery_app beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler`.
5. Asegurar que solo hay una instancia de beat corriendo — usar Redis lock con `celery.utils.abstract.CallableTask`.
6. Monitorizar con Celery Flower: comprobar que `last_run_at` de cada tarea se actualiza correctamente.

## Notes

- Beat es un proceso separado de los workers — arrancar con supervisor o como Deployment independiente en Kubernetes.
- Si falla la purga, Alertmanager debe notificar inmediatamente — es un incidente de compliance GDPR.
- Documentar el TTL exacto en el DPA (Data Processing Agreement) del cliente.