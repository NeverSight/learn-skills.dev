---
name: ela_analysis
description: Error Level Analysis (ELA) para detectar manipulación digital del documento por inconsistencias de compresión JPEG
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# ela_analysis

ELA detecta manipulaciones digitales en imágenes JPEG analizando inconsistencias en los niveles de error de compresión. Las regiones editadas muestran niveles de error diferentes al resto de la imagen.

## When to use

Aplicar sobre la imagen del documento después de la corrección de perspectiva para detectar alteraciones (foto pegada, texto modificado, datos falsificados).

## Instructions

1. Instalar: `pip install pillow`.
2. Guardar imagen con calidad conocida: `img.save('temp_ela.jpg', 'JPEG', quality=90)`.
3. Recargar imagen guardada: `recompressed = Image.open('temp_ela.jpg')`.
4. Calcular diferencia: `ela_img = ImageChops.difference(original, recompressed)`.
5. Amplificar diferencias: multiplicar píxeles de `ela_img` por factor (ej. 20).
6. Analizar mapa ELA: regiones uniformes con error alto = posible manipulación.
7. Calcular estadísticas por región del documento (foto, texto, fondo) y detectar outliers.
8. Generar score de integridad: `integrity_score = 1 - (anomaly_regions / total_regions)`.

## Notes

- La imagen debe ser JPEG; para PNG convertir primero.
- Una imagen enteramente regenerada (falsa de principio a fin) puede pasar ELA; combinar con Copy-Move detection.
- La calidad de recompresión (90) debe ser fija y documentada.