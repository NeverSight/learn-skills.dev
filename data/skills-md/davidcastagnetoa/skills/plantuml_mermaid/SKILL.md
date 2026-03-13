---
name: plantuml_mermaid
description: Diagramas de secuencia flujo de datos y topología de despliegue como código
type: Tool
priority: Recomendada
mode: Self-hosted
---

# plantuml_mermaid

Herramienta para crear diagramas técnicos como código utilizando PlantUML y Mermaid. Permite documentar secuencias de verificación, flujos de datos entre módulos y topologías de despliegue de forma versionable en Git.

## When to use

Usar cuando se necesite documentar la arquitectura del sistema de verificación de identidad, incluyendo flujos de verificación KYC, interacciones entre módulos (liveness, OCR, face_match) y topología de despliegue en Kubernetes. También aplica cuando se requiera comunicar decisiones arquitectónicas a otros miembros del equipo mediante diagramas reproducibles.

## Instructions

1. Instalar PlantUML localmente: `brew install plantuml` (macOS) o `apt-get install plantuml` (Linux).
2. Para Mermaid, usar el CLI: `npm install -g @mermaid-js/mermaid-cli`.
3. Crear archivos `.puml` o `.mmd` dentro de `docs/diagrams/` siguiendo la convención `<módulo>_<tipo>.puml` (e.g., `verification_flow_sequence.puml`).
4. Definir diagramas de secuencia para cada pipeline del sistema (captura selfie, liveness, comparación facial, decisión final).
5. Generar diagramas de despliegue mostrando contenedores Docker, servicios K8s, bases de datos (PostgreSQL, Redis) y almacenamiento (MinIO).
6. Renderizar los diagramas a PNG/SVG con: `plantuml docs/diagrams/*.puml` o `mmdc -i diagrama.mmd -o diagrama.svg`.
7. Integrar la generación de diagramas en CI para que se regeneren automáticamente cuando cambie el código fuente del diagrama.
8. Incluir los diagramas renderizados en la documentación del proyecto referenciándolos desde archivos de documentación existentes.

## Notes

- Preferir Mermaid para diagramas simples (secuencia, flujo) ya que se renderiza nativamente en GitHub/GitLab, y PlantUML para diagramas más complejos (despliegue, componentes).
- Los archivos fuente de los diagramas deben vivir junto al código en el repositorio, no en herramientas externas, para mantener la trazabilidad.
- Establecer una convención de colores y estilos consistente para distinguir módulos críticos (liveness, antifraud) de módulos auxiliares.