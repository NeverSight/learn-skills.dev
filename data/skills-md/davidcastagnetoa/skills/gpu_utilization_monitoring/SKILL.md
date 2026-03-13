---
name: gpu_utilization_monitoring
description: Monitorizar uso de GPU de workers de inferencia ML para optimizar recursos y detectar cuellos de botella
type: Tool
priority: Esencial
mode: Self-hosted
---

# gpu_utilization_monitoring

Skill para monitorizar en tiempo real el uso de GPU (memoria VRAM, compute utilization, temperatura y power draw) de los workers de inferencia ML del sistema de verificación KYC. Permite identificar cuellos de botella en el pipeline de modelos faciales, liveness y OCR, y optimizar la asignación de recursos entre modelos.

## When to use

Usar esta skill cuando el **model_server_agent** necesite configurar, consultar o ajustar la monitorización de recursos GPU en los nodos de inferencia. Aplica al dimensionar infraestructura, diagnosticar latencias elevadas, planificar escalado o detectar fugas de memoria VRAM en los modelos desplegados.

## Instructions

1. Configurar la recolección de métricas GPU mediante NVIDIA DCGM (Data Center GPU Manager) como fuente primaria:
   ```bash
   # Instalar y arrancar DCGM exporter para Prometheus
   docker run -d --gpus all --rm -p 9400:9400 \
     nvcr.io/nvidia/k8s/dcgm-exporter:3.3.5-3.4.0-ubuntu22.04
   ```

2. Definir las métricas clave a monitorizar por cada worker de inferencia:
   ```yaml
   # dcgm-metrics.yaml
   metrics:
     - DCGM_FI_DEV_GPU_UTIL        # % uso compute
     - DCGM_FI_DEV_MEM_COPY_UTIL   # % uso memoria
     - DCGM_FI_DEV_FB_USED         # VRAM usada (MB)
     - DCGM_FI_DEV_FB_FREE         # VRAM libre (MB)
     - DCGM_FI_DEV_GPU_TEMP        # Temperatura GPU
     - DCGM_FI_DEV_POWER_USAGE     # Consumo energético (W)
     - DCGM_FI_PROF_SM_OCCUPANCY   # Ocupación de SMs
   ```

3. Configurar dashboards en Grafana con paneles por modelo del pipeline KYC:
   ```
   Panel 1: GPU Utilization por modelo (ArcFace, Liveness, PaddleOCR)
   Panel 2: VRAM allocation y fragmentación
   Panel 3: Latencia de inferencia P50/P95/P99
   Panel 4: Throughput (inferencias/segundo) por modelo
   Panel 5: Temperatura y throttling events
   ```

4. Establecer umbrales de alerta para cada métrica:
   ```python
   GPU_ALERTS = {
       "gpu_util_low": {"threshold": 30, "condition": "below", "action": "consider_consolidation"},
       "gpu_util_high": {"threshold": 90, "condition": "above", "duration": "5m", "action": "scale_out"},
       "vram_usage": {"threshold": 85, "condition": "above_percent", "action": "alert_memory_pressure"},
       "temperature": {"threshold": 83, "condition": "above_celsius", "action": "alert_thermal_throttle"}
   }
   ```

5. Implementar script de diagnóstico rápido para consultar estado actual de GPUs:
   ```bash
   nvidia-smi --query-gpu=index,name,utilization.gpu,utilization.memory,memory.used,memory.total,temperature.gpu,power.draw \
     --format=csv,noheader,nounits
   ```

6. Configurar correlación entre métricas GPU y métricas de negocio (tiempo de verificación total < 8s) para identificar qué modelo es el cuello de botella.

7. Implementar auto-scaling basado en métricas GPU mediante Kubernetes HPA custom metrics:
   ```yaml
   apiVersion: autoscaling/v2
   kind: HorizontalPodAutoscaler
   spec:
     metrics:
       - type: Pods
         pods:
           metric:
             name: DCGM_FI_DEV_GPU_UTIL
           target:
             type: AverageValue
             averageValue: "75"
   ```

## Notes

- La monitorización GPU debe ejecutarse con mínimo overhead; DCGM opera a nivel driver y no impacta el rendimiento de inferencia, a diferencia de polling continuo con nvidia-smi.
- Considerar que los modelos del pipeline KYC tienen patrones de uso diferentes: ArcFace tiene picos en face_match, mientras que liveness es más constante. Dashboards separados por modelo facilitan el diagnóstico.
- Las métricas de temperatura son críticas en despliegues on-premise; el thermal throttling puede degradar latencias sin generar errores visibles en los logs de aplicación.
