---
name: tauri-migration
description: Alias corto para migracion Web a Desktop con Tauri en stack React + NestJS + Postgres en LAN. Usar para aplicar flujo de planificacion, implementacion, verificacion y release con sidecar y reglas de red.
---

# Tauri Migration (Alias)

Usar esta skill cuando pidas el flujo de migracion Tauri de forma abreviada.

## Flujo

1. Planificar
2. Implementar
3. Verificar
4. Liberar

## Reglas clave

- Backend local en `127.0.0.1`
- Base remota por `database.host` con IP fija
- Revisar logs de `%APPDATA%/sistema-caja/` antes de diagnosticar

## Errores tipicos

- `os error 2`: sidecar no encontrado
- `os error 32`: lock de archivos
- `Nest can't resolve JwtAuthGuard (JwtService)`: imports/exports de modulos
