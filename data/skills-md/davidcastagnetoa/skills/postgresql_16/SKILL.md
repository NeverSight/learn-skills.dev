---
name: postgresql_16
description: PostgreSQL 16 como base de datos principal del sistema KYC de verificación de identidad
type: Framework
priority: Esencial
mode: Self-hosted
---

# postgresql_16

PostgreSQL 16 es la base de datos relacional principal del pipeline de verificación de identidad. Se utiliza para persistir sesiones de verificación, resultados de auditoría, configuración del pipeline KYC y los scores emitidos por cada módulo. Aprovecha las mejoras de rendimiento y las nuevas funcionalidades de la versión 16 como paralelismo mejorado y logical replication optimizada.

## When to use

Usa esta skill cuando necesites instalar, configurar o desplegar PostgreSQL 16 como datastore principal del sistema KYC. Pertenece al **database_agent** y se aplica durante la fase de setup inicial de infraestructura o al migrar desde versiones anteriores.

## Instructions

1. Definir la versión exacta de PostgreSQL 16 en el Dockerfile del servicio de base de datos:
```dockerfile
FROM postgres:16-alpine
ENV POSTGRES_DB=verifid_kyc
ENV POSTGRES_USER=verifid_admin
COPY ./init-scripts/ /docker-entrypoint-initdb.d/
```

2. Configurar parámetros de rendimiento en `postgresql.conf` adaptados al pipeline KYC:
```conf
shared_buffers = '1GB'
effective_cache_size = '3GB'
work_mem = '64MB'
maintenance_work_mem = '256MB'
max_connections = 200
wal_level = 'replica'
max_wal_senders = 5
```

3. Crear el schema inicial con las tablas principales del sistema de verificación:
```sql
CREATE SCHEMA kyc;

CREATE TABLE kyc.verification_sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    confidence_score NUMERIC(5,4),
    reasons JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at TIMESTAMPTZ,
    ip_address INET,
    device_fingerprint TEXT
);

CREATE TABLE kyc.audit_logs (
    log_id BIGSERIAL PRIMARY KEY,
    session_id UUID REFERENCES kyc.verification_sessions(session_id),
    module_name VARCHAR(50) NOT NULL,
    module_score NUMERIC(5,4),
    details JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

4. Habilitar extensiones necesarias para el pipeline:
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
```

5. Configurar roles y permisos según el principio de mínimo privilegio:
```sql
CREATE ROLE verifid_app LOGIN PASSWORD 'secure_password';
GRANT USAGE ON SCHEMA kyc TO verifid_app;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA kyc TO verifid_app;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA kyc TO verifid_app;
```

6. Configurar `pg_hba.conf` para restringir accesos solo desde la red interna del cluster:
```conf
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    verifid_kyc     verifid_app     10.0.0.0/8              scram-sha-256
host    verifid_kyc     verifid_admin   10.0.0.0/8              scram-sha-256
host    all             all             0.0.0.0/0               reject
```

7. Añadir el servicio al `docker-compose.yml` del proyecto:
```yaml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: verifid_kyc
      POSTGRES_USER: verifid_admin
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U verifid_admin -d verifid_kyc"]
      interval: 10s
      timeout: 5s
      retries: 5
```

## Notes

- PostgreSQL 16 introduce mejoras significativas en paralelismo de queries y logical replication que benefician las consultas analíticas sobre sesiones de verificación.
- Las imágenes biométricas NO deben almacenarse en PostgreSQL; se usa MinIO para almacenamiento temporal de blobs con políticas de lifecycle de 15 minutos.
- Siempre usar `TIMESTAMPTZ` en lugar de `TIMESTAMP` para garantizar consistencia temporal en despliegues multi-región del pipeline KYC.
