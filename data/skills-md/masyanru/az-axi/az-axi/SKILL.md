---
name: az-axi
description: "Use az-axi to discover, inspect, query, and safely mutate Azure through compact TOON CLI workflows over every Azure CLI module."
user-invocable: false
---

# az-axi

Compact Azure CLI for agents. Prefer az-axi over raw Azure JSON for discovery, inspect, and safe mutations.

Invoke with `npx -y az-axi <command>`. If output suggests `az-axi ...`, run it as `npx -y az-axi ...`.
Requires Azure CLI installed and authenticated in a human terminal. Anything that is not a read verb (list, show, get, query, list-*, show-*, ...) needs `--execute`. Secret values stay redacted unless `--reveal`.

## Workflow

1. `npx -y az-axi` for live subscription context.
2. `npx -y az-axi doctor` before production work.
3. First-class nouns skip the passthrough prefix: `group`, `logs`, `containerapp`, `aks`, `acr`, `eventhubs`, `keyvault`, `ad`, `monitor`.
4. Any other module: `npx -y az-axi az <module> <verb>`.
5. Follow `help:` next steps. Do not dump Azure CLI `--help` into context.

## Commands

```
usage: az-axi [command] [args] [flags]
commands[8]{command,use}:
  doctor,check login and required extensions
  services,list first-class nouns and modules
  find,search installed commands
  group,resource groups
  logs,Log Analytics query
  containerapp,Container Apps
  az,any Azure module via compact passthrough
  setup,install session hooks
flags[9]:
  --subscription, --resource-group/-g, --fields, --limit, --full, --reveal, --execute, --confirm-subscription (--help always allowed)
examples:
  az-axi
  az-axi doctor
  az-axi group list
  az-axi logs query -w <workspace-id> --analytics-query "Heartbeat | take 5"
  az-axi az network vnet list
  az-axi bench containerapp list
```
