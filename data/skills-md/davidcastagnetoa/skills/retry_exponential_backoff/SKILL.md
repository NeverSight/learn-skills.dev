---
name: retry_exponential_backoff
description: Reintentar automáticamente errores transitorios con backoff exponencial y jitter
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# retry_exponential_backoff

Implementación de retry con backoff exponencial y jitter para manejar errores transitorios (5xx, timeouts) en las comunicaciones entre el gateway y los servicios downstream.

## When to use

Usar en el `api_gateway_agent` para reintentar automáticamente peticiones fallidas a servicios downstream. Solo reintentar errores transitorios (502, 503, 504), nunca errores de cliente (4xx).

## Instructions

1. Configurar en Nginx upstream:
   ```nginx
   proxy_next_upstream error timeout http_502 http_503 http_504;
   proxy_next_upstream_tries 3;
   proxy_next_upstream_timeout 5s;
   ```
2. Para lógica avanzada con Lua, implementar backoff exponencial:
   ```lua
   local delay = math.min(base_delay * 2^attempt, max_delay)
   delay = delay * (0.5 + math.random() * 0.5)  -- jitter
   ```
3. Base delay: 100ms, max delay: 2s, max retries: 3.
4. No reintentar peticiones POST/PUT (no idempotentes) sin confirmación.
5. Registrar cada retry en el log con `trace_id` y número de intento.
6. Incrementar contador Prometheus `gateway_retries_total` por cada retry.

## Notes

- El jitter evita thundering herd: todos los clientes reintentando al mismo tiempo.
- Si un servicio devuelve `Retry-After` header, respetar ese valor.
- Después de max retries, devolver 503 al cliente con mensaje descriptivo.