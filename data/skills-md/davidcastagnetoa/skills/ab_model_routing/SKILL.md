---
name: ab_model_routing
description: Routing A/B entre versiones de modelos ML para evaluar mejoras en producción con métricas FAR/FRR
type: Algorithm
priority: Recomendada
mode: Self-hosted
---

# ab_model_routing

Implementa un sistema de routing A/B para evaluar nuevas versiones de modelos de machine learning en producción dentro del pipeline de verificación de identidad. Permite dirigir un porcentaje configurable del tráfico de verificación a un modelo candidato (ej: ArcFace v2) mientras el modelo de control (ej: ArcFace v1) sirve el resto, recopilando métricas comparativas de FAR, FRR y latencia para tomar decisiones de promoción basadas en datos.

## When to use

Usa esta skill cuando necesites evaluar una nueva versión de modelo ML en producción dentro del **model_server_agent**. Aplica cuando se tenga un modelo candidato que haya pasado validación offline pero se requiera confirmar su rendimiento con tráfico real de verificación antes de hacer un rollout completo.

## Instructions

1. Definir la configuración del experimento A/B:

   ```python
   @dataclass
   class ABExperiment:
       experiment_id: str
       model_name: str              # ej: "arcface"
       control_version: str         # ej: "1.0.0"
       candidate_version: str       # ej: "2.0.0"
       traffic_split: float         # 0.0 a 1.0, porcentaje al candidato
       start_date: datetime
       min_samples: int             # mínimo de verificaciones para significancia
       status: str                  # "running", "completed", "aborted"
       metrics_config: dict         # métricas a comparar: ["far", "frr", "latency_p95"]
   ```

2. Implementar el router que asigna cada solicitud de verificación al modelo control o candidato:

   ```python
   class ABRouter:
       def __init__(self, experiment: ABExperiment):
           self.experiment = experiment
           self.control_model = load_model(experiment.control_version)
           self.candidate_model = load_model(experiment.candidate_version)

       def route(self, session_id: str) -> tuple[str, Model]:
           # Hash determinista por session_id para consistencia
           hash_value = int(hashlib.sha256(session_id.encode()).hexdigest(), 16)
           if (hash_value % 100) / 100 < self.experiment.traffic_split:
               return "candidate", self.candidate_model
           return "control", self.control_model
   ```

3. Registrar los resultados de cada verificación asociados al grupo (control/candidato):

   ```python
   class ABMetricsCollector:
       def record(self, experiment_id: str, group: str, session_id: str,
                  prediction: dict, ground_truth: dict = None):
           self.db.insert({
               "experiment_id": experiment_id,
               "group": group,
               "session_id": session_id,
               "similarity_score": prediction["score"],
               "is_match": prediction["is_match"],
               "latency_ms": prediction["latency_ms"],
               "timestamp": datetime.utcnow()
           })
   ```

4. Implementar el análisis estadístico para determinar si la diferencia entre modelos es significativa:

   ```python
   from scipy import stats

   def analyze_experiment(self, experiment_id: str) -> dict:
       control_scores = self.get_scores(experiment_id, "control")
       candidate_scores = self.get_scores(experiment_id, "candidate")

       t_stat, p_value = stats.ttest_ind(control_scores, candidate_scores)
       control_far = self.calculate_far(experiment_id, "control")
       candidate_far = self.calculate_far(experiment_id, "candidate")

       return {
           "p_value": p_value,
           "control_far": control_far,
           "candidate_far": candidate_far,
           "is_significant": p_value < 0.05,
           "recommendation": "promote" if candidate_far < control_far and p_value < 0.05 else "keep_control"
       }
   ```

5. Configurar guardrails automáticos que detengan el experimento si el modelo candidato degrada métricas críticas:

   ```python
   def check_guardrails(self, experiment_id: str):
       candidate_far = self.calculate_far(experiment_id, "candidate")
       if candidate_far > 0.001:  # FAR > 0.1% -> abortar
           self.abort_experiment(experiment_id)
           self.alert("AB experiment aborted: candidate FAR exceeded threshold")
   ```

6. Exponer un dashboard o endpoint con métricas en tiempo real del experimento: FAR, FRR, latencia p50/p95, volumen de muestras por grupo y significancia estadística actual.

7. Al completar el experimento, generar un informe automático y, si el candidato es superior, integrarse con la skill `model_versioning` para promover la nueva versión.

## Notes

- El routing debe ser determinista por `session_id` para que todas las llamadas de una misma verificación (embedding, comparación) usen el mismo modelo, evitando inconsistencias en los resultados.
- Comenzar con un traffic split conservador (5-10% al candidato) e incrementar gradualmente solo si los guardrails no se activan; nunca iniciar un experimento con mas del 20% en el candidato sin validación previa.
- Los experimentos A/B en modelos de seguridad KYC requieren un volumen mínimo significativo (recomendado >1000 verificaciones por grupo) antes de tomar decisiones de promoción; resultados prematuros pueden ser engañosos.
