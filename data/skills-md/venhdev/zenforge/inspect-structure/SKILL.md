---
name: inspect-structure
description: "Audit source code modules for structural smells, God classes, and duplication anti-patterns before refactoring."
disable-model-invocation: true
---

# inspect-structure — Code Quality & Structural Debt Inspector

## Domain Rubric

### 1. Scope & Operational Boundaries

- **Structural Debt vs. Syntax Formatting**: Confine analysis strictly to structural, OOP, and cognitive debt across module, class, and method tiers; defer whitespace, semicolons, and styling nits entirely to native linters.
- **Architectural Cohesion vs. Line Quotas (LOC / `wc -l`)**: Prohibit raw line counts (LOC) or `wc -l` as a primary metric or verdict for "God Class". Assess structural cohesion, actor boundaries, and I/O coupling instead of file length. Distinguish declarative UI component hierarchies (markup, layout trees, responsive styling) and configuration/token registries from OOP God Classes; an expansive declarative view component bound to a single presenter/controller is architecturally valid, whereas a compact class interweaving persistence, network transport, and domain state is a dangerous God Class.
- **Architectural Form vs. Business Logic**: Audit structural cohesion and maintainability exclusively; never evaluate domain business rules, pricing logic, or math formulas without authoritative specs (route bug isolation to `/diagnose`; route spec drift to `/assay`).
- **Read-Only Audit vs. Code Mutation**: Deliver structured inspection dossiers only; forbid modifying files on disk, generating code diffs, or applying automatic refactorings (route remediation planning to `/changeset`).

### 2. Structural Inspection Dimensions

1. **Class Cohesion & SRP (God Class)**
   - **Evaluation Criteria**:
     - *Lack of Cohesion (LCOM)*: Assess whether methods operate on a shared state cluster or partition into isolated, disjoint state silos.
     - *Responsibility & Actor Clustering*: Confirm whether the class serves multiple external actors, disparate lifecycles, or unrelated subsystem concerns (e.g., storage, transport, hardware drivers).
     - *Boundary Separation*: Verify whether presentation/UI components execute I/O, manage persistence, or perform transport requests directly instead of delegating to domain controllers, presenters, or state notifiers.
   - **True Anti-Patterns**: Mixing direct I/O or persistence into presentation components; coordinating multiple independent aggregate roots in one service; violating Single Responsibility (multiple actors or axes of change).
   - **False Positives to Avoid**: Never flag a God class solely on line counts (LOC); tolerate expansive declarative UI trees, view styling, serialization tables, and configuration/token registries when bound to a single cohesive responsibility.
   - **Remedy**: Decompose into single-responsibility domain services, value objects, controllers/presenters, or strategy delegates.
   - **Micro-Snippets**:
     ```text
     Smell (OOP God Class):    class OrderManager { calculateTax(); sendEmail(); saveToDb(); renderPdf(); }
     Remedy:                   class OrderService delegates to TaxCalculator, OrderMailer, OrderRepository, PdfRenderer.

     Smell (UI Boundary Leak): class ProfileView { render() { http.get("/user"); db.save(); } }
     Remedy:                   ProfileView binds to ProfileController; controller coordinates UserService and Repository.
     ```

2. **Method & Flow Complexity (Long Method / Deep Nesting)**
   - Smell: Methods exceeding manageable length, control-flow nesting ≥ 3 levels deep, arrow anti-pattern, or high cognitive load.
   - Remedy: Invert conditions into guard clauses, flatten nested blocks, and decompose into focused single-task helper subroutines.
   - Micro-Snippet:
     ```text
     Smell:  void process() { if (a) { while (b) { if (c) { try { ... } } } } }
     Remedy: Use guard clauses for early returns; extract loop bodies into private subroutines.
     ```

3. **Systemic Duplication (Macro & Micro DRY)**
   - Smell: Copy-pasted algorithmic routines, multi-step validation sequences, or error handling pipelines spanning multiple classes, files, or methods.
   - Remedy: Extract shared rules into pure functions or composed helpers; consider base abstractions only when duplicated logic shares lifecycle, dependencies, and ownership. Each call site retains its own transaction-boundary verification.
   - Micro-Snippet:
     ```text
     Smell:  ServiceA and ServiceB replicate identical decision logic inside their own transactions.
     Remedy: Extract a pure function accepting a state snapshot; each service retains its own transaction, lock, and state read.
     ```

4. **Coupling & Encapsulation Bleed**
   - Smell: Methods manipulating internal data of external classes (Feature Envy); classes exposing mutable internal collections directly via getters.
   - Remedy: Apply "Tell, Don't Ask"; encapsulate state mutations behind domain methods; return immutable snapshots or defensive copies.
   - Micro-Snippet:
     ```text
     Smell:  if (order.getCustomer().getAddress().getCountry().equals("US")) { ... }
     Remedy: if (order.isDomesticDelivery()) { ... }
     ```

5. **Polymorphism & Strategy Deficits (Scattered Branching)**
   - Smell: Parallel `switch(type)` or `if (type == A)` cascades scattered across multiple classes, inducing Shotgun Surgery on variant changes.
   - Remedy: Consider Strategy or Polymorphism when variants evolve independently and new variants force multi-file edits. Prefer explicit conditionals when branches are cohesive cases of one policy in one location; evaluate cohesion and change cost before extraction.
   - Micro-Snippet:
     ```text
     Smell:  PaymentService, InvoiceService, and EmailService all maintain parallel switch (user.getPlanTier()).
     Remedy: Encapsulate tier-specific behaviors in PlanTier strategies (three independent services change in lockstep per new tier).
     ```

6. **Robustness & Resource Hygiene**
   - Smell: Swallowing errors via empty catch blocks; unmanaged streams, database connection handles, or event listeners lacking cleanup hooks.
   - Remedy: Explicitly handle or rethrow with contextual metadata; encapsulate resource lifecycles within deterministic disposal blocks (`defer`, `finally`, `using`).
   - Micro-Snippet:
     ```text
     Smell:  try { connect(); } catch (Exception e) {}
     Remedy: try { connect(); } catch (Exception e) { logger.error("DB connection failed", e); throw new ServiceUnavailableException(e); }
     ```

## Canonical Output Contract

```markdown
# Structural Inspection Dossier: <Target Scope / Module>

## 1. Executive Summary
- **Target Inspected**: `<file_or_directory_path>`
- **Health Rating**: <CLEAN | MODERATE_DEBT | CRITICAL_DEBT>
- **Primary Bottleneck**: <Single-sentence summary of greatest structural risk>

## 2. Technical Debt Catalog

### [<CRITICAL | MAJOR | MINOR>] <Dimension Name>: `<Target Entity / Symbol>`
- **Location**: [<file>#L<N>-L<M>](file:///path/to/file#L<N>-L<M>)
- **Smell**: <Observable anti-pattern description and maintainability impact>
- **Remedy**: <Exact architectural decomposition or extraction path>

*(Repeat for each distinct structural finding; emit 'No structural code smells observed across rubric dimensions' if clean)*
```

### Routing

- Multi-file structural refactoring, God class decomposition, or shared abstraction extraction → (via /changeset).
- Suspected runtime functional bugs or test failures → (via /diagnose).

## Execution Protocol

### Phase 1: Scope Triage & Macro Grounding

1. Ingest target path (`file`, `directory`, or `subsystem`).
2. Identify primary structural anchors (classes, module entrypoints, shared utilities) using symbol and file tools.

### Phase 2: Scale-Adaptive Inspection

- *In-Turn Execution* (< 10 files or cohesive module): Audit code directly in-turn against rubric dimensions.
- *Subagent Fan-Out* (broad multi-package subsystems or repositories): Launch concurrent `research` subagents dynamically scaled to partitioned slices or caller-declared budget (Role: `Structural Inspector (<Slice>)`), seeded with slice coordinates, discovered anchors, Domain Rubric, and Canonical Output Contract.

### Phase 3: Synthesis & Turn-Halt Gate (Fan-in)

1. Reconcile and deduplicate subagent findings into the Canonical Output Contract.
2. Assign definitive Health Rating:
   - `CLEAN`: Zero structural defects breaching rubric.
   - `MODERATE_DEBT`: Isolated encapsulation leaks, scattered conditionals, or minor duplication.
   - `CRITICAL_DEBT`: Pervasive God classes, cross-subsystem copy-paste, or systemic resource leaks.
3. Emit the completed Inspection Dossier into conversation stream and halt turn immediately.
