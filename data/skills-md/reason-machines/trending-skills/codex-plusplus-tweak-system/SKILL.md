---
name: codex-plusplus-tweak-system
description: Expert knowledge for using codex-plusplus to inject tweaks, patch Codex desktop app, and write custom ESM tweak modules with lifecycle APIs.
triggers:
  - install codex plusplus
  - write a tweak for codex
  - patch codex app with tweaks
  - add custom features to codex desktop
  - codex plusplus tweak development
  - how to create a codex tweak
  - codex plusplus install and setup
  - inject custom code into codex app
---

# codex-plusplus Tweak System

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

`codex-plusplus` is a tweak injection system for the [Codex](https://chatgpt.com/codex) desktop app (Electron-based). It patches `app.asar`, injects a loader stub, and runs a hot-reloadable runtime from the user directory. Tweaks are small ESM modules with a manifest and `start/stop` lifecycle — no app rebuild required.

---

## Installation

### Homebrew (macOS, recommended)
```sh
brew install b-nnett/codex-plusplus/codexplusplus
codexplusplus install
```

### Bun (global)
```sh
bun install -g github:b-nnett/codex-plusplus
codexplusplus install
```

### Source bootstrap (macOS / Linux)
```sh
curl -fsSL https://raw.githubusercontent.com/b-nnett/codex-plusplus/main/install.sh | bash
```

### Windows PowerShell
```powershell
irm https://raw.githubusercontent.com/b-nnett/codex-plusplus/main/install.ps1 | iex
```

The installer:
1. Locates `Codex.app` (or Windows equivalent)
2. Backs up the original to `~/.codex-plusplus/backup/`
3. Patches `app.asar` to require the loader
4. Recomputes asar header SHA-256, writes it into `Info.plist`
5. Flips `EnableEmbeddedAsarIntegrityValidation` in the Electron Framework binary
6. Re-signs ad-hoc on macOS (`codesign --force --deep --sign -`)
7. Installs a launch agent / login item for auto-repair on Codex updates
8. Installs default tweaks unless `--no-default-tweaks` is passed

---

## Key CLI Commands

```sh
codexplusplus install              # Patch Codex and install runtime
codexplusplus install --no-default-tweaks  # Skip default tweak set

codexplusplus status               # Show patch status and runtime version
codexplusplus doctor               # Diagnose issues (integrity, signing, etc.)
codexplusplus repair               # Re-apply patch (e.g. after Codex update)
codexplusplus repair --quiet       # Silent repair (used by watcher/launch agent)

codexplusplus update               # Pull latest codex-plusplus source, rebuild, repair
codexplusplus update-codex         # Restore official-signed Codex for Sparkle updater

codexplusplus uninstall            # Revert all patches, restore backup

codexplusplus tweaks list          # List installed tweaks and enabled state
codexplusplus tweaks open          # Open user tweaks directory in Finder/Explorer
```

---

## File Locations

| Artifact | Path |
|---|---|
| Loader stub | `Codex.app/Contents/Resources/app.asar` |
| Runtime | `<user-data-dir>/runtime/` |
| Tweaks | `<user-data-dir>/tweaks/` |
| Config | `<user-data-dir>/config.json` |
| Backup | `<user-data-dir>/backup/` |

**`<user-data-dir>` per OS:**
- macOS: `~/Library/Application Support/codex-plusplus/`
- Linux: `$XDG_DATA_HOME/codex-plusplus/` (default `~/.local/share/codex-plusplus/`)
- Windows: `%APPDATA%/codex-plusplus/`

---

## Writing a Tweak

### Folder Structure
```
<user-data-dir>/tweaks/my-tweak/
├── manifest.json
└── index.ts        # or .js / .mjs
```

### manifest.json
```json
{
  "id": "com.yourname.my-tweak",
  "name": "My Tweak",
  "version": "0.1.0",
  "githubRepo": "yourname/my-tweak",
  "author": "yourname",
  "description": "Short description of what this tweak does.",
  "minRuntime": "0.1.0"
}
```

**Required fields:** `id` (reverse-domain), `name`, `version`, `githubRepo` (for update checks), `author`, `description`, `minRuntime`.

### index.ts — Minimal Tweak
```ts
import type { Tweak } from "@codex-plusplus/sdk";

export default {
  start(api) {
    api.log.info("My tweak started");
  },
  stop() {
    // Cleanup: remove event listeners, DOM nodes, etc.
  },
} satisfies Tweak;
```

### index.ts — Settings Panel
```ts
import type { Tweak } from "@codex-plusplus/sdk";

export default {
  start(api) {
    api.settings.register({
      id: "my-tweak",
      title: "My Tweak",
      render(root) {
        root.innerHTML = `
          <div style="padding: 16px;">
            <h2>My Tweak Settings</h2>
            <label>
              <input type="checkbox" id="my-tweak-toggle" />
              Enable feature
            </label>
          </div>
        `;

        const toggle = root.querySelector<HTMLInputElement>("#my-tweak-toggle")!;
        toggle.checked = api.storage.get("enabled") ?? false;
        toggle.addEventListener("change", () => {
          api.storage.set("enabled", toggle.checked);
        });
      },
    });
  },
  stop() {},
} satisfies Tweak;
```

### index.ts — DOM Injection with Cleanup
```ts
import type { Tweak } from "@codex-plusplus/sdk";

let cleanup: (() => void) | null = null;

export default {
  start(api) {
    // Wait for DOM element to appear
    const unobserve = api.dom.waitFor(".codex-toolbar", (toolbar) => {
      const btn = document.createElement("button");
      btn.textContent = "My Action";
      btn.className = "codex-plusplus-btn";
      btn.addEventListener("click", () => {
        api.log.info("Button clicked");
      });
      toolbar.appendChild(btn);

      cleanup = () => btn.remove();
    });

    api.onStop(() => {
      unobserve();
      cleanup?.();
    });
  },
  stop() {},
} satisfies Tweak;
```

### index.ts — Keyboard Shortcut
```ts
import type { Tweak } from "@codex-plusplus/sdk";

export default {
  start(api) {
    const handler = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.shiftKey && e.key === "k") {
        e.preventDefault();
        api.log.info("Shortcut triggered: Cmd/Ctrl+Shift+K");
        // your action here
      }
    };

    document.addEventListener("keydown", handler);
    api.onStop(() => document.removeEventListener("keydown", handler));
  },
  stop() {},
} satisfies Tweak;
```

---

## Tweak API Reference (`api` object in `start`)

| API | Description |
|---|---|
| `api.log.info(msg)` | Log to Codex++ console |
| `api.log.warn(msg)` | Warning log |
| `api.log.error(msg)` | Error log |
| `api.settings.register({ id, title, render })` | Add a panel under Settings → Tweaks |
| `api.storage.get(key)` | Read persisted value for this tweak |
| `api.storage.set(key, value)` | Persist value (JSON-serializable) |
| `api.dom.waitFor(selector, cb)` | Watch for a DOM element; returns unobserve fn |
| `api.onStop(fn)` | Register a cleanup callback called on `stop()` |

---

## Config (`config.json`)

```json
{
  "autoRepair": true,
  "autoUpdateRuntime": true,
  "tweaks": {
    "com.yourname.my-tweak": {
      "enabled": true
    }
  }
}
```

- **`autoRepair`** — watcher re-patches after Codex updates (default `true`)
- **`autoUpdateRuntime`** — daily runtime refresh from CLI (default `true`); disable in Settings → Codex Plus Plus → Config

---

## Tweak Update Checks

Every tweak with `githubRepo` set is checked against GitHub Releases once per day. Codex++ compares the latest release tag (semver) to the local `manifest.json` version.

- **No auto-update** — users see "Update Available" in Settings → Tweaks with a link to the release.
- To publish a tweak update: create a GitHub Release with a semver tag (e.g. `v0.2.0`) and attach the tweak folder as a zip.

---

## Default Tweaks

Installed on first run (skip with `--no-default-tweaks`):

| ID | Repo |
|---|---|
| `co.bennett.custom-keyboard-shortcuts` | `b-nnett/codex-plusplus-keyboard-shortcuts` |
| `co.bennett.ui-improvements` | `b-nnett/codex-plusplus-bennett-ui` |

---

## Updating Codex (macOS — Sparkle conflict)

Codex++ ad-hoc signs the app, breaking Sparkle's integrity check. Use:

```sh
codexplusplus update-codex
```

This restores an official Developer ID–signed build for the updater. After Codex updates and restarts, the launch agent watcher re-applies Codex++ automatically.

---

## Uninstall

```sh
codexplusplus uninstall
```

Restores the backed-up original `app.asar`, removes the launch agent, and removes `<user-data-dir>`. Tweaks you wrote remain on disk unless you delete them manually.

---

## Troubleshooting

### "App is damaged and can't be opened" (macOS)
The ad-hoc signature isn't trusted on first launch. Run:
```sh
xattr -cr /Applications/Codex.app
```
Then open the app again.

### Patch not persisting after Codex update
The launch agent should re-run `repair` automatically. Check status:
```sh
codexplusplus status
codexplusplus doctor
```
If the launch agent isn't running, reinstall:
```sh
codexplusplus uninstall && codexplusplus install
```

### Tweak not loading
1. Check `manifest.json` has all required fields (`id`, `name`, `version`, `githubRepo`, `author`, `description`, `minRuntime`).
2. Ensure `index.js` / `index.ts` exports a default object with `start` and `stop`.
3. Check logs: `api.log.error` output appears in Codex DevTools console.
4. Run `codexplusplus doctor` for runtime integrity checks.

### Runtime version mismatch
```sh
codexplusplus repair   # refreshes runtime from CLI
```

### Tweaks directory location
```sh
codexplusplus tweaks open   # opens in Finder/Explorer
```

---

## Security Model

- Tweaks run in the **renderer process** with the same privileges as Codex's own renderer code.
- Codex++ does **not** auto-update tweak code — users must manually review and install updates.
- `githubRepo` is only used for version checks via the GitHub Releases API, not for auto-downloading code.
- See [`SECURITY.md`](https://github.com/b-nnett/codex-plusplus/blob/main/SECURITY.md) for the full policy and vulnerability reporting process.

---

## Community

- [Discord](https://discord.gg/6bY6gGX36H) — `#tweak-dev` channel for tweak authors
- [GitHub Issues](https://github.com/b-nnett/codex-plusplus/issues) — bug reports and feature requests
- Docs: [`docs/WRITING-TWEAKS.md`](https://github.com/b-nnett/codex-plusplus/blob/main/docs/WRITING-TWEAKS.md) and [`docs/ARCHITECTURE.md`](https://github.com/b-nnett/codex-plusplus/blob/main/docs/ARCHITECTURE.md)
