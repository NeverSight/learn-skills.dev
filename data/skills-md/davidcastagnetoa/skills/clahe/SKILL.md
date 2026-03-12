---
name: clahe
description: Normalización adaptativa de histograma (CLAHE) para mejorar legibilidad del texto del documento
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# clahe

CLAHE (Contrast Limited Adaptive Histogram Equalization) mejora el contraste local del documento, haciendo el texto más legible para OCR sin sobre-amplificar el ruido.

## When to use

Aplicar después de la corrección de perspectiva, antes de OCR y face extraction.

## Instructions

1. Convertir imagen a espacio LAB: `lab = cv2.cvtColor(warped, cv2.COLOR_BGR2LAB)`.
2. Extraer canal L: `l, a, b = cv2.split(lab)`.
3. Aplicar CLAHE al canal L: `clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))`. `l_enhanced = clahe.apply(l)`.
4. Reconstruir imagen: `enhanced = cv2.merge([l_enhanced, a, b])`. `result = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)`.
5. Para OCR, convertir adicionalmente a escala de grises y binarizar con Otsu: `_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)`.

## Notes

- `clipLimit=2.0` evita sobre-amplificación de ruido; ajustar si el documento tiene sombras severas.
- `tileGridSize=(8,8)` funciona bien para documentos A4/ID-1; ajustar para otros tamaños.