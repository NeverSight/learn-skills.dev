---
name: facenet_backup
description: Modelo de embeddings faciales alternativo a ArcFace para mayor resiliencia del pipeline
type: ML Model
priority: Recomendada
mode: Self-hosted
---

# facenet_backup

FaceNet (Google) genera embeddings de 128 o 512 dimensiones con buena generalización ante variaciones de pose e iluminación. Se usa como modelo de respaldo cuando ArcFace devuelve un score con baja confianza o como segunda opinión en casos borderline.

## When to use

Usar cuando el score de ArcFace cae en la zona gris (0.40-0.50) — ejecutar FaceNet como segunda opinión y promediar ambos scores. También usar como fallback si el servidor Triton del modelo ArcFace no está disponible.

## Instructions

1. Instalar via DeepFace (que incluye FaceNet): `pip install deepface`
2. O usar directamente `facenet-pytorch`: `pip install facenet-pytorch`
3. Con facenet-pytorch:
   ```python
   from facenet_pytorch import InceptionResnetV1
   import torch
   model = InceptionResnetV1(pretrained='vggface2').eval()
   def get_facenet_embedding(face_tensor: torch.Tensor) -> np.ndarray:
       with torch.no_grad():
           embedding = model(face_tensor.unsqueeze(0))
       return embedding.squeeze().numpy()
   ```
4. Normalizar el tensor de entrada: resize a (160, 160), normalizar a [-1, 1].
5. Comparar embeddings con cosine similarity — umbral de aprobación: 0.40 (FaceNet es menos discriminativo que ArcFace).
6. Estrategia de ensemble: `final_score = 0.7 * arcface_score + 0.3 * facenet_score` cuando ambos modelos están disponibles.

## Notes

- FaceNet VGGFace2 preentrenado tiene mejor cobertura de etnias que LFW — más robusto para KYC internacional.
- El modelo pesa ~100MB — puede cargarse en CPU para evitar competencia por VRAM con ArcFace.
- En producción, priorizar ArcFace R100 siempre — FaceNet es solo para enriquecer casos difíciles.