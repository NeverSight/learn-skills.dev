---
name: build-with-arcgis-maps-sdk-for-kotlin
license: Apache-2.0
description: "Build, extend, debug, and explain Android apps with ArcGIS Maps SDK for Kotlin using official docs. Cover Gradle, SDK/Toolkit, Compose, authentication, starter maps/scenes, layers, graphics, queries, editing, location, geocoding, routing, offline workflows, and validation. Excludes Kotlin Multiplatform and other ArcGIS SDKs."
---

# Build with ArcGIS Maps SDK for Kotlin

ArcGIS Maps SDK for Kotlin is a kotlin-first powerful mapping library for building offline-enabled, native mobile applications that incorporate mapping & location capabilities such as 2D and 3D visualization, geocoding, routing, navigation, editing, and spatial analysis. Apps can be deployed to android devices such as mobile phones and tablets. It supports accessing content from web services in ArcGIS Location Platform, ArcGIS Online, and ArcGIS Enterprise, as well as many OGC services and popular geodata file formats. The SDK includes an API designed to work seamlessly with Jetpack Compose UI and structured concurrency via coroutines and flows, many open-source toolkit components that provide ready-made UI for common user workflows, getting started tutorials, comprehensive samples, and rich API reference documentation and conceptual guide topics.

## Application requirements

If the application's development requirements are unclear, use the `gather-arcgis-application-requirements` skill to review project context and clarify consequential unknowns before proceeding. Then apply this skill's technology-specific guidance, reusing requirements already clear from the request or project.

## ArcGIS account requirements

Developers must have one of the following ArcGIS accounts to create applications: ArcGIS Location Platform (free), or ArcGIS Online or ArcGIS Enterprise with a Creator, Professional, or Professional Plus user type. The account's user type, role, and privileges provide access to different resources and operations.

## Authentication

DO NOT SKIP: Refer to the `follow-arcgis-authentication-patterns` skill for ArcGIS authentication requirements, including the appropriate type of authentication for different audiences, use cases, and types of application. If the skill is not available, search the project for any existing authentication patterns, and if none are found, query the Esri MCP server for developer documentation for authentication best practices.

## Installation and setup

1. Create a new Compose project in Android Studio or open an existing project where you want to integrate ArcGIS Maps SDK for Kotlin. Follow [instructions](https://developers.arcgis.com/kotlin/install-and-set-up/) for the most-up-to-date setup and project configuration.
2. Inspect Gradle files/version catalog, Android manifest, SDK version, UI framework, and authentication. Match documentation to the installed version, including 200.x; never silently upgrade. For migrations, read version-specific release and migration guidance before changing dependencies or APIs.
3. Check release requirements for Android Studio, Android API levels, Gradle/Android Gradle Plugin, Kotlin/Compose, JDK, architectures, and graphics. Complete configuration and available command-line checks; report manual tool, emulator/device, and account prerequisites. Request credentials through secure local configuration, not chat.
4. For a new starter map app, use the official **Display a map** tutorial as the implementation model, not merely a reference. Read the tutorial before generating code, and follow its project setup, code organization, map creation, and MapView integration patterns. Default to Jetpack Compose and Kotlin DSL unless the user specifies otherwise. Select the authentication method according to the Authentication section above. When the selected authentication method is API key or OAuth user authentication, follow the corresponding Display a map tutorial workflow directly. For these two workflows, do not replace the tutorial's authentication flow with a custom design or add screens or sign-in steps beyond those used by the selected tutorial workflow unless the user explicitly requests them. Do not add architectural layers, configuration wrappers, or custom validation unless explicitly requested or required by the documented authentication flow. For existing apps, preserve their UI framework, architecture, and working map/authentication flows; merge changes rather than replacing files with tutorial code.
5. Add Esri Maven `https://esri.jfrog.io/artifactory/arcgis` and SDK dependency `com.esri:arcgis-maps-kotlin`. Use the Toolkit compatibility table to select SDK/Toolkit versions and its bill of materials (BOM) to align modules. Add only needed modules: `geoview-compose` for Compose views and `authentication` when user-authentication UI is needed. Follow the selected release's setup, not current version numbers in older apps.
6. Configure `INTERNET` permission and required view graphics features. Request location permissions only for location features; handle denial/restrictions. Use Android scoped storage for offline files, not obsolete or unrelated permissions.
7. Follow the authentication guidance above and Kotlin-specific docs. Configure API keys and licensing with documented Kotlin APIs, not another SDK's initialization methods. Never commit/log credentials or embed client secrets. APK configuration, including build-generated values, is not secret storage.
8. Sync Gradle, build, and verify a starter map on a supported emulator/device. Build success does not prove rendering or authorized resource access.

## How to query documentation

Installing this skill individually does not configure **Esri MCP server for developer documentation** (`esri-mcp-server-for-developer-documentation`). Add that server at `https://developers-mcp.arcgis.com/mcp` using your client's MCP settings, or install the full **ArcGIS SDKs and APIs** plugin (`arcgis-sdks-and-apis-plugin`). If the MCP server is unavailable, consult the linked official Esri documentation.

Documentation can be queried using the Esri MCP server for developer documentation (`esri-mcp-server-for-developer-documentation`):
```
https://developers-mcp.arcgis.com/mcp
```
Use the `search_esri_developer_docs` tool to surface authoritative documentation pages with `kotlin-sdk` as the `focus_area` parameter in addition to a specified `search_term`. Use the `fetch_esri_developer_docs` tool with the `page_url` parameter set to return the full content of a documentation page in Markdown format. 

Clearly indicate any recommendations and assumptions that are not grounded in the official documentation. If the MCP server is unavailable, consult official documentation URLs below.

## Documentation links

- [Kotlin guide](https://developers.arcgis.com/kotlin/) - capabilities, release notes, migrations; [200.x guide](https://developers.arcgis.com/kotlin/v200/) for existing 200.x apps.
- [Install and set up](https://developers.arcgis.com/kotlin/install-and-set-up/) - dependencies, manifest, system requirements.
- [Toolkit](https://developers.arcgis.com/kotlin/toolkit/) - components, modules, SDK compatibility.
- [SDK API](https://developers.arcgis.com/kotlin/api-reference/) and [Toolkit API](https://developers.arcgis.com/kotlin/toolkit-api-reference/) - imports, signatures, version availability.
- [How to authenticate](https://developers.arcgis.com/kotlin/security-and-authentication/how-to-authenticate/) - Kotlin implementation of the selected authentication model.
- [Display a map](https://developers.arcgis.com/kotlin/maps-2d/tutorials/display-a-map/) - starter project; [tutorials](https://developers.arcgis.com/kotlin/tutorials/) for other features.
- [Layer types](https://developers.arcgis.com/kotlin/layers/layer-types/) - data sources, view support, query/edit/offline capabilities.
- [Samples](https://developers.arcgis.com/kotlin/sample-code/) and [Kotlin samples repository](https://github.com/Esri/arcgis-maps-sdk-kotlin-samples/tree/main) - match the app's SDK version.
- [GeoView patterns with Jetpack Compose](https://developers.arcgis.com/kotlin/programming-patterns/geoview-patterns-with-jetpack-compose/) - state, view proxies, concurrency.
- [Loading resources asynchronously](https://developers.arcgis.com/kotlin/programming-patterns/loading-resources-asynchronously/) - loading, failures, retries.
- [Offline maps, scenes, and data](https://developers.arcgis.com/kotlin/offline-maps-scenes-and-data/) - downloads, packages, synchronization.
- [License and deployment](https://developers.arcgis.com/kotlin/license-and-deployment/), [license levels and capabilities](https://developers.arcgis.com/kotlin/license-and-deployment/license-levels-and-capabilities/), and [license by API](https://developers.arcgis.com/kotlin/license-and-deployment/license-by-api/) - requirements for the operations and data used.

## Patterns and guidelines

Follow the [Programming patterns](https://developers.arcgis.com/kotlin/programming-patterns/) chapter for the SDK version in use. Read the relevant subpages before implementing a pattern; version-matched official documentation takes precedence over the reminders below. In the Programming patterns chapter, pay particular attention to [Compose-specific patterns](https://developers.arcgis.com/kotlin/programming-patterns/geoview-patterns-with-jetpack-compose/), [coroutine usage](https://developers.arcgis.com/kotlin/programming-patterns/concurrent-geoview-tasks/), and use of the composable MapView, Scene View, and LocalSceneView from the Toolkit, not the same-named classes from the ArcGIS Maps SDK for Kotlin API.
- Verify Kotlin APIs with `kotlin-sdk` queries that include the symbol, feature, and SDK version. Without MCP, use official documentation and disclose uncertainty. Never invent APIs or assume another SDK's names or behavior translate directly; verify a Kotlin equivalent before recommending it.
- Adapt official samples and suitable Toolkit components to the existing app. Preserve its UI framework, styling, architecture, dependency management, and working map/authentication flows; do not introduce a new framework solely to match a sample.
- Keep Compose map/scene models stable, collect state lifecycle-aware, and scope asynchronous work to the owning lifecycle. Avoid blocking the UI or repeating work during recomposition. Handle failures and empty results explicitly, preserve coroutine cancellation, and surface loading/error states; request or job completion alone does not prove success.

## Validation process

Validate for the app's SDK version, build variant, and supported Android target. Report unavailable tooling, device, credentials, account, network, or data and the checks still needed; never claim unperformed checks passed. Keep all credentials, tokens, and secrets out of source, logs, and validation output.

- [ ] **Dependencies and build:** Verify toolchain, SDK/Toolkit compatibility, dependencies/imports, manifest, and device graphics/API support. Run the Gradle wrapper's `assembleDebug` or appropriate variant task, relevant tests, and lint. Compare warnings with the baseline; report new errors/warnings and skipped checks.
- [ ] **Authentication and access:** Check audience/resource fit, portal/item/service privileges, and applicable OAuth redirects. Access an intended resource; for secured resources, verify unauthenticated rejection and authorized success. Test sign-in cancellation/denial where applicable.
- [ ] **Runtime behavior:** On a supported emulator/device, exercise changed success/failure paths. Check map/scene content, individual layers, rendering, pan/zoom, relevant GeoView interactions, and Logcat. Loading/errors must be visible without freezing the UI; a build alone proves no runtime behavior.
- [ ] **Lifecycle and workflow edges:** Test rotation, background/resume, and navigation away/back for lost state, repeated work, and coroutine cancellation. For features used, test permission denial, network loss/retry, empty results, editing results, and job failures. For offline work, test local content without connectivity and requested synchronization after reconnecting.
- [ ] **Patterns and regressions:** Review the guardrails above, including coroutine/`Result` handling and Toolkit reuse. Preserve existing architecture/dependency management; run relevant existing tests and check adjacent map/layer/workflow behavior. A starter map is not a full regression pass.
- [ ] **Production readiness:** Verify attribution and required license levels/extensions for actual operations/data. Authentication success is not licensing compliance; distinguish expected developer-use watermarks from production issues.
