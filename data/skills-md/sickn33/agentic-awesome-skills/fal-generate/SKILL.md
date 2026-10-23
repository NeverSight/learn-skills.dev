---
name: fal-generate
description: "Generate images and videos using fal.ai AI models"
risk: critical
source: "https://github.com/fal-ai-community/skills/blob/main/skills/claude.ai/fal-generate/SKILL.md"
date_added: "2026-02-27"
---

# Fal Generate

## Overview

Generate images and videos using fal.ai AI models

## When to Use

Prepare image or video generation through an available fal.ai integration when the user requests that media operation.

## Procedure and Inputs

Resolve prompt, intended use, aspect ratio, duration, reference permissions and budget. This AAS entrypoint does not bundle a fal client, model catalog,
credentials or executable examples. The historical upstream file is currently
unavailable; preserve its attribution and do not invent an endpoint or model ID.
Use only an already configured integration with a verified current schema, or
report execution unavailable and return the requested job specification.

Choose a currently available model from the actual integration, inspect its input schema, and submit the smallest requested job. Preserve returned job identity and distinguish queued, failed and completed status.

Confirm upload/privacy and paid-call scope before submitting. Use bounded status
polling appropriate to the actual tool; do not retry an ambiguous submission until
its job identity/account state is reconciled. Deliver the actual returned artifact
and state which requested properties were checked; a draft or queued job is not a
finished output.

## Example

**User request:**

> Generate images and videos using fal.ai AI models.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
