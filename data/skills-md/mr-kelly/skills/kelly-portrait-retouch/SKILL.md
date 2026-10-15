---
name: kelly-portrait-retouch
description: Natural, identity-preserving portrait retouching with a local CLI and a Busabase-backed review app. Use when the user asks to 美颜, 修人像, 磨皮, 提亮肤色, portrait retouch, headshot cleanup, profile-photo polish, before/after comparison, or batch portrait enhancement. Default to local non-destructive processing, preserve facial structure and skin texture, and require explicit approval before replacing or publishing any image.
license: MIT
metadata:
  category: production
  tags:
    - risk:local-write
    - industry:beauty
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-portrait-retouch
    resources:
      - jobs
      - candidates
      - settings
    risk: local-write

---

# Kelly Portrait Retouch

Turn portraits into natural, reviewable candidates. Keep the original image and
facial identity intact. Use the App as the review surface and the trusted CLI as
the image-processing boundary.

## Required Skills

1. Read and follow `$kelly-app-skill-creator` for the operator workflow,
   responsive UI, product onboarding, and visual acceptance contract.
2. Read and follow `$busabase-app-creator` for Busabase resource modeling,
   AirApp runtime limits, security, validation, synchronization, and deployment.
3. Use `$kelly-app-skill-creator-tests` for repository-level conformance,
   persistence, OSS Busabase, OAuth, and AirApp parity checks.

The approved product blueprint is [product-overlay.md](references/product-overlay.md).

## Defaults

- Use the `natural` preset at strength `35` unless the user asks otherwise.
- Create a new sibling file ending in `_retouched`; never overwrite by default.
- Strip EXIF/GPS metadata by default. Preserve metadata only when explicitly
  requested.
- Preserve face shape, age, skin tone, moles, freckles, scars, and other identity
  cues unless the user names a specific reversible edit.
- Do not whiten skin, enlarge eyes, shrink a face, or change body shape by
  implication. Ask before structural or identity-changing edits.
- Treat portraits as sensitive biometric data. Do not upload them to an external
  model unless the user explicitly approves that route.

## Local CLI

Install once from the skill directory:

```bash
pnpm install --frozen-lockfile
```

Create one natural candidate:

```bash
node scripts/retouch.mjs portrait.jpg --preset natural --strength 35
```

Create a candidate and a side-by-side proof:

```bash
node scripts/retouch.mjs portrait.jpg --output exports/portrait-natural.jpg --compare exports/portrait-proof.jpg
```

Create a reusable processing summary, inspect the dry-run sync plan, then write
the candidate through the trusted Busabase boundary:

```bash
node scripts/retouch.mjs portrait.jpg --compare exports/portrait-proof.jpg --summary exports/portrait-summary.json
node scripts/sync-candidate.mjs exports/portrait-summary.json
node scripts/sync-candidate.mjs exports/portrait-summary.json --apply
```

Use `--face x,y,width,height` when automatic face detection is unavailable or
needs correction. Coordinates are image pixels after orientation is applied.
Run `node scripts/retouch.mjs --help` for every option.

The CLI uses macOS Vision for face rectangles when available, then applies a
subtle masked texture blend with Sharp. On other platforms it performs only
whole-frame tone/detail polish unless `--face` is supplied. It never changes
facial geometry.

## Workflow

1. Inspect the source image at full resolution. Note blur, compression, clipping,
   mixed lighting, and whether the requested result is realistic.
2. Confirm any ambiguous identity-changing request. For ordinary “美颜”, use the
   natural defaults without asking.
3. Run the CLI and keep its JSON summary. Generate a comparison image when the
   user needs to judge strength.
4. Inspect the candidate at face scale and full-frame scale. Reject waxy skin,
   halos, flattened detail, color shifts, or softened eyes/hair.
5. Present the candidate and comparison for review. Iterate by reducing strength
   before adding more processing.
6. When Busabase is available, run the sync command as a trusted Agent. It
   uploads source/output/comparison files through Busabase Assets and upserts the
   `jobs` and `candidates` Bases with stable idempotency keys. Base rows store
   asset IDs, not image bytes or expiring URLs.
7. Export or replace only after the user names the approved candidate. Publishing
   remains outside this skill.

## Presets

- `natural`: restrained tone lift and face-local texture softening; default.
- `fresh`: slightly brighter and more saturated for casual/social portraits.
- `studio`: neutral color, restrained contrast, and crisper detail for headshots.

Read [retouch-policy.md](references/retouch-policy.md) before fulfilling a
structural edit, processing a minor's portrait, or using an external image model.

## App Contract

The canonical App source is in `content/kelly-portrait-retouch-app/`. It provides a quiet list/detail review
desk with hash routes, before/after inspection, strength and preset metadata,
approve/change/block decisions, bilingual chrome, phone navigation, and Help &
Settings. `?demo=queue` opens deterministic read-only data.

Busabase resources:

- Folder `kelly-portrait-retouch` owns the workflow.
- Base `jobs` stores one row per local processing request and its lifecycle.
- Base `candidates` stores candidate provenance, checks, and human verdicts.
- Base `settings` stores non-secret defaults and onboarding state.
- Busabase Assets stores source, candidate, and comparison files; Base records
  keep their stable asset IDs.

The browser never receives filesystem access, API keys, or Vault values. The
trusted Agent runs the CLI and performs content-addressed asset upload plus
idempotent record writes. The App only reads approved state and records human
decisions through stale-version-protected ChangeRequests. Runtime readiness and
product onboarding are separate; incomplete onboarding suppresses workflow rows.

## Validation

Run:

```bash
pnpm test
pnpm --dir content/kelly-portrait-retouch-app check
node scripts/retouch.mjs --help
node scripts/sync-candidate.mjs --help
```
