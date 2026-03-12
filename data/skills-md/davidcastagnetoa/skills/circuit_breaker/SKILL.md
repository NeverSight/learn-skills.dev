---
name: circuit_breaker
description: Patrón circuit breaker con pybreaker/tenacity para aislar fallos de agentes sin afectar al sistema completo
type: Library
priority: Esencial
mode: Self-hosted
---

# circuit_breaker

El circuit breaker detecta cuando un servicio/agente está fallando repetidamente y corta el flujo de peticiones temporalmente, evitando la cascada de fallos y permitiendo recuperación.

## When to use

Envolver todas las llamadas a servicios externos, modelos ML y otros agentes con un circuit breaker.

## Instructions

1. Instalar: `pip install pybreaker tenacity`.
2. Con pybreaker:
   ```python
   import pybreaker
   face_match_breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60)
   
   @face_match_breaker
   def call_face_match_service(embedding_1, embedding_2):
       return face_match_client.compare(embedding_1, embedding_2)
   ```
3. Estados: CLOSED (normal) → OPEN (fallo, rechaza peticiones) → HALF_OPEN (prueba recuperación).
4. Configurar `fail_max=5` (5 fallos consecutivos → OPEN) y `reset_timeout=60` (60s antes de HALF_OPEN).
5. En OPEN: devolver respuesta de fallback o error con código específico `SERVICE_UNAVAILABLE`.
6. Emitir métrica a Prometheus cuando el breaker cambia de estado.

## Notes

- `tenacity` complementa el circuit breaker con retry + backoff exponencial para errores transitorios.
- Cada agente debe tener su propio circuit breaker con parámetros ajustados a su SLO.