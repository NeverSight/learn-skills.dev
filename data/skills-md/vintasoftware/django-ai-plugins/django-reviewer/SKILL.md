---
name: django-reviewer
description: Review Django and Python changes for clarity, consistency, maintainability, ORM or DRF anti-patterns, and project conventions while preserving behavior. Use after Django code changes or when the user explicitly requests review. Report findings by default; apply refinements only when the user expresses explicit edit intent or the host has already authorized edits.
---

# Django Reviewer

Review Django and Python code without changing its intended behavior. Prefer
readable, explicit, project-consistent code over compact or speculative
rewrites.

## Authorization Boundary

- Treat a review request as report-only unless the user expresses explicit edit
  intent or the host has already authorized edits for this task.
- Never approve permissions, change tool configuration, or infer write
  authorization from the existence of this skill.
- When edits are not authorized, return findings and suggested changes without
  modifying files.
- When edits are authorized, change only the reviewed files and verify the
  behavior after editing.

## Focus Scope

1. Prefer explicitly named files or directories when the user supplies them.
2. Otherwise inspect `git diff`, `git diff --cached`, and `git status` to find
   recently modified Django or Python files.
3. If there are no changed files and no explicit target, ask for a target or
   return a bounded no-op. Do not broaden the review to the whole repository.
4. Read enough surrounding code and project instruction files to understand
   local conventions, but keep findings scoped to the target.

## 1. Preserve Functionality

Never change what the code does merely to make it look cleaner. Preserve public
interfaces, outputs, side effects, error behavior, and user-visible behavior.
Any behavior change must be separately justified and explicitly authorized.

## 2. Apply Project Standards

Follow the repository's project instruction files and established conventions:

- Apply PEP 8 and Django's coding style.
- Organize imports using the project's existing isort or formatter conventions.
- Add type hints only where the project already uses them.
- Use Django's built-in exceptions and local exception patterns.
- Keep naming consistent: `snake_case` for functions and variables,
  `PascalCase` for classes, and `UPPER_CASE` for constants.
- Prefer `reverse()` and `reverse_lazy()` to hard-coded URLs.
- Access settings through `django.conf.settings`.

## 3. Enhance Clarity

- Reduce unnecessary nesting with early returns where they improve readability.
- Remove dead or redundant code within the reviewed scope.
- Use descriptive names and keep related logic cohesive.
- Avoid comments that merely restate the code.
- Prefer the Django ORM when it expresses the query clearly.
- Use `select_related()` for foreign-key or one-to-one relationships and
  `prefetch_related()` for reverse foreign keys or many-to-many relationships.
- Prefer Django built-ins over extra dependencies when they solve the same
  problem.
- Prefer `get_object_or_404()` over repetitive `DoesNotExist` handling in views.
- Use queryset operations rather than Python-side filtering when practical.

## 4. Apply Django-Specific Best Practices

### Models

- Keep domain logic in models, managers, or focused services instead of views.
- Use appropriate `Meta` options, database constraints, and indexes.
- Use `TextChoices` or `IntegerChoices` instead of raw choice tuples.
- Define clear relationship names when the project convention requires them.

### Views and URLs

- Keep views focused on HTTP orchestration.
- Apply authentication and permission checks consistently.
- Return appropriate HTTP status codes.
- Choose class-based or function-based views based on the project's patterns,
  not as a blanket preference.

### Django REST Framework

- Prefer `ModelSerializer` for ordinary model CRUD.
- Use `ViewSet` and routers when they reduce duplication.
- Use `get_queryset()` and `get_serializer_class()` for request-dependent
  behavior instead of overriding broad actions unnecessarily.
- Check pagination, filtering, ordering, authentication, and permissions.

### Forms and Validation

- Validate untrusted input at the boundary with forms or serializers.
- Keep cross-field validation in `clean()` or serializer-level validation.
- Prefer database constraints when correctness must survive concurrent writes.

### Testing

- Follow the repository's chosen unittest or pytest style.
- Test behavior rather than private implementation details.
- Use query-count assertions when query performance is part of the contract.
- Mock external services rather than Django internals.

### Queries and Performance

- Flag N+1 query patterns and propose `select_related()` or
  `prefetch_related()` with the concrete relationship path.
- Prefer `.exists()` over `.count() > 0` for existence checks.
- Use `.iterator()` only when streaming semantics and memory behavior warrant
  it.
- Do not claim an optimization without tracing how the queryset is consumed.

## 5. Maintain Balance

Avoid refinements that:

- combine unrelated concerns;
- replace clear code with clever code;
- introduce premature abstractions or dependencies;
- add type hints to an otherwise untyped area;
- change behavior while being presented as cleanup; or
- expand beyond recently modified or explicitly named files.

## Review Process

1. Resolve the bounded target using the Focus Scope rules.
2. Read the surrounding models, serializers, views, URLs, tests, and project
   instructions needed to understand the change.
3. Check for correctness risks, Django anti-patterns, query regressions,
   authorization gaps, validation gaps, and inconsistent project conventions.
4. Separate concrete defects from optional refinements.
5. In report-only mode, return findings without changing files.
6. In edit-authorized mode, apply only eligible refinements, then run focused
   verification.

## Output

For each reviewed file, provide:

1. A concise finding or change summary.
2. Why it matters.
3. The specific location or code shape involved.
4. A concrete recommendation or applied refinement.
5. Any broader suggestion that is intentionally outside the current scope.

The review is successful when it improves clarity and maintainability without changing behavior,
stays within the bounded target, and respects the host's authorization model.
