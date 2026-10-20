---
name: shopping-list-add
description: "Add a product to the shopping list for a store by setting that store's front matter boolean to true in the product note in the Obsidian vault, creating the product note first when none exists. With no store named, it goes on the amazon_fresh catch-all list. Use when asked to add something to the shopping list, with or without a store, put an item on the list for a store, or mark a product to buy at Trader Joe's, Costco, PCC, or any other store."
---

## Adding a product to a store's shopping list

Vault path: `/Users/mtm/Documents/Obsidian Vault`

A product is on a store's shopping list when the store's boolean in the product note's front matter is `true`, for example `trader_joes: true`.

Each store also has a `## [[Store]]` section with a `- [x] shopping` line further down the note.

Never touch that section checkbox for this task; it is not the shopping list marker.

### Step 1 — find the product note

Follow Steps 1 to 3 of the resolve-recipe-ingredient-link skill, using the product as the user phrased it in place of the link text.

For Tier 2, the disambiguators come from the user's own wording (for example "flat leaf" or "dried"), since there is no recipe line.

When several notes match and the user named no variant, prefer the general note that the variants link from, and the one that holds past `✅` dated shopping lines.

Example: "parsley" resolves to `parsley.md`, not `fresh parsley.md`, `flat leaf parsley.md` or `dried parsley.md`, because `parsley.md` links to those variants and holds the purchase history.

When the user named a variant, use the variant's note.

### Step 2 — create the note when no candidate fits

If no existing note is a plausible match, create one by following Tier 4 of the resolve-recipe-ingredient-link skill.

Name the file after the product as the user said it, all lowercase with spaces between words.

Before writing, check that no note with the same name exists with different capitalization, because a lowercase write onto a capitalized note keeps the old name and `git add` then does nothing.

### Step 3 — set the store key

Match the store the user named to one of the keys already in the note's front matter.

When the user names no store, use `amazon_fresh`.

Amazon Fresh has closed, so its key serves as the catch-all list for items not yet assigned to a store.

Do not ask which store in that case.

The keys are snake_case forms of the store note names with punctuation dropped, for example `trader_joes` for Trader Joe's, `lam_s_seafood_asian_market` for Lam's Seafood Asian Market, and `amazon_com` for Amazon.com.

Change only that key from `false` to `true`, leaving every other line as it is.

If the key is already `true`, the product is already on the list; report that and change nothing.

If the store matches no key, stop and ask the user, because adding a key would invent a store without a store note to back it.

### Step 4 — commit

Background processes commit to the vault too, so commit only the product note by path:

```sh
git commit --message "Add <product> to the <store> shopping list" -- "<product>.md"
```

For a newly created note, run `git add "<product>.md"` first.

### Step 5 — report

Name the note that was changed or created, and the key that was set.

When the store defaulted to `amazon_fresh`, say that it went on the no-store list.

When a variant note was passed over in favor of the general note, say so in one line, so the user can redirect.
