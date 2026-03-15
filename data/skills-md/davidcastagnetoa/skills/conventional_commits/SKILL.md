---
name: conventional_commits
description: Estándar de mensajes de commit para generar changelogs automáticos y versiones semánticas
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# conventional_commits

Conventional Commits es un estándar ligero para los mensajes de commit que estructura la información de manera legible por humanos y máquinas. Es el input de `semantic-release` para determinar la versión y el CHANGELOG.

## When to use

Aplicar desde el primer commit del proyecto. Configurar `commitlint` + `husky` para rechazar commits que no sigan el formato.

## Instructions

1. Formato: `<type>(<scope>): <description>`
   - `feat(liveness): add MiDaS depth estimation` → minor bump
   - `fix(ocr): correct MRZ parsing for Spanish DNI` → patch bump
   - `feat!(api): change response format for /verify` → major bump (breaking change)
   - `chore(deps): update paddleocr to 2.7.3` → no release
   - `docs(architecture): add C4 component diagram`
   - `perf(face-match): optimize ArcFace inference batching`
2. Instalar commitlint: `npm install --save-dev @commitlint/cli @commitlint/config-conventional`
3. Configurar `.commitlintrc.json`: `{"extends": ["@commitlint/config-conventional"]}`
4. Configurar husky para ejecutar commitlint en `commit-msg` hook:
   ```bash
   npx husky add .husky/commit-msg 'npx --no-install commitlint --edit "$1"'
   ```
5. Scopes recomendados para el proyecto KYC: `capture`, `liveness`, `ocr`, `face-match`, `antifraud`, `decision`, `audit`, `gateway`, `infra`, `ml`.

## Notes

- Commitlint en el pre-commit hook previene que commits con formato incorrecto lleguen al repositorio.
- El scope es opcional pero muy recomendado — facilita el filtrado del CHANGELOG por agente.
- Los commits de merge automático de GitHub (`Merge pull request #123`) no siguen el formato pero son ignorados por semantic-release.