---
name: dynamic_batching_triton
description: Batching dinámico en Triton Inference Server para maximizar throughput GPU en inferencia facial
type: Algorithm
priority: Recomendada
mode: Self-hosted
---

# dynamic_batching_triton

Skill para configurar y optimizar el dynamic batching nativo de NVIDIA Triton Inference Server, agrupando requests de inferencia facial, liveness y OCR en batches óptimos para maximizar el throughput GPU. A diferencia del batching genérico a nivel aplicación, esta skill se centra en la configuración específica de Triton y sus parámetros de scheduling para el pipeline de verificación KYC.

## When to use

Usar esta skill cuando el **model_server_agent** necesite configurar, tunear o diagnosticar el dynamic batching dentro de Triton Inference Server. Aplica al desplegar nuevos modelos en Triton, optimizar latencia vs throughput, o resolver problemas de scheduling en modelos del pipeline KYC. Esta skill es complementaria a triton_inference_server (que cubre el servidor completo) y separada de dynamic_batching genérico.

## Instructions

1. Habilitar dynamic batching en el model config de Triton para cada modelo del pipeline:

   ```protobuf
   # model_repository/arcface/config.pbtxt
   name: "arcface"
   platform: "onnxruntime_onnx"
   max_batch_size: 32
   dynamic_batching {
     preferred_batch_size: [8, 16, 32]
     max_queue_delay_microseconds: 100000  # 100ms max wait
   }
   input [{
     name: "input"
     data_type: TYPE_FP32
     dims: [3, 112, 112]
   }]
   ```

2. Configurar parámetros de batching diferenciados por modelo según su perfil de latencia:

   ```protobuf
   # Liveness model - latencia crítica, batches pequeños
   dynamic_batching {
     preferred_batch_size: [4, 8]
     max_queue_delay_microseconds: 50000  # 50ms - más agresivo
   }

   # OCR model - tolerante a latencia, batches grandes
   dynamic_batching {
     preferred_batch_size: [16, 32, 64]
     max_queue_delay_microseconds: 200000  # 200ms
   }
   ```

3. Configurar prioridades de scheduling para que liveness (crítico en UX) tenga prioridad sobre OCR:

   ```protobuf
   dynamic_batching {
     priority_levels: 3
     default_priority_level: 2
     default_queue_policy {
       timeout_action: REJECT
       default_timeout_microseconds: 500000
     }
   }
   ```

4. Habilitar métricas de batching en Triton para monitorizar la efectividad:

   ```bash
   # Arrancar Triton con métricas habilitadas
   tritonserver --model-repository=/models \
     --metrics-port=8002 \
     --allow-metrics=true \
     --metrics-interval-ms=1000
   ```

5. Monitorizar métricas clave de batching via Prometheus endpoint:

   ```
   nv_inference_request_success       # Requests exitosas
   nv_inference_queue_duration_us     # Tiempo en cola
   nv_inference_compute_infer_duration_us  # Tiempo de inferencia
   nv_inference_exec_count            # Batches ejecutados
   nv_inference_request_duration_us   # Duración total
   ```

6. Tunear el max_queue_delay basándose en el SLA de 8 segundos totales del pipeline:

   ```python
   # Budget de latencia por modelo dentro del SLA de 8s
   LATENCY_BUDGET_MS = {
       "liveness": 500,      # Máx 500ms
       "arcface": 300,       # Máx 300ms
       "paddleocr": 1000,    # Máx 1000ms
       "antifraud": 200,     # Máx 200ms
   }
   # max_queue_delay = budget * 0.3 (30% del budget para queueing)
   ```

7. Configurar sequence batching para modelos que procesan múltiples frames (liveness con secuencia de frames):
   ```protobuf
   sequence_batching {
     max_sequence_idle_microseconds: 5000000
     control_input [{
       name: "START"
       control [{ kind: CONTROL_SEQUENCE_START }]
     }]
   }
   ```

## Notes

- El dynamic batching de Triton opera a nivel de inference server, no de aplicación. Esto es más eficiente que batching manual porque Triton conoce el estado exacto de la GPU y puede optimizar la ejecución de kernels CUDA.
- El parámetro max_queue_delay es el trade-off principal: valores altos mejoran throughput pero aumentan latencia. Para el pipeline KYC con SLA de 8s, mantener delays conservadores en modelos de la ruta crítica (liveness, face_match).
- Sequence batching es necesario para el módulo de liveness que analiza múltiples frames consecutivos; no confundir con dynamic batching que agrupa requests independientes.
