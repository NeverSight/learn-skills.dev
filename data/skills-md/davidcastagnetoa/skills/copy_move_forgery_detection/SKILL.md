---
name: copy_move_forgery_detection
description: Detectar regiones clonadas dentro del documento — foto pegada sobre otra foto o texto duplicado
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# copy_move_forgery_detection

Copy-Move Forgery Detection identifica regiones del documento copiadas y pegadas desde otra parte de la misma imagen, revelando manipulaciones como foto del titular pegada o número de documento clonado.

## When to use

Aplicar junto con ELA como parte del pipeline de integridad del documento.

## Instructions

1. Instalar: `pip install opencv-contrib-python-headless` (necesario para SIFT).
2. Implementar detección por SIFT keypoints:
   ```python
   import cv2, numpy as np
   def detect_copy_move(img, min_matches=10):
       gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
       sift = cv2.SIFT_create()
       keypoints, descriptors = sift.detectAndCompute(gray, None)
       if descriptors is None or len(keypoints) < min_matches:
           return {"copy_move_detected": False, "confidence": 0.0}
       bf = cv2.BFMatcher(cv2.NORM_L2)
       matches = bf.knnMatch(descriptors, descriptors, k=3)
       MIN_DIST_PIXELS = 50
       suspicious = []
       for m in matches:
           if len(m) >= 2:
               best, second = m[0], m[1]
               if best.queryIdx != best.trainIdx:
                   pt1 = keypoints[best.queryIdx].pt
                   pt2 = keypoints[best.trainIdx].pt
                   dist = np.linalg.norm(np.array(pt1) - np.array(pt2))
                   if dist > MIN_DIST_PIXELS and best.distance < 0.75 * second.distance:
                       suspicious.append((pt1, pt2))
       detected = len(suspicious) >= min_matches
       confidence = min(len(suspicious) / (min_matches * 3), 1.0)
       return {"copy_move_detected": detected, "confidence": float(confidence)}
   ```
3. Umbral: `match_count >= 10` con `confidence > 0.3` → flag `COPY_MOVE_DETECTED`.
4. Combinar con ELA: si ambos detectan anomalías → alta confianza de manipulación.

## Notes

- Documentos con hologramas o patrones repetitivos pueden dar falsos positivos; calibrar `min_matches` por tipo de documento.
- ORB es más rápido pero menos preciso que SIFT.