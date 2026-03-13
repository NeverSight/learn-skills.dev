---
name: microsoft-development
description: Microsoft docs lookup, code samples, and SDK reference for Azure, .NET, Microsoft 365, Windows, and Power Platform via Microsoft Learn MCP. Use for API reference or official MS documentation retrieval.
license: Complete terms in LICENSE.txt
---

# Microsoft Development

Use this skill when the answer should come from Microsoft documentation rather than memory or third-party summaries.

## Current MCP Reality

Microsoft's Learn Docs MCP server is publicly documented and currently exposes these core tools:

- `microsoft_docs_search`
- `microsoft_docs_fetch`
- `microsoft_docs_extract_code_examples`
- `microsoft_docs_search_by_product`

Microsoft's getting-started docs also describe installation through `npx -y @microsoft/learn-docs-mcp`.

## Activation Conditions

- Verifying Azure SDK usage, limits, or configuration
- Looking up .NET, Graph, Windows, or Microsoft 365 APIs
- Pulling official code examples before implementation
- Checking product-specific guidance for Azure, Power BI, or Power Platform

## Recommended Workflow

1. Search first with `microsoft_docs_search`.
2. Narrow by product with `microsoft_docs_search_by_product` when results are broad.
3. Fetch the relevant page with `microsoft_docs_fetch` for details.
4. Extract code examples with `microsoft_docs_extract_code_examples` if the user needs working snippets.
5. Prefer official code and limits over recollection.

## Query Patterns

- `"Azure Container Apps scale rules"`
- `"BlobClient UploadAsync Azure.Storage.Blobs"`
- `product="power-bi" query="row level security dax"`
- `product="microsoft-graph" query="send mail application permissions"`

## Guardrails

- Use Microsoft Learn MCP for Microsoft-specific answers before browsing elsewhere.
- Treat package versions, quotas, and service capabilities as time-sensitive.
- If Learn MCP is unavailable in the current client, use the included scripts and references as local fallbacks, then browse official docs.

## References & Resources

### Documentation
- [Azure Services Quick Reference](./references/azure-services-quickref.md) - Common Azure services, SDK packages, and decision points
- [.NET Patterns](./references/dotnet-patterns.md) - Practical .NET design and dependency-injection patterns
- [Microsoft Learn MCP](./references/microsoft-learn-mcp.md) - Current tool names, install command, and query workflow

### Scripts
- [Azure Health Check](./scripts/azure-health-check.ps1) - Validate Azure login and inspect common resource health in a resource group

### Examples
- [Azure Function API Example](./examples/azure-function-api-example.md) - Example serverless API workflow tied back to official Microsoft docs

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [azure-integrations](../azure-integrations/SKILL.md) | Deploy and configure Azure resources after researching them |
| [powerbi-modeling](../powerbi-modeling/SKILL.md) | Power BI modeling guidance backed by Microsoft docs |
| [excel-sheet](../excel-sheet/SKILL.md) | Spreadsheet workflows in Microsoft-oriented environments |
| [word-document](../word-document/SKILL.md) | Word automation workflows in Microsoft-oriented environments |
| [powerpoint-ppt](../powerpoint-ppt/SKILL.md) | PowerPoint automation workflows in Microsoft-oriented environments |
