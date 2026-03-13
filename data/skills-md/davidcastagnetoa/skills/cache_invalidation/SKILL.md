---
name: cache_invalidation
description: Invalidación activa de claves cuando los datos subyacentes cambian
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# cache_invalidation

Estrategia de invalidación activa de caché para mantener la consistencia entre Redis y PostgreSQL. Cuando los datos de origen cambian, las keys de caché correspondientes se eliminan proactivamente.

## When to use

Usar en el `cache_agent` para invalidar datos cacheados cuando se actualizan en PostgreSQL: blacklists, configuración de umbrales, y datos de sesión modificados.

## Instructions

1. **Write-through**: al actualizar PostgreSQL, invalidar Redis en la misma transacción.
   ```python
   async with db.transaction():
       await db.execute(update_query)
       await redis.delete(f'cache:{key}')
   ```
2. **Pattern-based**: invalidar por patrón: `redis.delete(*redis.keys('config:*'))`.
3. Para blacklist: usar pub/sub para notificar a todas las instancias.
   ```python
   redis.publish('cache:invalidate', json.dumps({'pattern': 'blacklist:*'}))
   ```
4. Implementar versioning de caché: `cache:v2:key` al cambiar estructura de datos.
5. Nunca depender solo de TTL para consistencia de datos críticos; invalidar activamente.
6. Registrar invalidaciones en métricas: `cache_invalidations_total{pattern}`.

## Notes

- Evitar `KEYS *` en producción; usar `SCAN` para buscar keys por patrón.
- La invalidación por pub/sub es eventual (milisegundos de delay); aceptable para este caso de uso.
- Para la configuración de umbrales, usar polling desde Redis cada 30s en lugar de invalidación.