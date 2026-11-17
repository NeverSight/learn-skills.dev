---
name: cx-datasets
description: >
  Discover the datasets a Coralogix team can query with the `cx datasets` CLI —
  the fully qualified `<dataspace>/<dataset>` names DataPrime `source` commands
  need. Use when the user asks to "list datasets", "what datasets do we have",
  "which datasets can I query", "find datasets", "show dataspaces", "discover
  datasets", "what data does this team have", "available DataPrime sources",
  "filter datasets by pillar", "queryable sources", "dataset names for
  DataPrime", or wants to enumerate or filter the queryable datasets before
  running a DataPrime query.
metadata:
  version: "0.1.0"
---

# Datasets Skill

Coralogix data lives in **datasets**, addressed as `<dataspace>/<dataset>` —
e.g. `default/logs`, `default/rum.events`, `system/labs.limitViolations`. Every
DataPrime query starts with `source <dataspace>/<dataset>`, so before querying
an unfamiliar team (or a source you are not sure exists), list what is actually
queryable instead of guessing names.

## CLI Commands

| Command | Purpose | Key flags |
|---|---|---|
| `cx datasets list` | List every dataset queryable by the current profile's team | `--filter <DPXL>` |
| `cx datasets list -o json` | Same, as a JSON array of dataset rows | - |

- Supports `-p <profile>` (repeatable) for multi-profile fan-out; a `profile`
  key is added to each JSON row when more than one profile is targeted.
- Read-only — no `--yes` confirmation needed.

## Dataset Row Fields

| Field | Meaning |
|---|---|
| `dataspace` | The dataset's dataspace, e.g. `default` or `system` |
| `dataset` | The dataset name inside its dataspace, e.g. `logs`, `rum.events` |
| `pillar` | The pillar the data belongs to: `logs`, `spans`, `data`, ... |
| `entityType` | The entity type behind the dataset, e.g. `logs`, `browserLogs/v2`, `jsonData` |
| `version` | The latest dataset version |
| `teamId` | The team that owns the dataset |

Only read-enabled, latest-version datasets are returned. The `Source` column in
text output is the copy-pasteable `source` argument.

## Workflow

1. **List the datasets** to see what exists:

   ```bash
   cx datasets list
   cx datasets list -o json | jq -r '.[] | .dataspace + "/" + .dataset' | sort
   ```

2. **Narrow with a DPXL filter** when looking for a specific pillar or dataspace:

   ```bash
   cx datasets list --filter "<v1> \$d.pillar == 'logs'"
   cx datasets list --filter "<v1> \$d.dataspace == 'default' && \$d.pillar == 'data'"
   cx datasets list --filter "<v1> \$d.dataset.contains('rum')" -o json
   ```

3. **Query the dataset** with DataPrime, using the full source name:

   ```bash
   cx dataprime query --source default/checkoutservice_dataset 'filter $d.severity == ERROR'
   cx dataprime query --source system/labs.limitViolations 'filter $m.timestamp > now()-1h'
   ```

   `--source` is a `cx dataprime query` flag — `cx logs` and `cx spans` always
   query the legacy `logs`/`spans` datasets and take no source override.

## DPXL Filter Syntax

`--filter` takes a DPXL expression **including its version tag** — it must start
with `<v1>`. An expression missing the tag is rejected with a 400. In
double-quoted shells (bash/zsh), escape the `$` as `\$d` so the shell does not
expand it — the examples above are copy-paste safe.

Available fields: `$d.dataspace`, `$d.dataset`, `$d.pillar`, `$d.entityType`,
`$d.teamId`. Compare with `==` / `!=` and combine with `&&` / `||`. Substring
matching uses method-call syntax — `$d.dataset.contains('rum')` (case-sensitive
substring), not an infix `contains` operator.

## Key Principles

- **Never guess dataset names** — a query against a wrong source fails or, worse,
  silently returns the wrong data. List first, then query.
- **The source is `<dataspace>/<dataset>`** — both parts are needed in
  DataPrime `source` commands; `default/logs` not just `logs`.
- **Use `-o json` with `jq`** when you need just the source strings:
  `cx datasets list -o json | jq -r '.[] | .dataspace + "/" + .dataset'`.
- **Filter server-side** with `--filter` rather than listing everything and
  grepping locally — same result, less output to parse.
- **Multi-profile fan-out** with `-p <profile>` (repeatable) lists datasets
  across environments in one call.

## Related Skills

- **`cx-telemetry-querying`** — run the DataPrime queries against the datasets
  discovered here (logs, spans, metrics, RUM).
