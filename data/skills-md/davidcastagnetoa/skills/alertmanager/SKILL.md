---
name: alertmanager
description: Gestor de alertas de Prometheus para notificar incidencias criticas del pipeline KYC
type: Tool
priority: Esencial
mode: Self-hosted
---

# alertmanager

Skill para configurar Prometheus Alertmanager como sistema de notificacion de alertas criticas del pipeline de verificacion de identidad KYC. Este skill se centra exclusivamente en la gestion de alertas (enrutamiento, agrupacion, silenciamiento, notificacion) y es independiente de la configuracion de Prometheus como tal. Cubre alertas para degradacion de metricas de calidad (FAR/FRR), caida de workers de inferencia, latencia excesiva del pipeline y agotamiento de error budget.

## When to use

Utilizar esta skill cuando el health_monitor_agent necesite configurar, ajustar o depurar el sistema de alertas del pipeline KYC. Aplica cuando se requiere definir nuevas reglas de alerta, configurar canales de notificacion (Slack, PagerDuty, email), ajustar umbrales de severidad, o resolver problemas de alertas ruidosas o silenciadas incorrectamente.

## Instructions

1. Desplegar Alertmanager con la configuracion base de enrutamiento para el pipeline KYC:
```yaml
# alertmanager-config.yaml
global:
  resolve_timeout: 5m
  slack_api_url: "https://hooks.slack.com/services/XXXXX"

route:
  receiver: "kyc-default"
  group_by: ["alertname", "service", "severity"]
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  routes:
  - match:
      severity: critical
    receiver: "kyc-critical"
    group_wait: 10s
    repeat_interval: 1h
  - match:
      severity: warning
      team: kyc-ml
    receiver: "kyc-ml-team"
    group_wait: 1m
  - match:
      alertname: KYCErrorBudgetBurn
    receiver: "kyc-sre-pagerduty"
    group_wait: 0s
    repeat_interval: 30m

receivers:
- name: "kyc-default"
  slack_configs:
  - channel: "#kyc-alerts"
    title: '{{ .GroupLabels.alertname }}'
    text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

- name: "kyc-critical"
  slack_configs:
  - channel: "#kyc-critical"
    title: 'CRITICAL: {{ .GroupLabels.alertname }}'
    text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
  pagerduty_configs:
  - service_key: "<PAGERDUTY_KEY>"
    severity: critical

- name: "kyc-ml-team"
  slack_configs:
  - channel: "#kyc-ml-models"

- name: "kyc-sre-pagerduty"
  pagerduty_configs:
  - service_key: "<PAGERDUTY_KEY>"
    severity: critical
```

2. Definir reglas de alerta para degradacion de metricas de calidad biometrica (FAR/FRR):
```yaml
# kyc-quality-alerts.yaml
groups:
- name: kyc-quality
  rules:
  - alert: KYCHighFalseAcceptanceRate
    expr: |
      (
        sum(rate(kyc_verification_result_total{result="accepted", ground_truth="impostor"}[1h]))
        /
        sum(rate(kyc_verification_result_total{ground_truth="impostor"}[1h]))
      ) > 0.001
    for: 15m
    labels:
      severity: critical
      team: kyc-ml
    annotations:
      summary: "FAR excede umbral del 0.1%"
      description: "La tasa de falsa aceptacion es {{ $value | humanizePercentage }}, superando el objetivo de 0.1%. Posible degradacion del modelo de face matching."

  - alert: KYCHighFalseRejectionRate
    expr: |
      (
        sum(rate(kyc_verification_result_total{result="rejected", ground_truth="genuine"}[1h]))
        /
        sum(rate(kyc_verification_result_total{ground_truth="genuine"}[1h]))
      ) > 0.05
    for: 15m
    labels:
      severity: warning
      team: kyc-ml
    annotations:
      summary: "FRR excede umbral del 5%"
      description: "La tasa de falso rechazo es {{ $value | humanizePercentage }}. Usuarios legitimos estan siendo rechazados."
```

3. Definir alertas para workers caidos y disponibilidad del pipeline:
```yaml
# kyc-availability-alerts.yaml
groups:
- name: kyc-availability
  rules:
  - alert: KYCServiceDown
    expr: up{namespace="kyc-pipeline"} == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Servicio KYC {{ $labels.job }} caido"
      description: "El servicio {{ $labels.job }} no responde desde hace mas de 1 minuto."

  - alert: KYCFaceMatchWorkersLow
    expr: |
      kube_deployment_status_replicas_available{
        deployment="face-match-service", namespace="kyc-pipeline"
      } < 2
    for: 2m
    labels:
      severity: critical
    annotations:
      summary: "Workers de face matching insuficientes"
      description: "Solo {{ $value }} replicas disponibles de face-match-service. Minimo requerido: 2."

  - alert: KYCPodRestartLoop
    expr: |
      increase(kube_pod_container_status_restarts_total{
        namespace="kyc-pipeline"
      }[1h]) > 5
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Pod {{ $labels.pod }} en restart loop"
      description: "El pod {{ $labels.pod }} se ha reiniciado {{ $value }} veces en la ultima hora."
```

4. Definir alertas de latencia del pipeline de verificacion:
```yaml
# kyc-latency-alerts.yaml
groups:
- name: kyc-latency
  rules:
  - alert: KYCHighLatencyP99
    expr: |
      histogram_quantile(0.99,
        sum(rate(kyc_verification_duration_seconds_bucket{namespace="kyc-pipeline"}[5m]))
        by (le)
      ) > 8
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Latencia p99 del pipeline KYC supera 8 segundos"
      description: "La latencia p99 es {{ $value }}s, superando el SLO de 8 segundos."

  - alert: KYCHighLatencyP99Critical
    expr: |
      histogram_quantile(0.99,
        sum(rate(kyc_verification_duration_seconds_bucket{namespace="kyc-pipeline"}[5m]))
        by (le)
      ) > 15
    for: 2m
    labels:
      severity: critical
    annotations:
      summary: "Latencia p99 critica: {{ $value }}s"
      description: "La latencia p99 duplica el SLO. Investigar inmediatamente."
```

5. Configurar inhibiciones para evitar alertas redundantes en cascada:
```yaml
# En alertmanager-config.yaml
inhibit_rules:
- source_match:
    alertname: "KYCServiceDown"
  target_match:
    severity: "warning"
  equal: ["service"]
  # Si un servicio esta caido, suprimir warnings de latencia/calidad de ese servicio

- source_match:
    alertname: "KYCFaceMatchWorkersLow"
    severity: "critical"
  target_match:
    alertname: "KYCHighLatencyP99"
  equal: ["namespace"]
  # Si hay workers insuficientes, la alerta de latencia es consecuencia
```

6. Configurar reglas de silenciamiento temporal para ventanas de mantenimiento:
```bash
# Crear silence para mantenimiento planificado
amtool silence add \
  --alertmanager.url=http://alertmanager:9093 \
  --author="health_monitor_agent" \
  --comment="Mantenimiento planificado: actualizacion modelo ArcFace" \
  --duration=2h \
  namespace="kyc-pipeline" \
  service="face-match"
```

7. Desplegar Alertmanager en Kubernetes como StatefulSet para alta disponibilidad:
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: alertmanager
  namespace: monitoring
spec:
  replicas: 3
  serviceName: alertmanager
  selector:
    matchLabels:
      app: alertmanager
  template:
    spec:
      containers:
      - name: alertmanager
        image: prom/alertmanager:v0.27.0
        args:
        - "--config.file=/etc/alertmanager/alertmanager.yml"
        - "--cluster.peer=alertmanager-0.alertmanager:9094"
        - "--cluster.peer=alertmanager-1.alertmanager:9094"
        - "--cluster.peer=alertmanager-2.alertmanager:9094"
        ports:
        - containerPort: 9093
        - containerPort: 9094
```

## Notes

- Las alertas criticas del pipeline KYC (servicio caido, FAR elevado, error budget agotado) deben tener un `for` corto (1-2 minutos) y notificar via PagerDuty; las alertas warning pueden tener un `for` mas largo (5-15 minutos) y notificar solo via Slack para evitar fatiga de alertas.
- Configurar inhibiciones es esencial para el pipeline KYC donde los fallos son frecuentemente en cascada: si face-match esta caido, la alerta de latencia del pipeline completo es redundante y debe suprimirse.
- Revisar y ajustar los umbrales de alerta mensualmente basandose en datos reales del pipeline; los valores iniciales de FAR < 0.1% y FRR < 5% son los objetivos del CLAUDE.md pero pueden necesitar calibracion segun el mix de documentos y poblacion de usuarios.
