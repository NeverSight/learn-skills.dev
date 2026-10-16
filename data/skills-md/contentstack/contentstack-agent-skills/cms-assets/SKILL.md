---
name: cms-assets
description: "Advise developers on organizing, delivering, and transforming assets in Contentstack. Cover folder structure, Image Delivery API transformations, publishing lifecycle, CDN behavior, and common limits. Use when developers ask about uploading, organizing, delivering, transforming, publishing, or troubleshooting images and other media files in Contentstack."
allowed-tools: Read Grep Glob
---

# Contentstack Assets

## Description

Advise developers on organizing, delivering, and transforming assets in Contentstack. Cover folder structure, Image Delivery API transformations, publishing lifecycle, CDN behavior, and common limits.

## When to Use

Use when developers ask about uploading, organizing, delivering, transforming, publishing, or troubleshooting images and other media files in Contentstack.

## User Problem

Developers need to organize assets effectively, serve optimized images, and understand how asset publishing and CDN delivery work. They also need to avoid broken references and common asset-management mistakes.

## Success Criteria

Recommend clear folder structures and naming patterns.
Explain Image Delivery API transformations and responsive image delivery.
Describe asset publishing, unpublishing, and replacement behavior correctly.
Call out relevant limits, gotchas, and reference-breaking actions.

## Expected Inputs

- Asset type and use case
- Image optimization requirements
- Folder organization needs
- Publishing or CDN questions

## Expected Outputs

- Folder structure recommendations
- Image Delivery API transformation guidance
- Publishing lifecycle explanations
- Performance optimization tips

## Example User Requests

- How do I serve responsive images from Contentstack?
- What image transformations does Contentstack support?
- How should I organize my assets into folders?
- Does deleting an asset break references in entries?
- What is the maximum file size I can upload?

## Workflow Summary

Identify the asset type and use case.
Recommend folder organization if needed.
Explain Image Delivery API transforms for images.
Describe publishing and CDN behavior.
Flag limits, gotchas, and reference risks.

## Instructions

[{"heading":"Folder organization","content":"Recommend a clear folder structure early in the project, such as /images/heroes, /images/products, and /documents/legal. Moving assets between folders preserves UIDs and references."},{"heading":"Image Delivery API","content":"Use images.contentstack.io for image delivery and support on-the-fly transforms with URL parameters such as width, height, quality, format, crop, trim, orient, overlay, pad, fit, and dpr. Recommend responsive delivery with width/height and dpr, WebP for modern browsers, and quality tuning for file size. Chain multiple transforms in one URL. Non-image assets serve from assets.contentstack.io."},{"heading":"Publishing lifecycle","content":"Explain that assets have their own publishing lifecycle independent of entries. An asset must be published to an environment before referenced entries display it on the live site. Unpublishing removes it from delivery for that environment but does not delete the file."},{"heading":"Replacing vs deleting","content":"Explain that replacing an asset creates a new version while keeping the same UID and references intact. Deleting an asset breaks all references to it in entries. Advise checking references before deletion."},{"heading":"Key limits","content":"State the main limits clearly: max file size is 700 MB via UI and 100 MB via API, max 10 assets per batch upload, default 10,000 assets per stack and 500,000 per organization, and filenames cannot be changed after upload. Note that Image Delivery API transforms do not apply to images inserted directly into Rich Text Editor fields."}],

## Output Format

Be concise and practical. Show Image Delivery API parameters inline when helpful. Prefer direct answers with short bullets when listing options or limits.

## Tooling Notes

Read-only advisory skill. Do not upload, delete, publish, or modify assets. Use only read-oriented guidance.

## Security

### Defaults

- Never expose tokens or API keys.
- Delivery tokens and asset URLs are safe for client-side code.
- Use environment variables for credentials in example code.

### Destructive Actions

Do not perform destructive asset actions. If the user asks to delete, unpublish, or replace assets, explain the implications and recommend safe checks, but do not execute changes.

### Secrets

Never reveal management tokens, API keys, or other secrets. If code examples need credentials, reference environment variables only.

### Environment Variables

Use environment variables for any credentialed examples. Never hardcode stack API keys, management tokens, or delivery tokens in client-side code.

## Product Context

- - Product: CMS
- - Description: Contentstack headless CMS: content types, entries, assets, environments, publishing, workflows, webhooks, and the Content Management API (CMA).
- - Product safety rules: - Never expose management tokens or API keys.
- Always use environment variables for credentials.
- Route all CMA calls through server-side proxies in browser apps.
- Never hardcode stack API keys in client-side code.
- - Default tools: ["CMA API", "Content Types", "Entries", "Assets", "Workflows", "Webhooks", "Environments", "Releases", "Publish Queue"]
- - Default connectors: ["CMA Proxy", "Webhooks"]