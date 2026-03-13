---
name: ia-context-sync
description: Mantiene actualizados Architecture.md, devlog.md, history.md e ia-context.md. Crea los archivos si no existen. Aplica la Golden Rule de sincronización al inicio y al final de cada tarea. Usar cuando se trabaje en un repo con documentación de contexto o cuando el usuario pida mantener docs de contexto.
---

# IA Context Sync

## Cuándo aplicar

- El proyecto tiene (o debe tener) `Architecture.md`, `devlog.md`, `history.md`, `ia-context.md`.
- El usuario pide mantener actualizada la documentación de contexto.
- Al inicio de sesión para cargar contexto; al final de cada tarea para sincronizar docs.

## Instrucciones

1. **Seguir la regla instalada:** `.cursor/rules/ia-context-sync.mdc` (contenido en `rules.md`).
2. **Al iniciar:** Comprobar si existen los cuatro archivos de contexto; **si alguno no existe, crearlo** (con la estructura/plantilla de la regla). Leer Architecture + últimas entradas de history y devlog; incluir en los todos las actualizaciones de documentación necesarias.
3. **Durante la tarea:** Usar Architecture como referencia; tener en el checklist los ítems de actualización de architecture, history, devlog, ia-context.
4. **Al cerrar la tarea:** Ejecutar la fase de documentación (actualizar Architecture por anclas, history, devlog, ia-context si cambia API/pipeline, how-to si aplica).

No dar por completada la tarea sin haber cumplido la fase de documentación.

## Referencia

Ver [rules.md](rules.md) para los MUST y anclas exactos de cada archivo de contexto.
