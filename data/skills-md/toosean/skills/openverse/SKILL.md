---
name: openverse
description: Search Openverse API for openly licensed images and audio using OAuth credentials. Use when Codex needs to find image assets, photos, illustrations, artwork, sound effects, music, audio clips, license details, attribution text, source links, thumbnails, waveforms, media details, or related Openverse results.
---

# Openverse

Search Openverse for images and audio, returning links, source pages, license metadata, and attribution text.

## Workflow

1. Require OAuth credentials before searching.
Use environment variables:
- `OPENVERSE_CLIENT_ID`
- `OPENVERSE_CLIENT_SECRET`

Do not fall back to anonymous requests. If credentials are missing, ask the user to configure them or provide credentials through the environment.

2. Use the bundled CLI for repeatable searches:

```powershell
python openverse/scripts/openverse_search.py search --media image --query "red fox" --page-size 5 --format markdown
python openverse/scripts/openverse_search.py search --media audio --query "rain ambience" --page-size 5 --format markdown
```

3. Default to search only; do not download source media unless the user explicitly asks for a download workflow.

4. Always surface license information.
For each useful result, include:
- title
- creator
- provider/source
- media URL
- landing page URL
- license and license URL
- attribution text

5. If the user needs commercial or modification-safe media, filter with Openverse parameters rather than guessing:

```powershell
python openverse/scripts/openverse_search.py search --media image --query "office" --license-type commercial --format markdown
python openverse/scripts/openverse_search.py search --media audio --query "button click" --license cc0 --format markdown
```

## CLI Commands

Search:

```powershell
python openverse/scripts/openverse_search.py search --media image --query "mountain lake"
python openverse/scripts/openverse_search.py search --media audio --query "footsteps"
```

Detail:

```powershell
python openverse/scripts/openverse_search.py detail --media image --id "<openverse-id>" --format markdown
python openverse/scripts/openverse_search.py detail --media audio --id "<openverse-id>" --format markdown
```

Related:

```powershell
python openverse/scripts/openverse_search.py related --media image --id "<openverse-id>" --page-size 5 --format markdown
python openverse/scripts/openverse_search.py related --media audio --id "<openverse-id>" --page-size 5 --format markdown
```

The default output format is raw JSON. Use `--format markdown` when the user wants a concise result list.

## Search Guidance

- Keep queries short and literal.
- Prefer `--license-type commercial` for commercial-use requests.
- Prefer `--license cc0` when the user wants the least restrictive results.
- Use `--source` only when the user names a specific provider or a prior result shows a good source.
- For image-specific filtering, use `--category`, `--aspect-ratio`, and `--size`.
- For audio-specific filtering, use `--category`, `--length`, and `--extension`.

## References

Read `references/openverse-api.md` when you need endpoint details, supported parameters, OAuth behavior, or response fields.

## Troubleshooting

- `Missing OPENVERSE_CLIENT_ID or OPENVERSE_CLIENT_SECRET`: configure OAuth credentials first.
- `invalid_client`: check the client ID and client secret.
- `429 Too Many Requests`: reduce request volume or wait for the rate limit window.
- Poor results: shorten the query, remove over-specific filters, or try tags/title/creator filters.
- License uncertainty: use the Openverse `license_url`, landing page, and attribution text; do not assume commercial permission from title or source alone.
