---
name: json_schema_evolution
description: Garantizar backwards-compatibility al evolucionar contratos entre agentes
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# json_schema_evolution

Algoritmo y conjunto de reglas para evolucionar schemas JSON/Pydantic entre versiones sin romper la compatibilidad con consumidores existentes. Define qué cambios son seguros, cuáles requieren migración y cómo gestionar la transición entre versiones.

## When to use

Usar cada vez que se necesite modificar un schema existente del sistema de verificación, ya sea para agregar nuevos campos al resultado de liveness, cambiar el formato de respuesta del OCR, o actualizar la estructura del motor de decisión. Aplicar antes de hacer merge de cualquier PR que modifique modelos Pydantic compartidos.

## Instructions

1. Clasificar los cambios según su impacto: **aditivos** (nuevo campo opcional) son seguros, **destructivos** (eliminar campo, cambiar tipo, renombrar) son breaking changes.
2. Para cambios aditivos, agregar el nuevo campo con valor por defecto: `new_field: Optional[str] = None` para mantener compatibilidad.
3. Para breaking changes, crear una nueva versión del schema (e.g., `V1` a `V2`) y mantener ambas versiones activas durante un periodo de transición.
4. Implementar adaptadores de conversión entre versiones: `def v1_to_v2(data: SchemaV1) -> SchemaV2` para migración automática.
5. Documentar cada cambio de schema en un changelog dedicado `backend/schemas/CHANGELOG.md` con fecha, versión, tipo de cambio y razón.
6. Configurar tests automatizados que validen que datos generados con la versión anterior se deserializan correctamente con la nueva versión.
7. Implementar un periodo de deprecación mínimo de 2 releases antes de eliminar una versión antigua de un schema.

## Notes

- La regla de oro es: los productores de datos pueden agregar campos, los consumidores deben ignorar campos desconocidos.
- Usar el campo `schema_version` en cada mensaje para que los consumidores puedan seleccionar el parser correcto.
- Automatizar la detección de breaking changes en CI con la skill `breaking_change_detector`.