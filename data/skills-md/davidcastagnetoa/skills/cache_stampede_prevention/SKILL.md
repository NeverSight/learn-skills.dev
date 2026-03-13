---
name: cache_stampede_prevention
description: Evitar que múltiples workers recarguen el mismo dato al expirar simultáneamente
type: Algorithm
priority: Recomendada
mode: Self-hosted
---

# cache_stampede_prevention

Prevención de cache stampede (thundering herd) cuando una key popular expira y múltiples workers intentan recalcularla simultáneamente, saturando el backend.

## When to use

Usar en el `cache_agent` para keys de alta concurrencia como configuración de umbrales, blacklists y resultados de modelos. No es necesario para keys de sesión individual.

## Instructions

1. **Probabilistic Early Expiration**: renovar la key antes de que expire.
   ```python
   ttl = redis.ttl(key)
   if ttl < threshold and random.random() < probability:
       value = recompute()
       redis.set(key, value, ex=original_ttl)
   ```
2. **Lock-based**: usar lock distribuido para que solo un worker recalcule.
   ```python
   if redis.set(f'lock:{key}', 1, nx=True, ex=5):
       value = recompute()
       redis.set(key, value, ex=ttl)
       redis.delete(f'lock:{key}')
   ```
3. Configurar jitter en TTLs: `ttl = base_ttl + random.randint(0, 60)`.
4. Para la blacklist, usar refresh programado (Celery Beat) en lugar de TTL.
5. Monitorizar cache miss rate por key pattern para detectar stampedes.

## Notes

- Probabilistic Early Expiration es más simple y no requiere locks distribuidos.
- El lock-based approach garantiza un solo recálculo pero puede causar latencia si el lock se pierde.
- Combinar ambas técnicas: jitter + lock para las keys más críticas.
