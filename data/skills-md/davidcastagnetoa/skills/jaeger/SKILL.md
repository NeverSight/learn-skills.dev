---
name: jaeger
description: Jaeger como backend de trazas distribuidas para almacenar y visualizar spans del pipeline de verificación KYC.
type: Tool
priority: Esencial
mode: Self-hosted
---

# jaeger

Despliega y configura Jaeger como backend de trazas distribuidas para el pipeline de verificación de identidad. Almacena, indexa y visualiza los spans generados por los microservicios KYC, permitiendo analizar el flujo completo de una verificación desde la captura de selfie hasta la decisión final. Este skill se centra en Jaeger como infraestructura de trazas, separada de la instrumentación con OpenTelemetry SDK.

## When to use

Usar este skill cuando el observability_agent necesite desplegar o configurar Jaeger para recibir, almacenar y visualizar trazas distribuidas del pipeline KYC, o cuando se necesite optimizar el almacenamiento y la consulta de spans.

## Instructions

1. Desplegar Jaeger all-in-one para desarrollo o con componentes separados para producción:
   ```yaml
   # docker-compose.yml - Desarrollo
   jaeger:
     image: jaegertracing/all-in-one:1.52
     ports:
       - "16686:16686"   # UI
       - "4317:4317"     # OTLP gRPC
       - "4318:4318"     # OTLP HTTP
       - "14250:14250"   # gRPC collector
     environment:
       - COLLECTOR_OTLP_ENABLED=true
       - SPAN_STORAGE_TYPE=badger
       - BADGER_EPHEMERAL=false
       - BADGER_DIRECTORY_VALUE=/badger/data
       - BADGER_DIRECTORY_KEY=/badger/key
     volumes:
       - jaeger_data:/badger
   ```

2. Para producción, desplegar Jaeger con Elasticsearch como backend de almacenamiento:
   ```yaml
   # docker-compose-prod.yml
   jaeger-collector:
     image: jaegertracing/jaeger-collector:1.52
     environment:
       - SPAN_STORAGE_TYPE=elasticsearch
       - ES_SERVER_URLS=http://elasticsearch:9200
       - ES_USERNAME=elastic
       - ES_PASSWORD=${ELASTIC_PASSWORD}
       - ES_INDEX_PREFIX=jaeger-kyc
     ports:
       - "4317:4317"
       - "14250:14250"

   jaeger-query:
     image: jaegertracing/jaeger-query:1.52
     environment:
       - SPAN_STORAGE_TYPE=elasticsearch
       - ES_SERVER_URLS=http://elasticsearch:9200
       - ES_USERNAME=elastic
       - ES_PASSWORD=${ELASTIC_PASSWORD}
       - ES_INDEX_PREFIX=jaeger-kyc
     ports:
       - "16686:16686"
   ```

3. Configurar el OpenTelemetry Collector como intermediario entre los servicios KYC y Jaeger:
   ```yaml
   # otel-collector-config.yaml
   receivers:
     otlp:
       protocols:
         grpc:
           endpoint: 0.0.0.0:4317
         http:
           endpoint: 0.0.0.0:4318

   processors:
     batch:
       timeout: 5s
       send_batch_size: 1024
     attributes:
       actions:
         - key: kyc.pipeline
           value: "identity-verification"
           action: upsert

   exporters:
     jaeger:
       endpoint: jaeger-collector:14250
       tls:
         insecure: true

   service:
     pipelines:
       traces:
         receivers: [otlp]
         processors: [batch, attributes]
         exporters: [jaeger]
   ```

4. Configurar sampling adaptativo para controlar el volumen de trazas del pipeline KYC:
   ```json
   {
     "service_strategies": [
       {
         "service": "kyc-liveness",
         "type": "probabilistic",
         "param": 1.0
       },
       {
         "service": "kyc-face-match",
         "type": "probabilistic",
         "param": 1.0
       },
       {
         "service": "kyc-ocr",
         "type": "probabilistic",
         "param": 0.5
       }
     ],
     "default_strategy": {
       "type": "probabilistic",
       "param": 0.1
     }
   }
   ```

5. Configurar retención y limpieza de spans en Elasticsearch:
   ```bash
   # Crear ILM policy para spans de Jaeger
   curl -X PUT "http://elasticsearch:9200/_ilm/policy/jaeger-kyc-span-policy" \
     -H 'Content-Type: application/json' -d '{
     "policy": {
       "phases": {
         "hot": { "actions": { "rollover": { "max_age": "1d", "max_size": "5GB" } } },
         "delete": { "min_age": "14d", "actions": { "delete": {} } }
       }
     }
   }'

   # Ejecutar limpieza manual de spans antiguos
   jaeger-es-rollover init http://elasticsearch:9200
   jaeger-es-rollover rollover http://elasticsearch:9200
   ```

6. Configurar Jaeger como datasource en Grafana para correlación con métricas y logs:
   ```yaml
   # grafana/provisioning/datasources/jaeger.yml
   apiVersion: 1
   datasources:
     - name: Jaeger
       type: jaeger
       access: proxy
       url: http://jaeger-query:16686
       jsonData:
         tracesToLogsV2:
           datasourceUid: loki
           filterByTraceID: true
           filterBySpanID: true
         tracesToMetrics:
           datasourceUid: prometheus
           queries:
             - name: "Request duration"
               query: "kyc_verification_duration_seconds_bucket{$$__tags}"
   ```

7. Verificar que Jaeger está recibiendo trazas del pipeline KYC:
   ```bash
   # Verificar servicios registrados
   curl -s "http://localhost:16686/api/services" | jq .

   # Buscar trazas de un servicio específico
   curl -s "http://localhost:16686/api/traces?service=kyc-face-match&limit=5" | jq '.data[0].spans | length'

   # Buscar una traza por trace_id
   curl -s "http://localhost:16686/api/traces/{trace_id}" | jq '.data[0].spans[] | {operationName, duration}'
   ```

## Notes

- En producción, usar sampling rate de 1.0 (100%) para los módulos críticos de seguridad (liveness, face_match) para garantizar trazabilidad completa de decisiones; módulos menos críticos como OCR pueden usar sampling reducido.
- La retención de 14 días para spans es adecuada para debugging operacional; para requisitos de auditoría, los datos relevantes deben extraerse y almacenarse en el sistema de logs de auditoría con retención de 1 año.
- Jaeger UI permite visualizar el flujo completo de una verificación KYC como un trace waterfall, mostrando la latencia de cada módulo (liveness, OCR, face_match, antifraud, decision) y facilitando la identificación de cuellos de botella.
