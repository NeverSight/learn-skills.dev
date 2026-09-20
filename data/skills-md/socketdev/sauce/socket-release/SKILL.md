---
name: socket-release
description:
  Stand up SocketDev publishing (npm, crates.io, GitHub releases, Homebrew
  tap) in a repo - copy in the socket-release kit from a sauce checkout and
  run its bootstrap through name reservation, GitHub environments, npm
  trusted publisher, publishing-access tightening, staged publish config,
  and verification.
disable-model-invocation: true
---

# Socket Release Setup

Install the socket-release kit into the current repo and stand publishing
up. Everything destructive is dry-run by default; the bootstrap prints the
exact next command after every run, and every human moment renders as a
🖐 HUMAN GATE - stop and show it, never improvise around it.

## When to Use

- Standing up publishing in a repo that has never released - reserving the
  package name, wiring the npm trusted publisher, restricting GitHub
  environments, and tightening publishing access to staged-only.
- Adding a new channel (npm, crates.io, GitHub releases, or a Homebrew tap)
  to a repo that already publishes on the others.
- Cutting a release once publishing is stood up: stage the artifact, then
  clear the human-gated approve before anything becomes public.
- Any time you want the staged-then-approve safety model - a verified,
  hashed artifact held behind a human gate - instead of a one-shot publish.
- Recovering or verifying an existing setup: re-run the bootstrap `verify`
  to confirm the trusted publisher, environments, and access are still
  conforming.

Each channel has its own subskill; this top-level skill installs the kit,
runs the bootstrap, and points you at the right channel subskill for the
actual publish.

## Steps

<details><summary>Clone the kit, install it, pin its deps, then bootstrap through the gates</summary>

1. **Get the kit source.** Shallow-clone sauce to the canonical clone home:

   ```bash
   git clone --depth=1 --single-branch https://github.com/SocketDev/sauce.git ~/.socket/_wheelhouse/repo-clones/SocketDev-sauce
   ```

   Done when: `~/.socket/_wheelhouse/repo-clones/SocketDev-sauce/release-kit/install.mts` exists.

2. **Install the kit.** Plan first, then apply with the channels this repo
   publishes on (`npm`, `crates`, `github-release`, `brew`):

   ```bash
   node ~/.socket/_wheelhouse/repo-clones/SocketDev-sauce/release-kit/install.mts --target . --channels npm,github-release
   node ~/.socket/_wheelhouse/repo-clones/SocketDev-sauce/release-kit/install.mts --target . --channels npm,github-release --apply
   ```

   Done when: the same command with `--verify` exits 0.

3. **Pin the kit dependencies.** The payload imports plain specifiers; add
   the exact pins:

   ```bash
   pnpm add -D @socketsecurity/lib@6.5.2 @socketsecurity/sdk@4.1.3 playwright-core@1.61.1
   ```

   Done when: `node scripts/socket-release/bootstrap.mts preflight` shows
   the `kit-deps-resolvable` check passing.

4. **Bootstrap.** Run the plan, then follow `nextCommand` and the gates:

   ```bash
   node scripts/socket-release/bootstrap.mts
   node scripts/socket-release/bootstrap.mts --apply
   ```

   The run stops at human gates (reserve-name consent, npm web-2FA,
   staged-placeholder promote, GitHub 403 fallback) - render the gate and
   wait. Done when: `node scripts/socket-release/bootstrap.mts verify`
   exits 0 and reports the stood-up detail (trusted publisher conforming,
   environments restricted, publishing access staged-only).

</details>

## Browser law

Playwright browser law (verbatim, non-negotiable):

- Launch ONLY via openNpmBrowserSession (scripts/socket-release/publish-infra/npm/browser-session.mts) on the durable staged-browser profile that module owns under ~/.config.
- The launch shape is channel + chromiumSandbox: true + headless + the two sanctioned ignoreDefaultArgs entries, and nothing else - never an args array, never a sandbox-disabling flag.
- Login is NEVER scripted: the operator signs in once in the headed window; no password, OTP, or cookie passes through the process.
- All npm browser tools share the ONE durable profile so a single sign-in covers every tool.
- npm auth is decided by the /-/whoami BODY on the website origin, never the HTTP status.
- A human-verification challenge PAUSES the run for the operator with a visible countdown and is never retried blindly.

## Operating the channels

- **npm staged publishing**: see [npm-publish](npm-publish/SKILL.md)
- **GitHub releases + ORDER RULE**: see [github-release](github-release/SKILL.md)
- **crates.io staged model**: see [cargo-publish](cargo-publish/SKILL.md)
- **Homebrew tap bumps**: see [brew-publish](brew-publish/SKILL.md)

## Tips

- Start every destructive run with `--dry-run` and read the plan before you
  add `--apply`; nothing writes to a registry until you drop the dry-run.
- Respect the human gates: when a 🖐 HUMAN GATE prints (reserve-name
  consent, npm web-2FA, staged-placeholder promote, GitHub 403 fallback),
  render it verbatim and wait - never script the sign-in or improvise past
  the gate.
- Let the bootstrap run its eight steps in canonical order - `preflight`,
  `placeholder`, `npm-access-permissive`, `github-env`, `staged-config`,
  `trusted-publisher`, `npm-access-staged-only`, `verify` - and follow the
  `nextCommand` it prints rather than jumping ahead; the order brackets the
  irreversible placeholder publish between permissive and staged-only access.
- Pin the kit dependencies to exact versions before bootstrapping; the
  `kit-deps-resolvable` preflight check fails fast when they drift.
- Prefer the staged path over `--direct`: staged gives you a verified,
  hashed artifact and a server-side rescue before anything goes public, and
  on crates.io the publish is permanent (yank-only), so the approve gate is
  the last stop before it is forever.
- Re-run `bootstrap.mts verify` after any change to confirm the trusted
  publisher, environments, and publishing access are still conforming.
