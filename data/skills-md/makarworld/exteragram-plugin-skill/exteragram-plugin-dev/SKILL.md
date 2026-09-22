---
name: exteragram-plugin-dev
description: >-
  Build exteraGram plugins (Python on BasePlugin SDK 1.4.4.3, exteraGram 12.5.1+,
  Python 3.11 via Chaquopy v16). Use when writing or editing .plugin files,
  implementing hooks (on_send_message_hook, pre_request_hook, post_request_hook,
  on_update_hook), creating plugin settings (ui.settings: Header/Switch/Selector/
  Input/Text/Custom), sending messages (send_text/send_photo/send_document/
  edit_message), Xposed method hooking (MethodHook/HookFilter), Java class proxy
  (java_subclass/joverride/jmethod), file handlers (FilesController), bulletins
  (BulletinHelper), dialogs (AlertDialogBuilder), intents (IntentsManager), Elyx
  structured plugins (refmap/metainfo/assets/strings), reflection (hook_utils
  find_class/get_private_field), or debugging the dev server (127.0.0.1:42690).
  Covers multi-account scoping, text formatting, PIP dependencies, and the
  awesome-plugins repo conventions (.plugin is source, docs.md, releases/, Ruff).
---

# exteraGram Plugin Development

## Baseline

- SDK version: `1.4.4.3` (multi-account helpers need `>=1.4.5.0`, Elyx needs `>=1.4.5.3`)
- Python runtime: **3.11** (bytecode builds MUST use 3.11)
- Minimum app: **exteraGram 12.5.1+** (older builds enter safe mode and refuse plugin init)
- Engine: Chaquopy v16 + Xposed-style method hooking
- SDK modules are stub imports on desktop — IDE flags them as missing; add `# pyright: ignore[reportMissingImports]` or `# noqa`

## Quickstart — Minimal Plugin

A plugin is one Python file (extension `.plugin` in the awesome-plugins repo, `.py` on device). The file must contain:

1. **Metadata as plain top-level constants** (loader parses them via AST — never build dynamically)
2. **One class inheriting from `BasePlugin`**

```python
from base_plugin import BasePlugin

__id__ = "hello_world"              # 2-32 chars, latin/digits/_/-, start with letter
__name__ = "Hello World"            # required
__description__ = "My first plugin" # markdown supported in UI
__author__ = "@yourUsername"
__version__ = "1.0.0"               # default "1.0" if omitted
__icon__ = "exteraPlugins/1"        # StickerPackShortName/index
__app_version__ = ">=12.5.1"        # supports >=, <=, ==, >, <
__sdk_version__ = ">=1.4.4.3"
__requirements__ = ["mpmath"]       # PEP 508, pure-Python wheels only


class HelloWorldPlugin(BasePlugin):
    pass
```

For a fuller first plugin (`.hello` command + settings + outgoing-message hook), see [examples/hello_command.py](examples/hello_command.py).

## API Map by Module

| Module | Key capabilities | Reference |
|--------|------------------|-----------|
| `base_plugin` | `BasePlugin`, metadata, lifecycle, hooks, menu items, `MethodHook`/`MethodReplacement`/`HookFilter`/`MenuItemData`/`AppEvent` | [plugin-class.md](reference/plugin-class.md) |
| `ui.settings` | `Header`/`Divider`/`Switch`/`Selector`/`Input`/`EditText`/`Text`/`Custom`, `SimpleSettingFactory` | [settings.md](reference/settings.md) |
| `client_utils` | `run_on_queue`, `send_request`, `send_text`/`send_photo`/`send_document`/`send_video`/`send_audio`/`send_message`, `edit_message`, `get_last_fragment`/`get_messages_controller`/..., `NotificationCenterDelegate` | [client-utils.md](reference/client-utils.md) |
| `android_utils` | `run_on_ui_thread`, `R` (Runnable proxy), `OnClickListener`/`OnLongClickListener`, `log`, `copy_to_clipboard` | [android-utils.md](reference/android-utils.md) |
| `hook_utils` | `find_class`, `get_private_field`/`set_private_field`, static variants — reflection | [hook-utils.md](reference/hook-utils.md) |
| `extera_utils.classes` | `@java_subclass`, `@joverride`/`@joverload`/`@jmethod`/`jfield`/`@jconstructor`, MVEL, `JA`/`JGS`/`JIR`/`JS` modifiers | [class-proxy.md](reference/class-proxy.md) |
| `extera_utils.text_formatting` | `parse_text(text, parse_mode="HTML"\|"Markdown")`, `TLEntityType` | [text-formatting.md](reference/text-formatting.md) |
| `file_utils` | `get_plugins_dir`/`get_cache_dir`/..., `read_file`/`write_file`/`read_file_bytes`/`write_file_bytes`, `list_dir`, `FilesController` | [file-utils.md](reference/file-utils.md) |
| `ui.bulletin` | `BulletinHelper.show_info`/`show_error`/`show_success`/`show_with_button`/`show_undo` | [ui-helpers.md](reference/ui-helpers.md) |
| `ui.alert` | `AlertDialogBuilder` — message/loading/spinner dialogs | [ui-helpers.md](reference/ui-helpers.md) |
| `intents` | `IntentsManager.new_global_before_handler`/`new_global_after_handler`, scheme/host/path/action/flags filters | [intents.md](reference/intents.md) |
| multi-account | `account=` on every hook/controller, `self.client(account)` → `AccountClient`, `get_selected_account`, `get_hook_account` | [multi-account.md](reference/multi-account.md) |
| `elyx` | Structured multi-file plugins: `refmap.yml`, `metainfo.yml`, `assets`, `strings`, bundled wheels, `ElyxBuilder` CLI | [elyx.md](reference/elyx.md) |
| dev workflow | Setup, dev server (`127.0.0.1:42690`), PIP deps, pre-installed libs, common Telegram classes | [dev-workflow.md](reference/dev-workflow.md) |
| repo (awesome-plugins) | `.plugin` is source, `docs.md`, `releases/`, `secure.md`, Ruff, Pluggy | [repo-conventions.md](reference/repo-conventions.md) |

## Hooks (most-used API)

Register in `on_plugin_load`:

```python
class MyPlugin(BasePlugin):
    def on_plugin_load(self):
        self.add_hook("TL_messages_setTyping")     # request by name
        self.add_on_send_message_hook()             # outgoing messages
```

Signatures and `HookResult`:

| Hook | Signature | Modify via |
|------|-----------|------------|
| `pre_request_hook` | `(self, request_name, account, request)` | `HookResult.request` |
| `post_request_hook` | `(self, request_name, account, response, error)` | `HookResult.response` |
| `on_update_hook` | `(self, update_name, account, update)` | `HookResult.update` |
| `on_updates_hook` | `(self, container_name, account, updates)` | `HookResult.updates` |
| `on_send_message_hook` | `(self, account, params)` | `HookResult.params` |

```python
from base_plugin import HookResult, HookStrategy

# Strategies:
HookStrategy.DEFAULT       # do nothing
HookStrategy.CANCEL        # stop the operation
HookStrategy.MODIFY        # use the modified object
HookStrategy.MODIFY_FINAL  # modify and stop further plugin processing

def on_send_message_hook(self, account, params) -> HookResult:
    if isinstance(getattr(params, "message", None), str) and params.message.startswith(".hello"):
        params.message = "Hello!"
        return HookResult(strategy=HookStrategy.MODIFY, params=params)
    return HookResult()  # unchanged
```

## Multi-Account Rule (critical)

exteraGram keeps every logged-in account connected. Background accounts still fire hooks. **Every hook callback receives `account`** — use it for anything you do in response:

```python
def on_update_hook(self, update_name, account, update) -> HookResult:
    client = self.client(account)  # AccountClient bound to one account
    client.send_text(update.message.dialog_id, "reply")
    return HookResult()
```

Without `account=`, helpers default to the UI-selected account and the SDK logs a warning once per helper. See [multi-account.md](reference/multi-account.md).

## Pre-Commit Checklist (awesome-plugins repo)

```
[ ] ruff check PluginName/plugin_name.plugin        # only mandatory check
[ ] docs.md updated when hooks/architecture/keys change
[ ] README.md updated when UX or raw download URL changes
[ ] releases/vX.Y.Z/ created ONLY when publishing a release (not during iteration)
[ ] Pluggy (pluggy_analyze.ps1 -> secure_*.md) ONLY on release, not every edit
```

`.plugin` is the **source** — edit it directly. There is no build step. Full conventions: [repo-conventions.md](reference/repo-conventions.md).

## Common Beginner Mistakes

1. **Forgetting `self.add_on_send_message_hook()`** in `on_plugin_load` — implementing the method alone does nothing.
2. **Dynamic metadata** — `__version__ = compute_version()` breaks AST parsing; use plain constants.
3. **`params.message` without `isinstance` check** — some sends are media-only; always validate.
4. **Slow work on the UI thread** — use `run_on_queue(...)` (from `client_utils`) for network/file/long compute.
5. **Wrong account** — see Multi-Account Rule above.
6. **Shadowing SDK/stdlib module names** — never name a local file `json.py`, `ui.py`, `java.py`, `elyx.py`.

## Elyx (Structured Multi-File Plugins)

Use Elyx instead of single-file when you need multiple modules, bundled assets, localization, or bundled wheels. Same `BasePlugin` API; Elyx adds `refmap.yml` + `metainfo.yml` + `assets/` + `strings/`.

```yaml
# refmap.yml
metainfo: metainfo.yml
main: main.py
assets: assets
strings: strings
```

```yaml
# metainfo.yml
id: my_plugin
name: My Plugin
version: "1.0.0"
sdk_version: ">=1.4.5.3"
```

Scaffold: `python -m pip install --upgrade ElyxBuilder && elyb new -g -n "My Plugin" -a author`. Build: `elyb build --ast -v -nf`. Full guide: [elyx.md](reference/elyx.md).

## Examples

- [examples/minimal.py](examples/minimal.py) — bare skeleton (metadata + `BasePlugin`)
- [examples/hello_command.py](examples/hello_command.py) — `.hello` command + settings + `on_send_message_hook`
- [examples/ghost_mode.py](examples/ghost_mode.py) — `pre_request_hook` cancel/modify + settings + menu items
- [examples/custom_setting.py](examples/custom_setting.py) — `SimpleSettingFactory` + custom Java view row

## Source

Distilled from [plugins.exteragram.app/docs](https://plugins.exteragram.app/docs) (32 pages, SDK 1.4.4.3). When the live docs disagree with this skill, the live docs win for SDK behavior; this skill wins for awesome-plugins repo conventions.
