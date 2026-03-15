---
name: prd-creator
description: >
  Genera Product Requirements Documents (PRDs) completos a partir de una conversación interactiva
  con el usuario. Usa preguntas adaptativas con la herramienta `question` para entender el problema,
  clasificar su complejidad, y recopilar requisitos de negocio. El output es un .md orientado a
  problemas de negocio y requisitos (NO técnico). Usar cuando el usuario quiere crear un PRD,
  documentar requisitos de producto, definir un problema a resolver, o dice "quiero un PRD",
  "documentar requisitos", "definir qué vamos a construir".
---

# Protocolo prd-creator

## Flujo general

```
FASE 0: Exploración del Contexto del Proyecto
    ↓ resumen silencioso (no checkpoint — solo informa al usuario)
FASE 1: Recepción del Problema
    ↓ clasificación de complejidad
FASE 2: Entrevista Adaptativa (preguntas con `question` tool)
    ↓ checkpoint — usuario confirma que se entendió bien
FASE 3: Generación del PRD
    ↓ checkpoint — usuario aprueba el .md
FASE 4: Persistencia
```

---

## FASE 0 — Exploración del Contexto del Proyecto

**Objetivo**: Entender el proyecto para contextualizar las preguntas y el PRD.

El agente (silenciosamente, sin preguntar):
1. Lee `package.json` / `go.mod` / `pyproject.toml` / `Cargo.toml` para entender el dominio
2. Lee `README.md` si existe
3. Busca `docs/prd/` para ver PRDs existentes y entender el estilo

**IMPORTANTE**: Esta información es para contexto interno del agente. El PRD de salida NO debe mencionar stack técnico específico — debe ser orientado a negocio y requisitos.

Luego muestra un resumen breve:

```
Entendí el contexto del proyecto:
- Dominio: [dominio detectado]
- PRDs existentes: [lista o "ninguno"]

Contame: ¿qué problema querés resolver o qué necesitás construir?
```

Si el usuario ya proporcionó el problema en su mensaje inicial, saltar directamente a FASE 1.

---

## FASE 1 — Recepción del Problema y Clasificación

**Objetivo**: Recibir el input del usuario y clasificar la complejidad para determinar cuántas preguntas hacer.

### Clasificación de complejidad

Basándose en el input del usuario, clasificar:

| Complejidad | Señales | Rondas de preguntas | Total preguntas aprox |
|-------------|---------|---------------------|-----------------------|
| **simple** | Cambio puntual, mejora menor, scope claro | 0-1 rondas | 0-4 |
| **media** | Feature nueva, múltiples usuarios, algunos flujos | 1-2 rondas | 4-8 |
| **alta** | Sistema nuevo, múltiples actores, reglas de negocio complejas | 2-3 rondas | 8-15 |
| **muy alta** | Plataforma, múltiples módulos, compliance, integraciones | 3-4 rondas | 15-20 |

**Si el usuario ya dio suficiente contexto** (descripción detallada >150 palabras con problema claro, usuarios, alcance): reducir preguntas a solo lo que falta clarificar.

**Si el input es vago** (<30 palabras): empezar con preguntas amplias de descubrimiento.

Mostrar clasificación al usuario:

```
Clasifiqué tu solicitud como complejidad [X].
Voy a hacerte [N] preguntas para entender bien lo que necesitás.
```

---

## FASE 2 — Entrevista Adaptativa

**Objetivo**: Recopilar toda la información de negocio necesaria para el PRD.

### Reglas absolutas

1. **SIEMPRE usar la herramienta `question`** — nunca preguntas en texto plano
2. **Máximo 4 preguntas por ronda** — nunca más
3. **Mezclar preguntas con opciones y abiertas** según el tipo de información necesaria
4. La herramienta `question` agrega "Type your own answer" automáticamente
5. Si una respuesta anterior ya cubre una pregunta → saltarla
6. Si una respuesta genera nueva ambigüedad → agregarla a la siguiente ronda
7. **NUNCA preguntar sobre stack técnico, tecnologías, o implementación** — el PRD es de negocio
8. Adaptar las preguntas al contexto — no usar preguntas genéricas si el usuario ya dio info

### Estructura de rondas

El banco de preguntas completo está en [references/question-bank.md](references/question-bank.md). Consultar ese archivo para elegir las preguntas adecuadas según la complejidad y el tipo de problema.

**Resumen de la estructura**:

```
Ronda 1 → Problema y Contexto + Usuarios y Alcance
           máx 4 preguntas, las más abiertas y amplias

Ronda 2 → Flujos y Comportamiento + Criterios de Éxito
           máx 4 preguntas, adaptadas a respuestas de Ronda 1
           (solo si complejidad >= media)

Ronda 3 → Edge Cases + Priorización
           máx 4 preguntas
           (solo si complejidad >= alta)

Ronda 4 → Restricciones de Negocio + Métricas de Impacto
           máx 4 preguntas
           (solo si complejidad = muy alta)
```

### Al final de cada ronda (excepto la última)

```
Hasta ahora entiendo:
- [bullet resumen]
- [bullet resumen]
- [bullet resumen]

¿Hay algo incorrecto o querés agregar algo antes de continuar?
```

### Checkpoint final de la entrevista

Después de la última ronda, presentar un resumen completo:

```
Resumen de lo que entendí:

**Problema**: [resumen en 1-2 oraciones]
**Usuarios**: [quiénes]
**Alcance**: [qué incluye y qué no]
**Flujos principales**: [resumen]
**Criterios de éxito**: [resumen]

¿Está completo? ¿Falta algo importante antes de generar el PRD?
```

El usuario confirma o hace correcciones.

---

## FASE 3 — Generación del PRD

**Objetivo**: Generar el documento .md completo orientado a negocio.

Usar el template definido en [references/prd-template.md](references/prd-template.md).

### Reglas de generación

| Sección | Regla |
|---------|-------|
| **Problema** | Máx 2 párrafos. Lenguaje de negocio, cero jerga técnica. |
| **Usuarios** | Describir personas con pain points reales, no perfiles genéricos. |
| **Objetivos** | Medibles cuando sea posible. Usar métricas de negocio, no técnicas. |
| **Alcance — fuera de alcance** | Obligatorio con al menos 2 items fuera de alcance. Si el usuario no los mencionó, el agente los propone. |
| **Requisitos funcionales** | Priorizados P0/P1/P2. Cada uno con criterio de aceptación. |
| **Requisitos no funcionales** | Solo si surgieron en la entrevista. Expresados en términos de negocio ("el usuario no debe esperar más de 2 segundos") no técnicos ("latencia < 200ms"). |
| **Flujos** | Solo los que surgieron en la entrevista. Omitir sección si no aplica. |
| **Criterios de éxito** | Formato Gherkin simplificado (Dado/Cuando/Entonces). Siempre se genera — el agente los deriva de los flujos si el usuario no los mencionó. |
| **Riesgos** | Solo si la complejidad es alta o muy alta. |
| **Preguntas abiertas** | Cualquier decisión pendiente o ambigüedad detectada durante la entrevista. |

### Presentación al usuario

Mostrar el PRD completo y preguntar:

```
¿Aprobás este PRD para guardarlo?
Podés pedirme ajustes antes de confirmar.
```

El usuario puede pedir ajustes. El agente los incorpora y vuelve a presentar.

**Checkpoint**: El usuario aprueba el PRD.

---

## FASE 4 — Persistencia

**Objetivo**: Guardar el PRD como archivo .md en el repositorio.

1. Crear el directorio `docs/prd/` si no existe
2. Generar nombre de archivo: `YYYY-MM-DD-<nombre-kebab-case>.md`
   - La fecha es la fecha actual
   - El nombre se deriva del título del PRD en kebab-case
   - Ejemplo: `2026-03-06-sistema-de-notificaciones.md`
3. Escribir el archivo
4. Mostrar confirmación:

```
PRD guardado: docs/prd/YYYY-MM-DD-nombre-del-prd.md

¿Necesitás algo más con este PRD?
```

---

## Ejemplos de uso

### Ejemplo 1: Solicitud simple

Usuario: `"quiero agregar notificaciones por email cuando un pedido cambia de estado"`

→ Complejidad: **simple** (scope claro, un flujo principal)
→ 1 ronda de 3-4 preguntas

```
Pregunta 1: "¿Qué cambios de estado deben disparar la notificación?"
- Todos los cambios
- Solo cambios críticos (cancelado, entregado, devuelto)
- Solo cuando pasa a "enviado" y "entregado"

Pregunta 2: "¿Quién recibe las notificaciones?"
- Solo el cliente que hizo el pedido
- El cliente + el vendedor
- Configurable por el usuario

Pregunta 3: "¿El usuario puede desactivar las notificaciones?"
- Sí, debe poder elegir cuáles recibir
- Sí, todo o nada
- No, siempre se envían
```

### Ejemplo 2: Solicitud compleja

Usuario: `"necesito un sistema de gestión de inventario para nuestros 3 almacenes"`

→ Complejidad: **alta** (múltiples ubicaciones, múltiples actores, reglas de negocio)
→ 3 rondas de 3-4 preguntas cada una

Ronda 1: Problema y contexto
```
Pregunta 1: "¿Cómo gestionan el inventario hoy?"
- Planillas de Excel
- Sistema actual que quieren reemplazar
- No hay sistema, todo manual/verbal

Pregunta 2: "¿Quiénes van a usar el sistema?"
- Solo encargados de almacén
- Encargados + vendedores + gerencia
- Todo el equipo

Pregunta 3: "¿Qué es lo más urgente o doloroso del proceso actual?"
[ABIERTA - que describa el pain point principal]

Pregunta 4: "¿Los 3 almacenes manejan los mismos productos o son independientes?"
- Mismos productos, stock compartido
- Productos distintos por almacén
- Mix: algunos compartidos, otros exclusivos
```

### Ejemplo 3: Solicitud vaga

Usuario: `"quiero mejorar cómo manejamos los clientes"`

→ Complejidad: **no determinada** — necesita preguntas amplias de descubrimiento

```
Pregunta 1: "¿Qué aspecto del manejo de clientes querés mejorar?"
- Seguimiento de conversaciones/contactos
- Gestión de ventas/oportunidades
- Soporte post-venta
- Registro y datos de clientes
- Todo lo anterior

Pregunta 2: "¿Cuál es el problema principal que tenés hoy?"
[ABIERTA - que describa su dolor]

Pregunta 3: "¿Cuántas personas van a usar esto?"
- Solo yo
- Un equipo pequeño (2-5 personas)
- Un equipo mediano (5-20 personas)
- Toda la organización (20+)
```

---

## Reglas CRÍTICAS

1. **SIEMPRE usar herramienta `question`** — nunca preguntas en texto plano
2. **Máximo 4 preguntas por ronda**
3. **El PRD es de NEGOCIO** — nunca mencionar stack técnico, lenguajes, frameworks, bases de datos, APIs en el output
4. **Adaptar las preguntas** — si el usuario ya dio contexto, no preguntar lo obvio
5. **Derivar lo que falta** — si el usuario no mencionó criterios de éxito o items fuera de alcance, el agente los propone
6. **El archivo va en `docs/prd/`** con formato `YYYY-MM-DD-<nombre>.md`
7. **Mezclar preguntas con opciones y abiertas** según el tipo de información
