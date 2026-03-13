---
name: opentelemetry_sdk
description: SDK de OpenTelemetry para instrumentación unificada de métricas, trazas y logs del pipeline KYC en Python.
type: Library
priority: Esencial
mode: Self-hosted
---

# opentelemetry_sdk

Implementa el SDK de OpenTelemetry en el código Python del pipeline de verificación de identidad para instrumentación unificada de métricas, trazas y logs. Proporciona una API estándar y vendor-neutral que permite enviar telemetría a múltiples backends (Prometheus, Jaeger, Loki) sin acoplamiento directo. Este skill se centra en la instrumentación del código, separada del backend de trazas Jaeger.

## When to use

Usar este skill cuando el observability_agent necesite instrumentar los servicios Python del pipeline KYC con OpenTelemetry, configurar exporters, o añadir spans y métricas personalizadas al código de verificación.

## Instructions

1. Instalar las dependencias de OpenTelemetry necesarias para el pipeline KYC:

   ```bash
   pip install opentelemetry-api \
     opentelemetry-sdk \
     opentelemetry-instrumentation-fastapi \
     opentelemetry-instrumentation-httpx \
     opentelemetry-instrumentation-logging \
     opentelemetry-exporter-otlp-proto-grpc \
     opentelemetry-exporter-prometheus
   ```

2. Configurar el proveedor de trazas con exportador OTLP para enviar spans al collector:

   ```python
   from opentelemetry import trace
   from opentelemetry.sdk.trace import TracerProvider
   from opentelemetry.sdk.trace.export import BatchSpanProcessor
   from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
   from opentelemetry.sdk.resources import Resource

   resource = Resource.create({
       "service.name": "kyc-face-match",
       "service.version": "1.0.0",
       "deployment.environment": "production",
       "service.namespace": "kyc-pipeline"
   })

   tracer_provider = TracerProvider(resource=resource)
   otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True)
   tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
   trace.set_tracer_provider(tracer_provider)
   ```

3. Configurar el proveedor de métricas con exportador Prometheus:

   ```python
   from opentelemetry import metrics
   from opentelemetry.sdk.metrics import MeterProvider
   from opentelemetry.exporter.prometheus import PrometheusMetricReader

   prometheus_reader = PrometheusMetricReader()
   meter_provider = MeterProvider(resource=resource, metric_readers=[prometheus_reader])
   metrics.set_meter_provider(meter_provider)

   meter = metrics.get_meter("kyc-pipeline")
   verification_counter = meter.create_counter(
       "kyc.verifications.total",
       description="Total de verificaciones procesadas"
   )
   verification_duration = meter.create_histogram(
       "kyc.verification.duration",
       unit="s",
       description="Duración de la verificación"
   )
   ```

4. Instrumentar automáticamente FastAPI y las llamadas HTTP entre servicios:

   ```python
   from fastapi import FastAPI
   from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
   from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

   app = FastAPI(title="KYC Face Match Service")
   FastAPIInstrumentor.instrument_app(app)
   HTTPXClientInstrumentor().instrument()
   ```

5. Añadir spans personalizados para operaciones críticas del pipeline KYC:

   ```python
   from opentelemetry import trace

   tracer = trace.get_tracer("kyc.face_match")

   async def compare_faces(selfie_embedding, document_embedding):
       with tracer.start_as_current_span("face_comparison") as span:
           span.set_attribute("kyc.module", "face_match")
           span.set_attribute("kyc.embedding_dimension", len(selfie_embedding))

           similarity = cosine_similarity(selfie_embedding, document_embedding)

           span.set_attribute("kyc.confidence_score", similarity)
           span.set_attribute("kyc.threshold", 0.85)
           span.set_attribute("kyc.decision", "match" if similarity > 0.85 else "no_match")

           if similarity < 0.85:
               span.set_status(trace.Status(trace.StatusCode.OK))
               span.add_event("face_mismatch_detected", {
                   "similarity": similarity,
                   "threshold": 0.85
               })

           return similarity
   ```

6. Configurar la propagación de contexto para mantener las trazas entre servicios:

   ```python
   from opentelemetry.propagate import set_global_textmap
   from opentelemetry.propagators.composite import CompositePropagator
   from opentelemetry.propagators.b3 import B3MultiFormat
   from opentelemetry.trace.propagation import TraceContextTextMapPropagator

   set_global_textmap(CompositePropagator([
       TraceContextTextMapPropagator(),
       B3MultiFormat()
   ]))
   ```

7. Integrar OpenTelemetry con el logging existente para correlación automática:

   ```python
   from opentelemetry.instrumentation.logging import LoggingInstrumentor
   import logging

   LoggingInstrumentor().instrument(set_logging_format=True)

   logging.basicConfig(
       format="%(asctime)s %(levelname)s [%(name)s] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s] %(message)s",
       level=logging.INFO
   )
   logger = logging.getLogger("kyc-pipeline")
   ```

8. Crear un módulo de inicialización reutilizable para todos los servicios del pipeline:

   ```python
   # shared/telemetry.py
   def init_telemetry(service_name: str, otlp_endpoint: str = "http://otel-collector:4317"):
       """Inicializa OpenTelemetry para un servicio del pipeline KYC."""
       resource = Resource.create({"service.name": service_name, "service.namespace": "kyc-pipeline"})

       # Traces
       tracer_provider = TracerProvider(resource=resource)
       tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)))
       trace.set_tracer_provider(tracer_provider)

       # Metrics
       prometheus_reader = PrometheusMetricReader()
       meter_provider = MeterProvider(resource=resource, metric_readers=[prometheus_reader])
       metrics.set_meter_provider(meter_provider)

       # Logging
       LoggingInstrumentor().instrument(set_logging_format=True)

       return trace.get_tracer(service_name), metrics.get_meter(service_name)
   ```

## Notes

- Usar la auto-instrumentación de FastAPI y httpx reduce significativamente el código manual necesario; los spans de HTTP requests/responses se generan automáticamente con latencias, status codes y headers relevantes.
- Los atributos de span personalizados (kyc.confidence_score, kyc.module, kyc.decision) son esenciales para poder filtrar y analizar trazas específicas del pipeline de verificación en Jaeger o Grafana Tempo.
- Nunca incluir datos biométricos (embeddings, imágenes) como atributos de span; limitar los atributos a metadatos operacionales (scores, decisiones, duraciones) para cumplir con GDPR/LOPD.
