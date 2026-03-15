---
name: linus-kiss-dry-yagni
description: Refactoriza código existente complejo. Usa esta skill cuando el usuario pida simplificar, reescribir, limpiar o mejorar código con funciones largas, código duplicado, anidamiento profundo, parámetros excesivos, lógica críptica tipo clever, dependencias inyectadas o sobre-ingeniería. Aplica KISS, DRY, YAGNI y filosofía Linus Torvalds.
---

# KISS-DRY-YAGNI + Linus Torvalds

Skill directiva de simplicidad. Aplica correcciones automáticamente.

## Quick Reference

| Situación | Recurso |
|-----------|---------|
| Aplicar correcciones | Usa tablas abajo |
| Anti-patrones comunes | `resources/anti-patterns/common.md` |
| Límites y métricas | `resources/decision/metrics.md` |
| Diseñar desde cero | `resources/design/kiss-driven-design.md` |
| Ejemplos Python | `resources/examples/python.md` |
| Ejemplos TypeScript | `resources/examples/typescript.md` |
| Ejemplos Go | `resources/examples/go.md` |
| Ejemplos Kotlin | `resources/examples/kotlin.md` |
| Ejemplos Rust | `resources/examples/rust.md` |
| Decisión arquitectónica | `resources/decision/framework.md` |
| Principios Linus | `resources/principles/linus-torvalds.md` |
| Case studies | `resources/cases/case-studies.md` |
| Estrategias simplificación | `resources/strategies/simplification-strategies.md` |
| Fundamentos | `resources/principles/fundamentals.md` |
| Protección de seguridad | `resources/security/safety-guards.md` |

## Límites Concretos (NO Negociables)

Estos son los límites máximos. Si los excedes, debes refactorizar:

| Elemento | Límite Máximo | Qué hacer si se excede |
|----------|---------------|------------------------|
| **Líneas por función** | 20 | Dividir en funciones más pequeñas (ver excepciones abajo) |
| **Parámetros por función** | 4 | Usar objeto/struct para agrupar |
| **Niveles de anidamiento** | 2 | Usar guard clauses |
| **Clases por archivo** | 1 | Separar en archivos |
| **Responsabilidades por clase** | 1 | Extraer responsabilidades |
| **Duplicación de código** | 0 veces | Extraer función común |
| **Interfaces sin uso** | 0 | Eliminar hasta necesitar (excepto código de seguridad) |
| **Comentarios "qué"** | 0 | Renombrar código (preservar comentarios `SECURITY:`) |

### ⚠️ Excepción Crítica: Código de Seguridad

El código de seguridad tiene límites ampliados (ver `resources/security/safety-guards.md`):

| Elemento | Código Normal | Código de Seguridad |
|----------|---------------|---------------------|
| **Líneas por función** | Max 20 | **Max 50** (validaciones completas requieren espacio) |
| **Niveles de anidamiento** | Max 2 | **Max 4** (validaciones múltiples necesitan profundidad) |
| **Parámetros por función** | Max 4 | **Max 6** (configuración de seguridad puede necesitar más) |
| **Interfaces con 1 uso** | Eliminar | **Mantener** (auth/encryption pueden necesitar otra implementación) |
| **Código "por si acaso"** | Eliminar | **Preservar** (defensa en profundidad es necesaria) |
| **Comentarios** | Eliminar "qué" | **Preservar** si contienen `NUNCA`, `CVE`, `SECURITY` |

**¿Qué es código de seguridad?**
- Funciones con prefijos: `validate*`, `sanitize*`, `authenticate*`, `hash*`, `encrypt*`, `verify*`
- Uso de bibliotecas: `bcrypt`, `argon2`, `jsonwebtoken`, `helmet`, `csurf`, `DOMPurify`
- Comparaciones de secrets/tokens/passwords
- Headers de seguridad HTTP
- SQL parametrizado/prepared statements

**Regla de oro:** "La simplicidad nunca debe sacrificar la seguridad. Un código simple pero inseguro es peor que código complejo pero seguro."

## Anti-Patrones Comunes

| Anti-Patrón | Señales de Alerta | Solución Inmediata |
|-------------|-------------------|-------------------|
| **Pyramid of Doom** | 3+ niveles de if/else | Guard clauses con returns tempranos |
| **God Function** | Función hace 3+ cosas | Dividir en funciones de 1 responsabilidad |
| **Parameter Explosion** | 5+ parámetros | Objeto/struct config |
| **Interface Pollution** | Interface con 1 implementación | Eliminar interface, usar clase directa |
| **Abstraction Addiction** | Fábricas de fábricas | Simplificar a funciones directas |
| **Future Proofing** | Código "por si acaso" | Eliminar, agregar solo cuando se necesite |
| **Clever Code** | One-liners crípticos | Expandir a código obvio y legible |
| **Comment Cancer** | Comentarios explicando "qué" | Renombrar variables/funciones |

## Reglas de Aplicación Automática

### KISS - Simplificar

| Si detectas | Aplicar |
|------------|---------|
| Función hace 2+ cosas | Dividir en funciones separadas |
| 4+ niveles de anidamiento | Extraer función o usar guard clauses |
| 5+ parámetros | Usar objeto/config struct |
| Nombre necesita comentario | Renombrar |
| Existe solución más simple | Usarla |
| One-liner críptico | Expandir a múltiples líneas claras |
| Lógica compleja sin tests | Simplificar primero, testear después |

### DRY - Centralizar

| Si detectas | Aplicar |
|------------|---------|
| Código idéntico 2+ veces | Extraer función |
| Constantes repetidas | Centralizar |
| Validaciones similares | Crear utilidad común (ver excepción abajo) |
| Estructura de datos duplicada | Extraer tipo/interfaz |

**Advertencia**: Código que PARECE igual pero representa conceptos distintos → mantener separado.

**⚠️ Excepción de Seguridad: Validaciones por Contexto de Confianza**

DRY NO aplica cuando el mismo tipo de dato necesita validaciones diferentes según el contexto:

```python
# API pública - validación estricta
def create_user_public(data):
    validate_email_strict(data['email'])      # No temp emails
    validate_password_strong(data['password'])  # Complejidad requerida

# Admin interno - validación relajada
def create_user_admin(data):
    validate_email_basic(data['email'])       # Cualquier email válido
    # Password generado automáticamente, no validar complejidad
```

**Por qué mantener separado:** Diferentes threat models (público vs interno) y diferentes casos de uso. Centralizar crearía un único punto de fallo.

### YAGNI - Eliminar

| Si detectas | Aplicar |
|------------|---------|
| Feature "por si acaso" | Eliminar (excepto defensa en profundidad de seguridad) |
| Abstracción sin uso actual | Eliminar (excepto código de seguridad crítico) |
| Interface con 1 implementación | Eliminar (excepto auth/crypto/encryption) |
| Configuración no requerida | Eliminar |
| Código comentado | Eliminar (está en git) |
| Métodos no usados | Eliminar |
| Dependencias no usadas | Eliminar de imports/requires (excepto librerías de seguridad) |

**⚠️ YAGNI NO aplica a:**
- Validación de entrada en múltiples capas (MIME + extensión + magic bytes)
- Rate limiting en endpoints de autenticación
- Headers de seguridad HTTP (HSTS, CSP, X-Frame-Options)
- Logging de auditoría para acciones sensibles
- Manejo de errores que no filtra información sensible
- Graceful shutdown para integridad de datos

Ver `resources/security/safety-guards.md` para lista completa.

### Orden de Prioridad

1. **YAGNI** → Eliminar primero
2. **KISS** → Simplificar segundo
3. **DRY** → Centralizar tercero

Este orden evita crear abstracciones sobre código que debería eliminarse.

### Excepción: Archivos Esenciales de Proyecto

Los archivos de configuración y estructura de proyecto necesarios para que el código compile/ejecute **NO son YAGNI**. Al crear proyectos nuevos, incluir siempre los archivos esenciales que el lenguaje/framework requiere para funcionar.

## Casos de Estudio Rápidos

### Caso 1: Función God
**Antes**: 80 líneas, valida, calcula, guarda, notifica
**Después**: 4 funciones de 15 líneas cada una
**Por qué**: Cada función hace una cosa, testeable, reusable

### Caso 2: Anidamiento Profundo
**Antes**: 6 niveles de if → imposible de seguir
**Después**: Guard clauses planas → flujo lineal
**Por qué**: El código debe ser legible de arriba a abajo

### Caso 3: Sobre-ingeniería
**Antes**: Interface + Factory + Strategy para 2 opciones
**Después**: If/else o diccionario de funciones
**Por qué**: La simplicidad vence a la "elegancia" teórica

### Caso 4: Duplicación
**Antes**: Validación de email en 5 lugares diferentes
**Después**: Función `isValidEmail()` usada en los 5 lugares
**Por qué**: Un cambio en un solo lugar

## Formato de Salida

**IMPORTANTE**: Siempre ESCRIBIR los archivos al sistema. No solo mostrar código.

```
### Archivos Creados
- path/to/archivo.go (descripción breve)

### Correcciones Aplicadas
- [KISS] Descripción del cambio
- [YAGNI] Descripción del cambio
- [DRY] Descripción del cambio
- [LINUS] Descripción del cambio

### Protecciones de Seguridad Aplicadas
- [SECURITY] Qué se preservó y por qué
- [SECURITY] Verificaciones post-simplificación
- [SECURITY] Código identificado como crítico (no simplificado)
```

**Sin preguntas. Sin confirmaciones. Escribir archivos directamente.**

**⚠️ Excepción**: Si se detecta código de seguridad crítico que podría verse afectado, verificar con `resources/security/safety-guards.md` antes de proceder.

## Checklist Antes de Entregar

### Checklist KISS-DRY-YAGNI
- [ ] Funciones tienen ≤20 líneas
- [ ] Máximo 4 parámetros por función
- [ ] Máximo 2 niveles de anidamiento
- [ ] Sin código duplicado
- [ ] Sin interfaces con 1 implementación
- [ ] Sin código "por si acaso"
- [ ] Nombres describen el "qué", no necesitan comentarios
- [ ] Código legible sin explicaciones adicionales

### ⚠️ Checklist de Seguridad (CRÍTICO)
- [ ] **Validaciones preservadas**: ¿Todas las validaciones de entrada siguen presentes?
- [ ] **Sanitización**: ¿Los datos de usuario se sanitizan antes de usar?
- [ ] **SQL seguro**: ¿No se introdujo string interpolation en SQL?
- [ ] **Headers de seguridad**: ¿Se preservaron los headers de seguridad?
- [ ] **Manejo de errores**: ¿Los errores no filtran información sensible?
- [ ] **Password hashing**: ¿Se mantuvo el uso de bcrypt/argon2?
- [ ] **CSRF/Tokens**: ¿Se preservaron las protecciones contra CSRF?
- [ ] **Rate limiting**: ¿Se mantuvo el rate limiting en endpoints críticos?
- [ ] **Comentarios de seguridad**: ¿Se preservaron comentarios críticos (`// NUNCA`, `// CVE`, `// SECURITY`)?
- [ ] **Código de seguridad**: ¿No se simplificó a expensas de la protección?

### Excepciones Aplicadas
- [ ] Código de seguridad identificado y preservado (ver `resources/security/safety-guards.md`)
- [ ] Funciones de seguridad con >20 líneas justificadas
- [ ] Validaciones por contexto de confianza mantenidas separadas (no DRY)
- [ ] Comentarios `SECURITY:` preservados

## Cómo Usar

`/kiss-dry-yagni [código o descripción]`

Aplica automáticamente cuando:
- Usuario pide refactorizar código
- Usuario pide simplificar código
- Usuario pide limpiar código
- Usuario pide revisar código
- Hay código con múltiples problemas obvios
- Se detecta sobre-ingeniería
- Se detecta código duplicado

NO aplica cuando:
- Usuario pide explícitamente prototipo/throwaway
- Usuario deshabilita la skill
