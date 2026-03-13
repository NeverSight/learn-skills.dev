---
name: easyocr
description: OCR alternativo a PaddleOCR, excelente en caracteres especiales y múltiples scripts
type: ML Model
priority: Recomendada
mode: Self-hosted
---

# easyocr

EasyOCR es un motor OCR basado en deep learning que soporta más de 80 idiomas y scripts. Funciona como alternativa/fallback a PaddleOCR con mejor rendimiento en caracteres especiales y alfabetos no latinos.

## When to use

Usar en el `ocr_agent` como segundo motor OCR cuando PaddleOCR tiene baja confianza (< 0.7) en la extracción. Especialmente útil para documentos con caracteres árabes, cirílicos o asiáticos.

## Instructions

1. Instalar: `pip install easyocr`.
2. Inicializar reader con idiomas: `reader = easyocr.Reader(['es', 'en', 'fr'], gpu=True)`.
3. Ejecutar OCR: `results = reader.readtext(image)`.
4. Cada resultado contiene: `[bbox, text, confidence]`.
5. Filtrar resultados con confianza < 0.5.
6. Comparar resultados con PaddleOCR y usar el de mayor confianza por campo.
7. Normalizar texto extraído con el `regex_data_normalizer`.

## Notes

- EasyOCR es más lento que PaddleOCR (~2x); usar solo como fallback.
- El modelo se descarga automáticamente la primera vez; pre-descargar en el Docker build.
- No soporta MRZ de forma nativa; usar `mrz_parser` para la zona MRZ.