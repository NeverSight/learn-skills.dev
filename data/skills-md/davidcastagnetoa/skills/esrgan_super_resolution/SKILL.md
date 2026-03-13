---
name: esrgan_super_resolution
description: Super-resolución de la foto del documento para mejorar calidad del face match cuando la foto es de baja resolución
type: ML Model
priority: Recomendada
mode: Self-hosted
---

# esrgan_super_resolution

ESRGAN (Enhanced Super-Resolution GAN) aumenta la resolución de la foto del documento ×4, mejorando significativamente la calidad del face match en documentos con fotos de baja resolución o antiguas.

## When to use

Aplicar cuando la foto extraída del documento tenga resolución menor a 100×100 píxeles o calidad BRISQUE > 50.

## Instructions

1. Instalar Real-ESRGAN: `pip install realesrgan`.
2. Descargar modelo: `RealESRGAN_x4plus.pth` — https://github.com/xinntao/Real-ESRGAN.
3. Inicializar: `upsampler = RealESRGANer(scale=4, model_path='RealESRGAN_x4plus.pth', tile=0, tile_pad=10, pre_pad=0, half=True)`.
4. Aplicar: `output, _ = upsampler.enhance(face_crop, outscale=4)`.
5. Redimensionar resultado al tamaño esperado por ArcFace (112×112).
6. Usar solo cuando sea necesario para no añadir latencia innecesaria.

## Notes

- Repositorio: https://github.com/xinntao/Real-ESRGAN
- `half=True` usa FP16 en GPU, reduciendo memoria y aumentando velocidad.
- Benchmark: mejora el face match score ~0.05-0.15 en fotos de documentos de baja calidad.