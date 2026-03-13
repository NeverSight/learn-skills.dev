---
name: k6
description: Pruebas de carga con scripting en JavaScript más ligero que Locust
type: Tool
priority: Recomendada
mode: Self-hosted
---

# k6

Herramienta de pruebas de carga y rendimiento que utiliza scripts en JavaScript para definir escenarios de prueba. Es más ligera que Locust y permite validar que el sistema de verificación cumple con el objetivo de respuesta menor a 8 segundos bajo carga concurrente.

## When to use

Usar para validar los requisitos de rendimiento del sistema de verificación antes de cada release a producción. Ejecutar pruebas de carga contra los endpoints del pipeline KYC (captura, liveness, OCR, face_match, decisión) para asegurar que el tiempo de respuesta total se mantiene por debajo de 8 segundos y la disponibilidad supera el 99.9%.

## Instructions

1. Instalar k6: `brew install k6` (macOS) o descargar desde https://k6.io/docs/getting-started/installation/.
2. Crear el directorio `backend/tests/load/` para almacenar los scripts de pruebas de carga.
3. Escribir un script base `backend/tests/load/verification_flow.js` que simule el flujo completo de verificación KYC.
4. Definir escenarios de carga progresiva: `stages: [{duration: '1m', target: 10}, {duration: '3m', target: 50}, {duration: '1m', target: 0}]`.
5. Configurar thresholds que reflejen los requisitos del sistema: `thresholds: { http_req_duration: ['p(95)<8000'], http_req_failed: ['rate<0.001'] }`.
6. Crear scripts específicos para cada módulo crítico: liveness endpoint, OCR processing, face_match comparison.
7. Ejecutar las pruebas: `k6 run backend/tests/load/verification_flow.js` y analizar los resultados.
8. Integrar en CI como paso opcional en PRs y obligatorio antes de releases: exportar resultados a JSON para comparación histórica.

## Notes

- Ejecutar pruebas de carga contra un entorno de staging dedicado, nunca contra producción ni contra entornos compartidos de desarrollo.
- Los módulos de ML (liveness, face_match) serán los cuellos de botella; diseñar tests específicos para medir su throughput y latencia bajo concurrencia.
- Usar k6 Cloud o Grafana para visualización de resultados si se necesitan dashboards históricos de rendimiento.