---
name: form-design
description: Designs and builds forms people actually finish, with single-column layout, top-aligned labels, correct input types, inputmode and autocomplete, logical grouping, required and optional marking, well-timed validation, clear inline errors, multi-step progress, preserved input and accessible error handling. Use when asked to create a sign-up, checkout, settings or contact form, or to fix validation and errors. Not for wording alone (use ux-writing).
---

# Form Design

Produces forms that ask only for what is needed, are quick to complete on any device, work with autofill and assistive technology, and recover gracefully from errors.

## When to use
- "Build a sign-up / checkout / contact / settings form."
- "Users drop off on this form" or "our validation is annoying."
- Adding validation, error messages, or a multi-step wizard.
- Auditing a form for accessibility or mobile usability.

## Workflow
1. List every field and justify it: who uses the data, and when. Remove or defer anything not needed now; decide which fields are required.
2. Order fields the way users think about them (name before address, card number before expiry) and group related ones under headings or `fieldset` and `legend`.
3. Choose the control per field: text input, radio buttons for 2–5 options so all are visible, select or searchable combobox for longer lists, checkbox for independent choices, textarea for free text.
4. Set `type`, `inputmode`, and `autocomplete` for every input.
5. Define each field's validation rule, when it runs, and the exact error message.
6. If the form is long or covers distinct topics, split it into steps with progress and a final review.
7. Build with native elements and the accessible error pattern below; preserve input on every failure path.
8. Test with keyboard only, a screen reader, browser autofill, a password manager, and a 375px viewport.

## Rules
**Layout and labels**
- Single column, labels above fields; short related pairs (city and postal code) may share a row. Field width hints at the expected length.
- Every control has a visible `label` tied by `for` and `id`. Placeholders never replace labels; put format hints in text under the label.
- Inputs use at least 16px text (smaller text triggers zoom on focus in iOS Safari) and are at least 44px tall on touch layouts.
- The submit button names the outcome ("Create account", "Pay $48.00") and aligns with the fields; full-width on mobile.

**Input attributes**
- Use `type="email"`, `"tel"`, or `"url"` where they fit. For card numbers, codes, and postal codes use `type="text"` with `inputmode="numeric"`, not `type="number"`.
- Always set `autocomplete`: `name`, `email`, `tel`, `street-address`, `postal-code`, `country-name`, `cc-number`, `cc-exp`, `username`, `new-password`, `current-password`, `one-time-code`.
- Allow paste everywhere, including password and code fields, and offer a show-password toggle.
- For known dates such as date of birth, use day, month, and year text inputs rather than a calendar picker.

**Required and optional**
- If most fields are required, mark only the optional ones "(optional)"; otherwise mark required ones and explain the marker once. Add the `required` attribute either way.

**Validation and errors**
- Validate a field on blur and the whole form on submit, never on every keystroke before the first blur. Once a field shows an error, re-check it on input so the error clears as soon as it is fixed.
- Keep the submit button enabled. On a failed submit, show an error summary at the top that links to each invalid field, and move focus to it.
- Show each error directly below its field with an icon and text, not just a red border; set `aria-invalid="true"` and reference the error in `aria-describedby` along with the hint.
- Messages say what is wrong and how to fix it ("Enter a date in the past"), never "Invalid input". Use ux-writing for tone.

**Multi-step and submit**
- Show "Step 2 of 4" with step names, allow Back without losing data, save progress for long forms, and end with a review step that links to each section.
- Do not ask again for information given earlier in the process (WCAG 2.2 Redundant Entry, 3.3.7); prefill it or offer "Same as shipping address".
- On submit, show a loading state on the button and block double submission; after a server error, keep every value and say what to do next.

## Output
- Field inventory: label, control, `type`/`inputmode`/`autocomplete`, required, validation rule, error message.
- Form code with semantic HTML (`form`, `label`, `fieldset`, `legend`, native inputs) and CSS custom properties, or React + Tailwind with the project's existing form library. No new dependencies.
- The accessible field pattern, applied consistently (error state shown):

```html
<label for="email">Email</label>
<p id="email-hint" class="hint">We will send your receipt here.</p>
<input id="email" name="email" type="email" autocomplete="email" required
       aria-describedby="email-hint email-error" aria-invalid="true">
<p id="email-error" class="error">Enter an email address like name@example.com</p>
```

## Avoid
- Placeholder text as the only label.
- Multi-column layouts where tab order and reading order disagree.
- Errors that fire while the user is still typing.
- A disabled submit button with no explanation of what is missing.
- Clearing fields after an error, on Back, or after a failed request.
- Blocking paste in password or code fields, or puzzles with no alternative (WCAG 2.2 Accessible Authentication, 3.3.8).
- Asking for phone, company, or birthday "just in case".
- Custom selects and checkboxes that lose keyboard and screen reader support.

## Final check
- [ ] Every input has a visible, programmatically associated label.
- [ ] `type`, `inputmode`, and `autocomplete` are correct and browser autofill works.
- [ ] Errors appear on blur or submit, below the field, with `aria-invalid` and `aria-describedby`.
- [ ] A failed submit shows a linked error summary and moves focus to it.
- [ ] Required and optional marking is consistent and explained.
- [ ] Input survives errors, Back navigation, and server failures.
- [ ] Works at 375px with 16px input text and targets at least 44px tall.
