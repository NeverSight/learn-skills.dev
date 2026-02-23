---
name: mantine-combobox
description: >
  Build custom dropdown/select/autocomplete/multiselect components using Mantine's Combobox
  primitives. Use this skill when: (1) creating a new custom select-like component with
  Combobox primitives, (2) building a searchable dropdown, (3) implementing a multi-select
  or tags input variant, (4) customizing option rendering, (5) adding custom filtering logic,
  or (6) any task involving useCombobox, Combobox.Target, Combobox.Option, or Combobox.Dropdown.
---

# Mantine Combobox Skill

## Overview

`Combobox` provides low-level primitives for building any select-like UI. The built-in
`Select`, `Autocomplete`, and `TagsInput` components are all built on top of it.

## Core Workflow

### 1. Create the store

```tsx
const combobox = useCombobox({
  onDropdownClose: () => combobox.resetSelectedOption(),
  onDropdownOpen: () => combobox.selectFirstOption(),
});
```

### 2. Render structure

```tsx
<Combobox store={combobox} onOptionSubmit={handleSubmit}>
  <Combobox.Target>
    <InputBase
      component="button"
      pointer
      rightSection={<Combobox.Chevron />}
      onClick={() => combobox.toggleDropdown()}
    >
      {value || <Input.Placeholder>Pick value</Input.Placeholder>}
    </InputBase>
  </Combobox.Target>
  <Combobox.Dropdown>
    <Combobox.Options>
      {options.map((item) => (
        <Combobox.Option value={item} key={item}>{item}</Combobox.Option>
      ))}
    </Combobox.Options>
  </Combobox.Dropdown>
</Combobox>
```

### 3. Handle submit

```tsx
const handleSubmit = (val: string) => {
  setValue(val);
  combobox.closeDropdown();
};
```

## Target Types

| Scenario | Use |
|---|---|
| Button trigger (no text input) | `<Combobox.Target targetType="button">` |
| Input trigger | `<Combobox.Target>` (default) |
| Pills + separate input (multi-select) | `<Combobox.DropdownTarget>` + `<Combobox.EventsTarget>` |

## References

- **[`references/api.md`](references/api.md)** — Full API: `useCombobox` options and store, all sub-component props, CSS variables, Styles API selectors
- **[`references/patterns.md`](references/patterns.md)** — Code examples: searchable select, multi-select with pills, groups, custom rendering, clear button, form integration
