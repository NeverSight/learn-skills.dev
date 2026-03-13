---
name: dependency_graph_analysis
description: Visualizar y analizar grafo de dependencias entre agentes para detectar ciclos
type: Algorithm
priority: Recomendada
mode: Self-hosted
---

# dependency_graph_analysis

Algoritmo para construir, visualizar y analizar el grafo de dependencias entre los módulos y agentes del sistema de verificación. Detecta automáticamente ciclos de dependencia, identifica módulos huérfanos y genera visualizaciones del grafo para facilitar la comprensión de la arquitectura.

## When to use

Usar cuando se agreguen nuevos módulos o agentes al sistema, cuando se sospechen dependencias circulares, o como parte de la revisión arquitectónica periódica. Ejecutar antes de refactorizaciones grandes para entender el impacto de los cambios. Especialmente útil para validar que el pipeline de verificación KYC mantiene un flujo unidireccional sin ciclos.

## Instructions

1. Instalar herramientas de análisis: `pip install pydeps graphviz` y el binario de Graphviz: `brew install graphviz`.
2. Generar el grafo de dependencias del backend: `pydeps backend/modules --cluster --max-bacon=3 -o docs/diagrams/dependency_graph.svg`.
3. Implementar detección de ciclos usando DFS (Depth-First Search) en el grafo de importaciones: crear `backend/scripts/detect_cycles.py`.
4. Analizar el grafo para identificar: ciclos (error), dependencias transitivas innecesarias (warning), módulos aislados sin conexiones (info).
5. Generar un reporte con métricas del grafo: número de nodos, número de aristas, profundidad máxima, componentes fuertemente conectados.
6. Validar que el grafo refleja la arquitectura esperada: flujo lineal desde captura hacia liveness, OCR, face_match, antifraud y finalmente decisión.
7. Integrar la detección de ciclos en CI como paso que bloquee el merge si se introduce una dependencia circular.

## Notes

- Un grafo de dependencias saludable para este sistema debería ser un DAG (Directed Acyclic Graph) con el motor de decisión como sumidero.
- Distinguir entre dependencias de código (imports) y dependencias de datos (schemas compartidos); ambas deben analizarse pero con reglas diferentes.
- Actualizar la visualización del grafo automáticamente en CI y publicarla como artefacto para que el equipo siempre tenga una vista actualizada de la arquitectura.