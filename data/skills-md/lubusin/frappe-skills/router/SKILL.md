---
name: router
description: Route to the appropriate Frappe skill based on task type. Use as the entry point when working on Frappe projects to determine which specialized skill to apply.
---

# Frappe Router

Route to the appropriate Frappe skill based on your task.

## When to use

- First step when starting any Frappe-related work
- To determine which specialized skill applies to your task

## Procedure

### 0) Identify task type

| Task | Skill |
|------|-------|
| Understand project structure, versions, apps | → `project-triage` |
| Scaffold new app, hooks, architecture, background jobs | → `app-development` |
| Create/modify DocTypes, fields, controllers | → `doctype-development` |
| Build REST/RPC APIs, webhooks, integrations | → `api-development` |
| Customize Desk UI, form scripts, list views, JS API | → `desk-customization` |
| Build Vue 3 frontends with Frappe UI, portals | → `frontend-development` |
| UI/UX patterns from CRM/Helpdesk/HRMS | → `ui-patterns` |
| Create print formats, email templates, Jinja, PDFs | → `printing-templates` |
| Build reports (Builder, Query, Script) | → `reports` |
| Create public web forms for data collection | → `web-forms` |
| Write or run tests | → `testing` |
| Set up dev environment with Docker/FM | → `frappe-manager` |
| Build CRM/Helpdesk/enterprise systems | → `enterprise-patterns` |

### 1) Run triage first (recommended)

Before deep work, run `project-triage` to understand:
- Project type (bench/FM/standalone)
- Frappe version
- Installed apps
- Available tooling

### 2) Combine skills as needed

Complex tasks may require multiple skills:
- New app = `app-development` + `doctype-development` + `api-development` + `testing`
- Feature with UI = `doctype-development` + `desk-customization` + `api-development`
- Custom frontend = `frontend-development` + `api-development`
- Document workflow = `doctype-development` + `printing-templates` + `reports`
- Enterprise app = `enterprise-patterns` + `doctype-development`

## Quick decision tree

```
Is this about understanding the project?
  → project-triage

Is this about creating a new app or app architecture?
  → app-development

Is this about data models or DocTypes?
  → doctype-development

Is this about APIs or external access?
  → api-development

Is this about Desk UI, form scripts, or client-side JS?
  → desk-customization

Is this about a Vue 3 frontend or portal?
  → frontend-development

Is this about UI/UX patterns or app design?
  → ui-patterns

Is this about print formats, PDFs, or Jinja templates?
  → printing-templates

Is this about reports or data analysis views?
  → reports

Is this about public web forms?
  → web-forms

Is this about testing?
  → testing

Is this about local dev environment?
  → frappe-manager

Is this a complex enterprise system?
  → enterprise-patterns
```

## Guardrails

- **Always run triage first** before making code changes to unknown projects
- **Check Frappe version** before recommending features (API availability varies significantly between v13, v14, v15, v16)
- **Don't assume ERPNext** - many projects use Frappe Framework without ERPNext
- **Verify site context** - commands like `bench migrate` affect specific sites

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Skipping project triage | Applying wrong patterns for version | Always run triage first |
| Using ERPNext-specific code in Frappe-only projects | Module not found errors | Check installed apps first |
| Wrong skill for task | Incomplete implementation | Match task type to skill carefully |
| Ignoring version differences | Deprecated/missing APIs | Check version compatibility in skill references |
| Working on wrong site | Changes don't appear | Always specify `--site` flag |
| Using vanilla JS/jQuery for frontends | Ecosystem mismatch | Use Frappe UI (Vue 3) via `frontend-development` |
| Custom app shell for CRUD apps | Inconsistent UX | Follow CRM/Helpdesk patterns via `enterprise-patterns` |
