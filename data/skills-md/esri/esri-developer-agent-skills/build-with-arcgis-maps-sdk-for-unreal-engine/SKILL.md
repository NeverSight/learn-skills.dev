---
name: build-with-arcgis-maps-sdk-for-unreal-engine
license: Apache-2.0
description: "Use this skill to build Unreal Engine apps with ArcGIS Maps SDK for Unreal Engine. Check current compatibility and install the plugin, choose Modes Panel, Components, Blueprints, or C++ for map setup, configure ArcGIS Maps and layers, and validate spatial references, authentication, camera behavior, and packaging. Consult linked SDK documentation and the API reference for current details."
---

# Build with ArcGIS Maps SDK for Unreal Engine

ArcGIS Maps SDK for Unreal Engine is a plugin for using real-world maps and 3D ArcGIS content in interactive 3D and XR experiences. Use it to bring geospatial data into Unreal Engine through the Modes Panel, Components, Blueprints, or the C++ API.

## Application requirements

If the application's development requirements are unclear, use the `gather-arcgis-application-requirements` skill to review project context and clarify consequential unknowns before proceeding. Then apply this skill's technology-specific guidance, reusing requirements already clear from the request or project.

## ArcGIS account requirements

Developers must have one of the following ArcGIS accounts to create applications: ArcGIS Location Platform (free), or ArcGIS Online or ArcGIS Enterprise with a Creator, Professional, or Professional Plus user type. The account's user type, role, and privileges provide access to different resources and operations.

## Authentication

DO NOT SKIP: Refer to the `follow-arcgis-authentication-patterns` skill for ArcGIS authentication requirements, including the appropriate type of authentication for different audiences, use cases, and types of application. If the skill is not available, search the project for any existing authentication patterns, and if none are found, query the Esri MCP server for developer documentation for authentication best practices.

## Installation and setup

1. Check the [system requirements](https://developers.arcgis.com/unreal-engine/system-requirements/) for the SDK release in use, including its supported Unreal Engine, operating system, IDE, and target platforms. Do not assume unlisted configurations are supported.
2. Install a compatible Unreal Engine version and C++ development environment. For a new project, use a Games or Simulation template and make it a C++ project with at least one C++ class; the SDK requires a C++ class for packaging.
3. Download the plugin from the [ArcGIS Maps SDK for Unreal Engine downloads page](https://developers.arcgis.com/unreal-engine/downloads/). Close Unreal Editor and the IDE, create a `Plugins` folder in the project directory, and extract the `ArcGISMapsSDK` folder into it. Reopen the project and confirm the plugin is enabled under **Edit > Plugins**.
4. For an existing project, follow the [existing-project installation guide](https://developers.arcgis.com/unreal-engine/install-and-set-up/add-the-plugin-to-an-existing-project/). If it has no C++ class, add one before packaging.
5. Configure ArcGIS access using the authentication guidance above. For upgrades, follow the [plugin upgrade guide](https://developers.arcgis.com/unreal-engine/install-and-set-up/upgrade-to-a-new-plugin-version/) and recheck compatibility.

## How to query documentation

Installing this skill individually does not configure **Esri MCP server for developer documentation** (`esri-mcp-server-for-developer-documentation`). Add that server at `https://developers-mcp.arcgis.com/mcp` using your client's MCP settings, or install the full **ArcGIS SDKs and APIs** plugin (`arcgis-sdks-and-apis-plugin`). If the MCP server is unavailable, consult the linked official Esri documentation.

Documentation can be queried using the Esri MCP server for developer documentation (`esri-mcp-server-for-developer-documentation`):
```
https://developers-mcp.arcgis.com/mcp
```
Use the `search_esri_developer_docs` tool to surface authoritative documentation pages with `unreal-engine-sdk` as the `focus_area` parameter in addition to a specified `search_term`. Use the `fetch_esri_developer_docs` tool with the `page_url` parameter set to return the full content of a documentation page in Markdown format. 

Clearly indicate any recommendations and assumptions that are not grounded in the official documentation. If the MCP server is unavailable, consult official documentation URLs below.

## Documentation links

- [ArcGIS Maps SDK for Unreal Engine](https://developers.arcgis.com/unreal-engine/) - Overview and current resources.
- [API reference](https://developers.arcgis.com/unreal-engine/api-reference/) - Verify C++ classes and members.
- [Install and setup](https://developers.arcgis.com/unreal-engine/install-and-set-up/) - Create a project and install the plugin.
- [System requirements](https://developers.arcgis.com/unreal-engine/system-requirements/) - Check current engine, IDE, and platform compatibility.
- [Existing-project setup](https://developers.arcgis.com/unreal-engine/install-and-set-up/add-the-plugin-to-an-existing-project/) - Add the plugin to an existing project.
- [Scene setting options](https://developers.arcgis.com/unreal-engine/install-and-set-up/scene-setting-options/) - Choose Modes Panel, Components, Blueprints, or C++.
- [Tutorials](https://developers.arcgis.com/unreal-engine/tutorials/) - Follow a map setup workflow for each authoring method.
- [Maps](https://developers.arcgis.com/unreal-engine/maps/) - Configure map type, origin, camera, and elevation.
- [Spatial references](https://developers.arcgis.com/unreal-engine/spatial-reference-and-data-analysis/spatial-references/) - Check coordinate system and layer compatibility.
- [View state](https://developers.arcgis.com/unreal-engine/maps/view-state/) - Inspect layer, elevation, and view status.
- [FAQ](https://developers.arcgis.com/unreal-engine/faq/) - Troubleshoot loading, camera, and packaging issues.
- [Sample code](https://developers.arcgis.com/unreal-engine/sample-code/) - Find working C++ examples.

## Patterns and guidelines

- Use C++ with the SDK API as the default approach; Use the SDK API directly; do not assume SDK Components are required. Use the Modes Panel for no-code map setup or SDK Components for Actor-based integration. Components can also be configured through C++. Use Blueprints when requested or required by the existing project.
- Configure the view and camera to load and display geographic content. For component-based workflows, attach an ArcGIS Camera Component to a camera.
- Choose a global or local map for the geographic extent. Set the map's origin and spatial reference deliberately; if unspecified, the first loaded layer can determine the map's spatial reference. Tiled layers must be compatible with the map's reference.
- For missing or misaligned data, inspect the ArcGIS View State Logging Component and Output Log, camera extent, layer source, authentication, supported formats, and spatial references.
- Keep a C++ class in the project to avoid packaging failures ( the SDK requires a C++ class for packaging). Validate both editor and Play modes; their camera views may differ.
- Consult the matching API reference and SDK samples instead of recreating map and layer behavior.

## Validation process

- [ ] Check engine, IDE, operating system, target platform, and plugin compatibility against the system requirements.
- [ ] Confirm the plugin is enabled and the project contains a C++ class before packaging.
- [ ] Verify authentication and access to required ArcGIS resources without exposing credentials.
- [ ] Run the level and confirm the ArcGIS Map, camera, expected extent, and basemap/data/elevation layers behave as intended.
- [ ] Check the Output Log and view-state messages for layer or elevation errors; verify spatial references and supported formats if content is missing.
- [ ] Package and test for the intended target platform when available.
