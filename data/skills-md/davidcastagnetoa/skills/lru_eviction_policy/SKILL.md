---
name: lru_eviction_policy
description: Gestión de memoria evictando datos menos usados cuando se llena la memoria
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# lru_eviction_policy

Política de eviction LRU (Least Recently Used) que elimina automáticamente las keys menos accedidas cuando Redis alcanza el límite de memoria configurado.

## When to use

Configurar en el `cache_agent` para garantizar que Redis nunca se queda sin memoria. Las sesiones antiguas y embeddings no accedidos se eliminan automáticamente.

## Instructions

1. Configurar maxmemory: `maxmemory 2gb`.
2. Configurar política: `maxmemory-policy allkeys-lru`.
3. Alternativa: `volatile-lru` para solo evictar keys con TTL (preservar keys permanentes).
4. Configurar samples: `maxmemory-samples 10` para mejor aproximación LRU.
5. Monitorizar evictions: `INFO stats` → `evicted_keys`.
6. Alertar si `evicted_keys` crece rápidamente (indica memoria insuficiente).
7. Ajustar maxmemory según métricas de uso real.

## Notes

- `allkeys-lru` es más seguro; evita OOM incluso si se olvida poner TTL a una key.
- Redis usa aproximación LRU (sampling), no LRU exacto; con samples=10 la precisión es excelente.
- Si las evictions son frecuentes, considerar aumentar memoria o reducir TTLs.