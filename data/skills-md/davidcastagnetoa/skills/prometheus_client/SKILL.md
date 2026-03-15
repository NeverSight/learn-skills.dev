---
name: prometheus_client
description: Cliente Python de Prometheus para instrumentar el pipeline KYC con metricas custom
type: Library
priority: Recomendada
mode: Self-hosted
---

# prometheus_client

Cliente Python de Prometheus para instrumentar el codigo del pipeline de verificacion de identidad KYC con metricas custom. Permite definir contadores de verificaciones exitosas y fallidas, histogramas de latencia por modulo (liveness, OCR, face match), y gauges para monitorear el estado de modelos ML cargados en memoria.

## When to use

Usa esta skill cuando necesites instrumentar los microservicios del pipeline KYC con metricas de Prometheus. Pertenece al **observability_agent** y se aplica cuando hay que exponer metricas custom desde el codigo Python (FastAPI) para que Prometheus las recolecte.

## Instructions

1. Instalar la libreria del cliente de Prometheus para Python:
   ```bash
   pip install prometheus-client
   ```

2. Definir las metricas custom en un modulo compartido del backend:
   ```python
   from prometheus_client import Counter, Histogram, Gauge

   VERIFICATION_TOTAL = Counter(
       'kyc_verifications_total',
       'Total de verificaciones KYC procesadas',
       ['status', 'module']
   )

   VERIFICATION_LATENCY = Histogram(
       'kyc_verification_duration_seconds',
       'Latencia de cada etapa de verificacion',
       ['stage'],
       buckets=[0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 8.0]
   )

   MODELS_LOADED = Gauge(
       'kyc_models_loaded',
       'Numero de modelos ML actualmente cargados',
       ['model_name']
   )
   ```

3. Instrumentar los endpoints de FastAPI con las metricas definidas:
   ```python
   from prometheus_client import start_http_server

   @app.on_event("startup")
   async def startup():
       start_http_server(9090)  # Puerto dedicado para metricas
   ```

4. Registrar contadores en cada paso del pipeline de verificacion:
   ```python
   @app.post("/api/v1/verify")
   async def verify_identity(session: VerificationSession):
       with VERIFICATION_LATENCY.labels(stage="liveness").time():
           liveness_result = await liveness_module.check(session)
       VERIFICATION_TOTAL.labels(status=liveness_result.status, module="liveness").inc()
   ```

5. Actualizar los gauges cuando se carguen o descarguen modelos de inferencia:
   ```python
   def load_model(model_name: str):
       model = load_insightface_model(model_name)
       MODELS_LOADED.labels(model_name=model_name).set(1)
       return model
   ```

6. Agregar metricas de negocio especificas del KYC como tasa de fraude detectado:
   ```python
   FRAUD_DETECTED = Counter(
       'kyc_fraud_detected_total',
       'Intentos de fraude detectados',
       ['fraud_type']  # deepfake, printed_photo, screen_replay, mask
   )
   ```

7. Configurar el scrape en Prometheus apuntando al puerto de metricas:
   ```yaml
   scrape_configs:
     - job_name: 'kyc-pipeline'
       scrape_interval: 15s
       static_configs:
         - targets: ['kyc-backend:9090']
   ```

8. Validar que las metricas se exponen correctamente accediendo al endpoint `/metrics` y verificando que los tipos (counter, histogram, gauge) son correctos.

## Notes

- Los histogramas de latencia deben tener buckets alineados con el objetivo de respuesta total de 8 segundos definido en los criterios de calidad del sistema.
- Evitar alta cardinalidad en las labels; no usar session_id como label ya que generaria series temporales ilimitadas. Usar labels categoricas como status, module o fraud_type.
- Las metricas deben exponerse en un puerto separado del API principal para no interferir con el trafico de verificacion y facilitar el acceso desde Prometheus sin exponer endpoints de negocio.
