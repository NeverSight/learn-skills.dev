---
name: onnx_runtime_standalone
description: ONNX Runtime como runtime independiente de inferencia, alternativa ligera a Triton para deployments simples
type: Library
priority: Esencial
mode: Self-hosted
---

# onnx_runtime_standalone

Skill para desplegar y gestionar ONNX Runtime como runtime de inferencia independiente para los modelos del pipeline de verificación KYC. ONNX Runtime ofrece una alternativa ligera a Triton Inference Server para escenarios de deployment más simples, edge computing o entornos donde no se dispone de infraestructura GPU enterprise. Soporta ejecución en CPU y GPU con providers intercambiables (CUDA, TensorRT, OpenVINO, DirectML).

## When to use

Usar esta skill cuando el **model_server_agent** necesite desplegar modelos del pipeline KYC sin la complejidad de Triton, en entornos con recursos limitados, deployments edge o single-node. Aplica como alternativa ligera para ambientes de staging, demos, o cuando se requiere inferencia en CPU. Esta skill es independiente de triton_inference_server y tensorrt.

## Instructions

1. Instalar ONNX Runtime con el execution provider adecuado para el entorno:
   ```bash
   # GPU con CUDA
   pip install onnxruntime-gpu==1.18.0

   # CPU only (deployments ligeros)
   pip install onnxruntime==1.18.0

   # Con TensorRT provider (máximo rendimiento GPU sin Triton)
   pip install onnxruntime-gpu --extra-index-url https://aiinfra.pkgs.visualstudio.com/PublicPackages/_packaging/onnxruntime-cuda-12/pypi/simple/
   ```

2. Crear la clase de inferencia para el modelo ArcFace con session pooling:
   ```python
   import onnxruntime as ort
   import numpy as np

   class ArcFaceInference:
       def __init__(self, model_path: str, device: str = "cuda"):
           providers = ["CUDAExecutionProvider", "CPUExecutionProvider"] if device == "cuda" \
               else ["CPUExecutionProvider"]

           sess_options = ort.SessionOptions()
           sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
           sess_options.intra_op_num_threads = 4
           sess_options.execution_mode = ort.ExecutionMode.ORT_PARALLEL

           self.session = ort.InferenceSession(
               model_path, sess_options=sess_options, providers=providers
           )

       def get_embedding(self, face_image: np.ndarray) -> np.ndarray:
           input_name = self.session.get_inputs()[0].name
           result = self.session.run(None, {input_name: face_image})
           return result[0]
   ```

3. Configurar el pipeline completo de verificación con todos los modelos en ONNX Runtime:
   ```python
   class KYCInferencePipeline:
       def __init__(self, models_dir: str, device: str = "cuda"):
           self.face_model = ArcFaceInference(f"{models_dir}/arcface.onnx", device)
           self.liveness_model = LivenessInference(f"{models_dir}/liveness.onnx", device)
           self.ocr_det_model = OCRDetInference(f"{models_dir}/ocr_det.onnx", device)
           self.ocr_rec_model = OCRRecInference(f"{models_dir}/ocr_rec.onnx", device)

       def verify(self, selfie: np.ndarray, document: np.ndarray) -> dict:
           liveness_score = self.liveness_model.predict(selfie)
           selfie_embedding = self.face_model.get_embedding(selfie)
           doc_embedding = self.face_model.get_embedding(document)
           similarity = cosine_similarity(selfie_embedding, doc_embedding)
           return {"liveness": liveness_score, "match_score": similarity}
   ```

4. Optimizar el modelo ONNX antes de despliegue con optimizaciones de grafo:
   ```python
   import onnxruntime as ort

   # Optimizar y guardar modelo transformado
   sess_options = ort.SessionOptions()
   sess_options.optimized_model_filepath = "arcface_optimized.onnx"
   sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

   # La sesión optimiza al construirse
   ort.InferenceSession("arcface.onnx", sess_options)
   ```

5. Configurar ONNX Runtime con TensorRT execution provider para rendimiento cercano a TensorRT nativo:
   ```python
   providers = [
       ("TensorrtExecutionProvider", {
           "trt_max_workspace_size": 4 * 1024 * 1024 * 1024,  # 4GB
           "trt_fp16_enable": True,
           "trt_engine_cache_enable": True,
           "trt_engine_cache_path": "/cache/trt_engines/",
           "trt_max_partition_iterations": 1000,
       }),
       ("CUDAExecutionProvider", {
           "device_id": 0,
           "arena_extend_strategy": "kNextPowerOfTwo",
           "gpu_mem_limit": 4 * 1024 * 1024 * 1024,  # 4GB limit
       }),
       "CPUExecutionProvider"
   ]
   session = ort.InferenceSession("arcface.onnx", providers=providers)
   ```

6. Implementar wrapper FastAPI para servir los modelos como microservicio:
   ```python
   from fastapi import FastAPI, UploadFile
   import uvicorn

   app = FastAPI()
   pipeline = KYCInferencePipeline("/opt/models", device="cuda")

   @app.post("/v1/verify")
   async def verify(selfie: UploadFile, document: UploadFile):
       selfie_arr = preprocess_image(await selfie.read())
       doc_arr = preprocess_image(await document.read())
       return pipeline.verify(selfie_arr, doc_arr)

   # uvicorn main:app --host 0.0.0.0 --port 8080 --workers 2
   ```

7. Configurar IO binding para reducir copias CPU-GPU cuando se usa CUDA provider:
   ```python
   io_binding = session.io_binding()
   io_binding.bind_input("input", "cuda", 0, np.float32, [1, 3, 112, 112], input_tensor.data_ptr())
   io_binding.bind_output("embedding", "cuda")
   session.run_with_iobinding(io_binding)
   embedding = io_binding.copy_outputs_to_cpu()[0]
   ```

## Notes

- ONNX Runtime es ideal como alternativa a Triton para deployments single-node o cuando el equipo no necesita las capacidades enterprise de Triton (model ensembles, multi-GPU scheduling). Para producción a escala, considerar migrar a Triton.
- El fallback de providers (TensorRT -> CUDA -> CPU) permite que el mismo codigo funcione en diferentes entornos sin modificaciones, lo cual es util para mantener paridad entre desarrollo local y produccion.
- Las sesiones de ONNX Runtime son thread-safe para inferencia concurrente pero no para carga de modelo. Crear las sesiones al inicio y reutilizarlas; no crear sesiones por request ya que la carga del modelo es costosa.
