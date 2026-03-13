---
name: xceptionnet_gan_detector
description: Clasificador de imágenes sintéticas generadas por GAN (XceptionNet/EfficientNet fine-tuned)
type: ML Model
priority: Recomendada
mode: Self-hosted
---

# xceptionnet_gan_detector

XceptionNet fine-tuned en FaceForensics++ clasifica frames como reales o sintéticos (generados por GAN/deepfake). Complementa al clasificador FaceForensics++ principal con un segundo modelo de diferente arquitectura para mayor robustez.

## When to use

Usar como segundo clasificador anti-deepfake en el `liveness_agent`. Ejecutar en paralelo con FaceForensics++ classifier para ensemble voting. Especialmente útil contra face swaps y reenactment.

## Instructions

1. Descargar pesos pre-entrenados de XceptionNet en FaceForensics++.
2. Exportar a ONNX: `torch.onnx.export(model, dummy_input, 'xceptionnet_ff.onnx')`.
3. Input: face crop de 299x299 normalizado a [-1, 1].
4. Output: `[real_prob, fake_prob]` — usar `fake_prob` como score de deepfake.
5. Umbral: `fake_prob > 0.6` marca como sospechoso de deepfake.
6. Ensemble con FaceForensics++ classifier: `final_score = 0.5 * xception_score + 0.5 * ff_score`.
7. Registrar ambos scores individuales en auditoría para análisis posterior.

## Notes

- XceptionNet tiene ~23M parámetros; latencia ~80ms en GPU.
- EfficientNet-B4 es alternativa más ligera si el hardware es limitado.
- Re-entrenar periódicamente con nuevos ejemplos de deepfakes para mantener la eficacia.