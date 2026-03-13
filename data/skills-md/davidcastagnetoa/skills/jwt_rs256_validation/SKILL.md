---
name: jwt_rs256_validation
description: Validación de tokens JWT firmados con RS256 (clave pública) para autenticación de clientes
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# jwt_rs256_validation

Los clientes del API KYC se autentican presentando un JWT firmado con RS256. El gateway valida la firma usando la clave pública del emisor (almacenada en Vault), el tiempo de expiración y los claims requeridos. RS256 es asimétrico — el gateway solo necesita la clave pública, nunca la privada.

## When to use

Usar en el middleware de FastAPI que protege todos los endpoints `/v1/`. Rechazar con 401 cualquier request sin token válido antes de iniciar el pipeline KYC.

## Instructions

1. Instalar: `pip install python-jose[cryptography] cryptography`
2. Cargar clave pública desde Vault al arrancar: `PUBLIC_KEY = vault.read("secret/kyc/jwt_public_key")`.
3. Middleware de validación en `backend/api/middleware/auth.py`:
   ```python
   from jose import jwt, JWTError
   async def verify_jwt(token: str) -> dict:
       try:
           payload = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"],
                                options={"verify_exp": True, "verify_aud": True},
                                audience="kyc-api")
           return payload
       except JWTError as e:
           raise HTTPException(status_code=401, detail="Token inválido")
   ```
4. Extraer `sub` (client_id) del payload y añadir a los contextvars de logging.
5. Claims obligatorios en el token: `sub`, `exp`, `iat`, `aud="kyc-api"`, `scope`.
6. Cachear validaciones exitosas en Redis con TTL = `exp - now - 60s` para no verificar firma en cada request.
7. Endpoint de JWKS público en `GET /.well-known/jwks.json` para facilitar rotación de claves.

## Notes

- Nunca usar HS256 (simétrico) en producción — si la clave se filtra, cualquiera puede firmar tokens.
- El tiempo de expiración del token debe ser corto: 15-60 minutos. Los clientes renuevan via refresh token.
- En caso de compromiso de la clave privada, revocar publicando nueva clave en Vault + invalidar caché Redis.