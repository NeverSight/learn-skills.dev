---
name: decision_explainer
description: Generar razones legibles de la decisión para auditoría y revisión manual (LIME/SHAP)
type: Algorithm
priority: Recomendada
mode: Self-hosted
---

# decision_explainer

Genera explicaciones legibles por humanos de por qué se tomó una decisión de verificación. Combina los scores y flags de cada agente en una lista de razones priorizadas para auditoría y revisión manual.

## When to use

Usar en el `decision_agent` después de calcular el score global. Siempre generar explicaciones, pero son críticas para casos de `MANUAL_REVIEW` donde un operador humano necesita contexto.

## Instructions

1. Recopilar todos los scores parciales y flags de cada agente.
2. Identificar los factores que más contribuyeron a la decisión (mayor peso * desviación del umbral).
3. Generar razones en lenguaje natural:
   - `"Face match score bajo (0.62): posible discrepancia entre selfie y documento"`.
   - `"Documento posiblemente manipulado: ELA score 0.78"`.
4. Ordenar razones por impacto (contribución al score global).
5. Incluir máximo 5 razones principales en la respuesta.
6. Para casos de `MANUAL_REVIEW`, incluir recomendaciones al operador.
7. Registrar las razones como parte del evento de auditoría.

## Notes

- LIME/SHAP son opcionales para V1; la explicación basada en reglas es suficiente inicialmente.
- Las razones deben ser consistentes: misma situación siempre produce misma explicación.
- Nunca incluir datos biométricos en las explicaciones; solo scores y categorías.