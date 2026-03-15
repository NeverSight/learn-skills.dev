---
name: 4d-validate-form
description: Validate 4D form files (.4DForm) against the official JSON schema. Use this skill when the user wants to validate, check, or verify a 4D form file for errors. Detects invalid properties, missing required fields, and type mismatches.
license: Apache 2.0
---

# 4D Form Validator

Validate `.4DForm` files against the 4D forms JSON schema.

## Usage

```bash
python scripts/validate_form.py <path/to/form.4DForm>
# Or use just the form name (resolves to Project/Sources/Forms/<name>/form.4DForm)
python scripts/validate_form.py <FormName>
```

### Examples

```bash
# Full path
python scripts/validate_form.py Project/Sources/Forms/MyForm/form.4DForm

# Just form name (shorter, fewer tokens)
python scripts/validate_form.py MyForm
```

Requires `jsonschema` package: `pip install jsonschema`

## Resources

- `scripts/validate_form.py` - Validation script
- `assets/formsSchema.json` - Official 4D forms JSON schema
