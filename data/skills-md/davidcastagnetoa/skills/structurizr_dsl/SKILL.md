---
name: structurizr_dsl
description: Structurizr DSL para definir diagramas C4 como código versionable en el proyecto KYC
type: Tool
priority: Esencial
mode: Self-hosted
---

# structurizr_dsl

Skill para utilizar Structurizr DSL como lenguaje de definición de arquitectura como código, permitiendo escribir diagramas C4 del sistema KYC en archivos `.dsl` versionables en git. Facilita mantener la documentación arquitectónica del pipeline de verificación de identidad sincronizada con el código fuente, generando diagramas renderizables automáticamente. Esta skill se centra en la sintaxis y uso práctico del DSL, no en la metodología C4 en sí.

## When to use

Usar esta skill cuando el architecture_agent necesite crear, actualizar o mantener archivos Structurizr DSL (`.dsl`) que representen la arquitectura del sistema KYC como código. Es apropiada cuando se requiere generar diagramas C4 renderizables, integrar la documentación arquitectónica en el flujo de CI/CD, o actualizar los diagramas tras cambios en la estructura del pipeline de verificación.

## Instructions

1. **Crear el archivo workspace principal**: Inicializar el archivo `workspace.dsl` en el directorio `docs/architecture/` del proyecto con la estructura base del workspace de Structurizr.

```dsl
workspace "VerifID - KYC Identity Verification" "Sistema de verificación de identidad con comparación biométrica facial" {

    model {
        // Personas y sistemas se definen aquí
    }

    views {
        // Vistas C4 se definen aquí
    }
}
```

2. **Definir el modelo de software con personas y sistemas**: Declarar los actores, el sistema principal y los sistemas externos del ecosistema KYC usando la sintaxis DSL.

```dsl
model {
    endUser = person "Usuario Final" "Persona que necesita verificar su identidad"
    reviewer = person "Operador de Revisión" "Revisa casos marcados para revisión manual"

    verifid = softwareSystem "VerifID" "Sistema de verificación de identidad KYC" {
        apiBackend = container "API Backend" "Orquesta el pipeline de verificación" "FastAPI, Python"
        mobileApp = container "App Móvil" "Captura selfie y documento en vivo" "React Native"
        webApp = container "App Web" "Flujo de verificación web" "React"
        database = container "Base de Datos" "Datos de sesión y auditoría" "PostgreSQL"
        cache = container "Cache / Rate Limiter" "Rate limiting y sesiones" "Redis"
        objectStore = container "Almacenamiento Temporal" "Imágenes temporales (max 15 min)" "MinIO"
    }

    rekognition = softwareSystem "AWS Rekognition" "Fallback cloud para liveness" "Existing System"
    googleVision = softwareSystem "Google Vision" "Fallback cloud para OCR" "Existing System"
}
```

3. **Detallar los componentes internos del backend**: Expandir el contenedor del API Backend con los módulos del pipeline KYC como componentes.

```dsl
apiBackend = container "API Backend" "Orquesta el pipeline de verificación" "FastAPI, Python" {
    livenessModule = component "Liveness Detection" "Passive + Active liveness, depth estimation" "Python, Silent-Face-Anti-Spoofing"
    ocrModule = component "OCR Engine" "Extracción de texto y MRZ del documento" "PaddleOCR, EasyOCR"
    faceMatchModule = component "Face Match" "Comparación biométrica facial" "InsightFace, ArcFace"
    docProcessing = component "Document Processing" "Detección, corrección y validación del documento" "OpenCV, YOLOv8"
    antifraudModule = component "Antifraud Engine" "Detección de deepfakes, ELA, EXIF analysis" "Python, FaceForensics++"
    decisionEngine = component "Decision Engine" "Score compuesto y decisión final" "Python"
    apiEndpoints = component "API Endpoints" "Endpoints REST del pipeline" "FastAPI"
}
```

4. **Definir las relaciones entre elementos**: Establecer las dependencias y flujos de datos entre los componentes del sistema.

```dsl
endUser -> mobileApp "Captura selfie y documento"
endUser -> webApp "Captura selfie y documento"
mobileApp -> apiBackend "Envía imágenes cifradas" "HTTPS/TLS 1.3"
webApp -> apiBackend "Envía imágenes cifradas" "HTTPS/TLS 1.3"
apiBackend -> database "Lee/escribe sesiones"
apiBackend -> cache "Rate limiting, sesiones"
apiBackend -> objectStore "Almacena/recupera imágenes temporales"
apiBackend -> rekognition "Fallback liveness" "HTTPS"
apiBackend -> googleVision "Fallback OCR" "HTTPS"
reviewer -> apiBackend "Revisa casos pendientes"
```

5. **Crear las vistas para cada nivel C4**: Definir las vistas de contexto, contenedores y componentes con estilos visuales.

```dsl
views {
    systemContext verifid "SystemContext" {
        include *
        autoLayout
        description "Vista de contexto del sistema KYC VerifID"
    }

    container verifid "Containers" {
        include *
        autoLayout
        description "Contenedores del sistema VerifID"
    }

    component apiBackend "Components" {
        include *
        autoLayout
        description "Componentes internos del API Backend"
    }

    styles {
        element "Person" {
            shape Person
            background #08427B
            color #ffffff
        }
        element "Software System" {
            background #1168BD
            color #ffffff
        }
        element "Container" {
            background #438DD5
            color #ffffff
        }
        element "Component" {
            background #85BBF0
            color #000000
        }
        element "Existing System" {
            background #999999
            color #ffffff
        }
    }
}
```

6. **Renderizar los diagramas localmente**: Usar Structurizr CLI o Structurizr Lite (Docker) para generar los diagramas a partir del archivo DSL.

```bash
# Opción 1: Structurizr Lite con Docker
docker run -it --rm -p 8080:8080 -v $(pwd)/docs/architecture:/usr/local/structurizr structurizr/lite

# Opción 2: Structurizr CLI para exportar a PNG/SVG
docker run --rm -v $(pwd)/docs/architecture:/usr/local/structurizr structurizr/cli \
    export -workspace /usr/local/structurizr/workspace.dsl -format plantuml
```

7. **Integrar en el flujo de versionado**: Asegurar que el archivo `.dsl` esté incluido en el repositorio git y que los cambios arquitectónicos se reflejen como commits junto con los cambios de código correspondientes.

```
docs/
└── architecture/
    ├── workspace.dsl          # Definición principal
    ├── README.md              # Instrucciones de renderizado
    └── exports/               # Diagramas exportados (PNG/SVG)
```

## Notes

- Esta skill se enfoca en la sintaxis y uso práctico del DSL de Structurizr. Para la metodología C4 y las decisiones de qué incluir en cada nivel, utilizar la skill `c4_model`.
- Los archivos `.dsl` deben tratarse como código fuente: revisados en pull requests, con convenciones claras de nombrado de elementos, y acompañados de comentarios que expliquen decisiones no evidentes.
- Structurizr Lite (gratuito, Docker) es la opción recomendada para renderizado local, alineada con la preferencia del proyecto por soluciones self-hosted y evitando dependencia del servicio cloud de Structurizr.
