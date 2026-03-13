---
name: adr_tools
description: Herramienta CLI para gestionar Architecture Decision Records con numeración automática y linking
type: Tool
priority: Recomendada
mode: Self-hosted
---

# adr_tools

Skill para utilizar adr-tools como herramienta de línea de comandos que automatiza la gestión de Architecture Decision Records (ADRs) en el proyecto KYC. Proporciona comandos para crear nuevos ADRs con numeración secuencial, templates estandarizados, y enlaces entre decisiones relacionadas, manteniendo un registro estructurado de las decisiones arquitectónicas del pipeline de verificación de identidad. Esta skill se centra en la herramienta CLI, no en el framework conceptual de ADRs.

## When to use

Usar esta skill cuando el architecture_agent necesite crear, modificar o gestionar ADRs mediante la herramienta CLI adr-tools. Es apropiada cuando se requiere automatizar la creación de registros de decisión con numeración secuencial, establecer links entre decisiones que se superseden o complementen, o configurar templates personalizados para el contexto del sistema KYC.

## Instructions

1. **Instalar adr-tools**: Instalar la herramienta CLI en el entorno de desarrollo del proyecto.

```bash
# macOS
brew install adr-tools

# Linux (desde fuente)
git clone https://github.com/npryce/adr-tools.git
cd adr-tools && sudo make install

# Verificar instalación
adr help
```

2. **Inicializar el directorio de ADRs en el proyecto**: Crear la estructura de ADRs dentro del repositorio KYC, estableciendo el directorio base y el primer ADR de registro.

```bash
# Inicializar en el directorio docs/adr del proyecto
cd /path/to/identity-verification
adr init docs/adr

# Esto crea:
# docs/adr/0001-record-architecture-decisions.md
```

3. **Crear nuevos ADRs para decisiones del sistema KYC**: Usar el comando `adr new` para registrar decisiones arquitectónicas con numeración automática.

```bash
# Decisiones típicas del pipeline KYC
adr new "Usar InsightFace ArcFace como motor principal de comparación facial"
# Crea: docs/adr/0002-usar-insightface-arcface-como-motor-principal-de-comparacion-facial.md

adr new "Implementar liveness detection con enfoque híbrido passive-active"
# Crea: docs/adr/0003-implementar-liveness-detection-con-enfoque-hibrido-passive-active.md

adr new "Limitar almacenamiento de imágenes a 15 minutos máximo"
# Crea: docs/adr/0004-limitar-almacenamiento-de-imagenes-a-15-minutos-maximo.md

adr new "Priorizar soluciones self-hosted sobre servicios cloud externos"
# Crea: docs/adr/0005-priorizar-soluciones-self-hosted-sobre-servicios-cloud-externos.md
```

4. **Establecer links entre ADRs relacionados**: Usar la opción de superseding y linking para conectar decisiones que se reemplazan o complementan.

```bash
# Cuando una decisión reemplaza a otra
adr new -s 2 "Migrar de DeepFace a InsightFace ArcFace para mejor precisión"
# Crea un nuevo ADR que marca el 0002 como superseded

# Cuando una decisión complementa a otra
adr new -l "3:Complementa:Complementado por" "Añadir detección de profundidad 3D con MiDaS al módulo liveness"
# Crea un ADR con link bidireccional al 0003
```

5. **Personalizar el template para el contexto KYC**: Configurar un template que incluya secciones relevantes para decisiones de un sistema de verificación de identidad.

```bash
# Crear template personalizado
adr config template docs/adr/templates/template.md
```

```markdown
# {NUMBER}. {TITLE}

Fecha: {DATE}

## Estado

{STATUS}

## Contexto

<!-- Describir el problema o necesidad en el pipeline KYC -->

## Decisión

<!-- Describir la decisión tomada -->

## Módulos Afectados

<!-- Listar módulos del pipeline: liveness, ocr, face_match, doc_processing, antifraud, decision -->

## Impacto en Seguridad/Privacidad

<!-- Evaluar impacto en FAR/FRR, GDPR, almacenamiento de datos biométricos -->

## Consecuencias

<!-- Describir consecuencias positivas y negativas -->

## Alternativas Consideradas

<!-- Listar alternativas evaluadas y motivos de descarte -->
```

6. **Generar tabla de contenidos de ADRs**: Usar el comando de listado para generar un índice navegable de todas las decisiones registradas.

```bash
# Listar todos los ADRs con su estado
adr list

# Generar tabla de contenidos en formato markdown
adr generate toc > docs/adr/README.md

# Generar grafo de relaciones entre ADRs
adr generate graph | dot -Tpng -o docs/adr/adr-graph.png
```

7. **Integrar adr-tools en el flujo de trabajo del equipo**: Establecer convenciones para cuándo crear ADRs y cómo revisarlos en el contexto del proyecto KYC.

```bash
# Estructura resultante en el repositorio
docs/
└── adr/
    ├── 0001-record-architecture-decisions.md
    ├── 0002-usar-insightface-arcface-como-motor-principal.md
    ├── 0003-implementar-liveness-detection-hibrido.md
    ├── 0004-limitar-almacenamiento-imagenes-15-minutos.md
    ├── 0005-priorizar-self-hosted-sobre-cloud.md
    ├── README.md          # Tabla de contenidos generada
    └── templates/
        └── template.md    # Template personalizado KYC
```

## Notes

- Esta skill se enfoca en la herramienta CLI adr-tools y sus comandos. Para el marco conceptual de cuándo y por qué documentar decisiones arquitectónicas, utilizar la skill `adr_framework`.
- Los ADRs deben tratarse como inmutables una vez aceptados: si una decisión cambia, se crea un nuevo ADR que supersede al anterior usando `adr new -s`, nunca se edita el ADR original. Esto mantiene el historial completo de la evolución arquitectónica del sistema KYC.
- El comando `adr generate graph` requiere Graphviz instalado (`brew install graphviz` o `apt install graphviz`) y es especialmente útil para visualizar las dependencias entre decisiones del pipeline de verificación.
