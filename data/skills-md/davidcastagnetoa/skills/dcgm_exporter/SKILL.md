---
name: dcgm_exporter
description: NVIDIA DCGM Exporter para metricas de GPU en nodos de inferencia ML del pipeline KYC
type: Tool
priority: Esencial
mode: Self-hosted
---

# dcgm_exporter

NVIDIA Data Center GPU Manager (DCGM) Exporter para recopilar metricas detalladas de GPU de los nodos de inferencia del pipeline KYC. Monitorea utilizacion de GPU, memoria VRAM, temperatura, consumo energetico y errores ECC en las tarjetas que ejecutan los modelos de reconocimiento facial (ArcFace/InsightFace), deteccion de vida y analisis antifraude.

## When to use

Usa esta skill cuando necesites monitorear el estado y rendimiento de las GPUs que ejecutan inferencia ML en el pipeline de verificacion KYC. Pertenece al **observability_agent** y se aplica cuando hay que diagnosticar cuellos de botella en GPU, planificar escalado de nodos de inferencia o detectar degradacion de hardware en las tarjetas graficas.

## Instructions

1. Desplegar DCGM Exporter como DaemonSet en los nodos con GPU del cluster:
   ```yaml
   # k8s/dcgm-exporter-daemonset.yml
   apiVersion: apps/v1
   kind: DaemonSet
   metadata:
     name: dcgm-exporter
     namespace: monitoring
   spec:
     selector:
       matchLabels:
         app: dcgm-exporter
     template:
       metadata:
         labels:
           app: dcgm-exporter
       spec:
         nodeSelector:
           nvidia.com/gpu.present: "true"
         containers:
           - name: dcgm-exporter
             image: nvcr.io/nvidia/k8s/dcgm-exporter:3.3.8-3.6.0-ubuntu22.04
             ports:
               - containerPort: 9400
                 name: metrics
             securityContext:
               runAsNonRoot: false
               capabilities:
                 add: ["SYS_ADMIN"]
             volumeMounts:
               - name: dcgm-counters
                 mountPath: /etc/dcgm-exporter/customized.csv
                 subPath: customized.csv
         volumes:
           - name: dcgm-counters
             configMap:
               name: dcgm-custom-counters
   ```

2. Definir contadores personalizados relevantes para la carga de inferencia KYC:
   ```csv
   # customized.csv
   DCGM_FI_DEV_GPU_UTIL, gauge, GPU utilization
   DCGM_FI_DEV_MEM_COPY_UTIL, gauge, Memory utilization
   DCGM_FI_DEV_FB_FREE, gauge, Free framebuffer memory (MB)
   DCGM_FI_DEV_FB_USED, gauge, Used framebuffer memory (MB)
   DCGM_FI_DEV_GPU_TEMP, gauge, GPU temperature (C)
   DCGM_FI_DEV_POWER_USAGE, gauge, Power usage (W)
   DCGM_FI_DEV_ECC_SBE_VOL_TOTAL, counter, Single-bit ECC errors
   DCGM_FI_DEV_ECC_DBE_VOL_TOTAL, counter, Double-bit ECC errors
   DCGM_FI_DEV_SM_CLOCK, gauge, SM clock frequency (MHz)
   DCGM_FI_DEV_PCIE_TX_THROUGHPUT, counter, PCIe TX throughput
   DCGM_FI_DEV_PCIE_RX_THROUGHPUT, counter, PCIe RX throughput
   DCGM_FI_PROF_GR_ENGINE_ACTIVE, gauge, Graphics engine active ratio
   ```

3. Configurar el scrape de Prometheus para los endpoints de DCGM Exporter:
   ```yaml
   scrape_configs:
     - job_name: 'dcgm-exporter'
       scrape_interval: 15s
       kubernetes_sd_configs:
         - role: pod
       relabel_configs:
         - source_labels: [__meta_kubernetes_pod_label_app]
           regex: dcgm-exporter
           action: keep
         - source_labels: [__meta_kubernetes_pod_node_name]
           target_label: node
   ```

4. Crear alertas para condiciones criticas de GPU en los nodos de inferencia:
   ```yaml
   groups:
     - name: gpu-health
       rules:
         - alert: GPUHighTemperature
           expr: DCGM_FI_DEV_GPU_TEMP > 85
           for: 2m
           labels:
             severity: critical
           annotations:
             summary: "GPU {{ $labels.gpu }} en nodo {{ $labels.node }} a {{ $value }}C"
         - alert: GPUMemoryExhausted
           expr: DCGM_FI_DEV_FB_FREE < 512
           for: 1m
           labels:
             severity: critical
           annotations:
             summary: "GPU {{ $labels.gpu }} con menos de 512MB VRAM libre"
         - alert: GPUECCErrors
           expr: rate(DCGM_FI_DEV_ECC_DBE_VOL_TOTAL[5m]) > 0
           for: 1m
           labels:
             severity: critical
           annotations:
             summary: "Errores ECC double-bit detectados en GPU {{ $labels.gpu }}"
   ```

5. Definir alertas de rendimiento para detectar degradacion de la inferencia:
   ```yaml
         - alert: GPUUtilizationLow
           expr: DCGM_FI_DEV_GPU_UTIL < 10 and on(node) kube_node_status_condition{condition="Ready",status="true"} == 1
           for: 10m
           labels:
             severity: warning
           annotations:
             summary: "GPU infrautilizada en {{ $labels.node }}, considerar consolidar carga"
         - alert: GPUUtilizationSaturated
           expr: DCGM_FI_DEV_GPU_UTIL > 95
           for: 5m
           labels:
             severity: warning
           annotations:
             summary: "GPU saturada en {{ $labels.node }}, posible cuello de botella en inferencia"
   ```

6. Crear un dashboard de Grafana especifico para los nodos de inferencia KYC:
   ```json
   {
     "panels": [
       {
         "title": "GPU Utilization por Nodo",
         "targets": [{"expr": "DCGM_FI_DEV_GPU_UTIL", "legendFormat": "{{ node }}/{{ gpu }}"}]
       },
       {
         "title": "VRAM Usada vs Disponible",
         "targets": [
           {"expr": "DCGM_FI_DEV_FB_USED", "legendFormat": "Usada {{ gpu }}"},
           {"expr": "DCGM_FI_DEV_FB_FREE", "legendFormat": "Libre {{ gpu }}"}
         ]
       },
       {
         "title": "Correlacion GPU vs Latencia KYC",
         "targets": [
           {"expr": "DCGM_FI_DEV_GPU_UTIL"},
           {"expr": "histogram_quantile(0.95, rate(kyc_verification_duration_seconds_bucket{stage='face_match'}[5m]))"}
         ]
       }
     ]
   }
   ```

7. Verificar que el NVIDIA device plugin y los drivers estan correctamente instalados:
   ```bash
   kubectl get nodes -o json | jq '.items[].status.allocatable["nvidia.com/gpu"]'
   dcgmi discovery -l
   ```

## Notes

- Los modelos ArcFace e InsightFace requieren VRAM significativa; la alerta de GPUMemoryExhausted debe ajustarse segun el tamano de los modelos cargados y el batch size de inferencia configurado.
- Los errores ECC double-bit son criticos e indican degradacion del hardware de la GPU; cuando se detecten, se debe drenar el nodo y reemplazar la tarjeta para evitar resultados de inferencia corruptos en las comparaciones faciales.
- El throughput de PCIe es relevante para detectar cuellos de botella en la transferencia de imagenes entre CPU y GPU, especialmente cuando se procesan multiples sesiones de verificacion en paralelo.
