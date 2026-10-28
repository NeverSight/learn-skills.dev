---
name: django-ninja
description: |
  Django Ninja API endpoint patterns including routers, authentication tiers, typed
  requests, and Pydantic input/output models.
  Use when writing or reviewing Django Ninja API endpoints, routers, or auth
  configuration. Also use when creating new API modules or adding endpoints.
  Do NOT use for: Django views that return HTML (use django skill), FastAPI, DRF
  (Django REST Framework), or general Django patterns.
metadata:
  imankulov.skills-sh-group: Python
  imankulov.skills-sh-order: "30"
  imankulov.claude-display-name: Django Ninja
  imankulov.claude-category: development
  imankulov.claude-keywords: "django,ninja,agent-skills"
---

# Django Ninja API Endpoints

Opinionated conventions for building APIs with Django Ninja.

## Structure

- Place all endpoints in `api.py` files
- Create a router per module: `router = Router(tags=["module_name"])`
- Keep endpoints as thin wrappers that call service functions for all business logic

### One API instance

Construct `NinjaAPI` exactly once, in the project's root `urls.py`. Ninja refuses a second
instance sharing the same version, so tests and scripts import the existing one
(`from myproject.urls import api`) instead of building their own.

### Routers carry no prefix

A `Router` gets `tags=[...]` and nothing else. The mount prefix is set where the router is
attached in `urls.py`, derived from the app label. Putting a prefix on the router too
means the path is spelled in two places and they drift.

### Paths and signatures

- Every handler takes `request: HttpRequest` (or the tier-specific request type) as its
  first parameter; the body model is a separate parameter after it.
- A route on the collection itself uses the empty path — `@router.get("")`, not
  `@router.get("/")`. Without `CommonMiddleware` there's no `APPEND_SLASH` redirect, so a
  request to `/api/reports` has to match exactly.
- Never return a bare tuple. Ninja reads a 2-tuple as `(status, body)`, so a service
  returning `tuple[Model, ...]` has to be wrapped in `list(...)` under
  `response=list[Model]`.

### Naming Convention

Suffix API endpoint functions with `_api` so the service function they wrap keeps
the base name, and import the service directly without an `as` alias:

```python
# services.py — the real logic, no suffix
def create_user(*, email: str, name: str) -> User:
    ...

# api.py — thin wrapper, suffixed with _api
@router.post("/v1/users", auth=[require_user], response=UserResponse)
def create_user_api(request: AuthenticatedHttpRequest, input_data: CreateUserInput) -> UserResponse:
    user = create_user(email=input_data.email, name=input_data.name)
    return UserResponse.from_model(user)
```

## Authentication

Set authentication API-wide on the `NinjaAPI` instance so a new router is protected
without doing anything, and let the rare anonymous route opt out with `auth=None` — a
login endpoint, say. Defaulting to open and remembering to lock each route down is the
wrong way round.

Session auth enforces CSRF on unsafe methods. `CsrfViewMiddleware` never rejects these
calls, since API views are `csrf_exempt` at the Django level — it only sets the cookie —
so the client has to send the token back in the `X-CSRFToken` header.

Use two auth tiers, and match the request type annotation to the tier:

- **`require_user`** with `AuthenticatedHttpRequest`: endpoints that require authentication
- **`session_auth`** with `AnyUserHttpRequest`: endpoints serving both anonymous and authenticated users

Access the user via `request.auth`, not `request.user`. In mixed-auth endpoints, branch
on `request.auth.is_authenticated`:

```python
@router.get("/v1/features", auth=[session_auth], response=Features)
def get_features(request: AnyUserHttpRequest) -> Features:
    if not request.auth.is_authenticated:
        return get_anonymous_features()
    return get_user_features(user_id=request.auth.id)
```

## Input/Output Models

- Use Pydantic models for input parameters, suffixed with `Input`
- Return typed Pydantic response models, never dicts
- Keep models in `types.py` unless used only in one endpoint

## Errors

Raise `ninja.errors.HttpError` for client mistakes — a bad ID, a missing resource. For the
exceptions services raise on purpose, register one handler on the API instance that maps
the app's exception hierarchy to status codes. Handlers then stay free of `try`/`except`
wrappers, and every endpoint reports the same failure the same way.

## Interactive docs

The generated docs live at `/api/docs` and render through a template, so `TEMPLATES` needs
at least a minimal entry in settings even for a project that serves no HTML.
