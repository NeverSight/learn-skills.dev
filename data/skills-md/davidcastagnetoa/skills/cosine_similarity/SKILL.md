---
name: cosine_similarity
description: Métrica estándar de comparación entre embeddings faciales normalizados
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# cosine_similarity

La similitud coseno mide el ángulo entre dos vectores de embedding. Es la métrica estándar para comparar embeddings faciales porque es invariante a la escala (magnitud del vector).

## When to use

Usar para comparar cualquier par de embeddings faciales en el `face_match_agent`.

## Instructions

1. Asegurarse que ambos embeddings están normalizados a norma unitaria (L2 norm = 1).
2. Normalización: `embedding = embedding / np.linalg.norm(embedding)`.
3. Calcular similitud: `similarity = float(np.dot(embedding_1, embedding_2))`.
4. Rango de valores: -1 (opuesto) a 1 (idéntico). Para caras diferentes: típicamente < 0.3.
5. Mapear a porcentaje para UI: `score_pct = (similarity + 1) / 2 * 100`.
6. Registrar el score raw y el score mapeado en el evento de auditoría.
7. Si hay múltiples embeddings (varios frames de selfie), calcular la media de similitudes.

## Notes

- Para distancia euclidiana: `distance = np.linalg.norm(e1 - e2)`. Usar solo si los modelos están calibrados para esta métrica.
- NumPy `np.dot` sobre vectores normalizados es equivalente a `sklearn.metrics.pairwise.cosine_similarity` pero más rápido.