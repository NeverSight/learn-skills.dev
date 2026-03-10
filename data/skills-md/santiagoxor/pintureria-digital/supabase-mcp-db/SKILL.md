---
name: supabase-mcp-db
description: Apply Supabase migrations and manage the database using the Supabase MCP (user-supabase-SantiagoXOR). Use when the user asks to apply migrations, run migrations with MCP, manage the DB with Supabase MCP, list migrations, execute SQL, or inspect schema.
---

# Supabase MCP: migraciones y base de datos

## Cuándo usar esta skill

- El usuario pide **aplicar migraciones** (con MCP o "con tools mcp").
- Pide **gestionar la base de datos** usando el MCP de Supabase.
- Necesitas **listar migraciones aplicadas**, **ejecutar SQL** o **consultar esquema** sin usar la CLI local.

**Servidor MCP:** `user-supabase-SantiagoXOR`. Usar `call_mcp_tool` con este server.

---

## Aplicar una migración

1. **Leer el SQL** del archivo en `supabase/migrations/*.sql`.
2. **Nombre en snake_case:** usar el nombre del archivo sin fecha ni extensión (ej. `20260224100000_create_push_subscriptions.sql` → `create_push_subscriptions`).
3. **Llamar al MCP:**

   ```
   call_mcp_tool
   server: user-supabase-SantiagoXOR
   toolName: apply_migration
   arguments: { "name": "<snake_case_name>", "query": "<contenido SQL completo>" }
   ```

4. **Si falla por tipos en RLS** (ej. `operator does not exist: text = uuid`): en las políticas que usen `auth.uid()` o FKs, usar casts explícitos (`auth.uid()::text`, `user_id::text IN (SELECT id::text FROM ...)`). Corregir el archivo de migración en el repo y volver a aplicar.

**Importante:** Para DDL (CREATE TABLE, ALTER, políticas RLS, etc.) usar siempre `apply_migration`, no `execute_sql`.

---

## Otras herramientas útiles del MCP

| Herramienta | Uso |
|-------------|-----|
| `list_migrations` | Ver migraciones ya aplicadas en la DB (sin argumentos). |
| `execute_sql` | Ejecutar SELECT o DML (INSERT/UPDATE/DELETE). No usar para DDL; para eso usar `apply_migration`. |
| `list_tables` | Listar tablas del esquema (consultar descriptor en `mcps/user-supabase-SantiagoXOR/tools/list_tables.json` si hace falta). |
| `get_advisors` | Recomendaciones del proyecto Supabase. |
| `get_logs` | Logs del proyecto. |

Todas con `call_mcp_tool`, `server: user-supabase-SantiagoXOR`, `toolName: <nombre>`, `arguments: { ... }` según el descriptor en `mcps/user-supabase-SantiagoXOR/tools/<nombre>.json`.

---

## Orden al aplicar varias migraciones

Aplicar en **orden cronológico** (por prefijo de fecha en el nombre del archivo). Si una falla, corregir y reaplicar solo esa antes de seguir.

---

## Referencia

- Listado de herramientas y parámetros: [reference.md](reference.md).
- Antes de llamar una herramienta, leer el descriptor en `mcps/user-supabase-SantiagoXOR/tools/<toolName>.json` para argumentos requeridos.
