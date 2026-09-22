---
name: roboflow-batch-processing
description: Use when running a Roboflow Workflow over many images or videos with batch processing — Asset Library jobs (the platform stages workspace images for you) or staged jobs (you stage external local/cloud files with the inference-cli), plus monitoring jobs, downloading results, and routing imports to datasources (bucket mirror) instead.
---

> **For agents — source-of-truth:** This skill is authored in [`roboflow/computer-vision-skills`](https://github.com/roboflow/computer-vision-skills) and shipped with the Roboflow plugin. If your client has loaded the plugin (you'll see `roboflow:<name>` skills in your available skills list), use those local skills — they're read fresh from disk every session. The same content served as MCP resources at `roboflow://skills/<name>/...` is a fallback for clients without the plugin and may lag this repo. **Don't call `ReadMcpResourceTool` for `roboflow://skills/...` URIs when a local `roboflow:<name>` skill is available.**

# Batch Processing

Run a Roboflow Workflow over a very large set of images or videos on
Roboflow's autoscaling compute. Every job processes a temporary Data Staging
batch; the two input paths differ only in **who fills that batch**:

- **Asset Library job** — the files are already in Roboflow. You hand the
  platform a selection and it selects and stages them for you.
- **Staged job** — the files are outside Roboflow (local disk, cloud bucket,
  references file), so you stage them yourself with the inference-cli: only
  your machine and credentials can reach them. Nothing is imported into the
  workspace, and staged data expires after ~7 days.

## Which path? Three questions

1. **Are the files already in Roboflow (Asset Library)?** Call
   `batch_processing_asset_library_job_create` with a stable idempotency key
   and exactly one selection: `image_ids`, `query`, or `all_images=true`. The
   platform performs access checks, selects the files, stages them, verifies
   Workflow compatibility, bills, and registers the durable job. Poll the
   returned `taskId` with `batch_processing_asset_library_task_get` until the
   task is terminal; then monitor its `jobId` with `batch_processing_job_get`.
2. **Files outside Roboflow, and you only want the outputs?** Stage them
   yourself and drive the run with `batch_processing_guide` +
   `batch_processing_run` as described below (the classic ETL shape: nothing
   lands in the workspace). Staging and result export must run on the machine
   that can access the files.
3. **Files outside Roboflow that you want INSIDE it** (labeling, curation,
   training)? That is an import, not a batch processing job: mirror the
   bucket with a datasource (`connect_cloud_storage`, see the `cloud-storage`
   skill). Once mirrored, the files are Asset Library images, so if you also
   want bulk predictions, run an Asset Library job over them (the classic ELT
   shape: load first, then transform).

"Datasource" and "bucket mirror" are one thing: a datasource is the
user-facing name for a bucket-mirror config, the importer that fills the
Asset Library. It never runs Workflows itself.

In pipeline terms: a staged job is the T of an ETL flow (no load ever
happens), and an Asset Library job is the T of an ELT flow — the load
already happened, via uploads or a datasource mirror.

## Prerequisites

- The workspace needs the batch-processing feature. Gated calls fail with a
  402 "Batch processing is not enabled for this workspace. Upgrade your plan
  or contact sales at https://roboflow.com/sales."
- Jobs consume credits; the workspace must have a positive balance.
- The Workflow must already exist in the workspace (`workflows_list`,
  `workflows_create`). Jobs reference it by `workflow_id`; there is no
  inline-spec option.
- API key: the inference-cli reads `ROBOFLOW_API_KEY` from the environment,
  and every command also accepts `--api-key=<key>`. A key stored by
  `roboflow login` (`~/.config/roboflow/config.json`) is NOT picked up by
  the inference-cli: export it or pass `--api-key` explicitly. Mint one with
  the `api_keys_create` MCP tool. Never have the user paste a private key
  into chat.

## Where each step runs, and why

Two steps are inference-cli only, because the MCP server can neither read nor
write the user's disk:

- **Staging** runs on the machine that can reach the files (local disk) or
  with the user's cloud credentials (bucket sources).
- **Exporting results** (`export-batch`) downloads into a local directory.

Everything in between needs only an API key, so it works either way: the MCP
tools (`batch_processing_run`, `batch_processing_staged_job_start`,
`batch_processing_job_get`, `batch_processing_jobs_list`,
`batch_processing_job_logs`, `batch_processing_job_abort`,
`batch_processing_job_restart`, plus the
`batch_processing_asset_library_*` and `batch_processing_staging_*`
families) or the equivalent CLI commands. Prefer the MCP tools when the host has no shell or the user has
no local `inference-cli`; prefer the CLI when the user is already in a
terminal. The full command set for both content types is in sections 1-5.

The `batch_processing_guide` MCP tool routes a request: it settles the batch
id, picks the staging source, and returns the exact ordered commands. It
never touches files or the network, and it does not repeat this document.

## The master tool for staged batches: `batch_processing_run`

Prefer `batch_processing_run(batch_id, workflow_id, content_type, ...)` to
drive the flow over a staging batch you name (for Asset Library selections,
use `batch_processing_asset_library_job_create` instead). Each call reads
current state, advances what it can, and returns immediately with a status:

- `staging_required` — no batch yet; the response contains the CLI commands
  for the whole run plus cloud-credential guidance. Run them, then call again.
- `ingest_in_progress` — files still registering.
- `ingest_failed` — ingest failed or returned an unknown shard state; no paid
  job was started.
- `running` — the job was started or is still working; includes stage progress.
- `completed` — includes the export batch id and the first result files with
  signed download URLs.
- `failed` — includes logs and a restart hint.

**The server never waits on your behalf.** Non-terminal responses carry
`retryAfterSeconds`; sleep that long on your side, then call again with the
returned `job_id` and the same `batch_id` to resume. Omit optional creation
settings on a read-only resume: the paid job's stored definition is
authoritative. The server holds no state between calls.

The job is started under an id derived from (workspace, batch, workflow), so
retrying after a lost response re-registers the same job instead of paying for
a second run. (The platform checks credits before that idempotency comparison,
so a retry can still see a 429 first.) A 409 means that id already exists with
different batch/Workflow identity or conflicts with an optional setting you
explicitly supplied. Inspect the job, omit optional settings to monitor it as
stored, or pass a new explicit `job_id` for a separate run.

For the advanced knobs (`max_runtime_seconds`, `max_parallel_tasks`,
`max_image_failure_rate`, `image_outputs_to_save`) use
`batch_processing_staged_job_start` directly.

## Webhooks

Roboflow will POST job and ingest notifications to a URL you control. There is
no MCP-side relay: pass `notifications_url` to `batch_processing_staged_job_start`, or
`--notifications-url` on the CLI commands, pointing at your own receiver. The
POST carries an `Authorization` header with your publishable key.

Caveat: local **video** staging does not support `--notifications-url` (the CLI
prints a warning and drops it), and a small local **image** batch (32 files or
fewer stages as a simple batch) ignores it too. Sharded local image,
cloud-storage and references-file ingests all support it.

If you have no receiver, just poll `batch_processing_job_get` (or
`batch_processing_run`, which reports progress on each call).

## 1. Install the CLI

```bash
pip install inference-cli
# For s3:// gs:// az:// sources:
pip install 'inference-cli[cloud-storage]'
```

Every `inference rf-cloud` command below authenticates via `ROBOFLOW_API_KEY`
from the environment, or `--api-key=<key>` on the command itself.

Cloud credentials are picked up from the standard env chains on the machine
running the CLI: AWS via the default credential chain (`AWS_PROFILE` honored;
R2/MinIO work via `AWS_ENDPOINT_URL`, with `AWS_REGION` applied alongside it),
GCS via `GOOGLE_APPLICATION_CREDENTIALS`, Azure via
`AZURE_STORAGE_ACCOUNT_NAME` plus `AZURE_STORAGE_ACCOUNT_KEY` or
`AZURE_STORAGE_SAS_TOKEN`. For S3/GCS the CLI generates presigned URLs (24h
expiry); for Azure it appends your SAS token, so those URLs stay valid as long
as the token does. Either way the URLs are handed to Roboflow and bucket
secrets never leave the machine.

## 2. Stage a batch

Batch ids: lowercase letters, digits, `-` or `_`. Staged batches expire
after ~7 days.

```bash
# Local images (>32 images are packed into tar shards automatically)
inference rf-cloud data-staging create-batch-of-images \
  --batch-id my-batch --images-dir ./images

# Local videos (uploaded one by one via signed URLs)
inference rf-cloud data-staging create-batch-of-videos \
  --batch-id my-batch --videos-dir ./videos

# Cloud bucket (S3/GCS/Azure; glob over object paths).
# Videos work exactly the same way: create-batch-of-videos.
inference rf-cloud data-staging create-batch-of-images \
  --batch-id my-batch --data-source cloud-storage \
  --bucket-path 's3://my-bucket/images/**/*.jpg'

inference rf-cloud data-staging create-batch-of-videos \
  --batch-id my-batch --data-source cloud-storage \
  --bucket-path 's3://my-bucket/videos/**/*.mp4'

# References file: JSONL lines of {"name": ..., "url": "https://..."}
inference rf-cloud data-staging create-batch-of-images \
  --batch-id my-batch --data-source references-file --references refs.jsonl
```

Images vs videos is a choice you make, not something inferred from the path:
`create-batch-of-images` and `create-batch-of-videos` both accept every data
source. Pick the one matching the content.

Sharded, cloud-storage, and references ingests are asynchronous. Wait until
the batch is fully ingested before starting a job:

```bash
inference rf-cloud data-staging show-batch-details --batch-id my-batch
inference rf-cloud data-staging list-ingest-details --batch-id my-batch
```

or the `batch_processing_staging_batch_get` MCP tool, which returns the file
count plus an `ingest` block with `pending` and `failed` flags. Do not start a
job while `pending` is true or `failed` is true: the job costs credits and
would run over incomplete input.

Practical limits: up to 20,000 image references per ingest request
(auto-chunked; video references cap at 5,000 per request and are not chunked),
~1,000 videos per batch suggested, image formats jpg/png/webp/bmp/jp2,
video formats mp4/mov/avi/mkv/flv/wmv/m4v. `batch_processing_staging_batches_list`
shows every staged batch in the workspace (inputs and job results).

## 3. Start the job

CLI, images:

```bash
inference rf-cloud batch-processing process-images-with-workflow \
  --batch-id my-batch --workflow-id my-workflow --machine-type gpu
```

CLI, videos:

```bash
inference rf-cloud batch-processing process-videos-with-workflow \
  --batch-id my-batch --workflow-id my-workflow --machine-type gpu \
  --max-video-fps 5
```

Shared optional flags: `--workers-per-machine 1|2|4|8`,
`--aggregation-format jsonl|csv`, `--save-image-outputs`,
`--image-outputs-to-save <name>`, `--image-input-name <name>`,
`--workflow-params params.json`, `--max-runtime-seconds <n>`,
`--max-parallel-tasks <n>`, `--job-id <id>`, `--job-name <name>`,
`--notifications-url <url>`, `--part-name <part>`.

Images only: `--max-image-failure-rate 0.0-1.0` (the server rejects it on
video jobs). Videos only: `--max-video-fps <n>`.

MCP equivalent:

```
batch_processing_staged_job_start(
  job_id="my-stable-job-id",           # required; reuse for retries
  batch_id="my-batch", workflow_id="my-workflow",
  content_type="images",            # or "videos"
  machine_type="gpu",               # cpu|gpu, optional
  workers_per_machine=4,            # 1, 2, 4 or 8, optional
  aggregation_format="jsonl",       # or "csv"
  save_image_outputs=True,          # persist crops/visualizations
)
```

For videos, set `content_type="videos"` and optionally `max_video_fps=5`
(prediction subsampling). The tool rejects `max_video_fps` on image jobs and
`max_image_failure_rate` on video jobs, matching the platform.

### Choosing cpu vs gpu (`machine_type`)

Default compute is CPU. Decide with two quick checks before starting a paid
job over the whole batch:

1. **Test-run the Workflow on one representative image** (`workflows_run` MCP
   tool, or the hosted API) and measure the wall time. Run it twice and time
   the second call (the first may cold-start). If a single image takes more
   than about a second of model time, CPU workers will crawl through a large
   batch: take `gpu`.
2. **Inspect the Workflow spec** (`workflows_get`): count the model steps and
   note their sizes. One small fine-tuned detector/classifier: `cpu` is the
   cheapest and usually enough. Several models chained, or any large
   foundation model (SAM family, CLIP, OCR, VLM blocks): `gpu`.

Videos multiply per-frame work with `--max-video-fps`, so lean `gpu` there
too. `workers_per_machine` (1/2/4/8) then scales throughput on one machine:
more workers means better utilization but a higher OOM risk.

Same job_id plus an identical definition is idempotent; a divergent one is
rejected with a 409. The tool checks that ingest is complete before the paid
registration call. For a multipart input, pass `part_name`; it is also
supported by `batch_processing_run`. Both tools default to the current
`inference-models` backend; use `inference_backend="old-inference"` only for a
known compatibility requirement.

## 4. Monitor

```bash
inference rf-cloud batch-processing show-job-details --job-id my-job
inference rf-cloud batch-processing fetch-logs --job-id my-job
inference rf-cloud batch-processing abort-job --job-id my-job
inference rf-cloud batch-processing restart-job --job-id my-job
```

MCP equivalents, which return JSON rather than a rendered table:

- `batch_processing_job_get(job_id)` — status, current/planned stages,
  per-stage progress, output batches; `job.isTerminal` + `job.error` are the
  end states.
- `batch_processing_job_logs(job_id)` — info/error logs for diagnosis.
- `batch_processing_job_abort(job_id)` / `batch_processing_job_restart(job_id)`
  — stop a run, or retry a failed one (optionally overriding machine type,
  workers, timeout).
- `batch_processing_jobs_list(search=...)` — the workspace's recent Workflow
  jobs, for finding a job id you did not keep. Internal TensorRT compilation
  jobs are excluded. Both this tool and `batch_processing_job_get` label each
  job with `inputSource`: `asset-library` (platform-staged selection) or
  `staged-batch` (a batch you staged yourself).

## 5. Download results

Results land in Data Staging as platform-generated batches:
`<job-id>-processing` (raw per-shard outputs) and `<job-id>-export`
(packaged, downloadable archives).

Downloading writes to disk, so this step is CLI only:

```bash
inference rf-cloud data-staging export-batch \
  --batch-id my-job-export --target-dir ./results
```

It is resumable; add `--override-existing` to re-pull content already
exported, and `--part-name <part>` to fetch one part of a multipart batch.

The MCP tool `batch_processing_staging_batch_files_list(batch_id="<job-id>-export")`
lists the same files with signed `downloadURL`s (~24h expiry) so a host with no
shell can still fetch them. Export batches are multipart: the tool selects the
part automatically when there is exactly one, and otherwise asks you to pass
`part_name` (the parts are in `batch_processing_staging_batch_get`). Archives
(`.tar` / `.tar.gz`) must be unpacked after download, and listings are capped
at 10,000 entries per call — past that scale keep paginating with
`nextPageToken` and per-part `part_name` listings, or pull everything with the
resumable `export-batch`.

Do this within 7 days: staged inputs and results expire.
