---
name: media-use
description: Resolve reviewed local BGM, sound effects, images, icons, and brand assets into frozen project files plus a manifest. Use when a HyperFrames composition needs non-voice media that is already supplied, staged under assets/, present in the trusted local cache, or explicitly selected from a local review catalog after discovery and audition.
---

# media-use

Turn an approved local asset into a stable project path and ledger record. This skill is an inventory and ingestion layer: it performs no web search, download, media generation, or voice synthesis.

For revisioned audition decisions, generated images/video, derivatives and the distinction between a reviewed asset and one actually used in a release, read [review and derivative provenance](references/review-and-derivatives.md). Keep those editorial records alongside the resolver manifest; do not pretend its existing flags implement a full editorial state machine.

Voice is outside this resolver. [`fish-audio-api`](../fish-audio-api/SKILL.md) is the bundled synthesis adapter. Respect supplied narration or a user-selected provider; prepare that audio through its supported route, then import the resulting local narration file and measured timing into the composition.

## Public package setup

No media recordings, author library, review database or cache is included. Supply your own reviewed files and rights records. A new project can begin with an empty library; discovery may return no results. Use explicit `--source` ingestion when you already have a permitted file.

The project wrapper finds `.agents/skills/media-use` or the directory named by `MEDIA_USE_SKILL_DIR`. Its optional `MEDIA_CATALOG` points to a catalog within the project/workspace; `--catalog` overrides it. The resolver's optional `MEDIA_USE_GLOBAL_CACHE_DIR` selects a user-owned cache. These paths are configuration, not assets supplied by this release. Standalone resolver/catalog commands read environment variables; the scaffolded wrapper additionally reads the project `.env`.

## Resolve

```bash
node <SKILL_DIR>/scripts/resolve.mjs --type <type> --intent "<description-or-id>" --project <dir>
```

Types: `bgm`, `sfx`, `image`, `icon`, and the local-only `brand` record.

For `brand`, a local `frame.md`, `FRAME.md`, `design.md`, or `DESIGN.md` can be frozen as the design record. Flat YAML frontmatter is retained when present; a plain Markdown design document is still a valid local record.

Resolution is deterministic and local:

1. Reuse a valid project-manifest record matching the requested id, path, exact prompt, or entity.
2. Adopt a matching unregistered file from the project's `assets/` tree, preserving supplied review/rights flags. Strict HyperFrames audio delivery still requires those fields before wiring.
3. Reuse a frozen record from the local global cache. BGM and SFX cache entries must carry local-origin provenance.
4. On a miss, stop with staging instructions. The agent or user selects and reviews the asset before retrying.

### Review-catalog handoff

In a scaffolded HyperFrames project, `npm run audio:discover -- --type bgm --query "<semantic job>"` (or `--type sfx`) searches workspace review catalogs without copying or approving anything. Treat its result as a lead: inspect the source/license/technical metadata, audition the file, then ingest that exact reviewed candidate with `--source`, `--reviewed`, and the catalog's `--expected-sha256`. Preserve source id/page, catalog id, license name/URL, a substantive review note, and creator/attribution when present. Catalog membership alone is never approval, and a render must never reference the review-library path directly.

After explicit ingestion, the resolver prints one concise result:

```text
resolved sfx_001 → assets/sfx/soft-whoosh.wav (sfx)
```

### Ingest an explicit local file

Use `--source` after selecting and reviewing a file. The resolver copies it into `.media/`, probes its metadata, and records its local provenance.

```bash
node <SKILL_DIR>/scripts/resolve.mjs \
  --type sfx \
  --intent "soft interface whoosh" \
  --source /absolute/path/to/reviewed-whoosh.wav \
  --reviewed \
  --expected-sha256 <64-hex-catalog-hash> \
  --source-id <source-provider-asset-id> \
  --source-page <original-asset-page> \
  --catalog-id <catalog-asset-id> \
  --license <license-name-or-id> \
  --license-url <license-page> \
  --review-note "auditioned under narration; clean short tail" \
  --project .
```

`--source` is an explicit ingestion path, so it bypasses discovery and cache matching. It accepts a regular local file only. When `--catalog-id` is present, the review, hash, source, rights, and substantive-note fields shown above are mandatory. The resolver verifies the hash both before and after freezing the copy, before it writes the manifest.

### Flags

| Flag | Meaning |
| --- | --- |
| `--type, -t` | `bgm`, `sfx`, `image`, `icon`, or `brand` |
| `--intent, -i` | Description, manifest id, or manifest path |
| `--entity, -e` | Optional exact entity match |
| `--source` | Reviewed local file to freeze and register |
| `--source-page` | Original asset page retained as audit metadata |
| `--license` | License name or identifier retained as audit metadata |
| `--license-url` | License page retained as audit metadata |
| `--attribution` | Attribution text retained as audit metadata |
| `--reviewed` | Record that the candidate was explicitly reviewed before ingestion |
| `--expected-sha256` | Require the source bytes to match a 64-hex catalog hash |
| `--creator` | Creator retained as audit metadata |
| `--source-id` | Source provider's asset id retained as audit metadata |
| `--catalog-id` | Local review-catalog asset id retained as audit metadata |
| `--review-note` | Human audition/review note retained as audit metadata |
| `--project, -p` | Project directory; defaults to `.` |
| `--adopt` | Inventory supported files already under `assets/`; bulk inventory alone does not approve audio for rendering |
| `--json` | Emit machine-readable output |

## Adopt an existing project

```bash
node <SKILL_DIR>/scripts/resolve.mjs --adopt --project .
```

Adoption probes supported media with `ffprobe`, appends records to `.media/manifest.jsonl`, and regenerates `.media/index.md`. Bulk adoption is an inventory operation, not editorial approval: BGM/SFX records still need substantive review and rights provenance before the strict HyperFrames sound gate will allow them to render. Resolve a selected staged audio asset individually with the relevant review/license flags to make that provenance explicit. Narration and voice files are intentionally ignored; TTS outputs remain owned by the Fish Audio workflow.

## Inventory and cache

- `.media/manifest.jsonl` is the project source of truth.
- `.media/index.md` is the readable inventory.
- `~/.media/` is the frozen cross-project cache. `MEDIA_USE_GLOBAL_CACHE_DIR` may point the resolver at another trusted local cache root.

The resolver does not purge older cache entries. It simply refuses BGM or SFX records whose provenance does not establish local selection or adoption. Legacy adopted records marked with both `provider: local` and `adopted: true` remain reusable; a remote provider marker is never accepted as local provenance.

Cache eligibility is not current editorial approval. Before reuse, check the current project's decisions and exclusions by candidate id and source hash. A cached asset rejected in this project remains excluded even if an earlier project approved it.

## Miss handling

When resolution misses, use the HyperFrames project's read-only `audio:discover` command, or select a properly licensed asset outside this skill, then ingest the reviewed file with `--source`. Preserve source, license, attribution, hash, catalog identity, and review notes in the project record.

## Requirement

`ffprobe` is recommended for duration, codec, and dimensions. Resolution still works when probing fails, but those metadata fields remain empty.
