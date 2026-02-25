---
name: tauri-react-nest-lan-migration
description: Migrar aplicaciones React + NestJS + Postgres desde web a desktop con Tauri en entornos LAN. Usar cuando se necesite planificar, implementar, verificar y preparar release con backend local en 127.0.0.1, base remota por IP fija, sidecar estable y diagnostico de logs de arranque.
---

# Tauri React + Nest LAN Migration

Aplicar este flujo en orden para minimizar riesgos en migraciones Web -> Desktop.

## Flujo recomendado

1. Planificar migracion
2. Implementar cambios en backend/frontend/tauri
3. Verificar setup, login y CRUD con logs
4. Preparar release instalable

## Reglas LAN obligatorias

- Backend desktop siempre local: `127.0.0.1`
- Base de datos remota: IP fija del servidor en `database.host`
- No usar `localhost` como host de DB en clientes LAN

## Logs a revisar primero

- `%APPDATA%/sistema-caja/debug_startup.log`
- `%APPDATA%/sistema-caja/logs/error-YYYY-MM-DD.log`
- `%APPDATA%/sistema-caja/logs/application-YYYY-MM-DD.log`

## Diagnostico rapido de errores frecuentes

- `Cannot POST /api/config/test`
  - Backend en modo normal y no en setup

- `failed to fetch`
  - Backend caido o reiniciando (race de arranque)

- `Unexpected token` al parsear config
  - Archivo con BOM (ej. `config.json`)

- `os error 2`
  - Path o nombre de sidecar mal resuelto

- `os error 32`
  - Archivos bloqueados durante extraccion/uso

- `Nest can't resolve JwtAuthGuard (JwtService)`
  - Modulo de auth no importado/exportado donde corresponde

## Checklist de verificacion minima

- Setup inicial abre y guarda configuracion
- Login funciona con backend sidecar
- CRUD critico funciona con DB remota por IP
- No hay errores bloqueantes en logs de startup

## Criterio Go/No-Go

- Go: setup + login + CRUD + logs estables
- No-Go: errores de sidecar, caidas de backend, o fallas en auth/DB
