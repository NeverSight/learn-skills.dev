---
name: log_retention_policies
description: Políticas de retención de logs diferenciadas por tipo y sensibilidad para el pipeline KYC.
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# log_retention_policies

Define e implementa políticas de retención de logs diferenciadas según el tipo y la sensibilidad de los datos para el sistema de verificación de identidad. Establece períodos de retención escalonados: logs de auditoría KYC (1 año por requisitos regulatorios), logs operacionales (30 días), y logs de debug (7 días). Garantiza el cumplimiento normativo GDPR/LOPD mientras optimiza el uso de almacenamiento.

## When to use

Usar este skill cuando el observability_agent necesite configurar las políticas de retención y eliminación automática de logs del pipeline KYC, asegurando cumplimiento regulatorio y eficiencia de almacenamiento.

## Instructions

1. Clasificar los logs del pipeline KYC en tres categorías con sus períodos de retención:
   ```yaml
   # log-retention-config.yaml
   retention_policies:
     audit:
       description: "Logs de auditoría: decisiones KYC, verificaciones, resultados"
       retention_days: 365
       includes:
         - "verification_decision"
         - "identity_confirmed"
         - "identity_rejected"
         - "manual_review_triggered"
       storage_class: "cold"

     operational:
       description: "Logs operacionales: rendimiento, errores, métricas de servicio"
       retention_days: 30
       includes:
         - "request_processed"
         - "service_error"
         - "module_latency"
         - "ocr_extraction"
         - "face_match_score"
       storage_class: "warm"

     debug:
       description: "Logs de debug: trazas detalladas, datos de desarrollo"
       retention_days: 7
       includes:
         - "debug_trace"
         - "model_inference_detail"
         - "image_preprocessing_step"
       storage_class: "hot"
   ```

2. Configurar la retención en Grafana Loki usando table_manager o compactor:
   ```yaml
   # loki-config.yaml
   compactor:
     working_directory: /loki/compactor
     shared_store: filesystem
     retention_enabled: true
     retention_delete_delay: 2h

   limits_config:
     retention_period: 720h  # 30 días default

   # Per-tenant overrides para logs de auditoría
   overrides:
     kyc-audit:
       retention_period: 8760h  # 365 días
     kyc-debug:
       retention_period: 168h   # 7 días
   ```

3. Configurar ILM en Elasticsearch para las tres categorías de retención:
   ```json
   PUT _ilm/policy/kyc-audit-policy
   {
     "policy": {
       "phases": {
         "hot": { "actions": { "rollover": { "max_age": "1d" } } },
         "warm": { "min_age": "30d", "actions": { "shrink": { "number_of_shards": 1 }, "forcemerge": { "max_num_segments": 1 } } },
         "cold": { "min_age": "90d", "actions": { "allocate": { "require": { "data": "cold" } } } },
         "delete": { "min_age": "365d", "actions": { "delete": {} } }
       }
     }
   }

   PUT _ilm/policy/kyc-operational-policy
   {
     "policy": {
       "phases": {
         "hot": { "actions": { "rollover": { "max_age": "1d" } } },
         "delete": { "min_age": "30d", "actions": { "delete": {} } }
       }
     }
   }

   PUT _ilm/policy/kyc-debug-policy
   {
     "policy": {
       "phases": {
         "hot": { "actions": { "rollover": { "max_age": "1d" } } },
         "delete": { "min_age": "7d", "actions": { "delete": {} } }
       }
     }
   }
   ```

4. Implementar el etiquetado de logs en el código Python del pipeline para clasificarlos automáticamente:
   ```python
   import logging

   class RetentionClassifier(logging.Filter):
       AUDIT_EVENTS = {"verification_decision", "identity_confirmed", "identity_rejected"}
       DEBUG_EVENTS = {"debug_trace", "model_inference_detail"}

       def filter(self, record):
           event_type = getattr(record, "event_type", "")
           if event_type in self.AUDIT_EVENTS:
               record.retention_class = "audit"
           elif event_type in self.DEBUG_EVENTS:
               record.retention_class = "debug"
           else:
               record.retention_class = "operational"
           return True
   ```

5. Configurar alertas para monitorizar el cumplimiento de las políticas de retención:
   ```yaml
   # alerting-rules.yaml
   groups:
     - name: log_retention
       rules:
         - alert: AuditLogsRetentionRisk
           expr: loki_compactor_oldest_undeleted_chunk_timestamp_seconds{tenant="kyc-audit"} < (time() - 365*24*3600)
           for: 1h
           labels:
             severity: critical
           annotations:
             summary: "Los logs de auditoría KYC podrían no estar cumpliendo la retención de 365 días"
   ```

6. Crear un script de verificación periódica que valide que las políticas se aplican correctamente:
   ```bash
   #!/bin/bash
   # verify-retention.sh
   echo "=== Verificación de retención de logs KYC ==="

   # Verificar logs de auditoría (deben existir hasta 365 días)
   OLDEST_AUDIT=$(curl -s "http://loki:3100/loki/api/v1/query" \
     --data-urlencode 'query={retention_class="audit"} | json' \
     --data-urlencode 'direction=FORWARD' --data-urlencode 'limit=1' | jq -r '.data.result[0].values[0][0]')
   echo "Log de auditoría más antiguo: $(date -d @${OLDEST_AUDIT:0:10})"

   # Verificar que logs de debug mayores a 7 días fueron eliminados
   OLD_DEBUG=$(curl -s "http://loki:3100/loki/api/v1/query_range" \
     --data-urlencode 'query={retention_class="debug"}' \
     --data-urlencode "start=$(date -d '8 days ago' +%s)000000000" \
     --data-urlencode "end=$(date -d '7 days ago' +%s)000000000" | jq '.data.result | length')
   echo "Logs de debug antiguos (>7d) encontrados: $OLD_DEBUG"
   ```

## Notes

- Los logs de auditoría con decisiones KYC (VERIFICADO/RECHAZADO) deben retenerse al menos 1 año para cumplir con requisitos regulatorios GDPR/LOPD y posibles auditorías; nunca reducir este período sin aprobación legal.
- Los logs de debug pueden contener datos sensibles temporales (scores parciales, resultados intermedios); su retención corta de 7 días minimiza la exposición, pero deben sanitizarse igualmente.
- Monitorizar el consumo de almacenamiento por categoría de retención y ajustar las políticas de compactación para evitar crecimiento descontrolado, especialmente en los logs de auditoría de largo plazo.
