---
name: unfold-admin
description: "Django Unfold admin theme - build, configure, and enhance modern Django admin interfaces with Unfold. Use when working with: (1) Django admin UI customisation or theming, (2) Unfold ModelAdmin, inlines, actions, filters, widgets, or decorators, (3) Admin dashboard components and KPI cards, (4) Sidebar navigation, tabs, or conditional fields, (5) Any mention of 'unfold', 'django-unfold', or 'unfold admin'. Covers the full Unfold feature set: site configuration, actions system, display decorators, filter types, widget overrides, inline variants, dashboard components, datasets, sections, theming, and third-party integrations."
---

# Django Unfold Admin

Modern Django admin theme with Tailwind CSS, HTMX, and Alpine.js. Replaces Django's default admin with a polished, feature-rich interface.

## Quick Start

### Installation

```python
# settings.py - unfold MUST be before django.contrib.admin
INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",          # advanced filters
    "unfold.contrib.forms",            # array/wysiwyg widgets
    "unfold.contrib.inlines",          # nonrelated inlines
    "unfold.contrib.import_export",    # styled import/export
    "unfold.contrib.guardian",         # django-guardian integration
    "unfold.contrib.simple_history",   # django-simple-history integration
    "unfold.contrib.constance",        # django-constance integration
    "unfold.contrib.location_field",   # django-location-field integration
    # ...
    "django.contrib.admin",
]
```

### Minimal Admin

```python
from unfold.admin import ModelAdmin

@admin.register(MyModel)
class MyModelAdmin(ModelAdmin):
    pass  # inherits Unfold styling
```

### Site Configuration

Replace the default `AdminSite` or configure via `UNFOLD` dict in settings. See [references/configuration.md](references/configuration.md) for the complete settings reference.

```python
UNFOLD = {
    "SITE_TITLE": "My Admin",
    "SITE_HEADER": "My Admin",
    "SITE_SYMBOL": "dashboard",  # Material Symbols icon name
    "SIDEBAR": {
        "show_search": True,
        "navigation": [
            {
                "title": _("Navigation"),
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
        ],
    },
}
```

## Core Workflow

When building Unfold admin interfaces, follow this sequence:

1. **Configure site** - UNFOLD settings dict (branding, sidebar, theme)
2. **Register models** - Extend `unfold.admin.ModelAdmin`
3. **Enhance display** - `@display` decorator for list columns
4. **Add actions** - `@action` decorator for row/list/detail/submit actions
5. **Configure filters** - Replace default filters with Unfold filter classes
6. **Override widgets** - Apply Unfold widgets via `formfield_overrides`
7. **Set up inlines** - Use Unfold's inline classes with tabs, pagination, sorting
8. **Build dashboard** - `@register_component` + `BaseComponent` for KPI cards

## ModelAdmin Attributes

Unfold extends Django's `ModelAdmin` with these additional attributes:

| Attribute | Type | Purpose |
|-----------|------|---------|
| `list_fullwidth` | bool | Full-width changelist (no sidebar) |
| `list_filter_submit` | bool | Add submit button to filters |
| `list_filter_sheet` | bool | Filters in sliding sheet panel |
| `compressed_fields` | bool | Compact field spacing in forms |
| `warn_unsaved_form` | bool | Warn before leaving unsaved form |
| `ordering_field` | str | Field name for drag-to-reorder |
| `hide_ordering_field` | bool | Hide the ordering field column |
| `list_horizontal_scrollbar_top` | bool | Scrollbar at top of list |
| `list_disable_select_all` | bool | Disable "select all" checkbox |
| `change_form_show_cancel_button` | bool | Show cancel button on form |
| `actions_list` | list | Global changelist actions |
| `actions_row` | list | Per-row actions in changelist |
| `actions_detail` | list | Actions on change form |
| `actions_submit_line` | list | Actions in form submit area |
| `actions_list_hide_default` | bool | Hide default list actions |
| `actions_detail_hide_default` | bool | Hide default detail actions |
| `conditional_fields` | dict | JS expressions for field visibility |
| `change_form_datasets` | list | BaseDataset subclasses for change form |
| `list_sections` | list | TableSection/TemplateSection for list |
| `list_sections_classes` | str | CSS grid classes for sections |
| `readonly_preprocess_fields` | dict | Transform readonly field content |
| `add_fieldsets` | list | Separate fieldsets for add form (like UserAdmin) |

### Template Injection Points

Insert custom HTML before/after changelist or change form:

```python
class MyAdmin(ModelAdmin):
    # Changelist
    list_before_template = "myapp/list_before.html"
    list_after_template = "myapp/list_after.html"
    # Change form (inside <form> tag)
    change_form_before_template = "myapp/form_before.html"
    change_form_after_template = "myapp/form_after.html"
    # Change form (outside <form> tag)
    change_form_outer_before_template = "myapp/outer_before.html"
    change_form_outer_after_template = "myapp/outer_after.html"
```

### Conditional Fields

Show/hide fields based on other field values (Alpine.js expressions):

```python
class MyAdmin(ModelAdmin):
    conditional_fields = {
        "premium_features": "plan == 'PRO'",
        "discount_amount": "has_discount == true",
    }
```

## Actions System

Four action types, each with different signatures. See [references/actions-filters.md](references/actions-filters.md) for complete reference.

```python
from unfold.decorators import action
from unfold.enums import ActionVariant

# List action (no object context)
@action(description=_("Rebuild Index"), icon="sync", variant=ActionVariant.PRIMARY)
def rebuild_index(self, request):
    # process...
    return redirect(request.headers["referer"])

# Row action (receives object_id)
@action(description=_("Approve"), url_path="approve")
def approve_row(self, request, object_id):
    obj = self.model.objects.get(pk=object_id)
    return redirect(request.headers["referer"])

# Detail action (receives object_id, shown on change form)
@action(description=_("Send Email"), permissions=["send_email"])
def send_email(self, request, object_id):
    return redirect(reverse_lazy("admin:myapp_mymodel_change", args=[object_id]))

# Submit line action (receives obj instance, runs on save)
@action(description=_("Save & Publish"))
def save_and_publish(self, request, obj):
    obj.published = True
```

### Action Groups (Dropdown Menus)

```python
actions_list = [
    "primary_action",
    {
        "title": _("More"),
        "variant": ActionVariant.PRIMARY,
        "items": ["secondary_action", "tertiary_action"],
    },
]
```

### Permissions

```python
@action(permissions=["can_export", "auth.view_user"])
def export_data(self, request):
    pass

def has_can_export_permission(self, request):
    return request.user.is_superuser
```

## Display Decorator

Enhance list_display columns. See [references/actions-filters.md](references/actions-filters.md).

```python
from unfold.decorators import display

# Colored status labels
@display(description=_("Status"), ordering="status", label={
    "active": "success",    # green
    "pending": "info",      # blue
    "warning": "warning",   # orange
    "inactive": "danger",   # red
})
def show_status(self, obj):
    return obj.status

# Rich header with avatar
@display(description=_("User"), header=True)
def show_header(self, obj):
    return [
        obj.full_name,           # primary text
        obj.email,               # secondary text
        obj.initials,            # badge text
        {"path": obj.avatar.url, "width": 24, "height": 24, "borderless": True},
    ]

# Interactive dropdown
@display(description=_("Teams"), dropdown=True)
def show_teams(self, obj):
    return {
        "title": f"{obj.teams.count()} teams",
        "items": [{"title": t.name, "link": t.get_admin_url()} for t in obj.teams.all()],
        "striped": True,
        "max_height": 200,
    }

# Boolean checkmark
@display(description=_("Active"), boolean=True)
def is_active(self, obj):
    return obj.is_active
```

## Filters

Unfold provides advanced filter classes. See [references/actions-filters.md](references/actions-filters.md).

```python
from unfold.contrib.filters.admin import (
    TextFilter, RangeNumericFilter, RangeDateFilter, RangeDateTimeFilter,
    SingleNumericFilter, SliderNumericFilter, RelatedDropdownFilter,
    RelatedCheckboxFilter, ChoicesCheckboxFilter, AllValuesCheckboxFilter,
    BooleanRadioFilter, CheckboxFilter, AutocompleteSelectMultipleFilter,
)

class MyAdmin(ModelAdmin):
    list_filter_submit = True  # required for input-based filters
    list_filter = [
        ("salary", RangeNumericFilter),
        ("status", ChoicesCheckboxFilter),
        ("created_at", RangeDateFilter),
        ("category", RelatedDropdownFilter),
        ("is_active", BooleanRadioFilter),
    ]
```

### Custom Text Filter

```python
class NameFilter(TextFilter):
    title = _("Name")
    parameter_name = "name"

    def queryset(self, request, queryset):
        if self.value() in EMPTY_VALUES:
            return queryset
        return queryset.filter(name__icontains=self.value())
```

## Widgets

Override form widgets for Unfold styling. See [references/widgets-inlines.md](references/widgets-inlines.md).

```python
from unfold.widgets import (
    UnfoldAdminTextInputWidget, UnfoldAdminSelectWidget, UnfoldAdminSelect2Widget,
    UnfoldBooleanSwitchWidget, UnfoldAdminColorInputWidget,
    UnfoldAdminSplitDateTimeWidget, UnfoldAdminImageFieldWidget,
)
from unfold.contrib.forms.widgets import WysiwygWidget, ArrayWidget

class MyAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": WysiwygWidget},
        models.ImageField: {"widget": UnfoldAdminImageFieldWidget},
    }
```

### Text Input with Icons

```python
widget = UnfoldAdminTextInputWidget(attrs={
    "prefix_icon": "search",
    "suffix_icon": "euro",
})
```

## Inlines

Unfold inlines support tabs, pagination, sorting, and nonrelated models. See [references/widgets-inlines.md](references/widgets-inlines.md).

```python
from unfold.admin import TabularInline, StackedInline
from unfold.contrib.inlines.admin import NonrelatedStackedInline

class OrderItemInline(TabularInline):
    model = OrderItem
    tab = True          # show as tab
    per_page = 10       # paginated
    ordering_field = "weight"  # drag-to-reorder
    hide_title = True
    collapsible = True
```

## Fieldset Tabs

Group fieldsets into tabs using `"classes": ["tab"]`:

```python
fieldsets = [
    (None, {"fields": ["name", "email"]}),  # always visible
    (_("Profile"), {"classes": ["tab"], "fields": ["bio", "avatar"]}),
    (_("Settings"), {"classes": ["tab"], "fields": ["theme", "notifications"]}),
]
```

## Dashboard Components

Build KPI cards and custom dashboard widgets. See [references/dashboard.md](references/dashboard.md).

```python
from unfold.components import BaseComponent, register_component
from django.template.loader import render_to_string

@register_component
class ActiveUsersComponent(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["children"] = render_to_string("myapp/kpi_card.html", {
            "total": User.objects.filter(is_active=True).count(),
            "label": "Active Users",
        })
        return context
```

Configure in settings:

```python
UNFOLD = {
    "DASHBOARD_CALLBACK": "myapp.views.dashboard_callback",
}
```

## Sections (Changelist Panels)

Embed related data panels in changelist views:

```python
from unfold.sections import TableSection, TemplateSection

class RecentOrdersSection(TableSection):
    related_name = "order_set"
    fields = ["id", "total", "status"]
    height = 380

class ChartSection(TemplateSection):
    template_name = "myapp/chart.html"

class MyAdmin(ModelAdmin):
    list_sections = [RecentOrdersSection, ChartSection]
    list_sections_classes = "lg:grid-cols-2"
```

## Datasets (Change Form Panels)

Embed model listings within change forms:

```python
from unfold.datasets import BaseDataset

class RelatedItemsDatasetAdmin(ModelAdmin):
    list_display = ["name", "status"]
    search_fields = ["name"]

class RelatedItemsDataset(BaseDataset):
    model = RelatedItem
    model_admin = RelatedItemsDatasetAdmin
    tab = True  # show as tab

class MyAdmin(ModelAdmin):
    change_form_datasets = [RelatedItemsDataset]
```

## Paginator

Use infinite scroll pagination:

```python
from unfold.paginator import InfinitePaginator

class MyAdmin(ModelAdmin):
    paginator = InfinitePaginator
    show_full_result_count = False
    list_per_page = 20
```

## Third-Party Integrations

Unfold provides styled wrappers for common Django packages. See [references/resources.md](references/resources.md) for complete setup guides.

| Package | Unfold Module | Setup |
|---------|--------------|-------|
| django-import-export | `unfold.contrib.import_export` | Use `ImportForm`, `ExportForm`, `SelectableFieldsExportForm` |
| django-guardian | `unfold.contrib.guardian` | Styled guardian integration |
| django-simple-history | `unfold.contrib.simple_history` | Styled history integration |
| django-constance | `unfold.contrib.constance` | Styled constance config |
| django-location-field | `unfold.contrib.location_field` | Location widget |
| django-modeltranslation | Compatible | Mix `TabbedTranslationAdmin` with `ModelAdmin` |
| django-celery-beat | Compatible (rewire) | Unregister 5 models, re-register with Unfold |
| django-money | `unfold.widgets` | `UnfoldAdminMoneyWidget` |
| djangoql | Compatible | Mix `DjangoQLSearchMixin` with `ModelAdmin` |
| django-crispy-forms | Compatible | Unfold template pack available |

```python
# Multiple inheritance - Unfold ModelAdmin always last
@admin.register(MyModel)
class MyAdmin(DjangoQLSearchMixin, SimpleHistoryAdmin, GuardedModelAdmin, ModelAdmin):
    pass
```

## Built-In Template Components

Unfold ships reusable template components for dashboards and custom pages:

| Component | Path | Key Variables |
|-----------|------|---------------|
| Card | `unfold/components/card.html` | `title`, `footer`, `label`, `icon` |
| Bar Chart | `unfold/components/chart/bar.html` | `data` (JSON), `height`, `width` |
| Line Chart | `unfold/components/chart/line.html` | `data` (JSON), `height`, `width` |
| Progress | `unfold/components/progress.html` | `value`, `title`, `description` |
| Table | `unfold/components/table.html` | `table`, `card_included`, `striped` |
| Button | `unfold/components/button.html` | `name`, `href`, `submit` |
| Tracker | `unfold/components/tracker.html` | `data` |
| Cohort | `unfold/components/cohort.html` | `data` |

```html
{% load unfold %}
{% component "MyKPIComponent" %}{% endcomponent %}
```

## User Admin Forms

Unfold provides styled versions of Django's auth admin forms:

```python
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
```

## Reference Files

Detailed documentation split by topic:

- **[references/configuration.md](references/configuration.md)** - Complete UNFOLD settings dict, sidebar, tabs, theming, environment, login
- **[references/actions-filters.md](references/actions-filters.md)** - Action types and signatures, display decorator, all filter classes
- **[references/widgets-inlines.md](references/widgets-inlines.md)** - Complete widget class list (35+), inline variants, nonrelated inlines, forms
- **[references/dashboard.md](references/dashboard.md)** - Dashboard components, sections, datasets, custom templates, Tailwind patterns
- **[references/resources.md](references/resources.md)** - Official links, all third-party integrations, common patterns, version compatibility, Unfold Studio

Read the relevant reference file when you need detailed configuration options, the full list of available classes, complete code examples, or integration setup guides for a specific feature area.

### Key External References

| Resource | URL |
|----------|-----|
| Docs | https://unfoldadmin.com/docs/ |
| GitHub | https://github.com/unfoldadmin/django-unfold |
| Demo App (Formula) | https://github.com/unfoldadmin/formula |
| Live Demo | https://demo.unfoldadmin.com |
| Material Symbols (Icons) | https://fonts.google.com/icons |

When uncertain about an implementation pattern, consult `formula/admin.py` and `formula/settings.py` in the Formula demo repo - it covers virtually every Unfold feature.
