---
name: github_actions_cicd
description: Pipeline de CI/CD con gates de calidad automatizados en cada PR
type: Tool
priority: Esencial
mode: Self-hosted
---

# github_actions_cicd

GitHub Actions ejecuta automáticamente linting, tests, análisis de seguridad y build de imágenes Docker en cada Pull Request. Un PR solo puede mergearse si pasan todos los gates de calidad.

## When to use

Configurar antes de escribir el primer test. El pipeline de CI es la red de seguridad que previene que código roto llegue a main.

## Instructions

1. Crear `.github/workflows/ci.yml`:
   ```yaml
   name: CI
   on: [push, pull_request]
   jobs:
     quality:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v4
           with: { python-version: "3.11" }
         - run: pip install -r requirements-dev.txt
         - run: ruff check .
         - run: mypy backend/
         - run: bandit -r backend/ -ll
         - run: safety check
     tests:
       runs-on: ubuntu-latest
       services:
         postgres:
           image: postgres:16-alpine
           env: {POSTGRES_PASSWORD: test}
         redis:
           image: redis:7-alpine
       steps:
         - uses: actions/checkout@v4
         - run: pip install -r requirements.txt -r requirements-dev.txt
         - run: pytest backend/tests/ --cov=backend --cov-fail-under=80
     security-scan:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: aquasecurity/trivy-action@master
           with: { image-ref: "kyc-api:${{ github.sha }}", format: "table", exit-code: 1 }
   ```
2. Añadir branch protection en GitHub: requerir que `quality`, `tests` y `security-scan` pasen antes de merge.
3. Workflow de CD en `.github/workflows/deploy.yml`: build + push a registry + deploy a Kubernetes al hacer merge en `main`.
4. Usar `actions/cache` para cachear el pip install — reduce tiempo de CI de 5 min a 2 min.
5. Secrets en GitHub Actions (Settings > Secrets): `REGISTRY_TOKEN`, `KUBECONFIG`, `VAULT_TOKEN`.

## Notes

- El umbral de cobertura `--cov-fail-under=80` debe aumentarse gradualmente conforme madura el proyecto.
- Separar CI (en cada PR) de CD (solo en main) — nunca deployar desde una rama de feature.
- Para modelos ML pesados, usar runners self-hosted con GPU para los tests de integración del pipeline.