---
name: lbp_fourier_texture
description: Análisis de micro-textura mediante LBP y Fourier para detectar patrones de papel o píxel de pantalla
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# lbp_fourier_texture

Local Binary Patterns (LBP) y el análisis de frecuencias de Fourier detectan las micro-texturas características de materiales falsos: granos de papel en fotos impresas, patrones de subpíxel en pantallas.

## When to use

Usar como capa adicional de liveness pasivo, especialmente para detectar ataques de impresión de alta calidad que engañan a los modelos CNN.

## Instructions

1. Instalar: `pip install scikit-image`.
2. **LBP**: Extraer región facial. Calcular LBP: `lbp = local_binary_pattern(gray_face, P=8, R=1, method='uniform')`. Calcular histograma LBP normalizado. Clasificar con SVM o threshold estadístico preentrenado.
3. **Análisis Fourier**: Aplicar FFT 2D: `f = np.fft.fft2(gray_face)`. Calcular espectro de magnitud: `magnitude = np.abs(np.fft.fftshift(f))`. Analizar distribución de energía en frecuencias altas (pantallas muestran picos periódicos regulares en Fourier).
4. Combinar score LBP y score Fourier con media ponderada.
5. Umbral de rechazo: `combined_score < 0.5` → spoof detectado.

## Notes

- Los patrones de pantalla (LCD/OLED) crean frecuencias periódicas muy características en el espectro de Fourier.
- LBP es especialmente sensible a texturas de papel de baja resolución.