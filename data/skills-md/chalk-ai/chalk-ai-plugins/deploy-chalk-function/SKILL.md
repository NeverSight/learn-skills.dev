---
name: deploy-chalk-function
description: How to deploy a chalk function ("chalkcompute.function"). Useful for deploying a stand-alone python function in Chalk's container infrastructure. Use when someone wants to run a python function remotely on Chalk, deploy a chalkcompute function, or asks about the chalkcompute SDK.
---

# Deploy a Chalk function

Make a python file that uses the `chalkcompute` package (PyPI name is `chalkcompute`, not `chalk-sandbox-sdk`). Use a `uv` shebang. Pin Python to `<3.14` because a transitive Rust dep (`chalk-remote-call-python`) builds against PyO3 which currently maxes out at 3.13.

```py
#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.12,<3.14"
# dependencies = ["chalkcompute"]
# ///

import chalkcompute


@chalkcompute.function()
def some_function(arg_1: str) -> str:
    return f"hi {arg_1}"


if __name__ == "__main__":
    print(some_function("world"))
```

Notes:

- `@chalkcompute.function` must be **called** — `@chalkcompute.function()` (keyword-only args). Bare `@chalkcompute.function` raises `TypeError: function() takes 0 positional arguments but 1 was given`.
- The decorator deploys the function at import time (builds image, uploads, registers).
- Calling the decorated function (`some_function("world")`) invokes it remotely and returns the result.

## Required env vars

The SDK reads creds from env, **not** from `chalk` CLI config. The env var is `CHALK_ENVIRONMENT_ID`, not `CHALK_ENVIRONMENT`.

```
CHALK_API_SERVER
CHALK_CLIENT_ID
CHALK_CLIENT_SECRET
CHALK_ENVIRONMENT_ID
```

You can read these out of `chalk config` output for the current project. Example invocation:

```
CHALK_API_SERVER=... CHALK_CLIENT_ID=... CHALK_CLIENT_SECRET=... CHALK_ENVIRONMENT_ID=... ./your_script.py
```

Without `CHALK_ENVIRONMENT_ID` you'll get a `permission_denied` error from `CustomImageService.GetOrBuildCustomImage` even though `CHALK_CLIENT_ID`/`CHALK_CLIENT_SECRET` are valid.

## Local SDK source

If `chalkcompute` isn't on the configured index (e.g. the script can't resolve `chalkcompute` from PyPI), point uv at a local checkout of `chalk-sandbox-sdk`:

```
# [tool.uv.sources]
# chalkcompute = { path = "/path/to/chalk-sandbox-sdk" }
```
