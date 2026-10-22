---
name: phpcheck-url
description: Check the advertised PHP version from a URL or hostname.
---

From this skill's directory, run:

```sh
node scripts/phpcheck.js "https://example.com" --json
```

Use HTTPS for a bare hostname. The checker reads `Server` and `X-Powered-By`
headers. If the version is hidden, report unknown.

Compare the reported version with current PHP security guidance. Headers
can be changed and vendor backports may fix an older version, so a server-side
version and package check is stronger evidence. Do not run exploit probes.

Exit codes 1 and 3 mean vulnerable and unknown, not execution failures.
