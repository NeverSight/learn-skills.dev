---
name: celery_flower
description: Dashboard de monitorización de Celery para estado de workers y colas
type: Tool
priority: Recomendada
mode: Self-hosted
---

# celery_flower

Flower es el dashboard web de monitorización para Celery. Muestra en tiempo real el estado de workers, tareas en curso, profundidad de colas y métricas de rendimiento.

## When to use

Usar en el `worker_pool_agent` para visibilidad operativa de las colas de tareas. Especialmente útil en desarrollo y debugging, y como complemento a Grafana en producción.

## Instructions

1. Instalar: `pip install flower`.
2. Arrancar: `celery -A verifid flower --port=5555`.
3. Acceder al dashboard en `http://localhost:5555`.
4. Configurar autenticación: `--basic-auth=admin:password`.
5. Habilitar API REST para integración con alertas: `GET /api/workers`.
6. Configurar persistencia de datos: `--persistent=True --db=flower.db`.
7. En producción, proteger con Nginx reverse proxy y autenticación.

## Notes

- Flower consume poca memoria (~50MB) y se puede desplegar como sidecar.
- No exponer Flower directamente a internet; siempre detrás de Nginx con auth.
- Para métricas duraderas, exportar a Prometheus; Flower es mejor para debugging puntual.