---
name: design
description: Activates the Product Designer to create UI mockups and specs complying with Polaris. Use when designing user interfaces or planning UI components.
argument-hint: "[UI requirement or component to design]"
---

# Design UI

Create UI mockups and specifications using Polaris design system.

1. **Analyze Requirement**: Read the UI requirement provided in the argument.

2. **Act as Product Designer**:
    * Load the `product-designer` agent persona.
    * Identify the key components needed (e.g., Page, Card, ResourceList).
    * Propose a design:
        * Describe the structure using Polaris component names.
        * Explain the user flow.
        * (Optional) Use `generate_image` to create a low-fidelity mockup if visual clarity is needed.

3. **Review**: Ask the user for feedback on the proposed design.
