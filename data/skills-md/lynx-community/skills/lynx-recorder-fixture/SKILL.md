---
name: lynx-recorder-fixture
description: Inspect, decode, edit, and re-encode existing Lynx Recorder / TestBench fixtures. Use to analyze recordings, change mock responses, Action List, Callback, or Config, and troubleshoot replay inputs. Use lynx-recorder to create a new recording.
---

# Lynx Recorder / TestBench Fixture Editing

Recorder output and TestBench fixtures are Lynx engine recording and replay files. They store host-to-engine operations, JS-to-native calls and callback results, and environment settings such as screen dimensions and JSB configuration. Editing a fixture changes the inputs the engine receives during replay.

## Inspect and edit

The tool requires Python 3 and uses only the standard library. `decode`, `summary`, and `roundtrip` accept a local file or HTTP(S) URL; `encode` accepts a local decoded JSON file.

```bash
SKILL_DIR="<directory containing this SKILL.md>"
SOURCE="./recording.json"

# Start with a summary to identify the sections to inspect.
python3 "$SKILL_DIR/scripts/fixture_tool.py" summary "$SOURCE"

# Decode when you need to inspect or edit the contents.
python3 "$SKILL_DIR/scripts/fixture_tool.py" decode "$SOURCE" -o decoded.json

# After editing decoded.json as requested, write a new encoded file.
python3 "$SKILL_DIR/scripts/fixture_tool.py" encode decoded.json -o edited.fixture
```

For analysis requests, report your findings. After editing, report the generated file's absolute path and summarize the changes. `roundtrip SOURCE --workdir DIR` reads and decodes the fixture into `decoded.json` in an existing directory; it does not automatically edit, re-encode, or upload it.

A recorder file's `.json` extension does not imply plain JSON: the usual format is `base64(zlib(JSON))`. Validate by decoding, not by checking a prefix. If the file is already readable JSON, inspect or edit it directly, then use `encode` to produce the replay file. See [file format](references/format-and-encoding.md) for encoding details.

## Choose what to edit

| Section | Container | Purpose | Reference |
|---|---|---|---|
| `Action List` | array | Initialization, template loading, taps, custom events, and data updates | [Action list](references/action-list.md) |
| `Invoked Method Data` | array | Native methods called by JS and their arguments | [Calls and callbacks](references/invoked-methods-callbacks.md) |
| `Callback` | object | Mock response data | [Calls and callbacks](references/invoked-methods-callbacks.md) |
| `Config` | object | Screen dimensions and JSB settings | [File format](references/format-and-encoding.md) |
| `Component List` | array | Registered native components | [File format](references/format-and-encoding.md) |
| `SharedData` / `Scripts` / `Debug Info` | object/array | Shared data, scripts, and debugging information | [Calls and callbacks](references/invoked-methods-callbacks.md) |

Read the reference relevant to the requested change. See [synthetic fixture snippets](examples/fixture-snippets.md) for structural examples; module names, API names, and response schemas depend on the host app.

### Change a mock response

Find the target call in `Invoked Method Data` by `Module Name`, `Method Name`, and `Params.args`. Read its `Params.callback`, then edit the corresponding `Callback[id].Params.returnValue`.

For example, if the target call has callback ID `"31"` and its response contains `data.list` and `data.hasMore`:

```python
import json
from pathlib import Path

path = Path('decoded.json')
fx = json.loads(path.read_text(encoding='utf-8'))
response = fx['Callback']['31']['Params']['returnValue']
response['data']['list'] = []
response['data']['hasMore'] = False
path.write_text(json.dumps(fx, ensure_ascii=False, indent=2), encoding='utf-8')
```

Preserve the response's field names, types, and callback associations. Synchronous return values belong to the call entry's own `Params.returnValue`, separate from asynchronous `Callback` results.

### Other edits and constraints

- **Screen dimensions**: Edit `Config.screenWidth/screenHeight`. When changing the overall device model, check whether `updateViewPort.ratio` and the screen fields in `setGlobalProps` also need adjustment.
- **Interaction sequence**: Edit `Action List`, preserving `RecordMillisecond` order and the ordering of calls and callbacks.
- **Global properties**: Edit `Params.global_props` in `setGlobalProps`.
- **Template contents**: The `source` in `loadTemplate` / `LoadComponentWithCallback` is a compiled template encoded as base64; normally preserve it. The `templateData` wrapper varies by action; see the [action list](references/action-list.md).
- **Nested encoding**: Values in `Scripts` and `content` in `Debug Info` require another base64/zlib decoding step.

## Optional replay validation

When the user requests rendering validation, serve the encoded file at a device-accessible HTTP(S) URL to a Lynx Explorer build that supports TestBench replay. Use `agent-lynx open` to open `sslocal://arkview?url=<URL-encoded fixture URL>`. Uploading to a particular storage service is not a prerequisite for editing a file.

The CLI is normally on `PATH`. If it is not installed, use the public package:

```bash
npx --yes agent-lynx <command> [options]
```

See [replay validation](references/replay.md) for connection, URL encoding, replay, and troubleshooting steps.
