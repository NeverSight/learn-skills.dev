---
name: fal-image-edit
description: "AI-powered image editing with style transfer and object removal"
risk: critical
source: "https://github.com/fal-ai-community/skills/blob/main/skills/claude.ai/fal-image-edit/SKILL.md"
date_added: "2026-02-27"
---

# Fal Image Edit

## Overview

AI-powered image editing with style transfer and object removal

## When to Use

Edit a supplied image through an available fal.ai integration when the user requests that media operation.

## Procedure and Inputs

Resolve actual source image, requested edits, preservation constraints, output format and budget. This AAS entrypoint does not bundle a fal client, model catalog,
credentials or executable examples. The historical upstream file is currently
unavailable; preserve its attribution and do not invent an endpoint or model ID.
Use only an already configured integration with a verified current schema, or
report execution unavailable and return the requested job specification.

Inspect the actual image first, bind it to the edit request, and choose an available model that supports the requested operation. Review the returned image against preservation constraints and keep the original unchanged.

Confirm upload/privacy and paid-call scope before submitting. Use bounded status
polling appropriate to the actual tool; do not retry an ambiguous submission until
its job identity/account state is reconciled. Deliver the actual returned artifact
and state which requested properties were checked; a draft or queued job is not a
finished output.

## Example

**User request:**

> Use @fal-image-edit for this task: AI-powered image editing with style transfer and object removal.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
