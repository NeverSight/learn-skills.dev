---
name: document-generator
description: Unified gateway for all document generation tasks. Automatically routes to specialized artisan skills based on the requested format (PDF, DOCX, XLSX, PPTX, HTML).
status: implemented
arguments:
  - name: format
    short: f
    type: string
    required: true
category: Utilities
last_updated: '2026-02-13'
tags:
  - documentation
  - gemini-skill
---

# Document Generator (Gateway)

This skill provides a single interface for generating various document types. It coordinates specialized skills like `pdf-composer`, `word-artisan`, etc.

## Usage

- "Generate a PDF report from this markdown file."
- "Convert this JSON data into an Excel spreadsheet."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`.
