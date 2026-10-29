---
name: desk-customization
description: Customize Frappe Desk UI with form scripts, list view scripts, report scripts, dialogs, and client-side JavaScript APIs. Use when building interactive Desk experiences, adding custom buttons, or scripting form behavior.
---

# Frappe Desk Customization

Customize the Frappe Desk admin UI with form scripts, list views, dialogs, and client-side APIs.

## When to use

- Adding custom buttons or actions to forms
- Filtering Link fields dynamically
- Toggling field visibility based on conditions
- Customizing list view indicators and bulk actions
- Building interactive dialogs and prompts
- Adding client-side validation before save
- Injecting scripts into other apps' DocTypes via hooks

## Inputs required

- Target DocType for customization
- Whether script is app-level (version controlled) or Client Script (site-specific)
- Events to hook into (refresh, validate, field change, etc.)
- UI behavior requirements (buttons, filters, visibility)

## Procedure

### 0) Choose script type

| Type | Location | Version Controlled | Use Case |
|------|----------|-------------------|----------|
| App-level form script | `<app>/<module>/doctype/<doctype>/<doctype>.js` | Yes | Standard app behavior |
| Client Script | DocType: Client Script | No (DB) | Site-specific customization |
| Hook-injected script | Via `doctype_js` in `hooks.py` | Yes | Extend other apps' DocTypes |

### 1) Write form scripts

```javascript
frappe.ui.form.on("My DocType", {
    // Called once during form setup
    setup(frm) {
        frm.set_query("customer", function() {
            return {
                filters: { "status": "Active" }
            };
        });
    },

    // Called every time form loads or refreshes
    refresh(frm) {
        if (frm.doc.status === "Draft") {
            frm.add_custom_button(__("Submit for Review"), function() {
                frappe.call({
                    method: "my_app.api.submit_for_review",
                    args: { name: frm.doc.name },
                    callback(r) {
                        frm.reload_doc();
                    }
                });
            }, __("Actions"));
        }

        // Toggle field visibility
        frm.toggle_display("discount_section", frm.doc.grand_total > 1000);

        // Set field properties
        frm.set_df_property("notes", "read_only", frm.doc.docstatus === 1);
    },

    // Called before save — return false to cancel
    validate(frm) {
        if (frm.doc.end_date < frm.doc.start_date) {
            frappe.msgprint(__("End date must be after start date"));
            frappe.validated = false;
        }
    },

    // Field change handler (use fieldname as key)
    customer(frm) {
        if (frm.doc.customer) {
            frappe.db.get_value("Customer", frm.doc.customer, "territory",
                function(r) {
                    frm.set_value("territory", r.territory);
                }
            );
        }
    },

    // Before save hook
    before_save(frm) {
        frm.doc.full_name = `${frm.doc.first_name} ${frm.doc.last_name}`;
    },

    // After save hook
    after_save(frm) {
        frappe.show_alert({
            message: __("Document saved successfully"),
            indicator: "green"
        });
    }
});

// Child table events
frappe.ui.form.on("My DocType Item", {
    qty(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, "amount", row.qty * row.rate);
        calculate_total(frm);
    },

    items_remove(frm) {
        calculate_total(frm);
    }
});

function calculate_total(frm) {
    let total = 0;
    (frm.doc.items || []).forEach(row => {
        total += row.amount || 0;
    });
    frm.set_value("grand_total", total);
}
```

### 2) Build dialogs and prompts

```javascript
// Simple prompt
frappe.prompt(
    { fieldname: "reason", fieldtype: "Small Text", label: "Reason", reqd: 1 },
    function(values) {
        frappe.call({
            method: "my_app.api.reject",
            args: { name: frm.doc.name, reason: values.reason }
        });
    },
    __("Rejection Reason"),
    __("Reject")
);

// Multi-field dialog
let d = new frappe.ui.Dialog({
    title: __("Configure Settings"),
    fields: [
        { fieldname: "email", fieldtype: "Data", options: "Email", label: "Email", reqd: 1 },
        { fieldname: "frequency", fieldtype: "Select", options: "Daily\nWeekly\nMonthly", label: "Frequency" },
        { fieldname: "active", fieldtype: "Check", label: "Active", default: 1 }
    ],
    primary_action_label: __("Save"),
    primary_action(values) {
        frappe.call({
            method: "my_app.api.save_settings",
            args: values,
            callback() {
                d.hide();
                frappe.show_alert({ message: __("Settings saved"), indicator: "green" });
            }
        });
    }
});
d.show();

// Confirmation dialog
frappe.confirm(
    __("Are you sure you want to delete this?"),
    function() { /* Yes */ },
    function() { /* No */ }
);
```

### 3) Make server calls

```javascript
// Standard call (callback)
frappe.call({
    method: "my_app.api.get_stats",
    args: { customer: frm.doc.customer },
    freeze: true,
    freeze_message: __("Loading..."),
    callback(r) {
        if (r.message) {
            frm.set_value("total_orders", r.message.total);
        }
    }
});

// Promise-based call
let result = await frappe.xcall("my_app.api.get_stats", {
    customer: frm.doc.customer
});
```

### 4) Customize list views

```javascript
// my_app/public/js/sample_doc_list.js
// or via hooks: doctype_list_js = {"Sample Doc": "public/js/sample_doc_list.js"}

frappe.listview_settings["Sample Doc"] = {
    // Status indicator colors
    get_indicator(doc) {
        if (doc.status === "Open") return [__("Open"), "orange", "status,=,Open"];
        if (doc.status === "Closed") return [__("Closed"), "green", "status,=,Closed"];
        return [__("Draft"), "grey", "status,=,Draft"];
    },

    // Add bulk actions
    onload(listview) {
        listview.page.add_action_item(__("Mark as Closed"), function() {
            let names = listview.get_checked_items(true);
            frappe.call({
                method: "my_app.api.bulk_close",
                args: { names },
                callback() { listview.refresh(); }
            });
        });
    },

    // Hide default "New" button
    hide_name_column: true
};
```

### 5) Use realtime events

```javascript
// Listen for server-side events
frappe.realtime.on("export_complete", function(data) {
    frappe.show_alert({
        message: __("Export complete: {0} records", [data.count]),
        indicator: "green"
    });
});
```

### 6) Inject scripts via hooks

To extend a DocType from another app without modifying it:

```python
# hooks.py
doctype_js = {
    "Sales Order": "public/js/sales_order_custom.js"
}

doctype_list_js = {
    "Sales Order": "public/js/sales_order_list_custom.js"
}
```

```bash
# Rebuild assets after adding hook scripts
bench build --app my_app
```

### 7) Navigation and routing

```javascript
// Navigate to a document
frappe.set_route("Form", "Sales Order", "SO-001");

// Navigate to list with filters
frappe.route_options = { "status": "Open" };
frappe.set_route("List", "Sales Order");

// Get current route
let route = frappe.get_route();
```

## Verification

- [ ] Form script loads without JS console errors
- [ ] Custom buttons appear in correct conditions
- [ ] Field visibility toggles work
- [ ] Link field filters return correct options
- [ ] Validation prevents invalid saves
- [ ] List view indicators display correctly
- [ ] Dialogs open, collect input, and submit

## Failure modes / debugging

- **Script not loading**: Check file path matches DocType; run `bench build`
- **Button not appearing**: Check condition logic in `refresh`; verify `frm.doc.docstatus`
- **Event not firing**: Verify event name matches exactly (case-sensitive)
- **Hook script ignored**: Check `hooks.py` path; rebuild assets
- **`frappe.call` failing**: Check method path; verify `@frappe.whitelist()` on server

## Escalation

- For server-side controller logic → `doctype-development`
- For RPC endpoint implementation → `api-development`
- For Frappe UI (Vue 3) frontends → `frontend-development`

## References

- [references/desk.md](references/desk.md) — Desk UI views and scripting
- [references/js-api.md](references/js-api.md) — JavaScript client API reference

## Guardrails

- **Use `frm.doc` not `doc` directly**: Always access document via `frm.doc` for consistency and reactivity
- **Validate before save**: Use `frm.validate()` in `validate` event, not `before_save`
- **Async awareness**: `frappe.call()` is async; use callbacks or async/await for sequential operations
- **Refresh after field changes**: Call `frm.refresh_field()` or `frm.refresh_fields()` after programmatic changes
- **Check `frm.is_new()` appropriately**: Some operations only make sense on saved documents

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Missing `frm.refresh_field()` after `set_value` | UI doesn't update | Call `frm.refresh_field('fieldname')` after `frm.set_value()` |
| Wrong event hook name | Event never fires | Use exact names: `refresh`, `validate`, `onload`, `before_save` |
| Blocking UI with sync calls | Page freezes | Use `frappe.call()` with async: true (default) |
| Using `cur_frm` instead of `frm` | Breaks in dialogs/multiple forms | Always use the `frm` parameter passed to handlers |
| Not checking `frm.doc.docstatus` | Buttons appear on submitted docs | Check `frm.doc.docstatus == 0` before showing edit actions |
| `console.log(frm.doc)` showing stale data | Debugging confusion | Use `frm.reload_doc()` or check network responses |
