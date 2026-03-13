---
name: pg_stat_statements
description: Monitorización de queries lentas y optimización de rendimiento del pipeline KYC
type: Tool
priority: Recomendada
mode: Self-hosted
---

# pg_stat_statements

pg_stat_statements es una extensión de PostgreSQL que recopila estadísticas de ejecución de todas las queries SQL, permitiendo identificar consultas lentas, queries sin índices adecuados y patrones de acceso ineficientes en el pipeline de verificación de identidad. Es la herramienta fundamental para optimizar el rendimiento de las operaciones de lectura y escritura de sesiones de verificación, logs de auditoría y scores de módulos.

## When to use

Usa esta skill cuando necesites diagnosticar problemas de rendimiento en las queries del pipeline KYC, identificar índices faltantes o monitorizar el impacto de cambios en el schema. Pertenece al **database_agent** y se usa durante la optimización continua del sistema en producción.

## Instructions

1. Habilitar la extensión en PostgreSQL:
```sql
-- En postgresql.conf
-- shared_preload_libraries = 'pg_stat_statements'
-- pg_stat_statements.max = 10000
-- pg_stat_statements.track = 'all'

CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
```

2. Reiniciar PostgreSQL tras modificar `shared_preload_libraries` (requiere reinicio, no solo reload):
```bash
# Docker
docker restart postgres

# Systemd
sudo systemctl restart postgresql
```

3. Consultar las queries más lentas del pipeline de verificación:
```sql
SELECT
    queryid,
    calls,
    round(total_exec_time::numeric, 2) AS total_ms,
    round(mean_exec_time::numeric, 2) AS mean_ms,
    round(max_exec_time::numeric, 2) AS max_ms,
    rows,
    query
FROM pg_stat_statements
WHERE dbname = 'verifid_kyc'
ORDER BY mean_exec_time DESC
LIMIT 20;
```

4. Identificar queries con alto I/O que podrían beneficiarse de índices:
```sql
SELECT
    queryid,
    calls,
    shared_blks_read + shared_blks_hit AS total_blocks,
    round(
        100.0 * shared_blks_hit / NULLIF(shared_blks_read + shared_blks_hit, 0), 2
    ) AS cache_hit_ratio,
    query
FROM pg_stat_statements
WHERE dbname = 'verifid_kyc'
    AND calls > 10
ORDER BY shared_blks_read DESC
LIMIT 20;
```

5. Monitorizar queries específicas del módulo de decisión y auditoría:
```sql
-- Queries relacionadas con sesiones de verificación
SELECT calls, mean_exec_time, query
FROM pg_stat_statements
WHERE query LIKE '%verification_sessions%'
ORDER BY total_exec_time DESC;

-- Queries de inserción de audit logs
SELECT calls, mean_exec_time, rows, query
FROM pg_stat_statements
WHERE query LIKE '%audit_logs%'
ORDER BY calls DESC;
```

6. Resetear estadísticas periódicamente para obtener métricas frescas:
```sql
-- Resetear todas las estadísticas
SELECT pg_stat_statements_reset();

-- Útil después de cambios de schema o índices para medir el impacto
```

7. Crear una vista materializada para dashboards de rendimiento:
```sql
CREATE MATERIALIZED VIEW kyc.query_performance AS
SELECT
    queryid,
    calls,
    round(total_exec_time::numeric, 2) AS total_ms,
    round(mean_exec_time::numeric, 2) AS mean_ms,
    rows,
    left(query, 200) AS query_preview
FROM pg_stat_statements
WHERE dbname = 'verifid_kyc'
    AND calls > 5
ORDER BY total_exec_time DESC
LIMIT 100;

-- Refrescar periódicamente
REFRESH MATERIALIZED VIEW kyc.query_performance;
```

## Notes

- `pg_stat_statements` requiere estar en `shared_preload_libraries`, lo que implica un reinicio de PostgreSQL; planificar la activación durante una ventana de mantenimiento.
- Usar `pg_stat_statements.track = 'all'` para capturar queries de funciones y procedimientos almacenados; con `top` solo se capturan queries de nivel superior.
- Combinar los datos de pg_stat_statements con `EXPLAIN (ANALYZE, BUFFERS)` en las queries más lentas para obtener planes de ejecución detallados y crear los índices óptimos.
