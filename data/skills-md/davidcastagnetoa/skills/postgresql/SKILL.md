---
name: postgresql
description: Configuración y administración base de PostgreSQL para el datastore del sistema KYC
type: Framework
priority: Esencial
mode: Self-hosted
---

# postgresql

Configuración y administración base de PostgreSQL como motor de base de datos del sistema de verificación de identidad. Cubre la gestión de usuarios, permisos, tablespaces, tuning de rendimiento y configuraciones de seguridad necesarias para operar el datastore del pipeline KYC de forma segura y eficiente, independientemente de la versión específica de PostgreSQL.

## When to use

Usa esta skill cuando necesites administrar PostgreSQL a nivel de configuración: crear usuarios, ajustar permisos, optimizar parámetros de rendimiento o configurar seguridad del servidor. Pertenece al **database_agent** y se centra en la administración del motor, sin cubrir ORM ni migraciones.

## Instructions

1. Crear usuarios y roles con permisos mínimos para cada componente del pipeline:
```sql
-- Rol de aplicación (backend FastAPI)
CREATE ROLE verifid_app LOGIN PASSWORD 'secure_app_password';
GRANT CONNECT ON DATABASE verifid_kyc TO verifid_app;
GRANT USAGE ON SCHEMA kyc TO verifid_app;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA kyc TO verifid_app;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA kyc TO verifid_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA kyc
    GRANT SELECT, INSERT, UPDATE ON TABLES TO verifid_app;

-- Rol de solo lectura para auditoría
CREATE ROLE verifid_readonly LOGIN PASSWORD 'secure_ro_password';
GRANT CONNECT ON DATABASE verifid_kyc TO verifid_readonly;
GRANT USAGE ON SCHEMA kyc TO verifid_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA kyc TO verifid_readonly;

-- Rol de migraciones (solo para Alembic)
CREATE ROLE verifid_migrations LOGIN PASSWORD 'secure_migration_password';
GRANT ALL ON SCHEMA kyc TO verifid_migrations;
GRANT ALL ON ALL TABLES IN SCHEMA kyc TO verifid_migrations;
```

2. Configurar parámetros de rendimiento en `postgresql.conf` según los recursos del servidor:
```conf
# Memoria
shared_buffers = '25%_of_RAM'        # Ej: 2GB para 8GB RAM
effective_cache_size = '75%_of_RAM'   # Ej: 6GB para 8GB RAM
work_mem = '64MB'
maintenance_work_mem = '512MB'

# WAL y checkpoints
wal_level = 'replica'
checkpoint_completion_target = 0.9
max_wal_size = '2GB'
min_wal_size = '512MB'

# Planner
random_page_cost = 1.1               # Para SSD
effective_io_concurrency = 200        # Para SSD

# Conexiones
max_connections = 200
```

3. Configurar autenticación segura en `pg_hba.conf`:
```conf
# Conexiones locales
local   all             postgres                                peer
local   verifid_kyc     verifid_app                             scram-sha-256

# Conexiones desde la red del cluster
host    verifid_kyc     verifid_app     10.0.0.0/8              scram-sha-256
host    verifid_kyc     verifid_readonly 10.0.0.0/8             scram-sha-256
hostssl verifid_kyc     verifid_migrations 10.0.0.0/8           scram-sha-256

# Bloquear todo lo demás
host    all             all             0.0.0.0/0               reject
```

4. Habilitar SSL para conexiones cifradas:
```conf
# postgresql.conf
ssl = on
ssl_cert_file = '/etc/ssl/certs/server.crt'
ssl_key_file = '/etc/ssl/private/server.key'
ssl_min_protocol_version = 'TLSv1.3'
```

5. Configurar logging para auditoría del pipeline:
```conf
log_statement = 'mod'
log_min_duration_statement = 500
log_connections = on
log_disconnections = on
log_lock_waits = on
log_line_prefix = '%t [%p] %u@%d '
```

6. Crear índices esenciales para las queries más frecuentes del pipeline:
```sql
CREATE INDEX idx_sessions_status ON kyc.verification_sessions(status);
CREATE INDEX idx_sessions_created ON kyc.verification_sessions(created_at DESC);
CREATE INDEX idx_sessions_device ON kyc.verification_sessions(device_fingerprint);
CREATE INDEX idx_audit_session ON kyc.audit_logs(session_id);
CREATE INDEX idx_audit_module ON kyc.audit_logs(module_name, created_at DESC);
```

7. Configurar autovacuum agresivo para tablas de alta escritura:
```sql
ALTER TABLE kyc.verification_sessions SET (
    autovacuum_vacuum_scale_factor = 0.05,
    autovacuum_analyze_scale_factor = 0.02,
    autovacuum_vacuum_cost_delay = 10
);

ALTER TABLE kyc.audit_logs SET (
    autovacuum_vacuum_scale_factor = 0.05,
    autovacuum_analyze_scale_factor = 0.02
);
```

## Notes

- Esta skill cubre la administración base de PostgreSQL; para la versión 16 específica usar `postgresql_16`, para ORM usar `sqlalchemy_async`, y para migraciones usar `alembic`.
- Siempre usar `scram-sha-256` como método de autenticación en lugar de `md5`; es el estándar de seguridad recomendado desde PostgreSQL 14.
- Ajustar `shared_buffers` y `effective_cache_size` proporcionalmente a la RAM disponible; los valores por defecto de PostgreSQL son conservadores y subóptimos para cargas de trabajo KYC.
