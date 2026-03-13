---
name: histogram_analysis
description: Detectar sobreexposición, subexposición e iluminación desigual en frames capturados
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# histogram_analysis

El análisis del histograma de luminosidad detecta imágenes con iluminación deficiente que comprometerían la calidad del liveness y face match.

## When to use

Aplicar junto con laplacian_variance en el pipeline de validación de calidad de cada frame.

## Instructions

1. Convertir a HSV: `hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)`
2. Extraer canal V: `v_channel = hsv[:,:,2]`
3. Percentiles: `p5 = np.percentile(v_channel, 5)`, `p95 = np.percentile(v_channel, 95)`
4. Sobreexposición: si >10% píxeles con V>250 → `OVEREXPOSED`.
5. Subexposición: si >10% píxeles con V<20 → `UNDEREXPOSED`.
6. Devolver `{ quality_issues: [], brightness_mean: float, contrast_score: float }`.

## Notes

- Proporcionar feedback en tiempo real: "Mejora la iluminación", "Reduce el brillo".
- Iluminación artificialmente perfecta puede indicar spoofing de pantalla.