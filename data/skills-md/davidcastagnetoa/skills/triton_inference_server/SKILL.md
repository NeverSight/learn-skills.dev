---
name: triton_inference_server
description: Servidor de modelos production-grade con soporte TensorRT, ONNX y PyTorch en GPU
type: Tool
priority: Esencial
mode: Self-hosted
---

# triton_inference_server

NVIDIA Triton Inference Server centraliza el serving de todos los modelos ML del pipeline con optimización GPU, dynamic batching y múltiples frameworks soportados simultáneamente.

## When to use

Usar para servir en producción todos los modelos ML: MiniFASNet, ArcFace, YOLOv8, PaddleOCR, FaceForensics classifier.

## Instructions

1. Lanzar con Docker: `docker run --gpus all -p 8000:8000 -p 8001:8001 -p 8002:8002 -v /models:/models nvcr.io/nvidia/tritonserver:23.10-py3`.
2. Estructurar repositorio de modelos: `models/{model_name}/{version}/model.onnx` + `config.pbtxt`.
3. Configurar `config.pbtxt` para cada modelo: input/output shapes, instance groups (GPU/CPU), dynamic batching.
4. Exportar modelos a ONNX antes de desplegar: `torch.onnx.export(...)`.
5. Aplicar TensorRT optimization donde sea posible (ver skill `tensorrt`).
6. Usar el cliente gRPC para inferencia: `pip install tritonclient[grpc]`.
7. Health check: `GET http://triton:8000/v2/health/ready`.

## Notes

- Documentación: https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/
- Para entornos sin GPU NVIDIA: usar TorchServe como alternativa.
- Monitorizar GPU utilization con Prometheus GPU exporter.