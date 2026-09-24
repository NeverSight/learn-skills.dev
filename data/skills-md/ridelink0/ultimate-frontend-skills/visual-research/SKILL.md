---
name: visual-research
description: Use when a question is better answered by looking than by reading - researching how websites or apps look, gathering design references, finding what a style or palette or typeface actually is in the wild, comparing competitors visually, or building a moodboard. Renders real sites and searches real images, then reads them as pictures.
---

# Visual research

Most design questions are answered by looking at twenty examples, not by
reading one article about them. This gets the pictures in front of you cheaply.

## Render real sites - the highest-signal source

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/webdesign.mjs" study <url> <url> ...
node "${CLAUDE_PLUGIN_ROOT}/scripts/webdesign.mjs" study --list editorial
```

Renders each site at the top and one screen down in a real headless browser
and tiles them into contact sheets - eight references become one image to
read. Curated lists: `editorial`, `object`, `cinema`, `product`.

**Read the contact sheet first**, then the individual PNGs only for the two or
three worth a closer look. A sheet is roughly eight times cheaper than eight
reads.

Two things it cannot see, and it says so: WebGL sites render only their
preloader, and Cloudflare-walled ones show a challenge page. For those, use the
`-y900` tile (usually below any cookie modal) or find a video walkthrough.

## Find images on the open web

Free and no key needed:

| Source | Endpoint | Note |
|---|---|---|
| Openverse | `https://api.openverse.org/v1/images/?q=<q>` | ~600M CC images, no key for light use |
| Wikimedia Commons | `https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrnamespace=6&gsrsearch=<q>&prop=imageinfo&iiprop=url&format=json` | canvas-safe, CORS `*` |
| Art Institute of Chicago | `https://api.artic.edu/api/v1/artworks/search?q=<q>` then the IIIF URL | 60 req/min, CORS `*` |
| Met Museum | `https://collectionapi.metmuseum.org/public/collection/v1/search?q=<q>` | no key |

Unsplash and Pexels need a free key for their APIs, but their CDN URLs can be
hotlinked directly once you have an id. Verify every URL with a HEAD request
before shipping it - `look` reports images that failed to load, but only after
the fact.

## Design galleries, for finding sites worth rendering

Awwwards, Godly, Land-book, SiteInspire, Minimal Gallery, Curated.design,
One Page Love. Fetch the gallery page, extract the outbound site URLs, then
`study` them. The gallery's own thumbnails are small and colour-shifted -
render the real thing instead.

## Reading what you got

Go in with a question. "What do these have in common" produces mush; "where
does the eyebrow sit relative to the headline, and at what size" produces a
number you can build with.

Worth extracting every time: the type pairing and sizes, the ground colours,
where the accent appears, section rhythm, what the first screen does, and the
one move you have not seen before.

Palette straight off a rendered page:

```bash
node -e "import('./scripts/inspect.mjs').then(async m=>{
  const r = await m.inspect('https://example.com',{widths:[1440],out:'./shots'});
  console.log(JSON.stringify(r[0].stats));
})"
```

## Do not

Do not describe an image you have not read. Do not treat a gallery thumbnail as
evidence of colour. Do not conclude a site uses a library because the effect
looks like it - check the bundle. And say plainly when a render is a wall or a
preloader rather than guessing what is behind it.
