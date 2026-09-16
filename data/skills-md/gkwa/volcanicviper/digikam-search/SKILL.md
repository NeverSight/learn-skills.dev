---
name: digikam-search
description: "Find digikam notes and digikam setup information. Use when asked to search my digikam, find digikam media, or look up anything about the digikam configuration or database."
---

## Searching digikam

To find notes about the digikam setup — database location, SQLite schema, collection paths, sidecar settings, search queries, or anything else digikam-related — use islandiguana to retrieve all vault notes tagged `digikam`:

```sh
/Users/mtm/go/bin/islandiguana "/Users/mtm/Documents/Obsidian Vault" '.tags[] == "digikam"'
```

Read the returned notes.

They contain the authoritative information on where digikam stores its database, how to query it, where collection roots are defined, and how to search media.
