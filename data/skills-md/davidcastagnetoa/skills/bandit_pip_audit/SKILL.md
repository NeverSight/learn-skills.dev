---
name: bandit_pip_audit
description: Análisis de seguridad estático del código Python y escaneo de dependencias en busca de CVEs
type: Tool
priority: Esencial
mode: Self-hosted
---

# bandit_pip_audit

Bandit analiza el código Python en busca de patrones de código inseguro (SQL injection via f-strings, uso de `eval`, algoritmos criptográficos débiles). `pip-audit` escanea las dependencias instaladas contra bases de datos de CVEs (PyPI Advisory Database, OSV).

## When to use

Ejecutar en pre-commit hooks y en CI. Un CVE crítico en una dependencia o un `subprocess(shell=True)` deben bloquear el merge.

## Instructions

1. Instalar: `pip install bandit pip-audit`
2. Ejecutar bandit: `bandit -r backend/ -ll -x backend/tests/`
   - `-ll` = reportar solo severidad MEDIUM y HIGH.
   - `-x backend/tests/` = excluir tests (usan `assert` que bandit marca como warning).
3. Configurar `.bandit` en raíz:
   ```ini
   [bandit]
   exclude_dirs = ["tests", "migrations"]
   skips = ["B101"]  # skip assert_used en tests
   ```
4. Ejecutar pip-audit: `pip-audit -r requirements.txt --format=json --output=audit-report.json`
5. En CI, fallar si hay vulnerabilidades de severidad CRITICAL o HIGH:
   ```bash
   pip-audit -r requirements.txt --severity HIGH --fail-on-severity HIGH
   ```
6. Añadir en pre-commit hooks (ver skill `pre_commit_hooks`).

## Notes

- Bandit detecta patrones como: `pickle.loads()` (deserialization), `hashlib.md5()` (weak hash), `random.random()` (en lugar de `secrets.token_hex()` para tokens).
- `pip-audit` complementa a Trivy (que escanea imágenes) — pip-audit es más rápido en CI porque no requiere build de imagen.
- Actualizar dependencias vulnerables tan pronto como haya parche disponible — documentar en el ADR si hay motivo para no actualizar.