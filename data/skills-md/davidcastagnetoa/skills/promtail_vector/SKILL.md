---
name: promtail_vector
description: Agentes de recolección de logs (Promtail o Vector) para centralizar logs del pipeline KYC en Grafana Loki.
type: Tool
priority: Esencial
mode: Self-hosted
---

# promtail_vector

Configura agentes de recolección de logs como Promtail o Vector para capturar y enviar los logs generados por todos los microservicios del pipeline de verificación de identidad hacia Grafana Loki. Esto permite centralizar logs de módulos como liveness detection, OCR, face_match y antifraud en un único sistema consultable. Soporta etiquetado automático por servicio, entorno y nivel de severidad.

## When to use

Usar este skill cuando el observability_agent necesite configurar la recolección y envío centralizado de logs desde los servicios del pipeline KYC hacia Loki. Aplica tanto para despliegues Docker Compose como Kubernetes.

## Instructions

1. Elegir el agente de recolección según el entorno. Promtail es nativo de Loki; Vector es más flexible y soporta múltiples destinos:
   ```yaml
   # docker-compose.yml - Promtail
   promtail:
     image: grafana/promtail:2.9.0
     volumes:
       - /var/log:/var/log
       - ./promtail-config.yml:/etc/promtail/config.yml
     command: -config.file=/etc/promtail/config.yml
   ```

2. Configurar Promtail para descubrir y etiquetar logs de los contenedores del pipeline KYC:
   ```yaml
   # promtail-config.yml
   server:
     http_listen_port: 9080
   positions:
     filename: /tmp/positions.yaml
   clients:
     - url: http://loki:3100/loki/api/v1/push
   scrape_configs:
     - job_name: kyc-pipeline
       docker_sd_configs:
         - host: unix:///var/run/docker.sock
       relabel_configs:
         - source_labels: ['__meta_docker_container_name']
           target_label: 'service'
         - source_labels: ['__meta_docker_container_label_module']
           target_label: 'module'
   ```

3. Alternativamente, configurar Vector como agente de recolección con transformaciones:
   ```toml
   # vector.toml
   [sources.kyc_logs]
   type = "docker_logs"
   include_containers = ["liveness", "ocr", "face_match", "antifraud", "decision"]

   [transforms.parse_json]
   type = "remap"
   inputs = ["kyc_logs"]
   source = '''
   . = parse_json!(.message)
   .service = .container_name
   '''

   [sinks.loki]
   type = "loki"
   inputs = ["parse_json"]
   endpoint = "http://loki:3100"
   labels.service = "{{ service }}"
   labels.level = "{{ level }}"
   ```

4. Asegurar que todos los servicios FastAPI del pipeline emitan logs en formato JSON estructurado:
   ```python
   import logging
   import json_logging

   json_logging.init_fastapi(enable_json=True)
   logger = logging.getLogger("kyc-pipeline")
   logger.setLevel(logging.INFO)
   ```

5. Configurar labels diferenciados por módulo KYC para facilitar filtrado en Loki:
   ```yaml
   labels:
     service: "face_match"
     module: "biometric"
     environment: "production"
     pipeline: "kyc"
   ```

6. Verificar la conectividad y el flujo de logs consultando Loki directamente:
   ```bash
   curl -G "http://loki:3100/loki/api/v1/query" \
     --data-urlencode 'query={service="liveness"}' | jq .
   ```

7. En Kubernetes, desplegar Promtail como DaemonSet para capturar logs de todos los nodos:
   ```bash
   helm install promtail grafana/promtail \
     --set config.clients[0].url=http://loki:3100/loki/api/v1/push \
     --set config.snippets.extraScrapeConfigs=$(cat promtail-k8s-scrape.yaml)
   ```

## Notes

- Promtail es la opción más sencilla si el destino es exclusivamente Loki; Vector ofrece mayor flexibilidad si se necesitan múltiples destinos (Loki + Elasticsearch, por ejemplo).
- Los logs del pipeline KYC pueden contener datos sensibles (session_id, resultados biométricos); asegurarse de que el transporte entre agente y Loki use TLS y que no se logueen imágenes ni embeddings.
- Monitorizar el propio agente de recolección con métricas de bytes enviados, errores de push y lag de posición para evitar pérdida silenciosa de logs.
