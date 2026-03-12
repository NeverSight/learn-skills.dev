---
name: eliteforge-frontend-generator
description: Generate EliteForge frontend projects with the same logic as cisdigital-generator-app. Reuse the exact project type to template mapping for frontend_app/frontend_ui/frontend_sdk, naming rules for company/product/service, and onebase-cli command assembly. Use when users ask to scaffold EliteForge frontend app projects, Vue3 component monorepo projects, JS SDK/lib projects, or request a dry-run command preview aligned with this generator. Always require user-provided required parameters and never infer missing required fields.
---

# EliteForge 前端生成器

## Overview

Generate frontend projects with deterministic rules from the online generator app.
Use the bundled script to produce a dry-run payload/command preview or run project creation directly.
Project name is mandatory: `fe-<company_name>-<product_name>-<service_name>`.

## Package Manager Policy

- Treat `pnpm` as the only package manager for generated frontend projects.
- After project generation, always initialize dependencies with `pnpm i` inside the generated project directory.
- Do not replace `pnpm i` with `npm install`, `yarn`, or `pnpm install`.

## Project Naming Policy

- Always pass `project_name` to scaffold CLI as `fe-<company_slug>-<product_slug>-<service_slug>`.
- Never drop the `fe-` prefix.
- Never append project-type suffixes such as `-app`, `-ui`, or `-sdk`.

## Mandatory Input Policy

- Treat `project_type`, `company_name`, `product_name`, and `service_name` as required and user-provided only.
- Never infer required fields from repository name, current directory, previous conversation values, defaults, or examples.
- If any required field is missing, stop and ask only for missing fields first.
- Do not run dry-run or generation before all required fields are explicitly provided by the user.
- If user input is ambiguous (for example "same as before" or "use default"), ask for explicit values.

## Inputs

Collect the following fields.

Required (must come from the user message):

- `project_type`: `frontend_app`, `frontend_ui`, or `frontend_sdk`
- `company_name`: kebab-case
- `product_name`: kebab-case
- `service_name`: kebab-case

Optional:

- `cli_name`: default `onebase-cli`
- `output_dir`: default current working directory
- `auto_slugify`: default `false`; use only when the user explicitly asks to convert non-kebab names

## Workflow

1. Collect required fields only from explicit user input.
2. If required fields are missing, ask only for the missing fields and wait for user response.
3. Validate naming fields as kebab-case.
4. If naming is invalid and `auto_slugify` is not explicitly requested, ask the user to provide kebab-case values.
5. Run dry-run first to show payload and command.
6. Verify dry-run command uses `-p fe-<company_slug>-<product_slug>-<service_slug>`.
7. Execute the create command.
8. Change to generated project directory and run `pnpm i`.
9. Confirm generated folder exists and initialization completed.

Read [references/frontend-generation-logic.md](references/frontend-generation-logic.md) when the user asks why a template or project name is chosen.

## Commands

Dry-run:

```bash
python3 scripts/create_frontend_project.py \
  --project-type frontend_app \
  --company-name cisdigital \
  --product-name your-product \
  --service-name your-service \
  --dry-run
```

Generate `frontend_app`:

```bash
python3 scripts/create_frontend_project.py \
  --project-type frontend_app \
  --company-name cisdigital \
  --product-name your-product \
  --service-name your-service

cd fe-cisdigital-your-product-your-service
pnpm i
```

Generate `frontend_ui`:

```bash
python3 scripts/create_frontend_project.py \
  --project-type frontend_ui \
  --company-name cisdigital \
  --product-name your-product \
  --service-name your-component

cd fe-cisdigital-your-product-your-component
pnpm i
```

Generate `frontend_sdk`:

```bash
python3 scripts/create_frontend_project.py \
  --project-type frontend_sdk \
  --company-name cisdigital \
  --product-name your-product \
  --service-name your-jsdk

cd fe-cisdigital-your-product-your-jsdk
pnpm i
```

Use custom CLI or output directory:

```bash
python3 scripts/create_frontend_project.py \
  --project-type frontend_app \
  --company-name cisdigital \
  --product-name your-product \
  --service-name your-service \
  --cli-name onebase-cli \
  --output-dir /path/to/workspace

cd /path/to/workspace/fe-cisdigital-your-product-your-service
pnpm i
```

Convert non-kebab input (only when user explicitly requests conversion):

```bash
python3 scripts/create_frontend_project.py \
  --project-type frontend_app \
  --company-name "CIS Digital" \
  --product-name "My Product" \
  --service-name "Portal UI" \
  --auto-slugify \
  --dry-run
```

## Notes

- `frontend_project_type` exists in the form data but does not affect template selection in current generator logic.
- The script blocks generation if target project directory already exists.
- Always initialize generated projects with `pnpm i`.
- Generated project directory name is exactly `fe-<company_slug>-<product_slug>-<service_slug>`.
- Keep output concise: return generated directory, create command, and `pnpm i` result.
- Never guess or fill missing required fields on behalf of the user.
