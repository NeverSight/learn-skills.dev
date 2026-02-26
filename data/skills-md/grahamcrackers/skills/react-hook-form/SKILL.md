---
name: react-hook-form
description: React Hook Form patterns for performant, type-safe forms with Zod validation, field arrays, multi-step forms, and controlled components. Use when building forms, handling form validation, working with React Hook Form, or when the user asks about form patterns, field arrays, or form state management.
---

# React Hook Form Patterns

## Setup

```shell
npm install react-hook-form @hookform/resolvers zod
```

## Basic Form

```tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const schema = z.object({
    name: z.string().min(1, "Name is required"),
    email: z.string().email("Invalid email"),
});

type FormData = z.infer<typeof schema>;

function ContactForm() {
    const {
        register,
        handleSubmit,
        formState: { errors, isSubmitting },
    } = useForm<FormData>({
        resolver: zodResolver(schema),
        defaultValues: { name: "", email: "" },
    });

    async function onSubmit(data: FormData) {
        await api.createContact(data);
    }

    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            <div>
                <label htmlFor="name">Name</label>
                <input id="name" {...register("name")} />
                {errors.name && <p role="alert">{errors.name.message}</p>}
            </div>
            <div>
                <label htmlFor="email">Email</label>
                <input id="email" type="email" {...register("email")} />
                {errors.email && <p role="alert">{errors.email.message}</p>}
            </div>
            <button type="submit" disabled={isSubmitting}>
                Submit
            </button>
        </form>
    );
}
```

Always provide `defaultValues` — it enables proper reset behavior and avoids uncontrolled-to-controlled warnings.

## Validation Modes

```typescript
useForm({
    resolver: zodResolver(schema),
    mode: "onBlur", // validate on blur (good default for most forms)
    // mode: "onChange",    // real-time validation (can be noisy)
    // mode: "onSubmit",   // validate only on submit (default)
    // mode: "onTouched",  // validate on blur, then on change after first blur
    // mode: "all",        // validate on blur and change
});
```

- `onBlur` is the best default — validates after the user leaves a field without being intrusive.
- `onSubmit` for simple forms where inline validation isn't needed.
- `onChange` for search/filter inputs where immediate feedback matters.

## Controlled Components

For UI libraries (date pickers, selects, rich editors) that don't support `ref`:

```tsx
import { Controller } from "react-hook-form";

<Controller
    name="role"
    control={control}
    render={({ field, fieldState }) => (
        <Select value={field.value} onChange={field.onChange} onBlur={field.onBlur} error={fieldState.error?.message}>
            <Option value="admin">Admin</Option>
            <Option value="member">Member</Option>
        </Select>
    )}
/>;
```

## Field Arrays

Dynamic lists of fields (line items, addresses, tags):

```tsx
import { useFieldArray } from "react-hook-form";

const schema = z.object({
    items: z
        .array(
            z.object({
                name: z.string().min(1),
                quantity: z.coerce.number().min(1),
            }),
        )
        .min(1, "At least one item required"),
});

function OrderForm() {
    const { control, register, handleSubmit } = useForm({
        resolver: zodResolver(schema),
        defaultValues: { items: [{ name: "", quantity: 1 }] },
    });

    const { fields, append, remove } = useFieldArray({
        control,
        name: "items",
    });

    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            {fields.map((field, index) => (
                <div key={field.id}>
                    <input {...register(`items.${index}.name`)} />
                    <input type="number" {...register(`items.${index}.quantity`)} />
                    <button type="button" onClick={() => remove(index)}>
                        Remove
                    </button>
                </div>
            ))}
            <button type="button" onClick={() => append({ name: "", quantity: 1 })}>
                Add Item
            </button>
            <button type="submit">Submit</button>
        </form>
    );
}
```

Always use `field.id` as the `key`, not the array index.

## Multi-Step Forms

```tsx
const Step1Schema = z.object({
    name: z.string().min(1),
    email: z.string().email(),
});

const Step2Schema = z.object({
    address: z.string().min(1),
    city: z.string().min(1),
});

const FullSchema = Step1Schema.merge(Step2Schema);
type FullFormData = z.infer<typeof FullSchema>;

function MultiStepForm() {
    const [step, setStep] = useState(1);
    const form = useForm<FullFormData>({
        resolver: zodResolver(FullSchema),
        defaultValues: { name: "", email: "", address: "", city: "" },
        mode: "onBlur",
    });

    async function handleNext() {
        const fieldsToValidate = step === 1 ? (["name", "email"] as const) : (["address", "city"] as const);

        const valid = await form.trigger(fieldsToValidate);
        if (valid) setStep((s) => s + 1);
    }

    return (
        <form onSubmit={form.handleSubmit(onSubmit)}>
            {step === 1 && <Step1Fields register={form.register} errors={form.formState.errors} />}
            {step === 2 && <Step2Fields register={form.register} errors={form.formState.errors} />}
            {step < 2 ? (
                <button type="button" onClick={handleNext}>
                    Next
                </button>
            ) : (
                <button type="submit">Submit</button>
            )}
        </form>
    );
}
```

Use `trigger()` with specific field names to validate only the current step.

## Watching Values

React to field changes without re-rendering the entire form:

```tsx
const watchedRole = form.watch("role");

// For side effects
useEffect(() => {
    if (watchedRole === "admin") {
        form.setValue("permissions", ["read", "write", "delete"]);
    }
}, [watchedRole]);
```

For performance-critical cases, use `useWatch` from a child component to isolate re-renders.

## Server Errors

Map server-side validation errors to specific fields:

```tsx
async function onSubmit(data: FormData) {
    try {
        await api.createUser(data);
    } catch (error) {
        if (error instanceof ValidationError) {
            error.fields.forEach(({ field, message }) => {
                form.setError(field as keyof FormData, { message });
            });
        } else {
            form.setError("root", { message: "Something went wrong" });
        }
    }
}

// Display root-level errors
{
    form.formState.errors.root && <p role="alert">{form.formState.errors.root.message}</p>;
}
```

## Form Wrapper Component

Create a reusable form wrapper for consistent error display and layout:

```tsx
interface FormFieldProps {
    label: string;
    name: string;
    error?: string;
    children: React.ReactNode;
}

function FormField({ label, name, error, children }: FormFieldProps) {
    return (
        <div>
            <label htmlFor={name}>{label}</label>
            {children}
            {error && <p role="alert">{error}</p>}
        </div>
    );
}
```

## Guidelines

- Always use Zod (or another resolver) for validation — avoid inline `register` validation rules for anything beyond trivial forms.
- Always provide `defaultValues` to `useForm`.
- Use `register` for native HTML inputs. Use `Controller` for custom components.
- Avoid `watch()` in the parent form component for values only needed in a child — use `useWatch` in the child instead.
- Use `form.reset()` after successful submission, not manual state clearing.
- Disable the submit button with `isSubmitting` to prevent double submissions.
