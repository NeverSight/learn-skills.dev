---
name: 02-implement-features
description: Implement planned Antonella plugin features (models, services, controllers, APIs, and UI). Use after architecture and implementation plan are defined.
---

# Skill: 02-implement-features (Engineering & UI)

## 📜 Source of Truth
> **Standard**: [Architecture Standards](../../normative/architecture_standards.md)
> **Standard**: [Database Standards](../../normative/database_standards.md)
> **Standard**: [Security Standards](../../normative/security_standards.md)

## 🎯 Purpose
Translate the `implementation_plan.md` into high-performance code. This skill handles the heavy lifting: building models, services, request-handling layers, and orchestrating UI development based on user preferences. **You act as a senior backend and frontend engineer.**

---

## 🗣️ Agent Interaction Protocol — The Engineering Phase

> [!CAUTION]
> As a modern agent, review the `implementation_plan.md` first. If any feature involves a user interface (Admin pages, frontend views), you MUST ask the user how to proceed regarding the UI before writing HTML/CSS.

**First Action:** Outline the features to be built based on the plan. If UI is required, present the UI options:

"I am ready to implement the features outlined in the plan. I see that we need to build some user interfaces. How would you like me to handle the UI design?"

**Option A: Standard WordPress UI**
I will write clean, native WordPress HTML/CSS using standard admin classes and components.

**Option B: Custom Frontend Stack (Vue/React/Tailwind)**
I will set up standard API endpoints and you or I will configure a modern JS framework to consume them.

**Option C: Stitch-UI / External Generator**
If you have the `stitch-ui` skill pack installed, I will delegate the UI creation to it. *(Note: only select this if you actively use stitch-ui).*

*Wait for the user's response to proceed.*

---

## 🔄 Execution Protocol

### 🧭 Phase 1: Data Engineering
- **Models**: Create `src/Models/` classes for custom data. Use `$wpdb->prepare` for every raw query to ensure security against SQL injection.
- **CPTs**: Ensure all post types are registered correctly in `config/Config.php`.

### 🧭 Phase 2: Logic Engineering (Services)
Extract complex business rules into `src/Services/` to ensure code reusability and testability. Do not place business logic directly in the Controllers.

### 🧭 Phase 3: Delivery Mechanism (Controllers)
- Map routes in `config/Config.php`.
- Build "Thin Controllers" that orchestrate between Services and Views.
- Implement API endpoints or Webhooks with strict input validation using the `CH\Security` classes.

### 🧭 Phase 4: UI Build (Based on User Option)
- **If Option A:** Write the PHP Views in `src/Views/` ensuring separation of concerns (no inline PHP logic beyond `echo` or simple loops).
- **If Option B:** Ensure the API Controllers are perfectly structured (returning standard JSON with proper HTTP status codes).
- **If Option C:** Output the required `stitch-ui` context block (JSON) to hand off the prompt to the external UI generator. Once the generator produces the HTML, integrate it into `src/Views/`.

---

## 🏁 Quality Gates
- ✅ 100% of raw SQL is encapsulated in Models (No SQL in Controllers).
- ✅ Business logic is decoupled from WordPress hooks and stored in Services.
- ✅ All user input is sanitized via `CH\Security`.
- ✅ No raw HTML is hardcoded directly inside controller methods.
