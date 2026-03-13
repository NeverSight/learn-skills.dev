---
name: adr_framework
description: Framework para registrar Architecture Decision Records — decisiones arquitectónicas inmutables y auditables
type: Framework
priority: Esencial
mode: Self-hosted
---

# adr_framework

Los Architecture Decision Records (ADR) documentan cada decisión arquitectónica relevante en un formato estándar, creando un historial inmutable de por qué el sistema fue diseñado como está.

## When to use

Crear un ADR para cada decisión tecnológica significativa: elección de framework, librería, patrón de comunicación, estrategia de datos.

## Instructions

1. Instalar `adr-tools`: `npm install -g adr-tools` o usar el script: https://github.com/npryce/adr-tools.
2. Inicializar directorio ADR: `adr init docs/adr`.
3. Crear nuevo ADR: `adr new "Elección de FastAPI sobre Flask para el orquestador"`.
4. Formato estándar de cada ADR:
   - **Título**: número + descripción breve.
   - **Fecha**: cuándo se tomó la decisión.
   - **Estado**: `proposed | accepted | deprecated | superseded`.
   - **Contexto**: qué problema resuelve.
   - **Opciones evaluadas**: alternativas consideradas con pros/contras.
   - **Decisión**: qué se eligió y por qué.
   - **Consecuencias**: trade-offs aceptados.
5. Versionar todos los ADRs en Git: nunca borrar, solo deprecar/superseder.
6. Referenciar el ADR relevante en el código con comentarios: `# See ADR-001`.

## Notes

- Repositorio: https://github.com/npryce/adr-tools
- Los ADRs iniciales prioritarios para este proyecto: ADR-001 al ADR-010 listados en `Agents.md`.
