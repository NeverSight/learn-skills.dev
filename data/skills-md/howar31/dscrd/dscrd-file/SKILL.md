---
name: dscrd-file
description: "Download message attachments"
metadata:
  version: 0.2.0
  openclaw:
    category: "productivity"
    requires:
      bins:
        - dscrd
    cliHelp: "dscrd file --help"
---

# dscrd file

Download message attachments

> **PREREQUISITE:** Read `../dscrd-shared/SKILL.md` for auth, global flags, security rules, and exit codes. If missing, run `dscrd generate-skills`.

| Command | Description |
|---------|-------------|
| `dscrd file download` | Download an attachment from the Discord CDN |

## dscrd file download

Download an attachment from the Discord CDN

```bash
dscrd file download <attachment-url> [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--out` | — | — | output path (default: attachment file name) |


