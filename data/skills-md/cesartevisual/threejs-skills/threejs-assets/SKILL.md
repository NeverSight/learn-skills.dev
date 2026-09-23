---
name: threejs-assets
description: "Load, validate, compress, cache, and release glTF models, textures, decoder assets, and user-supplied 3D files."
---

# Asset Loading and Optimization

Use the project's installed versions and existing architecture. These instructions supplement the user's task; they do not authorize unrelated changes or external actions.

Inventory format, dimensions, units, animation clips, material features, texture sizes, provenance, and transfer size. Prefer a web-ready glTF/GLB pipeline when conversion is acceptable. Preserve source files and semantic names needed by application logic.

Configure GLTFLoader with the decoders the asset actually requires. Match decoder/transcoder binaries to the installed libraries, resolve their URLs through the build's asset conventions, and detect KTX2 support against the active renderer. Do not assume a compressed file needs only a single network request.

Represent loading, ready, failure, and retry explicitly. Unknown content length calls for indeterminate progress. On navigation or rapid selection, guard stale async completions with a generation token or supported cancellation; release late results that no longer have an owner. A manager's progress percentage is not necessarily download-byte percentage.

Budget decoded GPU texture memory as well as transfer bytes. Consider resizing, mesh simplification, Meshopt/Draco, and KTX2/Basis individually; compare decode time and visual quality before accepting a pipeline. Preserve required animation, skinning, morph targets, and metadata.

Cache immutable source assets and clone scene instances appropriately; skinned models need skeleton-aware cloning. Define cache eviction separately from component unmount. For user uploads, limit size/complexity, handle external URI policy and malformed files, and revoke object URLs after their consumers finish.

Verify missing decoder files, failed textures, rapid model switching, nested deployment paths, representative animation clips, and memory after repeated replacement.

## API reference

Consult the [official documentation](https://threejs.org/docs/pages/GLTFLoader.html) for exact signatures and revision-specific behavior. If documentation access is unavailable, inspect installed types/source and state any remaining uncertainty.
