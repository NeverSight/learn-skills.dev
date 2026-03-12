---
name: graceful_degradation
description: Devolver respuesta parcial si un servicio no crítico no está disponible
type: Algorithm
priority: Recomendada
mode: Self-hosted
---

# graceful_degradation

Patrón de degradación graceful que permite al sistema continuar operando con funcionalidad reducida cuando un servicio no crítico falla, en lugar de devolver un error total.

## When to use

Usar en el `api_gateway_agent` y `orchestrator_agent` cuando un agente no crítico (antifraud geo-check, age estimation) no responde. El pipeline continúa con penalización de score.

## Instructions

1. Clasificar agentes por criticidad:
   - **Críticos** (pipeline se detiene): liveness, face_match, document_processor.
   - **No críticos** (pipeline continúa): geo-check, age estimation, VPN detection.
2. Si agente no crítico falla, asignar score neutral (0.5) y flag `degraded`.
3. Incluir en respuesta: `"degraded_modules": ["antifraud_geo"]`.
4. Penalizar score global: reducir confianza en -0.05 por cada módulo degradado.
5. Si > 2 módulos degradados, derivar a `MANUAL_REVIEW` automáticamente.
6. Registrar modo degradado en métricas y auditoría.
7. Alertar al `health_monitor_agent` para investigar el servicio caído.

## Notes

- Nunca degradar módulos críticos (liveness, face_match); si fallan, retornar error.
- El modo degradado debe ser transparente para el cliente en la respuesta.
- Revisar semanalmente las métricas de degradación para identificar servicios inestables.
