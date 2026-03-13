---
name: http_health_check_probes
description: Endpoints HTTP de health check para microservicios del pipeline KYC con reporte de dependencias
type: Protocol
priority: Esencial
mode: Self-hosted
---

# http_health_check_probes

Skill para implementar endpoints HTTP estandarizados de health check (/health, /ready, /live) en cada microservicio del pipeline de verificacion de identidad KYC. Estos endpoints reportan el estado de las dependencias criticas como base de datos PostgreSQL, cache Redis y modelos de machine learning cargados en memoria. Permiten a orquestadores y balanceadores de carga tomar decisiones informadas sobre el enrutamiento de trafico.

## When to use

Utilizar esta skill cuando el health_monitor_agent necesite implementar o actualizar los endpoints de salud HTTP en cualquier microservicio del pipeline KYC (liveness detection, OCR, face matching, document processing, antifraud, decision engine). Es el primer paso para tener observabilidad basica del sistema.

## Instructions

1. Crear un modulo `health.py` en cada microservicio con un router FastAPI dedicado:

```python
from fastapi import APIRouter, Response
from enum import Enum

health_router = APIRouter(tags=["health"])

class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
```

2. Implementar el endpoint `/live` que indica si el proceso esta vivo (simplemente responde 200):

```python
@health_router.get("/live")
async def liveness():
    return {"status": "alive"}
```

3. Implementar el endpoint `/ready` que verifica si el servicio puede aceptar trafico, comprobando dependencias:

```python
@health_router.get("/ready")
async def readiness():
    checks = {
        "database": await check_db_connection(),
        "redis": await check_redis_connection(),
        "ml_model": check_model_loaded(),
    }
    all_ready = all(v for v in checks.values())
    status_code = 200 if all_ready else 503
    return Response(
        content=json.dumps({"ready": all_ready, "checks": checks}),
        status_code=status_code,
        media_type="application/json"
    )
```

4. Implementar el endpoint `/health` que ofrece un reporte detallado con latencias de cada dependencia:

```python
@health_router.get("/health")
async def health_check():
    db_latency = await measure_db_latency()
    redis_latency = await measure_redis_latency()
    model_status = check_model_inference_ready()
    return {
        "status": determine_overall_status(db_latency, redis_latency, model_status),
        "dependencies": {
            "postgresql": {"connected": True, "latency_ms": db_latency},
            "redis": {"connected": True, "latency_ms": redis_latency},
            "ml_models": model_status,
        },
        "uptime_seconds": get_uptime(),
        "version": settings.APP_VERSION,
    }
```

5. Crear funciones auxiliares para verificar cada dependencia con timeouts cortos (maximo 2 segundos):

```python
async def check_db_connection(timeout: float = 2.0) -> bool:
    try:
        async with asyncio.timeout(timeout):
            await db.execute("SELECT 1")
        return True
    except Exception:
        return False
```

6. Registrar el router en la aplicacion FastAPI principal de cada microservicio:

```python
app.include_router(health_router, prefix="")
```

7. Configurar respuestas con codigos HTTP apropiados: 200 para saludable, 503 para no disponible, 429 para sobrecargado:

```python
def determine_overall_status(db_lat, redis_lat, model_ok):
    if not model_ok or db_lat is None:
        return HealthStatus.UNHEALTHY
    if db_lat > 500 or redis_lat > 100:
        return HealthStatus.DEGRADED
    return HealthStatus.HEALTHY
```

8. Asegurar que los endpoints de health no requieran autenticacion y no generen logs excesivos en produccion (filtrar en middleware de logging).

## Notes

- Los endpoints de health check deben responder en menos de 3 segundos; si una dependencia tarda mas, marcarla como degradada pero no bloquear la respuesta completa.
- Cada microservicio del pipeline KYC (liveness, OCR, face_match, doc_processing, antifraud, decision) debe tener sus propios checks adaptados a sus dependencias especificas (por ejemplo, face_match verifica que ArcFace este cargado).
- No exponer informacion sensible en los endpoints de salud (versiones exactas de dependencias, credenciales, rutas internas); limitar la informacion detallada a redes internas.
