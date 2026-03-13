---
name: sqlalchemy_async
description: ORM async moderno con SQLAlchemy 2.0 para modelar entidades de verificación KYC
type: Library
priority: Esencial
mode: Self-hosted
---

# sqlalchemy_async

SQLAlchemy 2.0 con soporte async nativo permite modelar las entidades del pipeline de verificación KYC usando un ORM moderno y type-safe. Proporciona un mapeo declarativo de tablas como verification_sessions, audit_logs y module_scores a clases Python, facilitando la interacción con PostgreSQL desde el backend FastAPI de forma asíncrona y manteniendo la integridad del schema.

## When to use

Usa esta skill cuando necesites definir modelos ORM, configurar el engine async o realizar operaciones CRUD sobre las entidades del pipeline KYC usando SQLAlchemy 2.0. Pertenece al **database_agent** y se centra exclusivamente en el ORM async, sin cubrir la configuración base de PostgreSQL ni migraciones.

## Instructions

1. Instalar SQLAlchemy 2.0 con el driver async:
```bash
pip install "sqlalchemy[asyncio]>=2.0" asyncpg
```

2. Configurar el engine async y la session factory:
```python
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

DATABASE_URL = "postgresql+asyncpg://verifid_app:password@localhost:5432/verifid_kyc"

engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    echo=False
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
```

3. Definir los modelos declarativos para las entidades del pipeline KYC:
```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Numeric, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, INET, TIMESTAMPTZ
from datetime import datetime
from uuid import uuid4, UUID as PyUUID

class Base(DeclarativeBase):
    pass

class VerificationSession(Base):
    __tablename__ = 'verification_sessions'
    __table_args__ = {'schema': 'kyc'}

    session_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    status: Mapped[str] = mapped_column(String(20), default='pending')
    confidence_score: Mapped[float | None] = mapped_column(Numeric(5, 4))
    reasons: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMPTZ, default=datetime.utcnow
    )
    completed_at: Mapped[datetime | None] = mapped_column(TIMESTAMPTZ)
    ip_address: Mapped[str | None] = mapped_column(INET)
    device_fingerprint: Mapped[str | None] = mapped_column(String)

    audit_logs: Mapped[list["AuditLog"]] = relationship(back_populates="session")

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    __table_args__ = {'schema': 'kyc'}

    log_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('kyc.verification_sessions.session_id')
    )
    module_name: Mapped[str] = mapped_column(String(50))
    module_score: Mapped[float | None] = mapped_column(Numeric(5, 4))
    details: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMPTZ, default=datetime.utcnow
    )

    session: Mapped["VerificationSession"] = relationship(back_populates="audit_logs")
```

4. Crear un dependency injection para las sesiones en FastAPI:
```python
from fastapi import Depends
from typing import AsyncGenerator

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

5. Implementar operaciones CRUD para sesiones de verificación:
```python
from sqlalchemy import select

async def create_session(db: AsyncSession, ip: str, fingerprint: str):
    session = VerificationSession(
        ip_address=ip,
        device_fingerprint=fingerprint
    )
    db.add(session)
    await db.flush()
    return session

async def get_session(db: AsyncSession, session_id: PyUUID):
    stmt = select(VerificationSession).where(
        VerificationSession.session_id == session_id
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
```

6. Integrar el engine con el ciclo de vida de FastAPI:
```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
```

## Notes

- Usar `expire_on_commit=False` en la session factory para evitar lazy loads implícitos después del commit, que fallarían en contexto async.
- Esta skill cubre exclusivamente el ORM async de SQLAlchemy 2.0; para migraciones de schema usar la skill `alembic`, y para configuración base de PostgreSQL usar la skill `postgresql`.
- Al usar SQLAlchemy async con PgBouncer en modo `transaction`, configurar el engine con `pool_pre_ping=True` y evitar prepared statements.
