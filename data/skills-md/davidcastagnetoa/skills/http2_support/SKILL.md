---
name: http2_support
description: Multiplexación de conexiones HTTP/2 para reducir latencia en uploads de imágenes
type: Protocol
priority: Esencial
mode: Self-hosted
---

# http2_support

HTTP/2 permite multiplexar múltiples streams sobre una sola conexión TCP, eliminando el head-of-line blocking de HTTP/1.1. Crítico para el upload paralelo de selfie y documento.

## When to use

Configurar en el `api_gateway_agent` (Nginx) para todas las conexiones de clientes. Especialmente beneficioso cuando el cliente envía selfie y documento en paralelo.

## Instructions

1. Habilitar en Nginx:
   ```nginx
   listen 443 ssl http2;
   http2_max_concurrent_streams 128;
   http2_body_preread_size 64k;
   ```
2. Configurar tamaño máximo de frame: `http2_chunk_size 8k`.
3. Habilitar server push para recursos estáticos si hay frontend web.
4. Verificar soporte del cliente: `curl --http2 https://api.verifid.com/health`.
5. Configurar fallback a HTTP/1.1 para clientes que no soporten HTTP/2.
6. Monitorizar conexiones HTTP/2 activas en métricas Prometheus.

## Notes

- HTTP/2 requiere TLS; no funciona sobre conexiones no cifradas en navegadores.
- El upload de imágenes grandes se beneficia de la compresión de headers HPACK.
- Nginx soporta HTTP/2 hacia clientes pero usa HTTP/1.1 hacia backends por defecto.