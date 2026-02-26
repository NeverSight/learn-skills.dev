---
name: validation
description: Use when validating data with Standard Schema-compatible schemas or handling ValidationError results.
---

# validation

## Overview

Standard Schema helpers for consistent validation and error handling across Zod, Valibot, ArkType, and others.

## When to Use

- Validating inputs or API payloads with Standard Schema-compatible schemas
- Normalizing sync and async validation paths
- Handling a single `ValidationError` type across schema libraries

## When Not to Use

- You only need simple, ad-hoc checks without schema validation

## Quick Reference

- Guard: `isStandardSchema`
- Validate: `standardValidate`
- Sync only: `createSyncStandardValidator`
- Error: `ValidationError`

## Inputs to Request

- Schema library in use (Zod, Valibot, ArkType)
- Throwing vs non-throwing validation
- Desired error shape and handling

## Resources

- https://www.zapstudio.dev/packages/validation
- https://www.zapstudio.dev/llms.txt
