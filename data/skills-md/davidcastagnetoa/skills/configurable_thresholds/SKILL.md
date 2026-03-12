---
name: configurable_thresholds
description: Umbrales de decisión ajustables sin redeploy, servidos desde caché Redis
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# configurable_thresholds

Los umbrales de aprobación/rechazo/revisión manual son configurables en tiempo de ejecución a través de Redis, permitiendo ajustarlos sin necesidad de redeploy del código.

## When to use

Usar en el `decision_agent` para determinar si el score global resulta en APPROVED, REJECTED o MANUAL_REVIEW.

## Instructions

1. Definir estructura de umbrales en Redis (JSON): `{ 'auto_approve': 0.85, 'auto_reject': 0.40, 'manual_review_min': 0.40, 'manual_review_max': 0.85 }`.
2. Cargar umbrales al inicio del `decision_agent` con TTL de 60 segundos (cache refresh).
3. Lógica de decisión:
   ```
   if global_score >= auto_approve: APPROVED
   elif global_score <= auto_reject: REJECTED
   else: MANUAL_REVIEW
   ```
4. Permitir umbrales distintos por tipo de documento, nivel de riesgo del negocio y entorno (prod/staging).
5. Registrar en auditoría qué umbrales estaban activos en el momento de la decisión.
6. Implementar endpoint de admin para actualizar umbrales (protegido, requiere MFA).

## Notes

- En producción inicial, ser conservador: umbral de aprobación alto (0.90) para reducir FAR.
- Ajustar tras análisis de FRR real con usuarios legítimos.