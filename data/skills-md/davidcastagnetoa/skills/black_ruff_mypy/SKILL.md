---
name: black_ruff_mypy
description: Formateador, linter ultra-rápido y type checking estático para garantizar calidad del código Python
type: Tool
priority: Esencial
mode: Self-hosted
---

# black_ruff_mypy

Tres herramientas complementarias que se ejecutan juntas en cada commit y en CI para mantener la calidad del código Python sin debate entre developers.

## When to use

Configurar en pre-commit hooks desde el primer commit. Ejecutar también en CI como gate obligatorio antes de merge.

## Instructions

1. Instalar: `pip install black ruff mypy`
2. Configurar en `pyproject.toml`:

   ```toml
   [tool.black]
   line-length = 100
   target-version = ["py311"]

   [tool.ruff]
   line-length = 100
   select = ["E", "F", "I", "N", "W", "UP", "S", "B"]
   ignore = ["S101"]  # allow assert in tests

   [tool.mypy]
   python_version = "3.11"
   strict = true
   ignore_missing_imports = true
   plugins = ["pydantic.mypy"]
   ```

3. Añadir a `.pre-commit-config.yaml`:
   ```yaml
   repos:
     - repo: https://github.com/psf/black
       rev: 23.12.0
       hooks: [{id: black}]
     - repo: https://github.com/astral-sh/ruff-pre-commit
       rev: v0.1.9
       hooks: [{id: ruff, args: [--fix]}]
     - repo: https://github.com/pre-commit/mirrors-mypy
       rev: v1.8.0
       hooks: [{id: mypy, additional_dependencies: [pydantic, types-redis]}]
   ```
4. Instalar hooks: `pre-commit install`.
5. En CI: `ruff check . && black --check . && mypy backend/`.

## Notes

- Black reformatea automáticamente — los developers aceptan el formato sin discutir estilo.
- Ruff en modo `--fix` corrige automáticamente los errores que puede (imports desordenados, unused imports).
- mypy `strict=true` requiere type annotations en todo el código — es estricto pero previene bugs sutiles en async code.
- Ruff reemplaza Flake8, isort, pydocstyle y más — es 100x más rápido que las alternativas.
