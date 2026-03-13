---
name: thanos
description: Almacenamiento a largo plazo de metricas Prometheus con alta disponibilidad y query global
type: Tool
priority: Opcional
mode: Self-hosted
---

# thanos

Thanos como capa de almacenamiento a largo plazo y query global sobre metricas Prometheus del pipeline KYC. Permite retener metricas historicas mas alla de la retencion local de Prometheus, ejecutar queries federadas entre multiples instancias y analizar tendencias del sistema de verificacion a lo largo de meses para planificacion de capacidad y deteccion de regresiones.

## When to use

Usa esta skill cuando necesites configurar almacenamiento duradero de metricas, consultar datos historicos del pipeline KYC o federar metricas entre multiples clusters de Prometheus. Pertenece al **observability_agent** y se aplica cuando la retencion local de Prometheus es insuficiente para analisis de tendencias o cuando se requiere alta disponibilidad en la capa de metricas.

## Instructions

1. Desplegar Thanos Sidecar junto a cada instancia de Prometheus:
   ```yaml
   # k8s/thanos-sidecar.yml
   containers:
     - name: prometheus
       image: prom/prometheus:v2.52.0
       args:
         - '--storage.tsdb.min-block-duration=2h'
         - '--storage.tsdb.max-block-duration=2h'
         - '--storage.tsdb.retention.time=6h'
     - name: thanos-sidecar
       image: quay.io/thanos/thanos:v0.35.0
       args:
         - sidecar
         - '--tsdb.path=/prometheus'
         - '--prometheus.url=http://localhost:9090'
         - '--objstore.config-file=/etc/thanos/objstore.yml'
       volumeMounts:
         - name: prometheus-data
           mountPath: /prometheus
         - name: thanos-config
           mountPath: /etc/thanos
   ```

2. Configurar el almacenamiento de objetos usando MinIO (ya disponible en el stack KYC):
   ```yaml
   # objstore.yml
   type: S3
   config:
     bucket: thanos-metrics
     endpoint: minio.storage:9000
     access_key: ${MINIO_ACCESS_KEY}
     secret_key: ${MINIO_SECRET_KEY}
     insecure: true
   ```

3. Desplegar Thanos Store Gateway para servir datos historicos desde el object storage:
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: thanos-store
     namespace: monitoring
   spec:
     replicas: 2
     template:
       spec:
         containers:
           - name: thanos-store
             image: quay.io/thanos/thanos:v0.35.0
             args:
               - store
               - '--objstore.config-file=/etc/thanos/objstore.yml'
               - '--index-cache-size=500MB'
               - '--chunk-pool-size=2GB'
             ports:
               - containerPort: 10901
                 name: grpc
   ```

4. Desplegar Thanos Querier como punto unico de consulta:
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: thanos-query
     namespace: monitoring
   spec:
     replicas: 2
     template:
       spec:
         containers:
           - name: thanos-query
             image: quay.io/thanos/thanos:v0.35.0
             args:
               - query
               - '--store=dnssrv+_grpc._tcp.thanos-sidecar.monitoring.svc'
               - '--store=dnssrv+_grpc._tcp.thanos-store.monitoring.svc'
               - '--query.auto-downsampling'
             ports:
               - containerPort: 9090
                 name: http
   ```

5. Configurar Thanos Compactor para downsampling y compactacion de bloques historicos:
   ```yaml
   containers:
     - name: thanos-compact
       image: quay.io/thanos/thanos:v0.35.0
       args:
         - compact
         - '--objstore.config-file=/etc/thanos/objstore.yml'
         - '--retention.resolution-raw=30d'
         - '--retention.resolution-5m=180d'
         - '--retention.resolution-1h=365d'
         - '--wait'
         - '--compact.concurrency=2'
   ```

6. Configurar Grafana para usar Thanos Querier como datasource:
   ```yaml
   datasources:
     - name: Thanos
       type: prometheus
       url: http://thanos-query.monitoring:9090
       access: proxy
       jsonData:
         timeInterval: '15s'
   ```

7. Crear queries de ejemplo para analisis historico del pipeline KYC:
   ```promql
   # Tendencia mensual de tasa de verificacion exitosa
   avg_over_time(
     (rate(kyc_verifications_total{status="verified"}[1h]) /
      rate(kyc_verifications_total[1h]))[30d:1h]
   )

   # Evolucion trimestral de latencia p95 por modulo
   histogram_quantile(0.95,
     avg_over_time(rate(kyc_verification_duration_seconds_bucket[1h])[90d:1d])
   )
   ```

8. Validar la replicacion y disponibilidad de datos con queries de diagnostico:
   ```bash
   thanos tools bucket verify --objstore.config-file=objstore.yml
   thanos tools bucket ls --objstore.config-file=objstore.yml
   ```

## Notes

- El bucket de MinIO para Thanos debe estar separado del bucket usado para almacenamiento temporal de imagenes de verificacion, ya que tienen politicas de retencion y acceso completamente diferentes.
- La configuracion de downsampling (raw 30d, 5m resolution 180d, 1h resolution 365d) permite retener un ano de metricas historicas con un costo de almacenamiento razonable para analisis de tendencias del pipeline.
- Thanos Querier debe configurarse con `--query.auto-downsampling` para que automaticamente use resoluciones mas bajas en queries de rango largo, evitando timeouts al consultar meses de datos del pipeline KYC.
