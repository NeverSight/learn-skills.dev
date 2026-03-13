---
name: cortexfs
description: >-
  CortexFS Memory Skill - Persistent cognitive memory layer backed by CortexFS CLI.
  Allows saving, reading, searching knowledge and session states, scoped by project context.
  Includes automatic CLI installation and commands for OpenCode and Cursor.
  Todos los comandos son BASH/CLI que deben ejecutarse en la TERMINAL/SHELL.
---

# CortexFS Memory Skill

> **Version:** 0.6.0  
> **Execution:** Shell/Bash  
> **Auth:** None

## 🚀 AUTO-INSTALACIÓN (Ejecutar al inicio)

Cuando el skill se carga por primera vez, EL AGENTE DEBE ejecutar automáticamente estos comandos:

### 1. Instalar CortexFS CLI (si no existe)
```bash
if ! command -v cortex &> /dev/null; then
    npm install -g cortexfs-cli
    cortex config "$HOME/.cortexfs/brain"
fi
```

### 2. Copiar comandos a los agentes instalados

**Para OpenCode:**
```bash
mkdir -p ~/.config/opencode/commands
cp -r ~/.agents/skills/cortexfs/opencode-commands/* ~/.config/opencode/commands/
```

**Para Cursor:**
```bash
mkdir -p ~/.cursor/commands
cp -r ~/.agents/skills/cortexfs/opencode-commands/* ~/.cursor/commands/
```

**Verificación:**
```bash
which cortex || echo "NO_INSTALLED"
```

**Si no está instalado, ejecutar:**
```bash
npm install -g cortexfs-cli
```

---

### Prerequisitos

- **CortexFS CLI instalado**
  - Check: `which cortex || cortex --version`
  - Install: `npm install -g cortexfs-cli`

---

# 🧠 COMPORTAMIENTO AUTOMÁTICO DEL AGENTE

Este skill actúa como la **MEMORIA PERSISTENTE** del proyecto.
El agente DEBE seguir estas reglas de comportamiento:

## 🔍 REGLA 1: BUSCAR PRIMERO (Search-First)

**Cuándo:** SIEMPRE que el usuario pregunte algo sobre el proyecto, ANTES de responder o buscar en el código.

**Acción:**
1. Ejecutar: `cortex search "<términos relevantes de la pregunta>"`
2. Si hay resultados, usar `cortex read` para obtener el contenido completo
3. Usar ese conocimiento para responder o complementar la respuesta

**Ejemplos:**

| Pregunta del usuario | Ejecutar primero |
|---------------------|------------------|
| "¿Cómo funciona la autenticación?" | `cortex search 'autenticación auth login'` |
| "¿Cuáles son las convenciones de código?" | `cortex search 'convenciones código estilo'` |
| "¿Qué decisiones de arquitectura tomamos?" | `cortex search 'arquitectura decisiones'` |

**Por qué:** CortexFS contiene conocimiento curado y decisiones previas. Buscar aquí PRIMERO evita repetir trabajo o contradecir decisiones.

---

## 💾 REGLA 2: GUARDAR CONOCIMIENTO IMPORTANTE (Auto-Save)

**Cuándo:** Guardar AUTOMÁTICAMENTE cuando se descubra o defina:

- Decisiones de arquitectura o diseño
- Convenciones de código acordadas
- Patrones o soluciones reutilizables
- Configuraciones importantes del proyecto
- APIs o endpoints documentados
- Bugs importantes y sus soluciones
- Dependencias clave y su propósito
- Flujos de negocio o lógica compleja
- Información que el usuario pide recordar
- Contexto importante que se perdería entre sesiones

**Acción:**
1. Identificar la categoría apropiada
2. Crear un ID semántico descriptivo
3. Estructurar el contenido en JSON
4. Ejecutar: `cortex save "<category>" "<id>" "<contenido JSON>"`

### 📂 Categorías Recomendadas

| Categoría | Usar para |
|-----------|-----------|
| `arquitectura` | Decisiones de diseño, patrones, estructura |
| `convenciones` | Reglas de código, estilo, naming |
| `config` | Configuraciones, variables de entorno, settings |
| `api` | Endpoints, contratos, schemas |
| `bugs` | Problemas encontrados y soluciones |
| `flujos` | Lógica de negocio, workflows, procesos |
| `dependencias` | Librerías importantes y su uso |
| `memoria` | Información general que recordar |

---

## 🔄 REGLA 3: INICIO DE SESIÓN (Session Start)

**Cuándo:** Al inicio de una nueva conversación o sesión.

**Acción:**
1. Ejecutar: `cortex load-state`
2. Revisar el estado anterior para contexto
3. Ejecutar: `cortex list`
4. Conocer qué conocimiento está disponible

**Por qué:** Retomar contexto sin que el usuario tenga que repetir información.

---

## 🏁 REGLA 4: FIN DE SESIÓN (Session End)

**Cuándo:**
- El usuario indica que termina la sesión
- Se completó una tarea importante
- Hubo cambios significativos en el proyecto

**Acción:** Ejecutar `cortex save-state` con JSON estructurado:

```json
{
  "task": "qué se estaba haciendo",
  "status": "in_progress|blocked|review",
  "progress": {
    "completed": [],
    "pending": [],
    "blocked": []
  },
  "context": {
    "files_modified": [],
    "branch": ""
  },
  "next_steps": []
}
```

---

# 📋 COMANDOS DISPONIBLES

## `cortex config`

Configura el directorio raíz del brain.

```bash
cortex config "<path>"
```

**Ejemplo:**
```bash
cortex config '/ruta/al/brain'
```

---

## `cortex save`

Guarda conocimiento estructurado. SIEMPRE estructurar el contenido en JSON o Markdown.

```bash
cortex save "<category>" "<id>" "<content>"
```

**Parámetros:**
- `category`: Categoría del conocimiento (ej: arquitectura, convenciones)
- `id`: Identificador semántico
- `content`: Contenido - DEBE ser JSON estructurado o Markdown organizado

**Ejemplo JSON:**
```bash
cortex save 'agent' 'mi-agente' '{"name":"mi-agente","role":"asistente","capabilities":["buscar","analizar"]}'
```

**Ejemplo Markdown:**
```bash
cortex save 'project' 'readme' '# Proyecto\n\n## Descripción\nTexto aquí...'
```

---

## `cortex read`

Lee conocimiento persistido.

```bash
cortex read "<category>" "<id>"
```

**Ejemplo:**
```bash
cortex read 'agent' 'mi-agente'
```

---

## `cortex update`

Actualiza conocimiento existente.

```bash
cortex update "<category>" "<id>" "<content>"
```

**Ejemplo:**
```bash
cortex update 'agent' 'mi-agente' 'nuevo contenido'
```

---

## `cortex delete`

Elimina conocimiento.

```bash
cortex delete "<category>" "<id>"
```

**Ejemplo:**
```bash
cortex delete 'agent' 'mi-agente'
```

---

## `cortex list`

Lista conocimiento, opcionalmente filtrado por categoría.

```bash
cortex list [category]
```

**Ejemplos:**
```bash
cortex list              # Lista todas las categorías
cortex list 'agent'      # Lista entradas en categoría 'agent'
```

---

## `cortex search`

Busca conocimiento por query.

```bash
cortex search "<query>"
```

**Ejemplo:**
```bash
cortex search 'mi búsqueda'
```

---

## `cortex save-state`

Guarda el estado de la sesión. SIEMPRE usar formato estructurado para facilitar handoff.

```bash
cortex save-state "<summary>"
```

**Formato recomendado JSON:**
```bash
cortex save-state '{"task":"Implementar auth","status":"in_progress","progress":{"completed":["login"],"pending":["logout"]},"next_steps":["agregar tests"]}'
```

**Alternativa compacta:**
```bash
cortex save-state 'TASK: Auth OAuth2 | STATUS: in_progress | DONE: login | PENDING: logout | NEXT: tests'
```

---

## `cortex load-state`

Carga el estado más reciente de la sesión.

```bash
cortex load-state
```

---

# ⚡ FLUJO DE TRABAJO OBLIGATORIO

```
┌─────────────────────────────────────────────────────────┐
│  INICIO DE SESIÓN                                       │
│  1. cortex load-state    → Recuperar contexto anterior  │
│  2. cortex list          → Ver conocimiento disponible  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  CUANDO EL USUARIO PREGUNTE ALGO                        │
│  1. cortex search "..."  → BUSCAR PRIMERO en memoria    │
│  2. cortex read "..." "..."  → Leer detalles si existe  │
│  3. Luego buscar en código si es necesario              │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  CUANDO DESCUBRAS/DEFINAS ALGO IMPORTANTE               │
│  → cortex save "categoria" "id" "{...JSON...}"          │
│                                                         │
│  Guardar: decisiones, convenciones, configs, APIs,      │
│           bugs+soluciones, patrones, flujos de negocio  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  FIN DE SESIÓN / TAREA COMPLETADA                       │
│  → cortex save-state "{...estado estructurado...}"      │
└─────────────────────────────────────────────────────────┘
```

---

# 🔍 Ejemplo Completo: Usuario pregunta algo

**Usuario:** "¿Cómo manejamos los errores en la API?"

```bash
# PASO 1: Buscar primero en CortexFS
cortex search "errores API manejo error handling"

# PASO 2: Si encuentra resultados, leer el contenido
cortex read "convenciones" "error-handling"

# PASO 3: Responder usando ese conocimiento + código si necesario
```

---

# 💾 Ejemplo Completo: Guardar conocimiento importante

Después de definir cómo manejar errores:

```bash
cortex save "convenciones" "error-handling" '{
  "topic": "Manejo de errores en API",
  "rules": [
    "Usar AppError para errores controlados",
    "Logging con nivel según severidad",
    "Respuestas estandarizadas con code y message"
  ],
  "example": "throw new AppError(400, \"VALIDATION_ERROR\", \"Campo requerido\")",
  "decided_on": "2024-01-15",
  "reason": "Consistencia en respuestas de error"
}'
```

---

# ⚠️ Recordatorios Críticos

- **BUSCAR ANTES DE RESPONDER** - CortexFS tiene conocimiento curado
- **GUARDAR PROACTIVAMENTE** - Si es importante, persistirlo
- **ESTRUCTURAR EN JSON** - Facilita búsqueda y lectura futura
- Los comandos `cortex` son ejecutables BASH del sistema
- Requieren permisos de escritura fuera del workspace (usar "all")
