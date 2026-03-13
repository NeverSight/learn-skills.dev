---
name: kubernetes_hpa
description: Horizontal Pod Autoscaler para escalar workers de inferencia, OCR y face matching con metricas custom
type: Tool
priority: Recomendada
mode: Self-hosted
---

# kubernetes_hpa

Skill para configurar Horizontal Pod Autoscaler (HPA) de Kubernetes que escale automaticamente los workers de los servicios de inferencia del pipeline KYC basandose en metricas custom relevantes como profundidad de cola de tareas, latencia de procesamiento y utilizacion de GPU. El escalado automatico es critico para manejar picos de demanda en verificaciones de identidad sin degradar los tiempos de respuesta por debajo del SLO de 8 segundos.

## When to use

Utilizar esta skill cuando el health_monitor_agent necesite configurar o ajustar el autoescalado de los servicios del pipeline KYC. Es especialmente relevante cuando se observan aumentos de latencia bajo carga, cuando se planifican campanas de onboarding masivo, o cuando se necesita optimizar costes reduciendo replicas en horas de baja demanda.

## Instructions

1. Configurar el HPA basico con metricas de CPU y memoria para el servicio de face matching:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: face-match-hpa
  namespace: kyc-pipeline
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: face-match-service
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 30
      policies:
      - type: Pods
        value: 2
        periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Pods
        value: 1
        periodSeconds: 120
```

2. Desplegar Prometheus Adapter para exponer metricas custom al HPA de Kubernetes:
```yaml
# prometheus-adapter-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-adapter-config
  namespace: monitoring
data:
  config.yaml: |
    rules:
    - seriesQuery: 'kyc_verification_queue_depth{namespace="kyc-pipeline"}'
      resources:
        overrides:
          namespace: {resource: "namespace"}
          pod: {resource: "pod"}
      name:
        matches: "^(.*)$"
        as: "kyc_queue_depth"
      metricsQuery: 'sum(<<.Series>>{<<.LabelMatchers>>}) by (<<.GroupBy>>)'
    - seriesQuery: 'kyc_processing_latency_seconds{namespace="kyc-pipeline"}'
      resources:
        overrides:
          namespace: {resource: "namespace"}
          pod: {resource: "pod"}
      name:
        matches: "^(.*)$"
        as: "kyc_p99_latency"
      metricsQuery: 'histogram_quantile(0.99, sum(rate(<<.Series>>{<<.LabelMatchers>>}[2m])) by (le, <<.GroupBy>>))'
```

3. Configurar HPA con metricas custom de cola de tareas para el servicio de OCR:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ocr-hpa
  namespace: kyc-pipeline
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ocr-service
  minReplicas: 2
  maxReplicas: 8
  metrics:
  - type: Pods
    pods:
      metric:
        name: kyc_queue_depth
      target:
        type: AverageValue
        averageValue: "5"   # Escalar cuando hay mas de 5 tareas en cola por pod
  - type: Pods
    pods:
      metric:
        name: kyc_p99_latency
      target:
        type: AverageValue
        averageValue: "4"   # Escalar cuando p99 > 4 segundos
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 30
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Pods
        value: 1
        periodSeconds: 180
```

4. Configurar HPA para el servicio de liveness detection con metrica de GPU:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: liveness-hpa
  namespace: kyc-pipeline
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: liveness-service
  minReplicas: 2
  maxReplicas: 6
  metrics:
  - type: Pods
    pods:
      metric:
        name: nvidia_gpu_utilization
      target:
        type: AverageValue
        averageValue: "75"
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 65
```

5. Exponer metricas custom desde los microservicios FastAPI para que Prometheus las recolecte:
```python
from prometheus_client import Gauge, Histogram

queue_depth = Gauge(
    "kyc_verification_queue_depth",
    "Number of pending verification tasks",
    ["service"]
)

processing_latency = Histogram(
    "kyc_processing_latency_seconds",
    "Time to process a verification request",
    ["service", "step"],
    buckets=[0.5, 1, 2, 4, 6, 8, 10, 15, 30]
)

# Actualizar en cada request
async def process_verification(request):
    queue_depth.labels(service="face_match").set(get_queue_size())
    with processing_latency.labels(service="face_match", step="inference").time():
        result = await run_inference(request)
    queue_depth.labels(service="face_match").set(get_queue_size())
    return result
```

6. Configurar KEDA (Kubernetes Event-Driven Autoscaling) como alternativa avanzada para escalar basandose en la cola de Redis:
```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: face-match-scaledobject
  namespace: kyc-pipeline
spec:
  scaleTargetRef:
    name: face-match-service
  minReplicaCount: 2
  maxReplicaCount: 10
  cooldownPeriod: 300
  triggers:
  - type: redis
    metadata:
      address: redis.kyc-pipeline.svc:6379
      listName: kyc:face_match:queue
      listLength: "10"
      activationListLength: "3"
```

7. Implementar un dashboard de monitorizacion del HPA para el health_monitor_agent:
```bash
# Script para verificar estado del HPA
kubectl get hpa -n kyc-pipeline -o wide
kubectl describe hpa face-match-hpa -n kyc-pipeline
# Verificar metricas custom disponibles
kubectl get --raw "/apis/custom.metrics.k8s.io/v1beta1" | jq '.resources[].name'
```

## Notes

- Configurar el scaleDown con una ventana de estabilizacion de al menos 5 minutos (300 segundos) para evitar oscilaciones rapidas (flapping) que causan cold starts frecuentes en servicios ML donde cargar modelos toma mas de un minuto.
- Los minReplicas para servicios criticos del pipeline (face_match, liveness, ocr) nunca deben ser menores a 2 para garantizar disponibilidad; el decision engine puede funcionar con 1 replica minima al ser stateless y ligero.
- Monitorizar regularmente las metricas del HPA con `kubectl get hpa -n kyc-pipeline` y ajustar los targets segun los patrones de trafico observados; un HPA que esta constantemente al maximo de replicas indica que maxReplicas es insuficiente.
