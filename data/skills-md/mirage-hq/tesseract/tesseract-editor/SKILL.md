---
name: tesseract-editor
description: Build or modify a custom browser editor for Tesseract .tsrct files. Use for editor controls, previews, and saving projects; use the motion or video skill for direct project authoring.
---

# Build a Tesseract editor

The browser engine opens, previews, edits, and saves `.tsrct` projects locally. A static HTML application is sufficient; no backend or native CLI is required. The browser runtime does not export video.

The [browser API reference](references/browser-api.md) covers initialization, actions, playback, and saving. Examples: [general layer controls](examples/timeline-editor/README.md) and [controls for a bundled project](examples/bouncing-ball/README.md).

## Runtime and serving

`references/cli-version.txt`, when present, pins the browser runtime release too. The [installation reference](references/installation.md) identifies the release repository. The browser assets are `tesseract-<VERSION>-web.zip` and its `.sha256`; verify the checksum before use. The archive contains `runtime/`, used beside `index.html` in the examples. Its generated JavaScript, types, and WASM must come from the same release. No npm installation is needed. `version()` returns the runtime release.

The editor needs HTTP serving and browser GPU/media support. Its HTML depends on the runtime files; attachment viewers may not execute WASM. CLI or skill updates do not require upgrading an existing editor’s runtime.

## Editing and saving

`actionSchema()` describes supported engine actions. UI controls, playback scheduling, and selection gestures belong to the application. Await rendering so frames do not overlap; edit groups combine continuous changes into one history entry.

`TesseractEngine.create(file)` accepts a File or Blob. `toBlob()` packages the current document with its original assets; it does not write to disk. Overwriting the source file can invalidate asset reads; the API reference describes reopening the saved Blob. Page refresh discards unsaved edits.
