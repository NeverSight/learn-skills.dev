---
name: request_timeout_management
description: Timeout global por tipo de endpoint con cancelación limpia
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# request_timeout_management

Gestión de timeouts configurables por tipo de endpoint para garantizar que ninguna petición bloquee recursos indefinidamente. Alineado con el SLO de 8 segundos del pipeline KYC.

## When to use

Usar en el `api_gateway_agent` para establecer timeouts diferenciados por endpoint. El timeout total de verificación debe ser < 8s; endpoints de consulta < 2s.

## Instructions

1. Configurar timeouts en Nginx por location:
   ```nginx
   location /v1/verify {
       proxy_read_timeout 8s;
       proxy_connect_timeout 2s;
       proxy_send_timeout 2s;
   }
   location /v1/status {
       proxy_read_timeout 2s;
   }
   ```
2. Configurar timeout global de keepalive: `keepalive_timeout 65s`.
3. En FastAPI, usar asyncio timeout para cancelación limpia:
   ```python
   async with asyncio.timeout(7.5):  # 0.5s margen para response
       result = await orchestrator.verify(session)
   ```
4. Si timeout, devolver 504 Gateway Timeout con `session_id` para retry.
5. Registrar timeouts en métricas: `gateway_timeouts_total{endpoint}`.
6. Alertar si tasa de timeouts > 1% en ventana de 5 minutos.

## Notes

- El timeout del gateway debe ser mayor que el del backend para evitar cortar respuestas válidas.
- Implementar client-side timeout también en los SDKs de clientes.
- Los timeouts deben ser configurables por entorno (dev: más largos, prod: estrictos).