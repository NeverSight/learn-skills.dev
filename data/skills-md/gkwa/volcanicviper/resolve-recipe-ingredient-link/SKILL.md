---
name: resolve-recipe-ingredient-link
description: "Find the correct note to resolve an unresolved ingredient wikilink in a recipe note. Use when an ingredient wikilink like [[leeks]] in a recipe does not resolve to an existing note and you need to find the best matching product note to point it at. Uses islandiguana to enumerate product-tagged candidate notes, then semantically ranks the full list against the link text and its surrounding recipe ingredient line."
---

## Resolving an unresolved Obsidian wikilink

Given an unresolved wikilink (e.g. `[[leeks]]`), find the existing note that best matches it.

Binary: `/Users/mtm/go/bin/islandiguana`

Vault path: `/Users/mtm/Documents/Obsidian Vault`

### Method

The link text is the bare name inside the brackets (e.g. `leeks` from `[[leeks]]`).

For a piped wikilink (`[[leek|leeks]]`), the link text is the part before the `|`.

Step 1 — enumerate candidates.

Resolution candidates live among notes tagged `product`.

```sh
islandiguana "/Users/mtm/Documents/Obsidian Vault" '.tags[] == "product"'
```

Step 2 — read the full candidate list and rank it semantically.

Read every filename islandiguana returned and rank the whole list against the link text.

Do not pre-filter the list with a keyword search.

The match is semantic, not lexical — a keyword filter would discard good candidates the keywords failed to anticipate (a note named `wild ramps.md` resolves `[[leeks]]` even though it shares no letters with "leek").

The product pool is currently around 1,300 notes, which is small enough to read in full in a single pass.

Step 3 — resolve using a three-tier rule.

Tier 1 — near-exact name match.

If a candidate matches the link text exactly, or differs only by singular/plural, resolve to it.

Example: `leek.md` resolves `[[leeks]]`.

Tier 2 — disambiguate with the source line.

If no near-exact match exists, read the full line containing the wikilink in the source note, not just the bracketed text.

The descriptive words to the left of the linked noun are the disambiguators.

Example: the line `2 teaspoons whole black [[peppercorns]]` carries "black" and "whole", so the target is "whole black peppercorns", which resolves to `black peppercorn.md` rather than the literal-string match `sichuan peppercorns.md`.

Tier 3 — ask the user.

If the source line still does not settle the choice (e.g. `[[peppercorns]] to taste` names no type), report the candidates and ask the user to choose.

Tier 4 — create a new product note.

If no existing candidate is a plausible resolution at all, do not force a wrong match and do not leave the link dangling.

Create a new product note named after the link text so the wikilink resolves, following the product-note pattern below.

A near-miss substitution does not count as a resolution: `feta cheese` is not `cotija cheese`, and resolving one to the other is wrong even though both are crumbly cheeses.

Prefer a fresh note over a substitution whenever the ingredient is a distinct product.

The new note's filename is the bare link text with the same casing rules as other vault notes (all lowercase, spaces between words), e.g. `[[cotija cheese]]` becomes `cotija cheese.md`.

Use the following template, copying the store-boolean frontmatter and store sections verbatim from any existing product note (e.g. `habanero peppers.md`) so the new note matches the vault's structure exactly.

Set the `tags` to `product` plus a single category tag for the ingredient (e.g. `dairy`, `vegetable`, `spice`).

Include a Google image search link as the product reference, since a fresh note has no purchase page yet.

Omit the `pic` frontmatter field and the hero image unless a verified image URL is available, to avoid a broken link.

```
---
albertsons: false
amazon_com: false
amazon_fresh: false
central_co_op: false
chef_s_store: false
costco: false
dong_hing_market: false
east_african_imports_restaurant: false
franz_bakery: false
fred_meyer: false
grocery_outlet: false
h_mart: false
hau_hau_market: false
home_depot: false
india_depot_indian_grocery_kitchen_bakery: false
lam_s_seafood_asian_market: false
lowe_s: false
m2m: false
pacific_supply: false
pcc: false
public_storage: false
qfc: false
safeway: false
tags:
- product
- <category>
target: false
than_son_tofu_and_bakery: false
trader_joes: false
uwajimaya: false
walgreens: false
walmart: false
whole_foods: false
---

<Product Name>


Google image search: https://www.google.com/search?q=<product+name>&tbm=isch

## [[Amazon.com]]
- [x] shopping

## [[Central Co-op]]
- [x] shopping

## [[Grocery Outlet]]
- [x] shopping

## [[Chef's Store]]
- [x] shopping

## [[Hau Hau Market]]
- [x] shopping

## [[Lam's Seafood Asian Market]]
- [x] shopping

## [[M2M]]
- [x] shopping

## [[Pacific Supply]]
- [x] shopping

## [[PCC]]
- [x] shopping

## [[QFC]]
- [x] shopping

## [[Safeway]]
- [x] shopping

## [[Target]]
- [x] shopping

## [[Trader Joes]]
- [x] shopping

## [[Uwajimaya]]
- [x] shopping

## [[Walgreens]]
- [x] shopping

## [[Walmart]]
- [x] shopping

## [[Whole Foods]]
- [x] shopping

## [[Costco]]
- [x] shopping

## [[Fred Meyer]]
- [x] shopping

## [[H Mart]]
- [x] shopping

## [[Dong Hing Market]]
- [x] shopping

## [[Amazon Fresh]]
- [x] shopping

## [[Home Depot]]
- [x] shopping

## [[Franz Bakery]]
- [x] shopping

## [[Lowe's]]
- [x] shopping

## [[Than Son Tofu and Bakery]]
- [x] shopping

## [[India Depot Indian Grocery, Kitchen & Bakery]]
- [x] shopping

## [[Albertsons]]
- [x] shopping

## [[East African Imports & Restaurant]]
- [x] shopping

## [[Public Storage]]
- [x] shopping
```

Step 4 — report.

Report the number of candidates considered and the resolution, the ranked shortlist when asking the user, or the new product note created when no candidate matched.

Do not edit the wikilink unless explicitly asked — surface the resolution first.

### Writing the resolved link

When asked to apply the resolution, choose the link form by comparing the displayed word (the original link text, e.g. `leeks`) against the resolved note name (e.g. `leek`).

Never use the alias form (`[[note|displayed]]`) in an ingredient link.

When the displayed word and the note name differ, rewrite the recipe text to match the note name and keep a plain link, rather than papering over the mismatch with an alias.

Keeping the inflection outside the brackets is fine; an alias is not.

This extends to heading links, not just ingredient links.

For a link to a heading in the same note, use the alias-free relative form `[[#Heading]]` rather than `[[note#Heading|Display]]`.

The rule is firm: never introduce an alias, even when an AskUserQuestion option text proposes one.

Decide in this order:

Case 0 — absorb an adjacent disambiguator first.

If the resolution used Tier 2 — a descriptive word on the source line, outside the brackets, is what picked the note — and that word sits directly adjacent to the wikilink, pull it inside the brackets before comparing.

Then run the comparison below on the expanded phrase, not on the bare bracket text.

Example: line `2 teaspoons whole black [[peppercorns]]`, note `black peppercorn`.

The Tier 2 disambiguator "black" sits just left of the link, so the displayed phrase expands from `peppercorns` to `black peppercorns`.

The note name is now a prefix of that phrase, so the link is written `[[black peppercorn]]s`, and the adjacent `black` is consumed into it — the line reads `2 teaspoons whole [[black peppercorn]]s`.

This beats stranding the disambiguator as `black [[black peppercorn|peppercorns]]`, which leaves "black" outside the brackets and duplicates the word the note name already carries.

The principle: the word you used to disambiguate in Tier 2 belongs inside the link text, not orphaned beside an alias.

Case 1 — the displayed word equals the note name.

Write a plain link with no alias and no suffix.

Example: displayed `leek`, note `leek` becomes `[[leek]]`.

Case 2 — the note name is a prefix of the displayed word.

Keep the note name in the brackets and place the leftover suffix outside.

Example: displayed `leeks`, note `leek` becomes `[[leek]]s`.

Example: displayed `boxes`, note `box` becomes `[[box]]es`.

Case 3 — the note name is not a prefix of the displayed word.

The stem changes, so no suffix can be peeled off. Do not use an alias.

Instead, rewrite the recipe text to the note's word and use a plain link, adjusting the surrounding wording so the line reads naturally.

Example: displayed `leaves`, note `leaf` becomes `[[leaf]]` — change the line so it reads with "leaf" rather than stranding `[[leaf|leaves]]`.

If rewording the line to the note's word would read awkwardly, prefer creating or choosing a note whose name matches the ingredient as written over falling back to an alias.

### Notes

Always quote the vault path — it contains spaces.
