---
name: device_fingerprinting
description: Identificar dispositivo de forma única para detectar múltiples intentos de verificación fraudulentos
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# device_fingerprinting

El device fingerprinting crea un identificador único del dispositivo usando señales del browser/SO para detectar cuando un mismo dispositivo intenta verificarse múltiples veces con documentos distintos.

## When to use

Aplicar al inicio de cada sesión para generar el fingerprint, y consultarlo al detectar comportamiento sospechoso.

## Instructions

1. En el frontend recoger señales: User-Agent, pantalla (resolución, color depth), timezone, idioma, fuentes instaladas, WebGL renderer, Canvas fingerprint, AudioContext fingerprint.
2. Hashear la combinación: `device_id = sha256(signals_json)`.
3. Enviar `device_id` al backend en cada request (header `X-Device-ID`).
4. En Redis: `INCR device:{device_id}:attempts`. Si > N intentos en 24h: flag sospechoso.
5. Almacenar en Redis: `device_id → [session_ids]` con TTL de 7 días.
6. Detectar cuando el mismo `device_id` intenta verificar con >2 documentos distintos en 24h.
7. Para mayor robustez, combinar con IP fingerprinting.

## Notes

- Librería JavaScript recomendada: FingerprintJS (versión open-source: https://github.com/fingerprintjs/fingerprintjs).
- El fingerprint no es 100% estable (cambia con actualizaciones de browser); usar con tolerancia.
- No almacenar el fingerprint más allá del periodo de retención GDPR.