---
name: google_vision_ocr
description: Fallback cloud OCR para casos donde el OCR self-hosted falla
type: API
priority: Opcional
mode: Cloud
---

# google_vision_ocr

Google Cloud Vision OCR es un servicio cloud de alta precisión para extracción de texto. Se usa exclusivamente como fallback cuando los motores self-hosted (PaddleOCR, EasyOCR) fallan o devuelven confianza muy baja.

## When to use

Usar en el `ocr_agent` solo cuando todos los motores self-hosted devuelven confianza < 0.5 en los campos críticos. Nunca como motor primario para mantener la independencia de servicios externos.

## Instructions

1. Instalar: `pip install google-cloud-vision`.
2. Configurar service account: exportar `GOOGLE_APPLICATION_CREDENTIALS`.
3. Enviar imagen cifrada al API: `client.text_detection(image=vision_image)`.
4. Parsear respuesta: `response.text_annotations[0].description` para texto completo.
5. Mapear coordenadas de bounding boxes a los campos del documento.
6. Aplicar `regex_data_normalizer` a los resultados igual que con OCR self-hosted.
7. Registrar en auditoría que se usó fallback cloud (para métricas de dependencia).

## Notes

- Coste: ~$1.50 por 1000 imágenes; monitorizar uso para control de costes.
- Las imágenes se envían a servidores de Google; verificar compliance GDPR antes de activar.
- Implementar circuit breaker: si Google Vision falla 3 veces seguidas, desactivar temporalmente.