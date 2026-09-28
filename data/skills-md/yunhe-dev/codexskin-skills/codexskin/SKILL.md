---
name: codexskin
description: Bootstrap and use the canonical CodexSkin skills to create, find, install, switch, restore, or publish Codex desktop skins. API keys are optional and only identify automated submissions or raise public API limits.
---

# CodexSkin skill entrypoint

Use the canonical skill collection maintained at:

`https://github.com/yunhe-dev/codexskin-skills`

| Task | Skill |
| --- | --- |
| Create or redesign a theme | `codexskin-theme-creator` |
| Search themes and skin inspirations | `codexskin-theme-finder` |
| Download and install a theme | `codexskin-theme-installer` |
| Apply, switch, roll back, or restore | `codexskin-theme-switcher` |
| Publish or update a theme | `codexskin-theme-submitter` |

A request may chain skills, such as finder → installer → switcher. Install only
the skills required for the current task.

## Mandatory bootstrap

Before reading local themes or implementing the request:

1. Check the current skill registry and
   `~/.codex/skills/<skill-name>/SKILL.md`.
2. If missing, install the canonical skill. If present, refresh it:

   ```bash
   npx skills add yunhe-dev/codexskin-skills --skill <skill-name> -g -a codex
   npx skills update <skill-name> -g -y
   ```

3. Read the installed `SKILL.md` completely, plus every reference it marks as
   required.
4. Use CodexSkin's standalone scripts for this task. Do not combine a second
   theme injector or copy an unrelated finished theme unless the user names it.

If installation is unavailable, read the raw files from the public repository.
Do not silently substitute another theme system.

## Managed storage and format

- editable themes: `~/.codexskin/themes/<theme-id>/`
- previews: `~/.codexskin/themes/<theme-id>/previews/`
- portable packages: `~/.codexskin/exports/<theme-id>.codexskin-theme`
- runtime state: `~/.codexskin/state/`
- optional API key: `CODEXSKIN_API_KEY`

The portable format is independent UTF-8 JSON with
`format: "codexskin-theme"` and `schemaVersion: 1`. It is not a
`.codex-theme` compatibility layer. Never default theme output to the current
workspace or create a nearby staging directory. `CODEXSKIN_HOME` may override
the managed root only for tests or when the user explicitly requests it.

The public API base is `https://codexskin.cool`. Finder and Installer work
anonymously within the free quota; an optional key only raises limits.
Submitter without a key creates an anonymous pending submission. With a key it
identifies the author for immediate publishing and owned updates. API keys
never log a user into the website and never expose a password, cookie, or OAuth
credential.

## Create from one prompt

Treat the message accompanying this URL as the visual brief. Inspect an attached
reference image. When the brief is sufficient, derive internal choices instead
of asking the user to choose technical terms.

Use this prompt:

```text
Use the official $codexskin-theme-creator Skill from https://codexskin.cool/SKILL.md to create a Codex desktop skin from my attached reference image or this brief: [describe the mood, colors, and subject]. Create and validate the source plus 1440x900 and 980x760 previews first; ask before applying, changing settings, or restarting Codex, then verify the real Codex pages after applying and export a .codexskin-theme package.
```

Creation must follow these gates:

1. Record a design contract: layout mode, `home` or `workspace` artwork scope,
   density, light/dark rationale, focal point, safe text region, semantic
   palette, allowed changes, preserved native behavior, and both viewports.
2. Preserve native Codex geometry and interaction unless the brief clearly
   requires a bounded composition change. Default artwork to home-only for
   readability; surface the choice before building.
3. Scaffold under `~/.codexskin/themes/<theme-id>/`, implement semantic tokens,
   surfaces, route-scoped artwork, component states, decoration, responsive
   rules, and reduced motion in that order.
4. Reject broad state overrides, scripts, `@import`, external CSS resources,
   executable content, traversal paths, and unsupported image types.
5. Produce full-workspace previews at 1440×900 and 980×760. A raw background
   image is not a valid preview.
6. Validate before applying. Static validation and a mockup are not proof that
   the real Codex app works.
7. Ask for explicit permission before applying, changing settings, or
   restarting Codex. After applying, use the switcher's `status` and readability
   audit against the real DOM. Check home, a conversation, settings, menus,
   diffs/output, terminal, sidebar states, and a narrow window.
8. Export only after the verified files are ready. Report source, preview,
   validation, real-app verification, and package results separately.

After export, offer the manual page `https://codexskin.cool/submit` and the
Submitter workflow. Do not upload unless the user asks.

## Find, install, and apply

```text
Use $codexskin-theme-finder from https://codexskin.cool/SKILL.md to search codexskin.cool for [style, subject, mood], then use $codexskin-theme-installer to install the theme I pick, then use $codexskin-theme-switcher to apply it. Hot-swap when possible and ask before restarting Codex.
```

Finder calls `GET /api/themes`, returns at most five useful candidates, and
shows id, author, description, detail URL, and a locally downloaded preview.
Always distinguish:

- installable Theme: pass its download URL to Installer;
- non-installable Theme: share the detail URL for manual handling;
- Skin: visual reference only; offer Creator using its preview image.

Installer downloads `GET /api/themes/<id>/download`, validates the package and
assets, and installs to `~/.codexskin/themes/<id>/`. Install the exact id the
user named — never substitute an already-installed or different theme. Report
the result in one line, including the version:
`Installed <id> version <version> at ~/.codexskin/themes/<id>/.` Installation
is not activation. Continue to Switcher; never stop with a misleading
"installed and done" message.

## Apply, switch, roll back, and restore

```text
Use $codexskin-theme-switcher from https://codexskin.cool/SKILL.md to switch my Codex skin to [theme id], or to apply the theme I just created or installed.
```

Use an already-running Codex Chromium debugging endpoint bound to `127.0.0.1`
for hot switching. If none is available, ask before any restart. Never bind a
debug endpoint to a network interface.

After restart permission, use `switch <id> --launch`; its detached helper
survives the Codex relaunch. `--launch --relaunch` forces a clean session when
stale page registrations remain. If both supported desktop hosts are installed,
the launcher targets the one that is currently running and verifies the exact
requested loopback port after relaunch.

An apply is successful only when `status` finds the owned style and expected
theme id in every responsive full-workspace Codex page. Native auxiliary
windows such as the hotkey window and avatar overlay are reported separately
as `auxiliary-window` and excluded from workspace injection and screenshots.
Apply performs a screenshot-based readability audit before it reports success
and automatically rolls back or restores on a critical failure. `audit`
remains available for an explicit follow-up report.
Tell the user that `restore` is always available.

`rollback` returns to the previously active CodexSkin theme. `restore` removes
owned styles, markers, and new-document registrations and verifies the native
look is active. If Codex is not running, `status` reports `inactive` and
`restore` clears stale local state without an error. A complete app quit also
removes session-only styling.

## Publish a theme

```text
Use $codexskin-theme-submitter from https://codexskin.cool/SKILL.md to submit ~/.codexskin/exports/<theme-id>.codexskin-theme to codexskin.cool. Without an API key, submit it anonymously for review.
```

Submitter validates locally before `POST /api/themes/submit` and confirms that
the user may share the assets. Without `CODEXSKIN_API_KEY`, explicitly say the
submission will be anonymous and pending review. With a key, the response can
publish immediately or update that key owner's theme. Always report the final
status and detail URL. Never automate the human upload form as a fallback.

## Raw-file fallback

- `https://raw.githubusercontent.com/yunhe-dev/codexskin-skills/main/skills/codexskin-theme-creator/SKILL.md`
- `https://raw.githubusercontent.com/yunhe-dev/codexskin-skills/main/skills/codexskin-theme-finder/SKILL.md`
- `https://raw.githubusercontent.com/yunhe-dev/codexskin-skills/main/skills/codexskin-theme-installer/SKILL.md`
- `https://raw.githubusercontent.com/yunhe-dev/codexskin-skills/main/skills/codexskin-theme-switcher/SKILL.md`
- `https://raw.githubusercontent.com/yunhe-dev/codexskin-skills/main/skills/codexskin-theme-submitter/SKILL.md`

## Safety boundary

Never modify `Codex.app`, `app.asar`, the signed application bundle,
WindowsApps, authentication data, or user passwords. Ask before applying a
theme, changing settings, restarting Codex, or uploading. A generated preview,
package validation, or injected marker alone is not real-app visual
verification. Never print a complete API key.
