---
name: pgbouncer
description: Connection pooler para PostgreSQL que reduce overhead de conexiones en el pipeline KYC
type: Tool
priority: Esencial
mode: Self-hosted
---

# pgbouncer

PgBouncer es un connection pooler ligero para PostgreSQL que gestiona y reutiliza conexiones a la base de datos, reduciendo el overhead de establecimiento de conexiones en el pipeline de verificación de identidad de alta concurrencia. Permite atender miles de conexiones de aplicación con un número reducido de conexiones reales a PostgreSQL, esencial cuando múltiples workers del pipeline procesan verificaciones simultáneamente.

## When to use

Usa esta skill cuando necesites reducir el consumo de conexiones PostgreSQL del pipeline KYC, especialmente en escenarios de alta concurrencia con múltiples workers FastAPI. Pertenece al **database_agent** y se centra exclusivamente en la configuración y despliegue de PgBouncer como pooler independiente.

## Instructions

1. Añadir PgBouncer como servicio en `docker-compose.yml`:
```yaml
services:
  pgbouncer:
    image: edoburu/pgbouncer:latest
    environment:
      DATABASE_URL: postgres://verifid_app:password@postgres:5432/verifid_kyc
      POOL_MODE: transaction
      MAX_CLIENT_CONN: 500
      DEFAULT_POOL_SIZE: 25
      MIN_POOL_SIZE: 5
      RESERVE_POOL_SIZE: 5
    ports:
      - "6432:6432"
    depends_on:
      postgres:
        condition: service_healthy
```

2. Configurar `pgbouncer.ini` con los parámetros optimizados para el pipeline:
```ini
[databases]
verifid_kyc = host=postgres port=5432 dbname=verifid_kyc

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = scram-sha-256
auth_file = /etc/pgbouncer/userlist.txt

pool_mode = transaction
max_client_conn = 500
default_pool_size = 25
min_pool_size = 5
reserve_pool_size = 5
reserve_pool_timeout = 3

server_lifetime = 3600
server_idle_timeout = 600
client_idle_timeout = 300

log_connections = 1
log_disconnections = 1
log_pooler_errors = 1
stats_period = 60
```

3. Crear el archivo de autenticación `userlist.txt`:
```
"verifid_app" "SCRAM-SHA-256$4096:salt$stored_key:server_key"
```
Generar el hash con: `psql -c "SELECT concat('\"', usename, '\" \"', passwd, '\"') FROM pg_shadow WHERE usename = 'verifid_app';"`

4. Configurar el backend FastAPI para conectar a través de PgBouncer:
```python
# Apuntar al puerto de PgBouncer en lugar de PostgreSQL directamente
DATABASE_URL = "postgresql://verifid_app:password@pgbouncer:6432/verifid_kyc"
```

5. Seleccionar el modo de pooling adecuado según el patrón de uso:
```
# transaction: recomendado para el pipeline KYC
#   - Conexión asignada solo durante la transacción
#   - Mejor utilización de conexiones
#   - No soporta LISTEN/NOTIFY ni prepared statements cross-transaction

# session: usar solo si se necesitan prepared statements persistentes
#   - Conexión asignada durante toda la sesión del cliente

# statement: evitar - demasiado restrictivo para el pipeline
```

6. Configurar monitorización del pool consultando la consola administrativa:
```sql
-- Conectar a la consola admin de PgBouncer
psql -p 6432 -U pgbouncer pgbouncer

-- Ver estado de los pools
SHOW POOLS;
-- Ver estadísticas
SHOW STATS;
-- Ver clientes conectados
SHOW CLIENTS;
-- Ver servidores backend
SHOW SERVERS;
```

7. Añadir healthcheck para PgBouncer en el compose:
```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -h localhost -p 6432"]
  interval: 10s
  timeout: 5s
  retries: 3
```

## Notes

- En modo `transaction`, PgBouncer no soporta prepared statements que persistan entre transacciones; si se usa asyncpg con PgBouncer, desactivar el statement cache con `statement_cache_size=0`.
- El `default_pool_size` debe dimensionarse según el número de workers FastAPI y la concurrencia esperada del pipeline; consultar la skill `connection_pool_sizing` para el cálculo detallado.
- PgBouncer es un componente crítico para la disponibilidad del pipeline; considerar desplegar múltiples instancias detrás de un balanceador para eliminar el punto único de fallo.
