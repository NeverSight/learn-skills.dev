---
name: model_versioning
description: Gestión de versiones de modelos ML con registro, metadata y rollback sin downtime
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# model_versioning

Implementa un sistema de versionado de modelos de machine learning para el pipeline de verificación de identidad, permitiendo registrar, almacenar y gestionar múltiples versiones de cada modelo (ArcFace, MiniFASNet, YOLOv8). Soporta rollback instantáneo y despliegue de nuevas versiones sin interrumpir el servicio de verificación en producción.

## When to use

Usa esta skill cuando necesites gestionar el ciclo de vida de versiones de modelos ML dentro del **model_server_agent**. Aplica cuando se entrene o fine-tunee un nuevo modelo de face recognition o liveness detection y se requiera desplegarlo de forma controlada, o cuando sea necesario revertir a una versión anterior por degradación de métricas.

## Instructions

1. Definir el esquema de registro de modelos con metadata obligatoria:
   ```python
   from dataclasses import dataclass
   from datetime import datetime

   @dataclass
   class ModelVersion:
       model_name: str          # ej: "arcface", "minifasnet", "yolov8_doc"
       version: str             # semver: "1.2.0"
       artifact_path: str       # ruta al archivo del modelo
       format: str              # "onnx", "torchscript", "mar"
       metrics: dict            # {"far": 0.0008, "frr": 0.032, "latency_p95_ms": 45}
       training_dataset: str    # referencia al dataset de entrenamiento
       created_at: datetime
       status: str              # "staging", "production", "archived", "rolled_back"
   ```

2. Implementar el registro de modelos en PostgreSQL para persistencia y auditoría:
   ```python
   class ModelRegistry:
       def register(self, model: ModelVersion) -> str:
           """Registra una nueva versión y retorna el version_id."""
           model.status = "staging"
           self.db.insert(model)
           self._upload_artifact(model.artifact_path, model.version)
           return model.version

       def promote(self, model_name: str, version: str):
           """Promueve un modelo de staging a production."""
           current_prod = self.get_production_version(model_name)
           if current_prod:
               self._update_status(current_prod, "archived")
           self._update_status(version, "production")
   ```

3. Almacenar los artefactos de modelo en MinIO (S3-compatible) con versionado habilitado:
   ```python
   def _upload_artifact(self, local_path: str, version: str):
       self.minio_client.fput_object(
           bucket_name="model-artifacts",
           object_name=f"{model_name}/{version}/model.onnx",
           file_path=local_path,
           metadata={"version": version, "format": "onnx"}
       )
   ```

4. Implementar rollback instantáneo recargando la versión anterior sin reiniciar el servidor:
   ```python
   def rollback(self, model_name: str):
       """Revierte al último modelo en producción archivado."""
       previous = self.db.query(
           "SELECT * FROM model_versions WHERE model_name=? AND status='archived' ORDER BY created_at DESC LIMIT 1",
           model_name
       )
       self._update_status(previous.version, "production")
       self._update_status(self.get_production_version(model_name), "rolled_back")
       self.model_server.hot_reload(model_name, previous.artifact_path)
   ```

5. Validar automáticamente cada nueva versión contra un dataset de validación antes de permitir la promoción a producción:
   ```python
   def validate_before_promote(self, model_name: str, version: str) -> bool:
       model_path = self.get_artifact_path(model_name, version)
       metrics = self.evaluator.evaluate(model_path, self.validation_dataset)
       return metrics["far"] < 0.001 and metrics["frr"] < 0.05
   ```

6. Exponer endpoints de gestión para listar versiones, promover y hacer rollback desde la Management API del model server.

7. Configurar alertas automáticas que disparen rollback si las métricas de producción (FAR/FRR) degradan por encima de los umbrales definidos.

## Notes

- Nunca eliminar artefactos de versiones anteriores inmediatamente; mantener al menos las 3 últimas versiones disponibles para rollback rápido en caso de degradación post-despliegue.
- La validación automática (paso 5) es un gate obligatorio antes de promover cualquier modelo a producción; esto previene que modelos con FAR/FRR fuera de umbral lleguen a servir verificaciones reales.
- El hot-reload de modelos debe ser atómico: las solicitudes en vuelo deben completarse con la versión anterior mientras las nuevas solicitudes usan la versión actualizada.
