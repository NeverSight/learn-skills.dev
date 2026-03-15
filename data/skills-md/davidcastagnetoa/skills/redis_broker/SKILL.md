---
name: redis_broker
description: Backend de mensajería para Celery con baja latencia
type: Framework
priority: Esencial
mode: Self-hosted
---

# redis_broker

Redis como broker de mensajería para Celery ofrece la menor latencia posible (<1ms) para despacho de tareas. Es la opción preferida sobre RabbitMQ por simplicidad y rendimiento.

## When to use

Usar en el `worker_pool_agent` como broker de mensajería para Celery. Redis ya está desplegado para caché, lo que reduce la complejidad operativa.

## Instructions

1. Configurar en Celery: `broker_url = 'redis://redis:6379/0'`.
2. Usar database separada del caché: `/0` para broker, `/1` para results.
3. Configurar visibilidad de tareas: `broker_transport_options = {'visibility_timeout': 3600}`.
4. Habilitar persistencia en Redis para no perder tareas en reinicios.
5. Configurar `broker_connection_retry_on_startup = True`.
6. Monitorizar profundidad de colas: `redis-cli LLEN celery` o via Flower.
7. Alertar si la profundidad de cola supera el umbral configurado.

## Notes

- Redis broker no soporta prioridades nativas; usar múltiples colas con workers dedicados.
- Para garantías de entrega más estrictas, considerar RabbitMQ como alternativa.
- El visibility_timeout debe ser mayor que el task time limit más largo.
