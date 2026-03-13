---
name: deepface_framework
description: Wrapper que integra múltiples modelos faciales (ArcFace, FaceNet, VGG-Face, DeepID)
type: Library
priority: Recomendada
mode: Self-hosted
---

# deepface_framework

DeepFace es una librería Python que unifica múltiples modelos de reconocimiento facial bajo una API consistente. Permite cambiar entre ArcFace, FaceNet, VGG-Face y otros sin modificar el código del pipeline.

## When to use

Usar en el `face_match_agent` como capa de abstracción sobre los modelos faciales. Facilita el testing A/B entre modelos y proporciona un fallback automático si el modelo primario (ArcFace) falla.

## Instructions

1. Instalar: `pip install deepface`.
2. Verificar rostros: `result = DeepFace.verify(img1, img2, model_name='ArcFace')`.
3. Extraer embeddings: `embedding = DeepFace.represent(img, model_name='ArcFace')`.
4. Modelos disponibles: `ArcFace`, `Facenet512`, `VGG-Face`, `DeepID`, `SFace`.
5. Configurar modelo primario en config: `FACE_MODEL=ArcFace`.
6. Implementar fallback: si ArcFace falla, usar FaceNet automáticamente.
7. Comparar resultados entre modelos para validación cruzada en casos dudosos.

## Notes

- DeepFace descarga modelos automáticamente; pre-descargar en Docker build para producción.
- Para máximo rendimiento, usar InsightFace directamente en lugar de DeepFace wrapper.
- DeepFace incluye detector de rostros integrado; desactivar si ya se usa Mediapipe.