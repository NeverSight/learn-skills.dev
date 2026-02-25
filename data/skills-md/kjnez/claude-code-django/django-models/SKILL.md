---
name: django-models
description: Django model design patterns emphasizing fat models/thin views, QuerySet optimization, and domain logic encapsulation. Use when designing models, optimizing queries, implementing business logic, or working with the ORM.
---

# Django Model Patterns

## Core Philosophy: Fat Models, Thin Views

**Business logic belongs in models and managers, not views.** Views orchestrate workflows; models implement domain behavior. This principle creates testable, reusable code that stays maintainable as complexity grows.

**Good**: Model methods handle business rules, state transitions, validation
**Bad**: Views contain if/else logic for domain rules, calculate derived values

## Model Design

### Structure Your Models Around Domain Concepts
- Use `TextChoices`/`IntegerChoices` for status fields and enums
- Add `get_absolute_url()` for canonical object URLs
- Include `__str__()` for readable representations
- Set proper `ordering` in Meta for consistent default sorting
- Add database indexes for frequently filtered/sorted fields
- Use abstract base models for shared fields (timestamps, soft deletes, etc.)

### Field Selection Guidelines
- Use `blank=True, default=""` for optional text fields (avoid null)
- Use `null=True, blank=True` for optional foreign keys
- For unique optional fields, use `null=True` to avoid collision issues
- Leverage `JSONField` for flexible metadata (avoid creating many optional fields)
- Set appropriate `max_length` based on actual data needs

### Encapsulate Business Logic in Model Methods
- State transitions: `post.publish()`, `order.cancel()`
- Permission checks: `post.is_editable_by(user)`
- Complex calculations: `invoice.calculate_total()`
- Use properties for computed read-only values
- Specify `update_fields` when saving partial changes

## QuerySet Patterns: The Power of Composition

**Custom QuerySet classes are your secret weapon.** They make queries reusable, chainable, and testable.

### Pattern: QuerySet as Manager
```
Define a QuerySet subclass with domain-specific filter methods
Attach it to your model: objects = YourQuerySet.as_manager()
Chain methods for composable queries
```

### Benefits
- Reusable query logic across views, tasks, management commands
- Chainable methods enable expressive, readable queries
- Easy to test in isolation
- Encapsulates query complexity away from views

### Common QuerySet Methods
- Filtering by status/state
- Date range queries (recent, upcoming, expired)
- User-scoped queries (owned_by, visible_to)
- Combined lookups (published_and_recent)

## Query Optimization: Avoid N+1 Queries

### The Golden Rules
1. **select_related()**: Use for ForeignKey and OneToOneField (creates SQL JOIN)
2. **prefetch_related()**: Use for ManyToManyField and reverse ForeignKeys (separate query + Python join)
3. **only()**: Load specific fields when you don't need the whole object
4. **defer()**: Exclude heavy fields (TextField, JSONField) you won't use
5. **Prefetch()** object: Customize prefetch with filters and select_related

### Efficient Counting and Existence Checks
- Use `.exists()` instead of `if queryset:` or `if len(queryset):`
- Use `.count()` instead of `len(queryset.all())`
- Both perform database-level operations without loading objects

### Aggregation and Annotation
- `annotate()`: Add computed fields to each object (Count, Sum, Avg, etc.)
- `aggregate()`: Compute values across entire queryset
- Use `F()` expressions for database-level updates (`views=F('views') + 1`)
- Combine annotate with filter for "objects with at least N related items"

## Managers vs QuerySets

**Use QuerySets for chainable query logic.**
**Use Managers for model-level operations that don't return querysets.**

Manager: Think "factory methods" - `User.objects.create_user()`
QuerySet: Think "filters and transformations" - `Post.objects.published().recent()`

Most of the time, you want a custom QuerySet, not a custom Manager.

## Signals: Use Sparingly

Signals create implicit coupling and make code harder to follow. **Prefer explicit method calls.**

### When Signals Make Sense
- Audit logging (track all changes to a model)
- Cache invalidation (clear cache when model changes)
- Decoupling apps (third-party app needs to react to your models)

### When to Avoid Signals
- Business logic that should be in model methods
- Logic tightly coupled to the calling code (just call the function directly)
- Complex workflows (use explicit service layer instead)

**Rule of thumb**: If you control both the trigger and the reaction, don't use a signal.

## Migrations

### Workflow
- Run `makemigrations` after model changes
- Review generated migration files before applying
- Run `migrate` to apply migrations
- Migrations should be reversible when possible

### Data Migrations
Create with `makemigrations --empty app_name`. Use `apps.get_model()` to access models (not direct imports). Write both forward and reverse operations.

**Use data migrations for**: Populating new fields, transforming data, migrating between fields.

## Anti-Patterns to Avoid

### Query Anti-Patterns
- Iterating over objects and accessing relations without `select_related()`/`prefetch_related()`
- Using `if queryset:` instead of `.exists()`
- Using `len()` to count instead of `.count()`
- Loading entire objects when you only need specific fields

### Design Anti-Patterns
- Business logic in views instead of models
- Views performing calculations that belong in model methods
- Overusing signals for synchronous operations
- Creating new models when JSONField would suffice
- Forgetting to add indexes for filtered/sorted fields

## Integration

Works with:
- **pytest-django-patterns**: Factory-based model testing
- **celery-patterns**: Async operations on models (pass IDs, not instances)
- **django-forms**: ModelForm validation and saving
