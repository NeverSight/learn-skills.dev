---
name: font_consistency_analyzer
description: Detectar inconsistencias tipográficas que delaten edición del texto del documento
type: Algorithm
priority: Recomendada
mode: Self-hosted
---

# font_consistency_analyzer

Analiza la consistencia tipográfica del texto del documento de identidad para detectar campos editados digitalmente. Los documentos falsificados suelen tener inconsistencias en el grosor de trazo, espaciado entre caracteres y alineación de texto.

## When to use

Usar en el `document_processor_agent` como capa adicional de detección de falsificación. Ejecutar después del OCR para comparar las propiedades visuales de los caracteres extraídos.

## Instructions

1. Segmentar las regiones de texto del documento usando los bounding boxes del OCR.
2. Para cada campo de texto, calcular el stroke width promedio usando Stroke Width Transform (SWT).
3. Comparar el stroke width entre campos: desviación > 20% indica posible edición.
4. Analizar el espaciado inter-caracter (kerning) por campo con análisis de perfiles de proyección.
5. Verificar la alineación vertical de las líneas de texto usando regresión lineal.
6. Calcular `font_consistency_score`: promedio ponderado de consistencia de stroke, kerning y alineación.
7. Umbral: `score < 0.6` indica probable manipulación tipográfica.

## Notes

- Los documentos de baja resolución pueden dar falsos positivos; ajustar umbrales según calidad de imagen.
- Más efectivo en documentos con texto impreso; menos fiable en documentos con texto manuscrito.
- Combinar con ELA y Copy-Move Detection para un análisis de falsificación completo.