---
name: asyncpg
description: Cliente PostgreSQL async de alto rendimiento para el backend FastAPI del pipeline KYC
type: Library
priority: Esencial
mode: Self-hosted
---

# asyncpg

asyncpg es un driver PostgreSQL asíncrono de alto rendimiento para Python, diseñado para maximizar el throughput en aplicaciones asyncio como el backend FastAPI del sistema KYC. Proporciona acceso directo al protocolo binario de PostgreSQL sin capas intermedias, ofreciendo latencias significativamente menores que los drivers síncronos en operaciones de lectura/escritura de sesiones de verificación.

## When to use

Usa esta skill cuando necesites configurar el acceso directo async a PostgreSQL desde el backend FastAPI del pipeline de verificación. Pertenece al **database_agent** y se enfoca exclusivamente en el driver asyncpg, sin incluir pooling externo ni ORM.

## Instructions

1. Instalar asyncpg como dependencia del backend:
```bash
pip install asyncpg
```

2. Crear una conexión básica al datastore de verificaciones:
```python
import asyncpg

async def get_connection():
    conn = await asyncpg.connect(
        host='localhost',
        port=5432,
        user='verifid_app',
        password='secure_password',
        database='verifid_kyc',
        timeout=10,
        statement_cache_size=100
    )
    return conn
```

3. Configurar el pool de conexiones interno de asyncpg para el pipeline:
```python
import asyncpg

async def create_pool():
    pool = await asyncpg.create_pool(
        dsn='postgresql://verifid_app:password@localhost:5432/verifid_kyc',
        min_size=5,
        max_size=20,
        max_inactive_connection_lifetime=300,
        command_timeout=30
    )
    return pool
```

4. Implementar queries parametrizadas para insertar sesiones de verificación:
```python
async def create_verification_session(pool, session_data: dict):
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            '''
            INSERT INTO kyc.verification_sessions
                (status, ip_address, device_fingerprint)
            VALUES ($1, $2::inet, $3)
            RETURNING session_id, created_at
            ''',
            session_data['status'],
            session_data['ip_address'],
            session_data['device_fingerprint']
        )
        return dict(row)
```

5. Implementar transacciones para operaciones atómicas del pipeline:
```python
async def complete_verification(pool, session_id: str, score: float, reasons: list):
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(
                '''
                UPDATE kyc.verification_sessions
                SET status = $1, confidence_score = $2,
                    reasons = $3::jsonb, completed_at = now()
                WHERE session_id = $4
                ''',
                'verified' if score > 0.85 else 'rejected',
                score, json.dumps(reasons), session_id
            )
            await conn.execute(
                '''
                INSERT INTO kyc.audit_logs (session_id, module_name, module_score, details)
                VALUES ($1, 'decision_engine', $2, $3::jsonb)
                ''',
                session_id, score, json.dumps({'reasons': reasons})
            )
```

6. Registrar codecs personalizados para tipos JSONB usados en resultados de verificación:
```python
import json

async def init_connection(conn):
    await conn.set_type_codec(
        'jsonb',
        encoder=json.dumps,
        decoder=json.loads,
        schema='pg_catalog'
    )
```

7. Integrar el pool con el ciclo de vida de FastAPI:
```python
from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
async def startup():
    app.state.db_pool = await asyncpg.create_pool(
        dsn='postgresql://verifid_app:password@localhost:5432/verifid_kyc',
        min_size=5,
        max_size=20,
        init=init_connection
    )

@app.on_event("shutdown")
async def shutdown():
    await app.state.db_pool.close()
```

## Notes

- asyncpg usa el protocolo binario de PostgreSQL directamente, lo que lo hace entre 2x y 5x más rápido que psycopg2 en operaciones típicas del pipeline KYC.
- Esta skill cubre exclusivamente el driver asyncpg; para pooling externo con PgBouncer consultar la skill `pgbouncer`, y para ORM async consultar `sqlalchemy_async`.
- Siempre usar queries parametrizadas (`$1, $2`) en lugar de interpolación de strings para prevenir SQL injection en los endpoints de verificación.
