---
name: trace_id_propagation
description: Propagación de trace IDs a través de microservicios del pipeline KYC para correlación de logs y métricas.
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# trace_id_propagation

Este skill implementa la propagación de identificadores de traza (X-Request-ID y traceparent W3C) a través de todos los microservicios del pipeline de verificación de identidad KYC. Permite correlacionar logs, métricas y spans de una sesión de verificación completa, desde la captura de selfie hasta la decisión final. Es fundamental para depuración y observabilidad en un sistema distribuido con módulos de liveness, OCR, face match y antifraude.

## When to use

Usar este skill cuando el **api_gateway_agent** necesite configurar o verificar la propagación de trace IDs entre los microservicios del pipeline KYC, garantizando que cada request de verificación pueda rastrearse de extremo a extremo.

## Instructions

1. Configurar el middleware del API Gateway para generar un `X-Request-ID` único (UUID v4) si el cliente no lo envía, y propagar el header `traceparent` según el estándar W3C Trace Context:

```python
import uuid
from starlette.middleware.base import BaseHTTPMiddleware

class TraceIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        traceparent = request.headers.get("traceparent", self._generate_traceparent())
        request.state.request_id = request_id
        request.state.traceparent = traceparent
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        response.headers["traceparent"] = traceparent
        return response
```

2. Inyectar los trace IDs en cada llamada interna a los microservicios de verificación (liveness, OCR, face_match, doc_processing, antifraud, decision):

```python
async def call_service(service_url: str, payload: dict, request_id: str, traceparent: str):
    headers = {
        "X-Request-ID": request_id,
        "traceparent": traceparent,
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient() as client:
        return await client.post(service_url, json=payload, headers=headers)
```

3. Configurar el logger estructurado en cada microservicio para incluir el `request_id` y `trace_id` en cada línea de log:

```python
import structlog

logger = structlog.get_logger()

def configure_logging(request_id: str, trace_id: str):
    return logger.bind(request_id=request_id, trace_id=trace_id)
```

4. Implementar la generación del header `traceparent` conforme al estándar W3C Trace Context (version-trace_id-parent_id-trace_flags):

```python
def _generate_traceparent(self) -> str:
    trace_id = uuid.uuid4().hex
    parent_id = uuid.uuid4().hex[:16]
    return f"00-{trace_id}-{parent_id}-01"
```

5. Agregar el `request_id` y `session_id` de verificación KYC en la respuesta estructurada del motor de decisión para trazabilidad completa:

```python
response = {
    "status": "VERIFIED",
    "confidence_score": 0.92,
    "request_id": request_id,
    "session_id": session_id,
    "traceparent": traceparent,
    "reasons": [],
    "timestamp": datetime.utcnow().isoformat(),
}
```

6. Configurar la propagación de contexto en los exportadores de OpenTelemetry para que los spans de cada microservicio se vinculen automáticamente:

```python
from opentelemetry import trace
from opentelemetry.propagate import inject, extract

def propagate_context(headers: dict):
    ctx = extract(headers)
    tracer = trace.get_tracer("kyc-gateway")
    with tracer.start_as_current_span("verification_pipeline", context=ctx):
        inject(headers)
```

7. Validar que el formato del `traceparent` recibido sea correcto antes de propagarlo, descartando valores malformados y generando uno nuevo si es necesario.

## Notes

- El `X-Request-ID` debe mantenerse inmutable durante toda la sesión de verificación, incluso si el pipeline pasa por múltiples microservicios (liveness, OCR, face_match, antifraud, decision).
- Todos los logs de auditoría deben incluir el trace ID para cumplir con los requisitos de trazabilidad y anonimización descritos en las consideraciones de seguridad del sistema.
- En entornos con Kubernetes, asegurarse de que los sidecars de service mesh (Istio, Linkerd) no sobrescriban los headers de traza propagados por el gateway.
