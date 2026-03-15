---
name: figma-node-fetcher
description: "Fetch Figma node JSON or node image from a Figma URL. Use when users need layer/node structure, node screenshot export, or design-token inspection from Figma. Require URL with node-id query. Check FIGMA_ACCESS_TOKEN first and guide setup when missing."
---

# Figma Node Fetcher

Fetch data by node from Figma URL and avoid downloading full file trees.

## When To Use

- User provides a Figma link and needs node JSON structure.
- User needs node image export.
- User wants analysis for a specific node, not the whole file.

## Do Not Use

- URL has no `node-id` query.
- User asks to fetch an entire Figma file tree.
- Request is outside supported endpoints.

## Fixed Workflow

1. Check token config: `FIGMA_ACCESS_TOKEN`.
2. Validate Figma URL: must include `node-id`.
3. Route by need:
   - structure data → `type=node`
   - rendered image → `type=image`
4. Choose fetch mode:
   - single URL → `fetch`
   - multiple URLs → `fetch-batch`
5. Run script and return standardized JSON output.

## Config Policy

Read token in this order:
1. environment variable `FIGMA_ACCESS_TOKEN`
2. `{project_root}/.env`
3. `{project_root}/.env.local`
4. `{project_root}/.figma.env`

Recommended location: `{project_root}/.env.local`

## Scripts

### 1) Init config

```bash
python {skill_dir}/scripts/init_figma_config.py --project-root {project_root} --file .env.local
```

### 2) Check config

```bash
python {skill_dir}/scripts/figma_fetch.py check-config --project-root {project_root}
```

### 3) Validate URL

```bash
python {skill_dir}/scripts/figma_fetch.py validate-link --url "https://www.figma.com/file/xxx/xxx?node-id=1%3A2"
```

### 4) Fetch node JSON

```bash
python {skill_dir}/scripts/figma_fetch.py fetch \
  --project-root {project_root} \
  --url "https://www.figma.com/file/xxx/xxx?node-id=1%3A2" \
  --type node \
  --depth 2 \
  --output-dir {project_root}/.figma-output/node
```

### 5) Fetch node image

```bash
python {skill_dir}/scripts/figma_fetch.py fetch \
  --project-root {project_root} \
  --url "https://www.figma.com/file/xxx/xxx?node-id=1%3A2" \
  --type image \
  --format png \
  --scale 2 \
  --output-dir {project_root}/.figma-output/image
```

### 6) Batch fetch (multiple URLs)

```bash
python {skill_dir}/scripts/figma_fetch.py fetch-batch \
  --project-root {project_root} \
  --url "https://www.figma.com/file/xxx/A?node-id=1%3A2" \
  --url "https://www.figma.com/file/xxx/A?node-id=1%3A3" \
  --type node \
  --output-dir {project_root}/.figma-output/batch \
  --clean-output
```

or:

```bash
python {skill_dir}/scripts/figma_fetch.py fetch-batch \
  --project-root {project_root} \
  --urls-file {project_root}/figma-urls.txt \
  --type image \
  --format png \
  --output-dir {project_root}/.figma-output/batch-images
```

## Input Contract

Required fields:
- `url`
- `type` (`node` or `image`)
- `output-dir`

`url` must include `node-id` query.

Batch mode:
- Provide at least one `--url` or `--urls-file`
- Each URL must include `node-id`

## Output Contract

Always return JSON with:
- `ok`
- `mode`
- `type`
- single mode: `figma.file_key`, `figma.node_id`, `output`
- batch mode: `success_count`, `failure_count`, `items`, `failures`, `output_dir`

## Error Handling

- Missing token: return `missing_token` + setup guidance.
- Missing `node-id`: fail fast with clear error.
- No image URL from API: fail with explicit error.
- Batch mode partial failure: return non-zero code + `failures` array.

## API Scope Notes

Read and follow:
- `{skill_dir}/references/figma-rest-api-notes.md`
- `{skill_dir}/examples/integration.md`

Supported endpoints only:
- `/v1/files/{file_key}/nodes`
- `/v1/images/{file_key}`

Do not promise capabilities outside these scripts.

## Cross-Skill Orchestration

This skill can be called by other skills.

Recommended orchestration pattern:
1. Product/Frontend skill receives Figma URL from user.
2. Product/Frontend skill calls this skill (or runs `{skill_dir}/scripts/figma_fetch.py`) to fetch node JSON/image.
3. Product/Frontend skill consumes the fetched artifacts to continue implementation.

Practical rule:
- Do not switch to this skill first unless the user request is specifically “fetch Figma data/image”.
- In mixed tasks (e.g., “build page from Figma”), keep the main skill as orchestrator and use this skill as a data provider.
