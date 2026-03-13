---
name: chaos_toolkit
description: Inyectar fallos controlados en staging para validar resiliencia
type: Tool
priority: Opcional
mode: Self-hosted
---

# chaos_toolkit

Framework de ingeniería del caos que permite inyectar fallos controlados en el entorno de staging para validar que el sistema de verificación KYC se comporta correctamente ante errores. Verifica que los fallbacks funcionan, los timeouts se respetan y la degradación es graceful.

## When to use

Usar en entornos de staging antes de releases importantes para validar la resiliencia del sistema. Ejecutar experimentos de caos cuando se agreguen nuevos módulos al pipeline, se cambien timeouts o se modifiquen los mecanismos de fallback a servicios externos (AWS Rekognition, Google Vision). No ejecutar nunca en producción sin aprobación explícita.

## Instructions

1. Instalar Chaos Toolkit: `pip install chaostoolkit chaostoolkit-kubernetes chaostoolkit-lib`.
2. Crear el directorio `infra/chaos/` para almacenar los experimentos.
3. Definir un experimento base que simule la caída del servicio de liveness: crear un JSON con `steady-state-hypothesis`, `method` y `rollbacks`.
4. Crear experimentos para escenarios críticos: MinIO no disponible, PostgreSQL con latencia alta, Redis caído, timeout en modelo ML de face_match.
5. Ejecutar un experimento: `chaos run infra/chaos/liveness_failure.json` y verificar que el sistema responde con degradación controlada.
6. Validar que el motor de decisión emite `MANUAL_REVIEW` cuando un módulo falla, en lugar de crashear o aprobar sin verificación completa.
7. Documentar los resultados de cada ejecución y las acciones correctivas tomadas.

## Notes

- Comenzar con experimentos simples (matar un pod, agregar latencia) antes de avanzar a escenarios complejos (partición de red, corrupción de datos).
- Cada experimento debe incluir rollbacks automáticos que restauren el estado normal del entorno de staging.
- Los experimentos de caos deben ejecutarse en ventanas de mantenimiento programadas y con monitorización activa del equipo
