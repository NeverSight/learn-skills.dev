---
name: rilaykit
description: Best practices and patterns for RilayKit — a headless, type-safe React framework for building dynamic forms and multi-step workflows with builder pattern APIs, Standard Schema validation, and granular Zustand-powered hooks. Use this skill when working on projects that import @rilaykit/core, @rilaykit/forms, or @rilaykit/workflow packages, or when building forms, multi-step flows, component registries, or conditional field logic with RilayKit.
---

# RilayKit

RilayKit is a headless React framework for dynamic forms and multi-step workflows. It uses an immutable builder pattern, Standard Schema validation, and Zustand-powered granular state hooks.

## Architecture Overview

Three packages, layered dependency:

```
@rilaykit/core      → Foundation: ril instance, component registry, validation, conditions
@rilaykit/forms     → Form builder, components, hooks (depends on core)
@rilaykit/workflow   → Flow builder, navigation, persistence, analytics (depends on core + forms)
```

## Core Workflow

### 1. Create a ril instance and register components

```typescript
import { ril } from "@rilaykit/core";

export const r = ril
  .create()
  .addComponent("input", {
    name: "Text Input",
    renderer: InputRenderer,
    defaultProps: { placeholder: "Enter..." },
  })
  .addComponent("select", {
    name: "Select",
    renderer: SelectRenderer,
    validation: { validate: z.string().optional() },
  })
  .configure({
    rowRenderer: RowRenderer,
    bodyRenderer: BodyRenderer,
    fieldRenderer: FieldRenderer,
    submitButtonRenderer: SubmitButtonRenderer,
    stepperRenderer: StepperRenderer,
    nextButtonRenderer: NextButtonRenderer,
    previousButtonRenderer: PreviousButtonRenderer,
  });
```

Every component renderer follows the same interface:

```typescript
import type { ComponentRenderProps } from "@rilaykit/core";

type ComponentRenderer<T = any> = (props: ComponentRenderProps<T>) => React.ReactElement;

// Props received by every renderer:
// id, value, onChange, onBlur, props, error, disabled, context
```

### 2. Build forms with the fluent builder

```typescript
const loginForm = r
  .form("login")
  .add(
    { id: "email", type: "input", props: { label: "Email" }, validation: { validate: [required(), email()] } },
    { id: "password", type: "input", props: { type: "password" }, validation: { validate: [required()] } },
  );
```

- Fields passed to the same `.add()` call render on the **same row** (max 3 per row).
- Separate `.add()` calls create **separate rows**.

### 3. Render forms headlessly

```typescript
import { Form, FormBody, FormSubmitButton } from "@rilaykit/forms";

<Form formConfig={loginForm} onSubmit={handleSubmit} defaultValues={{ email: "" }}>
  <FormBody />
  <FormSubmitButton>Sign In</FormSubmitButton>
</Form>
```

### 4. Build multi-step workflows

```typescript
const onboarding = r
  .flow("onboarding", "User Onboarding")
  .addStep({ id: "personal", title: "Personal Info", formConfig: personalForm })
  .addStep({
    id: "company",
    title: "Company",
    formConfig: companyForm,
    conditions: { visible: when("personal.userType").equals("business") },
    onAfterValidation: async (stepData, helper) => {
      const result = await fetchCompany(stepData.siren);
      helper.setNextStepFields({ company: result.name });
    },
  })
  .configure({ analytics: myAnalytics })
  .build();
```

### 5. Render workflows

```typescript
import { Workflow, WorkflowStepper, WorkflowBody, WorkflowNextButton, WorkflowPreviousButton } from "@rilaykit/workflow";

<Workflow workflowConfig={onboarding} onWorkflowComplete={handleComplete} defaultValues={defaults}>
  <WorkflowStepper />
  <WorkflowBody />
  <div className="flex justify-between">
    <WorkflowPreviousButton />
    <WorkflowNextButton>{(p) => p.isLastStep ? "Complete" : "Next"}</WorkflowNextButton>
  </div>
</Workflow>
```

## Key Patterns

### Validation: Mix libraries freely via Standard Schema

```typescript
import { required, email, pattern, custom, async as asyncValidator } from "@rilaykit/core";
import { z } from "zod";

validation: {
  validate: [
    required("Required"),           // RilayKit built-in
    z.string().email("Invalid"),    // Zod
    asyncValidator(checkEmail, "Already exists"),  // Async
  ],
  validateOnBlur: true,
  debounceMs: 200,
}
```

### Conditions: Fluent builder with logical operators

```typescript
import { when } from "@rilaykit/core";

// Field-level conditions
conditions: {
  visible: when("accountType").equals("business"),
  required: when("accountType").equals("business"),
  disabled: when("status").equals("locked"),
}

// Combine with and/or
when("type").equals("premium")
  .and(when("status").in(["active", "verified"]))
  .or(when("age").greaterThan(65))

// Operators: equals, notEquals, greaterThan, lessThan, contains, notContains,
//            matches, in, notIn, exists, notExists
```

### Granular hooks: Subscribe only to what you need

```typescript
// Field-level (only re-renders when that field changes)
const email = useFieldValue<string>("email");
const errors = useFieldErrors("email");
const { setValue } = useFieldActions("email");

// Form-level
const isSubmitting = useFormSubmitting();
const allValues = useFormValues();
const { reset } = useFormActions();
```

### Reusable step definitions

```typescript
// Define once, use across multiple flows
export const personalInfoStep = (t: TranslationFn): StepDefinition => ({
  id: "personalInfo",
  title: t("steps.personalInfo.title"),
  formConfig: form.create(r).add(/* fields */),
});

// Conditionally add steps
if (!hasExistingClient) {
  workflowFlow = workflowFlow.addStep(personalInfoStep(t));
}
```

## Critical Rules

- **Immutable builders**: Every `.add()`, `.addStep()`, `.configure()` returns a new instance. Chain calls.
- **Headless architecture**: You provide ALL renderers. RilayKit handles state, validation, conditions, navigation.
- **One ril instance per app**: Register all components and renderers once, reuse everywhere.
- **Granular hooks over useFormConfigContext**: Prefer `useFieldValue`, `useFormSubmitting` etc. to avoid unnecessary re-renders.
- **Form data is namespaced by step ID** in workflows: Access via `data.stepId.fieldId`.
- **Always call `.build()`** on workflow configs before passing to `<Workflow>`. Form configs auto-build.

## Detailed API References

- **Core (ril instance, validation, conditions)**: See [references/core.md](references/core.md)
- **Forms (builder, components, hooks)**: See [references/forms.md](references/forms.md)
- **Workflow (flow builder, navigation, persistence, analytics)**: See [references/workflow.md](references/workflow.md)
