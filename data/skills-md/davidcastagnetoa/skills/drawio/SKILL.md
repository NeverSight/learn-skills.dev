---
name: drawio
description: Diagramas visuales complejos exportables a XML versionables en Git
type: Tool
priority: Recomendada
mode: Self-hosted
---

# drawio

Herramienta de diagramación visual que permite crear diagramas arquitectónicos complejos con interfaz gráfica. Los diagramas se almacenan como XML, lo que los hace versionables en Git y facilita la colaboración.

## When to use

Usar cuando se necesiten diagramas de arquitectura de alto nivel que requieran mayor detalle visual que PlantUML/Mermaid, como diagramas de infraestructura completos, mapas de red o diagramas de flujo con elementos gráficos personalizados. Ideal para presentaciones a stakeholders no técnicos o documentación de arquitectura detallada del sistema KYC.

## Instructions

1. Instalar draw.io Desktop desde https://github.com/jgraph/drawio-desktop/releases o usar la extensión de VS Code `hediet.vscode-drawio`.
2. Crear archivos `.drawio` dentro de `docs/diagrams/` con la convención `<nombre_descriptivo>.drawio`.
3. Diseñar diagramas de arquitectura del sistema de verificación incluyendo todos los módulos: liveness, OCR, face_match, doc_processing, antifraud y decision.
4. Representar las conexiones entre servicios, bases de datos (PostgreSQL, Redis), almacenamiento (MinIO) y APIs externas de fallback.
5. Exportar a SVG o PNG para inclusión en documentación: File > Export as > SVG/PNG.
6. Guardar siempre el archivo `.drawio` (XML) en el repositorio como fuente de verdad, además de los archivos exportados.
7. Configurar la extensión de VS Code para editar los diagramas directamente desde el IDE sin necesidad de abrir la aplicación de escritorio.

## Notes

- Los archivos `.drawio` son XML plano, lo que permite diffs legibles en Git aunque no sean perfectos visualmente.
- Usar la extensión de VS Code para edición rápida y la aplicación de escritorio para diagramas complejos que requieran mayor control visual.
- Mantener una librería de shapes personalizada para los componentes recurrentes del sistema (módulos, bases de datos, servicios ML).
