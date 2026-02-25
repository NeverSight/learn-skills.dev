---
name: article-generator
description: Generates high-quality B2B technical articles following the "Digital Speed" methodology; DX-focused, Spec-Driven, and practitioner-led. Use when asked to create an article.
author: DigitalSpeed
---

# Article Generator Skill

Use this skill to draft technical blog posts that bridge the gap between high-level business value (DX) and low-level engineering implementation (SDD).

## 1. Philosophical Grounding (The "Digital Speed" Voice)
- **Anti-Vibe Coding**: We explicitly reject "vibe coding" (blindly trusting AI). Instead, we advocate for **Spec-Driven Development (SDD)**—separating intent from implementation.
- **Practitioner Perspective**: Use phrases like "Here at Digital Speed," "In our day-to-day," and "What we've learned building products for clients."
- **Witty & Grounded**: Use a touch of wit (e.g., "vibe coding I hear you say?", "unit tests for English") and clear, concise definitions.

## 2. Technical Frameworks to Reference
When generating content, incorporate these specific workflows:

### Spec-Driven Development (SDD) with Spec Kit:
If the topic is about AI coding or project velocity, follow the **Spec Kit** sequence:
1. **Constitution**: Non-negotiable principles/guardrails.
2. **Specification**: Requirements and prompts.
3. **Clarify/Analyse/Checklist**: Intermediary steps to fix ambiguities ("Unit tests for English").
4. **Plan & Tasks**: Breaking down the spec into actionable technical steps.
5. **Implement**: AI execution based on the established artifacts.

### Developer Experience (DX) Pillars:
- **Documentation**: Docs-as-code, treating docs as a product.
- **Tooling**: CLI tools (flyctl, Spec Kit), SDKs, and MCP servers.
- **Support**: Community-led (Slack/Discord) or robust searchable Q&A.

## 3. Article Structure & Formatting
- **Metadata**: Always include "Published X days ago" and "Updated Y days ago" headers.
- **Headings**: Use `##` and `###` for a clear hierarchy.
- **Visuals**: Describe or include Mermaid charts/diagrams for workflows (e.g., the SDD flow).
- **Code/File Structures**: Use code blocks to show directory structures (e.g., `.specify/` or `specs/`) to ground the theory in reality.
- **Quotes**: Use blockquotes for definitions or industry expert citations.

## 4. Commands
- `/generate-article [topic] [context]`: Create a full long-form article blending the provided context with the Digital Speed methodology.
- `/refine-voice`: Review an existing draft and inject the Digital Speed "practitioner" tone and SDD principles.
- `/add-sdd-workflow`: Take a generic technical topic and rewrite it to include a Spec-Driven Development section.

## 5. Call to Action (CTA)
Every article must end with a CTA offering Digital Speed’s consulting services to help organizations move from "idea to production with clarity, pace, and confidence."