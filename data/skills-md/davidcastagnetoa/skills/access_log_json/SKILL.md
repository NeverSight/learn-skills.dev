---
name: access_log_json
description: Log de cada petición al gateway con IP, endpoint, latencia, status code y trace_id para trazabilidad end-to-end
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# access_log_json

El access log en formato JSON del gateway es el registro primario de todas las peticiones recibidas. Incluye el trace_id inyectado por el gateway para correlacionar con los logs de los microservicios downstream.

## When to use

Activar desde el inicio del proyecto. Es la fuente de verdad para análisis de rendimiento, detección de ataques y auditoría de accesos.

## Instructions

1. Definir formato JSON en `nginx.conf`:
   ```nginx
   log_format json_combined escape=json '{'
       '"time":"$time_iso8601",'
       '"remote_addr":"$remote_addr",'
       '"method":"$request_method",'
       '"uri":"$uri",'
       '"status":$status,'
       '"duration":$request_time,'
       '"bytes_sent":$bytes_sent,'
       '"trace_id":"$http_x_trace_id",'
       '"user_agent":"$http_user_agent"'
   '}';
   access_log /var/log/nginx/access.log json_combined;
   ```
2. Inyectar `X-Trace-ID` si no viene en el request: `$request_id` como fallback.
3. Propagar `X-Trace-ID` al upstream: `proxy_set_header X-Trace-ID $http_x_trace_id;`
4. Configurar Promtail para leer `/var/log/nginx/access.log` y enviar a Grafana Loki con label `job="nginx"`.
5. Excluir de los logs: `GET /health`, `GET /ready`, `GET /metrics` (demasiado verbosos, sin valor).
6. Retención de access logs: 90 días en Loki para logs normales, indefinido para logs de 4xx/5xx.

## Notes

- Nunca loguear el `Authorization` header ni el body de las peticiones — contienen JWTs e imágenes.
- El campo `trace_id` permite seguir una sesión KYC desde el access log hasta los spans de Jaeger.
- Para IPs de usuarios, considerar hashearlas en logs de Loki si hay requisitos GDPR estrictos.
