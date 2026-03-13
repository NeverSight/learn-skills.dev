---
name: pytest_cov
description: Medición de cobertura de tests con umbral mínimo configurable en CI
type: Tool
priority: Esencial
mode: Self-hosted
---

# pytest_cov

Plugin de pytest que mide la cobertura de código de los tests del sistema de verificación. Permite establecer umbrales mínimos de cobertura que se verifican automáticamente en CI, asegurando que los módulos críticos como liveness y face_match mantengan una cobertura adecuada.

## When to use

Usar en cada ejecución de tests del backend, tanto en desarrollo local como en CI/CD. Es obligatorio para validar que los módulos críticos del pipeline de verificación KYC mantienen la cobertura requerida. Especialmente importante al agregar nuevas funcionalidades o refactorizar módulos existentes.

## Instructions

1. Instalar el plugin: `pip install pytest-cov`.
2. Configurar en `pyproject.toml` o `setup.cfg` las opciones de cobertura bajo `[tool.pytest.ini_options]` y `[tool.coverage.run]`.
3. Ejecutar tests con cobertura: `pytest --cov=backend --cov-report=html --cov-report=term-missing`.
4. Establecer umbrales mínimos por módulo en `pyproject.toml`: `[tool.coverage.run] source = ["backend"]` y `[tool.coverage.report] fail_under = 80`.
5. Configurar umbrales diferenciados para módulos críticos: liveness (90%), face_match (90%), decision (95%), antifraud (85%), ocr (80%), doc_processing (75%).
6. Agregar el paso de cobertura en GitHub Actions: `pytest --cov=backend --cov-fail-under=80` para bloquear PRs que bajen la cobertura.
7. Generar reportes HTML de cobertura como artefactos de CI para revisión visual de las áreas no cubiertas.
8. Excluir de la medición archivos que no requieren tests: migraciones, configuraciones, scripts de utilidad.

## Notes

- No perseguir 100% de cobertura ciegamente; priorizar tests significativos en módulos críticos de seguridad (liveness, antifraud) sobre cobertura superficial.
- Configurar `[tool.coverage.report] exclude_lines` para ignorar líneas como `if __name__ == "__main__"` o `pragma: no cover`.
- Combinar con `pytest-xdist` para ejecutar tests en paralelo y reducir el tiempo de feedback: `pytest --cov=backend -n auto`.