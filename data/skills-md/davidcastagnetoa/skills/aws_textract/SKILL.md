---
name: aws_textract
description: Fallback cloud con soporte nativo para documentos de identidad
type: API
priority: Opcional
mode: Cloud
---

# aws_textract

AWS Textract es un servicio de extracción de texto que incluye soporte nativo para documentos de identidad (AnalyzeID). Extrae campos estructurados como nombre, fecha de nacimiento y número de documento directamente.

## When to use

Usar en el `ocr_agent` como alternativa cloud a Google Vision, especialmente cuando se necesita extracción estructurada de campos de documentos de identidad. Solo como fallback.

## Instructions

1. Instalar: `pip install boto3`.
2. Configurar credenciales AWS: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`.
3. Usar AnalyzeID para documentos de identidad:
   ```python
   client = boto3.client('textract')
   response = client.analyze_id(DocumentPages=[{'Bytes': image_bytes}])
   ```
4. Parsear campos: `response['IdentityDocuments'][0]['IdentityDocumentFields']`.
5. Mapear campos Textract a formato interno del sistema.
6. Aplicar `regex_data_normalizer` a los resultados.
7. Registrar uso de fallback cloud en auditoría.

## Notes

- AnalyzeID soporta pasaportes y DNIs de múltiples países de forma nativa.
- Coste: ~$10 por 1000 documentos con AnalyzeID; más caro que Google Vision.
- Misma consideración GDPR que Google Vision: imágenes salen del perímetro self-hosted.