---
name: exif_metadata_analyzer
description: Analizar metadatos EXIF para detectar edición previa con Photoshop, GIMP u otros editores
type: Library
priority: Recomendada
mode: Self-hosted
---

# exif_metadata_analyzer

Los metadatos EXIF contienen la firma del software que creó/modificó la imagen. Detectar Photoshop o GIMP en los metadatos del documento es señal de alerta de manipulación.

## When to use

Aplicar sobre la imagen del documento antes del procesamiento.

## Instructions

1. Instalar: `pip install piexif`.
2. Extraer y analizar metadatos:
   ```python
   import piexif
   def analyze_exif(image_bytes):
       try:
           exif_data = piexif.load(image_bytes)
       except Exception:
           return {"has_exif": False, "editing_software_detected": False}
       sw_tag = exif_data.get("0th", {}).get(piexif.ImageIFD.Software, b"")
       software = sw_tag.decode("utf-8", errors="ignore").lower() if isinstance(sw_tag, bytes) else ""
       EDITING_SOFTWARE = ["photoshop", "gimp", "lightroom", "paint.net", "affinity", "canva"]
       editing_detected = any(sw in software for sw in EDITING_SOFTWARE)
       make = exif_data.get("0th", {}).get(piexif.ImageIFD.Make, b"").decode("utf-8", errors="ignore")
       return {"has_exif": True, "software": software, "camera_make": make, "editing_software_detected": editing_detected}
   ```
3. Si `editing_software_detected = True`: añadir flag `EXIF_EDITING_SOFTWARE` al antifraud_agent.
4. Si hay EXIF de cámara real (Make/Model conocidos): señal positiva de imagen auténtica.

## Notes

- Las imágenes capturadas con WebRTC/CameraX generalmente tienen EXIF mínimo — no es señal de fraude.
- La ausencia de EXIF tampoco es señal de fraude por sí sola.