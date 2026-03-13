---
name: midas_depth_estimation
description: Estimación de profundidad facial para verificar volumen real (3D) con modelo monocular MiDaS
type: ML Model
priority: Recomendada
mode: Self-hosted
---

# midas_depth_estimation

MiDaS (Monocular Depth Estimation) estima un mapa de profundidad a partir de una sola imagen RGB. Permite distinguir entre un rostro real 3D y una foto plana (impresa o en pantalla) analizando la variación de profundidad.

## When to use

Usar como capa adicional de liveness pasivo en el `liveness_agent`. Complementa a MiniFASNet y Silent-Face para detectar ataques con fotos impresas o pantallas que no tienen variación de profundidad.

## Instructions

1. Instalar: `pip install timm torch torchvision`.
2. Descargar modelo MiDaS v3.1 small: `torch.hub.load('intel-isl/MiDaS', 'MiDaS_small')`.
3. Preprocesar frame: resize a 256x256, normalizar con transforms de MiDaS.
4. Inferir mapa de profundidad: `depth_map = model(input_tensor)`.
5. Recortar la región del rostro del mapa de profundidad usando bounding box de face detection.
6. Calcular la varianza de profundidad en la región facial: `depth_variance = np.var(face_depth)`.
7. Umbral: si `depth_variance < 0.05`, clasificar como posible ataque plano (foto/pantalla).
8. Registrar `depth_variance` en el evento de auditoría.

## Notes

- MiDaS small es suficiente para liveness (~50ms en GPU); no usar el modelo large en producción.
- La estimación monocular no reemplaza a una cámara de profundidad real, pero detecta ataques obvios.
- Combinar con análisis de textura (LBP/Fourier) para mayor robustez.