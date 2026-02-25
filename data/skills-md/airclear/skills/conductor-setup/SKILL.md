---
name: conductor-setup
description: Scaffolds the project and sets up the Conductor environment for Context-Driven Development. Use when starting a new project or initializing the Conductor workflow in an existing (brownfield) project. This skill guides the user through project discovery, product definition, tech stack configuration, and initial track planning.
---

# Conductor Setup

## Overview

This skill transforms a standard repository into a **Conductor-managed project**. It establishes the "Source of Truth" by creating structured documentation for the product vision, technical standards, and development workflows.

## Workflow Overview

The setup process follows these sequential phases:

1.  **Project Discovery:** Determines if the project is New (Greenfield) or Existing (Brownfield).
2.  **Product Definition:** Collaborative creation of `product.md` and `product-guidelines.md`.
3.  **Tech Stack:** Definition of the project's technical foundation in `tech-stack.md`.
4.  **Configuration:** Selection of code style guides and customization of `workflow.md`.
5.  **Track Generation:** Creation of the first unit of work (Track) with a `spec.md` and `plan.md`.

## State Management

Conductor tracks setup progress in `conductor/setup_state.json`. If the session is interrupted, you MUST check this file to resume from the `last_successful_step`.

- `2.1_product_guide` → Resume at Product Guidelines.
- `2.2_product_guidelines` → Resume at Tech Stack.
- `2.3_tech_stack` → Resume at Code Styleguides.
- `2.4_code_styleguides` → Resume at Workflow.
- `2.5_workflow` → Resume at Initial Track Generation.
- `3.3_initial_track_generated` → Setup complete.

## Implementation Details

Refer to the following protocols for detailed procedural instructions:

### 1. Initialization and Resolution
- **Resolution Protocol:** [references/resolution-protocol.md](references/resolution-protocol.md) - How to find Conductor artifacts.
- **Project Discovery:** [references/project-discovery.md](references/project-discovery.md) - Brownfield vs Greenfield detection logic.

### 2. Product Documentation
- **Product and Tech Stack:** [references/product-setup.md](references/product-setup.md) - Interactive questioning and document generation.

### 3. Standards and Workflow
- **Configuration:** [references/configuration.md](references/configuration.md) - Copying templates and customizing the development cycle.

### 4. Planning the First Track
- **Track Generation:** [references/track-generation.md](references/track-generation.md) - Creating the first `spec.md` and `plan.md`.

## Mandatory Constraints

- **TDD Integration:** When generating `plan.md`, you MUST adhere to the TDD principles defined in `workflow.md` (Red/Green/Refactor tasks).
- **Universal File Resolution:** ALWAYS use the protocol in `references/resolution-protocol.md` to find or verify files.
- **Git Hygiene:** Setup concludes with a commit of all `conductor/` files.

## Assets

Templates used during setup are located in `assets/templates/`:
- `workflow.md`: The base development workflow.
- `code_styleguides/`: Language-specific style guides (Python, TypeScript, Go, etc.).
