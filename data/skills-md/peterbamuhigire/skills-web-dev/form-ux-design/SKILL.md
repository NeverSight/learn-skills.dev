---
name: form-ux-design
description: Cross-platform form UX/UI patterns for web (Bootstrap 5/Tabler) and Android (Jetpack Compose). Covers field anatomy, validation, error states, multi-step wizards, accessibility, touch-friendly inputs, and submission workflows. Use when building any form — registration, data entry, settings, checkout, search, filters, or clinical forms. Companion to webapp-gui-design, healthcare-ui-design, pos-sales-ui-design, and jetpack-compose-ui skills.
---

## Required Plugins

**Superpowers plugin:** MUST be active for all work using this skill. Use throughout the entire build pipeline — design decisions, code generation, debugging, quality checks, and any task where it offers enhanced capabilities. If superpowers provides a better way to accomplish something, prefer it over the default approach.

**Frontend Design plugin:** Required for all UI generation from this skill. Use for form layout decisions, component styling, spacing, color selection for states, responsive form behavior, and visual QA of form elements.

# Form UX/UI Design

Cross-cutting form design patterns for **web** (Bootstrap 5 / Tabler + PHP) and **Android** (Jetpack Compose + Material 3). Apply this skill whenever you build, review, or refactor any form.

## Quick Reference

| Topic | Reference File | Scope |
|-------|---------------|-------|
| Web form components | `references/web-form-components.md` | Bootstrap/Tabler inputs, selects, checkboxes, radios, switches, textareas, file uploads |
| Android form components | `references/android-form-components.md` | Compose TextField, ExposedDropdownMenu, Checkbox, RadioButton, Switch, Slider |
| Validation patterns | `references/form-validation.md` | Validation logic, error states, async validation, submission workflows (both platforms) |
| Accessibility | `references/form-accessibility.md` | WCAG form requirements, ARIA, screen readers, keyboard nav, touch targets (both platforms) |

---

## 1. Form Design Philosophy

Five rules that govern every form decision:

### Rule 1 -- Labels Above Inputs

Stacked labels always. Never placeholder-only. Labels remain visible on focus and when filled. Placeholder text is supplementary hint text, not a replacement for the label.

### Rule 2 -- Single Column by Default

One column for forms. Two-column layout only for naturally paired fields (first name / last name, city / state). Mobile is always single column regardless.

### Rule 3 -- Progressive Disclosure

Show only what is needed now. Reveal advanced fields conditionally (toggles, dependency rules). Break long forms (more than 7 fields) into logical steps.

### Rule 4 -- Instant Feedback

Validate on blur (not on keystroke). Show errors inline below the field. Display success indicators (green border or checkmark) for completed fields that passed validation.

### Rule 5 -- Minimal Friction

Use smart defaults, autocomplete attributes, and auto-formatting (phone, currency). Reduce keystrokes. Never ask for information you already have or can derive.

---

## 2. Field Anatomy

Universal structure across both platforms:

```
+---------------------------------+
| Label *                         |  <- Always visible, * for required
+---------------------------------+
| [Icon] Placeholder text...      |  <- Input with optional leading icon
+---------------------------------+
| Helper text or character count  |  <- Below input, muted color
| Error: This field is required   |  <- Red, replaces helper on error
+---------------------------------+
```

**Rules:**
- Label is always above the input, never floating inside
- Required indicator is an asterisk `*` after the label text (not red color)
- Helper text and error text occupy the same space; error replaces helper when active
- Leading icons are optional; use them for fields where context helps (email, phone, search)
- Character count appears right-aligned in the helper text area for limited fields

---

## 3. Field States

| State | Web (Bootstrap 5) | Android (Compose) | Visual Cue |
|---------|---------------------|----------------------|-------------|
| Default | `form-control` | `OutlinedTextField` | Gray border |
| Focus | `:focus` blue border | `focusedBorderColor` | Blue/primary border + label color change |
| Filled | Value present | Value present | Default border, value displayed |
| Error | `is-invalid` class | `isError = true` | Red border + error message below |
| Success | `is-valid` class | Custom green indicator | Green border + checkmark icon |
| Disabled | `disabled` attribute | `enabled = false` | Gray background, reduced opacity |
| Loading | Spinner inside field | `CircularProgressIndicator` as trailing icon | Spinner replacing action icon |
| Read-only | `readonly` attribute | `readOnly = true` | No border, plain text appearance |

---

## 4. Essential Code Examples

### Web: Standard Form Field with Validation

```html
<div class="mb-3">
  <label class="form-label required" for="email">Email Address</label>
  <input type="email" class="form-control" id="email" name="email"
         placeholder="john@example.com" required autocomplete="email"
         aria-describedby="email-help email-error">
  <div id="email-help" class="form-text">We'll never share your email.</div>
  <div id="email-error" class="invalid-feedback">Please enter a valid email.</div>
</div>
```

**Key points:**
- `required` class on label shows the asterisk (Tabler CSS convention)
- `aria-describedby` links both helper and error text for screen readers
- `autocomplete="email"` enables browser autofill
- `invalid-feedback` is hidden by default, shown when `is-invalid` is on the input

### Web: Blur Validation with JavaScript

```javascript
document.querySelectorAll('.form-control[required]').forEach(input => {
    input.addEventListener('blur', function () {
        if (!this.checkValidity()) {
            this.classList.add('is-invalid');
            this.classList.remove('is-valid');
        } else {
            this.classList.remove('is-invalid');
            this.classList.add('is-valid');
        }
    });
});
```

### Android: Standard Form Field with Validation

```kotlin
@Composable
fun ValidatedTextField(
    value: String,
    onValueChange: (String) -> Unit,
    label: String,
    error: String? = null,
    helperText: String? = null,
    leadingIcon: @Composable (() -> Unit)? = null,
    keyboardOptions: KeyboardOptions = KeyboardOptions.Default,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier) {
        OutlinedTextField(
            value = value,
            onValueChange = onValueChange,
            label = { Text(label) },
            leadingIcon = leadingIcon,
            isError = error != null,
            keyboardOptions = keyboardOptions,
            supportingText = {
                Text(
                    text = error ?: helperText ?: "",
                    color = if (error != null) MaterialTheme.colorScheme.error
                            else MaterialTheme.colorScheme.onSurfaceVariant
                )
            },
            modifier = Modifier.fillMaxWidth()
        )
    }
}
```

### Android: Blur-Equivalent Validation (Focus Change)

```kotlin
var emailTouched by remember { mutableStateOf(false) }
val emailError = if (emailTouched && !isValidEmail(email)) "Invalid email" else null

OutlinedTextField(
    value = email,
    onValueChange = { email = it },
    label = { Text("Email Address") },
    isError = emailError != null,
    supportingText = { emailError?.let { Text(it) } },
    modifier = Modifier
        .fillMaxWidth()
        .onFocusChanged { if (!it.isFocused) emailTouched = true }
)
```

---

## 5. Multi-Step Form Pattern (Wizard)

Use when a form exceeds 7 fields or spans logically distinct sections.

### Structure

```
Step 1          Step 2          Step 3          Review
[Personal] ---> [Address] ---> [Payment] ---> [Summary]
  (active)       (pending)      (pending)      (pending)
```

### Rules

- **Progress indicator:** Show step number + label. Mark completed steps with green checkmark.
- **Navigation:** Back and Next buttons. Save draft state on each step transition.
- **Validation:** Validate the current step completely before allowing progression to next.
- **Summary step:** Display all collected inputs in read-only form for review before final submit.
- **Persistence:** Store partial data in session (web) or ViewModel (Android) so refresh/rotation does not lose progress.

### Web Implementation

Use Tabler's steps component. Each step renders inside a card body. Hide/show steps with JS. Store step data in a hidden form or session storage.

```html
<div class="steps steps-counter steps-blue mb-4">
  <a href="#" class="step-item active">Personal Info</a>
  <a href="#" class="step-item">Address</a>
  <a href="#" class="step-item">Review</a>
</div>
<div class="card card-body" id="step-1">
  <!-- Step 1 fields here -->
</div>
```

### Android Implementation

Use `HorizontalPager` with a custom step indicator composable. Each page is a composable form section. State lives in the ViewModel.

```kotlin
@Composable
fun WizardForm(viewModel: WizardViewModel = hiltViewModel()) {
    val pagerState = rememberPagerState(pageCount = { viewModel.stepCount })

    Column {
        StepIndicator(
            currentStep = pagerState.currentPage,
            totalSteps = viewModel.stepCount,
            stepLabels = viewModel.stepLabels
        )
        HorizontalPager(state = pagerState, userScrollEnabled = false) { page ->
            when (page) {
                0 -> PersonalInfoStep(viewModel)
                1 -> AddressStep(viewModel)
                2 -> ReviewStep(viewModel)
            }
        }
        WizardNavButtons(
            onBack = { /* animate to previous */ },
            onNext = { if (viewModel.validateStep(pagerState.currentPage)) /* animate to next */ },
            isLastStep = pagerState.currentPage == viewModel.stepCount - 1
        )
    }
}
```

---

## 6. Form Submission Workflow

Standard sequence for both platforms:

```
1. Client-side validation (all fields)
       |
       v  (all valid?)
2. Disable submit button + show loading spinner
       |
       v
3. Send request
   - Web: POST with CSRF token, FormData or JSON
   - Android: API call via Repository/UseCase
       |
       v
4. Handle response
   +-- Success ----> Toast/Snackbar + redirect or form reset
   +-- Validation error --> Map server errors to individual fields
   +-- Network error ----> Show retry option, preserve form state
       |
       v
5. Re-enable submit button
```

### Web: Submit Handler

```javascript
form.addEventListener('submit', async function (e) {
    e.preventDefault();
    if (!validateAllFields()) return;

    const btn = form.querySelector('[type="submit"]');
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Saving...';

    try {
        const res = await fetch(form.action, {
            method: 'POST',
            body: new FormData(form),
            headers: { 'X-CSRF-TOKEN': csrfToken }
        });
        const data = await res.json();
        if (data.success) {
            Swal.fire('Saved!', data.message, 'success');
        } else {
            mapServerErrors(data.errors); // Set is-invalid on each field
        }
    } catch (err) {
        Swal.fire('Error', 'Network error. Please try again.', 'error');
    } finally {
        btn.disabled = false;
        btn.innerHTML = 'Save';
    }
});
```

### Android: Submit in ViewModel

```kotlin
fun submit() {
    if (!validateAll()) return
    _uiState.update { it.copy(isSubmitting = true) }
    viewModelScope.launch {
        repository.submitForm(formData)
            .onSuccess {
                _events.emit(FormEvent.Success("Saved successfully"))
            }
            .onFailure { error ->
                when (error) {
                    is ValidationException -> _uiState.update {
                        it.copy(fieldErrors = error.fieldErrors)
                    }
                    else -> _events.emit(FormEvent.Error("Network error. Retry?"))
                }
            }
        _uiState.update { it.copy(isSubmitting = false) }
    }
}
```

---

## 7. Touch Target and Spacing Rules

| Element | Min Size (Web) | Min Size (Android) | Gap Between Elements |
|---------|---------------|--------------------|-----------------------|
| Text input | 44px height | 56dp height | 16px / 16dp |
| Checkbox / Radio | 44 x 44px | 48 x 48dp | 12px / 12dp |
| Button | 44px height | 48dp height | 8px / 8dp |
| Switch | 44px clickable area | 48dp clickable area | 12px / 12dp |

**Additional spacing rules:**
- Form sections separated by 24px / 24dp with a subtle divider or heading
- Label to input gap: 4px / 4dp
- Input to helper/error text gap: 4px / 4dp
- Submit button gets 24px / 24dp top margin from last field

---

## 8. Form DOs and DON'Ts

### DO

- Use visible labels above every input (never placeholder-only)
- Validate on blur, not on keystroke
- Show total error count on submit when multiple errors exist
- Preserve all form data on validation failure
- Use `autocomplete` attributes: `name`, `email`, `tel`, `address-line1`, `cc-number`
- Group related fields with `<fieldset>` + `<legend>` (web) or section headers (Android)
- Support keyboard Enter to submit on the last field
- Auto-focus the first field on form load
- Show character count for fields with a max length
- Use `inputmode` (web) and `keyboardOptions` (Android) to show the correct keyboard

### DON'T

- Don't use CAPTCHA unless absolutely necessary (prefer honeypot fields)
- Don't reset the form on validation error
- Don't disable the submit button until all fields are valid (let users click to discover errors)
- Don't use a dropdown select for fewer than 5 options (use radio buttons instead)
- Don't use multi-select dropdowns (use checkboxes instead)
- Don't split phone numbers or dates into multiple input fields
- Don't require users to match a format you could auto-format (phone, currency, card number)
- Don't use red color for required field indicators (use asterisk `*`)
- Don't put placeholder text that disappears as the only guidance for format
- Don't use generic error messages ("Invalid input") -- be specific ("Email must include @")

---

## 9. Common Form Types -- Quick Patterns

| Form Type | Key Fields | Special Considerations |
|-----------|-----------|------------------------|
| Registration | Name, email, password, confirm | Password strength meter, terms checkbox |
| Login | Email/username, password | "Remember me" checkbox, "Forgot password" link |
| Search / Filter | Keyword, dropdowns, date range | Instant apply (no submit button), clear-all action |
| Data Entry (CRUD) | Dynamic per entity | Pre-fill on edit, confirm on delete, dirty-form warning |
| Settings / Profile | Grouped preferences | Auto-save toggle or explicit save, section navigation |
| Checkout / Payment | Address, card, billing | PCI considerations, address autocomplete, order summary |
| Clinical / Medical | Vitals, notes, medications | Unit validation, required-field enforcement, audit trail |

---

## 10. Integration with Existing Skills

```
form-ux-design (this skill)
    |
    +-- webapp-gui-design ---------> Web form components, Tabler template pages
    +-- jetpack-compose-ui --------> Android form composables, Material 3 theming
    +-- pos-sales-ui-design -------> POS forms: customer entry, payment, invoice
    +-- api-error-handling --------> Server validation error mapping to form fields
    +-- vibe-security-skill -------> CSRF tokens, XSS prevention, input sanitization
    +-- dual-auth-rbac ------------> Login/registration forms, role-based field visibility
    +-- image-compression ---------> File upload fields with client-side compression
    +-- mysql-best-practices ------> Backend storage for form data, safe queries
```

**Usage pattern:** Load `form-ux-design` alongside the primary skill for your platform. For example:
- Building a web admin panel? Load `webapp-gui-design` + `form-ux-design`
- Building an Android data entry app? Load `jetpack-compose-ui` + `form-ux-design`
- Building POS forms? Load `pos-sales-ui-design` + `form-ux-design`

The form skill provides the UX rules and patterns; the platform skill provides the component library and architecture.
