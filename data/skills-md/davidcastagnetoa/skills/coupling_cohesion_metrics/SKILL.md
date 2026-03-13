---
name: coupling_cohesion_metrics
description: Medir acoplamiento entre módulos y cohesión interna para detectar degradación arquitectónica
type: Algorithm
priority: Recomendada
mode: Self-hosted
---

# coupling_cohesion_metrics

Algoritmo para medir cuantitativamente el acoplamiento entre los módulos del sistema de verificación y la cohesión interna de cada módulo. Permite detectar tempranamente cuando la arquitectura se degrada, identificando módulos que se vuelven demasiado dependientes entre sí o que asumen responsabilidades que no les corresponden.

## When to use

Usar de forma periódica (mensual o por sprint) para monitorizar la salud arquitectónica del sistema. Ejecutar cuando se sospeche que un módulo ha crecido demasiado, cuando las importaciones cruzadas aumenten, o cuando los cambios en un módulo requieran modificaciones en cascada en otros módulos. Complementa la skill `archunit_import_linter` con métricas cuantitativas.

## Instructions

1. Instalar herramientas de análisis: `pip install radon` para complejidad y `pip install import-linter` para dependencias.
2. Medir el acoplamiento aferente (Ca) de cada módulo: cuántos otros módulos dependen de él. Un Ca alto indica un módulo central que requiere estabilidad.
3. Medir el acoplamiento eferente (Ce) de cada módulo: de cuántos módulos depende. Un Ce alto indica un módulo con demasiadas dependencias externas.
4. Calcular la inestabilidad de cada módulo: `I = Ce / (Ca + Ce)`. Valores cercanos a 1 indican módulos inestables que deberían depender de abstracciones.
5. Medir la cohesión interna usando LCOM (Lack of Cohesion of Methods): analizar cuántas funciones de un módulo usan los mismos datos internos.
6. Crear un script `backend/scripts/architecture_metrics.py` que genere un reporte con estas métricas para todos los módulos del sistema.
7. Establecer umbrales de alerta: Ce > 5 (demasiadas dependencias), LCOM > 0.8 (baja cohesión), y trackear la evolución temporal.
8. Visualizar las métricas en un dashboard o generar un reporte en cada release que muestre la tendencia.

## Notes

- Los módulos `liveness`, `ocr`, `face_match` y `doc_processing` deben tener bajo acoplamiento entre sí (Ce bajo) y alta cohesión interna (LCOM bajo).
- El módulo `decision` tendrá naturalmente un Ce alto al depender de todos los demás; esto es aceptable por su rol de orquestación.
- Comparar las métricas antes y después de refactorizaciones significativas para validar que la mejora arquitectónica es real y medible.