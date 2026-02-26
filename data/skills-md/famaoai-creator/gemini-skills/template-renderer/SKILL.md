---
name: template-renderer
description: Render text from templates (Mustache/EJS) and data.
status: implemented
arguments:
  - name: template
    short: t
    type: string
    required: true
  - name: data
    short: d
    type: string
    required: true
  - name: out
    short: o
    type: string
category: Data & Content
last_updated: '2026-02-13'
tags:
  - data-engineering
  - gemini-skill
---

# Template Renderer

Render text from templates (Mustache/EJS) and data.

## Usage

node template-renderer/scripts/render.cjs [options]

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
