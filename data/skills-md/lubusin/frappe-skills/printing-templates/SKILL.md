---
name: printing-templates
description: Build print formats, email templates, and web page templates using Jinja. Generate PDFs and configure letter heads. Use when creating custom print layouts, email templates, or any Jinja-based rendering in Frappe.
---

# Frappe Printing & Templates

Create print formats, email templates, and document templates using Jinja in Frappe.

## When to use

- Creating custom print formats for documents
- Building email templates with dynamic content
- Generating PDFs from documents
- Using Jinja templating in web pages
- Configuring letter heads for branding
- Using the Print Format Builder

## Inputs required

- Target DocType for the print format
- Layout requirements (fields, tables, headers)
- Whether format is standard (version controlled) or custom (DB-stored)
- Letter Head / branding requirements
- PDF generation needs

## Procedure

### 0) Choose format type

| Type | How to Create | Version Controlled | Customizable by User |
|------|--------------|-------------------|---------------------|
| Standard | Developer Mode, saved as JSON | Yes | No |
| Print Format Builder | Drag-and-drop UI | No (DB) | Yes |
| Custom HTML (Jinja) | Type "new print format" in awesomebar | Optional | Depends |

### 1) Create a Jinja print format

Create via awesomebar → "New Print Format":
1. Set a unique name
2. Link to the target DocType
3. Set "Standard" = "No" (or "Yes" for dev mode export)
4. Check "Custom Format"
5. Set Print Format Type = "Jinja"
6. Write your Jinja HTML

```jinja
<div class="print-format">
    <h1>{{ doc.name }}</h1>
    <p><strong>{{ _("Customer") }}:</strong> {{ doc.customer }}</p>
    <p><strong>{{ _("Date") }}:</strong> {{ frappe.format_date(doc.transaction_date) }}</p>

    <table class="table table-bordered">
        <thead>
            <tr>
                <th>{{ _("Item") }}</th>
                <th>{{ _("Qty") }}</th>
                <th class="text-right">{{ _("Rate") }}</th>
                <th class="text-right">{{ _("Amount") }}</th>
            </tr>
        </thead>
        <tbody>
            {% for item in doc.items %}
            <tr>
                <td>{{ item.item_name }}</td>
                <td>{{ item.qty }}</td>
                <td class="text-right">{{ frappe.format(item.rate, {'fieldtype': 'Currency'}) }}</td>
                <td class="text-right">{{ frappe.format(item.amount, {'fieldtype': 'Currency'}) }}</td>
            </tr>
            {% endfor %}
        </tbody>
        <tfoot>
            <tr>
                <td colspan="3" class="text-right"><strong>{{ _("Total") }}</strong></td>
                <td class="text-right"><strong>{{ frappe.format(doc.grand_total, {'fieldtype': 'Currency'}) }}</strong></td>
            </tr>
        </tfoot>
    </table>

    {% if doc.terms %}
    <div class="terms">
        <h4>{{ _("Terms & Conditions") }}</h4>
        <p>{{ doc.terms }}</p>
    </div>
    {% endif %}
</div>

<style>
    .print-format { font-family: Arial, sans-serif; }
    .print-format h1 { color: #333; }
    .print-format table { width: 100%; margin-top: 20px; }
</style>
```

### 2) Use Frappe Jinja API

**Data fetching in templates:**

```jinja
{# Fetch a document #}
{% set customer = frappe.get_doc('Customer', doc.customer) %}
{{ customer.customer_name }}

{# List query (ignores permissions) #}
{% set open_orders = frappe.get_all('Sales Order',
    filters={'customer': doc.customer, 'status': 'To Deliver and Bill'},
    fields=['name', 'grand_total'],
    order_by='creation desc',
    page_length=5) %}

{# Permission-aware list query #}
{% set my_tasks = frappe.get_list('Task',
    filters={'owner': frappe.session.user}) %}

{# Single value lookup #}
{% set company_abbr = frappe.db.get_value('Company', doc.company, 'abbr') %}

{# Settings value #}
{% set timezone = frappe.db.get_single_value('System Settings', 'time_zone') %}
```

**Formatting:**

```jinja
{{ frappe.format(50000, {'fieldtype': 'Currency'}) }}
{{ frappe.format_date('2025-01-15') }}
{{ frappe.format_date(doc.posting_date) }}
```

**Session and context:**

```jinja
{{ frappe.session.user }}
{{ frappe.get_fullname() }}
{{ frappe.lang }}
{{ _("Translatable string") }}
```

**URLs:**

```jinja
<a href="{{ frappe.get_url() }}/app/sales-order/{{ doc.name }}">View Order</a>
```

### 3) Build email templates

```jinja
Dear {{ doc.customer_name }},

Your order {{ doc.name }} has been confirmed.

Items:
{% for item in doc.items %}
- {{ item.item_name }} x {{ item.qty }}
{% endfor %}

Total: {{ frappe.format(doc.grand_total, {'fieldtype': 'Currency'}) }}

Thank you,
{{ frappe.get_fullname() }}
```

### 4) Generate PDFs programmatically

```python
import frappe

# Generate PDF
pdf_content = frappe.get_print(
    doctype="Sales Invoice",
    name="SINV-001",
    print_format="Custom Invoice",
    as_pdf=True
)

# Attach PDF to document
frappe.attach_print(
    doctype="Sales Invoice",
    name="SINV-001",
    print_format="Custom Invoice",
    file_name="invoice.pdf"
)

# Send with email
frappe.sendmail(
    recipients=["customer@example.com"],
    subject="Your Invoice",
    message="Please find attached your invoice.",
    attachments=[{
        "fname": "invoice.pdf",
        "fcontent": pdf_content
    }]
)
```

### 5) Configure Letter Head

1. Navigate to Letter Head list → New
2. Upload company logo and header image
3. Set as default for the company
4. Letter Head appears automatically on print formats

### 6) Use Jinja filters

```jinja
{{ doc.customer_name|upper }}        {# UPPERCASE #}
{{ doc.notes|truncate(100) }}        {# Truncate text #}
{{ doc.description|striptags }}      {# Remove HTML #}
{{ doc.html_content|safe }}          {# Render raw HTML (trusted only!) #}
{{ items|length }}                   {# Count items #}
{{ items|first }}                    {# First item #}
{{ names|join(', ') }}               {# Join list #}
{{ amount|round(2) }}               {# Round number #}
{{ value|default('N/A') }}          {# Default if undefined #}
{{ data|tojson }}                    {# Convert to JSON #}
```

### 7) Template inheritance and macros

```jinja
{# macros/fields.html #}
{% macro field_row(label, value) %}
<tr>
    <td class="label"><strong>{{ _(label) }}</strong></td>
    <td>{{ value }}</td>
</tr>
{% endmacro %}

{# In print format #}
{% from "macros/fields.html" import field_row %}
<table>
    {{ field_row("Customer", doc.customer_name) }}
    {{ field_row("Date", frappe.format_date(doc.posting_date)) }}
    {{ field_row("Total", frappe.format(doc.grand_total, {'fieldtype': 'Currency'})) }}
</table>
```

## Verification

- [ ] Print format renders correctly in Print View
- [ ] All fields display with proper formatting
- [ ] PDF generation works without errors
- [ ] Email templates render with correct data
- [ ] Letter Head appears on printed documents
- [ ] Translations work in templates (`_()`)
- [ ] No XSS risks from unescaped content

## Failure modes / debugging

- **Template syntax error**: Check Jinja delimiters (`{{ }}`, `{% %}`); look for unclosed blocks
- **Field not rendering**: Verify field name matches DocType schema; check child table access pattern
- **PDF generation fails**: Check wkhtmltopdf installation; verify print format Jinja is valid
- **Styling issues in PDF**: Use inline styles; avoid complex CSS; test with Print View first
- **Permission error in template**: Use `frappe.get_all` (no permission check) vs `frappe.get_list`

## Escalation

- For app-level hooks and structure → `app-development`
- For DocType schema questions → `doctype-development`

## References

- [references/jinja.md](references/jinja.md) — Jinja templating and Frappe Jinja API
- [references/printing.md](references/printing.md) — Print formats and PDF generation

## Guardrails

- **Test with actual data**: Always preview with real documents; edge cases break templates
- **Handle missing fields gracefully**: Use `{{ doc.field or '' }}` or `{% if doc.field %}`
- **Use `get_url()` for images**: Never hardcode URLs; use `{{ frappe.utils.get_url() }}/files/...`
- **Escape user content**: Use `{{ value | e }}` for user-generated content to prevent XSS
- **Keep styling inline**: PDF generators don't support external CSS; use inline `style` attributes

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Wrong Jinja syntax | Template error, blank output | Use `{{ }}` for output, `{% %}` for logic; check closing tags |
| Missing filters | Raw data displayed | Use `frappe.format()` or `frappe.format_date()` for formatting |
| Hardcoded URLs | Images/links break across sites | Use `{{ frappe.utils.get_url() }}` for absolute URLs |
| Accessing child table wrong | Empty or error | Use `{% for item in doc.items %}` not `doc.child_table_name` |
| Complex CSS in print format | Styling lost in PDF | Use inline styles, simple layouts, `<table>` for structure |
| Not handling None values | `'None'` string in output | Use `{{ value or '' }}` or `{% if value %}` |
