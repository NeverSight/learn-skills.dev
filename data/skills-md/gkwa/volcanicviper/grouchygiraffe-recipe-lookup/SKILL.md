---
name: grouchygiraffe-recipe-lookup
description: Given a grouchygiraffe media file path, find the associated YAML, identify the recipe from the thumbnail, locate the author's home base, and return the recipe URL. Use when the user provides a path to a grouchygiraffe .mp4 or .jpg file and wants to know what recipe it is and where to find it.
---

## Recipe Lookup from Grouchygiraffe Media File

Given a path like `/Users/mtm/pdev/taylormonacelli/grouchygiraffe/data/DX9oSBkjsZR.mp4`, identify the recipe and find its URL on the author's site.

### Step 1: Derive the shortcode and sibling paths

The shortcode is the filename without its extension.

Given `/path/to/data/DX9oSBkjsZR.mp4`:

- Shortcode: `DX9oSBkjsZR`
- YAML: `/path/to/data/DX9oSBkjsZR.yaml`
- Thumbnail: `/path/to/data/DX9oSBkjsZR_thumb.jpg`

### Step 2: Read the YAML file

Use the Read tool on the YAML file. Extract:

- `uploader` — the author's display name (e.g., "Tom Walsh")
- `title` — contains the Instagram handle in the form "Video by <handle>" (e.g., `stealth_health_life`)
- `url` — the original Instagram post URL
- `description` — the post caption, which may contain the recipe directly (check this first before proceeding)

If `description` is non-null and contains a recipe, you may be able to skip steps 3 and 4.

### Step 3: Read the thumbnail to identify the recipe

Use the Read tool on the `_thumb.jpg` file — Claude can read images directly.

The thumbnail often has the recipe name as a text overlay.

Note the recipe name exactly as it appears in the image.

### Step 4: Find the author's home base

If the author's website is not already known, search for it:

```
WebSearch: <instagram_handle> Instagram <uploader_name>
```

Look for a personal website, Substack, or cookbook site in the results.

### Step 5: Search for the recipe on the author's site

Use the recipe name from the thumbnail and search the author's site:

```
WebSearch: site:<author_site> "<recipe name>"
```

If that returns nothing, try a broader search:

```
WebSearch: <instagram_handle> "<recipe name>" recipe ingredients
```

Also try fetching the author's recipes page directly with WebFetch if a URL is known.

### Step 6: Return the recipe URL

Report:

- The recipe name (from the thumbnail)
- The author's name and Instagram handle
- The author's home base URL
- The original Instagram post URL (from the `url` field in the YAML)
- The direct recipe URL (on their site, TikTok, or Substack)
- A summary of the recipe if ingredients were found

If the recipe is only on TikTok or Substack and the full ingredients are in the search snippet, include them in the response.
