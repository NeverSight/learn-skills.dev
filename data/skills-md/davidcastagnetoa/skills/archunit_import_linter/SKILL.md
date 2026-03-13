---
name: archunit_import_linter
description: Verificar reglas de dependencia entre módulos para evitar importaciones cruzadas
type: Tool
priority: Recomendada
mode: Self-hosted
---

# archunit_import_linter

Herramienta que verifica reglas de dependencia entre módulos del sistema analizando las importaciones del código Python. Previene que módulos independientes (como liveness y OCR) desarrollen dependencias cruzadas que degraden la arquitectura modular del sistema.

## When to use

Usar en CI para validar que la arquitectura modular del sistema de verificación se mantiene intacta. Ejecutar en cada PR para detectar importaciones que violen las reglas de dependencia definidas (e.g., el módulo de OCR no debe importar directamente del módulo de liveness). Fundamental para mantener la independencia entre los módulos del pipeline KYC.

## Instructions

1. Instalar import-linter: `pip install import-linter`.
2. Configurar las reglas de dependencia en `pyproject.toml` bajo `[tool.importlinter]`.
3. Definir los contratos de la arquitectura: `[[tool.importlinter.contracts]] name = "Módulos independientes" type = "independence" modules = ["backend.modules.liveness", "backend.modules.ocr", "backend.modules.face_match", "backend.modules.doc_processing"]`.
4. Definir contratos de capas: el módulo `decision` puede importar de todos los módulos, pero ningún módulo puede importar de `decision`.
5. Permitir dependencias explícitas solo a través de schemas compartidos: `backend.schemas` puede ser importado por cualquier módulo.
6. Ejecutar la verificación: `lint-imports` y revisar las violaciones reportadas.
7. Agregar `lint-imports` como paso obligatorio en CI, antes de los tests unitarios.
8. Documentar las reglas de dependencia permitidas en un diagrama de capas dentro de `docs/diagrams/`.

## Notes

- Las dependencias entre módulos deben fluir siempre en una dirección: módulos de captura hacia módulos de procesamiento, y de procesamiento hacia el motor de decisión.
- Cuando dos módulos necesiten compartir lógica, extraer esa lógica a un paquete `backend.common/` o `backend.schemas/` en lugar de crear dependencias cruzadas.
- Revisar periódicamente las reglas de import-linter para asegurar que reflejan la arquitectura deseada y no simplemente el estado actual del código.