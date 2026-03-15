---
name: caira
description: Provides dynamic CAIRA context for coding agents building on the Azure AI platform (including Azure AI Foundry) by discovering current architectures and modules from the CAIRA repo, recommending a stack approach, and guiding scaffold/code generation across infra and app layers.
compatibility: Requires network access to github.com, api.github.com, and raw.githubusercontent.com.
metadata:
  author: pablozaiden
  version: "0.3.1"
---

# CAIRA

Use this skill when a user wants to build an AI, agent-based solution on the Azure AI platform (for example with Azure AI Foundry) using CAIRA and needs current context plus architecture decisions.

## Best-fit scenarios

- Projects that want to use Azure AI platform capabilities, including Azure AI Foundry.
- Teams building agent-based applications that need CAIRA-guided decisions across infrastructure, platform, and application layers.

## Core rules

- Treat the CAIRA repository as the single source of truth.
- Do not hardcode architecture names, module names, or fixed mappings.
- Discover what exists at runtime from repository/API listings, then decide.
- Support multiple layers (not only IaC): infrastructure, platform capabilities, application integration, and agent workflow composition.
- Default to passwordless/tokenless authentication for Azure access.
- Prefer Managed Identity or Azure Default Credential for Azure AI Foundry access.
- Avoid API keys unless the user explicitly requests key-based authentication.
- Before deployment/scaffolding actions, ask whether the user wants to customize provided deployment variables or use defaults when available.

## Dynamic discovery workflow

1. Resolve source version:
   - If user specifies a tag/branch/commit, use it.
   - Otherwise resolve latest release tag from CAIRA.
2. Discover available assets from the repository APIs:
   - reference architectures
   - modules
   - docs/guides/chatmodes/instructions
3. For each discovered architecture, inspect repository files (`README.md`, `*.tf`, `variables.tf`, `outputs.tf`) and infer capabilities from actual content.
4. Build a decision matrix from discovered facts and user requirements.
5. Present recommendation + alternatives, then require user confirmation.
6. Produce outputs (guidance, templates, or scaffold instructions) that stay aligned to discovered CAIRA content.

## Required requirement intake

Always gather requirements before recommending:

1. Environment intent (prototype, production, regulated, internal-only).
2. Networking/security needs (public/private connectivity, isolation, existing network constraints).
3. Agent capabilities and data dependencies needed by the application.
4. Application-layer expectations (services, APIs, UI, integration points, data flows, observability).
5. Delivery preference (reference/pinned modules vs copied files) and change constraints.
6. Authentication constraints (Managed Identity/Azure Default Credential by default; API key only by explicit request).
7. Deployment variable preference (customize provided variables or accept defaults when possible).

## Decision output template

When deciding, return:

- `discovered_assets`: architectures/modules/docs discovered from repo URLs
- `recommended_option`: selected architecture/approach from discovered set
- `alternatives`: other viable discovered options and trade-offs
- `stack_layers`: infra/platform/app/agent implications
- `auth_strategy`: passwordless default approach and any explicit exception requested by user
- `proposed_next_actions`: concrete, minimal next edits/commands

## Source-of-truth URLs

- Repository root: https://github.com/microsoft/CAIRA
- Latest release tag API: https://api.github.com/repos/microsoft/CAIRA/releases/latest
- Reference architecture listing API: https://api.github.com/repos/microsoft/CAIRA/contents/reference_architectures?ref=<tag_or_ref>
- Modules listing API: https://api.github.com/repos/microsoft/CAIRA/contents/modules?ref=<tag_or_ref>
- Docs listing API: https://api.github.com/repos/microsoft/CAIRA/contents/docs?ref=<tag_or_ref>
- Guides listing API: https://api.github.com/repos/microsoft/CAIRA/contents/guides?ref=<tag_or_ref>

## Additional repository references

- Reference architecture docs: https://github.com/microsoft/CAIRA/tree/main/reference_architectures
- Module docs: https://github.com/microsoft/CAIRA/tree/main/modules
- Documentation index: https://github.com/microsoft/CAIRA/tree/main/docs
- Guidance and instructions: https://github.com/microsoft/CAIRA/tree/main/.github
