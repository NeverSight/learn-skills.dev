---
name: blacklist_db
description: Base de datos interna de documentos comprometidos consultada via Redis
type: Algorithm
priority: Recomendada
mode: Self-hosted
---

# blacklist_db

Base de datos interna de números de documento comprometidos, reportados o robados. Se almacena en PostgreSQL y se sirve desde Redis para consultas en menos de 1ms.

## When to use

Usar en el `antifraud_agent` para verificar cada número de documento contra la lista negra. Un match es rechazo automático (hard rule) independiente del score global.

## Instructions

1. Crear tabla en PostgreSQL: `blacklisted_documents(doc_number, reason, added_at, source)`.
2. Sincronizar a Redis como set: `SADD blacklist:documents <doc_number>`.
3. Job de sincronización: cada 5 minutos, actualizar Redis desde PostgreSQL.
4. Consulta: `is_blacklisted = redis.sismember('blacklist:documents', doc_number)`.
5. Si `is_blacklisted == True`, retornar rechazo inmediato con razón.
6. API de administración para agregar/eliminar documentos de la lista.
7. Registrar cada consulta a la blacklist en el log de auditoría.

## Notes

- Usar hashes SHA-256 de los números de documento en lugar del número en texto plano.
- La blacklist debe ser append-only en auditoría; los borrados se marcan como `soft_delete`.
- Implementar also blacklist por device fingerprint y por IP.