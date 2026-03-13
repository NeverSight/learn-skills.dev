---
name: hard_rule_engine
description: Reglas de rechazo/aprobación inmediata independientes del score global para casos deterministas
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# hard_rule_engine

El motor de reglas duras implementa condiciones binarias que producen rechazo o aprobación inmediata, independientemente del score compuesto. Garantizan que ciertos casos nunca pasen sin importar los scores individuales.

## When to use

Evaluar antes y después del weighted score aggregator. Las reglas duras tienen prioridad absoluta sobre cualquier score.

## Instructions

1. Definir reglas de rechazo inmediato (ANY condición = rechazado):
   - `liveness_score < 0.3` → `LIVENESS_FAILED`
   - `virtual_camera_detected = true` → `VIRTUAL_CAMERA`
   - `document_expired = true` → `DOCUMENT_EXPIRED`
   - `face_match_score < 0.2` → `IDENTITY_MISMATCH`
   - `rate_limit_exceeded = true` → `TOO_MANY_ATTEMPTS`
   - `mrz_checksum_failures > 2` → `DOCUMENT_TAMPERED`
2. Definir reglas de aprobación inmediata (solo si confianza muy alta en todos los módulos):
   - `liveness_score > 0.95 AND face_match_score > 0.95 AND doc_integrity > 0.9` → fast-track approval.
3. Servir las reglas desde Redis para actualizarlas sin redeploy.
4. Registrar qué regla disparó la decisión en el evento de auditoría.
5. Incluir el código de regla en el response al cliente: `{ status: 'REJECTED', reason: 'LIVENESS_FAILED' }`.

## Notes

- Las reglas duras deben ser revisadas por el equipo de fraude periódicamente.
- Documentar cada regla con su justificación en el ADR correspondiente.