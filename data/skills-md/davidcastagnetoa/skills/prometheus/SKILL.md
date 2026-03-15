---
name: prometheus
description: Prometheus como sistema de métricas time-series para monitorizar el pipeline KYC con scraping, almacenamiento y PromQL.
type: Tool
priority: Esencial
mode: Self-hosted
---

# prometheus

Despliega y configura Prometheus como sistema de métricas time-series para el pipeline de verificación de identidad. Gestiona el scraping de métricas desde todos los servicios KYC, el almacenamiento local de series temporales y las consultas PromQL para análisis de rendimiento. Este skill se centra exclusivamente en Prometheus como backend de métricas, separado de la visualización con Grafana.

## When to use

Usar este skill cuando el observability_agent necesite configurar Prometheus para recolectar y almacenar métricas del pipeline KYC, definir reglas de alertas basadas en PromQL, o ajustar la configuración de scraping y retención.

## Instructions

1. Desplegar Prometheus con Docker y configuración base para el pipeline KYC:
   ```yaml
   # docker-compose.yml
   prometheus:
     image: prom/prometheus:v2.48.0
     ports:
       - "9090:9090"
     volumes:
       - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
       - ./prometheus/rules/:/etc/prometheus/rules/
       - prometheus_data:/prometheus
     command:
       - '--config.file=/etc/prometheus/prometheus.yml'
       - '--storage.tsdb.path=/prometheus'
       - '--storage.tsdb.retention.time=30d'
       - '--web.enable-lifecycle'
   ```

2. Configurar los scrape targets para todos los microservicios del pipeline KYC:
   ```yaml
   # prometheus/prometheus.yml
   global:
     scrape_interval: 15s
     evaluation_interval: 15s

   rule_files:
     - "rules/*.yml"

   scrape_configs:
     - job_name: 'kyc-liveness'
       static_configs:
         - targets: ['liveness:8000']
       metrics_path: '/metrics'

     - job_name: 'kyc-ocr'
       static_configs:
         - targets: ['ocr:8000']

     - job_name: 'kyc-face-match'
       static_configs:
         - targets: ['face-match:8000']

     - job_name: 'kyc-antifraud'
       static_configs:
         - targets: ['antifraud:8000']

     - job_name: 'kyc-decision'
       static_configs:
         - targets: ['decision:8000']

     - job_name: 'kyc-api-gateway'
       static_configs:
         - targets: ['api-gateway:8000']
   ```

3. Instrumentar los servicios FastAPI del pipeline KYC con prometheus_client:
   ```python
   from prometheus_client import Counter, Histogram, Gauge, generate_latest
   from fastapi import FastAPI, Response

   app = FastAPI()

   VERIFICATION_REQUESTS = Counter(
       "kyc_verification_requests_total",
       "Total de solicitudes de verificación",
       ["module", "status"]
   )
   VERIFICATION_DURATION = Histogram(
       "kyc_verification_duration_seconds",
       "Duración de la verificación por módulo",
       ["module"],
       buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 8.0, 10.0]
   )
   CONFIDENCE_SCORE = Histogram(
       "kyc_confidence_score",
       "Distribución de scores de confianza",
       ["module"],
       buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 1.0]
   )
   ACTIVE_SESSIONS = Gauge(
       "kyc_active_sessions",
       "Sesiones de verificación activas"
   )

   @app.get("/metrics")
   async def metrics():
       return Response(generate_latest(), media_type="text/plain")
   ```

4. Definir reglas de recording para pre-calcular métricas agregadas del pipeline:
   ```yaml
   # prometheus/rules/kyc-recording.yml
   groups:
     - name: kyc_recording_rules
       rules:
         - record: kyc:verification_success_rate:5m
           expr: rate(kyc_verification_requests_total{status="success"}[5m]) / rate(kyc_verification_requests_total[5m])

         - record: kyc:p99_duration:5m
           expr: histogram_quantile(0.99, rate(kyc_verification_duration_seconds_bucket[5m]))

         - record: kyc:spoofing_detection_rate:1h
           expr: rate(kyc_verification_requests_total{module="liveness", status="rejected_spoofing"}[1h])
   ```

5. Configurar alerting rules para los SLOs del pipeline KYC:
   ```yaml
   # prometheus/rules/kyc-alerts.yml
   groups:
     - name: kyc_alerts
       rules:
         - alert: HighFalseAcceptanceRate
           expr: kyc:verification_success_rate:5m{module="face_match"} > 0.999
           for: 10m
           labels:
             severity: critical
           annotations:
             summary: "FAR potencialmente alto - el face_match acepta demasiadas verificaciones"

         - alert: VerificationLatencyHigh
           expr: kyc:p99_duration:5m > 8
           for: 5m
           labels:
             severity: warning
           annotations:
             summary: "Latencia p99 de verificación supera los 8 segundos (SLO)"

         - alert: LivenessServiceDown
           expr: up{job="kyc-liveness"} == 0
           for: 1m
           labels:
             severity: critical
           annotations:
             summary: "El servicio de liveness detection no está respondiendo"
   ```

6. En Kubernetes, usar ServiceMonitor para descubrimiento automático de targets:
   ```yaml
   apiVersion: monitoring.coreos.com/v1
   kind: ServiceMonitor
   metadata:
     name: kyc-pipeline-monitor
     labels:
       release: prometheus
   spec:
     selector:
       matchLabels:
         pipeline: kyc
     endpoints:
       - port: http
         path: /metrics
         interval: 15s
   ```

7. Verificar que Prometheus está scrapeando correctamente todos los targets:
   ```bash
   # Verificar targets activos
   curl -s http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | {job: .labels.job, health: .health}'

   # Ejecutar una query PromQL de prueba
   curl -s "http://localhost:9090/api/v1/query?query=up{job=~'kyc-.*'}" | jq .
   ```

## Notes

- El intervalo de scrape de 15 segundos es adecuado para el pipeline KYC; reducirlo aumenta la carga en Prometheus y en los servicios, sin beneficio significativo para las métricas de verificación.
- Los buckets del histograma de duración deben alinearse con el SLO de 8 segundos del pipeline; incluir buckets en 5s y 8s permite medir con precisión el cumplimiento.
- Configurar retención de 30 días para métricas operacionales; para análisis histórico a largo plazo, considerar Thanos o Cortex como almacenamiento remoto.
