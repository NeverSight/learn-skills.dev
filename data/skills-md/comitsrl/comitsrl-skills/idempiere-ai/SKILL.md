---
name: "idempiere-ai"
description: "Usar AI (Copilot/LLMs y agentes) en proyectos iDempiere para acelerar desarrollo y habilitar acceso conversacional a datos, con guardrails de seguridad, multi-tenant, observabilidad y control humano. Usar para POCs o disenos productivos de RAG y LLM a SQL."
---

# iDempiere AI (Dev + Datos + Agentes)

## Objetivo

Adoptar AI sin romper calidad/seguridad:
- acelerar desarrollo (boilerplate, tests, consultas),
- habilitar chat/consulta por lenguaje natural sobre datos del ERP,
- disenar agentes con intencion (acciones) con controles y auditoria.

## Workflow recomendado (alto nivel)

1) Definir el caso de uso
   - productividad de desarrollo (Copilot/LLM) vs chatbot/BI conversacional (LLM a SQL).
   - si el objetivo es mas amplio ("conciencia empresarial"): definir Percepcion/Memoria/Intencion/Gobernanza.
2) Definir guardrails
   - validacion de codigo/SQL generado,
   - politicas de datos sensibles (cloud vs local),
   - acceso por roles (solo lectura al inicio).
3) Reducir complejidad del schema
   - exponer **views**/modelo semantico acotado, no todas las tablas.
4) Prompting y confiabilidad
   - prompts "SQL only", whitelists de objetos, limites/orden, few-shot.
   - controlar errores: si falla, responder "no puedo" (no inventar).
5) Observabilidad y gobernanza
   - log de prompts/retrieval/SQL/acciones,
   - metricas (latencia, costo, fallos, abuse),
   - HITL para acciones de riesgo.

## Referencia

Detalles y guardrails: `references/ai-in-idempiere.md`.
Marco de "conciencia empresarial": `references/conciencia-empresarial.md`.
Template Control Tower: `references/control-tower-template.md`.
Template Data Contract minimo: `references/data-contract-minimo.md`.

