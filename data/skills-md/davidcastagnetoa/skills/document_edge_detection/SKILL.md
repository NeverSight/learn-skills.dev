---
name: document_edge_detection
description: Detectar bordes del documento para validar captura correcta y aplicar corrección de perspectiva
type: Algorithm
priority: Esencial
mode: Self-hosted
---

# document_edge_detection

Detecta el contorno del documento de identidad para validar que está correctamente encuadrado y extraer sus coordenadas para corrección de perspectiva posterior.

## When to use

Usar en la captura del documento, antes de pasarlo al document_processor_agent.

## Instructions

1. Escala de grises + blur gaussiano: `blur = cv2.GaussianBlur(gray, (5,5), 0)`
2. Canny: `edges = cv2.Canny(blur, 75, 200)`
3. Contornos: `contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)`
4. Ordenar por área descendente y tomar los 5 primeros.
5. Aproximar polígono: `approx = cv2.approxPolyDP(c, 0.02*peri, True)`
6. Buscar contorno de 4 vértices (cuadrilátero) de mayor área → es el documento.
7. Devolver los 4 puntos esquina ordenados.

## Notes

- Overlay en tiempo real mostrando el contorno detectado guía al usuario.
- Complementar con YOLOv8 para clasificación del tipo de documento.
