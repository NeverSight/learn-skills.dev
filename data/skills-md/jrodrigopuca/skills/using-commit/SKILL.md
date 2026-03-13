---
name: using-commit
description: Guía para escribir mensajes de commit siguiendo Conventional Commits. Usar cuando se vaya a realizar un commit, crear mensajes descriptivos, estandarizar el historial del proyecto, o automatizar versionado y changelogs. Incluye tipos de commit, scopes, breaking changes, formato y mejores prácticas. Activar con frases como "hacer commit", "mensaje de commit", "conventional commits", o "escribir commit semántico".
license: MIT
metadata:
  author: jrodrigopuca
  version: "1.0"
---

# Guía de Conventional Commits

Guía completa para escribir mensajes de commit estructurados siguiendo la especificación de Conventional Commits.

## Descripción General

Conventional Commits es una especificación para escribir mensajes de commit legibles por humanos y máquinas. Esta skill proporciona:

- Especificación completa basada en [conventionalcommits.org](https://www.conventionalcommits.org/)
- Tipos estándar de commits y cuándo usarlos
- Formato para scopes, breaking changes y footers
- Patrones para commits Multi-módulo y relacionados
- Mejores prácticas con ejemplos buenos y malos
- Integración con herramientas de versionado semántico

## Requisitos Previos

- Git instalado y configurado
- Conocimientos básicos de control de versiones
- Opcional: Herramientas como commitizen, commitlint, standard-version
- Opcional: Configuración de hooks con husky

## Instrucciones

### 1. Usar el Formato Básico

La estructura de un commit sigue este patrón:

```
<tipo>[scope opcional]: <descripción>

[cuerpo opcional]

[footer(s) opcional(es)]
```

**Ejemplo mínimo:**

```
feat: añadir sistema de autenticación
```

**Ejemplo completo:**

```
feat(auth): implementar login con OAuth2

Añade soporte para autenticación mediante Google y GitHub.
Incluye manejo de tokens y refresh automático.

Closes #123
BREAKING CHANGE: El endpoint /login ahora requiere redirect_uri
```

### 2. Elegir el Tipo Correcto

Los tipos más comunes son:

```bash
# Nuevas funcionalidades
git commit -m "feat: añadir búsqueda por filtros avanzados"

# Corrección de errores
git commit -m "fix: corregir cálculo de impuestos en checkout"

# Cambios en documentación
git commit -m "docs: actualizar guía de instalación"

# Cambios de formato (no afectan funcionalidad)
git commit -m "style: aplicar formato con Prettier"

# Refactorización de código
git commit -m "refactor: simplificar lógica de validación"

# Mejoras de rendimiento
git commit -m "perf: optimizar consulta de usuarios"

# Añadir o actualizar tests
git commit -m "test: añadir tests para módulo de pagos"

# Cambios en build o dependencias
git commit -m "build: actualizar a Node 20"

# Cambios en CI/CD
git commit -m "ci: añadir workflow de GitHub Actions"

# Tareas de mantenimiento
git commit -m "chore: actualizar dependencias"
```

Para una lista completa de tipos y cuándo usar cada uno, ver [references/tipos.md](references/tipos.md).

### 3. Especificar Scope (Ámbito)

El scope indica qué parte del proyecto se modificó:

```bash
# Por módulo/componente
git commit -m "feat(parser): añadir soporte para JSON5"
git commit -m "fix(navbar): corregir menu en móviles"

# Por capa de aplicación
git commit -m "refactor(api): extraer lógica de negocio"
git commit -m "test(service): añadir tests unitarios"

# Por funcionalidad
git commit -m "feat(i18n): añadir traducciones al francés"
git commit -m "fix(auth): resolver timeout en login"

# Múltiples scopes (separados por coma)
git commit -m "fix(auth,api): sincronizar validación de tokens"

# Sin scope (cuando afecta todo el proyecto)
git commit -m "chore: migrar a TypeScript 5"
```

### 4. Escribir Descripciones Claras

La descripción debe ser concisa e imperativa:

```bash
# ✅ BIEN - Modo imperativo, claro
git commit -m "feat: añadir validación de email"
git commit -m "fix: prevenir race condition en cache"
git commit -m "refactor: extraer utilidades de fecha"

# ❌ MAL - Tiempo pasado o poco descriptivo
git commit -m "feat: añadido un feature"  # Vago
git commit -m "fix: arreglé el bug"       # Tiempo pasado
git commit -m "update"                    # Sin tipo ni contexto
```

**Reglas para la descripción:**

- Máximo 72 caracteres (idealmente 50)
- Minúscula después de los dos puntos
- Sin punto final
- Modo imperativo: "añadir" no "añadido", "corregir" no "corrigió"

### 5. Añadir Cuerpo para Contexto

El cuerpo explica el **qué** y **por qué**, no el **cómo**:

```bash
git commit -m "feat(cache): implementar estrategia LRU

Reemplaza el cache simple por un LRU para optimizar memoria.
Esto previene que el cache crezca indefinidamente en
aplicaciones long-running.

La implementación usa un Map con orden de inserción para
track el último acceso a cada entrada.
"
```

**Mejores prácticas para el cuerpo:**

- Separar de la descripción con una línea en blanco
- Máximo 72 caracteres por línea
- Explicar motivación y contexto
- Mencionar trade-offs o decisiones importantes

### 6. Indicar Breaking Changes

Para cambios que rompen compatibilidad:

```bash
# Opción 1: ! después del tipo/scope
git commit -m "feat(api)!: cambiar formato de respuesta JSON

BREAKING CHANGE: El campo 'user_id' ahora se llama 'userId'.
Actualizar código cliente para usar la nueva nomenclatura."

# Opción 2: BREAKING CHANGE en el footer
git commit -m "refactor: reorganizar estructura de exports

BREAKING CHANGE: Los módulos internos ya no son exportados.
Usar solo los exports del index principal."

# Con multiple footers
git commit -m "feat(auth)!: migrar a JWT

Reemplaza sesiones basadas en cookies por tokens JWT.

BREAKING CHANGE: Requiere actualizar auth middleware.
Closes #456
Reviewed-by: @tech-lead
"
```

### 7. Usar Footers para Metadata

Los footers agregan información extra:

```bash
# Referencias a issues
git commit -m "fix(parser): manejar strings vacíos

Closes #234
Fixes #567
See also: #890"

# Revisores y co-autores
git commit -m "feat: añadir modo dark

Co-authored-by: Juan Pérez <juan@example.com>
Reviewed-by: María García <maria@example.com>"

# Información de despliegue
git commit -m "chore: actualizar versión

Refs: #456
Deployed-to: production
Release-notes: https://example.com/v2.0"

# Breaking change con contexto
git commit -m "refactor(api)!: cambiar estructura de endpoints

BREAKING CHANGE: Los endpoints ahora usan /api/v2 como base.
Migration-guide: docs/migration-v2.md
Deprecated: /api/v1 (soporte hasta 2026-06-01)"
```

#### Referencias a Tickets JIRA

Para proyectos que usan JIRA, incluye el ticket en los footers:

```bash
# Un solo ticket JIRA
git commit -m "feat(checkout): añadir opción de pago con PayPal

Implementa integración completa con PayPal SDK.
Incluye manejo de webhooks para confirmación.

JIRA: PROJ-1234"

# Múltiples tickets relacionados
git commit -m "fix(api): corregir validación de tokens expirados

Corrige bugs relacionados con refresh de tokens
y manejo de expiración en peticiones concurrentes.

JIRA: PROJ-456, PROJ-789
Fixes: PROJ-890"

# Ticket en el subject (formato alternativo)
git commit -m "[PROJ-1234] feat(checkout): añadir pago con PayPal"

# Combinado con otros footers
git commit -m "feat(reports)!: migrar a nueva API de reportes

BREAKING CHANGE: La API antigua quedará deprecada.
Closes #123
JIRA: PROJ-567
Reviewed-by: @team-lead"
```

**Formatos comunes para JIRA:**

- **En footer (recomendado)**: `JIRA: PROJ-1234` o `Refs: PROJ-1234`
- **En subject**: `[PROJ-1234] tipo(scope): descripción`
- **Múltiples tickets**: `JIRA: PROJ-123, PROJ-456` o en líneas separadas

**Mejores prácticas JIRA:**

- Un solo ticket principal por commit (preferible)
- Si hay múltiples, listar el principal primero
- Usar formato consistente en todo el equipo
- Configurar integración JIRA-Git para enlace automático

### 8. Aplicar Mejores Prácticas

1. **Un commit = un cambio lógico** - No mezclar refactor con feature
2. **Commits atómicos** - Cada commit debe dejar el código funcional
3. **Descripción descriptiva** - Que se entienda sin ver el diff
4. **Usar scope consistentemente** - Definir scopes en el equipo
5. **Breaking changes explícitos** - Siempre documentar incompatibilidades
6. **Tests antes de commit** - Verificar que todo funciona

Para ejemplos detallados de commits buenos y malos, ver [references/buenas-practicas.md](references/buenas-practicas.md).

## Tipos de Commit

Para referencia rápida:

| Tipo                        | Uso                                 | Afecta semver     |
| --------------------------- | ----------------------------------- | ----------------- |
| `feat`                      | Nueva funcionalidad                 | MINOR (0.X.0)     |
| `fix`                       | Corrección de bug                   | PATCH (0.0.X)     |
| `docs`                      | Solo documentación                  | -                 |
| `style`                     | Formato, espacios (no lógica)       | -                 |
| `refactor`                  | Cambio de código sin bug ni feature | -                 |
| `perf`                      | Mejora de rendimiento               | PATCH (0.0.X)     |
| `test`                      | Añadir o corregir tests             | -                 |
| `build`                     | Sistema build, dependencias         | -                 |
| `ci`                        | Scripts CI/CD                       | -                 |
| `chore`                     | Tareas mantenimiento                | -                 |
| `revert`                    | Revertir commit anterior            | Varía             |
| **!** o **BREAKING CHANGE** | Cambio incompatible                 | **MAJOR (X.0.0)** |

Ver [references/tipos.md](references/tipos.md) para descripción completa.

## Salida Esperada

Al usar Conventional Commits obtienes:

- **Historial legible** - Commits estructurados fáciles de buscar y filtrar
- **Changelogs automáticos** - Herramientas como standard-version generan CHANGELOG.md
- **Versionado semántico** - Determina automáticamente la próxima versión
- **Integración CI/CD** - Hooks que validan formato antes de push
- **Búsqueda eficiente** - `git log --grep="^feat"` encuentra todas las features
- **Releases automatizados** - Semantic-release publica basándose en commits

## Ejemplos

**Ejemplo: Feature con scope y breaking change**

Situación: Modificas la API de autenticación para usar headers en lugar de cookies.

```bash
git commit -m "feat(auth)!: migrar autenticación a headers

Cambiamos de cookies a Authorization header con Bearer tokens
para mejorar compatibilidad con aplicaciones móviles y SPAs.

Beneficios:
- Menor complejidad en CORS
- Mejor soporte para apps nativas
- Tokens con expiración explícita

BREAKING CHANGE: Los clientes deben enviar tokens en el header
Authorization en lugar de cookies. Ver guía de migración en
docs/auth-migration.md

Closes #789
"
```

**Ejemplo: Fix con contexto y referencias**

Situación: Corriges un race condition que causaba datos duplicados.

```bash
git commit -m "fix(database): prevenir inserción duplicada en race condition

Añade lock optimista usando version field para prevenir que
requests concurrentes creen registros duplicados.

El bug ocurría cuando múltiples workers procesaban el mismo
evento simultáneamente. Ahora el segundo insert falla y se
reintenta leyendo el registro existente.

Fixes #456
Related: #234, #345
"
```

**Ejemplo: Chore simple sin cuerpo**

Situación: Actualizas las dependencias del proyecto.

```bash
git commit -m "chore(deps): actualizar dependencias a últimas versiones"
```

**Ejemplo: Docs con múltiples scopes**

Situación: Actualizas README y añades ejemplos en varios componentes.

```bash
git commit -m "docs(readme,examples): actualizar guía de inicio rápido

Añade sección de troubleshooting común y ejemplos actualizados
para la v2.0 de la API.
"
```

## Recursos

- [Conventional Commits](https://www.conventionalcommits.org/) - Especificación oficial
- [Semantic Versioning](https://semver.org/) - Versionado semántico 2.0.0
- [Commitizen](https://github.com/commitizen/cz-cli) - CLI interactivo para commits
- [Commitlint](https://commitlint.js.org/) - Validador de mensajes de commit
- [Standard Version](https://github.com/conventional-changelog/standard-version) - Versionado automático
- [Semantic Release](https://semantic-release.gitbook.io/) - Releases automatizados
- [Husky](https://typicode.github.io/husky/) - Git hooks para validación
- [references/tipos.md](references/tipos.md) - Referencia completa de tipos de commit
- [references/buenas-practicas.md](references/buenas-practicas.md) - Ejemplos detallados y errores comunes
