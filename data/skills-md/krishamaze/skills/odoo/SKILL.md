---
name: odoo
description: >
  Authoritative Odoo 19.0 development knowledge. Use when the user mentions Odoo, odoo module,
  __manifest__, ORM, account.move, res.partner, ir.model, odoo addon, odoo model, odoo field,
  odoo view, odoo controller, odoo migration, odoo upgrade, or any Odoo development task.
  Triggers on: "odoo", "odoo module", "odoo model", "odoo ORM", "odoo 19", "odoo addon",
  "odoo development", "odoo accounting", "odoo customization". Source: odoo/odoo@19.0 on GitHub.
  Zero hallucination — all patterns verified from source code and official documentation.
license: MIT
metadata:
  author: NexaraTech
  version: "1.0.0"
  odoo-version: "19.0"
  source: "https://github.com/odoo/odoo/tree/19.0"
  evidence: "odoo/odoo@19.0 GitHub source + docs.odoo.com/19.0"
---

# Odoo 19.0 Development Skill

Source-verified knowledge of Odoo 19.0 internals — ORM, module structure, core models,
field types, decorators, and critical breaking changes from earlier versions.
No opinions about business logic. Pure platform facts.

---

## Version

**Current stable: 19.0** (default branch on `odoo/odoo` GitHub as of 2026)
Branch naming: `19.0`, `18.0`, `17.0` — each is a separate long-lived branch.
Community edition: `odoo/odoo`. Enterprise: `odoo/enterprise` (private).

---

## Module Structure

Official structure from `docs.odoo.com/19.0/contributing/development/coding_guidelines`:

```
my_module/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── my_model.py
├── views/
│   └── my_model_views.xml
├── security/
│   ├── ir.model.access.csv
│   └── my_module_security.xml
├── data/
│   └── my_module_data.xml
├── controllers/
│   ├── __init__.py
│   └── my_controller.py
├── report/
│   └── my_report.xml
└── static/
    └── src/
```

---

## `__manifest__.py`

```python
{
    'name': 'My Module',
    'version': '19.0.1.0.0',   # format: <odoo_version>.<major>.<minor>.<patch>.<fix>
    'summary': 'One-line description',
    'description': """Long description""",
    'author': 'Author Name',
    'website': 'https://example.com',
    'category': 'Accounting/Accounting',
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/my_views.xml',
    ],
    'demo': ['demo/demo_data.xml'],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
```

Required: `name`, `depends`. Everything else is optional but recommended.
`version` must start with the Odoo major version (`19.0.`).

---

## ORM — Imports (19.0)

```python
# Standard
from odoo import models, fields, api, Command, _
from odoo.fields import Domain
from odoo.exceptions import UserError, ValidationError, AccessError
from odoo.tools import float_compare, float_is_zero, float_round
from odoo.tools.translate import _

# Registry (CHANGED in 19.0)
from odoo.modules.registry import Registry   # NOT: from odoo import registry
```

---

## Model Definition

```python
from odoo import models, fields, api

class MyModel(models.Model):
    _name = 'my.model'
    _description = 'My Model'
    _order = 'name asc'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(default=True)
```

Model types:
- `models.Model` — persistent, stored in PostgreSQL
- `models.TransientModel` — temporary, auto-cleaned (wizards)
- `models.AbstractModel` — mixin, no table

To extend an existing model:
```python
class ResPartner(models.Model):
    _inherit = 'res.partner'
    my_field = fields.Char()
```

---

## Field Types

Read `references/fields.md` for full parameter reference. Quick types:

| Field | Python type | Notes |
|---|---|---|
| `Char` | str | max_length optional |
| `Text` | str | multi-line |
| `Html` | str | sanitized HTML |
| `Integer` | int | |
| `Float` | float | digits=(precision, scale) |
| `Monetary` | float | requires currency_field |
| `Boolean` | bool | |
| `Date` | date | stored as `DATE` in PG |
| `Datetime` | datetime | stored as `TIMESTAMP` in PG, always UTC |
| `Selection` | str | selection=[('key','Label')] |
| `Many2one` | int | FK to other model |
| `One2many` | recordset | inverse_name required |
| `Many2many` | recordset | relation table auto-created |
| `Binary` | bytes | attachment=True for large files |

---

## ORM Methods

```python
# Create
record = self.env['my.model'].create({'name': 'Test'})

# Read
record.name
records = self.env['my.model'].browse([1, 2, 3])

# Search
records = self.env['my.model'].search([('name', '=', 'Test')], limit=10, order='name asc')
count = self.env['my.model'].search_count([('active', '=', True)])

# Write
record.write({'name': 'Updated'})

# Unlink
record.unlink()

# sudo
self.env['my.model'].sudo().search([])

# with_company
self.env['my.model'].with_company(company_id).create({})
```

---

## Decorators

```python
@api.depends('field1', 'field2')          # computed field trigger
def _compute_something(self):
    for record in self:
        record.result = record.field1 + record.field2

@api.onchange('field1')                   # UI-only, not stored
def _onchange_field1(self):
    self.field2 = self.field1 * 2

@api.constrains('field1', 'field2')      # validation, raises ValidationError
def _check_something(self):
    for record in self:
        if record.field1 < 0:
            raise ValidationError("Field1 must be positive")

@api.model                                # class-level method (no self record)
def create(self, vals):
    return super().create(vals)

@api.model_create_multi                   # batch create (preferred over @api.model for create)
def create(self, vals_list):
    return super().create(vals_list)

@api.private                              # NEW in 19.0 — marks method as not RPC-accessible
def _internal_method(self):
    pass
```

---

## Commands (One2many / Many2many)

```python
from odoo import Command

# Create and link new record
Command.create({'name': 'New'})

# Link existing record (Many2many)
Command.link(record.id)

# Unlink (Many2many — remove from relation only)
Command.unlink(record.id)

# Delete record
Command.delete(record.id)

# Replace all records
Command.set([id1, id2, id3])

# Clear all
Command.clear()

# Update existing
Command.update(record.id, {'name': 'Updated'})
```

---

## Domain Syntax

```python
# Standard domain
[('field', 'operator', value)]

# Operators: =, !=, <, >, <=, >=, in, not in, like, ilike, not like, not ilike, =like, =ilike, any, not any

# Logical operators
['&', ('a', '=', 1), ('b', '=', 2)]   # AND (default)
['|', ('a', '=', 1), ('b', '=', 2)]   # OR
['!', ('a', '=', 1)]                   # NOT

# New in 17+: Domain class
from odoo.fields import Domain
d = Domain('field', '=', value)
combined = d & Domain('other', '!=', False)
```

---

## Critical Breaking Changes by Version

Read `references/breaking-changes.md` for full list. Critical ones:

### Broken in 17.0
- `name_get()` **deprecated** → override `_compute_display_name` instead
- `read_group()` **deprecated** → use `_read_group()` (internal) or `formatted_read_group()` (public)
- `group_operator` field attr **deprecated** → use `aggregator`
- Translations now stored as JSONB, not in database table

### Broken in 18.0
- `group_operator` produces deprecation warning — must use `aggregator`

### Broken in 19.0
- `read_group` **removed** from public API
- `name_get()` **removed** — `display_name` is the only way
- `odoo.osv` **deprecated**
- `record._cr`, `record._context`, `record._uid` **deprecated** (use `self.env.cr`, `self.env.context`, `self.env.uid`)
- HTTP routes: `type='json'` → must be `type='jsonrpc'`
- `res.partner.title` model **removed**
- `from odoo import registry` → `from odoo.modules.registry import Registry`
- UoM: use `relative_uom_id` for direct unit relationships
- `res.groups.privilege` replaces `ir.module.category` for group categories
- Demo data **not loaded by default** — must be explicitly requested
- ORM code moved to `odoo/orm/` subpackage (internal restructure)

---

## Reference Files

Load on demand:

| File | Load when |
|---|---|
| `references/fields.md` | Need full field parameter reference |
| `references/accounting.md` | Working with account.move, account.payment, account.journal |
| `references/breaking-changes.md` | Upgrading or porting modules between versions |
| `references/security.md` | Access rights, record rules, ir.model.access.csv |
