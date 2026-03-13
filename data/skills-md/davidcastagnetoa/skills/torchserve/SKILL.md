---
name: torchserve
description: Servidor de modelos PyTorch para inferencia de modelos de verificación de identidad con batching y versionado
type: Tool
priority: Recomendada
mode: Self-hosted
---

# torchserve

Configura y despliega TorchServe como servidor de modelos PyTorch para servir los modelos de liveness detection (MiniFASNet), face recognition (ArcFace) y anti-spoofing del pipeline KYC. Proporciona batching dinámico, versionado de modelos y métricas de rendimiento integradas para monitoreo en producción.

## When to use

Usa esta skill cuando necesites desplegar o configurar el servidor de inferencia PyTorch dentro del **model_server_agent**. Aplica cuando se requiera servir modelos ML del pipeline de verificación facial con soporte para batching, múltiples versiones simultáneas y endpoints de métricas.

## Instructions

1. Instalar TorchServe y sus dependencias:

   ```bash
   pip install torchserve torch-model-archiver torch-workflow-archiver
   ```

2. Empaquetar cada modelo como un MAR (Model Archive) usando `torch-model-archiver`:

   ```bash
   torch-model-archiver --model-name arcface \
     --version 1.0 \
     --model-file models/arcface.py \
     --serialized-file weights/arcface_r100.pth \
     --handler handlers/face_recognition_handler.py \
     --export-path model_store/
   ```

3. Configurar el archivo `config.properties` con batching dinámico, número de workers y puertos:

   ```properties
   inference_address=http://0.0.0.0:8080
   management_address=http://0.0.0.0:8081
   metrics_address=http://0.0.0.0:8082
   job_queue_size=100
   batch_size=8
   max_batch_delay=200
   default_workers_per_model=2
   ```

4. Crear handlers personalizados para cada tipo de modelo (liveness, face_match, anti-spoofing) que implementen `initialize()`, `preprocess()`, `inference()` y `postprocess()`.

5. Iniciar TorchServe con el model store y la configuración:

   ```bash
   torchserve --start --model-store model_store/ \
     --ts-config config.properties \
     --models arcface=arcface.mar liveness=minifasnet.mar
   ```

6. Registrar nuevas versiones de modelos en caliente mediante la Management API:

   ```bash
   curl -X POST "http://localhost:8081/models?url=arcface_v2.mar&model_name=arcface&initial_workers=2"
   ```

7. Configurar métricas de Prometheus para monitorear latencia de inferencia, throughput y errores por modelo:

   ```properties
   metrics_mode=prometheus
   metrics_format=prometheus
   ```

8. Implementar health checks en el endpoint `/ping` y validar que todos los modelos estén cargados antes de aceptar tráfico de verificación.

## Notes

- El batching dinámico es crítico para optimizar el throughput cuando múltiples verificaciones KYC llegan simultáneamente; ajustar `batch_size` y `max_batch_delay` según la carga esperada.
- Cada modelo debe tener su propio handler para manejar correctamente el preprocesamiento específico (normalización facial, resize de documentos, etc.).
- Monitorear el uso de memoria GPU constantemente ya que cargar múltiples modelos (ArcFace + MiniFASNet + anti-spoofing) puede exceder la VRAM disponible.
