---
name: oci-ds-jobs
description: Manage OCI Data Science Jobs and Job Runs natively (list, details, create from script or container, start runs, monitor, cancel, delete). Use when orchestrating Python scripts or containers as batch jobs. Requires compartment_id and project_id (from oci-ds-setup). Prefer OCI CLI for listing/runs; use ADS Python for creation.
---

# OCI Data Science: Jobs & Runs

This skill manages Jobs and Job Runs without the MCP server.

## Preconditions
- compartment_id and project_id available (see oci-ds-setup).
- Local auth via ~/.oci/config. CLI installed. For creation flows, Python `oci` and `oracle-ads` are recommended.

## List Jobs
```bash
oci data-science job list --compartment-id <COMPARTMENT_OCID> --all \
  --query "data[].{id:id,name:'display-name'}" --output table
```

## Job Details
```bash
oci data-science job get --job-id <JOB_ID> --output json
```

## Create Job from Script (ADS Python)
- Provide conda env, shape. For Flex shapes (E4/E5), require `ocpus` and `memory_in_gbs`. Block storage must be >= 50 GB.
```bash
python - <<'PY'
from ads.jobs import Job, DataScienceJob, ScriptRuntime
compartment_id = '<COMPARTMENT_OCID>'
project_id = '<PROJECT_OCID>'
display_name = '<JOB_NAME>'
script_path = '<PATH_TO_SCRIPT>'  # local or remote path accessible at runtime
conda_env = 'generalml_p311_cpu_x86_64_v1'
shape = 'VM.Standard2.2'          # or 'VM.Standard.E5.Flex'
block_storage_size = 50
ocpus = None   # e.g., 2 for Flex
memory_in_gbs = None  # e.g., 16 for Flex

infra = (DataScienceJob()
    .with_compartment_id(compartment_id)
    .with_project_id(project_id)
    .with_shape_name(shape)
    .with_block_storage_size(block_storage_size))
if ocpus and memory_in_gbs:
    infra = infra.with_shape_config_details(memory_in_gbs=memory_in_gbs, ocpus=ocpus)

job = (Job(name=display_name)
    .with_infrastructure(infra)
    .with_runtime(ScriptRuntime().with_service_conda(conda_env).with_source(script_path)))
job.create()
print({'job_id': job.id, 'name': job.name})
PY
```

## Create Job from Container Image (ADS Python)
```bash
python - <<'PY'
from ads.jobs import Job, DataScienceJob, ContainerRuntime
compartment_id = '<COMPARTMENT_OCID>'
project_id = '<PROJECT_OCID>'
display_name = '<JOB_NAME>'
image = '<CONTAINER_IMAGE_URL>'  # e.g., iad.ocir.io/tenancy/namespace/repo:tag
shape = 'VM.Standard2.1'

job = (Job(name=display_name)
    .with_infrastructure(DataScienceJob().with_compartment_id(compartment_id).with_project_id(project_id).with_shape_name(shape))
    .with_runtime(ContainerRuntime().with_image(image).with_replica(1)))
job.create()
print({'job_id': job.id, 'name': job.name})
PY
```

## Start a Job Run (CLI)
```bash
oci data-science job-run create \
  --compartment-id <COMPARTMENT_OCID> \
  --project-id <PROJECT_OCID> \
  --job-id <JOB_ID> \
  --display-name "<RUN_NAME>" \
  --query "data.{id:id,state:'lifecycle-state',time:'time-created'}" --output table
```

## Latest Job Run Status (CLI)
```bash
oci data-science job-run list --compartment-id <COMPARTMENT_OCID> --job-id <JOB_ID> \
  --limit 1 --sort-by timeCreated --sort-order DESC \
  --query "data[0].{id:id,displayName:'display-name',state:'lifecycle-state',time:'time-created'}" --output table
```

## List Job Runs (CLI)
```bash
oci data-science job-run list --compartment-id <COMPARTMENT_OCID> --job-id <JOB_ID> --all \
  --query "data[].{id:id,displayName:'display-name',state:'lifecycle-state',time:'time-created'}" --output table
```

## Cancel Most Recent Job Run (CLI)
```bash
JOB_RUN_ID=$(oci data-science job-run list --compartment-id <COMPARTMENT_OCID> --job-id <JOB_ID> \
  --limit 1 --sort-by timeCreated --sort-order DESC --query 'data[0].id' --raw-output)
oci data-science job-run cancel --job-run-id "$JOB_RUN_ID"
```

## Delete Job (Destructive)
```bash
# Confirm with the user first
oci data-science job delete --job-id <JOB_ID> --force
```

## Tips
- Prefer job OCIDs over names for actions.
- Record created `job_id` in memory for subsequent runs/cleanup.
- Ensure artifacts and data sources are accessible to the job (Object Storage, VCN, policies).
