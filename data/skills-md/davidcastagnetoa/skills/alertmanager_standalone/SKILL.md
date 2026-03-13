---
name: alertmanager_standalone
description: Alertmanager independiente para routing de alertas del pipeline KYC con integraciones externas
type: Tool
priority: Esencial
mode: Self-hosted
---

# alertmanager_standalone

Prometheus Alertmanager desplegado como componente independiente para gestionar el ciclo de vida completo de las alertas del pipeline KYC. Maneja routing inteligente de alertas, silencing durante ventanas de mantenimiento, agrupacion de alertas relacionadas e integracion con canales de notificacion como PagerDuty y Slack.

## When to use

Usa esta skill cuando necesites configurar o gestionar Alertmanager como servicio separado de Prometheus para el pipeline KYC. Pertenece al **observability_agent** y se aplica cuando hay que definir reglas de routing, configurar receptores de notificaciones, o gestionar silences y inhibiciones de alertas criticas del sistema de verificacion.

## Instructions

1. Desplegar Alertmanager como contenedor independiente en el cluster:

   ```yaml
   # docker-compose.alertmanager.yml
   services:
     alertmanager:
       image: prom/alertmanager:v0.27.0
       ports:
         - "9093:9093"
       volumes:
         - ./alertmanager/alertmanager.yml:/etc/alertmanager/alertmanager.yml
         - alertmanager-data:/alertmanager
       command:
         - '--config.file=/etc/alertmanager/alertmanager.yml'
         - '--storage.path=/alertmanager'
         - '--cluster.listen-address=0.0.0.0:9094'
       restart: unless-stopped
   ```

2. Configurar el routing de alertas con receptores diferenciados por severidad:

   ```yaml
   # alertmanager.yml
   global:
     resolve_timeout: 5m

   route:
     receiver: 'slack-default'
     group_by: ['alertname', 'module']
     group_wait: 30s
     group_interval: 5m
     repeat_interval: 4h
     routes:
       - match:
           severity: critical
         receiver: 'pagerduty-kyc'
         group_wait: 10s
       - match:
           module: liveness
         receiver: 'slack-antifraude'
       - match:
           severity: warning
         receiver: 'slack-default'
   ```

3. Configurar los receptores de PagerDuty para alertas criticas del pipeline:

   ```yaml
   receivers:
     - name: 'pagerduty-kyc'
       pagerduty_configs:
         - service_key_file: '/etc/alertmanager/secrets/pagerduty_key'
           severity: 'critical'
           description: '{{ .CommonAnnotations.summary }}'
           details:
             module: '{{ .CommonLabels.module }}'
             session_count: '{{ .CommonAnnotations.affected_sessions }}'
   ```

4. Configurar el receptor de Slack para alertas de severidad warning:

   ```yaml
     - name: 'slack-default'
       slack_configs:
         - api_url_file: '/etc/alertmanager/secrets/slack_webhook'
           channel: '#kyc-alerts'
           title: '[{{ .Status | toUpper }}] {{ .CommonLabels.alertname }}'
           text: '{{ .CommonAnnotations.description }}'
           send_resolved: true
     - name: 'slack-antifraude'
       slack_configs:
         - api_url_file: '/etc/alertmanager/secrets/slack_webhook'
           channel: '#kyc-antifraude'
           title: 'Alerta Liveness: {{ .CommonLabels.alertname }}'
           text: '{{ .CommonAnnotations.description }}'
   ```

5. Definir reglas de inhibicion para evitar cascadas de alertas:

   ```yaml
   inhibit_rules:
     - source_match:
         severity: 'critical'
       target_match:
         severity: 'warning'
       equal: ['alertname', 'module']
     - source_match:
         alertname: 'KYCServiceDown'
       target_match:
         alertname: 'KYCHighLatency'
       equal: ['module']
   ```

6. Definir las alerting rules en Prometheus apuntando al Alertmanager independiente:

   ```yaml
   # prometheus.yml
   alerting:
     alertmanagers:
       - static_configs:
           - targets: ['alertmanager:9093']

   rule_files:
     - '/etc/prometheus/rules/kyc_alerts.yml'
   ```

7. Crear reglas de alerta especificas para el pipeline KYC:

   ```yaml
   # kyc_alerts.yml
   groups:
     - name: kyc-pipeline
       rules:
         - alert: KYCHighFraudRate
           expr: rate(kyc_fraud_detected_total[5m]) > 0.1
           for: 2m
           labels:
             severity: critical
             module: antifraud
           annotations:
             summary: "Tasa de fraude anormalmente alta"
             description: "Se detectan mas de 0.1 fraudes/s en los ultimos 5 minutos"
         - alert: KYCVerificationLatencyHigh
           expr: histogram_quantile(0.95, rate(kyc_verification_duration_seconds_bucket[5m])) > 8
           for: 3m
           labels:
             severity: warning
           annotations:
             summary: "Latencia p95 supera el objetivo de 8 segundos"
   ```

8. Validar la configuracion con amtool antes de desplegar:
   ```bash
   amtool check-config alertmanager.yml
   amtool config routes show --config.file=alertmanager.yml
   ```

## Notes

- Alertmanager debe desplegarse en modo cluster (minimo 2 instancias) en produccion para alta disponibilidad, usando el flag `--cluster.peer` para sincronizacion.
- Los secrets de PagerDuty y Slack deben gestionarse mediante Kubernetes Secrets o un vault, nunca en texto plano en la configuracion.
- El grupo de alertas por `module` permite correlacionar problemas con etapas especificas del pipeline KYC (liveness, face_match, ocr, doc_processing) y escalar al equipo correcto.
