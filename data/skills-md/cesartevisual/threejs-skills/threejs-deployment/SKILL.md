---
name: threejs-deployment
description: "Prepare and verify Three.js web builds, asset hosting, decoder paths, caching, and deployment compatibility."
---

# Build and Delivery

Use the project's installed versions and existing architecture. These instructions supplement the user's task; they do not authorize unrelated changes or external actions.

Inspect the existing build tool, hosting target, base path, browser requirements, and deployment authorization. Preserve project conventions. Prepare and validate the build even when publishing requires a later authorized step.

Keep Three.js and addons on a compatible revision and deduplicate conflicting instances. Verify peer dependencies before upgrades. Include only required loaders/helpers and lazy-load heavy optional paths when useful. Inspect the output rather than assuming tree-shaking removed unused code.

Resolve model, texture, decoder, worker, and WASM URLs through build-aware paths. Test the actual nested base path and direct navigation to application routes. Serve the right MIME types; verify asset responses are not HTML fallbacks.

Set CORS for legitimately cross-origin assets and CSP directives needed by the chosen worker/decoder setup. Require secure contexts for features that need them. Add cross-origin isolation only when the actual threaded/runtime feature requires it; account for third-party resource implications.

Use immutable caching for content-hashed assets and a coherent update strategy for HTML and manifests. Avoid stale service workers pairing new code with old decoders. Handle offline/error states according to product requirements.

Run a production preview and check representative assets, cache behavior, load failures, fallback devices, and route reloads. Publish only within existing authorization and report the deployed URL only after verifying it.

## API reference

Consult the [official documentation](https://vite.dev/guide/assets) for exact signatures and revision-specific behavior. If documentation access is unavailable, inspect installed types/source and state any remaining uncertainty.
