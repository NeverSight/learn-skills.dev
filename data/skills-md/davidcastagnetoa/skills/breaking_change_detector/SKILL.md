---
name: breaking_change_detector
description: Detectar automáticamente breaking changes entre versiones de schema en CI/CD
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# breaking_change_detector

Algoritmo que compara automáticamente dos versiones de un schema JSON/Pydantic y detecta cambios incompatibles hacia atrás. Se integra en el pipeline de CI/CD para bloquear merges que introduzcan breaking changes no intencionados en los contratos entre módulos del sistema.

## When to use

Usar en cada PR que modifique schemas Pydantic compartidos entre módulos del sistema de verificación. El detector debe ejecutarse automáticamente en CI para prevenir que cambios destructivos lleguen a producción sin un proceso de migración planificado. Especialmente crítico para los contratos del motor de decisión y las interfaces entre módulos de liveness y face_match.

## Instructions

1. Instalar las dependencias necesarias: `pip install deepdiff jsonschema`.
2. Crear el script `backend/scripts/detect_breaking_changes.py` que compare el JSON Schema de la rama actual contra el de la rama base.
3. Definir las reglas de detección: eliminar campo requerido, cambiar tipo de campo, renombrar campo, agregar campo requerido sin default, cambiar enum reduciendo valores.
4. Usar `deepdiff` para comparar los JSON Schemas generados: `diff = DeepDiff(old_schema, new_schema, ignore_order=True)` y clasificar cada diferencia.
5. Generar un reporte con los cambios detectados categorizados como: SAFE (aditivo), WARNING (potencialmente breaking), BREAKING (incompatible).
6. Configurar el paso de CI en GitHub Actions que ejecute el detector y falle si hay cambios BREAKING sin una flag explícita `--allow-breaking`.
7. Cuando un breaking change sea intencional, requerir que el PR incluya un plan de migración documentado y la flag de aprobación.

## Notes

- Almacenar los JSON Schemas de la última versión de producción en `backend/schemas/baseline/` como referencia para la comparación.
- El detector debe ejecutarse antes de los tests unitarios en el pipeline de CI para dar feedback temprano.
- Integrar con la skill `json_schema_evolution` para sugerir automáticamente la estrategia de migración cuando se detecte un breaking change.