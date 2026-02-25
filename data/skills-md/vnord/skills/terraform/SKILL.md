---
name: terraform
description: Terraform and OpenTofu best practices for variables, modules, descriptions, resources, plan, and import
---

# Terraform

## Plan and import

- Don't run `terraform plan` directly; instead give the command and ask the user to execute it.
- NEVER run terraform import manually; use import statements instead.

## Variables

- Do not set `nullable = true` on variables; that is the default and is redundant.
- Only set `nullable = false` when the variable must not be null.
- Pass every value explicitly at the call site. Defaults and fallbacks—variable defaults, provider defaults, resource defaults, coalesce/fallback patterns—hide decisions and make behavior opaque. We hate them; use only as a last resort.

## Module structure

- Single call per concern: one module call per cohesive concern; merge related pieces into one module.

## Variables and outputs

- Remove unused outputs; keep only outputs that are referenced.
- Minimize environment config; don't parametrize values that never vary across environments.

## Descriptions

- Omit `description` unless it adds information not visible from the code; remove if unused.

