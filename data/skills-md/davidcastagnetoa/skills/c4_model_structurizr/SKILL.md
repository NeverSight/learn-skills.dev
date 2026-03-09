---
name: c4_model_structurizr
description: Diagramas de arquitectura C4 como código con Structurizr DSL, versionados en Git
type: Framework
priority: Esencial
mode: Self-hosted
---

# c4_model_structurizr

El modelo C4 (Context, Containers, Components, Code) proporciona un lenguaje común para diagramar arquitecturas de software a distintos niveles de abstracción. Structurizr DSL permite escribirlos como código.

## When to use

Usar para mantener actualizados los diagramas de arquitectura del sistema en 4 niveles: contexto, contenedores, componentes y código.

## Instructions

1. Instalar Structurizr Lite: `docker run -p 8080:8080 -v $(pwd):/usr/local/structurizr structurizr/lite`.
2. Crear `workspace.dsl` en `docs/architecture/`.
3. Definir los 4 niveles C4 en DSL:
   ```
   workspace {
     model {
       user = person "Usuario KYC"
       kyc_system = softwareSystem "Sistema KYC" {
         api_gateway = container "API Gateway" { technology "Nginx + Lua" }
         orchestrator = container "Orchestrator" { technology "FastAPI + Python" }
         ...
       }
     }
     views {
       systemContext kyc_system "Context" { include * autoLayout }
       container kyc_system "Containers" { include * autoLayout }
     }
   }
   ```
4. Visualizar en http://localhost:8080.
5. Exportar a PNG/SVG para documentación.
6. Mantener el DSL actualizado en Git; los diagramas son generados, no editados manualmente.

## Notes

- Documentación C4: https://c4model.com
- Structurizr: https://structurizr.com/help/dsl