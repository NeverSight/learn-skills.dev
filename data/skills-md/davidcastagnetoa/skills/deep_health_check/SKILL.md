---
name: deep_health_check
description: Health checks profundos que verifican funcionalidad real de cada componente del pipeline KYC
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# deep_health_check

Skill para implementar verificaciones profundas de salud que van mas alla de la simple conectividad, ejecutando pruebas funcionales reales en cada componente del pipeline de verificacion de identidad. Incluye inferencia dummy sobre modelos ML, queries funcionales a la base de datos, y verificacion de que los modelos estan correctamente cargados en memoria con los pesos esperados. Garantiza que un servicio reportado como "saludable" realmente pueda procesar solicitudes de verificacion.

## When to use

Utilizar esta skill cuando el health_monitor_agent necesite validar que los microservicios del pipeline KYC no solo estan conectados a sus dependencias, sino que realmente pueden ejecutar sus funciones principales. Es especialmente importante despues de despliegues, reinicios de pods, o cuando se detectan errores intermitentes que los health checks superficiales no capturan.

## Instructions

1. Crear un modulo `deep_check.py` con una clase base para checks profundos en cada microservicio:
```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
import time

@dataclass
class DeepCheckResult:
    component: str
    healthy: bool
    latency_ms: float
    details: Optional[str] = None
    error: Optional[str] = None

class DeepHealthCheck(ABC):
    @abstractmethod
    async def execute(self) -> DeepCheckResult:
        pass
```

2. Implementar el deep check para el modulo de face matching que ejecuta una inferencia dummy con una imagen de prueba:
```python
class FaceModelDeepCheck(DeepHealthCheck):
    def __init__(self, model_service):
        self.model = model_service

    async def execute(self) -> DeepCheckResult:
        start = time.monotonic()
        try:
            dummy_image = np.random.randint(0, 255, (112, 112, 3), dtype=np.uint8)
            embedding = self.model.get_embedding(dummy_image)
            assert embedding.shape == (512,), "Embedding dimension mismatch"
            latency = (time.monotonic() - start) * 1000
            return DeepCheckResult("face_model_arcface", True, latency)
        except Exception as e:
            latency = (time.monotonic() - start) * 1000
            return DeepCheckResult("face_model_arcface", False, latency, error=str(e))
```

3. Implementar el deep check para OCR que ejecuta una extraccion sobre una imagen de texto conocido:
```python
class OCRDeepCheck(DeepHealthCheck):
    EXPECTED_TEXT = "SPECIMEN"

    async def execute(self) -> DeepCheckResult:
        start = time.monotonic()
        try:
            test_image = load_test_specimen_image()
            result = await self.ocr_service.extract_text(test_image)
            assert self.EXPECTED_TEXT in result.upper()
            latency = (time.monotonic() - start) * 1000
            return DeepCheckResult("ocr_engine", True, latency)
        except Exception as e:
            latency = (time.monotonic() - start) * 1000
            return DeepCheckResult("ocr_engine", False, latency, error=str(e))
```

4. Implementar deep check para la base de datos que ejecuta una query funcional (no solo SELECT 1):
```python
class DatabaseDeepCheck(DeepHealthCheck):
    async def execute(self) -> DeepCheckResult:
        start = time.monotonic()
        try:
            row = await db.fetchone(
                "SELECT COUNT(*) FROM verification_sessions WHERE created_at > NOW() - INTERVAL '1 hour'"
            )
            latency = (time.monotonic() - start) * 1000
            return DeepCheckResult("postgresql", True, latency,
                                   details=f"sessions_last_hour={row[0]}")
        except Exception as e:
            latency = (time.monotonic() - start) * 1000
            return DeepCheckResult("postgresql", False, latency, error=str(e))
```

5. Implementar deep check para el modelo de liveness que verifica la clasificacion sobre una imagen de referencia:
```python
class LivenessModelDeepCheck(DeepHealthCheck):
    async def execute(self) -> DeepCheckResult:
        start = time.monotonic()
        try:
            test_face = load_reference_live_face()
            score = self.liveness_model.predict(test_face)
            assert 0.0 <= score <= 1.0, "Score out of range"
            latency = (time.monotonic() - start) * 1000
            return DeepCheckResult("liveness_model", True, latency,
                                   details=f"reference_score={score:.3f}")
        except Exception as e:
            latency = (time.monotonic() - start) * 1000
            return DeepCheckResult("liveness_model", False, latency, error=str(e))
```

6. Crear un endpoint `/health/deep` que ejecute todos los checks profundos del microservicio en paralelo:
```python
@health_router.get("/health/deep")
async def deep_health():
    checks = [FaceModelDeepCheck(model_svc), DatabaseDeepCheck(), RedisDeepCheck()]
    results = await asyncio.gather(*[c.execute() for c in checks])
    all_healthy = all(r.healthy for r in results)
    return {
        "status": "healthy" if all_healthy else "unhealthy",
        "checks": [asdict(r) for r in results],
        "total_latency_ms": sum(r.latency_ms for r in results),
    }
```

7. Configurar ejecucion periodica de deep checks cada 60 segundos en background y almacenar los resultados en Redis para consultas rapidas:
```python
async def periodic_deep_check(interval: int = 60):
    while True:
        results = await run_all_deep_checks()
        await redis.set("deep_health_cache", json.dumps(results), ex=interval * 2)
        if not results["healthy"]:
            logger.warning(f"Deep health check failed: {results}")
        await asyncio.sleep(interval)
```

8. Proteger el endpoint `/health/deep` con rate limiting ya que las inferencias dummy consumen recursos GPU/CPU:
```python
@health_router.get("/health/deep")
@rate_limit(max_calls=6, period=60)
async def deep_health():
    cached = await redis.get("deep_health_cache")
    if cached:
        return json.loads(cached)
    return await run_all_deep_checks()
```

## Notes

- Los deep checks consumen recursos reales (GPU para inferencia, CPU para OCR), por lo que no deben ejecutarse con demasiada frecuencia; un intervalo de 60 segundos es recomendable y nunca menos de 30 segundos.
- Incluir imagenes de referencia (specimen) como fixtures del proyecto para los checks de OCR y liveness; estas imagenes deben ser ligeras y no contener datos biometricos reales.
- Los deep checks deben tener un timeout global de 10 segundos; si un componente no responde en ese tiempo, marcarlo como unhealthy sin bloquear el resto de las verificaciones.
