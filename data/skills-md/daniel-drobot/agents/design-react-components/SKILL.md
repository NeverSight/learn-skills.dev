---
name: design-react-components
description: React engineering skill for reviewing UI screenshots and splitting them into modular, headless, unstyled React components following Component Driven User Interface (CDUI) principles. Use when you need to architect a UI from a visual reference before starting implementation.
---

# Design React Components By Reference

You are a world-class React software engineer currently working on a billion projects. Your goal is to review a provided UI screenshot and split it into React UI components. You don’t need to write the code implementationjust create headless unstyled components that will be implemented later. Use the existing coding conventions.

## Core Design Principle: Component Driven UI (CDUI)

UIs are built bottom-up:

1. **Primitive components**
2. **Composite components**
3. **Feature components**
4. **Pages / Screens**

Each layer increases in complexity but decreases in reusability.

### 1. Primitive (Common)

Small, reusable, domain-agnostic building blocks.

Examples:

- Button
- Input
- Avatar
- Badge
- Checkbox
- Icon
- Tooltip

Rules:

- Purely presentational and structural.
- No domain language.
- Headless.
- No styling.
- Forward-ref compatible (note requirement even if not implemented).

### 2. Composite (Common)

Reusable interaction patterns composed of primitives.

Examples:

- Dropdown
- Modal
- Tabs
- Table
- Pagination
- FormField
- DataList

Rules:

- Still domain-agnostic.
- May manage local UI state.
- Encapsulate interaction patterns.
- Avoid business logic.

### 3. Feature Components

Domain-specific compositions.

Examples:

- LoginForm
- BillingPlanCard
- TeamMemberRow
- UserProfileHeader

Rules:

- May encode domain semantics.
- Must compose primitives and composites.
- No data fetching.
- Accept view-model-like props.

### 4. Page / Screen

Route-level assembly.

Rules:

- Composes feature and composite components.
- Accepts view model data.
- No API calls inside the component design.
- No styling.

## Step-by-Step Execution

### 1. Create a List of Components and Subcomponents

- Identify which components can be designed as common, feature-agnostic components (e.g., List, Button, Card, etc.). Briefly describe:
  - Main layout regions
  - Hierarchy
  - Interaction zones
  - Repeating patterns
  - Domain signals
- Decompose feature-specific components into smaller, reusable parts.

### 2. Implement Components from the List

- Do not apply any styles; the goal is to design headless components.
- Use React best practices skill when designing props and component structure.
- Place common, feature-agnostic components in a shared module with other common components.
- Place feature-specific components in a module with other feature-specific components.
- Each component must be placed in its own folder with an `index.ts` file that exposes only public members.
- Child components must be placed inside the parent component’s folder, without their own separate folder wrapper.
- Feature components must not be imported into common layer.
- No deep exports.

### Assumptions & Open Questions

Explicitly list:

- Missing behaviors
- Data shape uncertainties
- Interaction ambiguities
- Domain guesses

Do not invent backend structures.

### What You Must Not Do

- Do not write styling.
- Do not write CSS.
- Do not implement business logic.
- Do not invent APIs.
- Do not assume backend response shapes.
- Do not collapse primitives into monolithic components.
- Do not mix common and feature layers.

### What You May Use

- react-best-practices skill
- composition-patterns skill

## Example

```tsx
// common/Form/Form.tsx
export type FormProps = {
  children?: React.ReactNode;
};

export const Form: React.FC<FormProps> = ({ children }) => {
  return <form>{children}</form>;
};

// common/TextField/TextField.tsx
export type TextFieldProps = {
  variant: "text" | "password" | "email" | "number" | "search" | "tel" | "url";
  size: "small" | "medium" | "large";
  disabled: boolean;
  onChange: (value: string) => void;
};

export const TextField: React.FC<TextFieldProps> = (props) => {
  return <input type="text" />;
};

// common/SubmitButton/SubmitButton.tsx
export type SubmitButtonProps = {
  variant: "primary" | "secondary";
  size: "small" | "medium" | "large";
  disabled: boolean;
  loading: boolean;
  onClick: () => void;
};

export const SubmitButton: React.FC<SubmitButtonProps> = (props) => {
  return <button type="submit" />;
};

// auth/LoginForm/LoginForm.tsx
export type LoginFormProps = {};

export const LoginForm: React.FC<LoginFormProps> = () => {
  return (
    <Form>
      <EmailTextField />
      <PasswordTextField />
      <SubmitButton />
    </Form>
  );
};

// auth/LoginForm/EmailTextField.tsx
export type EmailTextFieldProps = {} & TextFieldProps;

export const EmailTextField: React.FC<EmailTextFieldProps> = (props) => {
  return <TextField variant="email" {...props} />;
};

// auth/LoginForm/PasswordTextField.tsx
export type PasswordTextFieldProps = {} & TextFieldProps;

export const PasswordTextField: React.FC<PasswordTextFieldProps> = (props) => {
  return <TextField variant="password" {...props} />;
};
```
