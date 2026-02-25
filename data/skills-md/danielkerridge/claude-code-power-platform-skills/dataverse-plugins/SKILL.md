---
name: dataverse-plugins
description: >
  Use when developing, registering, or deploying Dataverse plugins (C# server-side extensions).
  Covers the IPlugin interface, execution pipeline stages, entity images, common patterns
  (auto-numbering, cascading updates, validation), and registration/deployment.
  Triggers on: "plugin", "server-side logic", "business logic", "auto-number",
  "cascading update", "pre-operation", "post-operation", "plugin registration",
  "IPlugin", "execution pipeline", "plugin trace", "InvalidPluginExecutionException",
  "PreValidation", "PostOperation".
license: MIT
compatibility: "Dataverse SDK, .NET 4.6.2+, Plugin Registration Tool"
metadata:
  author: custom
  version: "1.0.0"
  platform: "Microsoft Power Platform / Dataverse"
---

# Dataverse Plugins Skill

You are an expert in developing, registering, and deploying Dataverse plugins — C# server-side
extensions that execute custom business logic in response to data operations (create, update,
delete, retrieve, etc.) in the Dataverse execution pipeline.

## CRITICAL RULES

1. **Plugins run in a sandbox** by default. They have restricted access to external resources
   (limited HTTP endpoints, no file system, no registry). Plan accordingly.

2. **2-minute timeout** for synchronous plugins. Long-running operations should use async mode
   or be offloaded to Power Automate / Azure Functions.

3. **Throw `InvalidPluginExecutionException`** to show user-facing errors. All other exceptions
   result in generic "Business Process Error" messages.

4. **Never use static variables** for state. Plugin instances are cached and reused across
   requests. Use `IPluginExecutionContext.SharedVariables` for pipeline-scoped state.

5. **Always register entity images** when you need pre/post field values. Don't make extra
   Retrieve calls when an image would suffice.

6. **Test with Plugin Trace Log** enabled. Set the org's trace log setting to "All" during
   development, then reduce for production.

## Quick Reference

| Concept | Details |
|---|---|
| Interface | `Microsoft.Xrm.Sdk.IPlugin` |
| Entry point | `Execute(IServiceProvider serviceProvider)` |
| Error handling | Throw `InvalidPluginExecutionException` |
| Timeout | 2 minutes (sync), 24 hours (async) |
| Isolation | Sandbox (default) or None (on-premises only) |
| Assembly size | 16MB max |
| Registration | Plugin Registration Tool (PRT) or pac CLI |

## Resource Files

- `resources/plugin-anatomy.md` -- IPlugin interface, services, context, base class pattern
- `resources/execution-pipeline.md` -- Pipeline stages, sync/async, entity images
- `resources/common-patterns.md` -- Auto-numbering, validation, cascading updates, error handling
- `resources/registration-deployment.md` -- PRT, pac CLI, step registration, debugging
