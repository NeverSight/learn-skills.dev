---
name: django-api-debugger
description: Debug Django REST Framework API issues including serializers, viewsets, permissions, pagination, filtering, and response formatting. Use when troubleshooting API endpoints, serialization errors, permission denials, or unexpected response data.
allowed-tools: Read, Grep, Glob
---

# Django API Debugger

Analyzes and debugs Django REST Framework API issues in this project.

## Project Context

- Backend: Django 5.x with Django REST Framework
- API base path: `/api/v1/`
- Key apps: `core/projects`, `core/users`, `core/tools`
- Serializers located in: `*/serializers.py`
- Views located in: `*/views.py`
- URL routing: `*/urls.py`

## When to Use

- "API returning wrong data"
- "Serializer not including field"
- "Permission denied on endpoint"
- "Pagination not working"
- "Filter not applying"
- "API response format incorrect"

## Debugging Approach

### 1. Identify the Endpoint
- Check `urls.py` for URL pattern
- Find the corresponding view/viewset

### 2. Check the Serializer
- Verify fields are included
- Check `read_only` and `write_only` settings
- Look for custom `to_representation` or `to_internal_value`
- Verify nested serializers

### 3. Check the View
- Verify `queryset` and `get_queryset()`
- Check `permission_classes`
- Look for custom `get_serializer_context()`
- Verify pagination settings

### 4. Common Issues

**Missing fields in response:**
- Field not in serializer's `fields`
- Field is `write_only=True`
- Property not defined on model

**Permission errors:**
- Missing or incorrect `permission_classes`
- User not authenticated
- Object-level permissions failing

**Pagination issues:**
- Check `DEFAULT_PAGINATION_CLASS` in settings
- Verify `page_size` parameter
- Check for `next`/`previous` URLs in response

## Key Files to Check

```
core/
├── projects/
│   ├── serializers.py  # Project serializers
│   ├── views.py        # Project viewsets
│   └── urls.py         # Project URL patterns
├── users/
│   ├── serializers.py  # User serializers
│   └── views.py        # User viewsets
└── tools/
    ├── serializers.py  # Tool serializers
    └── views.py        # Tool viewsets
```

## Testing Tips

```bash
# Test endpoint directly
docker compose exec web python manage.py shell
>>> from core.projects.models import Project
>>> Project.objects.first().__dict__

# Check serializer output
>>> from core.projects.serializers import ProjectSerializer
>>> ProjectSerializer(Project.objects.first()).data
```
