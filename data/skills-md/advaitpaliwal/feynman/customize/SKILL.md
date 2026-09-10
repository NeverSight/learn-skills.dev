---
name: customize
description: Configure Feynman specialists, skills, connectors, permissions, memory categories, compute providers, and project setup. Use when the task asks to customize the research workbench or create a reusable Feynman research capability.
---

# Customize

Use this skill for Feynman-owned workbench customization.

Workflow:

1. Decide whether the request belongs in a specialist prompt, skill, connector, setting, permission grant, memory category, compute provider, or project/session context.
2. Use the narrowest durable layer. Specialists live in `.feynman/agents/`; reusable skills live in `skills/`; workbench settings live in `.feynman/workbench/settings.json`.
3. Keep user-facing names Feynman-owned and domain-centered. Do not expose local reference-app paths or connector names.
4. Verify the change through the workbench state or Pi command discovery, not only by reading files.
5. Record setup state and verification in the active plan or changelog when the customization changes product behavior.

Prefer a concrete research capability over a generic productivity surface.
