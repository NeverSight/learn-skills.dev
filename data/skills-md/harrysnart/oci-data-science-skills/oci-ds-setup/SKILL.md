---
name: oci-ds-setup
description: Initialize and validate native OCI credentials and working context (compartment/project) for OCI Data Science tasks. Use at the start of any OCI Data Science operation to set compartment_id and optionally project_id without relying on an MCP server.
---

# OCI Data Science: Native Setup & Context

Use this skill to establish the working context for OCI Data Science operations and verify local prerequisites.

## Goals
- Verify preconditions (OCI CLI or Python SDK/ADS, local ~/.oci/config)
- Select and remember a compartment_id
- Optionally select and remember a project_id

## Preconditions
- OCI API key auth is configured locally (uses ~/.oci/config). Profile: default unless user specifies otherwise.
- Either the OCI CLI is installed (preferred) or Python packages `oci` and `oracle-ads` are available.
- Follow least-privilege IAM practices. Never expose secrets in logs or messages.

## Workflow

1) Gather existing context
- If the user already supplied `compartment_id` or a compartment name, use it.
- If the user supplied a `project_id` or project name, use it.

2) Discover Compartments (choose one)
- If `compartment_id` not known, list compartments and let the user pick:
  - Option A (CLI):
    - Run: `oci iam compartment list --compartment-id $(python -c "import oci,sys;print(oci.config.from_file().get('tenancy'))") --all --compartment-id-in-subtree true --query "data[].{name:name,id:id}" --output table`
  - Option B (Python):
    - Run a short script to print name/id JSON:
      ```bash
      python - <<'PY'
      import oci, json
      cfg = oci.config.from_file()
      client = oci.identity.IdentityClient(cfg)
      tenancy = cfg['tenancy']
      resp = oci.pagination.list_call_get_all_results(
          client.list_compartments, tenancy,
          compartment_id_in_subtree=True, access_level='ANY')
      print(json.dumps([{'name':c.name,'id':c.id} for c in resp.data], indent=2))
      PY
      ```
- Ask the user to pick a compartment by name or id. Store as memory key `oci.compartment_id`.

3) Choose Project (optional but recommended)
- If the task requires a project and `project_id` is not known:
  - If Python ADS is available, list projects:
    ```bash
    python - <<'PY'
    from ads.catalog.project import ProjectCatalog
    import json, os
    compartment_id = os.environ.get('OCI_COMPARTMENT_ID') or ''
    if not compartment_id:
        raise SystemExit('Set OCI_COMPARTMENT_ID env var first')
    pc = ProjectCatalog(compartment_id=compartment_id)
    projs = pc.list_projects()
    print(json.dumps([{'id':p.id,'name':p.display_name,'description':p.description} for p in projs], indent=2))
    PY
    ```
  - Map the chosen name to `project_id`, confirm with the user, and store as `oci.project_id`.

4) Confirm Context
- Echo the chosen `compartment_id` and, if set, `project_id` back to the user for confirmation before continuing.

## Notes
- Prefer IDs over names when executing actions.
- Update memory keys if the user changes compartments or projects.
- For destructive actions (delete_*), always ask for explicit confirmation first.
- If you hit auth or CLI errors, see [troubleshooting.md](docs/troubleshooting.md).
