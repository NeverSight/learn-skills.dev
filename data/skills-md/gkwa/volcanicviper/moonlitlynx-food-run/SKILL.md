---
name: moonlitlynx-food-run
description: Tag untagged/undated food-related media in the digikam grouchygiraffe and shamblingshark collections. Use when asked to tag untagged food files, run a moonlitlynx food tagging pass, or process the digikam untagged or undated queue.
---

## What This Skill Does

Finds media files that match digikam's "untagged or undated" saved search within the grouchygiraffe and shamblingshark collections, reads their YAML metadata, classifies food vs. non-food content, and applies the appropriate digikam tags.

Always report what you find before applying any tags.

## Database

Path: `~/Pictures/digikam4.db`

Back up before every run:

```sh
cp ~/Pictures/digikam4.db ~/Pictures/digikam4.db.bak.$(date +%Y%m%d_%H%M%S)
```

## Finding the Files

The digikam saved search "untagged or undated" (id=42) translates to this SQL.

Both conditions must be true (AND, not OR):

```sql
SELECT i.name, ar.label
FROM Images i
JOIN Albums al ON al.id = i.album
JOIN AlbumRoots ar ON ar.id = al.albumRoot
LEFT JOIN ImageInformation ii ON ii.imageid = i.id
WHERE ar.label IN ('grouchygiraffe', 'shamblingshark')
AND i.id NOT IN (
  SELECT imageid FROM ImageTags
  WHERE tagid NOT IN (SELECT id FROM Tags WHERE name LIKE 'Color Label%')
)
AND (ii.creationDate IS NULL OR ii.creationDate < '1904-01-01T00:00:00')
ORDER BY ar.label, i.name;
```

The `Color Label%` exclusion is required — files with only a color label tag are treated as untagged by digikam's UI.

## Reading YAML Files

For grouchygiraffe files: `/Users/mtm/pdev/taylormonacelli/grouchygiraffe/data/<shortcode>.yaml`

Strip the file extension to get the shortcode (e.g. `DZY_GI9tCs5.mp4` → `DZY_GI9tCs5.yaml`).

Shamblingshark files in `/output` are UUID-named and have no YAML counterparts — skip classification, apply `noyamldesc`.

Read `uploader`, `title`, and `description` fields from each YAML.

## Classification

**Food** — apply `food` (id=109) plus any matching subtags:

| keyword pattern | subtag | digikam id |
|---|---|---|
| sourdough, levain, batard, boule, bulk ferment, crumb | sourdough | 113 |
| salsa, enchilada sauce, tomatillo, salsa verde, salsa roja | salsa | 115 |
| pepper, chile, jalapeño, chipotle, guajillo, cayenne | peppers | 151 |
| curry, masala, tikka, korma, biryani, desi, indian | indian | 114 |
| paneer | paneer | 123 |
| soup, stew, broth, ramen | soup | 153 |
| bean, lentil, chickpea | beans | 133 |
| tomato | tomato | 131 |
| coffee, espresso, barista | coffee | 130 |
| dumpling, potsticker, gyoza | dumpling | 233 |
| vegan, plant-based | vegan | 234 |
| pizza, pasta, focaccia, ciabatta, bread, loaf | pizza (pizza) or food only (bread) | 235 |
| mushroom | food only (no subtag exists) | — |
| honey | honey | 156 |

Match against the lowercased `description` and `uploader` fields.

Apply `food` even when no subtag matches — `food` is the base tag for all food content.

**Probably food / empty description** — apply `food` + `noyamldesc` when the YAML description is empty or null but the uploader username strongly implies food content (e.g. `eatinghealthytoday`, `thesourdoughnerd`, `katrina.the.earthy.vegan`, `myhealthydish`).

**No signal** — apply only `noyamldesc` when description is empty and uploader gives no food signal (e.g. `stealth_health_life` with no description, generic lifestyle accounts).

**Non-food** — skip entirely. Do not apply any tags. Examples: fitness/mobility, fashion, political, medical, humor, lifestyle.

## Special Tag: noyamldesc

`noyamldesc` (id=242, pid=0) marks files whose YAML has no useful description, making classification impossible.

Apply it alongside `food` when the username suggests food content, or alone when there is no content signal at all.

Always pair with `ai-tagged`.

## Tag IDs Quick Reference

| tag | id | pid |
|---|---|---|
| food | 109 | 0 |
| sourdough | 113 | 109 |
| salsa | 115 | 109 |
| indian | 114 | 109 |
| paneer | 123 | 109 |
| peppers | 151 | 109 |
| soup | 153 | 109 |
| tomato | 131 | 109 |
| beans | 133 | 109 |
| coffee | 130 | 0 |
| honey | 156 | 109 |
| dumpling | 233 | 109 |
| vegan | 234 | 109 |
| pizza | 235 | 109 |
| ai-tagged | 192 | 0 |
| noyamldesc | 242 | 0 |

## Applying Tags

Use `INSERT OR IGNORE` — the ImageTags table has a UNIQUE constraint on (imageid, tagid).

Look up image IDs by filename scoped to the correct album root:

```sql
SELECT i.id FROM Images i
JOIN Albums al ON al.id = i.album
JOIN AlbumRoots ar ON ar.id = al.albumRoot
WHERE ar.label = 'grouchygiraffe' AND i.name = 'DZY_GI9tCs5.mp4';
```

Or batch by name with subqueries in a single transaction:

```sql
BEGIN;
INSERT OR IGNORE INTO ImageTags (imageid, tagid)
SELECT i.id, 192 FROM Images i
JOIN Albums al ON al.id = i.album
JOIN AlbumRoots ar ON ar.id = al.albumRoot
WHERE ar.label IN ('grouchygiraffe', 'shamblingshark')
AND i.name IN ('DZY_GI9tCs5.mp4', ...);
COMMIT;
```

Scoping inserts by `ar.label` avoids tagging duplicate filename entries from other collections.

## Workflow

1. Back up the database.
2. Run the untagged/undated query and report the file count.
3. Read YAML for each file and classify: food, probably-food, no-signal, or non-food.
4. Present findings to the user before applying any tags. Show: shortcode, content summary, proposed tags.
5. On confirmation, apply tags in a single transaction.
6. Verify counts by checking `SELECT t.name, COUNT(*) FROM ImageTags it JOIN Tags t ON t.id = it.tagid JOIN Images i ON i.id = it.imageid WHERE i.name IN (...) GROUP BY t.name`.
7. Update `moonlitlynx progress.md` in the Obsidian vault with the run summary.
8. Commit the progress note.

## Progress Note

Progress is tracked in `/Users/mtm/Documents/Obsidian Vault/moonlitlynx progress.md`.

After each run, add a dated section under `## Food/recipe batch tag run` documenting:

- File count found and tagged
- New tags created (if any)
- Breakdown of subtags applied
- Files skipped and why
