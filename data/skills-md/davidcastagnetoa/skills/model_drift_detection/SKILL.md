---
name: model_drift_detection
description: Detectar degradación progresiva de modelos ML en producción monitorizando scores y métricas biométricas
type: Algorithm
priority: Recomendada
mode: Self-hosted
---

# model_drift_detection

Skill para detectar y alertar sobre la degradación progresiva de los modelos ML desplegados en el pipeline de verificación KYC. Monitoriza la distribución de scores de similitud facial, tasas FAR/FRR y métricas de liveness para identificar drift estadístico. Cuando los umbrales se desvían de los baselines establecidos, genera alertas y recomienda reentrenamiento o recalibración.

## When to use

Usar esta skill cuando el **model_server_agent** necesite configurar o gestionar el sistema de monitorización de drift en los modelos de producción. Aplica cuando se observan cambios en la distribución de scores de face_match, liveness o antifraud, o cuando se necesita establecer baselines tras un nuevo despliegue de modelo.

## Instructions

1. Configurar la recolección de scores de inferencia en cada módulo del pipeline, almacenando distribuciones en ventanas temporales:
   ```python
   from evidently.metrics import DataDriftPreset
   from evidently.report import Report

   drift_report = Report(metrics=[DataDriftPreset()])
   drift_report.run(reference_data=baseline_df, current_data=production_df)
   ```

2. Definir los baselines de referencia para cada modelo tras el despliegue inicial:
   ```python
   BASELINE_CONFIG = {
       "face_match_arcface": {"mean_score": 0.92, "std_score": 0.05, "far": 0.001, "frr": 0.03},
       "liveness_antispoofing": {"mean_score": 0.95, "std_score": 0.03, "spoofing_detection_rate": 0.99},
       "ocr_paddleocr": {"mean_confidence": 0.88, "mrz_checksum_pass_rate": 0.97}
   }
   ```

3. Implementar test estadístico de Kolmogorov-Smirnov para comparar distribuciones actuales contra baseline:
   ```python
   from scipy.stats import ks_2samp

   stat, p_value = ks_2samp(baseline_scores, current_scores)
   if p_value < 0.05:
       trigger_drift_alert(model_name, stat, p_value)
   ```

4. Configurar ventanas de monitorización: ventana corta (1 hora) para detección rápida y ventana larga (7 días) para tendencias graduales.

5. Monitorizar FAR y FRR en tiempo real comparando contra los objetivos del sistema (FAR < 0.1%, FRR < 5%):
   ```python
   current_far = false_accepts / total_impostor_attempts
   current_frr = false_rejects / total_genuine_attempts
   if current_far > 0.001 or current_frr > 0.05:
       trigger_threshold_alert(model_name, current_far, current_frr)
   ```

6. Configurar alertas escalonadas: WARNING cuando el drift supera 1 sigma, CRITICAL cuando supera 2 sigma respecto al baseline.

7. Generar reportes automáticos semanales con la evolución de métricas por modelo y recomendaciones de acción:
   ```python
   drift_report.save_html("reports/drift_weekly_{date}.html")
   ```

8. Integrar con el motor de decisión para ajustar umbrales automáticamente en modo conservador cuando se detecta drift moderado.

## Notes

- El drift puede ser causado por cambios en la demografía de usuarios, condiciones de captura (iluminación, dispositivos nuevos) o degradación real del modelo. Siempre investigar la causa raíz antes de reentrenar.
- Mantener los datasets de baseline versionados y asociados a cada versión de modelo desplegada para permitir comparaciones históricas precisas.
- Las métricas de drift deben ser anonimizadas y no contener embeddings biométricos en cumplimiento con GDPR/LOPD.
