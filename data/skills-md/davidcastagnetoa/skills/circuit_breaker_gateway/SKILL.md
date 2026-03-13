---
name: circuit_breaker_gateway
description: Abrir el circuito si un servicio downstream falla repetidamente para evitar cascada de errores
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# circuit_breaker_gateway

El circuit breaker en el gateway detecta cuando un microservicio downstream (liveness_agent, face_match_agent, etc.) está fallando y deja de enviarle tráfico temporalmente. Esto previene que errores en un servicio saturen el gateway y degraden toda la experiencia.

## When to use

Usar para todos los servicios upstream configurados en Nginx. Integrar con el health monitor para que el estado del circuito se refleje en los dashboards de Grafana.

## Instructions

1. Instalar en Python con tenacity para los clientes internos: `pip install tenacity pybreaker`
2. Configurar circuit breaker en `backend/core/circuit_breaker.py`:
   ```python
   from pybreaker import CircuitBreaker
   liveness_breaker = CircuitBreaker(fail_max=5, reset_timeout=30)
   face_match_breaker = CircuitBreaker(fail_max=5, reset_timeout=30)
   @liveness_breaker
   async def call_liveness_agent(payload): ...
   ```
3. En Nginx, usar `proxy_next_upstream error timeout http_500 http_502 http_503` para routing automático al siguiente upstream.
4. Configurar `proxy_connect_timeout 2s` y `proxy_read_timeout 10s` — timeouts cortos evitan que un upstream lento colapse el gateway.
5. Estado del circuito: CLOSED (normal) → OPEN (fallo, rechaza requests) → HALF-OPEN (prueba recuperación).
6. Exponer estado del circuito como métrica Prometheus: `circuit_breaker_state{service="liveness_agent"}`.
7. Alertar en Grafana si cualquier circuito lleva más de 60 segundos en estado OPEN.

## Notes

- `fail_max=5` significa que tras 5 fallos consecutivos se abre el circuito.
- `reset_timeout=30` segundos en OPEN antes de probar HALF-OPEN.
- Cuando el circuito está OPEN, devolver degraded response (no 500) — informar al cliente del estado parcial.
