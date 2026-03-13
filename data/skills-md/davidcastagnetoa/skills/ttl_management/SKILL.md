---
name: ttl_management
description: Expiración automática de datos con TTL diferenciado por tipo
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# ttl_management

Gestión de Time-To-Live (TTL) diferenciado por tipo de dato para garantizar que los datos temporales se eliminan automáticamente y cumplir con los requisitos GDPR de retención mínima.

## When to use

Usar en el `cache_agent` para asignar TTL apropiado a cada tipo de dato cacheado. Los datos biométricos tienen TTL estricto de 15 minutos por política de privacidad.

## Instructions

1. Definir TTLs por tipo:
   - Sesión activa: 15 minutos (`session:{id}`)
   - Embeddings cacheados: 10 minutos (`embedding:{hash}`)
   - Resultados OCR: 10 minutos (`ocr:{hash}`)
   - Rate limiting counters: 1 hora (`rate:{ip}`)
   - Config/umbrales: 5 minutos (`config:*`)
   - Geo-IP cache: 1 hora (`geoip:{ip}`)
2. Siempre usar `SET key value EX ttl_seconds`.
3. Nunca crear keys sin TTL para datos de sesión.
4. Verificar TTL restante: `TTL key`.
5. Renovar TTL en accesos activos si es necesario: `EXPIRE key ttl`.
6. Monitorizar keys sin TTL: alertar si hay keys de sesión sin expiración.

## Notes

- GDPR requiere eliminación de datos biométricos lo antes posible; 15 min es el máximo.
- Usar `EXPIREAT` para expiración en timestamp absoluto cuando se necesita sincronizar.
- Los TTL se validan en el CI con tests que verifican que toda key de sesión tiene TTL.