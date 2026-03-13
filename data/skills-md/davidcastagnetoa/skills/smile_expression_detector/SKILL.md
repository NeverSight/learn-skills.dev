---
name: smile_expression_detector
description: Verificar expresiones faciales (sonrisa) en el desafío de liveness activo
type: ML Model
priority: Recomendada
mode: Self-hosted
---

# smile_expression_detector

Detector de sonrisa y expresiones faciales basado en landmarks de Mediapipe Face Mesh. Calcula ratios geométricos entre puntos de la boca para determinar si el usuario está sonriendo como parte del challenge-response de liveness activo.

## When to use

Usar en el `liveness_agent` durante los desafíos activos cuando el sistema pide al usuario que sonría. Es uno de los posibles challenges aleatorios junto con parpadeo y giro de cabeza.

## Instructions

1. Obtener landmarks faciales de Mediapipe Face Mesh (468 puntos).
2. Extraer landmarks de la boca: puntos 61, 291 (comisuras), 13, 14 (labios superior/inferior).
3. Calcular Mouth Aspect Ratio (MAR): distancia vertical / distancia horizontal de la boca.
4. Calcular Smile Ratio: distancia entre comisuras / distancia entre ojos.
5. Umbral de sonrisa: `smile_ratio > 0.45` y `MAR > 0.3` indica sonrisa.
6. Verificar que la sonrisa se mantiene durante al menos 0.5 segundos (15 frames a 30fps).
7. Registrar `smile_score` y `duration_ms` en el evento de auditoría.

## Notes

- No usar modelos pesados de expresión facial; los ratios geométricos con Mediapipe son suficientes y rápidos (<5ms).
- Asegurar que el challenge de sonrisa se selecciona aleatoriamente para evitar ataques de replay.
- Combinado con EAR (parpadeo) y head pose (giro), forma el conjunto completo de challenges activos.