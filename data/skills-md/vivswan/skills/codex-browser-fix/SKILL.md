---
name: codex-browser-fix
description: Use when Codex on macOS must drive the user's Chromium browser (Brave, Vivaldi, Opera, Edge, Chrome) through the bundled Chrome plugin, or that plugin fails with "Codex auth token is unavailable", a missing extension connection, or a stale plugin cache after a desktop app update. Codex only.
license: SEE LICENSE IN LICENSE.md
metadata:
  author: Vivswan
---

# Codex Browser Fix

Codex only. The desktop app bundles a Chrome plugin that drives any Chromium browser through the ChatGPT extension. Two things break it, and the vendor skill covers neither:

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Codex auth token is unavailable` after the extension was discovered | `config.toml` sets a custom `model_provider`; the browser helper launches `codex app-server` and inherits it, so the ChatGPT sign-in is invisible | Preflight installs a launcher that overrides the provider for that one subprocess |
| Extension found yesterday, missing or erroring today | The desktop app updated; `~/.codex/plugins/cache/openai-bundled/chrome` still points at the old bundle | Preflight re-syncs the cache and the trust hashes to the installed app |
| User asked for Brave (or Vivaldi, Opera) and the agent picked Chrome | The vendor skill only names `chrome` and `edge`; other families need a `list()` match | Select by `family` (below) |

The installed Chrome plugin's own skill (`skills/control-chrome/SKILL.md` inside the app bundle) stays the authority for browser APIs. This skill owns local setup, recovery, and browser-family selection.

## When to Apply

- The user names Brave, Vivaldi, Opera, Edge, Chrome, or "my browser" for a task that needs their tabs or sign-in
- The Chrome plugin errors with `Codex auth token is unavailable`
- Browser discovery finds no extension connection, or fails right after a ChatGPT or Codex desktop update
- "check the browser setup" / "fix the browser connection"

## Workflow

### 1. Preflight the plugin

Run before importing `browser-client.mjs` or selecting a browser. Requires Bun and the ChatGPT or Codex desktop app. `<skill-dir>` is the installed skill folder (Codex default: `~/.codex/skills/codex-browser-fix`).

```bash
bun "<skill-dir>/scripts/browser-plugin-preflight.mts"          # sync + verify
bun "<skill-dir>/scripts/browser-plugin-preflight.mts" --check  # read-only verify, exit 1 on drift
```

It prints the app bundle version, the plugin path to import `browser-client.mjs` from, and which caches were synchronized. Re-run it after every desktop app update or restart. A failure names the missing file or stale setting and exits 1; a missing `config.toml`, bundle, or executable is an error, never a pass.

The codex home is `$CODEX_HOME` or `~/.codex`. A non-standard install passes `--plugin-dir <dir>` with the bundled Chrome plugin directory. `--check` on a missing `config.toml` exits 1; a missing `--plugin-dir` value exits 2.

What it changes, and nothing else (`<home>` is the codex home):

- `<home>/plugins/cache/openai-bundled/chrome`: every existing pinned version entry, the current version's entry, and the `latest` link follow the installed app bundle. `<home>/plugins/cache/openai-bundled/browser`: the current version's companion copy and its `latest` link only. Replaced stale copies move to `<home>/plugin-rollbacks/`.
- `<home>/config.toml`, under `[mcp_servers.node_repl.env]`: `CODEX_CLI_PATH`, the app version, and the trusted code paths. Under `[shell_environment_policy.set]`: the `browser-client.mjs` hash. Each value must already be assigned there; the edit is parse-verified to change nothing else.
- `<home>/scripts/browser-codex`: a generated launcher. Only its `app-server` subcommand gets `-c 'model_provider="openai"'`; every other subcommand passes through unchanged. The main provider, `CODEX_HOME`, and credentials are untouched.
- Each `<home>/hosts/<host>/`: its own `plugins/cache/openai-bundled/browser` companion cache, and, where it has a `config.toml`, the same config edits plus its own `scripts/browser-codex`. The Chrome cache is global only.

### 2. Bootstrap the vendor way

Follow the installed `control-chrome` skill through its `node_repl` JavaScript tool: import `browser-client.mjs` from the path the preflight printed, call `setupBrowserRuntime()` once, and reuse the `agent` and browser bindings across turns. Never reset a working session to repeat setup.

### 3. Select the browser family

Chrome and Edge have vendor selectors: `agent.browsers.get("chrome")` and `agent.browsers.get("edge")`. Every other Chromium family is matched from the list:

```js
// Declared once per session; call it again with a profile name after asking.
async function selectExtension(family, profileName) {
  const label = (c) => c.profileName ?? c.name; // the name shown when asking
  const candidates = (await agent.browsers.list()).filter(
    (c) =>
      c.type === "extension" &&
      c.family === family &&
      (profileName === undefined || label(c) === profileName),
  );
  if (candidates.length === 0) throw new Error(`No connected ${family} extension`);
  if (candidates.length > 1) {
    const profiles = candidates.map(label).join(", ");
    throw new Error(`Several ${family} profiles connected (${profiles}); ask which one`);
  }
  return agent.browsers.get(candidates[0].id);
}
let browser = await selectExtension("brave", undefined); // or ("brave", "Work") once known
nodeRepl.write(await browser.documentation());
```

- No candidate: report the browser as unavailable in the user's words (the extension is missing or disconnected). Several: ask which profile, then call `selectExtension` again with that name and reassign `browser`. Never guess.
- Family names follow the plugin's `scripts/extension-ids.json`: `brave`, `chrome`, `edge`, `opera`, `vivaldi`.
- An explicit browser request is a hard constraint. Never substitute Google Chrome because the plugin is named Chrome, and never fall back to Computer Use or a fresh browser.
- After selection, read the complete `documentation()` output as the vendor skill requires, name the session, then claim the exact tab object from `browser.user.openTabs()` that matches the task.
- A stale or closed tab gets a fresh tab from the existing browser binding. Re-select a browser only after an explicit disconnection or a user-requested switch.

### 4. Work and hand off

- Inspect the page before acting; re-check state after each meaningful action. A completed click or upload is not a saved result: verify the fields, media, and saved state on the page before reporting success.
- Read the vendor upload instructions before photo or document uploads.
- Preserve tabs per the vendor's handoff rules. Never clear browser storage; it holds local drafts and signed-in state.
- Connection setup authorizes nothing else. Applications, messages, purchases, and publications still follow the current request and project approval rules.

## Recovery

- `Codex auth token is unavailable`, empty discovery, cache or trust failures: run the preflight, then read [recovery](references/recovery.md).
- Discovery or selection fails after a good bootstrap: `await agent.documentation.get("bootstrap-troubleshooting")`.
- Extension install or communication fails: `await agent.documentation.get("chrome-troubleshooting")`.
- A running browser helper keeps the environment it started with. A new launcher setting takes effect when that helper next starts; do not kill a working connection to apply it.

Never: switch the main `model_provider` off and back on, copy tokens, patch app binaries, or reinstall components speculatively. Report a real sign-in requirement as the user's action.

## Fallback Without the Desktop Plugin

The preflight `--check` runs from any terminal with Bun, independent of an MCP host, and reports which bundle, cache, or setting is missing. Prepare task material locally where useful. Live browser work resumes only in a desktop Codex session with the Chrome plugin and the requested browser connection; never substitute another browser or automation transport.

## References

- `references/recovery.md`: the auth incident specimen, what the preflight synchronizes, and the extension-versus-tab failure split
- `scripts/browser-plugin-preflight.mts`: the sole setup implementation (sync and `--check`)
- `scripts/browser-auth-launcher.mts`: the launcher generator and the `config.toml` edit, unit-tested in the authoring repository
