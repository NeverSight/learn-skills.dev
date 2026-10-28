---
name: bitrix-files
description: 'b_file storage via CFile (SaveFile, MakeFileArray, GetFileArray, ResizeImageGet, Delete), upload validation, ui.uploader UploaderController, BFile delivery, File\ContentReplacer. Use when saving, validating, resizing or serving files.'
---

# Bitrix files

Baseline: main 23.0+ · Verified: main 26.800.0, ui 26.687.0

| Task | Read |
| --- | --- |
| Save, read, resize, delete; `b_file` layout; clouds; replace content keeping the ID | `rules/storage.md` |
| Accept uploads in your action: validation, MIME, legacy `main.file.input` | `rules/uploads.md` |
| `ui.uploader` backend: `UploaderController`, commit pending files | `rules/ui-uploader.md` |
| Serve files: `BFile`, private files, viewer | `rules/delivery.md` |

JS widgets (`ui.uploader`, `ui.viewer`): `bitrix-ui`. Uploader settings in `.settings.php`: `bitrix-settings`. File fields: `bitrix-iblocks`, `bitrix-highloadblock`.

## Invariants

- Write `b_file` only through `CFile`. `FileTable` is read-only: `add`/`update`/`delete` throw `NotImplementedException`. Store the file ID, never a path.
- For URLs use `CFile::GetFileArray()['SRC']` or `CFile::GetPath()`; for local bytes use `CFile::MakeFileArray($id)['tmp_name']`. Never glue `/upload/` + `SUBDIR` yourself: clouds, the `upload_dir` option and replacements all break it.
- Client name, MIME and size are untrusted: whitelist extensions, detect MIME from content, and decode images.
- Never pass user input to `CFile::MakeFileArray()`: it reads local paths, b_file IDs and URLs.
- Everything in `/upload/` is reachable by URL. Serve private files through an action that checks rights.
- `CFile::Delete()` removes the physical file and its resize cache. It cannot be undone.
