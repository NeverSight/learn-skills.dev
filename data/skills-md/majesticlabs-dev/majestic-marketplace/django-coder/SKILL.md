---
name: django-coder
description: Build Django applications with models, views, forms, templates, REST APIs, and modern Django 5.x patterns.
allowed-tools: Read Write Edit Grep Glob Bash WebSearch
---

# Django Coder

## Core Principles

| Principle | Application |
|-----------|-------------|
| **Convention over Configuration** | Follow Django's standard project layout |
| **DRY** | Use model inheritance, mixins, template inheritance |
| **Fat Models, Thin Views** | Business logic in models/managers, views just orchestrate |
| **Security First** | CSRF, SQL injection protection, XSS prevention built-in |
| **Explicit over Implicit** | Clear URL routing, explicit imports |

## Project Structure

```
project/
├── manage.py
├── config/                  # Project settings
│   ├── __init__.py
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   └── users/              # App per domain
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── forms.py
│       ├── models.py
│       ├── urls.py
│       ├── views.py
│       ├── services.py     # Business logic
│       ├── selectors.py    # Query logic
│       └── tests/
├── templates/
│   ├── base.html
│   └── users/
└── static/
```

## Models

### Model Definition

```python
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Custom user model."""
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True)

    class Meta:
        ordering = ["-date_joined"]

    def __str__(self):
        return self.email

class Post(models.Model):
    """Blog post model."""
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["status", "-created_at"]),
        ]
```

### Custom Managers

```python
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class Post(models.Model):
    # ... fields ...
    objects = models.Manager()
    published = PublishedManager()
```

## Views

### Class-Based Views

```python
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class PostListView(ListView):
    model = Post
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 10
    template_name = "posts/list.html"

class PostDetailView(DetailView):
    model = Post
    slug_field = "slug"
    slug_url_kwarg = "slug"
    template_name = "posts/detail.html"

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content", "status"]
    template_name = "posts/form.html"
    success_url = reverse_lazy("posts:list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
```

### Async Views (Django 4.1+)

```python
from django.http import JsonResponse
from asgiref.sync import sync_to_async

async def async_post_list(request):
    posts = await sync_to_async(list)(Post.published.all()[:10])
    data = [{"title": p.title, "slug": p.slug} for p in posts]
    return JsonResponse({"posts": data})
```

## Django REST Framework

### Serializers

```python
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "slug", "author", "content", "status", "created_at"]
        read_only_fields = ["slug", "created_at"]

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "content", "status"]

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)
```

### ViewSets

```python
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "slug"

    def get_queryset(self):
        if self.action == "list":
            return Post.published.all()
        return Post.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return PostCreateSerializer
        return PostSerializer

    @action(detail=True, methods=["post"])
    def publish(self, request, slug=None):
        post = self.get_object()
        post.status = Post.Status.PUBLISHED
        post.save()
        return Response({"status": "published"})
```

## Services Pattern

```python
# apps/posts/services.py
from django.db import transaction
from .models import Post

class PostService:
    @staticmethod
    @transaction.atomic
    def create_post(*, author, title: str, content: str) -> Post:
        post = Post.objects.create(
            author=author,
            title=title,
            content=content,
            status=Post.Status.DRAFT,
        )
        return post

    @staticmethod
    def publish_post(*, post: Post) -> Post:
        post.status = Post.Status.PUBLISHED
        post.save(update_fields=["status", "updated_at"])
        return post
```

## Quality Checklist

- [ ] Custom User model from project start
- [ ] Apps organized by domain
- [ ] Fat models, thin views
- [ ] Services for complex business logic
- [ ] Proper indexes on queryable fields
- [ ] CSRF protection on forms
- [ ] Login required where needed
- [ ] Proper related_name on ForeignKeys
- [ ] Tests for models, views, and services

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| No custom User model | Always start with AbstractUser |
| Logic in views | Move to services/models |
| N+1 queries | Use select_related/prefetch_related |
| No indexes | Add indexes for filtered/ordered fields |
| Hardcoded URLs | Use reverse() and {% url %} |
