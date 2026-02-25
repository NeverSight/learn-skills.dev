---
name: form-design
description: Form UX patterns, field types, multi-step wizards, and layout. Use when building forms, registration flows, or any data collection interfaces.
version: 1.0.0
---

# Form Design

This skill covers form UX patterns — field types, label placement, multi-step wizards, layout grouping, and data collection best practices.

## Use-When

This skill activates when:
- Agent builds forms (login, signup, settings)
- Agent creates multi-step flows or wizards
- Agent designs data collection interfaces
- Agent improves existing form conversion
- Agent groups related fields

## Core Rules

- ALWAYS use visible labels (never placeholder-only)
- ALWAYS group related fields into sections
- ALWAYS indicate required fields visually and programmatically
- ALWAYS inline validate after blur, not on every keystroke
- PREFER single-column layouts for mobile friendliness

## Common Agent Mistakes

- Using placeholder as label (disappears on focus)
- Putting too many fields on one screen
- Not grouping related fields
- Showing all validation errors at once (overwhelming)
- Not indicating required fields clearly

## Examples

### ✅ Correct

```tsx
// Visible labels with proper grouping
<form>
  <fieldset>
    <legend>Personal Information</legend>
    <div className="space-y-4">
      <div>
        <label htmlFor="name">Full Name</label>
        <input id="name" />
      </div>
      <div>
        <label htmlFor="email">Email</label>
        <input id="email" type="email" />
      </div>
    </div>
  </fieldset>
</form>
```

### ❌ Wrong

```tsx
// Placeholder as label
<input placeholder="Enter your name" />

// No grouping, too many fields
<form>
  <input placeholder="Name" />
  <input placeholder="Email" />
  <input placeholder="Phone" />
  <input placeholder="Address" />
  <input placeholder="City" />
  <input placeholder="State" />
  <input placeholder="Zip" />
  {/* ... more fields */}
</form>
```

## References

- [Nielsen Norman Group - Form Design](https://www.nngroup.com/articles/form-design/)
- [Google Material Design - Text Fields](https://m3.material.io/components/text-fields)
- [WebAIM - Forms](https://webaim.org/techniques/forms/)
