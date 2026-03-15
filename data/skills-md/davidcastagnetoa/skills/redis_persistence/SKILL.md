---
name: redis_persistence
description: Durabilidad con RDB para snapshots y AOF para WAL de operaciones
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# redis_persistence

Configuración de persistencia Redis con RDB (snapshots periódicos) y AOF (append-only file) para recuperar datos tras un reinicio. Combinar ambos métodos ofrece el mejor balance entre rendimiento y durabilidad.

## When to use

Configurar en el `cache_agent` para que los datos de sesión activa y rate limiting sobrevivan a reinicios del servicio Redis. Sin persistencia, un reinicio pierde todas las sesiones en curso.

## Instructions

1. Habilitar RDB: `save 900 1`, `save 300 10`, `save 60 10000`.
2. Habilitar AOF: `appendonly yes`, `appendfsync everysec`.
3. Configurar reescritura automática de AOF: `auto-aof-rewrite-percentage 100`, `auto-aof-rewrite-min-size 64mb`.
4. Montar volumen persistente en Docker/K8s para `/data`.
5. Verificar integridad: `redis-check-aof --fix` y `redis-check-rdb`.
6. Backup del RDB a almacenamiento externo (MinIO) diariamente.
7. Probar la restauración periódicamente como parte del disaster recovery.

## Notes

- `appendfsync everysec` pierde como máximo 1 segundo de datos; buen balance rendimiento/durabilidad.
- RDB es más eficiente para backups; AOF para mínima pérdida de datos.
- En Kubernetes, usar PersistentVolumeClaim con StorageClass apropiada.
