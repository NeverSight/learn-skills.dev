---
name: onnx_model_export
description: Exportar modelos PyTorch del pipeline KYC a formato ONNX para portabilidad y optimización
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# onnx_model_export

Convierte los modelos PyTorch del sistema de verificación de identidad (ArcFace para reconocimiento facial, MiniFASNet para liveness detection, YOLOv8 para detección de documentos) al formato ONNX. Esto permite desacoplar la inferencia del framework de entrenamiento, habilitando optimizaciones posteriores como cuantización y ejecución en ONNX Runtime o TensorRT.

## When to use

Usa esta skill cuando necesites convertir modelos PyTorch a ONNX dentro del **model_server_agent**. Aplica cuando se tenga un modelo entrenado o fine-tuned y se requiera exportarlo para su despliegue en producción con runtimes optimizados, o cuando se necesite portabilidad entre diferentes plataformas de inferencia.

## Instructions

1. Cargar el modelo PyTorch con sus pesos entrenados:
   ```python
   import torch
   from models.arcface import ArcFaceModel

   model = ArcFaceModel()
   model.load_state_dict(torch.load("weights/arcface_r100.pth", map_location="cpu"))
   model.eval()
   ```

2. Crear un tensor dummy con las dimensiones de entrada correctas para cada modelo:
   ```python
   # ArcFace: batch x 3 x 112 x 112
   dummy_input = torch.randn(1, 3, 112, 112)

   # MiniFASNet (liveness): batch x 3 x 80 x 80
   # YOLOv8 (documentos): batch x 3 x 640 x 640
   ```

3. Exportar el modelo a ONNX con nombres de entrada/salida descriptivos y ejes dinámicos para batching:
   ```python
   torch.onnx.export(
       model,
       dummy_input,
       "models/arcface.onnx",
       input_names=["face_image"],
       output_names=["embedding"],
       dynamic_axes={
           "face_image": {0: "batch_size"},
           "embedding": {0: "batch_size"}
       },
       opset_version=17,
       do_constant_folding=True
   )
   ```

4. Verificar la validez del modelo ONNX exportado:
   ```python
   import onnx
   model_onnx = onnx.load("models/arcface.onnx")
   onnx.checker.check_model(model_onnx)
   print("Modelo ONNX válido")
   ```

5. Simplificar el grafo ONNX para eliminar nodos redundantes:
   ```python
   import onnxsim
   model_simplified, check = onnxsim.simplify(model_onnx)
   assert check, "La simplificación falló"
   onnx.save(model_simplified, "models/arcface_simplified.onnx")
   ```

6. Validar numéricamente que las salidas del modelo ONNX coincidan con las del modelo PyTorch original:
   ```python
   import onnxruntime as ort
   import numpy as np

   session = ort.InferenceSession("models/arcface.onnx")
   onnx_output = session.run(None, {"face_image": dummy_input.numpy()})[0]

   with torch.no_grad():
       torch_output = model(dummy_input).numpy()

   np.testing.assert_allclose(torch_output, onnx_output, rtol=1e-3, atol=1e-5)
   print("Validación numérica exitosa")
   ```

7. Documentar los metadatos del modelo exportado (versión, dimensiones, opset, fecha) en el registro de modelos del sistema.

## Notes

- Usar `opset_version=17` o superior para asegurar compatibilidad con las operaciones utilizadas por ArcFace y YOLOv8; versiones anteriores pueden no soportar ciertos operadores.
- Los ejes dinámicos en la dimensión batch son esenciales para permitir batching dinámico en producción; sin ellos, el modelo solo aceptaría el tamaño de batch fijo usado en la exportación.
- Siempre ejecutar la validación numérica (paso 6) antes de desplegar un modelo exportado, ya que diferencias en la implementación de operadores entre PyTorch y ONNX pueden causar discrepancias en los embeddings faciales.
