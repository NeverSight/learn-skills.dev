---
name: build-with-arcgis-maps-sdk-for-unity
license: Apache-2.0
description: "Use this skill to build Unity apps with ArcGIS Maps SDK for Unity. Choose Map Creator, Components, or the C# API; add supported ArcGIS data; follow current setup, authentication, and compatibility guidance; and validate scenes and deployment targets. Consult the linked API reference for C# details."
---

# Build with ArcGIS Maps SDK for Unity

ArcGIS Maps SDK for Unity is a Unity plugin for using real-world maps and 3D ArcGIS content in interactive 3D and XR experiences. Use it to bring geospatial data into Unity scenes through Map Creator, SDK Components, or the C# API.

## Application requirements

If the application's development requirements are unclear, use the `gather-arcgis-application-requirements` skill to review project context and clarify consequential unknowns before proceeding. Then apply this skill's technology-specific guidance, reusing requirements already clear from the request or project.

## ArcGIS account requirements

Developers must have one of the following ArcGIS accounts to create applications: ArcGIS Location Platform (free), or ArcGIS Online or ArcGIS Enterprise with a Creator, Professional, or Professional Plus user type. The account's user type, role, and privileges provide access to different resources and operations.

## Authentication

DO NOT SKIP: Refer to the `follow-arcgis-authentication-patterns` skill for ArcGIS authentication requirements, including the appropriate type of authentication for different audiences, use cases, and types of application. If the skill is not available, search the project for any existing authentication patterns, and if none are found, query the Esri MCP server for developer documentation for authentication best practices.

## Installation and setup

1. Before creating or upgrading a project, check the [system requirements](https://developers.arcgis.com/unity/system-requirements/) for the SDK release in use. Verify Unity, render pipeline, and target-platform support.
2. Use HDRP or URP; the built-in render pipeline is unsupported. Check the setup guide for compatible render-pipeline package versions.
3. Install from the [Unity Asset Store](https://assetstore.unity.com/packages/tools/integration/arcgis-maps-sdk-for-unity-258537) or [SDK downloads](https://developers.arcgis.com/unity/downloads/). For tarballs, use Package Manager's **Add package from tarball**. For existing projects, follow the [setup guide](https://developers.arcgis.com/unity/install-and-set-up/add-the-plugin-to-an-existing-project/).
4. Import **Sample Content** if useful. Configure the scene with Map Creator, SDK Components, or the C# API according to the task.
5. Configure ArcGIS access using the authentication guidance above; keep credentials out of source control.
6. For upgrades, follow the [upgrade guide](https://developers.arcgis.com/unity/install-and-set-up/upgrade-to-a-new-plugin-version/) and recheck project compatibility.

## How to query documentation

Installing this skill individually does not configure **Esri MCP server for developer documentation** (`esri-mcp-server-for-developer-documentation`). Add that server at `https://developers-mcp.arcgis.com/mcp` using your client's MCP settings, or install the full **ArcGIS SDKs and APIs** plugin (`arcgis-sdks-and-apis-plugin`). If the MCP server is unavailable, consult the linked official Esri documentation.

Documentation can be queried using the Esri MCP server for developer documentation (`esri-mcp-server-for-developer-documentation`):
```
https://developers-mcp.arcgis.com/mcp
```
Use the `search_esri_developer_docs` tool to surface authoritative documentation pages with `unity-sdk` as the `focus_area` parameter in addition to a specified `search_term`. Use the `fetch_esri_developer_docs` tool with the `page_url` parameter set to return the full content of a documentation page in Markdown format. 

Clearly indicate any recommendations and assumptions that are not grounded in the official documentation. If the MCP server is unavailable, consult official documentation URLs below.

## Documentation links

- [ArcGIS Maps SDK for Unity](https://developers.arcgis.com/unity/) - Start here for an overview, key features, and links to current resources.
- [API reference](https://developers.arcgis.com/unity/api-reference/) - Look up SDK classes, methods, and properties before generating or changing C# code.
- [Install and setup](https://developers.arcgis.com/unity/install-and-set-up/) - Follow the current project creation and plugin installation workflow.
- [System requirements](https://developers.arcgis.com/unity/system-requirements/) - Check SDK-version-specific development and deployment compatibility.
- [Scene setting options](https://developers.arcgis.com/unity/install-and-set-up/scene-setting-options/) - Decide between Map Creator, Components, and the C# API.
- [Display a map with Map Creator](https://developers.arcgis.com/unity/maps/tutorials/display-a-map-ui/) - Create and configure a map through the editor UI.
- [Display a map with Components](https://developers.arcgis.com/unity/maps/tutorials/display-a-map-comp/) - Set up a map and layers using Unity components.
- [Display a map with the C# API](https://developers.arcgis.com/unity/maps/tutorials/display-a-map-api/) - Build a map setup through code.
- [Spatial references](https://developers.arcgis.com/unity/spatial-reference-and-data-analysis/spatial-references/) - Check coordinate-system support and map/data spatial-reference compatibility.
- [FAQ](https://developers.arcgis.com/unity/faq/) - Troubleshoot common data-loading and scene issues.
- [Sample code](https://developers.arcgis.com/unity/sample-code/) - Find working examples for SDK features.

## Patterns and guidelines

- Use C# scripting with the SDK API as the default approach; Use the SDK API directly; do not assume SDK Components are required. Use Map Creator for no-code map setup or SDK Components for GameObject-based integration. Components can also be configured through C#.
- Choose a global or local scene for the geographic extent. Ensure map and layer spatial references are compatible; the first layer may determine the map spatial reference.
- Preserve the ArcGIS Map's HPRoot setup, which addresses floating-point precision limits.
- For missing data, inspect view-state logs, camera extent, layer source, authentication, supported formats, and spatial-reference compatibility.
- Use the matching API reference and existing SDK components or samples instead of recreating SDK behavior.
- Check target-device requirements; editor success does not validate a player build.

## Validation process

- [ ] Check Unity, render pipeline, target platform, and installed SDK against the system requirements.
- [ ] Confirm the package and required Components are available; run a relevant sample when useful.
- [ ] Verify authentication and access to required ArcGIS resources without exposing credentials.
- [ ] Run the scene; check camera position, layer loading, Unity Console, and view-state logs.
- [ ] If data is missing, check spatial references, supported formats, and global/local scene choice.
- [ ] Build and test for the target platform when available.
