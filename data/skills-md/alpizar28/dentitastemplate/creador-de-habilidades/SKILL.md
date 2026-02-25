---
name: creador-de-habilidades
description: Utiliza esta habilidad cuando el usuario quiera crear, modificar o analizar una nueva "Skill" (habilidad) para Antigravity. Proporciona instrucciones sobre estructura de carpetas, YAML y Markdown.
---

# Skill Creator de Antigravity

Como agente con esta habilidad activa, tu objetivo es ayudar al usuario a expandir sus capacidades de IA siguiendo el estándar de Antigravity.

## Reglas de Diseño
1. **Carpeta por Skill**: Cada habilidad debe estar en `skills/[nombre-de-la-skill]`.
2. **Archivo Maestro**: Toda skill requiere un `SKILL.md`.
3. **Progressive Disclosure**: El YAML frontmatter debe ser conciso. La `description` es lo que activa al agente.

## Estructura Recomendada
```text
skills/nombre-habilidad/
├── SKILL.md
├── scripts/
└── examples/
```

## Instrucciones para Creación
1. Define el propósito y el disparador (trigger) en el YAML.
2. Escribe instrucciones claras en Markdown para el agente que la usará.
3. Si requiere lógica compleja, sugiere la creación de un script en `scripts/`.
