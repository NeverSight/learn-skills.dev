---
name: oci-ds-deployments
description: Manage OCI Data Science Model Deployments natively (list, get, create from catalog model, activate, deactivate, delete). Use to serve models behind a managed HTTPS endpoint. Requires compartment_id and project_id; creation requires model_id. Prefer ADS Python for creation; use OCI CLI for lifecycle ops.
---

# OCI Data Science: Model Deployments

This skill deploys models and manages their lifecycle without the MCP server.

## Preconditions
- compartment_id and project_id available (see oci-ds-setup)
- Local auth via ~/.oci/config. OCI CLI installed. Python `oracle-ads` recommended for creation.
- Network/logging: If using custom VCN, capture `subnet_id`. Optionally configure Logging (log group, access/predict logs).

## List Model Deployments (CLI)
```bash
oci data-science model-deployment list --compartment-id <COMPARTMENT_OCID> --all \
  --query "data[].{id:id,name:'display-name',state:'lifecycle-state'}" --output table
```

## Get Model Deployment (CLI)
```bash
oci data-science model-deployment get --model-deployment-id <DEPLOYMENT_ID> --output json
```

## Create Deployment from Catalog Model (ADS Python, Conda runtime)
- Mirrors ADS GenericModel.deploy used in the MCP server. Defaults to shape VM.Standard.E2.1; for Flex shapes provide `deployment_ocpus` and `deployment_memory_in_gbs`.
```bash
python - <<'PY'
from ads.model.generic_model import GenericModel
model_id = '<MODEL_OCID>'
compartment_id = '<COMPARTMENT_OCID>'
project_id = '<PROJECT_OCID>'
display_name = '<DEPLOYMENT_NAME>'
# Optional infra/logging
subnet_id = None       # e.g., 'ocid1.subnet.oc1..xxxx'
log_group = None       # Log group OCID
access_log = None      # Log OCID for access logs
predict_log = None     # Log OCID for prediction logs
shape = 'VM.Standard.E2.1'  # or 'VM.Standard.E4.Flex' / 'VM.Standard.E5.Flex'
deployment_ocpus = None     # e.g., 2 (Flex only)
deployment_memory_in_gbs = None  # e.g., 16 (Flex only)

m = GenericModel.from_id(model_id)
kwargs = {}
if subnet_id: kwargs['subnet_id'] = subnet_id
if log_group: kwargs['deployment_log_group_id'] = log_group
if access_log: kwargs['deployment_access_log_id'] = access_log
if predict_log: kwargs['deployment_predict_log_id'] = predict_log
if shape: kwargs['deployment_instance_shape'] = shape
if deployment_ocpus: kwargs['deployment_ocpus'] = deployment_ocpus
if deployment_memory_in_gbs: kwargs['deployment_memory_in_gbs'] = deployment_memory_in_gbs

deployment = m.deploy(display_name=display_name, project_id=project_id, compartment_id=compartment_id, **kwargs)
print({'id': deployment.model_deployment.id, 'name': deployment.model_deployment.display_name, 'url': deployment.model_deployment.url})
PY
```

## Activate / Deactivate Deployment (CLI)
```bash
# Activate
oci data-science model-deployment activate --model-deployment-id <DEPLOYMENT_ID>

# Deactivate
oci data-science model-deployment deactivate --model-deployment-id <DEPLOYMENT_ID>
```

## Delete Deployment (Destructive, CLI)
```bash
# Confirm with the user first
oci data-science model-deployment delete --model-deployment-id <DEPLOYMENT_ID> --force
```

## Test the Endpoint
- The returned URL typically ends with /predict. Payload format depends on the saved model.
```bash
curl -s -X POST "<PREDICT_URL>" \
  -H "Content-Type: application/json" \
  -d '{"data": [[1.0, 2.0, 3.0]]}'
```

## Tips
- Prefer OCIDs over names for actions; map from names via list + jq filters.
- For Flex shapes, always collect both OCPUs and Memory.
- Ensure policies allow the deployment to access necessary Object Storage and VCN resources.
