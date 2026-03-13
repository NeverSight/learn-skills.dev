---
name: pydantic_schema_registry
description: Definir schemas de todos los contratos entre agentes como modelos Pydantic versionados
type: Library
priority: Esencial
mode: Self-hosted
---

# pydantic_schema_registry

Registro centralizado de schemas Pydantic que define los contratos de datos entre todos los módulos y agentes del sistema de verificación. Cada schema se versiona explícitamente para garantizar compatibilidad entre servicios desplegados en diferentes momentos.

## When to use

Usar siempre que se defina o modifique un contrato de datos entre módulos del sistema (e.g., la respuesta del módulo liveness que consume el motor de decisión, o el resultado de OCR que alimenta al módulo antifraud). Es obligatorio para cualquier comunicación inter-módulo en el pipeline de verificación KYC.

## Instructions

1. Instalar Pydantic v2: `pip install pydantic>=2.0`.
2. Crear el directorio `backend/schemas/` como ubicación central de todos los modelos compartidos.
3. Definir un modelo base versionado que incluya metadatos: `class BaseSchema(BaseModel): schema_version: str; timestamp: datetime; session_id: str`.
4. Crear schemas específicos para cada módulo: `LivenessResult`, `OCRResult`, `FaceMatchResult`, `AntifraudResult`, `DecisionResult`, cada uno heredando de `BaseSchema`.
5. Incluir validadores Pydantic para reglas de negocio (e.g., `confidence_score` debe estar entre 0.0 y 1.0, `status` debe ser uno de VERIFIED/REJECTED/MANUAL_REVIEW).
6. Versionar los schemas con sufijo: `LivenessResultV1`, `LivenessResultV2`, manteniendo las versiones anteriores para backwards-compatibility.
7. Exportar JSON Schema de cada modelo con `model.model_json_schema()` para documentación automática y validación en otros lenguajes.
8. Registrar todos los schemas en un diccionario central `SCHEMA_REGISTRY` que mapee nombre y versión al modelo correspondiente.

## Notes

- Nunca eliminar un schema versionado que esté en uso en producción; deprecarlo y crear una nueva versión.
- Los schemas deben ser la fuente única de verdad para la documentación de la API (integrar con FastAPI automáticamente).
- Incluir ejemplos en cada schema usando `model_config = ConfigDict(json_schema_extra={"examples": [...]})` para facilitar testing y documentación.