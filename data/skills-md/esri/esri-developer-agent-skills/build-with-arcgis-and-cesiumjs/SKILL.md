---
name: build-with-arcgis-and-cesiumjs
license: Apache-2.0
description: Build and troubleshoot browser-based 3D mapping apps with CesiumJS and ArcGIS. Use for ArcGIS basemaps, terrain, feature and map services, I3S/scene layers, geocoding, routing, places, and spatial analysis. Guide setup, authentication, ArcGIS REST JS integration, coordinate handling, attribution, and performance using current Esri documentation.
---

# Build with CesiumJS and ArcGIS

CesiumJS is an open-source JavaScript library for high-performance, precise, interactive 3D globes and maps. Combine it with ArcGIS services and ArcGIS REST JS for browser-based 3D scenes using basemaps, elevation, hosted data, 3D content, and location services.

## Application requirements

If the application's development requirements are unclear, use the `gather-arcgis-application-requirements` skill to review project context and clarify consequential unknowns before proceeding. Then apply this skill's technology-specific guidance, reusing requirements already clear from the request or project.

## ArcGIS account requirements

Developers must have one of the following ArcGIS accounts to create applications: ArcGIS Location Platform (free), or ArcGIS Online or ArcGIS Enterprise with a Creator, Professional, or Professional Plus user type. The account's user type, role, and privileges provide access to different resources and operations.

## Authentication

DO NOT SKIP: Refer to the `follow-arcgis-authentication-patterns` skill for ArcGIS authentication requirements, including the appropriate type of authentication for different audiences, use cases, and types of application. If the skill is not available, search the project for any existing authentication patterns, and if none are found, query the Esri MCP server for developer documentation for authentication best practices.

## Installation and setup

Infer the app's requirements from the prompt and project files. If the framework, deployment target, or intended ArcGIS services are unclear and affect the implementation, ask before proceeding. Identify the ArcGIS services and data sources the app needs, and verify they support the required operations. Use CesiumJS for rendering and ArcGIS REST JS for ArcGIS Location Services and service requests.

### New application

Use a minimal starter appropriate to the requested setup. For lightweight demos, a versioned CDN can avoid bundler setup. For npm builds, configure Cesium’s worker and static asset paths, and verify them in both development and production.

#### New application with CDN

Load CesiumJS and its `Widgets/widgets.css` stylesheet from the same versioned Cesium CDN release URL documented in the [CesiumJS quickstart](https://cesium.com/learn/cesiumjs-learn/cesiumjs-quickstart/). Use the current release and supported URL format from the [CesiumJS API reference](https://cesium.com/learn/cesiumjs/ref-doc/). Load ArcGIS REST JS modules from a CDN only for the services the app uses. Prefer this approach for demos, tutorials, samples, and lightweight quickstarts; serve the app over HTTP(S), not `file://`.

#### New application with npm

Use Vite unless another framework is specified; supported frameworks include React, Angular, Vue, and Svelte. If using a vite template or another framework-specific template, remove all template files that are not relevant to the user's request (e.g. counter.js). Install `cesium` and import CesiumJS through the project's package manager and module system. Configure the bundler to copy Cesium's `Workers`, `ThirdParty`, `Assets`, and `Widgets` directories to static output, and set `CESIUM_BASE_URL` to their served location before importing CesiumJS. On Windows, normalize paths used by glob-based copy plugins. Import the Cesium widget stylesheet. Add only the ArcGIS REST JS packages needed by the app, such as `@esri/arcgis-rest-request` and the feature-service, geocoding, routing, places, or elevation modules. Use this approach for larger applications and production builds.

### Existing application

Before installing or changing packages, inspect the package manifest and lockfile, framework, module format, bundler, and existing static-asset configuration. Follow the project's package manager, import conventions, and build setup; preserve its credential and environment-variable patterns. Add Cesium's static directories and `CESIUM_BASE_URL` using the existing bundler's supported configuration, and avoid introducing a second build system.

### Service credentials and viewer setup

Set the ArcGIS access token before making ArcGIS requests or creating ArcGIS-backed providers. Cesium ion tokens are separate and only needed for ion resources. Restrict public API keys by referrer; never expose client secrets, and register exact OAuth redirect URIs. Users must create and restrict credentials and configure redirects or ion tokens as required by the chosen services. Give the viewer a non-zero size and load Cesium's widget stylesheet.

## How to query documentation

Installing this skill individually does not configure **Esri MCP server for developer documentation** (`esri-mcp-server-for-developer-documentation`). Add that server at `https://developers-mcp.arcgis.com/mcp` using your client's MCP settings, or install the full **ArcGIS SDKs and APIs** plugin (`arcgis-sdks-and-apis-plugin`). If the MCP server is unavailable, consult the linked official Esri documentation.

Documentation can be queried using the Esri MCP server for developer documentation (`esri-mcp-server-for-developer-documentation`):
```
https://developers-mcp.arcgis.com/mcp
```
Use the `search_esri_developer_docs` tool to surface authoritative documentation pages with `cesiumjs` as the `focus_area` parameter in addition to a specified `search_term`; Use the `arcgis-rest-js` focus area for ArcGIS REST JS queries. Use the `fetch_esri_developer_docs` tool with the `page_url` parameter set to return the full content of a documentation page in Markdown format. 

Clearly indicate any recommendations and assumptions that are not grounded in the official documentation. If the MCP server is unavailable, consult official documentation URLs below.


## Documentation links

- [CesiumJS and ArcGIS](https://developers.arcgis.com/cesiumjs/) - Start here for supported workflows and tutorials.
- [Get started](https://developers.arcgis.com/cesiumjs/get-started/) - Set up credentials and display a first scene.
- [CesiumJS API reference](https://cesium.com/learn/cesiumjs/ref-doc/) - Look up CesiumJS classes, methods, and properties.
- [CesiumJS installation quickstart](https://cesium.com/learn/cesiumjs-learn/cesiumjs-quickstart/) - Set up CesiumJS with npm or a CDN and configure a development environment.
- [Scenes and basemaps](https://developers.arcgis.com/cesiumjs/scenes/) - Add ArcGIS basemap imagery and elevation.
- [Layers](https://developers.arcgis.com/cesiumjs/layers/) - Display I3S/3D content and query or visualize features.
- [Reverse geocoding](https://developers.arcgis.com/cesiumjs/geocode-and-search/reverse-geocode/) - Add ArcGIS geocoding to a scene.
- [Route and directions](https://developers.arcgis.com/cesiumjs/route-and-directions/find-a-route-and-directions/) - Use ArcGIS routing services.
- [Nearby places](https://developers.arcgis.com/cesiumjs/places/places-nearby/) - Search ArcGIS Places.
- [Find an elevation](https://developers.arcgis.com/cesiumjs/elevation/find-the-elevation-of-a-point/) - Query ArcGIS elevation services.
- [Migration](https://developers.arcgis.com/cesiumjs/migration/) - Check current integration patterns and changes from earlier implementations.
- [ArcGIS REST JS](https://developers.arcgis.com/arcgis-rest-js/) - Find REST JS modules and API references for ArcGIS service requests.
- [Esri attribution](https://esriurl.com/attribution) - Follow credit and copyright requirements for ArcGIS content.

## Patterns and guidelines

- Use CesiumJS for scene rendering/interaction and ArcGIS REST JS for ArcGIS location, data, and analysis requests.
- Match source to content: imagery providers for basemaps, terrain providers for elevation, `I3SDataProvider` for I3S, and `GeoJsonDataSource` for suitably sized feature query results.
- Use REST JS `queryFeatures` to query a feature service's layer endpoint (`.../FeatureServer/<layerId>`) as GeoJSON. Request only needed fields and geometry. Paginate transfer-limited queries by explicitly checking `exceededTransferLimit` and use `queryAllFeatures` for large requests. Await `GeoJsonDataSource.load` before adding the source to `viewer.dataSources`.
- Style the loaded Cesium entities by geometry type: billboards or points, polylines, and polygons. Read attributes from entity.properties and use their public getValue(...) method; avoid relying on internal fields such as _value
- Follow the installed CesiumJS API reference and Esri migration guide; APIs evolve. Use supported async provider creation and handle rejected promises/service errors.
- Keep ArcGIS and ion credentials separate. Restrict browser API keys, use OAuth or server-side access for user-specific/confidential resources, and preserve required Esri/service credits including "Powered by Esri" and the basemap's data-source credits. When loading feature layers as GeoJSON, retrieve attribution from the hosted item's Acknowledgements and pass it as a Cesium `Credit`
- Verify coordinate order, spatial reference, units, and vertical datum when combining data. Geographic positions commonly use longitude, latitude order.
- Prefer tiled/streamed services such as I3S for large datasets. Vector tiles are not supported. Disable unused viewer widgets and avoid unnecessary picking calls.
- Terrain caveat: Some feature styling, outlines, and layer ordering may not work as expected with terrain enabled. Recommend testing the target Cesium version and disabling terrain only if those styling limitations matter.
- Handle credentials safely: Identify the environment-variable names the service expects; verify them without printing their values. Treat browser API keys as public credentials and recommend setting least-privilege and referrer restrictions.

## Validation process

- [ ] Check build errors. Don’t treat a successful build as proof Cesium is configured: check each static asset folder, then smoke-test the production preview.
- [ ] Viewer styles/container are correct; scene initializes without console errors.
- [ ] Verify the map actually renders: Confirm the viewer has a nonzero size, ArcGIS tile requests succeed, and the basemap appears. Handle provider errors and update the loading status; if rendering stalls after layer setup, request a scene render and retest.
- [ ] ArcGIS and any required ion authentication work independently; no client secret is exposed.
- [ ] Required layers/workflows work, including empty/error cases; queries honor capabilities, coordinates, and transfer limits.
- [ ] 3D data aligns vertically, credits remain visible, and performance is acceptable for representative data/devices.
- [ ] Browser visual smoke test confirms viewer, basemap, and data render correctly. Avoid local-server conflicts by checking if the chosen port is already in use. Wait for asynchronous map tiles and layers before judging a screenshot.
- [ ] Check console errors before diagnosing the map itself.
- [ ] Test missing and null feature attributes explicitly; validate values before converting them, especially numeric fields.
- [ ] Note Cesium bundle-size warnings during validation; decide whether code splitting is needed rather than ignoring the warning.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Blank viewer | Check container dimensions, styles, and Cesium static asset URL. |
| Authorization error | Verify the failed service's credential/privileges; check ArcGIS and ion tokens separately. |
| Missing layers | Check URL, access, response format, coordinate order, and vertical datum. |
| Layer misalignment with ground | Check terrain, other elevation providers, and vertical datum of the layer. |
| Incomplete query/credits | Handle transfer limits; keep Cesium credits visible and add required service credits. |
