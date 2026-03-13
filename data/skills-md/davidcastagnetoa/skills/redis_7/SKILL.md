---
name: redis_7
description: Store principal de caché O(1) en lecturas/escrituras
type: Framework
priority: Esencial
mode: Self-hosted
---

# redis_7

Redis 7+ es el store de caché principal del sistema. Proporciona operaciones O(1) para datos de sesión, rate limiting, blacklists y embeddings cacheados con soporte nativo de streams, pub/sub y módulos.

## When to use

Usar en el `cache_agent` como store central de caché para todo el sistema. Cada agente accede a Redis a través del cache_agent para datos temporales de alta velocidad.

## Instructions

1. Desplegar: `docker run -d --name redis redis:7-alpine --requirepass <password>`.
2. Configurar `maxmemory`: `maxmemory 2gb` (ajustar según hardware).
3. Configurar política de eviction: `maxmemory-policy allkeys-lru`.
4. Habilitar ACL por servicio: cada agente tiene su propio usuario Redis con permisos mínimos.
5. Configurar bind y protected-mode para seguridad de red.
6. Habilitar keyspace notifications para eventos de expiración: `notify-keyspace-events Ex`.
7. Monitorizar con `INFO` y exportar métricas a Prometheus.

## Notes

- Redis 7 incluye funciones Lua lado servidor y mejoras de ACL sobre Redis 6.
- Nunca exponer Redis a internet; solo accesible desde la red interna del cluster.
- Para datos que no caben en memoria, usar PostgreSQL; Redis es solo para datos hot.
