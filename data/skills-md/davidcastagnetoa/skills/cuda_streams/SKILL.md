---
name: cuda_streams
description: Paralelismo GPU para ejecutar múltiples inferencias simultáneamente
type: Library
priority: Esencial
mode: Self-hosted
---

# cuda_streams

CUDA Streams permiten ejecutar múltiples operaciones GPU en paralelo (inferencia de modelos distintos, copia de datos y cómputo simultáneo), maximizando la utilización del hardware GPU.

## When to use

Usar en el `worker_pool_agent` para ejecutar inferencias de múltiples modelos en paralelo en la misma GPU: face_match + liveness + deepfake detection simultáneamente.

## Instructions

1. Crear streams por modelo:
   ```python
   stream_liveness = torch.cuda.Stream()
   stream_facematch = torch.cuda.Stream()
   ```
2. Ejecutar inferencias en paralelo:
   ```python
   with torch.cuda.stream(stream_liveness):
       liveness_result = liveness_model(frame)
   with torch.cuda.stream(stream_facematch):
       facematch_result = facematch_model(face_crop)
   ```
3. Sincronizar streams: `torch.cuda.synchronize()`.
4. Usar `torch.cuda.Event` para timing preciso de cada modelo.
5. Monitorizar VRAM: `torch.cuda.memory_allocated()`.
6. Limitar número de streams activos según VRAM disponible.

## Notes

- Los streams solo paralelizzan si hay recursos GPU suficientes; en GPU pequeñas pueden serializar.
- No usar más de 4-8 streams simultáneos; más allá el overhead supera el beneficio.
- Triton Inference Server gestiona streams automáticamente; preferir Triton si está disponible.