---
name: build-with-arcgis-maps-sdk-for-dotnet
license: Apache-2.0
description: "Use this skill when building or extending native GIS applications with ArcGIS Maps SDK for .NET. Choose it for WPF or WinUI apps on Windows, or .NET MAUI apps for Windows, Android, iOS, and Mac Catalyst. Follow its guidance to set up and license the SDK, configure authentication, display 2D maps and 3D scenes, use ArcGIS Online, ArcGIS Enterprise, or ArcGIS Location Platform maps and services, and implement location, offline workflows, geocoding, routing, spatial analysis, editing, and synchronization. Use it for SDK-specific architecture, toolkit integration, validation, and platform considerations; consult follow-esri-authentication-patterns to select an authentication model."
---

# Build with ArcGIS Maps SDK for .NET

Use ArcGIS Maps SDK for .NET to build native GIS features in WPF or WinUI apps on Windows, or .NET MAUI apps on Windows, Android, iOS, and Mac Catalyst. Match setup and implementation to the project's framework and target platform, and verify SDK support before choosing APIs or adding packages. The SDK supports maps and scenes, ArcGIS data and services, device location, offline workflows, geocoding, routing, spatial analysis, and feature editing.

## Application requirements

If the application's development requirements are unclear, use the `gather-arcgis-application-requirements` skill to review project context and clarify consequential unknowns before proceeding. Then apply this skill's technology-specific guidance, reusing requirements already clear from the request or project.

## ArcGIS account requirements

Developers must have one of the following ArcGIS accounts to create applications: ArcGIS Location Platform (free), or ArcGIS Online or ArcGIS Enterprise with a Creator, Professional, or Professional Plus user type. The account's user type, role, and privileges provide access to different resources and operations.

## Authentication

DO NOT SKIP: Refer to the `follow-arcgis-authentication-patterns` skill for ArcGIS authentication requirements, including the appropriate type of authentication for different audiences, use cases, and types of application. If the skill is not available, search the project for any existing authentication patterns, and if none are found, query the Esri MCP server for developer documentation for authentication best practices.

## Installation and setup

Follow these steps to install ArcGIS Maps SDK for .NET:

- First, ensure the development environment meets the [system requirements](https://developers.arcgis.com/net/system-requirements/).

- For new projects, install for the ArcGIS project templates using `dotnet new install Esri.ArcGISRuntime.ProjectTemplates`. Then create a new project for the appropriate target framework using one of these commands:
    - `dotnet new wpfmap`
    - `dotnet new winuimap`
    - `dotnet new mauimap`

- For existing projects, use the instructions in [Reference .NET Maps SDK in your project](https://developers.arcgis.com/net/install-and-set-up/#reference-arcgis-maps-sdk-for-net-in-your-projects). Refer to [UI framework requirements](https://developers.arcgis.com/net/system-requirements/system-requirements-for-300-1/#ui-framework-requirements) to ensure the target framework is compatible with the SDK. On Windows, only x64 and ARM64 are supported.

- For .NET MAUI projects, add a call to the [`UseArcGISRuntime`](https://developers.arcgis.com/net/api-reference/api/net/Maui/Esri.ArcGISRuntime.Maui.AppHostBuilderExtensions.UseArcGISRuntime.html) extension method in `MauiProgram.cs`, typically within the `CreateMauiApp` method. This is where API key, license, or other application settings are configured.

- Only add [ArcGIS Maps SDK Toolkit](https://developers.arcgis.com/net/toolkit/) or [Calcite .NET Toolkit](https://github.com/Esri/calcite-dotnet-toolkit/) packages if the task requires them; for MAUI, call their setup methods after `UseArcGISRuntime()`.

## How to query documentation

Installing this skill individually does not configure **Esri MCP server for developer documentation** (`esri-mcp-server-for-developer-documentation`). Add that server at `https://developers-mcp.arcgis.com/mcp` using your client's MCP settings, or install the full **ArcGIS SDKs and APIs** plugin (`arcgis-sdks-and-apis-plugin`). If the MCP server is unavailable, consult the linked official Esri documentation.

Documentation can be queried using the Esri MCP server for developer documentation (`esri-mcp-server-for-developer-documentation`):
```
https://developers-mcp.arcgis.com/mcp
```
Use the `search_esri_developer_docs` tool to surface authoritative documentation pages with `net-sdk` as the `focus_area` parameter in addition to a specified `search_term`. Use the `fetch_esri_developer_docs` tool with the `page_url` parameter set to return the full content of a documentation page in Markdown format. 

Clearly indicate any recommendations and assumptions that are not grounded in the official documentation. If the MCP server is unavailable, consult official documentation URLs below.

## Documentation links

- [Maps SDK for .NET Guide](https://developers.arcgis.com/net/): Main entry point to the .NET Maps SDK documentation.
- [Maps SDK for .NET API Reference](https://developers.arcgis.com/net/api-reference/): API documentation for all supported platforms.
- [ArcGIS Maps SDK for .NET Samples repository](https://github.com/Esri/arcgis-maps-sdk-dotnet-samples/tree/main): Sample code for WPF, WinUI, and .NET MAUI.
- [Topic: How to authenticate](https://developers.arcgis.com/net/security-and-authentication/how-to-authenticate/) - Describes the authentication methods supported by the .NET Maps SDK.
- [Topic: Implement user authentication](https://developers.arcgis.com/net/security-and-authentication/implement-authentication/) - Provides guidance on how to implement user authentication (such as OAuth 2.0) in the .NET Maps SDK.

## Patterns and guidelines

Refer to the programming patterns discussed in the [Programming patterns](https://developers.arcgis.com/net/programming-patterns/) guide topic.

- Where possible, use the [ArcGIS Maps SDK Toolkit](https://github.com/Esri/arcgis-maps-sdk-dotnet-toolkit/tree/main) for UI components and functionality rather than creating custom implementations from scratch.

- Favor use of the [MVVM architectural pattern](https://learn.microsoft.com/en-us/dotnet/architecture/maui/mvvm) for structuring .NET applications using the .NET Maps SDK when the complexity of the application warrants it. Use Toolkit's `GeoViewController` to drive GeoViews through a view model.

- Favor use of [Dependency Injection](https://docs.microsoft.com/en-us/dotnet/core/extensions/dependency-injection) for managing dependencies and promoting testability in .NET applications using the .NET Maps SDK when appropriate.

- Use [data binding](https://docs.microsoft.com/en-us/dotnet/desktop/wpf/data/data-binding-overview) to synchronize UI elements with underlying data models.

## Validation process

Validate the changed feature for its target framework and platform. If a check is blocked by unavailable devices, credentials, network access, or an ArcGIS account, report the limitation instead of claiming it passed.

- [ ] **Restore and build:** Restore and build the relevant project for the target framework and configuration. Resolve new errors and package incompatibilities; for .NET MAUI, confirm the target platform workload is installed.

- [ ] **Authentication and licensing (when changed):** Verify access to the intended resource, required privileges, and license level. For secured resources, test both denied unauthenticated access and the configured credential flow. Never expose credentials in output.

- [ ] **Runtime behavior:** On a supported target, exercise the changed feature's main success and failure paths. Confirm maps or scenes load and respond, and that loading or errors do not block the UI.
