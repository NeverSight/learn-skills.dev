---
name: alembic
description: Migraciones de base de datos versionadas para evolucionar el schema del pipeline KYC
type: Tool
priority: Esencial
mode: Self-hosted
---

# alembic

Alembic es la herramienta estándar de migraciones para SQLAlchemy que permite evolucionar el schema de la base de datos del pipeline KYC de forma controlada, versionada y reversible. Cada cambio en las tablas de verificación, auditoría o configuración se registra como una migración que puede aplicarse o revertirse, garantizando consistencia entre entornos de desarrollo, staging y producción.

## When to use

Usa esta skill cuando necesites crear, aplicar o revertir migraciones del schema de base de datos del sistema de verificación. Pertenece al **database_agent** y se usa durante el desarrollo de nuevas funcionalidades que requieren cambios en el modelo de datos o al desplegar cambios a producción.

## Instructions

1. Instalar Alembic y configurarlo con soporte async:
```bash
pip install alembic
alembic init -t async alembic
```

2. Configurar `alembic.ini` con la conexión al datastore KYC:
```ini
[alembic]
script_location = alembic
sqlalchemy.url = postgresql+asyncpg://verifid_migrations:password@localhost:5432/verifid_kyc
```

3. Configurar `alembic/env.py` para usar el engine async y los modelos del pipeline:
```python
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from backend.modules.models import Base  # Importar los modelos KYC

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        include_schemas=True,
        version_table_schema='kyc'
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url")
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
        version_table_schema='kyc'
    )
    with context.begin_transaction():
        context.run_migrations()
```

4. Generar una migración automática a partir de cambios en los modelos:
```bash
alembic revision --autogenerate -m "add_document_type_to_sessions"
```

5. Revisar y editar la migración generada antes de aplicar:
```python
"""add_document_type_to_sessions"""

from alembic import op
import sqlalchemy as sa

revision = 'abc123'
down_revision = 'prev_revision'

def upgrade():
    op.add_column(
        'verification_sessions',
        sa.Column('document_type', sa.String(30), nullable=True),
        schema='kyc'
    )
    op.create_index(
        'idx_sessions_doc_type',
        'verification_sessions',
        ['document_type'],
        schema='kyc'
    )

def downgrade():
    op.drop_index('idx_sessions_doc_type', table_name='verification_sessions', schema='kyc')
    op.drop_column('verification_sessions', 'document_type', schema='kyc')
```

6. Aplicar migraciones pendientes:
```bash
# Aplicar todas las migraciones pendientes
alembic upgrade head

# Aplicar una migración específica
alembic upgrade +1

# Verificar estado actual
alembic current
alembic history --verbose
```

7. Revertir migraciones si es necesario:
```bash
# Revertir la última migración
alembic downgrade -1

# Revertir a una revisión específica
alembic downgrade abc123
```

8. Integrar migraciones en el pipeline de despliegue:
```yaml
# En el entrypoint del contenedor o job de Kubernetes
initContainers:
  - name: run-migrations
    image: verifid-backend:latest
    command: ["alembic", "upgrade", "head"]
    env:
      - name: DATABASE_URL
        valueFrom:
          secretKeyRef:
            name: db-credentials
            key: migration-url
```

## Notes

- Siempre revisar las migraciones autogeneradas antes de aplicarlas; Alembic puede no detectar correctamente cambios en índices, constraints o tipos personalizados.
- Usar un usuario de base de datos dedicado para migraciones (`verifid_migrations`) con permisos DDL, separado del usuario de la aplicación que solo tiene permisos DML.
- En producción, ejecutar migraciones como un paso previo al despliegue (init container o job) para garantizar que el schema está actualizado antes de que los pods de la aplicación arranquen.
