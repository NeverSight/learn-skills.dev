---
name: technology_radar
description: Mapa periódico de tecnologías del proyecto adopt trial assess hold formato ThoughtWorks
type: Framework
priority: Recomendada
mode: Self-hosted
---

# technology_radar

Framework para mantener un mapa actualizado de todas las tecnologías utilizadas y evaluadas en el proyecto, clasificándolas en cuatro anillos (Adopt, Trial, Assess, Hold) siguiendo el formato popularizado por ThoughtWorks. Facilita la toma de decisiones tecnológicas informadas y la gestión de la evolución del stack.

## When to use

Usar de forma periódica (trimestral) para revisar y actualizar el estado de las tecnologías del sistema de verificación. Consultar antes de introducir una nueva tecnología al stack, al evaluar alternativas para módulos existentes (e.g., cambiar de EasyOCR a PaddleOCR), o cuando se necesite justificar decisiones tecnológicas ante stakeholders.

## Instructions

1. Crear el archivo `docs/technology_radar.json` con la estructura: `{ "rings": ["Adopt", "Trial", "Assess", "Hold"], "quadrants": ["Languages & Frameworks", "Tools", "Platforms", "Techniques"], "entries": [...] }`.
2. Clasificar todas las tecnologías actuales del proyecto en los cuatro anillos: **Adopt** (usar en producción: FastAPI, PostgreSQL, InsightFace), **Trial** (probando activamente: PaddleOCR, k6), **Assess** (evaluando: alternativas cloud), **Hold** (no usar o migrar desde).
3. Organizar las tecnologías en cuadrantes: Languages & Frameworks (Python, Pydantic), Tools (Docker, pytest, OpenCV), Platforms (Kubernetes, MinIO, Redis), Techniques (liveness detection, chaos engineering).
4. Para cada entrada incluir: nombre, cuadrante, anillo actual, anillo anterior (si cambió), fecha de última revisión y justificación breve.
5. Generar la visualización del radar usando herramientas como `https://github.com/thoughtworks/build-your-own-radar` apuntando al JSON.
6. Revisar trimestralmente con el equipo: mover tecnologías entre anillos según la experiencia acumulada y documentar las razones del cambio.
7. Antes de proponer una nueva tecnología, verificar si ya existe una en Adopt o Trial que cubra la misma necesidad.

## Notes

- El radar tecnológico no es solo una herramienta de documentación: es una herramienta de decisión que previene la adopción desordenada de tecnologías y reduce la fragmentación del stack.
- Las tecnologías en Hold deben tener un plan de migración documentado con timeline; no basta con marcarlas para que eventualmente se reemplacen.
- Involucrar a todo el equipo técnico en la revisión trimestral del radar para que las decisiones reflejen experiencia real, no solo opiniones individuales.