---
name: bitrix24-portal
description: 'Bitrix24 on-premise portal from /local — pages in bitrix24 template, SidePanel slider, UI Toolbar, left menu, employee/extranet checks, humanresources departments, Disk upload/attach, workgroups. Use when customizing an intranet portal.'
---

# Bitrix24 portal (on-premise)

Scope: Bitrix24 on-premise · Verified: intranet 26.1350.0, humanresources 26.500.0, socialnetwork 26.150.0, extranet 26.300.0, disk 26.1175.0, ui 26.687.0, main 26.800.0

| Task | Read |
| --- | --- |
| Custom page, slider, toolbar, file placement, URLs | `rules/pages.md` |
| Left menu items | `rules/left-menu.md` |
| Employee / extranet / admin checks, departments, heads | `rules/users-structure.md` |
| User/group storage, upload, attach files to an entity | `rules/disk.md` |
| Groups, projects, collabs: membership, access | `rules/workgroups.md` |

Related: `bitrix-ui` (popups, grid, filter, entity selector), `bitrix24-crm`, `bitrix24-tasks`, `bitrix24-im`, `bitrix24-rest-api`.

## Invariants

- intranet, humanresources, socialnetwork, extranet, disk ship only with Bitrix24 editions: `Loader::includeModule()` each one and keep portal code out of modules shared with plain sites.
- The portal template is `bitrix24`. A slider request (`IFRAME=Y`) and an AJAX request get no template output: slider pages go through `bitrix:ui.sidepanel.wrapper`, AJAX goes to controllers.
- Extranet users are redirected from intranet-site pages to the extranet site (`CExtranet::ExtranetRedirect()`; `/pub/`, `/rest/`, Disk link prefixes are exempt). Pages for external users live on the extranet site.
- Portal composite (option `intranet`/`composite_enabled`) caches the template frame per user; `#page-area` is a dynamic area, so page bodies always render. Keep per-user output inside the page.
- Departments and heads come from the humanresources public API; `UF_DEPARTMENT` is a lagging compat copy.
- HR department assignment, socialnetwork member service and `Folder::uploadFile()` check no rights: check them before the call.
