---
name: technical_debt_backlog
description: Mantener y priorizar el backlog de deuda técnica como parte del proceso de desarrollo
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# technical_debt_backlog

Proceso sistemático para identificar, registrar, priorizar y resolver la deuda técnica del sistema de verificación de identidad. Establece un backlog dedicado donde cada elemento de deuda se cuantifica por impacto y esfuerzo, integrándose en el ciclo de desarrollo regular.

## When to use

Usar de forma continua durante todo el ciclo de desarrollo del sistema KYC. Registrar deuda técnica cuando se tomen atajos conscientes para cumplir deadlines, cuando se detecten áreas del código que necesiten refactorización, o cuando métricas de calidad (cobertura, complejidad, rendimiento) muestren degradación. Revisar y priorizar el backlog en cada sprint planning.

## Instructions

1. Crear un sistema de etiquetado en el issue tracker (GitHub Issues) con la etiqueta `tech-debt` y sub-etiquetas por categoría: `debt:architecture`, `debt:performance`, `debt:security`, `debt:testing`, `debt:documentation`.
2. Para cada elemento de deuda, documentar: descripción del problema, módulo afectado, impacto (alto/medio/bajo), esfuerzo estimado, y riesgo de no resolverlo.
3. Calcular la prioridad con la fórmula: `prioridad = (impacto * riesgo) / esfuerzo` para ordenar el backlog objetivamente.
4. Reservar un porcentaje fijo del sprint (recomendado 15-20%) para resolver deuda técnica, no como trabajo "si sobra tiempo".
5. Integrar detección automática: configurar análisis estático (ruff, mypy) y métricas de complejidad ciclomática que generen issues automáticamente cuando se superen umbrales.
6. Revisar el backlog de deuda técnica cada 2 semanas, actualizando prioridades según el contexto actual del proyecto.
7. Vincular cada resolución de deuda técnica con métricas de mejora medibles (tiempo de respuesta, cobertura, complejidad reducida).

## Notes

- La deuda técnica en módulos de seguridad (liveness, antifraud) debe tratarse con prioridad máxima ya que puede traducirse directamente en vulnerabilidades explotables.
- Documentar la deuda técnica al momento de crearla conscientemente (con un comentario `# TECH-DEBT:` en el código) es más efectivo que intentar descubrirla después.
- Medir la tendencia de la deuda técnica a lo largo del tiempo; si crece más rápido de lo que se resuelve, escalar el problema al equipo.