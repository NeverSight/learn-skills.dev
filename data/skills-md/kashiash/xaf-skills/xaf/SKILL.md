---
name: xaf
description: "DevExpress XAF (eXpressApp Framework) master index. Use this skill first when working with any XAF topic to find the right sub-skill. Covers Blazor and WinForms, EF Core and XPO, versions v24.2 and v25.1. Sub-skills: xaf-xpo-models, xaf-ef-models, xaf-controllers, xaf-editors, xaf-custom-editors, xaf-nonpersistent, xaf-security, xaf-multi-tenant, xaf-web-api, xaf-validation, xaf-reports, xaf-dashboards, xaf-office, xaf-blazor-ui, xaf-winforms-ui, xaf-conditional-appearance, xaf-deployment, xaf-memory-leaks."
---

# XAF (eXpressApp Framework) — Skill Index

DevExpress XAF is a cross-platform .NET application framework for building business applications (Blazor Server and WinForms). It provides MVVM architecture, ORM integration (EF Core and XPO), security, validation, and rich module ecosystem.

**Versions covered:** v24.2 and v25.1
**Platforms:** Blazor Server, WinForms, Web API (OData)
**Official docs:** https://docs.devexpress.com/eXpressAppFramework/112670/expressapp-framework
**DevExpress MCP:** https://api.devexpress.com/mcp/docs

---

## Sub-Skills — When to Use Each

### Data Modeling

| Skill | Load When |
|---|---|
| `xaf-xpo-models` | Defining XPO persistent objects (XPObject, BaseObject, associations, PersistentAlias) |
| `xaf-ef-models` | Defining EF Core entities (BaseObject EF, virtual properties, DbContext, migrations) |
| `xaf-nonpersistent` | Creating NonPersistent objects for custom data sources, API wrappers, input dialogs |

### UI Construction

| Skill | Load When |
|---|---|
| `xaf-controllers` | Creating controllers, SimpleAction/PopupWindowShowAction/SingleChoiceAction/ParametrizedAction |
| `xaf-editors` | Working with built-in property editors, list editors, GridListEditor customization |
| `xaf-custom-editors` | Building custom property editors (Blazor/WinForms) or custom list editors |
| `xaf-conditional-appearance` | Conditionally hiding/disabling/coloring UI elements via [Appearance] attribute |

### Platform-Specific

| Skill | Load When |
|---|---|
| `xaf-blazor-ui` | Blazor-specific UI, thread safety (InvokeAsync), Razor components in XAF, JS interop |
| `xaf-winforms-ui` | WinForms-specific UI, XtraGrid access, background workers, layout, splash |

### Security & Multi-Tenancy

| Skill | Load When |
|---|---|
| `xaf-security` | Roles, permissions, authentication (Standard/AD/OAuth2), programmatic permission checks |
| `xaf-multi-tenant` | Multi-tenant SaaS apps with separate DB per tenant (v24.2+) |

### Services & API

| Skill | Load When |
|---|---|
| `xaf-web-api` | Building/consuming XAF OData Web API (JWT, custom endpoints, $filter/$expand) |
| `xaf-validation` | Validation rules (RuleRequiredField, RuleCriteria, custom rules, programmatic validation) |

### Modules & Features

| Skill | Load When |
|---|---|
| `xaf-reports` | XtraReports integration (setup, predefined reports, export, designer, parameters) |
| `xaf-dashboards` | Dashboard analytics (setup, data sources, designer, permissions) |
| `xaf-office` | File attachments, Spreadsheet editor, RichText editor, PDF viewer |

### Deployment

| Skill | Load When |
|---|---|
| `xaf-deployment` | IIS/Azure/Docker for Blazor, ClickOnce/MSI for WinForms, migrations, license, logging |

### Diagnostics & Quality

| Skill | Load When |
|---|---|
| `xaf-memory-leaks` | Diagnosing memory leaks, auditing event handler cleanup, reviewing ObjectSpace/CollectionSource lifetime |

---

## Quick Architecture Reference

```
MySolution/
├── MySolution.Module/          ← platform-agnostic (business objects, controllers, modules)
│   ├── BusinessObjects/
│   ├── Controllers/
│   └── MySolutionModule.cs
├── MySolution.Blazor.Server/   ← Blazor-specific (Program.cs, BlazorApplication.cs)
│   └── DatabaseUpdate/Updater.cs
├── MySolution.Win/             ← WinForms-specific (Program.cs, WinApplication.cs)
└── MySolution.WebApi/          ← Web API service (Program.cs, OData endpoints)
```

---

## Key Concepts

- **ObjectSpace** (`IObjectSpace`) — unit of work; wraps EF Core DbContext or XPO Session. Not thread-safe. Never store in singleton services.
- **XafApplication** — application lifecycle, module registration, ObjectSpace creation.
- **ModuleBase** — platform-agnostic module; registers business objects, controllers, navigation items.
- **Application Model** — XML/in-memory model describing Views, Actions, Navigation — customizable without recompilation.
- **DatabaseUpdater** — runs on startup to apply schema changes and seed data (`Updater.cs`).

---

## Common Pitfalls (Quick Reference)

| Pitfall | Fix |
|---|---|
| `ObjectSpace` in singleton service | Use `IObjectSpaceFactory` + `using var os = factory.CreateObjectSpace(...)` |
| `async/await` + `ConfigureAwait(false)` in Blazor | Remove `ConfigureAwait(false)` — Blazor needs sync context |
| Non-virtual EF Core properties | All EF Core entity properties must be `virtual` |
| XPO property without `SetPropertyValue` | Use backing field + `SetPropertyValue` for change tracking |
| `AddDbContext` instead of `AddDbContextFactory` | XAF requires `IDbContextFactory<T>` |
| NonPersistent provider registered first | Register `.AddNonPersistent()` **after** persistent providers |

---

## Useful Links

- XAF Getting Started (Blazor): https://docs.devexpress.com/eXpressAppFramework/402189/getting-started/in-depth-tutorial-blazor
- XAF Getting Started (WinForms): https://docs.devexpress.com/eXpressAppFramework/402684/getting-started/in-depth-tutorial-winforms-webforms
- XAF API Reference: https://docs.devexpress.com/eXpressAppFramework/DevExpress.ExpressApp
- DevExpress Examples (GitHub): https://github.com/DevExpress-Examples
- DevExpress Support: https://supportcenter.devexpress.com
- XAF Community (Blogs): https://community.devexpress.com/tags/XAF
