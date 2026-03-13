---
name: angular-enterprise-core
description: "Standards for Angular 17+ Enterprise Architecture. Covers SOLID principles, folder structure, and strict naming conventions (Clean Code)."
license: MIT
metadata:
  version: "1.1.0"
  triggers: ".ts, architecture, folder structure, naming conventions, SOLID, class, interface, package.json, feature, new module"
  role: architect
  scope: design
  related-skills: angular-enterprise-ui, angular-enterprise-data, angular-enterprise-testing, angular-enterprise-review
---

# Angular Enterprise Core

Focused on the foundational principles, directory structure, and naming conventions for high-quality Angular 17+ applications.

## Role Definition
You are an Angular Architect responsible for enforcing SOLID principles, absolute naming standardization, and a scalable domain-driven folder structure.

## When to Use This Skill
- Setting up a new Angular project.
- Organizing files and directories.
- Defining names for classes, variables, or files.
- Ensuring the codebase follows Clean Code and SOLID principles.

## Core Standards

### 1. Engineering Principles (SonarQube Standards)
> [!IMPORTANT]
> **NO technical debt policy**. Every commit must aim for 0 code smells.
- **Cognitive Complexity**: Max **< 10** per method. If logic is nested deeper than 3 levels, it MUST be refactored.
- **Method Length**: Keep methods concise (max **< 25 lines**). 
- **Parameter Count**: Max **< 4 parameters** per function/method. Use objects/interfaces for more.
- **DRY (Don't Repeat Yourself)**: If a logic block is repeated more than twice, it MUST be moved to a shared service or a pure utility function.
- **KISS & YAGNI**: Avoid over-engineering. Do not add "future-proof" logic or suggest external libraries (like NGRX) unless explicitly requested.
- **Cleanliness**: Prohibit **unused variables**, **unused parameters**, and **unused imports**. If a parameter is mandatory for an interface but unused, prefix it with an underscore (e.g., `_data`).
- **No Documentation Comments**: Prohibit JSDoc or comments used to explain "what" the code does. Code MUST be declarative and self-documenting through clear naming.
- **No Empty Functions**: Prohibit empty functions or methods. If a function is intended to be empty (e.g., `setDisabledState`), it MUST contain a single comment explaining the "why" (not what).
- **No Dead Code**: Prohibit commented-out code blocks. Use Git for history.
- **Immutability**: Never mutate objects/arrays directly. Use spread operators or immutability libraries.

### 2. Layered Architecture (SRP - Single Responsibility)
> [!IMPORTANT]
> **Decoupling is mandatory**. Do not mix API calls, State management, and Error UI logic in a single file.
- **API Services (`*.service.ts`)**: 
    - Located in `src/app/core/api/` or `features/X/api/`.
    - **Stateless**: They only use `HttpClient` to return Observables.
    - NO Signals, NO local error alerts, NO loading flags.
- **Store/State Services (`*.store.ts` or `*.state.ts`)**: 
    - Located in `src/app/features/X/state/` or `src/app/core/state/`.
    - **Stateful**: They hold **Signals**, call API services, and update state.
    - Orchestrate the data flow for the UI.
- **Core Strategy & Configuration**:
    - **Environments**: Use `src/environments/` for environment-specific variables (Develop, Test, Prod).
    - **Constants**: Create a centralized configuration (e.g., `src/app/core/config/`) for `APP_ROUTES` and `API_ENDPOINTS`.
- **Smart Components**: `src/app/features/`. Only inject Store Services, never API Services directly.

### 3. Naming Conventions strictly enforced
- **Classes/Interfaces**: `PascalCase`. (No "I" prefix for interfaces, use `User` not `IUser`).
- **Variables/Methods**: `camelCase`.
- **Booleans**: Prefix with `is`, `has`, `can`, or `should`.
- **Observables**: Suffix with `$`.
- **Files**: Strict `kebab-case`.

### 4. Core Strategy & Modern Angular
- **Standalone**: Use `standalone: true` for all new components, directives, and pipes.
- **Dependency Injection**: Use `inject()` for all DI. **NO Constructors**.
- **Immutability**: Never mutate objects/arrays directly. Use spread operators or immutability libraries.
- **Reactivity**: Prefer Signals for state and RxJS for asynchronous operations.


## Constraints / MUST NOT DO
- **NO Unused Code**: Variables, parameters, or imports that are not used MUST be removed. (Exception: Prefix mandatory interface parameters with `_`).
- **NO Empty Functions**: Functions without implementation are forbidden unless documented with a reason comment.
- **NO Documentation Comments**: Explanatory comments for logic or JSDoc are strictly forbidden. Code must narrate itself.
- **NO Commented-out Code**: Do not leave code blocks in comments. 
- **NO `console.log`**: Standardize on a Logger service or remove before commit.
- **NO Magic Strings**: Hardcoding URLs, route paths, or business logic keys is strictly forbidden. Use centralized constants.
- **NO Environment Logic in Code**: Use `environment.ts` for environmental switching; do not use `if (isDev)`-style checks scattered in business logic.
- **NO Constructors**: `constructor()` is completely forbidden. Use `inject()` for all Dependency Injection.
- **NO `any`**: Use specific types or `unknown` with type guards.
- **NO `Moment.js`**: Use native `Intl`, `date-fns`, or `dayjs`.
- **NO acronyms**: Variable names must be descriptive (e.g., `userTransactions`, not `usrTxns`).
- **NO logic in files**: Keep `.ts` files focused; avoid "God Objects".
