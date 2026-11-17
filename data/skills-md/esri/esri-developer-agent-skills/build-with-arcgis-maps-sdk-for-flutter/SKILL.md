---
name: build-with-arcgis-maps-sdk-for-flutter
license: Apache-2.0
description: "Use this skill to build, extend, debug, and explain native iOS and Android apps with ArcGIS Maps SDK for Flutter. Guide SDK setup, authentication, maps and scenes, layers, location, offline workflows, and optional Toolkit widgets."
---

# Build with ArcGIS Maps SDK for Flutter

ArcGIS Maps SDK for Flutter builds native iOS and Android apps with 2D/3D maps and spatial capabilities.

Flutter does not yet include every Native Maps SDK capability; verify API availability before relying on a feature.

Before building a new app, clarify its target platform, SDK version, ArcGIS product, and access or authentication requirements.

## Application requirements

If the application's development requirements are unclear, use the `gather-arcgis-application-requirements` skill to review project context and clarify consequential unknowns before proceeding. Then apply this skill's technology-specific guidance, reusing requirements already clear from the request or project.

## ArcGIS account requirements

Developers must have one of the following ArcGIS accounts to create applications: ArcGIS Location Platform (free), or ArcGIS Online or ArcGIS Enterprise with a Creator, Professional, or Professional Plus user type. The account's user type, role, and privileges provide access to different resources and operations.

## Authentication

DO NOT SKIP: Refer to the `follow-arcgis-authentication-patterns` skill for ArcGIS authentication requirements, including the appropriate type of authentication for different audiences, use cases, and types of application. If the skill is not available, search the project for any existing authentication patterns, and if none are found, query the Esri MCP server for developer documentation for authentication best practices.

Before implementing or changing authentication, consult the selected SDK version's authentication guidance and applicable native-platform setup sections. For OAuth, verify consistency between the application's OAuth registration, SDK configuration, and required native callback configuration.

## Installation and setup

Check the ArcGIS Maps SDK for Flutter system requirements and installation instructions for the selected SDK version and target platform. Follow the authoritative documentation rather than relying on a local summary of setup steps.

For iOS, query the ArcGIS SDK setup or migration instructions appropriate to the existing project and SDK version. If search results omit required steps, consult the exact [new iOS applications](https://developers.arcgis.com/flutter/install-and-set-up/#new-ios-applications) or [migration](https://developers.arcgis.com/flutter/install-and-set-up/#migrating-existing-ios-applications) section. Preserve custom project configuration when applying setup or migration instructions.

Use optional Toolkit widgets when they suit the requested experience.

## How to query documentation

Installing this skill individually does not configure **Esri MCP server for developer documentation** (`esri-mcp-server-for-developer-documentation`). Add that server at `https://developers-mcp.arcgis.com/mcp` using your client's MCP settings, or install the full **ArcGIS SDKs and APIs** plugin (`arcgis-sdks-and-apis-plugin`). If the MCP server is unavailable, consult the linked official Esri documentation.

Documentation can be queried using the Esri MCP server for developer documentation (`esri-mcp-server-for-developer-documentation`):
```
https://developers-mcp.arcgis.com/mcp
```
Use the `search_esri_developer_docs` tool to surface authoritative documentation pages with `flutter-sdk` as the `focus_area` parameter in addition to a specified `search_term`. Use the `fetch_esri_developer_docs` tool with the `page_url` parameter set to return the full content of a documentation page in Markdown format. 

Clearly indicate any recommendations and assumptions that are not grounded in the official documentation. If the MCP server is unavailable, consult official documentation URLs below.

## Documentation links

- [Developer guide](https://developers.arcgis.com/flutter/) - Concepts and workflows.
- [API reference](https://developers.arcgis.com/flutter/api-reference/reference/) - SDK classes and members.
- [Install and set up](https://developers.arcgis.com/flutter/install-and-set-up/) and [system requirements](https://developers.arcgis.com/flutter/system-requirements/) - Installation and supported platforms.
- [Authentication](https://developers.arcgis.com/flutter/security-and-authentication/) - Secure resource access.
- [Programming patterns](https://developers.arcgis.com/flutter/programming-patterns/) - Async resource loading.
- [Tutorials](https://developers.arcgis.com/flutter/tutorials/) and [samples](https://developers.arcgis.com/flutter/sample-code/) - Guided and runnable workflows.
- [Toolkit](https://developers.arcgis.com/flutter/toolkit/) and [Toolkit API reference](https://developers.arcgis.com/flutter/toolkit-api-reference/) - Optional widgets.
- [SDK parity](https://developers.arcgis.com/flutter/parity/) - Feature availability.

## Patterns and guidelines

- Give each `ArcGISMapView`, `ArcGISSceneView`, or `ArcGISLocalSceneView` its own controller via `controllerProvider`; configure it in the corresponding `onMapViewReady`, `onSceneViewReady`, or `onLocalSceneViewReady` callback.
- Await `load()` on `Loadable` resources before reading metadata. Check load status and errors, handle failures, retry with `retryLoad()`, and use `cancelLoad()` carefully for shared resources. Keep loading and error states visible to app users.
- Prefer suitable Toolkit widgets and use only APIs available in the selected Flutter SDK release; do not assume APIs from other Native Maps SDKs are available.

## Validation process

- Run the app on the target platform and confirm the requested map or scene workflow renders and behaves as expected.
- For secured resources, confirm authentication and access work without exposing credentials or tokens.
- For browser-based authentication, exercise the browser-to-app round trip on each target platform and confirm authentication completes. A successful build does not validate authentication; explicitly report any platform's callback flow that remains unverified.
- Exercise relevant loading and error states, and test offline behavior when the workflow requires it.
- Summarize what you verified and disclose meaningful limitations or checks you could not run. Explain SDK or version constraints when they affect the implementation.

## New application

1. Confirm the target platform, SDK version, ArcGIS product, authentication needs, and requested map or scene workflow.
2. Check the system requirements, create the Flutter app, add `arcgis_maps`, and configure the required platform settings.
3. Implement the requested workflow, including appropriate authentication and visible loading and error states.
4. Run the app on the target platform and verify the requested map or scene behavior.

## Existing application

1. Inspect the existing Flutter setup, SDK version, platform configuration, and authentication pattern.
2. Check compatibility, then add or update the SDK dependency and platform settings while preserving existing project configuration.
3. Implement the requested workflow within the app's existing structure, including appropriate loading and error handling.
4. Run the relevant workflow on the target platform and verify the change without regressing existing behavior.
