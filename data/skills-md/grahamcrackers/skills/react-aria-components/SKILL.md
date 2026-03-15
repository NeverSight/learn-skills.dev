---
name: react-aria-components
description: React Aria Components patterns for building accessible, unstyled UI with composition-based architecture. Covers component structure, styling with Tailwind and CSS, render props, collections, forms, selections, overlays, and drag-and-drop. Use when building accessible components, using react-aria-components, creating design systems, or when the user asks about React Aria, accessible UI primitives, or headless component libraries.
---

# React Aria Components

## Overview

React Aria Components is a library of unstyled, accessible components from Adobe. Each component implements W3C ARIA patterns with built-in keyboard navigation, focus management, internationalization, and screen reader support — you bring your own styles.

## Setup

```shell
npm install react-aria-components
```

## Composition Model

Every component maps 1:1 to a DOM element. Build complex widgets by composing parts:

```tsx
import { Button, Dialog, DialogTrigger, Heading, Modal, ModalOverlay } from "react-aria-components";

function ConfirmDialog() {
    return (
        <DialogTrigger>
            <Button>Delete</Button>
            <ModalOverlay className="fixed inset-0 bg-black/50">
                <Modal className="fixed inset-0 flex items-center justify-center">
                    <Dialog className="bg-white rounded-lg p-6 max-w-md">
                        {({ close }) => (
                            <>
                                <Heading slot="title">Confirm Delete</Heading>
                                <p>This action cannot be undone.</p>
                                <div className="flex gap-2 mt-4">
                                    <Button onPress={close}>Cancel</Button>
                                    <Button
                                        onPress={() => {
                                            handleDelete();
                                            close();
                                        }}
                                    >
                                        Delete
                                    </Button>
                                </div>
                            </>
                        )}
                    </Dialog>
                </Modal>
            </ModalOverlay>
        </DialogTrigger>
    );
}
```

## Styling

### With Tailwind CSS

React Aria Components expose data attributes and render props for state-based styling:

```tsx
import { Button } from "react-aria-components";

<Button
    className="rounded-lg px-4 py-2 bg-blue-600 text-white
  hover:bg-blue-700
  pressed:bg-blue-800
  focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2
  disabled:opacity-50 disabled:cursor-not-allowed"
>
    Save
</Button>;
```

React Aria provides Tailwind CSS variants out of the box: `hover`, `pressed`, `focus-visible`, `disabled`, `selected`, `dragging`, `drop-target`, `entering`, `exiting`, etc.

Install the Tailwind plugin for full support:

```shell
npm install tailwindcss-react-aria-components
```

```css
/* In your CSS */
@import "tailwindcss";
@plugin "tailwindcss-react-aria-components";
```

### With Render Props

For dynamic class names or style objects:

```tsx
<Button
    className={({ isPressed, isFocusVisible }) =>
        `rounded-lg px-4 py-2 ${isPressed ? "bg-blue-800" : "bg-blue-600"} ${isFocusVisible ? "ring-2" : ""}`
    }
>
    Save
</Button>
```

### With Vanilla CSS

Use data attributes as selectors:

```css
.my-button {
    background: var(--color-primary);
}

.my-button[data-pressed] {
    background: var(--color-primary-dark);
}

.my-button[data-focus-visible] {
    outline: 2px solid var(--color-focus);
    outline-offset: 2px;
}

.my-button[data-disabled] {
    opacity: 0.5;
}
```

## Common Components

### Button

```tsx
import { Button } from "react-aria-components";

<Button onPress={() => save()} isDisabled={!isValid}>
    Save
</Button>;
```

Use `onPress` instead of `onClick` — it handles keyboard, touch, and pointer events consistently and prevents ghost clicks on mobile.

### TextField

```tsx
import { TextField, Label, Input, FieldError, Text } from "react-aria-components";

<TextField isRequired>
    <Label>Email</Label>
    <Input type="email" className="border rounded px-3 py-2" />
    <Text slot="description">We'll never share your email.</Text>
    <FieldError />
</TextField>;
```

### Select

```tsx
import { Select, Label, Button, SelectValue, Popover, ListBox, ListBoxItem } from "react-aria-components";

<Select>
    <Label>Country</Label>
    <Button>
        <SelectValue />
    </Button>
    <Popover>
        <ListBox>
            <ListBoxItem id="us">United States</ListBoxItem>
            <ListBoxItem id="uk">United Kingdom</ListBoxItem>
            <ListBoxItem id="ca">Canada</ListBoxItem>
        </ListBox>
    </Popover>
</Select>;
```

### ComboBox

```tsx
import { ComboBox, Label, Input, Button, Popover, ListBox, ListBoxItem } from "react-aria-components";

<ComboBox>
    <Label>Assignee</Label>
    <div className="flex">
        <Input className="border rounded-l px-3 py-2" />
        <Button>▼</Button>
    </div>
    <Popover>
        <ListBox>
            {users.map((user) => (
                <ListBoxItem key={user.id} id={user.id}>
                    {user.name}
                </ListBoxItem>
            ))}
        </ListBox>
    </Popover>
</ComboBox>;
```

### Menu

```tsx
import { MenuTrigger, Button, Popover, Menu, MenuItem, Separator, Section, Header } from "react-aria-components";

<MenuTrigger>
    <Button aria-label="Actions">⋯</Button>
    <Popover>
        <Menu onAction={(key) => handleAction(key)}>
            <Section>
                <Header>Edit</Header>
                <MenuItem id="cut">Cut</MenuItem>
                <MenuItem id="copy">Copy</MenuItem>
                <MenuItem id="paste">Paste</MenuItem>
            </Section>
            <Separator />
            <MenuItem id="delete" className="text-red-600">
                Delete
            </MenuItem>
        </Menu>
    </Popover>
</MenuTrigger>;
```

### Tabs

```tsx
import { Tabs, TabList, Tab, TabPanel } from "react-aria-components";

<Tabs>
    <TabList aria-label="Settings" className="flex border-b">
        <Tab id="general" className="px-4 py-2 selected:border-b-2 selected:border-blue-500">
            General
        </Tab>
        <Tab id="security" className="px-4 py-2 selected:border-b-2 selected:border-blue-500">
            Security
        </Tab>
    </TabList>
    <TabPanel id="general">General settings...</TabPanel>
    <TabPanel id="security">Security settings...</TabPanel>
</Tabs>;
```

### Table

```tsx
import { Cell, Column, Row, Table, TableBody, TableHeader, ResizableTableContainer } from "react-aria-components";

<ResizableTableContainer>
    <Table aria-label="Users" selectionMode="multiple">
        <TableHeader>
            <Column isRowHeader>Name</Column>
            <Column>Email</Column>
            <Column>Role</Column>
        </TableHeader>
        <TableBody>
            {users.map((user) => (
                <Row key={user.id}>
                    <Cell>{user.name}</Cell>
                    <Cell>{user.email}</Cell>
                    <Cell>{user.role}</Cell>
                </Row>
            ))}
        </TableBody>
    </Table>
</ResizableTableContainer>;
```

## Collections

React Aria uses a collection API for list-based components (ListBox, Menu, Table, TagGroup, etc.):

### Static

```tsx
<ListBox>
    <ListBoxItem id="one">Option One</ListBoxItem>
    <ListBoxItem id="two">Option Two</ListBoxItem>
</ListBox>
```

### Dynamic

```tsx
<ListBox items={options}>{(item) => <ListBoxItem id={item.id}>{item.name}</ListBoxItem>}</ListBox>
```

### Sections

```tsx
<ListBox>
    <Section>
        <Header>Fruits</Header>
        <ListBoxItem>Apple</ListBoxItem>
        <ListBoxItem>Banana</ListBoxItem>
    </Section>
    <Section>
        <Header>Vegetables</Header>
        <ListBoxItem>Carrot</ListBoxItem>
        <ListBoxItem>Broccoli</ListBoxItem>
    </Section>
</ListBox>
```

## Selection

Control selection on ListBox, Table, GridList, TagGroup, etc.:

```tsx
const [selected, setSelected] = useState<Selection>(new Set());

<ListBox
    selectionMode="multiple" // "none" | "single" | "multiple"
    selectedKeys={selected}
    onSelectionChange={setSelected}
>
    {items.map((item) => (
        <ListBoxItem key={item.id} id={item.id}>
            {item.name}
        </ListBoxItem>
    ))}
</ListBox>;
```

Selection is a `Set<Key>` or the string `"all"` for select-all.

## Forms

React Aria Components integrate with native form validation and React 19 server actions:

```tsx
import { Form, TextField, Label, Input, FieldError, Button } from "react-aria-components";

<Form
    onSubmit={(e) => {
        e.preventDefault(); /* handle */
    }}
>
    <TextField name="email" isRequired type="email">
        <Label>Email</Label>
        <Input />
        <FieldError />
    </TextField>
    <Button type="submit">Submit</Button>
</Form>;
```

### Server Validation

Display server-side errors:

```tsx
const [errors, setErrors] = useState({});

<Form validationErrors={errors}>
    <TextField name="email" isRequired>
        <Label>Email</Label>
        <Input />
        <FieldError />
    </TextField>
</Form>;
```

## Overlays

### Modal Dialog

```tsx
<DialogTrigger>
    <Button>Open</Button>
    <ModalOverlay className="fixed inset-0 bg-black/50 entering:animate-in entering:fade-in exiting:animate-out exiting:fade-out">
        <Modal className="fixed inset-0 flex items-center justify-center entering:animate-in entering:zoom-in-95 exiting:animate-out exiting:zoom-out-95">
            <Dialog className="bg-white rounded-xl p-6 max-w-md">
                {({ close }) => (
                    <>
                        <Heading slot="title">Dialog Title</Heading>
                        <p>Dialog content here.</p>
                        <Button onPress={close}>Close</Button>
                    </>
                )}
            </Dialog>
        </Modal>
    </ModalOverlay>
</DialogTrigger>
```

### Popover

```tsx
<DialogTrigger>
    <Button>Info</Button>
    <Popover className="bg-white shadow-lg rounded-lg p-4 entering:animate-in entering:fade-in exiting:animate-out exiting:fade-out">
        <Dialog>
            <p>Additional information here.</p>
        </Dialog>
    </Popover>
</DialogTrigger>
```

### Tooltip

```tsx
import { TooltipTrigger, Tooltip, Button } from "react-aria-components";

<TooltipTrigger delay={300}>
    <Button>Hover me</Button>
    <Tooltip className="bg-gray-900 text-white px-2 py-1 rounded text-sm">Helpful tooltip text</Tooltip>
</TooltipTrigger>;
```

## DatePicker

```tsx
import {
    DatePicker,
    Label,
    Group,
    DateInput,
    DateSegment,
    Button,
    Popover,
    Dialog,
    Calendar,
    CalendarGrid,
    Heading,
} from "react-aria-components";

<DatePicker>
    <Label>Date</Label>
    <Group className="flex border rounded">
        <DateInput className="flex px-2 py-1">{(segment) => <DateSegment segment={segment} />}</DateInput>
        <Button>📅</Button>
    </Group>
    <Popover>
        <Dialog>
            <Calendar>
                <header className="flex items-center justify-between">
                    <Button slot="previous">◀</Button>
                    <Heading />
                    <Button slot="next">▶</Button>
                </header>
                <CalendarGrid />
            </Calendar>
        </Dialog>
    </Popover>
</DatePicker>;
```

## Drag and Drop

```tsx
import { GridList, GridListItem, useDragAndDrop } from "react-aria-components";

function ReorderableList({ items, onReorder }) {
    const { dragAndDropHooks } = useDragAndDrop({
        getItems: (keys) => [...keys].map((key) => ({ "text/plain": key.toString() })),
        onReorder,
    });

    return (
        <GridList items={items} dragAndDropHooks={dragAndDropHooks} selectionMode="multiple">
            {(item) => <GridListItem>{item.name}</GridListItem>}
        </GridList>
    );
}
```

## Building a Design System

Wrap React Aria Components with your styling conventions:

```tsx
import { Button as AriaButton, type ButtonProps as AriaButtonProps } from "react-aria-components";
import { tv } from "tailwind-variants";

const button = tv({
    base: "inline-flex items-center justify-center rounded-lg font-medium transition-colors focus-visible:ring-2 focus-visible:ring-offset-2",
    variants: {
        variant: {
            primary: "bg-blue-600 text-white hover:bg-blue-700 pressed:bg-blue-800",
            secondary: "bg-gray-100 text-gray-900 hover:bg-gray-200 pressed:bg-gray-300",
            danger: "bg-red-600 text-white hover:bg-red-700 pressed:bg-red-800",
        },
        size: {
            sm: "text-sm px-3 py-1.5",
            md: "text-sm px-4 py-2",
            lg: "text-base px-5 py-2.5",
        },
    },
    defaultVariants: {
        variant: "primary",
        size: "md",
    },
});

interface ButtonProps extends AriaButtonProps {
    variant?: "primary" | "secondary" | "danger";
    size?: "sm" | "md" | "lg";
}

export function Button({ variant, size, className, ...props }: ButtonProps) {
    return <AriaButton className={button({ variant, size, className })} {...props} />;
}
```

This gives you accessible primitives with your design tokens. Use `tailwind-variants` or `cva` for variant management.

## Guidelines

- **Use `onPress` instead of `onClick`** — it handles keyboard, touch, and mouse consistently.
- **Every form field needs a `Label`** — React Aria handles the `htmlFor`/`id` association automatically.
- **Use render props** for state-dependent styling — `className` and `style` accept functions with state like `isPressed`, `isFocusVisible`, `isSelected`.
- **Don't add ARIA attributes manually** — React Aria sets `role`, `aria-*`, and keyboard handlers for you.
- **Drop down to hooks** when a component doesn't fit your use case — `useButton`, `useSelect`, etc. give you full control.
- **Use the Tailwind plugin** (`tailwindcss-react-aria-components`) for clean state variants in class names.
