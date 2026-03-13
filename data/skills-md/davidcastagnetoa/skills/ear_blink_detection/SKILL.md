---
name: ear_blink_detection
description: Detectar parpadeo natural midiendo Eye Aspect Ratio (EAR) frame a frame con landmarks faciales
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# ear_blink_detection

El Eye Aspect Ratio (EAR) mide la apertura del ojo usando 6 landmarks faciales. Un parpadeo natural produce una caída rápida y recuperación del EAR. Las fotos no parpadean.

## When to use

Usar como challenge principal de liveness activo: solicitar al usuario que parpadee 2 veces en 5 segundos.

## Instructions

1. Extraer landmarks del ojo usando MediaPipe Face Mesh.
2. Para el ojo izquierdo usar landmarks: [33, 160, 158, 133, 153, 144].
3. Calcular EAR: `EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)`.
4. Umbral de parpadeo: `EAR_THRESHOLD = 0.25` (ojo cerrado si EAR < threshold).
5. Detectar secuencia: EAR normal → cae por debajo del umbral → recupera → cuenta como 1 parpadeo.
6. Requerir mínimo 2 parpadeos en ventana de 5 segundos.
7. Validar velocidad del parpadeo: un parpadeo natural dura 150-400ms; más rápido o más lento es sospechoso.

## Notes

- Fórmula original: Soukupová & Čech (2016) "Real-Time Eye Blink Detection using Facial Landmarks".
- `EAR_THRESHOLD` puede necesitar calibración por etnia/edad; considerar threshold adaptativo.