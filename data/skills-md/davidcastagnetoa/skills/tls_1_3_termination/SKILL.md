---
name: tls_1_3_termination
description: Cifrado de todo el tráfico en tránsito con TLS 1.3
type: Protocol
priority: Esencial
mode: Self-hosted
---

# tls_1_3_termination

Terminación TLS 1.3 en el API Gateway para cifrar todo el tráfico entre clientes y el sistema. TLS 1.3 elimina handshakes inseguros y reduce la latencia de conexión con 0-RTT.

## When to use

Configurar en el `api_gateway_agent` (Nginx) como punto de terminación TLS para todo el tráfico externo. Todo endpoint público debe estar protegido con TLS 1.3.

## Instructions

1. Generar certificados con cert-manager o Let's Encrypt.
2. Configurar Nginx:
   ```nginx
   ssl_protocols TLSv1.3;
   ssl_prefer_server_ciphers off;
   ssl_certificate /etc/ssl/certs/server.crt;
   ssl_certificate_key /etc/ssl/private/server.key;
   ```
3. Habilitar HSTS: `add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;`.
4. Configurar OCSP stapling para validación rápida de certificados.
5. Deshabilitar TLS 1.0/1.1/1.2 en producción.
6. Probar con `openssl s_client -connect host:443 -tls1_3`.
7. Monitorizar expiración de certificados con alertas 30 días antes.

## Notes

- TLS 1.3 reduce el handshake de 2-RTT a 1-RTT (0-RTT para reconexiones).
- No usar certificados self-signed en producción; siempre Let's Encrypt o CA interna.
- Redirigir HTTP a HTTPS automáticamente: `return 301 https://$host$request_uri`.