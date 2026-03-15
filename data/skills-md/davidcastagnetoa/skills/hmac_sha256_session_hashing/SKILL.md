---
name: hmac_sha256_session_hashing
description: Hash de integridad por sesión para garantizar no-repudio e inmutabilidad del registro de auditoría
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# hmac_sha256_session_hashing

Cada registro de auditoría incluye un HMAC-SHA256 calculado sobre los campos clave de la sesión. Esto garantiza que los logs no han sido alterados a posteriori (no-repudio) y permite detectar manipulación del historial de decisiones KYC.

## When to use

Usar al persistir cada registro de auditoría en PostgreSQL. El hash se calcula antes del INSERT y se almacena como columna `integrity_hash`.

## Instructions

1. No requiere instalación adicional — usar `hmac` y `hashlib` de la stdlib Python.
2. Definir clave HMAC en Vault: `vault kv put secret/kyc/audit hmac_key=<random-256-bit-hex>`.
3. Cargar clave al arrancar: `HMAC_KEY = os.environ["AUDIT_HMAC_KEY"]`.
4. Calcular hash antes de persistir:
   ```python
   import hmac, hashlib, json
   def compute_integrity_hash(session_data: dict, key: bytes) -> str:
       payload = json.dumps(session_data, sort_keys=True, ensure_ascii=False).encode()
       return hmac.new(key, payload, hashlib.sha256).hexdigest()
   ```
5. Campos a incluir en el payload: `session_id, timestamp, decision, global_score, agent_scores, user_id_hash`.
6. Al leer un registro, verificar con `hmac.compare_digest()` para prevenir timing attacks.
7. Rotar la clave HMAC en Vault sin downtime usando doble validación (aceptar clave anterior durante 24h).

## Notes

- Nunca usar SHA256 directo sin HMAC — sin la clave secreta, cualquiera puede recalcular el hash.
- `hmac.compare_digest()` es obligatorio para la verificación — nunca comparar strings directamente.
- Los registros con hash inválido deben generar alerta crítica en Alertmanager.