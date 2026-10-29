---
name: doctype-development
description: Create and modify Frappe DocTypes including schema design, controllers, child tables, and customization. Use when building data models, adding fields, or implementing document lifecycle logic.
---

# Frappe DocType Development

Build and modify DocTypes—the core data model abstraction in Frappe Framework.

## When to use

- Creating new DocTypes (standard, single, child table, submittable, tree)
- Adding or modifying fields on existing DocTypes
- Implementing controller logic (validate, before_save, on_submit, etc.)
- Setting up naming series and auto-naming
- Configuring permissions and workflows
- Building child tables and parent-child relationships

## Inputs required

- Target app and module path
- DocType name and type (standard/single/child/submittable/tree)
- Field definitions (name, type, options)
- Permission requirements by role
- Whether workflow is needed

## Procedure

### 0) Verify environment

```bash
# Ensure developer mode is enabled
bench --site <site> console
>>> frappe.conf.developer_mode  # Must be True
```

### 1) Choose DocType type

| Type | Use Case | Key Setting |
|------|----------|-------------|
| Standard | Multiple records | Default |
| Single | Config/settings (one record) | `issingle: 1` |
| Child Table | Rows in parent table | `istable: 1` |
| Submittable | Draft→Submit→Cancel workflow | `is_submittable: 1` |
| Tree | Hierarchical data | `is_tree: 1` |
| Virtual | External data source | `is_virtual: 1` |

### 2) Create DocType

**Option A: Via UI (recommended for new DocTypes)**
1. Navigate to DocType List → New
2. Define fields, permissions, settings
3. Save (exports to app in developer mode)

**Option B: Via code**
```python
# Create DocType JSON in: 
# <app>/<module>/doctype/<doctype_name>/<doctype_name>.json
```

### 3) Define fields

Common field patterns:
```json
{
  "fieldname": "customer",
  "fieldtype": "Link",
  "label": "Customer",
  "options": "Customer",
  "reqd": 1
}
```

See [references/field-types.md](references/field-types.md) for all field types.

### 4) Implement controller

Create `<doctype_name>.py` alongside the JSON:

```python
import frappe
from frappe.model.document import Document

class MyDocType(Document):
    def validate(self):
        # Lightweight validation
        if not self.customer:
            frappe.throw("Customer is required")
    
    def before_save(self):
        # Pre-save normalization
        self.full_name = f"{self.first_name} {self.last_name}"
    
    def after_insert(self):
        # Post-create side effects
        frappe.publish_realtime("new_doc", {"name": self.name})
```

### 5) Set up naming

```json
{
  "autoname": "naming_series:",
  "fields": [
    {
      "fieldname": "naming_series",
      "fieldtype": "Select",
      "options": "PRJ-.YYYY.-\nPRJ-.YYYY.-.###"
    }
  ]
}
```

Options: `field:fieldname`, `naming_series:`, `hash`, `format:PREFIX-{####}`

### 6) Configure permissions

Set in DocType → Permissions tab:
- Role + Read/Write/Create/Delete/Submit/Cancel
- User permissions for row-level filtering

### 7) Add workflow (if needed)

Create Workflow DocType linking to your DocType with states and transitions.

## Verification

- [ ] DocType appears in list and can create new records
- [ ] All fields save correctly
- [ ] Controller hooks fire (check logs)
- [ ] Permissions enforced for each role
- [ ] Naming series generates correctly
- [ ] Run: `bench --site <site> migrate` succeeds

## Failure modes / debugging

- **DocType not found**: Check module path and app installation
- **Controller not loading**: Verify class name matches DocType name (PascalCase)
- **Fields not saving**: Check fieldtype and options compatibility
- **Permission denied**: Verify role permissions and User Permissions

## Escalation

- For complex permission logic, see [references/permissions.md](references/permissions.md)
- For child table patterns, see [references/child-tables.md](references/child-tables.md)
- For Virtual DocTypes, see [references/virtual-doctypes.md](references/virtual-doctypes.md)

## References

- [references/field-types.md](references/field-types.md) - All field types and options
- [references/controllers.md](references/controllers.md) - Controller lifecycle hooks
- [references/child-tables.md](references/child-tables.md) - Parent-child patterns
- [references/naming.md](references/naming.md) - Naming patterns

## Guardrails

- **Check developer_mode before schema changes**: DocType modifications only export to files when `developer_mode = 1` in site config
- **Verify naming series uniqueness**: Ensure naming series prefixes don't conflict with existing DocTypes
- **Test child tables separately**: Child tables have their own lifecycle; test them in isolation before parent integration
- **Always run migrate after changes**: Schema changes require `bench --site <site> migrate` to apply
- **Validate fieldname conventions**: Use snake_case, max 140 chars, no reserved SQL keywords

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Missing `reqd` on mandatory fields | Users can save incomplete data | Set `reqd: 1` on fields that must have values |
| Wrong fieldtype for data | Data truncation or validation errors | Match fieldtype to data (e.g., `Currency` for money, not `Float`) |
| Not running `bench migrate` | Schema changes not applied to database | Always run `bench --site <site> migrate` after DocType changes |
| Circular Link dependencies | DocType creation fails | Use Dynamic Link or restructure relationships |
| Controller class name mismatch | Controller methods not called | Class name must be PascalCase of DocType name (e.g., `SalesOrder` for "Sales Order") |
| Missing `in_list_view` on key fields | Fields not visible in list | Set `in_list_view: 1` on important fields |
