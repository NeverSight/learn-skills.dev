---
name: c4_model
description: Metodología C4 para documentar la arquitectura del sistema KYC en niveles progresivos de detalle
type: Framework
priority: Esencial
mode: Self-hosted
---

# c4_model

Skill para aplicar la metodología C4 (Context, Container, Component, Code) como marco conceptual de documentación arquitectónica del sistema de verificación de identidad KYC. Permite descomponer la arquitectura del pipeline de verificación en cuatro niveles de abstracción progresivos, desde la vista de contexto del sistema hasta el detalle de código de cada módulo. Esta skill se centra exclusivamente en la metodología y los principios de modelado, no en herramientas específicas de renderizado.

## When to use

Usar esta skill cuando el architecture_agent necesite documentar, comunicar o razonar sobre la arquitectura del sistema KYC a distintos niveles de abstracción. Es apropiada para crear documentación arquitectónica que sea comprensible tanto por perfiles técnicos como no técnicos, y para planificar la estructura de los diagramas antes de implementarlos con cualquier herramienta.

## Instructions

1. **Definir el Nivel 1 - Diagrama de Contexto del Sistema**: Identificar el sistema KYC como caja central y mapear todos los actores externos (usuarios finales, operadores de backoffice, sistemas externos de fallback como AWS Rekognition o Google Vision) y sus interacciones principales.

```
Nivel 1 - Context:
- Sistema: "VerifID - Sistema de Verificación de Identidad KYC"
- Personas: Usuario Final, Operador de Revisión Manual
- Sistemas externos: Servicios cloud de fallback (Rekognition, Azure Face API), Base de datos PostgreSQL, Redis, MinIO
```

2. **Definir el Nivel 2 - Diagrama de Contenedores**: Descomponer el sistema KYC en sus contenedores principales: API Backend (FastAPI), Frontend Móvil (React Native/Flutter), Frontend Web, base de datos PostgreSQL, Redis para rate limiting, y MinIO para almacenamiento temporal de imágenes.

```
Nivel 2 - Containers:
- API Backend (FastAPI, Python) - Orquesta el pipeline de verificación
- App Móvil (React Native/Flutter) - Captura selfie y documento
- App Web - Versión web del flujo de verificación
- PostgreSQL - Datos de sesión y auditoría
- Redis - Rate limiting y caché de sesiones
- MinIO - Almacenamiento temporal de imágenes (max 15 min)
```

3. **Definir el Nivel 3 - Diagrama de Componentes del Backend**: Detallar los módulos internos del backend siguiendo la estructura del proyecto: liveness detection, OCR, face_match, doc_processing, antifraud y decision engine, mostrando las dependencias entre ellos.

```
Nivel 3 - Components (Backend API):
- LivenessModule: Passive liveness + Active challenge-response + Depth estimation
- OCRModule: PaddleOCR/EasyOCR + MRZ parser + Checksum validator (ICAO 9303)
- FaceMatchModule: InsightFace (ArcFace) embeddings + Cosine similarity
- DocProcessingModule: OpenCV contour detection + Homografía + ELA
- AntifraudModule: EXIF analysis + Deepfake detection + Geolocalización
- DecisionEngine: Score compuesto + Reglas configurables + Logging de auditoría
```

4. **Definir el Nivel 4 - Diagrama de Código**: Para módulos críticos como liveness y face_match, documentar las clases, interfaces y funciones principales con sus relaciones internas.

```
Nivel 4 - Code (FaceMatchModule):
- FaceExtractor: Extrae rostros de selfie y documento
- EmbeddingGenerator: Genera vectores con ArcFace/FaceNet
- SimilarityCalculator: Calcula cosine similarity entre embeddings
- ThresholdEvaluator: Evalúa contra umbral configurable (>0.85)
```

5. **Establecer convenciones de nomenclatura y estilo**: Definir un estándar para nombrar elementos en cada nivel, incluyendo el formato de las descripciones, la tecnología entre paréntesis, y el estilo de las relaciones entre elementos.

6. **Documentar las decisiones de frontera entre niveles**: Especificar qué elementos pertenecen a cada nivel y por qué, evitando mezclar niveles de abstracción. Por ejemplo, Redis es un contenedor (Nivel 2), no un componente del backend.

7. **Crear narrativas por nivel**: Para cada diagrama C4, redactar una descripción textual que explique el propósito del nivel, los elementos incluidos, y las decisiones arquitectónicas relevantes del pipeline KYC que justifican la estructura.

8. **Validar completitud y coherencia entre niveles**: Verificar que cada contenedor del Nivel 2 aparece como zoom-in en algún diagrama de Nivel 3, y que los componentes críticos tienen su correspondiente Nivel 4.

## Notes

- Esta skill se enfoca exclusivamente en la metodología C4 como marco de pensamiento arquitectónico. Para la implementación de diagramas como código, utilizar la skill `structurizr_dsl` que maneja el DSL específico de Structurizr.
- Los cuatro niveles no son obligatorios para todos los módulos: el Nivel 4 (Code) solo debe aplicarse a módulos de alta criticidad como liveness detection, face_match y el decision engine.
- La metodología C4 debe reflejar las restricciones de seguridad del sistema KYC, como el almacenamiento temporal de imágenes (máximo 15 minutos) y la transmisión cifrada, incluyéndolas como anotaciones en los niveles apropiados.
