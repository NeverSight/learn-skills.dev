---
name: litestar-data-services
description: "Auto-activate for SQLAlchemyAsyncRepositoryService, SQLSpecAsyncService, create_filter_dependencies, LimitOffsetFilter, OffsetPagination, filters, or CRUD services. Not for raw drivers."
---

# Litestar Data Services

Use this skill for repositories, service layers, CRUD boundaries, filters, and pagination.

## Code Style Rules

- Match the existing persistence stack before choosing patterns.
- Keep handlers out of query construction and transaction management.
- Use filter dependency objects rather than ad hoc query params.
- Return typed pagination envelopes for collection endpoints.

## Quick Reference

- Service patterns: [services.md](references/services.md)
- Pagination and filters: [pagination.md](references/pagination.md)
- Advanced Alchemy details: [advanced-alchemy](../advanced-alchemy/SKILL.md)
- sqlspec details: [sqlspec](../sqlspec/SKILL.md)

<workflow>

## Workflow

1. Identify the project's data stack.
2. Put persistence operations behind a service boundary.
3. Add filters and pagination through the stack's native pattern.
4. Return DTO-ready data to Controllers.

</workflow>

<guardrails>

## Guardrails

- Do not mix repository stacks in one feature.
- Do not place SQL or ORM session handling in route handlers.
- Do not hand-roll pagination query params.
- Do not return persistence internals when DTOs are required.

</guardrails>

<validation>

## Validation Checkpoint

- [ ] Service methods own data access.
- [ ] Filters and pagination match the selected stack.
- [ ] Controller code stays thin.
- [ ] DTO conversion is explicit or handled by the service stack.

</validation>

<example>

## Example

```python
class UserService(SQLAlchemyAsyncRepositoryService[User]):
    repository_type = UserRepository
```

</example>

## References Index

- [services.md](references/services.md)
- [pagination.md](references/pagination.md)

## Official References

- <https://docs.litestar.dev/> - Litestar documentation
- <https://docs.litestar.dev/latest/reference/> - Litestar API reference

## Shared Styleguide Baseline

- [General](../litestar-styleguide/references/general.md)
- [Python](../litestar-styleguide/references/python.md)
- [Litestar](../litestar-styleguide/references/litestar.md)
