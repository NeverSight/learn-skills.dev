---
name: datamodel_code_generator
description: Generar modelos Pydantic a partir de OpenAPI/JSON Schema como fuente única de verdad
type: Tool
priority: Recomendada
mode: Self-hosted
---

# datamodel_code_generator

Herramienta que genera automáticamente modelos Pydantic a partir de especificaciones OpenAPI o JSON Schema. Permite mantener una fuente única de verdad para los contratos de datos del sistema, evitando inconsistencias entre la documentación de la API y el código.

## When to use

Usar cuando se trabaje con APIs externas de fallback (AWS Rekognition, Google Vision, Mindee) que proveen especificaciones OpenAPI, o cuando se defina primero el schema JSON y se quiera generar código Python automáticamente. También útil al integrar nuevos servicios al pipeline de verificación KYC.

## Instructions

1. Instalar la herramienta: `pip install datamodel-code-generator`.
2. Crear un directorio `backend/schemas/sources/` para almacenar los JSON Schema u OpenAPI specs fuente.
3. Generar modelos desde JSON Schema: `datamodel-codegen --input schema.json --output models.py --output-model-type pydantic_v2.BaseModel`.
4. Generar modelos desde OpenAPI: `datamodel-codegen --input openapi.yaml --output models.py --input-file-type openapi`.
5. Configurar opciones de generación: `--use-standard-collections --use-union-operator --field-constraints` para código Python moderno.
6. Agregar un script `backend/scripts/generate_models.sh` que regenere todos los modelos desde las specs fuente de forma reproducible.
7. Integrar la generación en CI para verificar que los modelos generados están sincronizados con las specs: comparar el output del generador con los archivos committeados.
8. Personalizar los modelos generados mediante herencia en archivos separados, nunca editando directamente los archivos auto-generados.

## Notes

- Marcar los archivos auto-generados con un comentario `# AUTO-GENERATED - DO NOT EDIT` en la primera línea para evitar ediciones manuales accidentales.
- Cuando la fuente de verdad sea el código Pydantic (no el schema), usar el flujo inverso: exportar JSON Schema desde Pydantic con `model_json_schema()`.
- Configurar pre-commit hooks para verificar que los modelos generados están actualizados antes de cada commit.
