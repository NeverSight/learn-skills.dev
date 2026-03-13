---
name: log_correlation
description: Correlación de logs entre microservicios del pipeline KYC usando trace_id y session_id.
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# log_correlation

Implementa la correlación de logs entre los distintos microservicios del pipeline de verificación de identidad mediante identificadores compartidos como trace_id y session_id. Permite reconstruir el flujo completo de una sesión KYC desde la captura de selfie hasta la decisión final, facilitando el diagnóstico de fallos y la auditoría de verificaciones. Es fundamental para entender el comportamiento end-to-end del sistema distribuido.

## When to use

Usar este skill cuando el observability_agent necesite implementar o mejorar la trazabilidad entre servicios del pipeline KYC, permitiendo seguir una sesión de verificación a través de liveness, OCR, face_match, antifraud y decision.

## Instructions

1. Definir un middleware FastAPI que genere y propague el trace_id y session_id en cada request:
   ```python
   import uuid
   from starlette.middleware.base import BaseHTTPMiddleware
   from contextvars import ContextVar

   trace_id_var: ContextVar[str] = ContextVar("trace_id", default="")
   session_id_var: ContextVar[str] = ContextVar("session_id", default="")

   class CorrelationMiddleware(BaseHTTPMiddleware):
       async def dispatch(self, request, call_next):
           trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))
           session_id = request.headers.get("X-Session-ID", str(uuid.uuid4()))
           trace_id_var.set(trace_id)
           session_id_var.set(session_id)
           response = await call_next(request)
           response.headers["X-Trace-ID"] = trace_id
           response.headers["X-Session-ID"] = session_id
           return response
   ```

2. Configurar un logging filter que inyecte automáticamente los IDs de correlación en cada log:
   ```python
   import logging

   class CorrelationFilter(logging.Filter):
       def filter(self, record):
           record.trace_id = trace_id_var.get("")
           record.session_id = session_id_var.get("")
           return True

   logger = logging.getLogger("kyc-pipeline")
   logger.addFilter(CorrelationFilter())
   ```

3. Configurar el formato de log JSON para incluir los campos de correlación:
   ```python
   import json

   class JSONFormatter(logging.Formatter):
       def format(self, record):
           log_entry = {
               "timestamp": self.formatTime(record),
               "level": record.levelname,
               "service": record.name,
               "module": getattr(record, "module", "unknown"),
               "trace_id": getattr(record, "trace_id", ""),
               "session_id": getattr(record, "session_id", ""),
               "message": record.getMessage(),
           }
           return json.dumps(log_entry)
   ```

4. Propagar los IDs de correlación en las llamadas HTTP entre microservicios:
   ```python
   import httpx

   async def call_face_match(selfie_data: bytes, doc_face_data: bytes):
       headers = {
           "X-Trace-ID": trace_id_var.get(),
           "X-Session-ID": session_id_var.get(),
       }
       async with httpx.AsyncClient() as client:
           response = await client.post(
               "http://face-match:8000/compare",
               headers=headers,
               files={"selfie": selfie_data, "document": doc_face_data}
           )
       return response.json()
   ```

5. Crear queries de correlación en Loki/LogQL para reconstruir una sesión completa:
   ```logql
   {pipeline="kyc"} | json | session_id="sess-abc123" | line_format "{{.timestamp}} [{{.service}}] {{.message}}"
   ```

6. Crear queries equivalentes en Elasticsearch/Kibana:
   ```json
   {
     "query": {
       "bool": {
         "must": [
           { "term": { "session_id": "sess-abc123" } }
         ]
       }
     },
     "sort": [{ "timestamp": "asc" }]
   }
   ```

7. Implementar un endpoint de diagnóstico que devuelva el timeline de una sesión:
   ```python
   @app.get("/api/v1/sessions/{session_id}/timeline")
   async def get_session_timeline(session_id: str):
       logs = await query_loki(f'{{pipeline="kyc"}} | json | session_id="{session_id}"')
       return {
           "session_id": session_id,
           "steps": [parse_log_entry(log) for log in logs],
           "total_duration_ms": calculate_duration(logs)
       }
   ```

## Notes

- El trace_id y session_id deben propagarse consistentemente en TODOS los microservicios del pipeline; un solo servicio sin propagación rompe la cadena de correlación.
- En entornos con colas de mensajes (Redis, RabbitMQ), los IDs de correlación deben incluirse en los metadatos del mensaje para mantener la trazabilidad asíncrona.
- Los IDs de correlación son esenciales para cumplir requisitos de auditoría GDPR/LOPD, ya que permiten reconstruir exactamente qué procesamiento se aplicó a los datos de un usuario.
