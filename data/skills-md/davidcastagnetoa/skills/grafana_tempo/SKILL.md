---
name: grafana_tempo
description: Backend de trazas distribuidas para visualizar el flujo completo de verificacion KYC
type: Tool
priority: Recomendada
mode: Self-hosted
---

# grafana_tempo

Grafana Tempo como backend de trazas distribuidas para almacenar y consultar trazas completas de las sesiones de verificacion KYC. Permite visualizar el flujo de una solicitud a traves de todos los microservicios del pipeline (liveness, OCR, face_match, doc_processing, antifraud, decision) e identificar cuellos de botella y errores en cada etapa.

## When to use

Usa esta skill cuando necesites desplegar o configurar Grafana Tempo para almacenar trazas distribuidas del pipeline de verificacion KYC. Pertenece al **observability_agent** y se aplica cuando hay que analizar el recorrido completo de una sesion de verificacion, diagnosticar latencias entre microservicios o correlacionar trazas con metricas y logs.

## Instructions

1. Desplegar Grafana Tempo en el cluster con almacenamiento en MinIO:
   ```yaml
   # docker-compose.tempo.yml
   services:
     tempo:
       image: grafana/tempo:2.5.0
       ports:
         - "3200:3200"    # Tempo API
         - "4317:4317"    # OTLP gRPC
         - "4318:4318"    # OTLP HTTP
       volumes:
         - ./tempo/tempo.yml:/etc/tempo/tempo.yml
         - tempo-data:/var/tempo
       command:
         - '-config.file=/etc/tempo/tempo.yml'
   ```

2. Configurar Tempo con el backend de almacenamiento y limites apropiados:
   ```yaml
   # tempo.yml
   server:
     http_listen_port: 3200

   distributor:
     receivers:
       otlp:
         protocols:
           grpc:
             endpoint: 0.0.0.0:4317
           http:
             endpoint: 0.0.0.0:4318

   storage:
     trace:
       backend: s3
       s3:
         bucket: tempo-traces
         endpoint: minio.storage:9000
         access_key: ${MINIO_ACCESS_KEY}
         secret_key: ${MINIO_SECRET_KEY}
         insecure: true
       wal:
         path: /var/tempo/wal
       block:
         bloom_filter_false_positive: 0.05
       pool:
         max_workers: 100
         queue_depth: 10000

   compactor:
     compaction:
       block_retention: 72h

   metrics_generator:
     registry:
       external_labels:
         source: tempo
     storage:
       path: /var/tempo/generator/wal
       remote_write:
         - url: http://prometheus:9090/api/v1/write
   ```

3. Instrumentar los microservicios del pipeline KYC con OpenTelemetry:
   ```python
   from opentelemetry import trace
   from opentelemetry.sdk.trace import TracerProvider
   from opentelemetry.sdk.trace.export import BatchSpanProcessor
   from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
   from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

   provider = TracerProvider()
   processor = BatchSpanProcessor(
       OTLPSpanExporter(endpoint="tempo:4317", insecure=True)
   )
   provider.add_span_processor(processor)
   trace.set_tracer_provider(provider)

   FastAPIInstrumentor.instrument_app(app)
   ```

4. Crear spans personalizados para cada etapa del pipeline de verificacion:
   ```python
   tracer = trace.get_tracer("kyc-pipeline")

   async def verify_identity(session_id: str):
       with tracer.start_as_current_span("kyc.verification",
           attributes={"session.id": session_id}) as root_span:

           with tracer.start_as_current_span("kyc.liveness_check"):
               liveness_result = await liveness_module.check(session_id)
               trace.get_current_span().set_attribute("liveness.score", liveness_result.score)

           with tracer.start_as_current_span("kyc.document_processing"):
               doc_result = await doc_module.process(session_id)

           with tracer.start_as_current_span("kyc.face_match"):
               match_result = await face_match.compare(session_id)
               trace.get_current_span().set_attribute("face_match.similarity", match_result.score)

           with tracer.start_as_current_span("kyc.antifraud_analysis"):
               fraud_result = await antifraud.analyze(session_id)

           with tracer.start_as_current_span("kyc.decision"):
               decision = await decision_engine.evaluate(session_id)
               root_span.set_attribute("verification.result", decision.status)
   ```

5. Configurar Grafana para usar Tempo como datasource de trazas:
   ```yaml
   datasources:
     - name: Tempo
       type: tempo
       url: http://tempo:3200
       access: proxy
       jsonData:
         tracesToMetrics:
           datasourceUid: prometheus
           tags:
             - key: "service.name"
               value: "module"
         tracesToLogs:
           datasourceUid: loki
           filterByTraceID: true
           tags:
             - key: "session.id"
         serviceMap:
           datasourceUid: prometheus
   ```

6. Habilitar el generador de metricas de Tempo para obtener RED metrics automaticas:
   ```yaml
   metrics_generator:
     processor:
       service_graphs:
         dimensions:
           - session.status
       span_metrics:
         dimensions:
           - session.status
           - verification.result
   ```

7. Crear queries de ejemplo en Grafana para buscar trazas del pipeline KYC:
   ```
   # TraceQL: buscar verificaciones rechazadas con latencia alta
   { span.verification.result = "rejected" && duration > 5s }

   # TraceQL: buscar sesiones con score de liveness bajo
   { span.liveness.score < 0.5 && name = "kyc.liveness_check" }

   # TraceQL: buscar errores en face_match
   { name = "kyc.face_match" && status = error }
   ```

## Notes

- Configurar la retencion de trazas (block_retention) en funcion del tiempo maximo de resolucion de incidencias; 72 horas es un punto de partida razonable para el pipeline KYC.
- La integracion traces-to-logs y traces-to-metrics en Grafana permite navegar directamente desde una traza lenta a los logs y metricas correspondientes de esa sesion de verificacion, acelerando el diagnostico.
- No almacenar datos biometricos (embeddings, imagenes) como atributos de span; usar solo identificadores de sesion y scores numericos para cumplir con las politicas de privacidad GDPR del sistema.
