---
name: compression_artifact_analysis
description: Detectar artefactos de recompresión típicos de deepfakes y manipulaciones
type: Algorithm
priority: Recomendada
mode: Self-hosted
---

# compression_artifact_analysis

Analiza los artefactos de compresión JPEG en la imagen para detectar recompresiones múltiples típicas de imágenes manipuladas o deepfakes. Las zonas editadas muestran niveles de compresión inconsistentes con el resto de la imagen.

## When to use

Usar en el `liveness_agent` como señal complementaria anti-deepfake. Los deepfakes suelen recomprimirse varias veces al procesarse, dejando artefactos detectables en el dominio de frecuencia.

## Instructions

1. Convertir frame a escala de grises.
2. Aplicar DCT (Discrete Cosine Transform) por bloques de 8x8 píxeles.
3. Analizar la distribución de coeficientes DCT: buscar patrones de doble cuantización.
4. Calcular el histograma de coeficientes AC: picos periódicos indican recompresión.
5. Usar `cv2.dct()` para la transformación y `numpy` para el análisis estadístico.
6. Score: `compression_anomaly_score` entre 0 (normal) y 1 (alta sospecha de recompresión).
7. Umbral: `score > 0.7` indica probable manipulación.

## Notes

- Este análisis solo aplica a imágenes JPEG; frames capturados en vivo desde cámara suelen ser RAW/YUV.
- Más útil para detectar documentos manipulados que para liveness de selfie.
- Combinar con ELA (Error Level Analysis) del `document_processor_agent` para mayor cobertura.