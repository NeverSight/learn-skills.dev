---
name: laplacian_variance
description: Medición de nitidez de imagen para rechazar capturas borrosas antes del análisis
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# laplacian_variance

La varianza del Laplaciano mide la nitidez de una imagen. Una imagen borrosa tiene varianza baja. Usar como filtro de calidad previo a los modelos ML.

## When to use

Aplicar a cada frame capturado antes de enviarlo al liveness_agent o document_processor_agent.

## Instructions

1. `pip install opencv-python-headless`
2. `gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)`
3. `laplacian = cv2.Laplacian(gray, cv2.CV_64F)`
4. `variance = laplacian.var()`
5. Umbral: `BLUR_THRESHOLD = 100.0`. Si `variance < threshold`: rechazar.
6. Incluir el score de nitidez en el evento de auditoría.

## Notes

- El umbral depende de la resolución; calibrar con imágenes de referencia.
- Complementar con histogram_analysis para detección de calidad completa.