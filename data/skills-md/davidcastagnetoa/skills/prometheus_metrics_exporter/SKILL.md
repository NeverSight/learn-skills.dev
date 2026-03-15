---
name: prometheus_metrics_exporter
description: Exportar métricas del API Gateway KYC al formato Prometheus para monitorización del pipeline de verificación.
type: Library
priority: Esencial
mode: Self-hosted
---

# prometheus_metrics_exporter

Este skill configura la exportación de métricas del API Gateway del sistema KYC en formato Prometheus. Recopila datos de latencia por endpoint, tasa de errores, requests por segundo y métricas específicas del pipeline de verificación de identidad (tiempos de liveness, OCR, face match). Permite construir dashboards y alertas para garantizar el cumplimiento de los objetivos de rendimiento del sistema (respuesta < 8s, disponibilidad > 99.9%).

## When to use

Usar este skill cuando el **api_gateway_agent** necesite implementar o ajustar la instrumentación de métricas Prometheus en el API Gateway, configurar endpoints de scraping, o definir métricas personalizadas para el pipeline de verificación KYC.

## Instructions

1. Instalar e integrar la librería `prometheus-fastapi-instrumentator` en la aplicación FastAPI del gateway para instrumentación automática de endpoints:

```python
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="KYC Verification Gateway")

Instrumentator().instrument(app).expose(app, endpoint="/metrics")
```

2. Definir métricas personalizadas para cada módulo del pipeline KYC usando los tipos de Prometheus (Histogram para latencias, Counter para operaciones, Gauge para estados):

```python
from prometheus_client import Histogram, Counter, Gauge

VERIFICATION_LATENCY = Histogram(
    "kyc_verification_duration_seconds",
    "Duración total del pipeline de verificación",
    buckets=[1.0, 2.0, 4.0, 6.0, 8.0, 10.0, 15.0],
)

MODULE_LATENCY = Histogram(
    "kyc_module_duration_seconds",
    "Duración por módulo del pipeline",
    ["module"],  # liveness, ocr, face_match, antifraud, decision
    buckets=[0.5, 1.0, 2.0, 4.0, 8.0],
)

VERIFICATION_TOTAL = Counter(
    "kyc_verifications_total",
    "Total de verificaciones procesadas",
    ["status"],  # VERIFIED, REJECTED, MANUAL_REVIEW
)

LIVENESS_FAILURES = Counter(
    "kyc_liveness_failures_total",
    "Intentos de spoofing detectados",
    ["attack_type"],  # photo, screen, mask, deepfake
)

ACTIVE_SESSIONS = Gauge(
    "kyc_active_sessions",
    "Sesiones de verificación activas",
)
```

3. Instrumentar cada llamada a los microservicios del pipeline para medir latencia y registrar errores:

```python
import time

async def call_module(module_name: str, service_url: str, payload: dict):
    ACTIVE_SESSIONS.inc()
    start = time.perf_counter()
    try:
        response = await http_client.post(service_url, json=payload)
        MODULE_LATENCY.labels(module=module_name).observe(time.perf_counter() - start)
        return response
    except Exception as e:
        VERIFICATION_TOTAL.labels(status="ERROR").inc()
        raise
    finally:
        ACTIVE_SESSIONS.dec()
```

4. Configurar el endpoint `/metrics` con autenticación básica para evitar exposición pública de datos operativos:

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

@app.get("/metrics")
async def metrics(credentials: HTTPBasicCredentials = Depends(security)):
    if not verify_metrics_credentials(credentials):
        raise HTTPException(status_code=401)
    return generate_latest()
```

5. Definir alertas de Prometheus basadas en los SLOs del sistema KYC (latencia < 8s, FAR < 0.1%, disponibilidad > 99.9%):

```yaml
groups:
  - name: kyc_alerts
    rules:
      - alert: HighVerificationLatency
        expr: histogram_quantile(0.95, kyc_verification_duration_seconds_bucket) > 8
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Latencia de verificación KYC supera 8 segundos (p95)"

      - alert: HighErrorRate
        expr: rate(kyc_verifications_total{status="ERROR"}[5m]) / rate(kyc_verifications_total[5m]) > 0.001
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Tasa de errores del pipeline KYC superior al 0.1%"

      - alert: SpoofingSpike
        expr: rate(kyc_liveness_failures_total[10m]) > 5
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Pico de intentos de spoofing detectado"
```

6. Configurar el `scrape_config` en Prometheus para recopilar métricas del gateway y de cada microservicio del pipeline:

```yaml
scrape_configs:
  - job_name: "kyc-gateway"
    scrape_interval: 15s
    metrics_path: "/metrics"
    basic_auth:
      username: "prometheus"
      password_file: "/etc/prometheus/gateway_password"
    static_configs:
      - targets: ["gateway:8000"]

  - job_name: "kyc-modules"
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        regex: "kyc-(liveness|ocr|face-match|antifraud|decision)"
        action: keep
```

7. Registrar métricas de rate limiting para monitorizar bloqueos por IP y detectar patrones de abuso:

```python
RATE_LIMIT_HITS = Counter(
    "kyc_rate_limit_hits_total",
    "Requests bloqueados por rate limiting",
    ["endpoint", "reason"],  # reason: ip_limit, device_limit, session_limit
)
```

## Notes

- Los buckets del histograma de latencia deben alinearse con el SLO de 8 segundos de tiempo de respuesta total, incluyendo valores intermedios para identificar cuellos de botella por módulo.
- Las métricas de spoofing (liveness_failures) son especialmente importantes para detectar ataques coordinados y ajustar los umbrales del módulo de detección de vida.
- En producción con Kubernetes, preferir `kubernetes_sd_configs` para autodiscovery en lugar de targets estáticos, manteniendo coherencia con la infraestructura descrita en el stack tecnológico.
