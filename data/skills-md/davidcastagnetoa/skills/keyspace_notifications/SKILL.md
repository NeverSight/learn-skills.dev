---
name: keyspace_notifications
description: Suscribirse a eventos de expiración de claves para ejecutar acciones de limpieza
type: Algorithm
priority: Recomendada
mode: Self-hosted
---

# keyspace_notifications

Keyspace notifications de Redis permiten suscribirse a eventos como expiración de claves, SET, DEL, etc. Útil para ejecutar acciones de limpieza automática cuando los datos de sesión expiran.

## When to use

Usar en el `cache_agent` para recibir notificaciones cuando las sesiones expiran y trigger la limpieza de datos biométricos asociados en MinIO y PostgreSQL.

## Instructions

1. Habilitar en Redis config: `notify-keyspace-events Ex` (expiración de keys).
2. Suscribirse al canal de expiración:
   ```python
   pubsub = redis.pubsub()
   await pubsub.psubscribe('__keyevent@0__:expired')
   async for message in pubsub.listen():
       expired_key = message['data']
       if expired_key.startswith('session:'):
           await cleanup_session(expired_key)
   ```
3. En `cleanup_session`: eliminar imágenes de MinIO y marcar sesión como expirada en PostgreSQL.
4. Ejecutar el listener como worker dedicado (no en el handler de peticiones).
5. Implementar retry si la limpieza falla.
6. Registrar cada limpieza en auditoría con timestamp.

## Notes

- Redis no garantiza entrega de notificaciones si el subscriber no está conectado; usar como complemento, no como único mecanismo de limpieza.
- Implementar también un Celery Beat job que limpia sesiones huérfanas cada 30 minutos como safety net.
- Las notificaciones tienen overhead; habilitar solo los eventos necesarios.