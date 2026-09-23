---
name: dify-knowledge-base-upload
description: Upload local files to a Dify pipeline knowledge base through the published pipeline datasource flow and optionally apply existing metadata fields. Use when the target dataset is a published rag_pipeline/local_file knowledge base or ordinary Dify document create APIs return completed with 0 chunks.
---

# Dify Knowledge Base Upload

## Use this skill when
- The target Dify knowledge base is backed by a published pipeline datasource.
- UI uploads succeed but `document/create-by-file` or `create-by-text` yields `completed` with `0 chunks`.
- You need to upload one local file and optionally write existing metadata fields afterward.

## Prepare caller-side inputs
- Provide a local file path to upload.
- For pure text, save it as `.txt` or `.md` first and upload that file.
- Set caller env values:
  - `DIFY_API_BASE_URL`
  - `DIFY_DATASET_ID`
  - `DIFY_API_KEY`
- Optionally provide pipeline `inputs` JSON if the published pipeline exposes user input variables.
- Optionally provide metadata JSON:
  - a flat object mapping existing Dify metadata field names to values, or
  - a list of `{ "name": ..., "value": ... }` / `{ "id": ..., "value": ... }` items.
  - The skill does not hardcode your metadata schema. Pass the current field names or ids in the JSON you provide at runtime.
- Read `references/env.md` only if you need env or debug details.

## Run workflow
- Use `scripts/upload_to_dataset.py` to:
  - discover the published datasource plugin from `${DIFY_API_BASE_URL}/datasets/${DIFY_DATASET_ID}/pipeline/datasource-plugins?is_published=true`
  - upload the file to `${DIFY_API_BASE_URL}/datasets/pipeline/file-upload`
  - run the published pipeline through `${DIFY_API_BASE_URL}/datasets/${DIFY_DATASET_ID}/pipeline/run`
  - poll `${DIFY_API_BASE_URL}/datasets/${DIFY_DATASET_ID}/documents/{batch}/indexing-status`
  - fetch `${DIFY_API_BASE_URL}/datasets/${DIFY_DATASET_ID}/documents/{document_id}?metadata=without`
  - optionally resolve metadata field names through `${DIFY_API_BASE_URL}/datasets/${DIFY_DATASET_ID}/metadata`
  - optionally update metadata through `${DIFY_API_BASE_URL}/datasets/${DIFY_DATASET_ID}/documents/metadata`
- Upload without metadata:

```bash
python3 scripts/upload_to_dataset.py \
  --file /path/to/document.pdf
```

- Upload with pipeline inputs:

```bash
python3 scripts/upload_to_dataset.py \
  --file /path/to/document.pdf \
  --inputs-json assets/example-pipeline-inputs.json
```

- Upload and then apply metadata:

```bash
python3 scripts/upload_to_dataset.py \
  --file /path/to/document.pdf \
  --metadata-json assets/example-metadata.json
```

## Interpret response
- Success prints JSON with `batch`, `document_id`, `file_upload_response`, `pipeline_run_response`, `indexing_status_response`, `document_response`, optional `metadata_response`, and `validation`.
- `validation.ok` is only true when:
  - `indexing_status = "completed"`
  - `total_segments > 0`
  - `segment_count > 0`
- If `tokens` is returned by the document detail API, it should also be greater than `0`. Some pipeline deployments leave `tokens = null`; the script reports that as a warning instead of a hard failure.
- The script exits non-zero if the required checks fail.
- If `--metadata-json` is omitted, the script uploads the file only and skips metadata API calls.
- Metadata keys must already exist in the target dataset. Unknown names fail fast before the metadata write request.
- `assets/example-metadata.json` is only a template. Replace its keys with your own existing Dify metadata field names before live use.
- Use `--dry-run` to validate local files and request shape without calling Dify.

## Troubleshoot quickly
- If auth fails, verify `DIFY_API_KEY` and `Authorization` header format.
- If datasource discovery fails, verify the dataset has a published pipeline datasource and the key belongs to that dataset.
- If the pipeline run fails with missing input errors, inspect `user_input_variables` from `discovery_response` and pass the missing keys in `--inputs-json`.
- If the published datasource is not `local_file`, this skill is not the right uploader.
- If metadata resolution fails, rename keys in the metadata JSON to the exact field names defined in Dify.
- If you only have raw text, save it to `.txt` or `.md` and upload that file.
- In the current tested deployment, `.md` uploaded successfully while `.txt` hit a Dify-side indexing `400`. If plain text fails as `.txt`, retry as `.md`.

## References
- `references/env.md`
- `references/request-response.md`
- `references/testing.md`

## Assets
- `assets/example-pipeline-inputs.json`
- `assets/example-metadata.json`
