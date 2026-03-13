---
name: dex_mivolo_age_estimator
description: Estimar edad del usuario por el rostro y comparar con fecha de nacimiento del documento
type: ML Model
priority: Esencial
mode: Self-hosted
---

# dex_mivolo_age_estimator

DEX (Deep EXpectation) y MiVOLO son modelos de estimación de edad facial. Predicen la edad aparente del usuario a partir de la selfie y la comparan con la fecha de nacimiento del documento para detectar inconsistencias.

## When to use

Usar en el `antifraud_agent` para verificar coherencia edad-documento. Si la edad estimada difiere significativamente de la edad calculada por fecha de nacimiento, es señal de fraude (documento de otra persona).

## Instructions

1. Instalar MiVOLO: `pip install mivolo` o clonar repositorio oficial.
2. Cargar modelo: `model = MiVOLO(weights='mivolo_d1_224.pth', device='cuda')`.
3. Input: face crop de la selfie, alineado y normalizado.
4. Output: `estimated_age` (float, años).
5. Calcular edad real: `real_age = (fecha_actual - fecha_nacimiento).days / 365.25`.
6. Calcular diferencia: `age_diff = abs(estimated_age - real_age)`.
7. Score: si `age_diff > 10`, flag de riesgo alto; si `age_diff > 15`, rechazo recomendado.

## Notes

- MiVOLO es más preciso que DEX (~3 años de MAE vs ~5 años).
- La estimación de edad tiene sesgo con ciertas etnias; usar solo como señal complementaria.
- Latencia: ~50ms en GPU; se puede ejecutar en paralelo con el face match.