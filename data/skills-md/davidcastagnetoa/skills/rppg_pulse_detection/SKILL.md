---
name: rppg_pulse_detection
description: Detectar pulso cardiaco en el video como señal biológica irrefutable de vida
type: ML Model
priority: Opcional
mode: Self-hosted
---

# rppg_pulse_detection

Remote Photoplethysmography (rPPG) detecta cambios sutiles en el color de la piel causados por el flujo sanguíneo, permitiendo medir el pulso cardiaco desde video. Una señal de pulso válida es evidencia biológica irrefutable de que hay una persona viva frente a la cámara.

## When to use

Usar como señal de liveness de última línea en el `liveness_agent`. Requiere 5-10 segundos de video estable. Aplicar solo cuando otros métodos de liveness dan scores ambiguos (entre 0.4 y 0.7).

## Instructions

1. Capturar mínimo 5 segundos de video a 30fps con iluminación estable.
2. Detectar y trackear la región de la frente/mejillas frame a frame con Mediapipe.
3. Extraer la señal de color verde promedio (canal G) de la ROI facial por frame.
4. Aplicar filtro bandpass (0.7-4 Hz) para aislar frecuencias cardiacas (42-240 bpm).
5. Calcular FFT de la señal filtrada e identificar el pico dominante.
6. Si el pico está entre 50-120 bpm con SNR > 3dB, clasificar como pulso válido.
7. Score: `rppg_confidence` basado en la claridad del pico de frecuencia.

## Notes

- Requiere iluminación estable; luz artificial parpadeante puede crear artefactos.
- No funciona bien con pieles muy oscuras o con maquillaje pesado; usar solo como señal complementaria.
- Implementaciones open-source: `pyVHR`, `rPPG-Toolbox`.