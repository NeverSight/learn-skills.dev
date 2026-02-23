---
name: mantine-form
description: >
  Build forms using @mantine/form in the mantine-9 repository. Use this skill when: (1) setting
  up a form with useForm, (2) adding validation rules or async validation, (3) working with nested
  object or array fields, (4) sharing form state across components with createFormContext,
  (5) using uncontrolled mode for performance, (6) using the standalone useField hook, or
  (7) any task involving useForm, getInputProps, onSubmit, insertListItem, or form validation.
---

# Mantine Form Skill

## Core Workflow

### 1. Set up the form

```tsx
const form = useForm({
  mode: 'controlled',       // or 'uncontrolled' for large forms
  initialValues: {
    email: '',
    age: 0,
  },
  validate: {
    email: isEmail('Invalid email'),
    age: isInRange({ min: 18 }, 'Must be at least 18'),
  },
});
```

### 2. Wire inputs with getInputProps

```tsx
<TextInput {...form.getInputProps('email')} label="Email" />
<NumberInput {...form.getInputProps('age')} label="Age" />
```

For checkboxes pass `{ type: 'checkbox' }`:
```tsx
<Checkbox {...form.getInputProps('agreed', { type: 'checkbox' })} label="I agree" />
```

### 3. Handle submission

```tsx
<form onSubmit={form.onSubmit((values) => console.log(values))}>
  ...
  <Button type="submit">Submit</Button>
</form>
```

`onSubmit` only calls the handler when validation passes. To handle failures:
```tsx
form.onSubmit(
  (values) => save(values),
  (errors) => console.log('Validation failed', errors)
)
```

## Validation

### Rules object (most common)
```tsx
validate: {
  name: isNotEmpty('Required'),
  email: isEmail('Invalid email'),
  password: hasLength({ min: 8 }, 'Min 8 chars'),
  confirmPassword: matchesField('password', 'Passwords do not match'),
}
```

### Function (for cross-field logic)
```tsx
validate: (values) => ({
  endDate: values.endDate < values.startDate ? 'End must be after start' : null,
})
```

### When to validate
```tsx
validateInputOnChange: true,        // validate all fields on every change
validateInputOnChange: ['email'],    // validate specific fields only
validateInputOnBlur: true,          // validate on blur instead
```

## Modes

| Mode | State storage | Re-renders | Input props |
|---|---|---|---|
| `'controlled'` (default) | React state | On every change | `value` + `onChange` |
| `'uncontrolled'` | Refs | None | `defaultValue` + `onChange` |

In uncontrolled mode, use `form.key('fieldPath')` as the React `key` prop when you need to force a re-render of an input.

## References

- **[`references/api.md`](references/api.md)** — Full API: `useForm` options, complete return value, `useField`, `createFormContext`, `createFormActions`, all built-in validators, key types
- **[`references/patterns.md`](references/patterns.md)** — Code examples: nested objects, array fields, async validation, form context across components, `transformValues`, `useField` standalone
