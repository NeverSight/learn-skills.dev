---
name: contextualizar-repo
description: Contextualiza un repositorio existente (brownfield) para trabajar AI-first sobre él - verifica cómo se arranca y se prueba, crea el índice de CodeGraph, reconstruye el mapa de capas real, documenta las decisiones heredadas como ADR, arma el catálogo de patrones (canon vs. legado), el mapa de deuda y las reglas de construcción verificables, todo con evidencia archivo:línea, y se detiene para aprobación humana. Use when the ARCH role starts on an existing codebase without a PRD, or when asked to contextualize, onboard, document, map or understand a legacy/brownfield repository before working on it.
type: skill
tags: [arch, brownfield, contexto, patrones, deuda, agents-md]
---

# Contextualizar repo (brownfield)

## Goal

Dejar un sistema existente **igual que un greenfield**: que cualquier agente o persona que llegue
después encuentre escrito cómo se arranca, cómo está construido, qué decisiones se heredan, qué
patrones imitar y cuáles no, dónde está la deuda y qué reglas respetar al tocarlo.

Esta skill cubre el **contexto técnico** (capas 1, 2 y 5). El contexto funcional (capacidades,
reglas de negocio y glosario) lo documenta el BA con `contextualizar-negocio`.

**Esta skill no modifica código ni arregla deuda.** Lee, mide, documenta, pregunta y se detiene.

## Principios

1. **Nada sin evidencia.** Toda afirmación sobre el sistema lleva `archivo:línea`, un comando con
   su salida, o queda marcada `NO VERIFICADO`.
2. **La documentación existente es una fuente, no la verdad.** README, AGENTS.md, CLAUDE.md o
   docs previas se leen, y cada afirmación que se reutiliza se verifica contra el código.
3. **Se describe lo que el código es, no lo que debería ser.** Las propuestas de mejora van al
   mapa de deuda, nunca mezcladas con la descripción.
4. **No se toman decisiones de arquitectura nuevas.** Se documentan las heredadas. Elegir el
   canon cuando conviven varios patrones lo confirma el humano.

## Input

- La ruta del repositorio (por defecto, el directorio actual).
- Documentación existente, si la hay: `README*`, `AGENTS.md`, `CLAUDE.md`, `docs/`, ADRs previos.
- Opcional: qué parte del sistema le importa más al equipo (para profundizar ahí primero).

## Workflow

### 1. Hacerlo legible (capa 1)

1. Encontrar cómo se instala, arranca y prueba: `package.json` (o equivalente), `README`,
   `Dockerfile`, `docker-compose*`, documentación existente.
2. **Verificar** cada comando: si el usuario lo autoriza, correrlo y anotar resultado y tiempo. Si
   no se corre, queda `NO VERIFICADO`.
3. **Índice de CodeGraph:**
   - Si `codegraph` está instalado: `codegraph init` (o `codegraph index` si ya existe
     `.codegraph/`). Anotar cuánto tardó.
   - Si no está instalado: proponer instalarlo (ver su documentación vigente) y seguir sin él,
     dejando escrito que el mapa de dependencias se armó leyendo el código.
   - Usar el índice en los pasos siguientes para dependencias, impacto y callers.

### 2. Mapa de capas real (capa 2)

1. Recorrer la estructura de carpetas y asignar a cada una su responsabilidad **observada**.
2. Seguir **un flujo típico de punta a punta** (una petición desde que entra hasta que toca los
   datos) y anotar cada archivo que atraviesa. Ese recorrido valida el mapa.
3. Señalar las capas que existen en dos generaciones (por ejemplo, un frontend viejo y uno nuevo).

### 3. Decisiones heredadas (capa 2)

1. Identificar las decisiones **estructurales** ya tomadas: persistencia, mecanismo de extensión,
   protocolo de comunicación, autenticación, organización de módulos, estrategia de pruebas.
2. Escribir un ADR por decisión con estado **`Aceptado (heredado)`**, usando
   `assets/adr-heredado-template.md` (o la plantilla de `generar-tech-design` si está instalada).
   Numerar desde el siguiente número libre en `adrs/`.
3. La Decisión describe lo que el código ya hace, con evidencia. Las Consecuencias incluyen al
   menos un costo real que hoy se paga por esa decisión.

### 4. Catálogo de patrones (capa 2)

Para cada tema relevante (cómo se agrega un endpoint o ruta, acceso a datos, manejo de errores,
configuración, dependencias, pruebas, organización de módulos, textos visibles, extensión):

1. Detectar **cuántas formas distintas conviven** de resolver ese tema, con un ejemplo
   `archivo:línea` de cada una y un conteo aproximado de usos.
2. Proponer cuál es el **canon** (imitar) y cuál el **legado** (no imitar), declarando el
   criterio: lo que recomienda la documentación del proyecto, lo que usa el código más reciente o
   lo mayoritario en el código nuevo.
3. Si no hay un criterio claro, **no se elige**: queda como pregunta para el humano.
4. Incluir explícitamente cómo se conectan las dependencias (inyectadas o importadas directo) y
   qué consecuencia tiene eso para poder probar el código.

### 5. Mapa de deuda (capa 2)

Registrar, **sin arreglar**, cada hallazgo con: id, descripción, evidencia, riesgo (alto · medio ·
bajo) y cuándo conviene atacarlo (normalmente: cuando una feature pase por ahí).

Buscar como mínimo:

- archivos o módulos muy grandes o con demasiadas responsabilidades;
- caminos duplicados para hacer lo mismo;
- compatibilidad heredada que no se puede borrar;
- deuda declarada por el propio equipo (`TODO`, `FIXME`, `HACK`);
- tipos débiles o validaciones ausentes;
- acoplamiento alto (muchos archivos dependen de uno), usando CodeGraph si está disponible.

**Rendimiento:** solo se registran **candidatos a medir**, nunca bugs confirmados sin una medición.

### 6. Reglas de construcción (capa 5)

Derivar las reglas del canon y de los ADRs heredados. Cada regla lleva:

- el enunciado ("las funcionalidades nuevas van como plugin");
- su origen (ADR, patrón canon o documentación del proyecto);
- **cómo se verifica**: un comando, una herramienta o una prueba existente.

Si una regla no tiene forma de verificarse, se marca **regla blanda** y se propone cómo
verificarla (lint, prueba o guardrail con `crear-guardrail`), sin crearla.

### 7. Escribir

| Archivo | Contenido | Plantilla |
|---|---|---|
| `docs/contexto/ARQUITECTURA.md` | Arranque y pruebas verificados, mapa de capas, flujo de punta a punta | `assets/arquitectura-template.md` |
| `docs/contexto/PATRONES.md` | Catálogo canon vs. legado | `assets/patrones-template.md` |
| `docs/contexto/DEUDA.md` | Mapa de deuda | `assets/deuda-template.md` |
| `adrs/NNNN-*.md` | Decisiones heredadas | `assets/adr-heredado-template.md` |
| `AGENTS.md` | **Índice corto** + reglas de construcción | `assets/agents-md-template.md` |

- Si ya existe un `AGENTS.md`, **no se sobrescribe**: se propone el cambio y lo decide el humano.
- `AGENTS.md` deja la entrada al glosario y a las capacidades apuntando a `docs/contexto/`, aunque
  esos archivos los complete el BA.

### 8. Autovalidación

Antes de presentar nada:

- Volver a abrir cada `archivo:línea` citado y confirmar que dice lo que se afirma.
- Confirmar que cada comando documentado fue corrido o está marcado `NO VERIFICADO`.
- Confirmar que ninguna propuesta de mejora quedó escrita como si fuera descripción.

Recomendar al humano una **revisión cruzada**: correr `audit-agent-context` desde una sesión
limpia, idealmente con otro modelo, para que el contexto no se valide a sí mismo.

### 9. Gate humano

Presentar un resumen y las decisiones pendientes:

- canon a confirmar en cada tema con más de un patrón;
- reglas blandas y cómo se propone verificarlas;
- todo lo marcado `NO VERIFICADO`.

**Esperar aprobación explícita.** Nada de este contexto se usa ni se comunica a otros agentes
antes de que el humano lo apruebe.

### 10. Coordinación con el BA

Si hay un BA en la sesión (ver `invoke-agent`), después de la aprobación:

- Enviar `CONTEXTO TÉCNICO LISTO: <rutas de docs/contexto y adrs> — <puntos abiertos>`.
- Cuando el BA envíe `GLOSARIO: TÉRMINOS NUEVOS`, completar la columna "Dónde vive" de cada
  término en `docs/contexto/GLOSARIO.md`, con evidencia, y responder `GLOSARIO COMPLETO`.
- Máximo dos vueltas por el mismo desacuerdo; después decide el humano.

## Constraints

- No modifica código, configuración ni dependencias del proyecto.
- No arregla deuda, aunque sea trivial.
- No elige el canon cuando el criterio no es claro: pregunta.
- No sobrescribe documentación existente sin aprobación.
- No se comunica con otros agentes antes del gate humano.
