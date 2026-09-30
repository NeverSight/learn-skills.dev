---
name: platform-cli
description: >
  Use when operating Ultralytics Platform from a terminal or script with the ul cloud CLI
  (ul cloud RESOURCE OPERATION key=value, PyPI package ultralytics-platform) — listing,
  creating, updating, cloning, or moving projects, datasets, and models; inspecting
  dataset images, statistics, metadata, duplicates, and similar images; starting and
  monitoring cloud training runs; per-image model validation analysis; downloading
  weights, exports, deployments, uploads, trash and restore, storage integrations, and
  account usage, storage, and billing. For the Platform web UI or local yolo commands,
  see yolo; for choosing what to train and how to improve it, see yolo-training and
  yolo-tuning.
---

# Platform CLI (`ul cloud`)

`ul` needs Python 3.11+ and comes with `pip install ultralytics` or
`pip install ultralytics-platform`. `ul cloud` calls the Platform API through the generated
SDK; `ul login`, `ul train`, `ul predict`, and the other local commands delegate to the
`ultralytics` package. This skill covers Platform operations, not model selection or
hyperparameter tuning.

```bash
pip install ultralytics                   # or `pip install ultralytics-platform`
export ULTRALYTICS_API_KEY="YOUR_API_KEY" # or `ul login API_KEY`
ul cloud --help                           # every resource and operation
ul cloud training start --help            # one operation's arguments, types, and choices
```

Endpoint semantics are documented in the
[Platform API reference](https://docs.ultralytics.com/platform/api).

## Canonical command shapes

```bash
ul cloud account summary # plan, credits, counts; `username` is your workspace
ul cloud datasets list   # omit owner= for your own workspace; owner=TEAM for a team
ul cloud projects create project=helmets name="Helmet Detection" visibility=private
ul cloud models create body='{"owner":"WS","project":"helmets","model":"exp1","name":"Experiment 1"}'
ul cloud training start model_id=MODEL_ID gpu_type=l4 \
  train_args='{"model":"yolo26n.pt","data":"ul://WS/datasets/helmets","epochs":50}'
ul cloud models training project=helmets model=exp1 # live status, epoch progress, metrics
ul cloud models files project=helmets model=exp1    # short-lived weights download URL
```

Argument rules:

- Use the command shapes shown here without a preliminary `--help` call. Check operation help
  when a needed argument is missing or after an argument error.
- Arguments are SDK Python names as `key=value` (`gpu_type`, `project_id`), never
  `--key value`. A bare boolean means `true`. Quote JSON for the shell.
- An operation takes one `body=` JSON object exactly when its help lists
  `body (dict[str, Any])`. These are the operations whose API request is a union of
  shapes: `models create`, `deployments update`, `images update`, `lifecycle delete-trash`,
  `datasets ingest`, `datasets create-batch`, `upload signed-url`,
  `storage-integrations create`/`discover`, and `models predict`/`deployments predict`. Every
  other operation takes flat fields; nested objects such as `train_args`, `metadata`, and
  `args` are still JSON values.
- Object and array values accept `@file.json` or `@-` for stdin. Multipart binaries such as
  the predict `file` field accept `@path` only.
- For body keys and value types, read the request schema from the production contract
  instead of guessing or loading the whole file:

```bash
curl -s https://platform.ultralytics.com/openapi.json | python3 -c \
  "import json,sys; print(json.dumps(json.load(sys.stdin)['paths']['/api/models']['post']['requestBody'], indent=1))"
```

Behavior rules:

- Output is the complete API response on stdout, printed as JSON, text, or bytes according
  to its content type. Download operations return signed URLs, not bytes: `datasets export`,
  `datasets create-export`, `models files`, and a completed `exports retrieve` return URLs
  that expire. Preserve them verbatim and fetch them separately.
- Failures go to stderr: exit 1 for API/connection errors, 2 for argument/file errors, 130
  when interrupted. Interrupting does not cancel a submitted job; use its cancel operation
  (`models delete-training`, `exports delete`, `datasets delete-batch`).
- There is no `--json`, `--fields`, `--dry-run`, or automatic pagination. `datasets list`
  (`limit`, `include_samples`, `include_image_urls`) and `projects list` (`limit`) take no
  `offset` or `search`; pass `include_samples=false` to keep dataset listings small.
  `models list` requires `project=`. Operations that page expose `page`,
  `offset`, `cursor`, or `page_token`; the CLI never fetches the next page. Follow returned
  continuation fields until exhausted. A limit-only listing may still be incomplete.
- An omitted path `owner` defaults to the logged-in username after one account lookup. Pass
  `owner=TEAM` for team workspaces. Account, billing, trash, storage-integration, and Roboflow
  commands act on the credential's own account, and `account summary` does not list teams
  for API keys.
- Display names, URL slugs, database IDs, and URIs are distinct. Training data is
  `ul://OWNER/datasets/DATASET`; starting weights are a checkpoint name or
  `ul://OWNER/PROJECT/MODEL`. Carry returned IDs and slugs into the next command; retrieve
  missing identifiers instead of inferring them from names or URLs. Take a named dataset's or
  project's slug from its listing before retrieving it.

## Working method

1. Resolve the requested outcome and target. Use exact supplied identifiers; otherwise list
   and pick one unambiguous match. For several matches, inspect distinguishing metadata and
   ask when the target or consequence stays ambiguous. When a named resource is not found,
   say so and offer the closest matches; never substitute another one. A bounded listing does
   not prove absence; broaden discovery or report what was searched. Retrieve named datasets in the
   caller's workspace; use Explore to find new public datasets. Start with one short keyword
   (`aerial`, then `UAV`) and narrow with `task=`; dataset search uses token autocomplete, while project search matches literal
   substrings. There is no relevance sort. Before recommending them for training, verify clone
   eligibility, labels, and splits. If none match or search fails, say so.
2. Read current state when it affects the change (visibility, status, existing children).
3. Execute the smallest requested change, then verify from the response. Retrieve again when
   the response omits needed state, the write is uncertain, or the job is asynchronous.
4. Report what actually changed, current status, warnings, and a verified resource link when
   one exists. Creating an entry, accepting a job, and completing it are separate outcomes.

Execute clearly requested actions without repeated confirmation. For spending, sharing, or
irreversible changes, resolve ambiguity about target or consequence first. A request for
advice is not authorization to act; "clean things up" is not permission for account-wide
deletion. Do not invent commands, flags, or status edits to simulate operations the CLI does
not expose; use the UI for those.

## Workflows

Commands drop only the `ul cloud` prefix and the defaulted owner.

| Goal               | Commands                                                                                                                                                                                                                                                                                                                                                 |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Inventory          | `projects list`, `datasets list`, `models list project=P`. `explore search q=... type=datasets` searches public content, which is not private inventory. Retrieve a dataset to check task, classes, splits, and readiness.                                                                                                                               |
| Create             | `projects create project=slug name="Display"`, `datasets create dataset=slug name="Display" task=detect`. Set `visibility=` deliberately.                                                                                                                                                                                                                |
| Copy               | `datasets clone dataset=D owner_body=DEST_OWNER`, `projects clone project=P owner_body=DEST_OWNER`, `models clone project=P model=M owner_body=DEST_OWNER project_body=DEST_PROJECT`. Path fields name the source; `*_body` fields name the destination. A model's destination project must exist.                                                       |
| Rename, edit, move | `<resource> update` with the changed fields only. Move a model with `models update project=P model=M project_id=DEST_ID` alone.                                                                                                                                                                                                                          |
| Compare runs       | `projects retrieve project=P` for model summaries, `models list project=P`, or `datasets models dataset=D` for runs on a dataset; `models retrieve project=P model=M` only for missing metrics. Tabulate status, dataset/version, configuration, and requested metrics with links. Missing metrics are unknown, not zero. There is no compare command.   |
| Analyze model      | `models retrieve project=P model=M analysis=1`, then `models find-similar-training-images project=P model=M` when needed. See [Model analysis and similarity](#model-analysis-and-similarity) for coverage and hash selection.                                                                                                                           |
| Weights            | `models files project=P model=M` returns a temporary checkpoint URL. No training or export is needed.                                                                                                                                                                                                                                                    |
| Convert            | `exports create project=P model=M format=onnx`, then `exports retrieve project=P model=M export_id=ID` for progress and the download URL. `format=engine` needs `gpu_type`. Exporting does not deploy.                                                                                                                                                   |
| Dataset versions   | `datasets create-export dataset=D` saves an immutable numbered snapshot with a signed NDJSON URL; `datasets export dataset=D` (`v=N` for a saved version) returns a download URL; `datasets restore dataset=D version=N` rolls the dataset back; `datasets update-export dataset=D version=N description="TEXT"` updates a saved version's description.  |
| Deploy             | `deployments create project=P model=M deployment=slug name="Display" region=us-central1`. `deployments update deployment=D body='{"action":"replace","project":"P","model":"M"}'` swaps the model on the same URL; `body='{"action":"stop"}'` and `{"action":"start"}` pause and resume it. `deployments health deployment=D` warms it.                  |
| Usage, services    | `account storage`, `billing usage-summary`, and `billing transactions` inspect workspace usage; `deployments list`, `retrieve`, `logs`, and `metrics` inspect endpoints. See [Usage and billing](#usage-and-billing) and [Compute](#compute) for filters and pagination.                                                                                 |
| Inference          | `models predict project=P model=M body='{"file":"@image.jpg"}'` or `deployments predict deployment=D body='{"file":"@image.jpg"}'`. `images predict image_id=ID model_id=ul://...` predicts on a dataset image without saving labels.                                                                                                                    |
| Import data        | `datasets create dataset=D name="Display"`, then `upload signed-url body=` (`assetType`, `assetId`, `filename`, `contentType`, `totalBytes`), PUT the bytes with the returned headers, `upload complete session_id=S`, `datasets ingest dataset=D body='{"sessionId":"S"}'` (or `{"sourceUrl":...}`), then retrieve until ready. Queued is not imported. |
| Trash              | `projects delete project=P`, `datasets delete dataset=D`, and `models delete project=P model=M` move them to 30-day trash. `lifecycle trash` lists it, `lifecycle restore id=ID type=model` undeletes, `lifecycle delete-trash body='{"id":"ID","type":"model"}'` purges one item, and `body='{"all":true}'` permanently empties all workspace trash.    |

## Cloud training

1. Resolve the workspace, project, a ready dataset, starting weights, and requested settings.
   Check `training gpu-availability` before choosing `gpu_type`; cloud training spends
   credits. `data` must use the dataset's actual owner, which may differ from the model's.
2. `models create body=...` with `owner`, `project`, the `model` slug, and `name` for a new
   experiment. Reuse a pending entry from a failed start after checking its state.
3. `training start model_id=ID gpu_type=... train_args=...` with a fresh `train_args`
   holding `model`, `data`, and numeric `epochs` plus requested settings. Omit `device`.
   Do not copy stored worker arguments wholesale; saved data paths may be worker-local.
4. `models training` or `models retrieve` for progress. Return the run link and actual
   status without waiting for completion unless asked. `models delete-training` cancels a
   run and keeps its entry; never start an active run again.

## Recover

- **401**: check the credential source without exposing secrets. `ULTRALYTICS_API_KEY`
  overrides the saved login key, so logging in again does not replace a stale environment
  value. If the execution environment injects credentials, use its flow. Verify with a read
  afterwards.
- **403**: read the error for workspace access, permissions, or operation constraints; do
  not assume an expired login.
- Fix clear validation errors within the requested action. After a timeout or uncertain
  write, inspect state before retrying. Stop on unresolved inputs, permissions, or repeated
  failure; report partial results and remaining work instead of duplicating writes.

Resource links use `https://platform.ultralytics.com`: projects `/{owner}/{project}`,
datasets `/{owner}/datasets/{dataset}`, models and training `/{owner}/{project}/{model}`.
Use returned slugs after changes; retrieve missing slugs. Deployments are the exception:
there is no per-deployment Platform page. Link to
`/{owner}/{project}/{model}?tab=deploy` by default; use `/deploy` only when the owning model
identifiers are unavailable. After status is `ready`, report the exact `serviceUrl` returned
by `deployments retrieve` for inference; never construct a UI or service URL from the
deployment ID, name, or slug.

## Operation gotchas

Operation help already says what each command does. These are the side effects and
constraints it omits; `--help` and the error text still win when they disagree.

### Clone

- Project, dataset, and model clones need a different destination workspace. Cloning is
  not how to create a same-workspace experiment; use `models create`.
- Model sources need usable weights and must not be training. Project clones carry
  completed models with weights but not datasets, deployments, exports, or unfinished runs.

### Visibility

- Creation may default to public and clones may keep the source's visibility, so set
  `visibility=` explicitly. Public projects expose their models. Public visibility is not
  collaborator edit access.

### Update

- Arrays and `metadata` objects replace prior values. Send the full list for a partial edit.
- `starred` is handled by a separate branch that ignores other fields in the same call. Send
  it alone.
- Starting training again on an existing model clears its prior run metrics and results.
  Create a new model to keep them. Fine-tuning from existing weights does not resume the
  optimizer or epoch count.
- `capture_dataset_version=true` saves a new snapshot; it does not select an existing one.

### Delete, trash, restore

- `lifecycle delete-trash` is irreversible. Run it only when the user explicitly requests
  permanent deletion of the specified items; `body='{"all":true}'` requires an explicit
  request to empty all workspace trash. Otherwise, leave purging to the user in the UI.
- `projects update archived=true` only organizes; it frees nothing.
- Trashing a project also trashes its models and cancels their training. Both
  `projects delete` and `models delete` permanently delete attached deployments during
  the trash operation; restoring the project or model does not restore deployments.
  HTTP 502 means cleanup is incomplete; inspect deployments before reporting them deleted.
  If deployments are attached, explain this consequence and obtain explicit authorization
  before trashing, unless the user's request already covers their permanent deletion.
- Restore a parent before its children; independently trashed children need their own
  restore. Dataset version restore is separate: `datasets restore dataset=D version=N`
  replaces the current images, splits, classes, and annotations with the selected snapshot.
  It cannot be undone unless the current state was first versioned. When preservation
  matters, first run `datasets create-export dataset=D`. Stop active annotation and wait for
  the dataset to return to `ready` after restoring.
- `images delete` and `images delete-bulk` are permanent and bypass trash.
- `datasets create-export` reuses an identical existing snapshot instead of creating a
  duplicate.

### Labels and auto-annotation

- `images update body='{"labels":[...]}'` replaces every label on the image, and
  `images predict` alone saves nothing. Retrieve first for a partial edit, and when the
  retrieve reports `labelsTruncated`, do not overwrite the labels you did not see.
- `datasets create-batch` persists labels and saves a version, normally on unlabeled images
  only. Use `datasets create-batch dataset=D body='{"modelId":"ul://OWNER/PROJECT/MODEL"}'`;
  `"includeAnnotated":true` in its body also processes labeled images while retaining old
  labels. `delete-batch` cancels or dismisses a run without undoing labels already saved.
- `datasets create-batch dataset=D body='{"operation":"blur"}'` blurs faces in the dataset's
  images (one image with `imageId`) and saves no version; run `datasets create-export` first
  when the originals matter.
- Annotation prediction needs compatible tasks and classes, or an explicit mapping:
  `class_mapping=` for `images predict`, `classMapping` inside `body=` for
  `datasets create-batch`. It rejects connected, depth, and more-than-three-channel datasets.

### Classes, splits, task

- `class_names` replaces names by index; keep the order for a rename. Merging or deleting
  classes remaps or removes labels and shifts IDs.
- `redistribute-splits` reshuffles the whole dataset. `images update-bulk` moves selected IDs,
  and conflict policy `replace` may remove target images.
- `adopt-images` adds unlabeled public-image references to the train split, skipping
  existing images; it copies no labels or splits.
- Changing `task` converts no annotations. Switching to or from depth needs an empty dataset.

### Dataset inspection and analysis

- For duplicates or split leakage, group all image records by hash and compare IDs and splits.
  Storage deduplication does not prevent duplicate records. Use small pages or a downloaded
  export; if records are missing or clipped, report partial coverage, not zero duplicates.
- `datasets retrieve dataset=D` returns task, classes, splits, and counts.
  `datasets class-stats dataset=D` returns distributions and heatmaps; a set `sampleSize`
  means the stats came from a capped subset, and histogram bins carry a `size` width.
- List a dataset's images with `datasets images dataset=D` (there is no `images list`); it
  filters by `split`, `has_label`, `has_error`, `class_ids`, and `search`. For counts alone,
  use `limit=1` and read `total` (included by default), not the page length. `has_error`
  means a recorded processing error. Disable
  `include_thumbnails`, `include_image_urls`, and `include_labels` to keep inventory pages
  small; pass `nextCursor` as `cursor` while `hasMore`. The cursor works only with the
  default `newest`/`oldest` sort; other sorts page with `offset`. Equal `hash` values mean
  the same stored bytes, not visual similarity.
- `search=TERM` matches substrings of filenames (extension optional) and metadata keys,
  scalar values, and array entries, but not values inside nested objects. There is no
  field selector; retrieve matches to verify which field hit. A 32-hex term
  matches the content `hash` exactly and a 24-hex term matches the image ID, so
  `search=HASH` finds every stored copy of an image without exporting.
- Listings omit custom `metadata`; `images retrieve image_id=ID` returns it with labels.
  Both listing and retrieval can truncate labels: honor `labelsTruncated` and compare
  returned lengths with `labelCount` or retrieval's `properties.annotationCount`.
  `datasets selected-images dataset=D image_ids='["ID1","ID2"]'` fetches several known IDs in
  one call, not one `images retrieve` each, with the same optional fields;
  `images urls image_ids='["ID1","ID2"]'` refreshes signed URLs for up to 100 IDs from one
  dataset. `datasets export dataset=D` provides NDJSON metadata and annotations for bulk
  aggregation; On Premise datasets cannot export.
- `images find-similar-images image_id=ID` returns up to 24 near neighbors from public
  datasets, excluding the image's own dataset and near-duplicate copies of the query. It
  takes only an existing image ID. HTTP 404 `not_embedded` means no embedding is currently
  available for the image's hash; embeddings come from dataset analysis, so an unanalyzed
  dataset's image is searchable only when the same content was analyzed elsewhere.
- `datasets embeddings dataset=D` reports analysis freshness and progress.
  `datasets clustering dataset=D` returns 2D UMAP points, not raw embeddings; pass
  `nextOffset` as `offset` while `hasMore`, including with the default page size.
  `not_analyzed` means no layout exists; use returned IDs with `selected-images` for
  details. `create-embeddings` starts analysis; `delete-embeddings` cancels it, not images.

### Model analysis and similarity

- `models retrieve project=P model=M analysis=1` requires authentication and returns
  per-image validation `analysis` instead of model details; null means analysis is
  unavailable. A completed detection run with recorded per-image results is required;
  a missing dataset version or manifest returns scores with `traitsAvailable=false`
  and `coverage.mode="unavailable"`, not null analysis.
  Before generalizing, compare `population` with `retained` and read `coverage.mode`:
  only `full` covers every validation image. `traitsAvailable` gates `comparisons` (image
  traits versus F1); `cohorts.worst` and `.best` give whole-cohort `count` and `metrics`
  but only the first 100 rows as `examples`, whose labels come from the run's saved
  manifest, not the current dataset. `scatterSample.rows` are
  `[f1, width, height, pixels, aspectRatio, instanceCount]` points. Per-image
  `tp`/`fp`/`fn`/`f1` use IoU 0.50 at a confidence threshold the run did not record, so
  they cannot rebuild metrics at another threshold. Check the model's reported precision/recall
  before diagnosing poor performance; these counts alone do not establish deployment precision
  or explain a particular false positive.
- `models find-similar-training-images project=P model=M` searches public datasets from
  the run's worst validation images, excluding its training dataset. Use credentials with
  access to the model's workspace. The command returns candidates without adding them to
  the dataset. `hashes=H1,H2` must all come from
  `analysis.cohorts.worst.examples[].hash`; any other hash rejects the whole request. A run
  without a captured cohort returns an empty list; missing run/dataset identifiers or
  unavailable embeddings return errors instead.

### Connected storage

- Connected datasets (cloud storage or On Premise) are indexed in place, not copied.
  They cannot take appended uploads, versions, clones, batch annotation, or new embedding
  analysis; do not start analysis to obtain a missing clustering layout.
- Disconnecting an integration leaves provider objects intact but breaks dataset access
  until the same account reconnects. Roboflow credentials are separate from Platform
  credentials.

### Usage and billing

- `account storage` returns quotas as `usage.<resource>.current/limit/percent`, where
  `limit=-1` is unlimited; `details=true` adds the ten largest `breakdown.topItems`, not a
  full inventory. `billing usage-summary` returns plan usage and credits.
- `billing transactions from_=START to=END` uses `from_`, not `from`, and needs full ISO
  datetimes such as `2026-09-01T00:00:00Z`; bare dates are rejected. Timestamps are in
  `createdAt`.

### Compute

- Editing a model's `status` starts or stops nothing.
- `deployments list model=P/M` filters by a project's model, not a model ID or bare name.
  Use the returned `deployment` slug for `deployments retrieve`, `logs`, and `metrics`.
  Logs page with `nextPageToken` as `page_token`; `metrics range=` selects the window and
  `sparkline=true` returns the compact dashboard summary instead of the full response.
- Deployment `delete` is permanent; there is no trash for deployments.
- Export `delete` cancels a running conversion or removes the finished file; the source
  model is untouched.

The installed CLI is the authority: `ul version` shows the versions, `ul cloud <resource>
<operation> --help` lists valid arguments and choices, and error text beats any command
shape or caveat in this file. For endpoint semantics, the
[Platform API reference](https://docs.ultralytics.com/platform/api) and the live
`/openapi.json` win over memory.
