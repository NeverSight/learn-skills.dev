---
name: grafana
description: Grafana como plataforma de visualización de dashboards para métricas, logs y trazas del pipeline KYC.
type: Tool
priority: Esencial
mode: Self-hosted
---

# grafana

Configura Grafana como plataforma central de visualización y dashboarding para el sistema de verificación de identidad. Integra múltiples fuentes de datos (Prometheus, Loki, Jaeger, Elasticsearch) en dashboards unificados que muestran el estado del pipeline KYC en tiempo real. Este skill se centra exclusivamente en Grafana como capa de visualización, separada de los backends de datos.

## When to use

Usar este skill cuando el observability_agent necesite crear, configurar o mantener dashboards de Grafana para visualizar métricas, logs y trazas del pipeline de verificación KYC, o cuando se necesite configurar datasources y alertas visuales.

## Instructions

1. Desplegar Grafana con Docker y provisioning automático de datasources:
   ```yaml
   # docker-compose.yml
   grafana:
     image: grafana/grafana:10.2.0
     ports:
       - "3000:3000"
     environment:
       - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_ADMIN_PASSWORD}
       - GF_USERS_ALLOW_SIGN_UP=false
     volumes:
       - grafana_data:/var/lib/grafana
       - ./grafana/provisioning:/etc/grafana/provisioning
       - ./grafana/dashboards:/var/lib/grafana/dashboards
   ```

2. Configurar provisioning automático de datasources para el pipeline KYC:
   ```yaml
   # grafana/provisioning/datasources/datasources.yml
   apiVersion: 1
   datasources:
     - name: Prometheus
       type: prometheus
       access: proxy
       url: http://prometheus:9090
       isDefault: true

     - name: Loki
       type: loki
       access: proxy
       url: http://loki:3100

     - name: Jaeger
       type: jaeger
       access: proxy
       url: http://jaeger:16686

     - name: Elasticsearch
       type: elasticsearch
       access: proxy
       url: http://elasticsearch:9200
       database: "kyc-*"
       jsonData:
         timeField: "timestamp"
         esVersion: "8.0.0"
   ```

3. Crear un dashboard principal de overview del pipeline KYC con paneles clave:
   ```json
   {
     "dashboard": {
       "title": "KYC Pipeline - Overview",
       "panels": [
         {
           "title": "Verificaciones por Minuto",
           "type": "timeseries",
           "targets": [{ "expr": "rate(kyc_verification_requests_total[5m])" }]
         },
         {
           "title": "Tasa de Aprobación",
           "type": "gauge",
           "targets": [{ "expr": "kyc:verification_success_rate:5m" }],
           "fieldConfig": { "defaults": { "thresholds": { "steps": [
             { "value": 0, "color": "red" },
             { "value": 0.7, "color": "yellow" },
             { "value": 0.9, "color": "green" }
           ]}}}
         },
         {
           "title": "Latencia p99 por Módulo",
           "type": "timeseries",
           "targets": [{ "expr": "histogram_quantile(0.99, rate(kyc_verification_duration_seconds_bucket[5m]))" }]
         },
         {
           "title": "Intentos de Spoofing Detectados",
           "type": "stat",
           "targets": [{ "expr": "increase(kyc_verification_requests_total{status='rejected_spoofing'}[1h])" }]
         }
       ]
     }
   }
   ```

4. Crear un dashboard específico para análisis de fraude y liveness:
   ```json
   {
     "dashboard": {
       "title": "KYC - Anti-Fraud & Liveness",
       "panels": [
         {
           "title": "Distribución de Confidence Scores",
           "type": "histogram",
           "targets": [{ "expr": "kyc_confidence_score_bucket{module='face_match'}" }]
         },
         {
           "title": "Tipos de Ataque Detectados",
           "type": "piechart",
           "targets": [{ "expr": "sum by (attack_type) (increase(kyc_spoofing_detected_total[24h]))" }]
         },
         {
           "title": "Logs de Verificaciones Rechazadas",
           "type": "logs",
           "datasource": "Loki",
           "targets": [{ "expr": "{pipeline=\"kyc\"} | json | decision=\"REJECTED\"" }]
         }
       ]
     }
   }
   ```

5. Configurar provisioning automático de dashboards desde archivos JSON:
   ```yaml
   # grafana/provisioning/dashboards/dashboards.yml
   apiVersion: 1
   providers:
     - name: 'KYC Dashboards'
       orgId: 1
       folder: 'KYC Pipeline'
       type: file
       disableDeletion: false
       editable: true
       options:
         path: /var/lib/grafana/dashboards
         foldersFromFilesStructure: true
   ```

6. Configurar alertas visuales en Grafana para notificaciones del pipeline KYC:
   ```yaml
   # grafana/provisioning/alerting/contact-points.yml
   apiVersion: 1
   contactPoints:
     - orgId: 1
       name: kyc-ops-team
       receivers:
         - uid: slack-kyc
           type: slack
           settings:
             url: ${SLACK_WEBHOOK_URL}
             channel: "#kyc-alerts"
         - uid: email-kyc
           type: email
           settings:
             addresses: "kyc-ops@company.com"
   ```

7. Configurar variables de template para filtrado dinámico en los dashboards:
   ```json
   {
     "templating": {
       "list": [
         {
           "name": "module",
           "type": "query",
           "query": "label_values(kyc_verification_requests_total, module)",
           "datasource": "Prometheus"
         },
         {
           "name": "environment",
           "type": "custom",
           "options": [
             { "text": "production", "value": "production" },
             { "text": "staging", "value": "staging" }
           ]
         }
       ]
     }
   }
   ```

## Notes

- Organizar los dashboards en folders por dominio (Overview, Liveness, OCR, Face Match, Anti-Fraud) para mantener la navegabilidad a medida que el sistema crece.
- Los dashboards deben incluir links de correlación entre paneles de métricas (Prometheus), logs (Loki) y trazas (Jaeger) para facilitar el drill-down durante incidentes.
- Restringir el acceso a dashboards con datos sensibles de verificación mediante roles y permisos de Grafana; el equipo de operaciones no necesita ver los mismos datos que el equipo de compliance.
