---
name: input_size_validation
description: Rechazo de payloads que excedan el tamaño máximo permitido para prevenir ataques DoS
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# input_size_validation

Sin límite de tamaño, un atacante puede enviar archivos de cientos de MB para saturar la memoria de los workers o el almacenamiento de MinIO. La validación de tamaño ocurre en dos capas: Nginx (antes de que el payload llegue a FastAPI) y FastAPI (validación de tipo y dimensiones de imagen).

## When to use

Aplicar en Nginx como primera línea y en el endpoint de FastAPI que recibe las imágenes. Rechazar con 413 antes de leer el body completo.

## Instructions

1. En Nginx: `client_max_body_size 20M;` — rechaza con 413 sin pasar al upstream.
2. En FastAPI, validar el campo `UploadFile`:
   ```python
   MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB por imagen
   async def validate_image(file: UploadFile):
       content = await file.read(MAX_IMAGE_SIZE + 1)
       if len(content) > MAX_IMAGE_SIZE:
           raise HTTPException(413, "Imagen demasiado grande. Máximo 10MB.")
       await file.seek(0)
       return content
   ```
3. Validar que el Content-Type sea `image/jpeg` o `image/png` — rechazar otros tipos con 415.
4. Validar dimensiones mínimas: ancho y alto ≥ 640px (imagen demasiado pequeña → calidad insuficiente).
5. Validar dimensiones máximas: ancho o alto ≤ 6000px (imágenes de cámaras DSLR innecesariamente grandes).
6. Registrar en logs todos los rechazos por tamaño con la IP origen para análisis de amenazas.

## Notes

- El check de tamaño en Nginx es O(0) — rechaza sin leer el body. El check en FastAPI es más preciso pero ya leyó el body.
- Límite recomendado: selfie máx 5MB, documento máx 10MB. Ajustar según calidad de cámara de los clientes.
- Imágenes demasiado pequeñas (<640px) deben rechazarse en `capture_agent` con mensaje de UI explicativo.