---
name: tenacity
description: Retry con backoff exponencial y circuit breaker para llamadas entre microservicios KYC
type: Library
priority: Esencial
mode: Self-hosted
---

# tenacity

Skill para implementar patrones de resiliencia en las comunicaciones entre microservicios del pipeline de verificacion de identidad usando la libreria Tenacity de Python. Cubre reintentos con backoff exponencial, jitter aleatorio y circuit breaker para manejar fallos transitorios sin saturar servicios degradados. Especialmente critico para las llamadas entre el orquestador y los servicios de inferencia ML (liveness, face matching, OCR) que pueden experimentar picos de latencia.

## When to use

Utilizar esta skill cuando el health_monitor_agent necesite configurar o mejorar la resiliencia de las llamadas HTTP/gRPC entre los microservicios del pipeline KYC. Aplica especialmente cuando se detectan fallos transitorios frecuentes, timeouts en servicios de inferencia ML, o cuando se requiere implementar circuit breaker para evitar cascadas de fallos.

## Instructions

1. Instalar la libreria tenacity y agregarla a los requirements del proyecto:

```bash
pip install tenacity
```

```python
# requirements.txt
tenacity>=8.2.0
```

2. Configurar el decorador de retry basico con backoff exponencial y jitter para llamadas entre microservicios:

```python
from tenacity import (
    retry, stop_after_attempt, wait_exponential_jitter,
    retry_if_exception_type, before_sleep_log
)
import logging

logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential_jitter(initial=0.5, max=10, jitter=2),
    retry=retry_if_exception_type((ConnectionError, TimeoutError, httpx.HTTPStatusError)),
    before_sleep=before_sleep_log(logger, logging.WARNING),
)
async def call_face_match_service(selfie_data: bytes, doc_face_data: bytes) -> dict:
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(
            f"{FACE_MATCH_URL}/api/v1/compare",
            files={"selfie": selfie_data, "document_face": doc_face_data},
        )
        response.raise_for_status()
        return response.json()
```

3. Implementar un circuit breaker usando tenacity para proteger servicios de inferencia ML sobrecargados:

```python
from tenacity import retry, stop_after_attempt, wait_fixed, CircuitBreaker

face_match_breaker = CircuitBreaker(
    fail_max=5,
    reset_timeout=30,
)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential_jitter(initial=1, max=15),
    retry=retry_if_exception_type((ConnectionError, TimeoutError)),
)
async def call_with_circuit_breaker(service_url: str, payload: dict) -> dict:
    if face_match_breaker.current_state == "open":
        raise ServiceUnavailableError(f"Circuit breaker open for {service_url}")
    try:
        result = await make_request(service_url, payload)
        face_match_breaker.success()
        return result
    except Exception as e:
        face_match_breaker.failure()
        raise
```

4. Crear configuraciones de retry diferenciadas por tipo de servicio del pipeline KYC:

```python
# Servicios ML (GPU-bound): mas reintentos, waits mas largos
ML_RETRY_CONFIG = {
    "stop": stop_after_attempt(4),
    "wait": wait_exponential_jitter(initial=1.0, max=20, jitter=3),
    "retry": retry_if_exception_type((ConnectionError, TimeoutError)),
}

# Servicios ligeros (Redis, DB): menos reintentos, waits cortos
FAST_RETRY_CONFIG = {
    "stop": stop_after_attempt(2),
    "wait": wait_exponential_jitter(initial=0.2, max=2, jitter=0.5),
    "retry": retry_if_exception_type((ConnectionError, TimeoutError)),
}

# OCR (CPU-bound): reintentos moderados
OCR_RETRY_CONFIG = {
    "stop": stop_after_attempt(3),
    "wait": wait_exponential_jitter(initial=0.5, max=10, jitter=1),
    "retry": retry_if_exception_type((ConnectionError, TimeoutError)),
}
```

5. Implementar callbacks para registrar metricas de reintentos en Prometheus:

```python
from tenacity import after_log, before_sleep_log
from prometheus_client import Counter, Histogram

retry_counter = Counter("kyc_retry_total", "Total retries", ["service", "attempt"])
retry_latency = Histogram("kyc_retry_duration_seconds", "Retry duration", ["service"])

def on_retry(retry_state):
    service = retry_state.fn.__name__
    retry_counter.labels(service=service, attempt=str(retry_state.attempt_number)).inc()

@retry(
    **ML_RETRY_CONFIG,
    after=on_retry,
)
async def call_liveness_service(frames: list[bytes]) -> dict:
    return await make_request(LIVENESS_URL, {"frames": frames})
```

6. Configurar excepciones especificas que NO deben reintentar (errores de negocio vs errores transitorios):

```python
from tenacity import retry_if_not_exception_type

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential_jitter(initial=0.5, max=10),
    retry=(
        retry_if_exception_type((ConnectionError, TimeoutError))
        & retry_if_not_exception_type(ValidationError)
    ),
)
async def call_ocr_service(document_image: bytes) -> dict:
    # ValidationError (documento ilegible) no debe reintentar
    # ConnectionError/TimeoutError si deben reintentar
    result = await make_request(OCR_URL, {"image": document_image})
    if result.get("error_type") == "validation":
        raise ValidationError(result["message"])
    return result
```

7. Implementar un wrapper reutilizable con circuit breaker integrado para todos los servicios del pipeline:

```python
class ResilientServiceClient:
    def __init__(self, service_name: str, base_url: str, retry_config: dict):
        self.service_name = service_name
        self.base_url = base_url
        self.retry_config = retry_config
        self.breaker = CircuitBreaker(fail_max=5, reset_timeout=30)

    @retry(**ML_RETRY_CONFIG)
    async def call(self, endpoint: str, payload: dict) -> dict:
        if self.breaker.current_state == "open":
            raise CircuitOpenError(self.service_name)
        try:
            result = await httpx.AsyncClient().post(
                f"{self.base_url}{endpoint}", json=payload, timeout=15.0
            )
            self.breaker.success()
            return result.json()
        except Exception as e:
            self.breaker.failure()
            raise

face_client = ResilientServiceClient("face_match", FACE_MATCH_URL, ML_RETRY_CONFIG)
ocr_client = ResilientServiceClient("ocr", OCR_URL, OCR_RETRY_CONFIG)
```

## Notes

- Nunca reintentar errores de validacion o errores 4xx del negocio (documento invalido, rostro no detectado); solo reintentar errores de infraestructura (5xx, timeouts, connection refused) para evitar trabajo redundante y latencia innecesaria.
- El tiempo total de reintentos para una verificacion KYC completa no debe superar los 8 segundos segun los SLOs del sistema; configurar los timeouts y max_attempts en consecuencia.
- Monitorizar la tasa de reintentos como metrica clave; un aumento sostenido indica degradacion del servicio destino y debe disparar alertas del health_monitor_agent antes de que el circuit breaker se abra.
