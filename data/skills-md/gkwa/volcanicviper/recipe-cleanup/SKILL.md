---
name: recipe-cleanup
description: Reformat a recipe file using consistent style rules. Use when the user wants to clean up or standardize a recipe note in the vault, or create a new recipe note from a URL.
---

## Recipe Cleanup

Parse the input: the first argument is either a local recipe file path or a URL to a recipe page. The optional second argument is the source URL for the original recipe. Any remaining text after the URL or file path is treated as inline recipe content (ingredients, instructions, notes).

Determine the input mode from the first argument:
- If it starts with `http://` or `https://`, treat it as a URL — fetch the page to extract the recipe content, and treat that URL as the implicit source URL (unless a second argument overrides it)
  - **YouTube watch URLs** (`youtube.com/watch?v=VIDEO_ID`): extract the video ID and set the thumbnail to `https://i.ytimg.com/vi/VIDEO_ID/hq720.jpg`, then attempt to retrieve the description using the following fallback sequence:
    1. Try WebFetch on the YouTube URL first — if it returns usable description content, use that
    2. If WebFetch fails or returns no description, fall back to Playwright: navigate to the page, wait 3 seconds for it to load, then click the "...more" button to expand the full description
    3. Once the description is obtained (by either method), scan it for recipe content:
       - **Recipe in description**: if the description contains ingredients or instructions directly, use that as the recipe content
       - **Link in description**: if the description contains a link to an external recipe page (e.g. a blog post or dedicated recipe URL), fetch that URL using WebFetch and extract the recipe from there instead; record both the YouTube URL and the recipe page URL — both will appear in the output file
       - **Inline text fallback**: if neither is found in the description, fall back to any inline text provided in the arguments
    4. Use the channel name and video title to identify the creator
- Otherwise, treat it as a local file path — read the file

**Creator identification from channel URL:**
- If any argument is a YouTube channel URL (e.g., `youtube.com/@Handle` or `youtube.com/c/name`), try to fetch that page to extract the creator's real name
- If the fetch fails, derive the name from the handle by splitting on capitalisation (e.g., `@FastEasyRecipes` → `Fast Easy Recipes`)
- Use that name in the `creator` frontmatter field

Apply the formatting rules below to the recipe content.

**Frontmatter:**
- Generate YAML frontmatter at the top of the file (before the source URL line) with these fields:
  ```
  ---
  creator: '[[Author Name]]'
  pic: <hero-image-url>
  tags:
  - recipe
  - <creator tag>
  ---
  ```
- The creator tag is the resolved page name lowercased with all spaces and separators removed (e.g., `Andrea Geary` → `andreagreary`, `budgetbytes` → `budgetbytes`, `Fast Easy Recipes` → `fasteasyrecipes`)
- Extract the author/creator name from the recipe page (e.g., from the recipe card's author field or the blog's about page)
- Resolve the creator's page name using this priority order:
  1. If the recipe comes from the author's own personal domain, use the domain name without TLD as the page name (e.g., `budgetbytes.com` → `budgetbytes`, `halfbakedharvest.com` → `halfbakedharvest`). This is their chosen vanity identity.
  2. If the recipe comes from a major publication (e.g., Bon Appétit, Serious Eats, NYT Cooking, Food Network, Epicurious, Tasty), use the author's name as credited on that publication — the content belongs to the publication, not the individual's personal brand.
  3. If there is no personal domain (e.g., YouTube-only creators), use the author's real name.
- Use the resolved page name in the `creator` frontmatter wikilink (e.g., `[[budgetbytes]]`)
- After writing the file, check whether a page named `<page name>.md` exists in the same directory as the recipe file — if it does not exist, create a minimal stub: a file containing `# <page name>` followed by a blank line and the author's source URL (e.g. their YouTube channel URL, website, or wherever the recipe came from)

## Formatting rules

**Ingredients:**
- Format every ingredient line as a checked checkbox: `- [x] quantity [[ingredient name]]`
- Wrap the ingredient name (not the quantity or descriptors) in Obsidian wikilinks: `[[ingredient name]]`
- Ensure the wikilink covers the entire product name to link to the corresponding product page in the repository
  - Example: `1 cup julienned carrots` → `- [x] 1 cup julienned [[carrots]]`
  - Example: `2 teaspoons sesame oil` → `- [x] 2 teaspoons [[sesame oil]]` (not `sesame [[oil]]`)
- If the ingredient already has a wikilink, leave it as-is
- After the file is written, resolve every ingredient wikilink that does not point to an existing note — see the "Resolving ingredient wikilinks" section below

**Resolving ingredient wikilinks:**
- After the cleaned file is written, every ingredient name is wrapped in a `[[wikilink]]` — but many of those will not point to an existing product note in the vault
- Do not invent or hand-craft a resolution; delegate to the `resolve-recipe-ingredient-link` skill, which is the single canonical resolver
- For each ingredient wikilink whose target note does not already exist in the vault (resolved by basename, the way Obsidian resolves links), invoke `resolve-recipe-ingredient-link` to find the best matching product note and rewrite the link to its resolved form
- Pass the resolver the full ingredient line as context, not just the bare bracket text — the descriptive words around the linked noun are what disambiguate the match
- Enumerate the candidate product notes once and resolve all unresolved links for the recipe against that single list, rather than re-enumerating per ingredient
- A wikilink that already resolves to an existing note is left untouched
- If the resolver cannot settle a link from the ingredient line alone, follow its three-tier rule — surface the shortlist and ask the user rather than forcing a wrong match

**Instructions:**
- Never capitalize the first letter of an instruction line (lowercase start)
- Do not end any instruction with a period
- Each sentence is its own paragraph — split multi-sentence instructions into individual sentences, each separated by a blank line
- Remove any bold, italics, or emphasis formatting — plain text only
- Always use plain paragraphs for instructions — if the original uses a numbered/ordered list, convert each item to a plain paragraph
- If a step lists multiple items in a comma-separated sequence (e.g., "add onions, oil, butter, and salt"), expand that list into a Markdown bullet sub-list, keeping the surrounding sentence intact:

  Example input:
  ```
  add onions, oil, remaining butter, salt and pepper to pan
  ```
  Example output:
  ```
  add

  - onions
  - oil
  - remaining butter
  - salt
  - pepper

  to pan
  ```

**Mise en place:**
- Mise en place — "everything in its place" — is the practice of completing all preparation before cooking begins, so that execution runs uninterrupted
- The principle: decouple preparation from execution; a cook who is still slicing while the pan is hot will burn both the food and their focus
- Extract all prep-type steps from the instructions and place them in a `## Mise en Place` section immediately above the first cooking section — rename any existing `## Prep` section to `## Mise en Place`
- Prep steps include any task that can be completed before heat or timing begins: chopping, dicing, mincing, slicing, peeling, measuring, soaking, washing, resting dough, bringing ingredients to room temperature, preheating, etc.
- When a recipe has distinct cooking phases (e.g. making a broth, making a sauce, preparing a filling), give each phase its own named section (e.g. `## Broth`, `## Sauce`) rather than collapsing everything into a single `## Instructions` section — this applies the mise en place principle at the phase level, not just the ingredient level
- Reserve `## Instructions` for final assembly steps only
- Format each prep step as a plain paragraph (no leading bullet), separated by blank lines — same structure as instructions
- If a prep step involves multiple constituent items, keep the action as a plain paragraph and list the items as a bullet sub-list beneath it (same comma-expansion rule as instructions)
- Apply the same instruction formatting rules: lowercase start, no trailing period
- Remove extracted steps from the cooking sections — do not duplicate them
- If a `## Mise en Place` section already exists, merge any newly extracted steps into it

**Dish image:**
- Find the main hero image for the recipe (e.g., from og:image meta tag or the primary recipe photo)
- Place it as an inline markdown image immediately after the frontmatter block, before the source URL: `![dish name](image-url)`
- If an image is already present at that position, leave it as-is

**Nutrition section:**
- Remove the Nutrition section entirely if present

**YouTube links:**
- Convert any long YouTube URLs to short format: `https://youtu.be/VIDEO_ID`
  - Example: `https://www.youtube.com/watch?v=abc123` → `https://youtu.be/abc123`
  - Example: `https://www.youtube.com/watch?v=abc123&t=45s` → `https://youtu.be/abc123?t=45`
- Keep existing short `youtu.be` URLs as-is
- If a YouTube video ID is present and the file has a `pic` frontmatter field, verify the thumbnail URL before using it: run `curl -s -o /dev/null -w "%{http_code}" URL` on `hq720.jpg` first — if it returns 200 use it; if it returns 404 fall back to `hqdefault.jpg`

**Timestamps:**
- If an instruction references a video timestamp in `[MM:SS]` format with an associated YouTube URL, convert it to an absolute markdown link using the `?t=` parameter in seconds
  - Example: `[00:17]` with video `https://youtu.be/Wnt90dkEwFs` → `[00:17](https://youtu.be/Wnt90dkEwFs?t=17)`
  - Example: `[01:05]` → `?t=65`
- The link text should be the timestamp in `[MM:SS]` format
- If no YouTube URL is available for a timestamp, leave it as plain text

## Example output

```
crack the eggs into a bowl, see [00:05](https://youtu.be/Wnt90dkEwFs?t=5)

whisk until fully combined

pour into a heated, greased pan, see [00:17](https://youtu.be/Wnt90dkEwFs?t=17)

cook until edges begin to set
```

## Steps

1. Determine input mode from the first argument (URL vs file path)
2. Fetch or read the recipe content accordingly; extract the author name and hero image URL
3. Apply all formatting rules to the recipe content — convert instruction ordered lists to plain paragraphs; apply instruction-specific rules (lowercase, no trailing period, sentence splitting) only to instruction lines
4. Place YAML frontmatter at the very top of the file with `creator`, `pic`, and `tags`
5. Place the hero image immediately after the frontmatter block, then the source URL(s) on the next line(s), followed by a blank line — if a source URL already exists, replace it; if the recipe was fetched from an external page linked in a YouTube description, place the YouTube URL first and the recipe page URL on the line below it
6. Do not include a `# Title` heading — the filename serves as the page title in Obsidian
7. For file mode: overwrite the file with the cleaned content and confirm success — do not output the full recipe content to the chat
8. For URL mode: display the formatted recipe in the chat, then immediately write it to a file without asking — derive the filename from the recipe title using spaces (not hyphens) with a `.md` extension; when the creator is known, prefix the filename with the creator name to avoid collisions between recipes with the same dish name (e.g., `Fast Easy Recipes crepes.md`); save to the same directory as other recipe files in the vault
9. After writing the file, check whether the creator's page exists in the same directory — if not, create a stub page named `<page name>.md` containing just `# <page name>` (using the resolved page name from the frontmatter rules above)
10. After writing the file, resolve unresolved ingredient wikilinks by delegating to the `resolve-recipe-ingredient-link` skill — see the "Resolving ingredient wikilinks" formatting rule above

## Creator Namespace

Derive a creator's namespace from their handle or personal domain, collapsed to lowercase letters and digits only.

Use that single token in all three places: the `creator` frontmatter wikilink, the `tags` entry, and the stub page filename.

Instagram handle `chef.sam.black` becomes `chefsamblack` everywhere — `[[chefsamblack]]`, tag `chefsamblack`, file `chefsamblack.md`. Personal domain `halfbakedharvest.com` becomes `halfbakedharvest`.

Tags cannot contain dots, spaces, or other separators, and real names collide, so the collapsed handle gives a unique separator-free namespace that works as tag, wikilink, and filename at once.

Fall back to a real name, also collapsed, only when no handle or domain exists.

Existing vault precedent: `pantrymama`, `thesaltymarshmallow`, `ediblealchemyacademy`, `allrecipes`.
