---
name: w3c_trace_context
description: Estandar W3C Trace Context para propagacion de trazas entre microservicios KYC
type: Protocol
priority: Esencial
mode: Self-hosted
---

# w3c_trace_context

Implementacion del estandar W3C Trace Context (headers traceparent y tracestate) para la propagacion uniforme del contexto de trazas distribuidas entre todos los microservicios del pipeline de verificacion KYC. Garantiza que una sesion de verificacion pueda rastrearse de extremo a extremo, desde la captura de selfie hasta la decision final, independientemente del lenguaje o framework de cada servicio.

## When to use

Usa esta skill cuando necesites configurar o depurar la propagacion de contexto de trazas entre los microservicios del pipeline KYC. Pertenece al **observability_agent** y se aplica cuando hay que asegurar que el trace ID se transmite correctamente entre servicios, cuando se integran servicios nuevos al pipeline o cuando las trazas aparecen fragmentadas.

## Instructions

1. Configurar OpenTelemetry para usar el propagador W3C Trace Context en el backend FastAPI:
   ```python
   from opentelemetry import context
   from opentelemetry.propagators import set_global_textmap
   from opentelemetry.propagate import inject, extract
   from opentelemetry.propagators.composite import CompositePropagator
   from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
   from opentelemetry.baggage.propagation import W3CBaggagePropagator

   set_global_textmap(CompositePropagator([
       TraceContextTextMapPropagator(),
       W3CBaggagePropagator(),
   ]))
   ```

2. Entender la estructura del header traceparent segun el estandar W3C:
   ```
   traceparent: {version}-{trace-id}-{parent-id}-{trace-flags}
   Ejemplo:     00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01

   version:     00 (version actual)
   trace-id:    32 hex chars - identificador unico de la traza completa
   parent-id:   16 hex chars - identificador del span padre
   trace-flags: 01 = sampled, 00 = not sampled
   ```

3. Implementar middleware para extraer e inyectar el contexto en cada microservicio:
   ```python
   from opentelemetry.propagate import extract, inject
   from opentelemetry import trace
   from starlette.middleware.base import BaseHTTPMiddleware

   class TraceContextMiddleware(BaseHTTPMiddleware):
       async def dispatch(self, request, call_next):
           ctx = extract(carrier=dict(request.headers))
           with trace.get_tracer("kyc-service").start_as_current_span(
               f"{request.method} {request.url.path}",
               context=ctx
           ):
               response = await call_next(request)
               return response
   ```

4. Propagar el contexto en llamadas HTTP entre microservicios del pipeline:
   ```python
   import httpx
   from opentelemetry.propagate import inject

   async def call_face_match_service(session_id: str, images: dict):
       headers = {}
       inject(headers)  # Inyecta traceparent y tracestate en headers
       async with httpx.AsyncClient() as client:
           response = await client.post(
               "http://face-match-service:8000/api/v1/compare",
               json={"session_id": session_id, "images": images},
               headers=headers
           )
       return response.json()
   ```

5. Usar tracestate para agregar informacion especifica del pipeline KYC:
   ```python
   from opentelemetry.baggage import set_baggage, get_baggage

   # Al inicio de la verificacion, agregar contexto de negocio
   ctx = set_baggage("kyc.session_id", session_id)
   ctx = set_baggage("kyc.document_type", "passport", context=ctx)

   # En servicios downstream, recuperar el contexto
   session_id = get_baggage("kyc.session_id")
   ```

6. Configurar la propagacion en servicios que usan colas de mensajes (Redis):
   ```python
   from opentelemetry.propagate import inject, extract

   # Productor: inyectar contexto en el mensaje
   def enqueue_antifraud_check(session_id: str, data: dict):
       carrier = {}
       inject(carrier)
       message = {
           "session_id": session_id,
           "data": data,
           "trace_context": carrier
       }
       redis_client.lpush("antifraud_queue", json.dumps(message))

   # Consumidor: extraer contexto del mensaje
   def process_antifraud_check(message: dict):
       ctx = extract(carrier=message.get("trace_context", {}))
       with tracer.start_as_current_span("antifraud.process", context=ctx):
           # Procesar analisis antifraude
           pass
   ```

7. Validar que la propagacion funciona correctamente entre todos los servicios:
   ```python
   # Test de integracion para verificar propagacion
   async def test_trace_propagation():
       async with httpx.AsyncClient() as client:
           response = await client.post(
               "http://kyc-gateway:8000/api/v1/verify",
               json=test_payload,
               headers={"traceparent": "00-aaaabbbbccccddddeeeeffffaaaabbbb-1111222233334444-01"}
           )
           # Verificar que el trace_id aparece en los logs de todos los servicios
           assert response.headers.get("traceresponse") is not None
   ```

8. Documentar el flujo de propagacion del trace context a traves del pipeline:
   ```
   Cliente -> [traceparent] -> API Gateway
     -> [traceparent] -> Liveness Service
     -> [traceparent] -> Document Processing Service
     -> [traceparent] -> OCR Service
     -> [traceparent] -> Face Match Service
     -> [traceparent via Redis] -> Antifraud Service
     -> [traceparent] -> Decision Engine
   ```

## Notes

- Todos los microservicios del pipeline KYC deben usar el mismo propagador (W3C Trace Context) para evitar trazas fragmentadas; si se integra un servicio de terceros, verificar que soporte este estandar o implementar un bridge de propagacion.
- El trace ID debe incluirse en los logs estructurados de cada servicio para permitir la correlacion traces-to-logs en Grafana, vinculando logs de una sesion de verificacion con su traza completa.
- No incluir datos biometricos o PII en los campos de baggage ya que estos se propagan en texto claro en los headers HTTP; usar solo identificadores de sesion y metadatos operacionales.
