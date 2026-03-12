---
name: encryption_tls
description: Cifrado TLS 1.3 en todas las comunicaciones y cifrado de imágenes en tránsito
type: Protocol
priority: Esencial
mode: Self-hosted
---

# encryption_tls

Todas las comunicaciones del sistema deben usar TLS 1.3 mínimo. Las imágenes biométricas deben cifrarse adicionalmente antes de transmitirse por la red interna.

## When to use

Configurar como requisito base de toda la infraestructura. No opcional.

## Instructions

1. Certificados TLS: usar `cert-manager` en Kubernetes para gestión automática con Let's Encrypt.
2. Configurar Nginx para TLS 1.3 exclusivamente: `ssl_protocols TLSv1.3; ssl_prefer_server_ciphers off;`.
3. HSTS header: `add_header Strict-Transport-Security "max-age=31536000; includeSubDomains"`.
4. Para comunicación interna entre microservicios: mTLS via Istio service mesh.
5. Cifrado adicional de imágenes biométricas: usar AES-256-GCM con clave gestionada por Vault.
6. Clave de cifrado de imágenes: generada por sesión, nunca reutilizada, eliminada tras verificación.
7. Verificar configuración TLS periódicamente con `testssl.sh` o SSL Labs.

## Notes

- mTLS con Istio: cada servicio tiene su propia identidad de certificado (SPIFFE/SPIRE).
- No transmitir embeddings biométricos sin cifrar, ni siquiera en la red interna.