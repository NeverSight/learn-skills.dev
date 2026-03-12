---
name: head_pose_estimation
description: Calcular orientación (yaw/pitch/roll) de la cabeza para el challenge de giro de cabeza
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# head_pose_estimation

Estima los ángulos de orientación de la cabeza (yaw=izquierda/derecha, pitch=arriba/abajo, roll=inclinación) usando PnP (Perspective-n-Point) con landmarks de MediaPipe Face Mesh.

## When to use

Usar para el challenge de liveness activo "gira la cabeza a la derecha/izquierda" y para verificar que el rostro está frontal al inicio de la sesión.

## Instructions

1. Definir puntos 3D del modelo facial canónico (nariz, mentón, ojo izquierdo, ojo derecho, boca izquierda, boca derecha).
2. Extraer los landmarks 2D correspondientes del Face Mesh.
3. Resolver PnP: `success, rotation_vector, translation_vector = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs)`.
4. Convertir a ángulos de Euler: `rotation_matrix, _ = cv2.Rodrigues(rotation_vector)`.
5. Extraer yaw, pitch, roll de la matriz de rotación.
6. Challenge de giro: solicitar yaw > 30° hacia un lado aleatorio, verificar en máximo 3 segundos.
7. Aleatorizar la dirección del challenge (izquierda o derecha) en cada sesión.

## Notes

- La matrix de cámara puede estimarse de la resolución del frame: `focal_length = width; center = (width/2, height/2)`.
- Combinar con blink detection para un challenge multicapa más robusto.