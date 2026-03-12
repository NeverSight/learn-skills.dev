---
name: camerax_avfoundation
description: Acceso nativo a cámara en apps móviles con CameraX (Android) y AVFoundation (iOS)
type: Framework
priority: Esencial
mode: Self-hosted
---

# camerax_avfoundation

CameraX (Android) y AVFoundation (iOS) proporcionan acceso directo al hardware de cámara del dispositivo, permitiendo capturar video en vivo y bloquear el acceso a la galería de fotos durante la verificación KYC.

## When to use

Usar en el `capture_agent` para la captura de selfie y documento en apps móviles nativas (React Native / Flutter). Complementa a WebRTC que se usa en la versión web.

## Instructions

1. **React Native**: usar `react-native-camera` o `expo-camera` que abstrae CameraX/AVFoundation.
2. Configurar permisos: `CAMERA` en AndroidManifest.xml y `NSCameraUsageDescription` en Info.plist.
3. Bloquear el acceso a galería: no usar `ImagePicker`, solo captura en vivo.
4. Configurar resolución mínima: 720p para selfie, 1080p para documento.
5. Capturar secuencia de frames (3-5 segundos) para liveness, no solo un snapshot.
6. Validar que el dispositivo tiene cámara frontal disponible antes de iniciar.
7. Implementar overlay guiado para alinear el documento dentro del frame.

## Notes

- CameraX simplifica el manejo de lifecycle en Android (auto-bind al lifecycle del fragment).
- En Flutter, usar `camera` plugin oficial que soporta ambas plataformas.
- Detectar cámaras virtuales verificando el nombre del dispositivo de cámara contra una lista negra.