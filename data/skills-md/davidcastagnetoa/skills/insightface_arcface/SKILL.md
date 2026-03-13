---
name: insightface_arcface
description: Reconocimiento facial de estado del arte con ArcFace R100 para comparar selfie con foto del documento
type: ML Model
priority: Esencial
mode: Self-hosted
---

# insightface_arcface

InsightFace con el modelo ArcFace R100 es el estándar de facto en reconocimiento facial de alta precisión. Genera embeddings de 512 dimensiones que permiten comparar identidades con alta fiabilidad.

## When to use

Usar como modelo principal de face matching entre la selfie verificada y la foto extraída del documento.

## Instructions

1. Instalar: `pip install insightface onnxruntime-gpu`.
2. Inicializar: `app = FaceAnalysis(name='buffalo_l', providers=['CUDAExecutionProvider'])`. `app.prepare(ctx_id=0, det_size=(640, 640))`.
3. Detectar y extraer embedding de selfie: `faces = app.get(selfie_img)`. `selfie_embedding = faces[0].embedding`.
4. Detectar y extraer embedding de foto de documento (con ESRGAN si baja resolución).
5. Normalizar embeddings: `e1 = selfie_embedding / np.linalg.norm(selfie_embedding)`.
6. Calcular similitud coseno: `similarity = np.dot(e1, e2)`.
7. Umbral de aceptación: `similarity > 0.45` para ArcFace R100 (equivale a >85% en escala 0-1).
8. Exportar modelo a ONNX para Triton: `onnx_model` ya está incluido en InsightFace.

## Notes

- Repositorio oficial: https://github.com/deepinsight/insightface
- Modelos disponibles: `buffalo_l` (alta precisión), `buffalo_s` (más rápido, menor precisión).
- El umbral 0.45 tiene FAR < 0.001% en LFW benchmark; ajustar según requisitos del negocio.