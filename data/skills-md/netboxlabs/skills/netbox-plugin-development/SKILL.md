---
name: netbox-plugin-development
description: >
  How to build NetBox plugins — models, views, REST/GraphQL APIs, forms, tables,
  filtersets, navigation, template extensions, testing, and packaging. Use this
  skill when creating, modifying, or debugging a NetBox plugin targeting v4.5+.
license: Apache-2.0
---

# NetBox Plugin Development

> **Your knowledge of NetBox plugin APIs may be outdated.** Base classes, mixins, template tags, and registration patterns change between NetBox releases. Prefer retrieval over pre-trained knowledge.

## Retrieval Sources

| Source | URL / Method | Use for |
|--------|-------------|---------|
| Plugin development docs | `https://netboxlabs.com/docs/netbox/plugins/development/` | Plugin framework reference |
| NetBox repo | `https://github.com/netbox-community/netbox` | Base classes, mixins, current APIs |
| NetBox release notes | `https://netboxlabs.com/docs/netbox/release-notes/` | Breaking changes, new plugin features |
| Example plugins | `https://github.com/netbox-community` | Community plugin patterns |

Build plugins that extend NetBox with custom models, views, APIs, and UI elements.
Target: **NetBox 4.5–4.7** / **Python 3.12–3.14**. Note the Django split: **NetBox 4.5 runs on Django 5.2, NetBox 4.6 on Django 6.0, NetBox 4.7 on Django 6.1** — code, migrations, and third-party deps must be Django 6.0-compatible when targeting 4.6+, and 6.1-compatible when targeting 4.7+.

> For REST API client patterns (pagination, filtering, tokens), see
> [netbox-api-integration](../netbox-api-integration/SKILL.md).

---

## Quick Reference — Key Imports

```python
# Models
from netbox.models import NetBoxModel          # base for all plugin models
from netbox.models import PrimaryModel         # adds description + comments (4.5+)
from netbox.models import OrganizationalModel  # name/slug/description/comments (4.5+)

# Views
from netbox.views.generic import (ObjectListView, ObjectView, ObjectEditView,
    ObjectDeleteView, BulkImportView, BulkEditView, BulkDeleteView)
from utilities.views import register_model_view, ViewTab

# Forms
from netbox.forms import NetBoxModelForm, NetBoxModelBulkEditForm
from netbox.forms import NetBoxModelFilterSetForm, NetBoxModelImportForm

# Tables
from netbox.tables import NetBoxTable, columns

# FilterSets
from netbox.filtersets import NetBoxModelFilterSet
from utilities.filters import register_filterset  # 4.5+: UI lookup modifiers

# REST API
from netbox.api.serializers import NetBoxModelSerializer
from netbox.api.viewsets import NetBoxModelViewSet
from netbox.api.routers import NetBoxRouter

# Navigation
from netbox.plugins import PluginMenu, PluginMenuItem, PluginMenuButton
```

---

## 1. Plugin Structure & Setup

### Package Layout

```
netbox_myplugin/
├── __init__.py              # PluginConfig + config variable
├── version.py               # __version__ = '1.0.0'
├── models.py                # Django models (NetBoxModel subclasses)
├── views.py                 # UI views
├── tables.py                # django-tables2 table classes
├── forms.py                 # Model, bulk edit, filter, import forms
├── filtersets.py            # FilterSet classes
├── navigation.py            # Menu items (auto-discovered)
├── search.py                # Search indexes (auto-discovered)
├── graphql/                 # Strawberry GraphQL schema
│   ├── schema.py            # Query class (auto-discovered)
│   ├── types.py
│   └── filters.py
├── api/
│   ├── urls.py              # NetBoxRouter config
│   ├── views.py             # API ViewSets
│   └── serializers.py
├── templates/netbox_myplugin/
│   └── myplugin_model.html  # Detail view templates
├── template_content.py      # Template extensions (auto-discovered)
├── event_rules.py           # EventRuleAction subclasses (4.7+, auto-discovered)
├── jinja_env.py             # Config-template Jinja filters (4.7+, auto-discovered)
├── graphql_extensions.py    # Fields/filters on core GraphQL types (4.7+, auto-discovered)
└── tests/
    ├── test_models.py
    ├── test_views.py
    ├── test_api.py
    └── test_forms.py
```

### PluginConfig (`__init__.py`)

```python
from netbox.plugins import PluginConfig
from .version import __version__

class MyPluginConfig(PluginConfig):
    name = 'netbox_myplugin'
    verbose_name = 'My Plugin'
    description = 'Adds custom functionality to NetBox'
    version = __version__
    author = 'Your Name'
    author_email = 'you@example.com'
    base_url = 'myplugin'               # URL prefix under /plugins/
    min_version = '4.5.0'
    max_version = '4.7.99'              # span 4.5–4.7; use .99 to allow patch releases
    default_settings = {'feature_x': True}
    required_settings = []

    def ready(self):
        super().ready()
        from . import signals  # deferred imports to avoid circular deps

config = MyPluginConfig  # MUST be module-level variable named 'config'
```

**Auto-discovery:** NetBox automatically discovers `navigation.menu`, `navigation.menu_items`,
`template_content.template_extensions`, `search.indexes`, `graphql.schema`, and *(4.7+)*
`event_rules.event_rule_actions`, `jinja_env.filters`, `graphql_extensions.type_extensions`/`.filter_extensions`.

---

## 2. Models

Subclass `NetBoxModel` for full feature support (tags, custom fields, change logging,
bookmarks, journaling, export templates, event rules, notifications).

```python
from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel

class AccessList(NetBoxModel):
    name = models.CharField(max_length=100)
    device = models.ForeignKey(
        to='dcim.Device',
        on_delete=models.CASCADE,
        related_name='%(app_label)s_access_lists',  # avoid FK collisions
    )
    type = models.CharField(max_length=50, choices=AccessListTypeChoices)

    class Meta:
        ordering = ['name']
        unique_together = ('device', 'name')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_myplugin:accesslist', args=[self.pk])
```

> **4.5+**: `PrimaryModel` (description + comments) and `OrganizationalModel`
> (name/slug/description/comments, enforces unique name+slug) are now part of the
> plugins API. Use them when your model fits those patterns.

**Key gotchas:**
- Use `%(app_label)s_` prefix on `related_name` to avoid FK collisions across plugins
- Reference core models as strings (`'dcim.Device'`) in ForeignKey fields
- Always define `get_absolute_url()` — follows `plugins:<plugin_name>:<model_name>` pattern
- Permissions format: `netbox_myplugin.view_accesslist`, `.add_accesslist`, etc.

See [references/model-patterns.md](references/model-patterns.md) for base class hierarchy,
mixins, choices patterns, and migration tips.

---

## 3. Views

Use the `@register_model_view` decorator for standard CRUD views:

```python
from netbox.views.generic import (
    ObjectListView, ObjectView, ObjectEditView, ObjectDeleteView,
    BulkImportView, BulkEditView, BulkDeleteView
)
from utilities.views import register_model_view, ViewTab
from .models import AccessList
from .tables import AccessListTable
from .forms import AccessListForm, AccessListFilterForm, AccessListBulkEditForm
from .filtersets import AccessListFilterSet

@register_model_view(AccessList, 'list')
class AccessListListView(ObjectListView):
    queryset = AccessList.objects.all()
    table = AccessListTable
    filterset = AccessListFilterSet
    filterset_form = AccessListFilterForm

@register_model_view(AccessList)
class AccessListView(ObjectView):
    queryset = AccessList.objects.all()

@register_model_view(AccessList, 'edit')
class AccessListEditView(ObjectEditView):
    queryset = AccessList.objects.all()
    form = AccessListForm

@register_model_view(AccessList, 'delete')
class AccessListDeleteView(ObjectDeleteView):
    queryset = AccessList.objects.all()
```

### URL Configuration (`urls.py`)

```python
from netbox.views.generic import get_model_urls
from . import models

urlpatterns = get_model_urls('netbox_myplugin', models)
```

See [references/views-and-api.md](references/views-and-api.md) for all view classes, URL patterns,
`ViewTab` (adding tabs to core object views), declarative layouts + breadcrumbs *(4.7)*, GraphQL
core-type extensions *(4.7)*, and custom event rule actions *(4.7)*.

---

## 4. REST API

### Serializer

```python
from netbox.api.serializers import NetBoxModelSerializer
from ..models import AccessList

class AccessListSerializer(NetBoxModelSerializer):
    class Meta:
        model = AccessList
        fields = ('id', 'url', 'display', 'name', 'device', 'type',
                  'tags', 'custom_fields', 'created', 'last_updated')
        brief_fields = ('id', 'url', 'display', 'name')  # for nested representation
```

### ViewSet

```python
from netbox.api.viewsets import NetBoxModelViewSet
from ..models import AccessList
from ..filtersets import AccessListFilterSet
from .serializers import AccessListSerializer

class AccessListViewSet(NetBoxModelViewSet):
    queryset = AccessList.objects.all()
    serializer_class = AccessListSerializer
    filterset_class = AccessListFilterSet
```

### Router (`api/urls.py`)

```python
from netbox.api.routers import NetBoxRouter
from . import views

router = NetBoxRouter()
router.register('access-lists', views.AccessListViewSet)
urlpatterns = router.urls
```

**API URL naming:** `plugins-api:netbox_myplugin-api:accesslist-detail`
(this matters for `HyperlinkedIdentityField` on serializers).

See [references/views-and-api.md](references/views-and-api.md) for GraphQL, nested
serializers, and advanced API patterns.

---

## 5. Forms, Tables & FilterSets

### Model Form

```python
from netbox.forms import NetBoxModelForm
from utilities.forms.fields import DynamicModelChoiceField
from utilities.forms.rendering import FieldSet
from dcim.models import Device
from .models import AccessList

class AccessListForm(NetBoxModelForm):
    device = DynamicModelChoiceField(queryset=Device.objects.all())

    fieldsets = (
        FieldSet('name', 'device', 'type'),
        FieldSet('tags', name='Tags'),
    )

    class Meta:
        model = AccessList
        fields = ('name', 'device', 'type', 'tags')
```

### Table

```python
import django_tables2 as tables
from netbox.tables import NetBoxTable, columns

class AccessListTable(NetBoxTable):
    name = tables.Column(linkify=True)    # no LinkColumn in netbox.tables.columns
    device = tables.Column(linkify=True)
    type = columns.ChoiceFieldColumn()
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        model = AccessList
        fields = ('pk', 'name', 'device', 'type', 'tags')
        default_columns = ('name', 'device', 'type')
```

### FilterSet

```python
from netbox.filtersets import NetBoxModelFilterSet
from utilities.filters import register_filterset
from .models import AccessList

@register_filterset  # 4.5+: enables lookup modifiers in UI
class AccessListFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = AccessList
        fields = ('name', 'device', 'type')

    def search(self, queryset, name, value):
        """Required for ?q= parameter to work."""
        return queryset.filter(name__icontains=value)
```

> **4.5+**: The `@register_filterset` decorator is required for lookup modifiers
> (e.g., `name__ic`, `device_id__n`) to appear in the UI filter forms.

See [references/forms-tables-filtersets.md](references/forms-tables-filtersets.md) for
bulk edit/import/filter forms, `GenericObjectChoiceField` *(4.7)*, and django-tables2 v3 notes *(4.7)*.

---

## 6. Navigation

```python
# navigation.py — auto-discovered
from netbox.plugins import PluginMenu, PluginMenuItem, PluginMenuButton

menu = PluginMenu(
    label='My Plugin',
    icon_class='mdi mdi-shield-lock',
    groups=(
        ('Access Control', (
            PluginMenuItem(
                link='plugins:netbox_myplugin:accesslist_list',
                link_text='Access Lists',
                permissions=['netbox_myplugin.view_accesslist'],
                buttons=(
                    PluginMenuButton(
                        link='plugins:netbox_myplugin:accesslist_add',
                        title='Add',
                        icon_class='mdi mdi-plus-thick',
                        permissions=['netbox_myplugin.add_accesslist'],
                    ),
                ),
            ),
        )),
    ),
)
```

---

## 7. Template Extensions

Two approaches — use **ViewTab** (modern) for tab-based extensions, or
**PluginTemplateExtension** for injecting content into existing pages:

```python
# template_content.py
from netbox.plugins import PluginTemplateExtension

class DeviceAccessInfo(PluginTemplateExtension):
    models = ['dcim.device']  # list of strings, not model classes; None = global

    def right_page(self):
        return self.render('netbox_myplugin/inc/device_access.html', extra_context={
            'access_lists': self.context['object'].accesslists.all()
        })

template_extensions = [DeviceAccessInfo]
```

Available methods: `head()`, `navbar()`, `list_buttons()`, `buttons()`, `alerts()`,
`left_page()`, `right_page()`, `full_width_page()`.

---

## 8. Testing

```python
from django.test import TestCase
from utilities.testing import APITestCase
from .models import AccessList

class AccessListAPITest(APITestCase):
    model = AccessList

    def setUp(self):
        self.device = Device.objects.create(name='test-device', ...)
        self.access_list = AccessList.objects.create(
            name='test-acl', device=self.device, type='standard'
        )

    def test_list(self):
        url = reverse('plugins-api:netbox_myplugin-api:accesslist-list')
        response = self.client.get(url, **self.header)
        self.assertEqual(response.status_code, 200)
```

See [references/testing-guide.md](references/testing-guide.md) for fixtures, view tests,
form tests, and CI setup.

---

## 9. Packaging

Use `pyproject.toml` (modern) or `setup.py`:

```toml
[project]
name = "netbox-myplugin"
version = "1.0.0"
dependencies = []   # never list "netbox" here — see note below

[project.entry-points."netbox.plugins"]
netbox_myplugin = "netbox_myplugin:config"
```

> **Note:** The entry point key must match `PluginConfig.name` and point to the
> module-level `config` variable. Never list `netbox` in `dependencies`: NetBox is published
> to PyPI since 4.7, so pip would install a second NetBox into the venv next to the real one —
> declare compatibility with `min_version`/`max_version` on `PluginConfig` instead.

See [references/packaging.md](references/packaging.md) for versioning strategy,
publishing to PyPI, and version compatibility matrix.

---

## 10. Common Gotchas

1. **`config` must be module-level** in `__init__.py` — not inside a function
2. **FK `related_name` collisions** — prefix with `%(app_label)s_` when multiple plugins target the same core model
3. **URL namespace** — views: `plugins:<plugin>:<view>`, API: `plugins-api:<plugin>-api:<basename>-detail`
4. **Missing `search()` on filterset** — `?q=` won't work without it
5. **`models` on TemplateExtension** — must be list of `'app.model'` strings, not classes; `None` = global
6. **Heavy imports in `__init__.py`** — use `ready()` for signals and deferred imports (fixed in 4.5.2 but still best practice)
7. **`max_version` too strict** — use `'4.7.99'` (or your top minor's `.99`) not `'4.5.0'` to allow patches
8. **GraphQL uses Strawberry** since 4.0 — Graphene patterns will not work
9. **`@register_filterset`** (4.5+) — without it, lookup modifiers won't appear in UI
10. **Permissions** — format is `<plugin_name>.view_<model>`, `<plugin_name>.add_<model>`, etc. **Custom actions (4.6.0+):** declare extra actions via your model's `Meta.permissions`; NetBox auto-registers them as actions selectable in the ObjectPermission form (preferred over ad-hoc permission checks).

---

## Version Notes

### NetBox 4.7 (2026-09-02)
- **PostgreSQL 15+** (system check fails on 14, including under `manage.py test`) and **Django 6.1**; NetBox is on PyPI (never depend on `netbox` in `pyproject.toml`); recommend **≥4.7.2** — 4.7.0/4.7.1 recorded plaintext API tokens created via background bulk requests in job results
- **Removed:** `DEFAULT_ACTION_PERMISSIONS`, legacy view actions, `registry['models']` (use `ObjectType.objects.public()`) and `registry['denormalized_fields']`, `OptionalLimitOffsetPagination` (→ `NetBoxPagination`), `ExpandableIPAddressField`/`expand_ipaddress_pattern()` (→ `*IPNetwork*`), `populate_custom_field_defaults()`, `OwnerMixin`'s reverse relation (`site_set`), Django `EMAIL_*` settings, and NetBox's `querystring` tag (use Django's, without `request`: `{% querystring page=1 %}`) — full checklist in [netbox-4.7-migration](references/netbox-4.7-migration.md)
- **Changed:** `custom_fields`/`get_for_model()` return lists; django-tables2 v3 (`querystring_replace`, no `RelatedLinkColumn`); filterset test mixins renamed `*TestMixin`; search indexing deferred to on-commit (tests: `captureOnCommitCallbacks(execute=True)`); plugin viewsets inherit `?background=true` + per-object bulk errors
- **Core trees moved from MPTT to ltree** (Region, Location, Platform, …): `level` can't be filtered/ordered on; `get_root()`/`get_family()`/`is_leaf_node()`/`move_to()`/`insert_at()` are gone. `NestedGroupModel` is deprecated → `NestedLtreeGroupModel`; plugins that installed ltree triggers on 4.7.0 need a `ReinstallLtreeTriggers` migration — see [model-patterns](references/model-patterns.md)
- **New plugin extension points** (all need `min_version='4.7.0'`): core GraphQL type/filter extensions (`graphql_extensions.py`), custom event rule actions (`EventRuleAction`), Jinja filters + config-template context (`jinja_env.py`, `get_jinja_context()`), breadcrumbs on layouts, `GenericObjectChoiceField`, choice descriptions

### NetBox 4.6 (2026)
- **Django 6.0** (was 5.2 in 4.5) — ensure code, migrations, and dependencies are Django 6.0-compatible; set `min_version='4.6.0'` for any plugin using 4.6-only APIs below
- **Declarative view layouts / reusable UI components** — `from netbox.ui import layout` (`Layout`/`Row`/`Column`); the modern alternative to hand-written detail templates (requires NetBox ≥4.6.0)
- **Custom model actions / permissions via `Meta.permissions`** — declare them on your model's `Meta`; NetBox auto-registers them as actions selectable in the ObjectPermission form
- **Custom serializer resolvers** for `get_serializer_for_model()` (4.6.2) — register a resolver to control serializer lookup
- **Security:** ExportTemplate/ConfigTemplate `environment_params` RCE (CVE-2026-29514) fixed in 4.6.1 — the allowlist blocks `extensions`/`finalize`/`loader`/`bytecode_cache`
- **Deprecations to avoid:** `DEFAULT_ACTION_PERMISSIONS`, legacy view actions, the internal registry `models` key, the custom `querystring` template tag, and `OptionalLimitOffsetPagination`

### NetBox 4.5 (2026-01-06)
- **Python 3.12+ required** (dropped 3.10/3.11); Django 5.2
- `PrimaryModel`, `OrganizationalModel`, `NestedGroupModel` now in plugins API
- `@register_filterset` decorator enables UI lookup modifiers
- `OwnerMixin` available for object ownership
- **Breaking:** GraphQL filter syntax requires lookup modifiers for IDs/enums

### NetBox 4.4 (2025-09-02)
- Background job logging: `self.logger.info()` in job methods
- `ObjectAction` for custom individual/bulk operations on views
- `register_model_feature()` for plugins to register custom model features
- `ArrayColumn` support in tables
