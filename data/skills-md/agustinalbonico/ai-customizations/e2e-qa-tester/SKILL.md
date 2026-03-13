---
name: e2e-qa-tester
description: "Ejecuta pruebas E2E y QA manual usando Playwright MCP para verificar la ultima tarea completada en la conversacion. Usar cuando se necesite: (1) Probar un flujo recien implementado, (2) Verificar que una funcionalidad funciona correctamente, (3) Hacer QA manual de una nueva feature, (4) Testear formularios, flujos de autenticacion, o cualquier interaccion de usuario. El skill busca credenciales en CREDENTIALS.md, intenta conectar al puerto 5173 por defecto, y pide confirmacion antes de ejecutar las pruebas."
---

# E2E QA Tester

Ejecuta pruebas end-to-end y QA manual usando Playwright MCP para verificar funcionalidades recien implementadas.

## Flujo de Trabajo

### 1. Identificar la Tarea a Probar

Antes de ejecutar cualquier prueba, revisa el historial de la conversacion actual para identificar la ultima tarea completada:

```
Busca en los mensajes recientes:
- Tareas marcadas como "completadas" o "done"
- Implementaciones finalizadas
- Features agregadas o modificadas
- Bug fixes aplicados
```

Si no puedes identificar claramente la tarea, pregunta al usuario: "¿Que funcionalidad o flujo debo probar?"

### 2. Buscar Credenciales de Prueba

**SIEMPRE** antes de intentar login, busca credenciales de prueba:

```powershell
# Buscar archivo de credenciales en el proyecto
Get-ChildItem -Path . -Filter "CREDENTIALS.md" -Recurse
```

Ubicaciones comunes:
- `CREDENTIALS.md` (raiz del proyecto)
- `docs/CREDENTIALS.md`
- `.credentials/CREDENTIALS.md`
- `testing/CREDENTIALS.md`

Formato esperado en CREDENTIALS.md:
```markdown
## Usuario Admin
- Email: admin@test.com
- Password: admin123

## Usuario Regular
- Email: user@test.com
- Password: user123
```

**Si NO encuentras CREDENTIALS.md:**
1. Detente y pregunta al usuario por las credenciales
2. NO intentes adivinar ni usar credenciales genericas

### 3. Conectar a la Aplicacion

Intenta conectar al puerto por defecto:

```powershell
# Verificar si puerto 5173 esta en uso
Test-NetConnection -ComputerName 127.0.0.1 -Port 5173 -InformationLevel Quiet
```

- **Si el puerto 5173 esta ocupado**: Usar esa conexion
- **Si el puerto 5173 NO esta en uso**: 
  1. Verificar si hay otro puerto comun (3000, 4200, 8080)
  2. Si no hay ningun puerto activo, preguntar al usuario

### 4. Confirmacion Pre-Prueba (OBLIGATORIO)

Antes de ejecutar cualquier prueba, presenta al usuario:

```
## Plan de Prueba

**Tarea identificada**: [descripcion de la tarea completada]

**Flujo a probar**:
1. [Paso 1]
2. [Paso 2]
3. [Paso 3]

**Credenciales a usar**: [rol/usuario del CREDENTIALS.md]

**URL de inicio**: http://127.0.0.1:[puerto]

¿Procedo con esta prueba? (s/n)
```

**NO proceder hasta recibir confirmacion explicita del usuario.**

Si el usuario rechaza:
1. Pregunta que debe hacer diferente
2. Ajusta el plan segun sus indicaciones
3. Vuelve a pedir confirmacion

### 5. Ejecutar la Prueba

Una vez confirmado, usa Playwright MCP para ejecutar la prueba:

#### Iniciar Navegador (headless)

```
playwright_browser_navigate con url http://127.0.0.1:[puerto]
```

#### Si hay Login requerido

1. Tomar snapshot para ver estado actual
2. Identificar campos de email/usuario y password
3. Completar formulario con credenciales del CREDENTIALS.md
4. Enviar formulario
5. Verificar login exitoso (snapshot, buscar elemento de exito)

#### Ejecutar Flujo de Prueba

1. Navegar a la funcionalidad objetivo
2. Interactuar con elementos segun el flujo identificado
3. Tomar snapshots en puntos clave
4. Verificar resultados esperados

#### Comandos Playwright Utiles

| Accion | Herramienta |
|--------|-------------|
| Ver estado actual | `playwright_browser_snapshot` |
| Navegar | `playwright_browser_navigate` |
| Click | `playwright_browser_click` |
| Escribir texto | `playwright_browser_type` |
| Seleccionar dropdown | `playwright_browser_select_option` |
| Llenar formulario | `playwright_browser_fill_form` |
| Esperar | `playwright_browser_wait_for` |
| Screenshot | `playwright_browser_take_screenshot` |

### 6. Reportar Resultados

Al finalizar, presenta un reporte claro:

```markdown
## Resultado de Prueba E2E

**Estado**: [PASO / FALLO]

**Tarea probada**: [descripcion]

**Pasos ejecutados**:
1. [Paso 1] - [OK/FALLO: razon]
2. [Paso 2] - [OK/FALLO: razon]
3. [Paso 3] - [OK/FALLO: razon]

**Resultado final**:
[Descripcion de que paso, si hubo errores, comportamiento observado]

**Evidencia**:
- [Screenshots tomados o pasos verificados]
```

## Casos de Uso Comunes

### Probar Formulario Nuevo

1. Identificar campos del formulario
2. Completar con datos de prueba validos
3. Enviar y verificar respuesta exitosa
4. Probar validaciones (campos vacios, formatos invalidos)

### Probar Flujo de Autenticacion

1. Verificar pantalla de login
2. Usar credenciales de CREDENTIALS.md
3. Verificar redireccion post-login
4. Verificar elementos visibles solo para usuarios autenticados

### Probar CRUD

1. **Create**: Crear nuevo registro, verificar aparicion en lista
2. **Read**: Verificar datos mostrados correctamente
3. **Update**: Editar registro, verificar cambios persistidos
4. **Delete**: Eliminar registro, verificar desaparece de lista

### Probar Feature Toggle

1. Verificar estado antes de activar feature
2. Activar/trigger la feature
3. Verificar estado despues (UI visible, comportamiento cambiado)

## Manejo de Errores

### Si la aplicacion no carga
1. Verificar que el servidor este corriendo
2. Verificar URL y puerto correctos
3. Reportar al usuario

### Si el login falla
1. Verificar credenciales en CREDENTIALS.md
2. Verificar que el formulario tenga los campos correctos
3. Reportar error especifico al usuario

### Si un elemento no se encuentra
1. Tomar snapshot para ver estado actual
2. Buscar selectores alternativos
3. Si persiste, reportar al usuario con evidencia

### Si hay errores de consola
1. Usar `playwright_browser_console_messages` para obtener errores
2. Incluir en reporte de resultados

## Notas Importantes

- **SIEMPRE** usar modo headless (--headed=false) para no interferir con el usuario
- **SIEMPRE** buscar CREDENTIALS.md antes de pedir credenciales
- **SIEMPRE** pedir confirmacion antes de ejecutar pruebas
- **NUNCA** crear, modificar o eliminar usuarios de prueba
- **NUNCA** usar IPv6, siempre 127.0.0.1
