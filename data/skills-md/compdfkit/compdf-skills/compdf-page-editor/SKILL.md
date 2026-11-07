---
name: compdf-page-editor
description: Merge, split, rotate, insert, delete, and extract PDF pages with ComPDF. Use for PDF page management, document assembly, cleanup, restructuring, and selected-page output.
---

# ComPDF Page Editor

## Overview

ComPDF Page Editor gives AI agents a focused PDF page-management skill for assembling, cleaning, and restructuring documents. It supports merging multiple PDFs, splitting large files, rotating pages, inserting new pages, deleting pages, and extracting selected pages or ranges. The skill fits document-prep workflows before review, filing, delivery, or automation.

Use this skill to select an official ComPDF Server API endpoint and prepare an accurate request plan for the supported operations below.

## Supported Operations

| Operation | Official page or index section |
| --- | --- |
| Merge PDFs | `merge` |
| Split PDF | `split` |
| Rotate pages | `rotate` |
| Insert pages | `insert` |
| Delete pages | `delete` |
| Extract pages | `extract` |

## Scope

Use only page-management endpoints. Validate one-based page ranges and request confirmation for destructive edits unless already authorized.

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
