---
name: fastapi
description: Framework async de alto rendimiento para exponer endpoints REST en el orquestador
type: Framework
priority: Esencial
mode: Self-hosted
---

# fastapi

FastAPI es el framework web principal del sistema. Expone todos los endpoints REST con soporte nativo de `asyncio`, tipado estricto vía Pydantic y generación automática de documentación OpenAPI.

## When to use

Usar para definir y gestionar todos los endpoints del `orchestrator_agent`: recepción de sesiones, consulta de estado y entrega de resultados.

## Instructions

1. Instalar: `pip install fastapi uvicorn[standard]`
2. Definir el router principal en `backend/api/routers/verification.py`.
3. Usar `async def` en todos los handlers para no bloquear el event loop.
4. Validar el body de entrada con modelos Pydantic v2 anotados con tipos estrictos.
5. Devolver siempre `{ status, confidence_score, reasons[], timestamp, session_id }` como response model.
6. Configurar middleware de CORS, trusted hosts y compresión GZip.
7. Montar health check en `GET /health` y readiness en `GET /ready`.
8. Arrancar con Uvicorn en modo worker multiple: `uvicorn main:app --workers 4 --loop uvloop`.

## Notes

- No usar `def` síncrono en handlers de alta frecuencia; bloquea el event loop.
- Documentación auto-generada disponible en `/docs` (Swagger) y `/redoc`.
- Versionar la API: prefijo `/v1/` en todos los endpoints.
