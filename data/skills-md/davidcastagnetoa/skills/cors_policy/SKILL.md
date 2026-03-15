---
name: cors_policy
description: Control de orígenes permitidos para peticiones cross-origin desde el frontend
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# cors_policy

La política CORS define qué dominios frontend pueden realizar peticiones al API KYC. Una configuración incorrecta (wildcard `*`) permite a cualquier web maliciosa hacer peticiones en nombre del usuario autenticado.

## When to use

Configurar antes de exponer cualquier endpoint. Aplicar tanto en FastAPI (para dev) como en Nginx (producción) — Nginx es el punto de entrada real y es quien envía los headers CORS al browser.

## Instructions

1. En FastAPI para desarrollo (`backend/main.py`):
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   ALLOWED_ORIGINS = os.environ["ALLOWED_ORIGINS"].split(",")
   app.add_middleware(CORSMiddleware,
       allow_origins=ALLOWED_ORIGINS,
       allow_methods=["POST", "GET"],
       allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
       allow_credentials=True,
       max_age=3600,
   )
   ```
2. En Nginx (producción), en el bloque `server`:
   ```nginx
   set $cors_origin "";
   if ($http_origin ~* "^https://(app\.tudominio\.com|admin\.tudominio\.com)$") {
       set $cors_origin $http_origin;
   }
   add_header "Access-Control-Allow-Origin" $cors_origin always;
   add_header "Access-Control-Allow-Credentials" "true" always;
   add_header "Access-Control-Allow-Methods" "POST, GET, OPTIONS" always;
   ```
3. Manejar preflight OPTIONS devolviendo 204 sin pasar al upstream.
4. Definir `ALLOWED_ORIGINS` en Vault/config por entorno: dev, staging, producción tienen listas distintas.
5. Nunca incluir `localhost` en la lista de producción.
6. Verificar en tests de integración que peticiones desde origen no permitido reciben 403.

## Notes

- `allow_credentials=True` requiere que `allow_origins` sea una lista explícita, nunca `["*"]`.
- El preflight request (OPTIONS) no lleva JWT — el middleware CORS debe responder antes del middleware de auth.
