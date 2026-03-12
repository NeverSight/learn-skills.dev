---
name: human_review_queue
description: Cola de casos ambiguos para revisión humana con SLA de respuesta
type: Framework
priority: Recomendada
mode: Self-hosted
---

# human_review_queue

Sistema de cola para casos de verificación ambiguos que requieren revisión por un operador humano. Implementa SLA de respuesta, priorización y distribución de carga entre revisores.

## When to use

Usar en el `decision_agent` cuando el score global cae en la zona ambigua (entre umbrales de rechazo y aprobación automática). También cuando hard rules específicas requieren revisión manual.

## Instructions

1. Crear tabla: `manual_reviews(session_id, status, priority, assigned_to, created_at, resolved_at)`.
2. Encolar caso: insertar en `manual_reviews` con status `pending` y prioridad basada en score.
3. Notificar al equipo de revisión via webhook/Slack.
4. Dashboard de revisión: listar casos pendientes ordenados por prioridad y antigüedad.
5. El revisor accede a: scores parciales, razones de la decisión, imágenes (temporales, max 15 min).
6. Acciones del revisor: `APPROVE`, `REJECT`, `ESCALATE`.
7. SLA: responder en < 30 minutos para prioridad alta, < 2 horas para prioridad normal.

## Notes

- Las imágenes biométricas siguen el TTL de 15 minutos; el revisor debe actuar antes de que expiren.
- Implementar métricas de revisión: tiempo medio de resolución, tasa de acuerdo con el sistema automático.
- Si el SLA se incumple, escalar automáticamente al siguiente nivel.