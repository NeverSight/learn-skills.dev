---
name: cross_field_consistency_checker
description: Verificar coherencia entre campos MRZ y zona visual del documento para detectar falsificaciones
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# cross_field_consistency_checker

Compara los datos extraídos de la MRZ con los datos de la zona de lectura visual (VIZ) del documento. Las discrepancias detectan documentos manipulados donde se ha modificado solo una zona.

## When to use

Usar después de obtener resultados de `paddleocr` y `mrz_parser` para validar coherencia.

## Instructions

1. Normalizar campos antes de comparar: quitar acentos, convertir a mayúsculas, limpiar caracteres especiales.
2. Comparar: `document_number_mrz` vs `document_number_viz`.
3. Comparar: `birth_date_mrz` vs `birth_date_viz` (normalizar formato de fecha).
4. Comparar: `expiry_date_mrz` vs `expiry_date_viz`.
5. Comparar: `name_mrz` vs `name_viz` (usar distancia de Levenshtein para tolerancia a errores OCR; umbral ≤2).
6. Calcular score de consistencia: `n_matching / n_total_fields`.
7. Si score < 0.7: emitir flag `DOCUMENT_INCONSISTENCY` al `antifraud_agent`.
8. Documentar qué campos divergen en el evento de auditoría.

## Notes

- Distancia de Levenshtein: `pip install python-Levenshtein`.
- Pequeñas diferencias pueden ser errores OCR; el contexto de múltiples discrepancias es lo relevante.