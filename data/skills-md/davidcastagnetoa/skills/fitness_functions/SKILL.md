---
name: fitness_functions
description: Tests automatizados que verifican propiedades arquitectónicas como latencia máxima y acoplamiento entre módulos
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# fitness_functions

Las fitness functions son tests automatizados que verifican propiedades no funcionales del sistema: que ningún agente supera su presupuesto de latencia, que las dependencias entre capas siguen las reglas arquitectónicas, y que el acoplamiento no crece sin control.

## When to use

Ejecutar en CI en cada PR. Fallan el build si alguna propiedad arquitectónica se viola, proporcionando feedback inmediato al developer.

## Instructions

1. Latencia por agente: test que ejecuta cada agente con input sintético y mide el tiempo:
   ```python
   import pytest, time
   from backend.agents.liveness import LivenessAgent
   LATENCY_BUDGETS = {
       "liveness_passive": 0.1,    # 100ms
       "face_match": 0.2,          # 200ms
       "ocr": 0.3,                 # 300ms
       "document_processor": 0.2,  # 200ms
   }
   @pytest.mark.asyncio
   async def test_liveness_latency_budget():
       agent = LivenessAgent()
       start = time.perf_counter()
       result = await agent.run(SYNTHETIC_FRAME)
       elapsed = time.perf_counter() - start
       assert elapsed < LATENCY_BUDGETS["liveness_passive"],            f"Liveness agent exceeded budget: {elapsed:.3f}s > {LATENCY_BUDGETS['liveness_passive']}s"
   ```
2. Dependencias entre capas con `import-linter`: instalar `pip install import-linter` y configurar `setup.cfg`:
   ```ini
   [importlinter]
   root_packages = backend
   [[importlinter:contract:layers]]
   name = KYC layer architecture
   type = layers
   layers = backend.api | backend.agents | backend.infrastructure
   ```
3. Test de acoplamiento: verificar que ningún agente importa directamente de otro agente (solo via interfaz).
4. Test de schema compatibility: verificar backwards-compatibility de los modelos Pydantic entre versiones.

## Notes

- Las fitness functions documentan implícitamente las decisiones arquitectónicas — si fallan, hay que justificar la excepción.
- El presupuesto de latencia por agente debe sumar menos de 8s considerando la paralelización del pipeline.
- Ejecutar las fitness functions de latencia en hardware similar a producción — en CI sin GPU los tiempos son irrelevantes para los agentes ML.