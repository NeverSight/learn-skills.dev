---
name: astroshot
description: >
  Capture deterministic PNG screenshots and journey movies with the unified
  @archastro/astroshot CLI. Use React for isolated browser components, Ink for
  fixed terminal component states, PTY for real interactive terminal
  executables, and movie for browser, truecolor PTY, native macOS window, or
  custom-frame recordings. Use agent-browser for one-off live browser actions;
  use astroshots-review to stream captures and read feedback; use screenshot
  to orchestrate a documentation image set.
---

# Astroshot capture

## Native `archdev shots` support

When `archdev shots` is available and enabled, the same engine runs as a
command group of `archdev`. Detect it once per session:

```bash
if command -v archdev >/dev/null 2>&1 && archdev shots doctor >/dev/null 2>&1; then
  NATIVE=1   # archdev shots is installed and enabled
else
  NATIVE=0   # use the standalone astroshot commands in this skill
fi
```

`archdev shots doctor` exits 0 only when the feature is installed and enabled
(`archdev settings set shots on`). Any other result means: use the standalone
`astroshot` commands below, which stay the fallback.

| Standalone | Native |
|---|---|
| `astroshot react\|ink\|pty\|movie …` | `archdev shots react\|ink\|pty\|movie …` |
| `astroshot review` | `archdev shots review` |
| `astroshot doctor`, `init`, `demo` | `archdev shots doctor`, `init`, `demo` |
| render, then `astroshot-capture --source` | `archdev shots react\|ink\|pty <fixture> --feature <f> --slug <s>` renders and publishes into `.astroshot/<f>/` in one step |
| `astroshot-capture …` | `archdev shots capture …` |

Subcommands and arguments are otherwise identical, so every `astroshot …`
example in this skill works as `archdev shots …`.

Use one CLI with four capture boundaries:

| Target state | Mode | Read |
|---|---|---|
| Isolated browser React component | `react` | [React mode](references/react.md) |
| Fixed Ink component tree | `ink` | [Terminal modes](references/terminal.md) |
| Real terminal executable and keyboard flow | `pty` | [Terminal modes](references/terminal.md) |
| Multi-step journey recording | `movie` | Run `astroshot movie which-source "<intent>"` first |

Two setup verbs come before all of them:

| Need | Command |
|---|---|
| Prove the `.astroshot` path works, with zero prerequisites | `astroshot demo` |
| Diagnose why nothing appears in the Astroshots tray | `astroshot doctor` |

Choose the smallest boundary that proves the intended state. Do not rebuild a
full application shell in a fixture merely to avoid running the application.

## Preflight

The public command is:

```bash
npx astroshot --help
```

Prove the setup before capturing anything real:

```bash
astroshot demo      # writes a real .astroshot/ set: stills + movie + manifest.json
astroshot doctor    # per-check pass/fail with the exact fix command
```

- `demo` requires **no** Chromium download and no assets of your own. It writes
  bundled fixtures, so it works immediately after install and while the app is
  closed, then prints where to look. Options: `--feature <name>`,
  `--root <dir>`, `--json`.
- `doctor` reports Node vs `engines`, whether this project sits inside a folder
  Astroshots actually watches (read live from the app's own configuration —
  never a guessed `~/Projects`), whether the app is installed and running,
  whether the managed Chromium runtime is present, and macOS Screen Recording
  state for `desktop.window`. Every failing line carries the exact remediation
  command. It exits non-zero when a required check fails, and it never installs
  or mutates anything. Options: `--root <dir>`, `--json`, `--skip-screen`.

When the tray stays empty, run `astroshot doctor` and follow its `fix:` line
instead of guessing about watched folders.

From a clone of the Astroshots repository, use the checked-out CLI when the
package is not yet available from npm:

```bash
node packages/astroshot/bin/astroshot.mjs --help
```

Do not silently substitute the old `react-shot`, `tui-shot`, or
`astroshot-movie` executables. They are engine packages; the supported command
surface is `astroshot demo|doctor|react|ink|pty|movie`.

Install Chromium once:

```bash
npx astroshot install-browser
```

On Linux CI images that need browser system libraries, add `--with-deps`.
Pin an exact Astroshot version in CI.

## Still-image workflow

1. Decide whether fixed props, a fixed Ink tree, or a real PTY process owns the
   state.
2. Read the matching mode reference above.
3. Generate a fixture with `astroshot init react|ink|pty` when starting fresh.
4. Replace generated placeholders with production imports or the real command.
5. Use synthetic data, fixed dimensions, and a content-based readiness check.
6. Capture the PNG and open it with the available image inspection tool.
7. Check clipping, wrapping, loading states, colors, transparency, and private
   data.
8. Report the mode, fixture, command, output path, dimensions, and assertion.

React and Ink also support maintained image sets:

```bash
astroshot react batch ./shots.yaml
astroshot ink batch ./terminal-shots.yaml
```

## Movie workflow

Movies are for journeys, not replacements for stable component stills. Choose
the source from intent before recording:

```bash
astroshot movie which-source "record a native SwiftUI onboarding window"
astroshot movie --help
```

| Intent | `--source` | Never substitute |
|--------|------------|------------------|
| Web / SPA / Playwright | `browser` | Desktop-grab Chrome |
| TUI / CLI / truecolor | `pty` | `desktop.window` on Terminal/iTerm/Ghostty |
| Native macOS app window | `desktop.window` | Browser or terminal capture |
| Caller-owned PNG/JPEG sequence | `frames` | A custom output layout |

1. Run `which-source`; follow its recommendation.
2. Use one stable `--run-id` for movies in the same journey.
3. Supply `--feature`, `--slug`, a human title, and what the movie proves.
4. For native windows, run `list-windows` and check Screen Recording access.
   `desktop.window` refuses off-screen or nearly blank frames by default;
   `--allow-blank` is an explicit escape hatch.
5. Confirm poster, video, duration, source, and chapters under
   `.astroshot/<feature>/`, then finalize execution as `pass` or `fail`.

```bash
astroshot movie run --source browser --feature checkout --slug purchase \
  --url https://example.com/checkout --run-id checkout-20260811

astroshot movie list-windows
astroshot movie run --source desktop.window --feature desktop-onboarding \
  --slug first-run --bundle-id com.example.App --duration-ms 4000
```

Every source writes a poster PNG plus WebM/MP4 video into the normal manifest.
Astroshots shows duration in the Shots stream and provides tray/full-screen
playback. `desktop.window` is macOS-only; browser, PTY, and frames are
cross-platform.

## Review and documentation

`astroshot` creates an image or movie artifact. It does not imply human review.

- To stream a standalone PNG into `.astroshot/<feature>/`, read the
  **astroshots-review**
  skill and pass the file to `astroshot-capture --source` (or
  `archdev shots capture --source` when native support is available).
- Movies already write poster+video+manifest into `.astroshot/<feature>/`; do
  not pass their poster through `astroshot-capture` again.
- To plan, embed, inventory, and render-check a documentation image set, read
  the **screenshot** skill.

Do not infer Seen from `manifest.json.status`; human acknowledgement and
feedback live in the Astroshots `review.json` contract and apply only to the
reviewed run and image hash.

## Trust boundary

Fixtures, configuration, imports, and PTY commands execute with the current
user's permissions. Review untrusted changes before capture. A temporary Vite
server, Chromium process, or pseudoterminal is not a security sandbox.
