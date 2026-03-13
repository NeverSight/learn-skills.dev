---
name: age_progression_compensation
description: Ajustar el embedding para compensar diferencia de edad si la foto del documento es antigua
type: Algorithm
priority: Opcional
mode: Self-hosted
---

# age_progression_compensation

Algoritmo de compensación de envejecimiento que ajusta la comparación facial cuando hay una diferencia significativa de edad entre la foto del documento y la selfie actual. Reduce falsos rechazos en documentos con fotos antiguas.

## When to use

Usar en el `face_match_agent` cuando la fecha de emisión del documento indica que la foto tiene más de 5 años de antigüedad y el score de similitud está en zona ambigua (0.70-0.85).

## Instructions

1. Calcular antigüedad de la foto: `años = fecha_actual - fecha_emisión_documento`.
2. Si `años > 5`, activar compensación de edad.
3. Estimar edad en ambas imágenes usando el modelo DEX/MiVOLO del `antifraud_agent`.
4. Calcular delta de edad: `age_delta = edad_selfie - edad_documento`.
5. Aplicar factor de tolerancia al umbral de similitud: `threshold_adjusted = threshold - (0.02 * age_delta)`.
6. Mínimo umbral ajustado: 0.70 (nunca bajar de este valor por seguridad).
7. Registrar `age_delta` y `threshold_adjusted` en auditoría.

## Notes

- La compensación solo relaja el umbral, nunca lo endurece.
- Para diferencias > 20 años, recomendar revisión manual independientemente del score.
- Este módulo es complementario; si el score sin compensación ya supera 0.85, no es necesario.