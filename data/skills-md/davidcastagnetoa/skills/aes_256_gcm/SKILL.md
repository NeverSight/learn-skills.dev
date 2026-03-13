---
name: aes_256_gcm
description: Cifrado AES-256-GCM para datos biométricos en reposo con autenticación integrada
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# aes_256_gcm

AES-256-GCM es el algoritmo de cifrado simétrico estándar para proteger datos biométricos en reposo. GCM (Galois/Counter Mode) proporciona tanto confidencialidad como autenticación de la integridad — detecta si los datos cifrados han sido manipulados.

## When to use

Usar para cifrar embeddings faciales y referencias a imágenes antes de almacenar en PostgreSQL o Redis. Las imágenes se cifran en MinIO con Server-Side Encryption (mismo algoritmo, gestionado por MinIO).

## Instructions

1. Instalar: `pip install cryptography`
2. Implementar en `backend/core/encryption.py`:
   ```python
   from cryptography.hazmat.primitives.ciphers.aead import AESGCM
   import os
   class BiometricEncryption:
       def __init__(self, key: bytes):
           assert len(key) == 32, "Key must be 256 bits (32 bytes)"
           self.aesgcm = AESGCM(key)
       def encrypt(self, data: bytes, associated_data: bytes = b"") -> bytes:
           nonce = os.urandom(12)  # 96-bit nonce, único por operación
           ciphertext = self.aesgcm.encrypt(nonce, data, associated_data)
           return nonce + ciphertext  # nonce prepended al ciphertext
       def decrypt(self, encrypted: bytes, associated_data: bytes = b"") -> bytes:
           nonce, ciphertext = encrypted[:12], encrypted[12:]
           return self.aesgcm.decrypt(nonce, ciphertext, associated_data)  # lanza InvalidTag si manipulado
   ```
3. Cargar clave desde Vault: `ENCRYPTION_KEY = bytes.fromhex(vault.read("secret/kyc/biometric_key"))`.
4. `associated_data` debe incluir el `session_id` — vincula el ciphertext a la sesión específica, previene reutilización.
5. Rotar la clave de cifrado anualmente sin downtime: cifrar con nueva clave, almacenar versión de clave en el registro.
6. Nunca almacenar el nonce por separado — prependerlo al ciphertext como en el ejemplo.

## Notes

- `AESGCM.decrypt()` lanza `cryptography.exceptions.InvalidTag` si el ciphertext fue manipulado — capturar y tratar como intento de fraude.
- Los embeddings faciales son datos biométricos especiales bajo GDPR Art. 9 — su cifrado no es opcional.
- Tamaño del embedding cifrado: 512 floats × 4 bytes = 2048 bytes de plaintext → ~2072 bytes cifrado (nonce + ciphertext + tag).