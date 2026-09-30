---
name: oci-ds-projects
description: Manage OCI Data Science Projects natively using OCI CLI or Python ADS. Use to list, count, create, update, or delete Data Science projects. Requires a compartment_id (set via oci-ds-setup) and explicit confirmation for destructive actions.
---

# OCI Data Science: Projects

Use this skill to manage Data Science Projects without the MCP server. Prefer OCI CLI for simple list/update/delete; use ADS Python only when necessary.

## Preconditions
- compartment_id is known. If not, run oci-ds-setup to choose one and remember it (e.g., as oci.compartment_id).
- OCI CLI is configured (uses ~/.oci/config). Optional: Python packages oci and oracle-ads if using ADS flows.

## Common
- If you only have a project name, resolve to id first:
  ```bash
  # Replace <COMPARTMENT_OCID> and <PROJECT_NAME>
  oci data-science project list --compartment-id <COMPARTMENT_OCID> --all --output json \
    | jq -r '.data[] | select(."display-name"=="<PROJECT_NAME>") | .id'
  ```
- Always confirm with the user before update/delete.

## List Projects
```bash
oci data-science project list --compartment-id <COMPARTMENT_OCID> --all \
  --query "data[].{id:id,name:'display-name',description:description,timeCreated:time-created}" --output table
```

## Count Projects
```bash
oci data-science project list --compartment-id <COMPARTMENT_OCID> --all --output json | jq ' .data | length '
```

## Create Project
```bash
oci data-science project create \
  --compartment-id <COMPARTMENT_OCID> \
  --display-name "<DISPLAY_NAME>" \
  --description "<DESCRIPTION>" \
  --wait-for-state SUCCEEDED
```
- Capture the returned project id and store it as oci.project_id for reuse.

## Update Project
```bash
oci data-science project update \
  --project-id <PROJECT_ID> \
  [--display-name "<NEW_NAME>"] \
  [--description "<NEW_DESCRIPTION>"] \
  --wait-for-state SUCCEEDED
```

## Delete Project (Destructive)
```bash
# Confirm with the user first
oci data-science project delete --project-id <PROJECT_ID> --force --wait-for-state DELETED
```

## Notes
- Prefer IDs over names when executing commands.
- For teams, consider applying tags or naming conventions to make filtering simpler via --query.
- If ADS is preferred, ProjectCatalog from oracle-ads can also list/create/delete projects; however, the CLI above is usually simpler and avoids Python dependencies.
