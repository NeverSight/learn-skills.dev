---
name: oci-ds-models
description: Work with OCI Data Science Model Catalog natively (list, count, get details, download artifacts, manage model version sets). Use to inspect models, fetch artifacts locally, or explore version sets. Requires compartment_id; for artifact download you need model_id.
---

# OCI Data Science: Models & Model Version Sets

Manage models and model version sets without the MCP server using OCI CLI and optional Python/ADS snippets.

## Preconditions
- compartment_id available (see oci-ds-setup).
- Local auth via ~/.oci/config. OCI CLI installed. Optional: Python `oci` and `oracle-ads` for ADS flows.

## List Models (CLI)
```bash
oci data-science model list --compartment-id <COMPARTMENT_OCID> --all \
  --query "data[].{id:id,name:'display-name',state:'lifecycle-state',timeCreated:'time-created'}" --output table
```

## Model Count (CLI)
```bash
oci data-science model list --compartment-id <COMPARTMENT_OCID> --all --output json | jq '.data | length'
```

## Get Model Details (CLI)
```bash
oci data-science model get --model-id <MODEL_OCID> --output json
```

## Download Model Artifact
- Preferred (CLI):
```bash
# Downloads artifact tarball to the given path
oci data-science model-artifact get \
  --model-id <MODEL_OCID> \
  --file ./model_artifact.tar.gz
```

- Alternative (ADS Python): mirrors server behaviour
```bash
python - <<'PY'
from ads.model.generic_model import GenericModel
model_id = '<MODEL_OCID>'
target_dir = './model_artifact'  # directory to place extracted artifact
m = GenericModel.from_model_catalog(model_id, target_dir, force_overwrite=True, remove_existing_artifact=True)
print(m._to_yaml())
PY
```

## List Model Version Sets (CLI)
```bash
oci data-science model-version-set list --compartment-id <COMPARTMENT_OCID> --all \
  --query "data[].{id:id,name:name}" --output table
```

## Model Version Set Details (CLI)
```bash
oci data-science model-version-set get --model-version-set-id <MVS_OCID> --output json
```

## Tips
- Prefer using OCIDs when performing actions; map from names if needed using list filters/--query.
- The artifact tarball typically contains model.pkl or MLflow/ONNX/etc. structure; handle accordingly.
- Ensure you have authorization to access the model catalog in the selected compartment.
