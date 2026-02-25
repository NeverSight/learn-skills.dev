---
name: django-forms
description: Django form handling patterns including ModelForm, validation, clean methods, and HTMX form submission. Use when building forms, implementing validation, or handling form submission.
---

# Django Forms

## Philosophy

- Prefer ModelForm for model-backed forms
- Keep validation logic in forms, not views
- Always handle and display form errors
- Use `commit=False` when you need to modify the instance before saving

## Validation

**Field-level** (`clean_<field>`):
- Validate and transform a single field
- Return the cleaned value or raise `ValidationError`
- Use for: format checks, uniqueness, normalization

**Cross-field** (`clean`):
- Call `super().clean()` first
- Access multiple fields via `cleaned_data`
- Use `self.add_error(field, message)` for field-specific errors
- Use for: password confirmation, conditional requirements

## View Integration

- Check `request.method` explicitly
- Instantiate form with `request.POST` for POST, empty for GET
- Use `form.save(commit=False)` to set additional fields (e.g., author)
- Return redirect on success, re-render with form on error

**HTMX handling:**
- Check `request.headers.get("HX-Request")` for HTMX requests
- Return partial template on success/error for HTMX
- Use `HX-Trigger` header to notify other components

## Templates

- Display `form.non_field_errors` for cross-field errors
- Display `field.errors` for each field
- Use partial templates (`_form.html`) for HTMX responses
- Include loading indicator with `hx-indicator`

## Widgets

- Override in `Meta.widgets` dict
- Set HTML attributes via `attrs` parameter
- Common: `Textarea(attrs={"rows": 5})`, `DateTimeInput(attrs={"type": "datetime-local"})`

## Formsets

- Use `inlineformset_factory` for related model collections
- Validate both form and formset: `form.is_valid() and formset.is_valid()`
- Pass `instance` for editing existing parent objects

## Pitfalls

- Validating in views instead of forms
- Silently redirecting without checking `is_valid()`
- Forgetting `commit=False` when setting related fields
- Not displaying form errors to users
