---
name: redis_py_async
description: Cliente Python async para Redis sin bloquear el event loop
type: Library
priority: Esencial
mode: Self-hosted
---

# redis_py_async

`redis-py` con soporte async nativo permite operaciones Redis no bloqueantes desde FastAPI y otros frameworks asyncio. Reemplaza al deprecado `aioredis` que ahora está integrado en redis-py 4.2+.

## When to use

Usar en todos los agentes Python que acceden a Redis a través del `cache_agent`. Nunca usar el cliente síncrono en handlers async de FastAPI.

## Instructions

1. Instalar: `pip install redis[hiredis]` (hiredis para parser C de alto rendimiento).
2. Crear pool de conexiones async:
   ```python
   import redis.asyncio as aioredis
   pool = aioredis.ConnectionPool.from_url('redis://localhost:6379', max_connections=20)
   client = aioredis.Redis(connection_pool=pool)
   ```
3. Usar en handlers: `value = await client.get('key')`.
4. Usar pipeline para operaciones múltiples:
   ```python
   async with client.pipeline() as pipe:
       pipe.get('key1')
       pipe.get('key2')
       results = await pipe.execute()
   ```
5. Cerrar pool en shutdown: `await pool.disconnect()`.
6. Configurar `socket_timeout=2` y `socket_connect_timeout=1`.

## Notes

- `hiredis` es 10x más rápido que el parser Python puro; siempre instalarlo.
- El pool de conexiones evita el overhead de conectar/desconectar en cada operación.
- `aioredis` standalone está deprecado; usar `redis.asyncio` de redis-py >= 4.2.
