---
name: dependabot_renovate
description: Actualizaciones automáticas de dependencias con PRs generados automáticamente
type: Tool
priority: Recomendada
mode: Self-hosted
---

# dependabot_renovate

Herramientas que monitorizan las dependencias del proyecto y generan Pull Requests automáticos cuando hay actualizaciones disponibles. Dependabot es nativo de GitHub y Renovate es self-hosted con mayor configurabilidad. Ambos ayudan a mantener las dependencias de seguridad actualizadas en el sistema KYC.

## When to use

Usar de forma continua en el repositorio para mantener actualizadas las dependencias de Python (pip), JavaScript (npm), Docker y Kubernetes. Especialmente crítico para dependencias de seguridad en un sistema que maneja datos biométricos sensibles. Configurar al inicio del proyecto y mantener activo durante todo el ciclo de vida.

## Instructions

1. Para Dependabot (GitHub nativo), crear `.github/dependabot.yml` en la raíz del repositorio.
2. Configurar los ecosistemas a monitorizar: `package-ecosystem: "pip"` para backend Python, `"docker"` para imágenes base, `"github-actions"` para workflows.
3. Establecer frecuencia de actualización: `schedule: interval: "weekly"` para dependencias generales y `"daily"` para actualizaciones de seguridad.
4. Agrupar dependencias relacionadas para reducir el número de PRs: `groups: ml-dependencies: patterns: ["insightface", "opencv*", "torch*"]`.
5. Para Renovate (alternativa self-hosted), instalar la GitHub App o ejecutar como contenedor Docker: `docker run renovate/renovate`.
6. Configurar `renovate.json` con reglas de auto-merge para actualizaciones patch que pasen CI: `"automerge": true, "matchUpdateTypes": ["patch"]`.
7. Definir reglas estrictas para dependencias críticas de ML y seguridad: requieren revisión manual antes del merge.
8. Monitorizar los PRs generados semanalmente y resolver conflictos o incompatibilidades rápidamente.

## Notes

- Priorizar actualizaciones de seguridad (CVEs) sobre actualizaciones de features; configurar alertas inmediatas para vulnerabilidades en dependencias como OpenCV, Pillow o cryptography.
- Configurar un límite máximo de PRs abiertos simultáneamente (recomendado: 5-10) para no saturar al equipo de revisión.
- Las actualizaciones de modelos ML (InsightFace, PaddleOCR) requieren validación de rendimiento adicional antes del merge, ya que pueden afectar FAR/FRR.