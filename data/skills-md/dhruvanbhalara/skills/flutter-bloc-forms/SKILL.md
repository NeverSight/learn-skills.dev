---
name: flutter-bloc-forms
description: Form State Management, Validation & Input Patterns
metadata:
    platforms: "flutter"
    languages: "dart"
    category: "ui"
---

# Form Architecture with BLoC

-   Manage form state in a dedicated `FormBloc` — NOT in widget `setState`
-   Each form field maps to a property in the BLoC state
-   Validate on field change (real-time) or on submit (batch) depending on UX requirements
-   Emit `FormSubmitting`, `FormSuccess`, `FormError` states for submission flow

## Form Events

-   `FieldChanged(field, value)` — update a single field in state
-   `FormSubmitted` — trigger validation and submission
-   `FormReset` — clear all fields and errors

## Form State

-   Use a single state class with all field values, field-level errors, and form status:
    ```dart
    sealed class FormStatus { initial, submitting, success, failure }
    ```
-   Field errors: `Map<String, String?>` keyed by field name — `null` means valid

# Validation Patterns

-   Validate in the domain layer — NOT in widgets or BLoCs
-   Create pure validator functions that return `String?` (null = valid, string = error message):
    ```dart
    String? validateEmail(String value) =>
      value.contains('@') ? null : 'Invalid email';
    ```
-   Compose validators: `String? validate(String v) => validateRequired(v) ?? validateEmail(v)`
-   Use localized error messages via `context.l10n` — no hardcoded validation strings

# Input Widgets

-   Use `TextFormField` with `InputDecoration` for consistent styling
-   Always set `textInputAction` for proper keyboard behavior (`next`, `done`)
-   Always set `keyboardType` matching the field type (`emailAddress`, `phone`, `number`)
-   Use `inputFormatters` to restrict input (e.g., `FilteringTextInputFormatter.digitsOnly`)
-   Assign `Key('feature_fieldName')` to every form field for test access
-   Use `AutofillHints` for login/signup forms (email, password, name)
-   Wrap form fields with `Focus` or `FocusTraversalGroup` for proper tab order

# Controller Lifecycle

-   Declare `TextEditingController` as `late final` in `initState()` — dispose in `dispose()`
-   Sync controllers to BLoC via `onChanged` callback or controller listener

# Form Submission

-   Disable submit button while `FormStatus.submitting` to prevent double-submission
-   Show inline field errors below each field — not just a top-level error
-   On success: navigate, show success feedback, and reset form if staying on same page
-   On failure: show error feedback via `SnackBar` or inline, keep form data intact

# Common Form Patterns

-   **Search**: Use `debounce` transformer on search events (300-500ms delay)
-   **Multi-step**: Each step is a separate form state within one `FormBloc`, validated independently
-   **Dependent fields**: Update dependent field options in `on<FieldChanged>` handler (e.g., country → city)
