---
name: media-images-and-files
description: Shows, picks and stores images - expo-image, picker, camera, a media store. Use when adding photos, avatars, attachments, uploads or save-to-Photos, or images flicker. Not for icons (icons-app-icon-and-splash).
---

# Media: images and files

Every content image is an expo-image view with a box, a cache policy for its kind of source, a recycling
key in recycled lists and a name (or a decorative mark); photos are picked or captured only from a
press, through ports, the camera only after the permission gate; every picked file is downscaled and
re-encoded once, copied into the app's media folder under a new name and its temporaries discarded;
records hold that name (a MediaRef), never a file URI; files are never overwritten, swept when orphaned,
and leave the device only through ports. A zero-dependency checker proves it on iOS and Android code alike.

## Rules that must hold

1. **Every content image renders with expo-image inside a box.** A `style` with width and height (or
   one plus `aspectRatio`, or flex in a sized parent); `contentFit`, never React Native's `resizeMode`,
   `defaultSource` or `fadeDuration`. Why: without a box the view is 0 x 0 or jumps when the image
   loads, and the compatibility props are deprecated. (`image-size`, `image-legacy-prop`)
2. **Every expo-image `<Image>` is named or marked decorative.** `accessible` with
   `accessibilityLabel={t(...)}` for content, `accessible={false}` for decoration. Why: expo-image is not
   an accessibility element by default, so VoiceOver and TalkBack skip a photo silently. (`image-a11y`)
3. **An image in a recycled list cell has a `recyclingKey`** (the row id). Why: FlashList reuses the
   cell and its image view shows the previous row's photo until the new one loads. (`list-recycling-key`)
4. **The cache policy matches the source.** Stored files `cachePolicy="memory"` (they are on disk
   already); public remote images the default disk cache; private images memory-only or caches cleared
   on sign-out. Why: a disk cache duplicates stored files and keeps private photos after sign-out.
5. **Pick and capture only from a press, through `MediaPickerPort`: images only, no base64, no EXIF.**
   Why: a picker opened from an effect surprises the person and reopens after a cancel; base64 puts
   megabytes on the JS heap; EXIF carries the GPS position. (`picker-on-press`, `picker-options`)
6. **The camera opens only after the permission gate; only `src/services/permissions/` asks.** The
   library picker needs no permission on iOS 14+ and Android; the picker adapter reads the camera
   state through the gate's access (injected), never through its own permission functions. Why: iOS
   rejects `launchCameraAsync` without the grant and Android shows the system dialog with no
   explanation; one gate handles denied, rationale and blocked on both. (`permission-outside-gate`)
7. **The app config declares only the capture and library permissions the code uses.**
   `cameraPermission: false` when nothing opens a camera, `microphonePermission: false` when nothing
   records; these block the permission for the whole app, so never while expo-camera or expo-audio
   needs it. A save-only app keeps `READ_MEDIA_IMAGES`/`VIDEO` out. Why: the defaults add
   `RECORD_AUDIO`, and Play restricts broad photo reads (its Photo and Video Permissions policy).
   (`unused-permission`)
8. **Every picked or captured image is downscaled and re-encoded once (2048 px long edge, JPEG 0.8),
   one at a time, before it is stored; image bytes never live in JS.** Why: a 12 MP photo decodes to
   49 MB; the re-encode drops EXIF and turns HEIC into JPEG; base64 data URIs cost memory twice and
   defeat every cache. (`data-uri`)
9. **Kept media lives in the media store (`Paths.document/media/`), never in the cache, and records
   hold a MediaRef (a plain file name), never a URI.** Resolve with `uriOf(ref)` at render time. Why:
   the system purges the cache, and the absolute path of the app's folders changes after an update or a
   restore, so a stored `file://` URI breaks. (`media-in-cache`, `stored-uri`)
10. **A changed image is a new file under a new name; nothing is overwritten.** Write the partial file,
    rename it into place, save the record, then remove the old file. Why: image caches are keyed by URI
    and keep showing old pixels, and a crash mid-write corrupts the only copy. (`overwrite-in-place`)
11. **Every stored file has one owner record, and an orphan sweep runs after startup and after a
    restore.** Save the record first, then delete the file; the sweep keeps every file this process
    imported and every file the restore's safety copy references (`protectedRefs`), and removes stale
    partial copies. Why: crashes and abandoned imports leave files no record references, and nothing
    else removes them; the undo of a restore needs its photos.
    (`sweep-wired`)
12. **Only current SDK 57 APIs.** expo-file-system's `File`/`Directory`/`Paths` and expo-media-library's
    object API; never their legacy main-entry functions or `/legacy` entries. Why: in SDK 57 the old
    functions compile (declared `@deprecated`) and throw at runtime; `documentDirectory` and
    `cacheDirectory` are no longer exported (a tsc error, or `undefined` in untyped code). (`legacy-api`)
13. **Images leave the device only through ports, from a press**: the share sheet (data-export-and-
    restore's `ShareSheetPort`), `PhotoSaverPort`, and `FileTransferPort` for uploads and downloads,
    with URLs from `src/api` and headers from the session. Why: one adapter per SDK, the app's network
    policy keeps its single entry per transport, and only re-encoded, metadata-free files leave.
    (`transfer-outside-port`)

## Workflow

1. Read [references/displaying-images.md](references/displaying-images.md) for any image on screen, and
   [references/picking-and-capturing.md](references/picking-and-capturing.md) plus
   [references/files-and-storage.md](references/files-and-storage.md) when the person adds photos.
2. Prerequisites: the Result module (error-handling-typed-results) and the composition root
   (architecture-and-boundaries). Install:
   `npx expo install expo-image-picker expo-image-manipulator expo-file-system expo-device expo-crypto`
   (SDK 57: `~57.0.20`, `~57.0.20`, `~57.0.7`, `~57.0.2`, `~57.0.3`; `expo-image ~57.0.5` ships with the template, expo-file-system often arrives
   with persistence-and-migrations; verified 2026-10-14; re-verify with `npx expo install --check`).
3. Stop and ask the developer to classify the new SDKs (an architecture decision): merge
   `examples/contracts/architecture.json` into `contracts/architecture.json` and add the packages to
   `VENDOR_SDK_PATHS` in `eslint.config.mjs` in one commit with a Gate-Change trailer.
4. Copy the templates: `templates/src/core/media/`, `templates/src/services/{media-picker,media-store,image-resizer}/`,
   `templates/src/data/media/`, `templates/src/ui/media/` (list `StoredImage` in the component catalogue,
   ui-component-library). Copy the resizer adapter from
   `examples/src/services/image-resizer/` once expo-image-manipulator is installed.
5. Set the picker plugin options in `app.config.ts` (picking-and-capturing.md, section 8): purpose texts
   from the catalogs (i18n-strings-and-catalogs), `false` for every permission no code uses (they block
   it for the whole app: check expo-camera and expo-audio first).
6. Compose once: the three adapters in `createDeviceServices` (fakes in `createTestServices`), the picker
   with `isCameraAllowed: async () => isPermissionAllowed(await permissions.access.camera.permission())`
   and `isCameraPresent: () => Platform.OS !== 'ios' || Device.isDevice` (expo-device; opening the camera
   on the iOS simulator crashes, picking-and-capturing.md section 5), and `createMediaImporter({ picker, resizer, store, nextMediaId })`; features read `useServices()`.
   In the startup work after the data layer opened (app-startup-and-bootstrap), `await
   importer.importPendingPick()` first, then `sweepMedia(...)` with the safety copy's refs as
   `protectedRefs` (files-and-storage.md section 9); sweep again after a restore. `nextMediaId` is
   `() => randomUUID().toLowerCase()` from expo-crypto (Hermes has no global `crypto.randomUUID`).
7. Store MediaRefs: a `*_ref TEXT` column through a migration (persistence-and-migrations) or a
   `MediaRef` field in a store; a repository method lists every ref for the sweep.
8. Build the feature from `examples/src/features/tasks/` (model hook, jobs, photo strip): "Take photo"
   calls permissions-and-system-prompts' `usePermissionGate` `requestAccess` and the capture runs from
   its `onAllowed`, the screen renders the gate's sheet; one message per failure kind, the busy state
   blocking a second press, a failed record save removing the new files, remove = save then delete.
9. Sharing, Photos, uploads: [references/sharing-and-transfer.md](references/sharing-and-transfer.md)
   and `examples/src/services/{photo-saver,file-transfer}/`; tell networking-and-server-state and
   privacy-and-store-declarations about a new transport or data type before it ships.
10. Run the tests ([references/testing-and-checker.md](references/testing-and-checker.md)):
    `npx jest src/core/media src/services/media-picker src/services/media-store src/services/image-resizer src/data/media src/ui/media --ci`
    and `npm run typecheck`.
11. After an adapter change, run the media drill on a named iOS simulator and Android emulator
    (testing-and-checker.md, section 3), or say in the report that it is owed.
12. Run `node ${CLAUDE_SKILL_DIR}/scripts/check-media.mjs .`; fix every `FAIL` line and rerun until it
    prints `RESULT: PASS`.

## Definition of done

- [ ] Every expo-image `<Image>` has a box, `contentFit` (no legacy props), a name or
      `accessible={false}`, a cache policy fit for its source, and a `recyclingKey` in recycled cells.
- [ ] Picks and captures run from presses through `MediaPickerPort`; images only, no base64, no EXIF;
      the camera behind the permission gate; no plugin declares an unused capture or library permission.
- [ ] Every picked image goes through the importer: downscaled to 2048 px, JPEG, one at a time, stored
      under a new MediaRef in `Paths.document/media/`, temporaries discarded, all or nothing per batch.
- [ ] Records and stores hold MediaRefs, resolved with `uriOf` at render; nothing overwrites a stored
      file; deletes save the record first; the sweep runs after startup and after a restore and keeps
      the safety copy's refs (`protectedRefs`).
- [ ] No legacy expo-file-system or expo-media-library API; uploads and downloads only in the
      file-transfer adapter; sharing through `ShareSheetPort`.
- [ ] The tests of workflow step 10 pass; after an adapter change the drill passed on iOS and Android,
      or the report says it is owed.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-media.mjs .` prints `RESULT: PASS`. Expected only before the
      app config exists: `SKIP app.config.ts [unused-permission] not yet created
      (app-variants-and-environment creates it)`. An app without media code prints `NOT APPLICABLE: no
      source file under src/ imports expo-image, expo-image-picker, expo-camera, expo-image-manipulator,
      expo-media-library, expo-file-system, and there is no src/services/media-store/`.

## Anti-patterns

- **Saving `asset.uri` from the picker in a record.** It is a cache file the system purges, at an
  absolute path that changes; import it and store the MediaRef.
- **`base64: true` "to upload it easily", or a `data:image` URI.** Megabytes on the JS heap, decoded
  twice, no cache; upload the stored file with `FileTransferPort`.
- **Opening the picker in `useEffect` when a screen mounts.** It reopens after a cancel and on every
  focus; open it from the press.
- **Calling `requestCameraPermissionsAsync` in a screen.** No explanation, no blocked state; the gate.
- **`cameraPermission: false` on the picker in an app with an expo-camera scanner.** The option strips
  `CAMERA` from the merged manifest for every package; the scanner can never be granted.
- **`granularPermissions` left at the default in a save-only app.** It declares `READ_MEDIA_IMAGES` and
  `READ_MEDIA_VIDEO`, which Play reviews under its Photo and Video Permissions policy.
- **Overwriting `photo.jpg` after a crop.** Every view keeps the old image; a new ref per change.
- **Deleting the file, then saving the record.** A crash leaves a record pointing at nothing; record
  first, the sweep removes leftovers.
- **Shipping full-size camera photos.** 5 to 10 MB per file, 49 MB per decode, Android's 25 MB backup
  quota gone after a few photos; downscale once on import.
- **Sharing the picked original.** It carries the GPS position; share the stored, re-encoded file.
- **`allowDownscaling={false}` or `contentFit="none"` in a list.** Full-size decodes per cell.
- **`saveToLibraryAsync` or `readAsStringAsync` from the main entries.** They throw in SDK 57; use the
  object APIs.
- **A second expo-sharing adapter.** Reuse data-export-and-restore's `ShareSheetPort`.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/displaying-images.md](references/displaying-images.md) | expo-image API, sizing, cache policies, recycling, memory arithmetic, names, remote images, placeholders, platform differences, pitfalls | Workflow step 1, any image on screen |
| [references/picking-and-capturing.md](references/picking-and-capturing.md) | Picker and camera API, permissions per platform (read in the native sources), the gate, Android's lost activity, returned files, app config, expo-camera | Workflow steps 1-3, 5, 8 |
| [references/files-and-storage.md](references/files-and-storage.md) | The folders, MediaRef, the import, no overwrite, owners and the sweep, disk space and backups, the SDK 57 file-system API and its throwing legacy names, backups and media | Workflow steps 1, 6-7 |
| [references/sharing-and-transfer.md](references/sharing-and-transfer.md) | Share sheet, saving to Photos (expo-media-library 57), the file-transfer port, privacy, receiving images | Workflow step 9 |
| [references/testing-and-checker.md](references/testing-and-checker.md) | The shipped tests, testing with fakes, the media drill on named devices, every check-media rule with its fix, configuration | Workflow steps 10-12 |
| `templates/src/core/media/` | `media-ref.ts` (MediaRef, extensions), `image-fit.ts` (fit, decoded bytes, `MEDIA_LIMITS`), `media-sweep.ts` (the sweep plan), each with its test | Workflow step 4 |
| `templates/src/services/` | `media-picker/`, `media-store/`, `image-resizer/`: ports, the picker and file-system adapters, fakes with tests | Workflow steps 4, 6 |
| `templates/src/data/media/` | `media-importer.ts` (pick, downscale, store, discard; all or nothing; protected from the sweep from the moment each file is stored until the process ends) and `media-sweeper.ts` (stale partials, orphans), with tests | Workflow steps 4, 6 |
| `templates/src/ui/media/` | `stored-image.tsx` (sized, memory-cached, recycled, named) and its test | Workflow step 4 |
| `examples/src/services/` | `image-resizer/` (expo-image-manipulator adapter), `photo-saver/` (expo-media-library port and adapter), `file-transfer/` (upload and download port and adapter), type-checked against their SDK 57 packages | Workflow steps 4, 9 |
| `examples/src/features/tasks/` | A task's photos: model hook (the camera through `usePermissionGate`) and its test (allowed, refused, rationale, blocked, failed save), press jobs (import, save, remove, share), the photo strip (a FlatList: the list is bounded) | Workflow step 8 |
| `examples/contracts/architecture.json` | The vendor SDK entries to merge | Workflow step 3 |
| `examples/task-photos-messages.en.json` | The example's catalog keys | Workflow step 8 |
| `scripts/check-media.mjs` | The checker (15 rules; `--json`) | Workflow step 12, and at the end |
| `scripts/lib/media-rules.mjs` | The checker's rules | Never by hand |
| `scripts/lib/source-scan.mjs` | Shared source scanner, synced from the library (do not edit here) | Never by hand |
| `scripts/check-lib.mjs` | Shared script helper, synced from the library (do not edit here) | Never by hand |
| `scripts/selftest.mjs` | Proves the checker passes the templates and examples and catches every planted bug | After changing a script, a template or an example |
| `assets/shared.json` | The shared files this skill copies in | When adding a shared file |
| `assets/template-placeholders.json` | Template placeholder values (none) | When adding a placeholder |
| `tests/` | The fixture app (`bases/app`) and the overlay cases of check-media (one planted bug per rule) | When adding a rule |

## Related skills

- `icons-app-icon-and-splash` - icons, the logo and illustrations drawn in code; bundled art.
- `permissions-and-system-prompts` - the camera and photo-library permission gate.
- `data-export-and-restore` - `ShareSheetPort`, backups (media refs vs files).
- `architecture-and-boundaries` - ports, adapters, SDK classification, the composition root.
- `persistence-and-migrations` - the MediaRef columns and their migrations.
- `networking-and-server-state` - the ApiClient beside the file-transfer transport.
- `privacy-and-store-declarations` - Photos or Videos in the store answers, the network audit.
- `performance-budgets` - the memory budget and how to measure it on devices.
- `accessibility-as-code` - image names, Reduce Motion for transitions.
- `react-components-and-hooks` - lists, effects, `useIsAppActive` for a camera view.
- `expo-prebuild-and-config-plugins`, `i18n-strings-and-catalogs` - plugin listing and purpose texts.
- `auth-and-secure-storage` - headers for private images, clearing caches on sign-out.
- `unit-and-component-tests`, `e2e-maestro` - test conventions and device flows.
- `ios-simulator-build`, `android-emulator-build` - the builds the drill installs.
