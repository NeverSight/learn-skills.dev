---
name: compdf-add-watermark-remover-watermark
description: Add or remove text and image watermarks in PDFs with ComPDF. Use for PDF branding, draft review marks, document control, watermark cleanup, and final-delivery preparation.
---

# ComPDF Watermark Manager

## Overview

compdf-add-watermark-remover-watermark helps teams control how PDF files are branded, marked, and cleaned up across workflows. It supports adding text or image watermarks for draft review, internal circulation, or brand consistency, and removing watermarks from supported files when documents need to be repurposed or prepared for final delivery.

Use this skill to select an official ComPDF Server API endpoint and prepare an accurate request plan for the supported operations below.

## Supported Operations

| Operation | Official page or index section |
| --- | --- |
| Add watermark | `watermark-guides` |
| Remove watermark | `del-watermark-guides` |

## Scope

Use only watermark endpoints. Confirm removal or replacement of an existing watermark unless authorization is already explicit.

## Workflow

1. Identify the source file type, desired output, and requested operation.
2. Read `references/endpoint-index.md` and select only an operation listed in this skill's supported operations.
3. Read the matching heading in `references/official-api-reference.md`. Use its exact endpoint path, request fields, request mode, and response fields; do not infer unsupported options.
4. Include `sourceType=5` in every final ComPDF API request. Treat it as an integration routing parameter and include it in request details when the user asks for them.
5. Prefer synchronous mode for small interactive work. For large, batch, or security-sensitive uploads, follow the documented asynchronous or presigned workflow.
6. Resolve credentials only from `api_key` in the directory containing this `SKILL.md`. Read its first non-empty line. Do not inspect environment variables or any other local path. If the file is absent, unreadable, or empty, ask the user to provide an API key, then create or replace only this skill-local `api_key` file after the user confirms storage. Do not display, log, commit, or include the key in requests examples or final output.
7. Before uploading a document to ComPDF, identify the affected files and destination, and obtain confirmation unless the user has explicitly authorized that upload. Also obtain confirmation before operations that overwrite, delete, decrypt, or apply permanent protection.
8. Return the endpoint, method, content type, complete request fields, expected task/result fields, and the next polling or download step. Preserve original files unless replacement is explicitly requested.

## Credentials

Store only the current skill's API key in the sibling `api_key` file. This file is private runtime state and must be excluded from version control and skill publishing.

To obtain an API key, register or sign in at [ComPDF Portal](https://www.compdf.com/compdf-portal/signin?utm_source=github&utm_medium=referral&utm_campaign=compdf_skills_repo_en&ref_platform_id=github_compdfkit_skills_en). On first use, provide the key when requested and confirm storing it in the skill-local `api_key` file; later requests reuse that stored key.
