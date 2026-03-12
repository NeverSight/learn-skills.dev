---
name: create-azure-agent
description: Interactive initialization script that generates Azure AI Foundry Agent API deployment wrappers (Python SDK and Bicep basics) from an existing Agent Skill. Use when adapting a skill into an Azure Foundry environment.
allowed-tools: Bash, Write, Read
---
# Create Azure AI Foundry Agent

## Overview

This skill scaffolds the deployment code necessary to instantiate an existing Open Agent-Skill as an **Azure AI Foundry Agent Service**. It reads a target `SKILL.md` and generates the Python SDK orchestration code and Bicep infrastructure templates required to deploy it within an Azure environment (with standard VNet and Cosmos DB limits in mind).

## Prerequisites

- An existing, governed Agent Skill (e.g., in `../../SKILL.md`).
- Azure CLI and Bicep tools (if deploying).

## Usage

You are the Azure Agent Scaffolder. When the user requests to deploy an existing skill to Azure Foundry, you must:

1. **Ask for the target skill:** Identify the path to the `SKILL.md` the user wants to adapt.
2. **Execute the scaffolder:** Run the python script to generate the Azure integration code.

```bash
# Example invocation
python ./scripts/scaffold_azure_agent.py --skill ../../skills/my-skill
```

## How It Works (The 128 Tool Limit)

Because Azure AI Foundry enforces a strict 128-tool limit, this scaffolder generates a *focused worker agent*. The generated python service (`azure_agent.py`) will precisely parse your `SKILL.md` into the `instructions` context, ensuring the Azure Agent is tightly coupled to the authoritative open standard without bloat.

## Outputs

The script will generate an `azure_deployment/` directory within the target skill containing:
1. `scaffold_azure_agent.py` - The `azure-ai-projects` Python SDK orchestration script.
2. `main.bicep` - The infrastructure-as-code template for the required Cosmos DB, AI Search, and Foundry Project.


## Next Actions
- Offer to run `audit-plugin` to validate the generated artifacts.
