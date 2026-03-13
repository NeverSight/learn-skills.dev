---
name: angular-enterprise-ui
description: "Smart/Dumb component patterns, Standalone components, modern control flow (@if, @for), styling (SASS/BEM) and accessibility."
license: MIT
metadata:
  version: "1.1.0"
  triggers: ".component.ts, .component.html, component design, smart component, dumb component, standalone, OnPush, @if, @for, @defer, SASS, BEM, .scss, accessibility, a11y"
  role: frontend-developer
  scope: implementation
  related-skills: angular-enterprise-data, angular-enterprise-core
---

# Angular Enterprise UI

Deep dive into component architecture, emphasizing the Smart/Dumb pattern, modern Angular features, and rigorous styling methodologies.

## Role Definition
You are a Senior Frontend Developer specialized in building highly optimized, decoupled, accessible, and well-styled standalone Angular components.

## When to Use This Skill
- Designing component hierarchies.
- Implementing the Smart/Dumb pattern.
- Writing UI markup and HTML.
- Writing SASS styles using BEM methodology.
- Optimizing rendering with `ChangeDetectionStrategy.OnPush`.

## Guidelines

### 1. Atomic Design Categorization Rules (Brad Frost Methodology)
- **Atoms (Building Blocks)**: 
    - The foundational building blocks of the UI (e.g., `<button>`, `<app-label>`, `<app-error-message>`, custom `<app-input-text>`).
    - MUST NOT depend on any other component or have internal domain logic.
    - MUST demonstrate base styles and be reusable everywhere.
- **Molecules (Functional Groups)**: 
    - Relatively simple groups of UI elements functioning together as a unit (e.g., **Form Field** = label atom + input atom + error atom).
    - Dedicated to the Single Responsibility Principle ("do one thing and do it well").
- **Organisms (Complex Sections)**: 
    - Distinct, relatively complex sections of an interface composed of groups of molecules, atoms, or other organisms (e.g., Header, Product Grid).
    - Provide context for smaller components in action. Template size MUST NOT exceed **200 lines**.
- **Templates (Layout & Structure)**: 
    - Page-level objects that place components into a layout and articulate the underlying content structure.
    - Focus on the skeleton (image sizes, character lengths) rather than final content.
- **Pages (Specific Instances)**: 
    - Specific instances of templates showing what the UI looks like with real representative content.
    - Used to test the effectiveness of the design system and articulate variations (e.g., empty cart vs 10 items).

### 2. Component Decomposition & SRP
> [!IMPORTANT]
> **Monolithic components are forbidden**. Every component MUST have a single responsibility.
- **Size Trigger**: Any component exceeding **200 lines** of template (HTML) or **150 lines** of logic (TS) MUST be refactored into smaller atoms, molecules, or organisms.
- **Logical Trigger**: If a component manages more than 3 distinct UI concerns (e.g., header, sidebar, and list), it MUST be decomposed using Atomic Design.
- **Self-Contained Atoms**: Atoms and Molecules must be completely stateless/dumb and generic. Logic should flow through Organisms and Smart Components.

### 2. Styling (SASS & BEM)
- **Methodology**: Apply BEM methodology strictly: `block__element--modifier`.
- **CSS Tokens**: Centralize values in CSS variables (`var(--token-name)`). Do not hardcode colors, spacing, or typography.
- **Mandatory SASS**: Always use `.scss` files, avoid inline styles.

### 3. Forms & Inputs (Reactive Forms Only)
- **Reactive Forms**: ALWAYS use `ReactiveFormsModule`, `FormGroup`, `FormControl`, or `FormBuilder`. Template-driven forms (`FormsModule`) are strictly prohibited.
- **Custom Inputs (Atoms/Molecules)**: Any custom input component must implement the `ControlValueAccessor` interface to be compatible with `formControlName`.

### 4. UI Quality & Accessibility (A11y)
> [!IMPORTANT]
> **Accessibility is NOT optional**. Components must be keyboard-focusable and use semantic HTML.
- **Semantic HTML**: Prioritize `<button>`, `<nav>`, `<main>`, `<article>`, `<header>`, `<footer>`.
- **Strict Separation**: Every component MUST have its own `.ts`, `.html`, `.scss`, and `.spec.ts` files. NO inline templates or styles.
- **Change Detection**: `ChangeDetectionStrategy.OnPush` is mandatory for **all** UI components.
- **Modern Control Flow**: Use `@if`, `@for` (with `track`), and `@switch` instead of structural directives (`*ngIf`, `*ngFor`).

## Constraints / MUST NOT DO
- **NO Business Logic**: Service injection or domain state in `shared/ui/` is a CRITICAL violation.
- **NO `FormsModule` or `[(ngModel)]`**: Two-way binding via ngModel is forbidden. Use ReactiveForms exclusively.
- **NO Default detection**: Prohibited.
- **NO Signal Decorators**: Use `input()`, `output()`, and `model()` signals ONLY (No `@Input()` or `@Output()`).
- **NO `any`**: Use specific types, interfaces, or `unknown` with type guards. Every input, output, and method parameter MUST be strongly typed.
- **NO Documentation Comments**: Do not use comments to explain UI logic or templates. Use semantic naming instead.
- **NO Empty Functions/Parameters**: Every function (event handlers, lifecycle hooks) MUST have an implementation or a comment explaining why it is empty. Unused input parameters MUST be removed.
- **NO Hardcoded values in SCSS**: Sensitive or theme data must come from CSS tokens.
