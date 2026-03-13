---
name: weighted_score_aggregator
description: Algoritmo de agregación ponderada de scores parciales en score global de verificación
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# weighted_score_aggregator

Combina los scores emitidos por cada agente en un score global único usando pesos configurables por entorno.

## When to use

Usar en el decision_agent como paso previo a la aplicación de reglas de negocio.

## Instructions

1. Definir pesos en configuración externa (Redis o YAML): `{ liveness: 0.30, face_match: 0.35, doc_integrity: 0.20, antifraud: 0.15 }`.
2. Asegurar que suma de pesos = 1.0; validar en arranque.
3. Calcular: `global_score = sum(score_i * weight_i for i in agents)`.
4. Si un agente no responde: usar score de penalización (0.0) o excluir con renormalización.
5. Exponer scores individuales en el response para trazabilidad.
6. Permitir overrides de pesos por tipo de documento.

## Notes

- Los pesos deben ser reconfigurables sin redeploy (desde Redis via cache_agent).
- Documentar el racional de cada peso en el ADR correspondiente.