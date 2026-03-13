---
name: faceforensics_classifier
description: Clasificador de deepfakes y face swaps entrenado en el dataset FaceForensics++
type: ML Model
priority: Esencial
mode: Self-hosted
---

# faceforensics_classifier

Modelo de clasificación binaria (real/fake) entrenado en FaceForensics++ para detectar deepfakes, face swaps (DeepFaceLab, FaceSwap) y GAN-generated faces en el video de selfie.

## When to use

Ejecutar sobre los frames del video de selfie como capa de detección de deepfakes, después de liveness pasivo y antes de la decisión final.

## Instructions

1. Descargar modelos preentrenados de FaceForensics++: https://github.com/ondyari/FaceForensics
2. Modelo recomendado: XceptionNet entrenado en c23 (calidad media): `xception_c23.pkl`.
3. Preprocesar: detectar y recortar cara, redimensionar a 299x299, normalizar a [-1, 1].
4. Inferencia: `pred = model(preprocessed_face)` → score de probabilidad de ser fake.
5. Umbral de rechazo: `fake_score > 0.5` → posible deepfake, incrementar flag antifraude.
6. Analizar múltiples frames (mínimo 5) y promediar scores para reducir falsos positivos.
7. Exportar a ONNX y desplegar en Triton para latencia óptima.

## Notes

- Repositorio oficial: https://github.com/ondyari/FaceForensics
- El modelo c40 (alta compresión) es más robusto ante videos comprimidos por WebRTC.
- Fine-tuning con DeepFaceLab y Face2Face mejora significativamente la detección de ataques actuales.