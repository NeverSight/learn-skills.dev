---
name: bagisto-attribute-development
description: Use when working with Bagisto's EAV attribute system — adding or changing an attribute, attribute family or group, reading or writing a product attribute value, or debugging a value that reads back empty or from the wrong locale or channel. Trigger phrases include "attribute", "EAV", "attribute family", "attribute group", "attribute option", "custom attribute", "value_per_locale", "value_per_channel", "product_flat", "swatch".
requires: bagisto-coding-standards
license: MIT
---

# Attribute Development

Bagisto stores product data as **EAV** — entity, attribute, value — rather than
as columns on `products`. A product row carries almost nothing; its name, price,
description and every custom field live in `product_attribute_values`, one row
per attribute per locale per channel.

This is the concept most Bagisto mistakes trace back to, so it is worth reading
[eav.md](eav.md) before changing anything that touches product data.

## Reference files

| File | Load when |
|---|---|
| [eav.md](eav.md) | How values are stored and resolved — the column map, scope, the flat index |
| [attributes.md](attributes.md) | Creating attributes, families, groups, options, validation and swatches |

## The shape

```
attribute_families            a product type's whole form  (e.g. "Default")
  └── attribute_groups        a tab/section within it      (e.g. "General")
        └── attributes        a field                      (e.g. "name")
              └── attribute_options   for select, multiselect and checkbox
```

A product belongs to one family, and that family decides which attributes it
has. `AttributeFamily::custom_attributes()` and
`AttributeGroup::custom_attributes()` are the relations that walk it.

## The column map

An attribute's `type` decides which column of `product_attribute_values` holds
its value:

| type | column |
|---|---|
| `text`, `textarea`, `multiselect`, `checkbox`, `file`, `image` | `text_value` |
| `price` | `float_value` |
| `boolean` | `boolean_value` |
| `select` | `integer_value` |
| `date` | `date_value` |
| `datetime` | `datetime_value` |

This map lives on `Attribute::$attributeTypeFields`, and the model exposes the
resolved name as `$attribute->column_name`. Never guess the column — read it
from the attribute, or a `select` silently writes into `text_value` and reads
back as null.

`AttributeTypeEnum` is the authoritative list of types; `ValidationEnum`
(`numeric`, `email`, `decimal`, `url`, `regex`) and `SwatchTypeEnum`
(`dropdown`, `color`, `image`, `text`) cover the rest.

## Scope: the two flags that cause most bugs

Every attribute carries `value_per_locale` and `value_per_channel`. Together
they decide how many rows a single attribute has for one product, and which one
a read returns:

| `value_per_channel` | `value_per_locale` | Rows per product |
|---|---|---|
| false | false | 1 |
| false | true | one per locale |
| true | false | one per channel |
| true | true | one per channel per locale |

`Product::getCustomAttributeValue()` resolves the right row for the **requested**
channel and locale, falling back to the default channel and locale when the
requested one is empty. A value that "disappears" on a second locale is almost
always an attribute written without honouring these flags.

The table enforces this with a unique index on
`(channel, locale, attribute_id, product_id)`, so writing the wrong scope
combination is a constraint violation rather than a silent duplicate.

## Non-negotiables

- **Go through the repository.** `AttributeRepository`, `AttributeFamilyRepository`,
  `AttributeGroupRepository`, `AttributeOptionRepository` — never write
  `product_attribute_values` by hand.
- **Read the column from the attribute**, via `column_name` or
  `$attributeTypeFields`. A hard-coded column is a bug waiting for the first
  non-text attribute.
- **Honour `value_per_locale` and `value_per_channel` on every write**, not just
  on read. Writing one row for an attribute scoped per locale loses every other
  locale's value.
- **A `select`/`multiselect` value is an option id**, not the label. `select`
  stores one id in `integer_value`; `multiselect` stores comma-separated ids in
  `text_value`.
- **Option labels are translatable** — they live in
  `attribute_option_translations`, so a label added in one locale must be added
  in all 22.
- **Changing an attribute's `type` orphans its existing values**, because the
  new type reads a different column. Treat it as a data migration, not an edit.
- **Reindex after a change that affects listing.** Filterable and listing
  attributes are denormalised into `product_flat` by the flat indexer; until it
  runs, the grid and storefront show the old value.

**REQUIRED SUB-SKILL:** Use bagisto-change-verification before calling any change done.
