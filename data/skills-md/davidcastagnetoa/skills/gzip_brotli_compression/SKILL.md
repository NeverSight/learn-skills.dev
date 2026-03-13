---
name: gzip_brotli_compression
description: Comprimir respuestas JSON con Gzip/Brotli para reducir payload de red
type: Algorithm
priority: Recomendada
mode: Self-hosted
---

# gzip_brotli_compression

Compresión de respuestas HTTP con Gzip y Brotli para reducir el tamaño de transferencia. Brotli ofrece ~20% mejor compresión que Gzip para contenido textual (JSON, HTML).

## When to use

Configurar en el `api_gateway_agent` para comprimir todas las respuestas JSON. No comprimir imágenes (ya están comprimidas) ni streams de video.

## Instructions

1. Configurar Gzip en Nginx:
   ```nginx
   gzip on;
   gzip_types application/json text/plain application/javascript;
   gzip_min_length 1000;
   gzip_comp_level 6;
   ```
2. Configurar Brotli (requiere módulo ngx_brotli):
   ```nginx
   brotli on;
   brotli_types application/json text/plain;
   brotli_comp_level 6;
   ```
3. Brotli tiene prioridad si el cliente lo soporta (`Accept-Encoding: br`).
4. No comprimir respuestas < 1KB (overhead de compresión > ahorro).
5. Excluir imágenes y binarios: ya están comprimidos.
6. Verificar: `curl -H 'Accept-Encoding: br' -I https://api.verifid.com/v1/status`.

## Notes

- Brotli solo funciona sobre HTTPS; Gzip funciona en HTTP y HTTPS.
- La compresión de nivel 6 es buen balance entre ratio y CPU. No usar nivel 11 (muy lento).
- Las respuestas JSON del pipeline (~2-5KB) se reducen a ~500B-1KB con Brotli.