---
name: isolation_forest
description: Detectar patrones de sesión inusuales (outliers) indicativos de fraude con Isolation Forest
type: ML Model
priority: Recomendada
mode: Self-hosted
---

# isolation_forest

Isolation Forest es un algoritmo de detección de anomalías no supervisado. Detecta sesiones que presentan una combinación inusual de características que difiere del comportamiento legítimo normal.

## When to use

Usar sobre el vector de características de cada sesión como capa adicional de detección de fraude.

## Instructions

1. Instalar: `pip install scikit-learn`.
2. Definir el vector de características de sesión: `[liveness_time, challenge_completion_time, score_liveness, score_face_match, retry_count, device_age_days, ip_geolocation_match, ...]`.
3. Entrenar el modelo con sesiones legítimas históricas: `clf = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)`. `clf.fit(legitimate_sessions_matrix)`.
4. Predecir anomalía: `anomaly_score = clf.decision_function([current_session_features])`.
5. Score negativo = más anómalo; umbral típico: `score < -0.1` → sospechoso.
6. Serializar modelo: `joblib.dump(clf, 'isolation_forest.pkl')`.
7. Reentrenar periódicamente (semanal/mensual) con nuevos datos.

## Notes

- El modelo mejora significativamente con más datos históricos; iniciar con umbrales conservadores.
- Combinar con reglas deterministas (hard rules) para mayor robustez.