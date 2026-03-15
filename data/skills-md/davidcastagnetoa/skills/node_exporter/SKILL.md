---
name: node_exporter
description: Exportador de metricas de sistema para correlacionar recursos del nodo con rendimiento KYC
type: Tool
priority: Esencial
mode: Self-hosted
---

# node_exporter

Prometheus Node Exporter para recopilar metricas de hardware y sistema operativo (CPU, memoria, disco, red) de cada nodo del cluster donde se ejecuta el pipeline KYC. Permite correlacionar el consumo de recursos con el rendimiento de las verificaciones y detectar cuellos de botella en la infraestructura subyacente.

## When to use

Usa esta skill cuando necesites monitorear los recursos fisicos de los nodos que ejecutan el pipeline de verificacion KYC. Pertenece al **observability_agent** y se aplica cuando hay que diagnosticar problemas de rendimiento, planificar capacidad o correlacionar la degradacion del pipeline con la saturacion de recursos del sistema.

## Instructions

1. Desplegar Node Exporter como DaemonSet en Kubernetes para cubrir todos los nodos:
   ```yaml
   # k8s/node-exporter-daemonset.yml
   apiVersion: apps/v1
   kind: DaemonSet
   metadata:
     name: node-exporter
     namespace: monitoring
   spec:
     selector:
       matchLabels:
         app: node-exporter
     template:
       metadata:
         labels:
           app: node-exporter
       spec:
         hostNetwork: true
         hostPID: true
         containers:
           - name: node-exporter
             image: prom/node-exporter:v1.8.0
             args:
               - '--path.rootfs=/host'
               - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
             ports:
               - containerPort: 9100
                 hostPort: 9100
             volumeMounts:
               - name: rootfs
                 mountPath: /host
                 readOnly: true
         volumes:
           - name: rootfs
             hostPath:
               path: /
   ```

2. Configurar Prometheus para descubrir automaticamente los Node Exporters:
   ```yaml
   scrape_configs:
     - job_name: 'node-exporter'
       kubernetes_sd_configs:
         - role: node
       relabel_configs:
         - source_labels: [__address__]
           regex: '(.*):10250'
           replacement: '${1}:9100'
           target_label: __address__
         - source_labels: [__meta_kubernetes_node_name]
           target_label: node
   ```

3. Definir alertas de saturacion de recursos relevantes para el pipeline KYC:
   ```yaml
   groups:
     - name: node-resources
       rules:
         - alert: NodeHighCPU
           expr: 100 - (avg by(node) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 85
           for: 5m
           labels:
             severity: warning
           annotations:
             summary: "CPU del nodo {{ $labels.node }} al {{ $value }}%"
         - alert: NodeHighMemory
           expr: (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100 > 90
           for: 3m
           labels:
             severity: critical
           annotations:
             summary: "Memoria del nodo {{ $labels.node }} al {{ $value }}%"
   ```

4. Monitorear el disco para prevenir problemas con el almacenamiento temporal de imagenes en MinIO:
   ```yaml
         - alert: NodeDiskSpaceLow
           expr: (1 - node_filesystem_avail_bytes{fstype!~"tmpfs|overlay"} / node_filesystem_size_bytes) * 100 > 80
           for: 10m
           labels:
             severity: warning
           annotations:
             summary: "Disco al {{ $value }}% en {{ $labels.mountpoint }} del nodo {{ $labels.node }}"
         - alert: NodeDiskIOHigh
           expr: rate(node_disk_io_time_seconds_total[5m]) > 0.9
           for: 5m
           labels:
             severity: warning
           annotations:
             summary: "IO de disco saturado en nodo {{ $labels.node }}"
   ```

5. Configurar metricas de red para detectar problemas de comunicacion entre microservicios:
   ```yaml
         - alert: NodeNetworkErrors
           expr: rate(node_network_receive_errs_total[5m]) + rate(node_network_transmit_errs_total[5m]) > 10
           for: 3m
           labels:
             severity: warning
           annotations:
             summary: "Errores de red elevados en nodo {{ $labels.node }}"
   ```

6. Crear dashboards de Grafana que correlacionen metricas de nodo con metricas del pipeline:
   ```json
   {
     "targets": [
       {
         "expr": "histogram_quantile(0.95, rate(kyc_verification_duration_seconds_bucket[5m]))",
         "legendFormat": "KYC Latency p95"
       },
       {
         "expr": "100 - avg(rate(node_cpu_seconds_total{mode='idle'}[5m])) * 100",
         "legendFormat": "CPU Usage %"
       }
     ]
   }
   ```

7. Habilitar collectors especificos relevantes para los nodos de inferencia ML:
   ```bash
   node_exporter \
     --collector.cpu \
     --collector.meminfo \
     --collector.diskstats \
     --collector.netdev \
     --collector.loadavg \
     --collector.thermal_zone \
     --no-collector.wifi \
     --no-collector.zfs
   ```

## Notes

- En los nodos que ejecutan inferencia ML (face_match, liveness), prestar especial atencion a la memoria disponible ya que los modelos ArcFace e InsightFace consumen cantidades significativas de RAM.
- Las metricas de disco son criticas porque MinIO almacena temporalmente las imagenes de verificacion; si el disco se satura, todo el pipeline KYC se detiene.
- Usar `hostNetwork: true` es necesario para que Node Exporter acceda a las metricas reales del nodo, pero debe limitarse al namespace de monitoring con NetworkPolicies apropiadas.
