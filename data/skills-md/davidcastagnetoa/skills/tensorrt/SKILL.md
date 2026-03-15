---
name: tensorrt
description: Compilación y optimización de modelos con TensorRT para máximo rendimiento en GPU NVIDIA
type: Tool
priority: Esencial
mode: Self-hosted
---

# tensorrt

Skill para compilar y optimizar los modelos ML del pipeline de verificación KYC usando NVIDIA TensorRT como compilador de deep learning. TensorRT transforma modelos entrenados en engines optimizados con fusión de capas, cuantización, selección de kernels y calibración, logrando latencias mínimas en GPUs NVIDIA. Esta skill se centra exclusivamente en TensorRT como herramienta de compilación, separada de onnx_runtime_standalone (runtime alternativo) y triton_inference_server (servidor de modelos).

## When to use

Usar esta skill cuando el **model_server_agent** necesite compilar modelos a formato TensorRT engine (.plan) para producción, optimizar la latencia de inferencia de modelos faciales o de liveness, o configurar cuantización INT8/FP16 para los modelos del pipeline KYC. Aplica al preparar modelos para despliegue en Triton o como engines standalone.

## Instructions

1. Convertir el modelo ArcFace de PyTorch a ONNX como paso intermedio hacia TensorRT:
   ```python
   import torch

   model = load_arcface_model("arcface_r100.pth")
   model.eval()

   dummy_input = torch.randn(1, 3, 112, 112).cuda()
   torch.onnx.export(
       model, dummy_input, "arcface.onnx",
       input_names=["input"],
       output_names=["embedding"],
       dynamic_axes={"input": {0: "batch_size"}, "embedding": {0: "batch_size"}},
       opset_version=17
   )
   ```

2. Compilar el modelo ONNX a TensorRT engine usando trtexec con perfiles de optimización:
   ```bash
   trtexec \
     --onnx=arcface.onnx \
     --saveEngine=arcface_fp16.plan \
     --fp16 \
     --minShapes=input:1x3x112x112 \
     --optShapes=input:8x3x112x112 \
     --maxShapes=input:32x3x112x112 \
     --workspace=4096 \
     --verbose
   ```

3. Compilar con cuantización INT8 para máximo throughput usando calibración:
   ```python
   import tensorrt as trt

   calibrator = trt.IInt8EntropyCalibrator2(
       calibration_data_loader,   # Dataset representativo de rostros
       cache_file="arcface_int8_calib.cache"
   )

   config.set_flag(trt.BuilderFlag.INT8)
   config.int8_calibrator = calibrator
   ```

4. Generar el dataset de calibración INT8 con imágenes representativas del pipeline KYC:
   ```python
   # Usar distribución real de imágenes: selfies variadas en iluminación,
   # etnias, edades y fotos de documentos
   CALIBRATION_IMAGES = 1000  # Mínimo recomendado
   calibration_set = load_representative_faces(
       selfies=500,
       document_photos=500,
       diverse_demographics=True
   )
   ```

5. Validar la precisión del engine compilado contra el modelo original:
   ```python
   import numpy as np

   # Comparar embeddings entre modelo original y TensorRT
   original_embedding = original_model(test_face)
   trt_embedding = trt_engine(test_face)

   cosine_sim = np.dot(original_embedding, trt_embedding) / (
       np.linalg.norm(original_embedding) * np.linalg.norm(trt_embedding)
   )
   assert cosine_sim > 0.999, f"Degradación inaceptable: {cosine_sim}"
   ```

6. Compilar todos los modelos del pipeline con configuraciones optimizadas por modelo:
   ```bash
   # Liveness model - latencia crítica, FP16
   trtexec --onnx=liveness.onnx --saveEngine=liveness_fp16.plan --fp16 \
     --minShapes=input:1x3x224x224 --optShapes=input:4x3x224x224 --maxShapes=input:8x3x224x224

   # OCR detection - puede tolerar INT8
   trtexec --onnx=ocr_det.onnx --saveEngine=ocr_det_int8.plan --int8 --fp16 \
     --calib=ocr_calib.cache \
     --minShapes=input:1x3x640x640 --optShapes=input:1x3x640x640 --maxShapes=input:4x3x640x640
   ```

7. Benchmark del engine compilado para verificar que cumple SLA de latencia:
   ```bash
   trtexec --loadEngine=arcface_fp16.plan \
     --shapes=input:1x3x112x112 \
     --iterations=1000 \
     --warmUp=500 \
     --duration=10
   # Verificar: P99 latency < 300ms para face_match
   ```

## Notes

- Los engines TensorRT (.plan) son especificos de la arquitectura GPU en la que se compilan (e.g., un engine compilado en A100 no funciona en T4). Compilar engines para cada tipo de GPU del cluster y versionar junto con la GPU target.
- La cuantización INT8 puede degradar ligeramente la precisión del face_match; siempre validar que el cosine similarity entre embeddings original y cuantizado sea > 0.999 y que FAR/FRR se mantengan dentro de los objetivos del sistema.
- Usar dynamic shapes (min/opt/max) en lugar de shapes fijas para soportar el dynamic batching de Triton. El optShapes debe coincidir con el preferred_batch_size configurado en Triton.
