---
name: bitrix-documentgenerator
description: 'Document generator (DOCX/PDF from templates) — Template, Document::createByTemplate, custom DataProvider, placeholders, numerators, storage, transformer PDF, rights, documentgenerator.* REST. Use when generating documents from own data.'
---

# Bitrix document generator

Baseline: main 23.0+ · Verified: documentgenerator 26.200.100, main 26.800.0

Bitrix24 editions only (cloud and on-premise): install requires `humanresources`; absent from "Site Management". PDF/JPG need module `transformer` and a document server.

| Task | Read |
| --- | --- |
| Placeholders, modifiers, tables, images, create template from code | `rules/templates.md` |
| Own entity data: provider class, fields, lists, registration | `rules/providers.md` |
| Generate DOCX/PDF, numbers, storage, delete, events | `rules/generation.md` |
| Module rights, roles, template access, REST, UI components | `rules/access-rest.md` |

CRM documents (invoices, deals) use CRM's own providers: `bitrix24-crm`.

## Invariants

- `Loader::requireModule('documentgenerator')`; code lives in your module under `/local/modules/`, the provider is registered by that module id.
- Template `MODULE_ID` = provider `MODULE` = an installed module; otherwise the provider is silently ignored.
- Call `Template::setSourceType()` before `getFields()` / `Document::createByTemplate()` and check `getSourceType()`.
- Check rights explicitly: `UserPermissions`, template access, `Document::hasAccess()`. Loading and creating check nothing; user `0` passes data checks.
- Reference files by `b_documentgenerator_file.ID` (`FILE_ID`, `PDF_ID`); convert with `FileTable::getBFileId()`.
- PDF is asynchronous: generate with `getFile(false)` or skip conversion errors, react to `onDocumentTransformationComplete`.
