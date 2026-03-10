---
name: api_key_management
description: Autenticación para clientes server-to-server mediante API Keys
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# api_key_management

Gestión de API Keys para autenticación de clientes server-to-server (backends de terceros que integran el sistema KYC). Complementa JWT para clientes móviles/web.

## When to use

Usar en el `api_gateway_agent` para autenticar peticiones de clientes B2B que integran la API de verificación. Los clientes móviles/web usan JWT; los backends externos usan API Keys.

## Instructions

1. Generar API Keys con `secrets.token_urlsafe(32)` — mínimo 256 bits de entropía.
2. Almacenar hash SHA-256 de la key en PostgreSQL: `api_keys(key_hash, client_id, scopes, created_at, expires_at)`.
3. El cliente envía la key en header: `X-API-Key: <key>`.
4. Nginx valida contra Redis (cache de keys activas): `redis.sismember('active_api_keys', sha256(key))`.
5. Implementar rate limiting por API Key además de por IP.
6. Rotación: emitir nueva key, período de gracia con ambas activas, revocar la antigua.
7. Auditar todos los accesos por API Key.

## Notes

- Nunca loguear la API Key completa; solo los últimos 4 caracteres para identificación.
- Implementar scopes por key: `verify`, `status`, `admin`.
- Las keys expiradas se revocan automáticamente; el cliente debe renovar proactivamente.