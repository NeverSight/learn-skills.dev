---
name: redis_cluster
description: Sharding horizontal para escalar Redis más allá de un nodo
type: Tool
priority: Recomendada
mode: Self-hosted
---

# redis_cluster

Redis Cluster distribuye datos automáticamente entre múltiples nodos usando hash slots (16384 slots). Permite escalar horizontalmente cuando un solo nodo Redis no es suficiente.

## When to use

Usar cuando el dataset de caché supera la memoria de un nodo o cuando se necesita throughput superior a ~100K ops/s. Para la mayoría de despliegues iniciales, Redis Sentinel es suficiente.

## Instructions

1. Mínimo 6 nodos: 3 masters + 3 réplicas.
2. Crear cluster: `redis-cli --cluster create node1:6379 node2:6379 ... --cluster-replicas 1`.
3. Configurar cada nodo: `cluster-enabled yes`, `cluster-config-file nodes.conf`.
4. Usar cliente cluster-aware: `redis-py` con `RedisCluster(startup_nodes=[...])`.
5. Evitar operaciones multi-key que cruzan slots: usar `{hash_tag}` para colocar keys relacionadas en el mismo slot.
6. Monitorizar redistribución de slots durante rebalanceo.
7. Configurar `cluster-node-timeout 5000` para detección de fallos.

## Notes

- Redis Cluster no soporta SELECT (múltiples databases); solo database 0.
- Las operaciones Lua multi-key deben operar en keys del mismo slot.
- Para el caso de uso de KYC, Redis Sentinel suele ser suficiente; Cluster es para escala masiva.