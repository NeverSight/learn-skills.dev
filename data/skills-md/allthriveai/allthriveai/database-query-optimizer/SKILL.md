---
name: database-query-optimizer
description: Analyze and optimize Django ORM queries including N+1 problems, missing indexes, slow queries, and migration issues. Use when troubleshooting slow API responses, database performance, query optimization, or migration errors.
allowed-tools: Read, Grep, Glob, Bash
---

# Database Query Optimizer

Analyzes and optimizes Django ORM queries and database performance.

## Project Context

- Database: PostgreSQL (in Docker)
- ORM: Django ORM
- Key models: Project, User, Tool, Technology, Company
- Search: Weaviate (vector DB) for semantic search

## When to Use

- "API response is slow"
- "N+1 query problem"
- "Database query optimization"
- "Missing index"
- "Migration failing"
- "Slow queryset"

## Common Performance Issues

### N+1 Query Problem

**Symptom:** Many small queries instead of one efficient query

```python
# BAD - N+1 queries (1 + N queries)
projects = Project.objects.all()
for project in projects:
    print(project.user.username)  # Each access = 1 query!

# GOOD - select_related for ForeignKey/OneToOne
projects = Project.objects.select_related('user').all()

# GOOD - prefetch_related for ManyToMany/reverse FK
projects = Project.objects.prefetch_related('tools', 'technologies').all()
```

### Missing select_related/prefetch_related

Check serializers for nested data:

```python
# If serializer includes nested user data:
class ProjectSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Needs select_related!

# View must optimize:
class ProjectViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Project.objects.select_related('user')
```

### Unindexed Filters

```python
# If filtering frequently on a field, add index:
class Project(models.Model):
    slug = models.SlugField(db_index=True)  # Has index
    is_private = models.BooleanField(db_index=True)  # Add index!
```

## Debugging Queries

### 1. Django Debug Toolbar
Already configured - check bottom of page in development.

### 2. Query Logging
```python
# settings.py - enable query logging
LOGGING = {
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
        }
    }
}
```

### 3. Shell Analysis
```python
# Django shell
from django.db import connection, reset_queries
from django.conf import settings
settings.DEBUG = True

reset_queries()
# Run your query
list(Project.objects.all())
print(f"Queries: {len(connection.queries)}")
for q in connection.queries:
    print(q['sql'][:100])
```

### 4. Explain Query
```python
# See query execution plan
print(Project.objects.filter(is_private=False).explain())
```

## Key Optimizations

### select_related (ForeignKey, OneToOne)
```python
# Single JOIN query
Project.objects.select_related('user', 'user__profile')
```

### prefetch_related (ManyToMany, Reverse FK)
```python
# Separate query, joined in Python
Project.objects.prefetch_related('tools', 'likes')
```

### only() / defer() - Load Specific Fields
```python
# Only load needed fields
Project.objects.only('id', 'title', 'slug')

# Exclude heavy fields
Project.objects.defer('description', 'content')
```

### values() / values_list() - Skip Model Instantiation
```python
# Returns dicts, not model instances
Project.objects.values('id', 'title')

# Returns tuples
Project.objects.values_list('id', 'title')
```

### Aggregation at DB Level
```python
from django.db.models import Count, Avg

# Do counting in database, not Python
Project.objects.annotate(like_count=Count('likes'))
```

### Bulk Operations
```python
# BAD - N queries
for project in projects:
    project.views += 1
    project.save()

# GOOD - 1 query
Project.objects.filter(id__in=ids).update(views=F('views') + 1)

# Bulk create
Project.objects.bulk_create([Project(...), Project(...)])
```

## Migration Issues

### Check Migration Status
```bash
docker compose exec web python manage.py showmigrations
```

### Create Missing Migrations
```bash
docker compose exec web python manage.py makemigrations
```

### Fake Problematic Migration
```bash
docker compose exec web python manage.py migrate --fake app_name 0001
```

### Squash Migrations
```bash
docker compose exec web python manage.py squashmigrations app_name 0001 0010
```

## Key Files to Check

```
core/
├── projects/
│   ├── models.py       # Project model, indexes
│   ├── views.py        # QuerySet optimization
│   └── serializers.py  # Nested serializers need optimization
├── users/
│   └── models.py       # User model
└── tools/
    └── models.py       # Tool model

config/
└── settings.py         # DATABASE config, DEBUG
```

## PostgreSQL Commands

```bash
# Connect to database
docker compose exec db psql -U postgres -d allthriveai

# List tables
\dt

# Describe table
\d core_project

# Show indexes
\di

# Analyze slow query
EXPLAIN ANALYZE SELECT * FROM core_project WHERE is_private = false;

# Show running queries
SELECT pid, query, state FROM pg_stat_activity WHERE state != 'idle';
```

## Adding Indexes

```python
# In model
class Project(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['is_private', 'created_at']),
            models.Index(fields=['user', 'is_private']),
        ]

# Or on field
is_private = models.BooleanField(default=False, db_index=True)
```

Then run:
```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```
