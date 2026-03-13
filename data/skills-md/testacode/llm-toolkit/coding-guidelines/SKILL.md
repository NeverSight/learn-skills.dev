---
name: coding-guidelines
description: Principios para escribir codigo de calidad. Usa cuando el usuario diga "buenas practicas", "best practices", "coding guidelines", "code quality", "clean code", "principios de codigo", "refactorizar con principios", "refactor with principles", o quiera seguir patrones de calidad.
allowed-tools: Read, Grep, Glob
---

# Coding Guidelines

Principios core para trabajar con LLMs en tareas de desarrollo.

## 4 Principios

### 1. Pensa Antes de Codear

**NO empezar a escribir codigo inmediatamente.**

- Surfacea assumptions antes de implementar
- Pregunta sobre preferencias: estructuras de datos, patrones, librerias
- Presenta multiples opciones con trade-offs
- Confirma alineamiento antes de codear

### 2. Simplicidad Primero

**El codigo mas simple que resuelve el problema.**

- KISS, DRY, YAGNI siempre
- Sin abstracciones especulativas ("por si algun dia...")
- Sin features no pedidas
- Sin over-engineering: 3 lineas similares > abstraccion prematura

### 3. Cambios Quirurgicos

**Editar lo minimo necesario.**

- Matchear patterns existentes del codebase
- No refactorizar codigo que no toca la feature
- No agregar docstrings/comments donde no habia
- No cambiar estilo/formato de codigo existente

### 4. Objetivos Verificables

**Criterios claros para saber cuando esta listo.**

- Definir que significa "funciona"
- Tests que validen el comportamiento esperado
- Checkear lint, types, build antes de terminar

## Aplicacion por Lenguaje

Ver referencias para reglas especificas:

- `references/typescript.md` - TypeScript strict mode, testing, estructura
- `references/python.md` - Type hints, mypy, pytest, ruff

## Ejemplos de Uso

### Ejemplo 1: Usuario pide agregar feature de logging

**Usuario:** "Agregá logging a este servicio"

**MAL (sin consultar):**
```typescript
// Empezar a agregar winston, estructurar logs, crear middleware...
import winston from 'winston';
const logger = winston.createLogger({...});
```

**BIEN (consultar primero):**
```
Antes de agregar logging, necesito entender:

1. ¿Qué librería de logging prefieren? (winston, pino, console estructurado)
2. ¿A dónde van los logs? (stdout, archivo, servicio externo)
3. ¿Qué nivel de detalle? (solo errores, debug incluido)
4. ¿Hay un formato estándar en el proyecto?

Vi que ya usan console.log en otros lugares. ¿Prefieren mantener
consistencia o migrar todo a una librería?
```

### Ejemplo 2: Usuario pide refactorizar

**Usuario:** "Este archivo está muy largo, refactorizalo"

**MAL (hacer todo):**
```typescript
// Extraer todo a archivos separados, agregar types, cambiar naming...
```

**BIEN (proponer opciones):**
```
El archivo tiene 450 líneas. Opciones:

A) Extraer helpers a utils/helpers.ts (reduce a ~300 líneas)
B) Separar por dominio: user.ts, auth.ts, session.ts
C) Solo extraer la función más larga (validateUserSession, 80 líneas)

¿Cuál preferís? Recomiendo C porque es el cambio mínimo
que mejora legibilidad sin reestructurar todo.
```

### Ejemplo 3: Usuario pide implementar validación

**Usuario:** "Agregá validación al form de registro"

**MAL (asumir):**
```typescript
// Instalar zod, crear schemas, agregar validación client y server...
import { z } from 'zod';
const userSchema = z.object({...});
```

**BIEN (preguntar scope):**
```
¿Qué tipo de validación necesitás?

1. Solo frontend (mostrar errores en el form)
2. Solo backend (retornar 400 con errores)
3. Ambos (schema compartido)

Vi que el proyecto usa yup en otros forms.
¿Sigo con yup o preferís otra librería?
```

## Anti-patrones

### ❌ Saltar a codear sin discutir

```typescript
// Usuario: "Agregá cache"
// Inmediatamente:
import Redis from 'ioredis';
const redis = new Redis(); // ← ¿Quién pidió Redis?
```

**Problema:** Asumiste Redis cuando podría ser in-memory, localStorage, o un servicio externo.

### ❌ Agregar features "por las dudas"

```typescript
// Te pidieron: agregar un botón de logout
// Agregaste:
<Button onClick={logout}>Logout</Button>
<ConfirmModal /> {/* ← Nadie pidió confirmación */}
<SessionTimeoutWarning /> {/* ← Nadie pidió esto */}
```

**Problema:** Features no solicitadas = código extra que mantener.

### ❌ Refactorizar de paso

```typescript
// Te pidieron: corregir bug en calculateTotal()
// Hiciste:
- function calculateTotal(items) {
+ function calculateTotal(items: CartItem[]): Money { // ← Tipos nuevos
    // ... fix del bug ...
  }
+ // También renombré variables para mayor claridad ← NO
+ // Y extraje la lógica de descuentos ← NO
```

**Problema:** El PR tiene cambios mezclados, difícil de revisar.

### ❌ Over-engineering

```typescript
// Te pidieron: guardar preferencia de tema (dark/light)
// Hiciste:
class ThemeManager implements IThemeProvider {
  private strategy: ThemeStrategy;
  private observers: ThemeObserver[] = [];
  constructor(config: ThemeConfig) { ... }
}

// Cuando bastaba:
localStorage.setItem('theme', 'dark');
```

**Problema:** Complejidad innecesaria. Un boolean no necesita un patrón Observer.

### ❌ Asumir en vez de preguntar

```typescript
// Usuario: "No funciona el login"
// Empezaste a reescribir el auth flow completo...

// Cuando el bug era:
- if (password = storedHash) // typo: = en vez de ===
+ if (password === storedHash)
```

**Problema:** Investigar primero, preguntar qué error ven, antes de reescribir.
