---
name: document_expiry_validator
description: Verificar fecha de expiración del documento de identidad y países/tipos soportados
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# document_expiry_validator

Valida que el documento no está caducado, que ha sido emitido recientemente (no demasiado antiguo), y que pertenece a un país o tipo de documento soportado por el sistema.

## When to use

Usar después de la extracción OCR, como validación de negocio antes del face match.

## Instructions

1. Extraer `expiry_date` del resultado OCR/MRZ (formato YYMMDD en MRZ).
2. Convertir a objeto `datetime.date`.
3. Verificar no expirado: `if expiry_date < date.today(): reject('DOCUMENT_EXPIRED')`.
4. Verificar no futuro inválido: fecha de expiración no puede ser más de 15 años desde hoy.
5. Verificar antigüedad máxima razonable de la foto (si el documento fue emitido hace >10 años, foto puede ser muy diferente → flag para revisión manual, no rechazo automático).
6. Verificar país aceptado: comparar `country_code` MRZ contra lista de países soportados.
7. Verificar tipo de documento soportado: TD1/TD2/TD3/PASSPORT según configuración.

## Notes

- Mantener la lista de países soportados en configuración actualizable sin redeploy.
- Documentos de menos de 1 mes de antigüedad merecen mayor escrutinio (pueden ser recién creados).