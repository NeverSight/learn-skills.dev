---
name: omarchy-flux
description: Use, install, diagnose, develop, and release Omarchy Flux. Use this skill for the flux-cli command, fluxd, Flux for Android, Flux for iOS, Flux for macOS, phone, iPhone, and Mac pairing, connections through Tailscale, file or clipboard transfers, phone notifications, webcam or microphone streams, screen mirror, fingerprint approval, herdr agents on the phone, the Flux Qt app, the Flux Omarchy plugin, AUR packages, and Flux APK workflows. Scope this skill to Flux tasks, not general Android or Omarchy configuration.
---

# Omarchy Flux

Flux connects an Omarchy desktop to Flux for Android, Flux for iOS, or Flux for macOS on the same local network.
A paired device can also connect through Tailscale with an extra address.
The desktop includes the `flux-cli` command, `fluxd`, a Qt app, and an Omarchy shell plugin.
`flux` is a short name for `flux-cli` when no other program uses it.
The `fluxcd` package also installs a `flux` command, so always run `flux-cli`.

## Choose the task

| Task | Reference |
| --- | --- |
| Pair a phone, use the CLI, change settings, or diagnose a connection | [Runtime reference](references/runtime.md) |
| Build, install, test, package, or release Flux | [Build and release reference](references/build-release.md) |
| Change the source | Read the relevant files in the repository and the topic in `docs/README.md`. |
| Change fingerprint approval | Read `docs/approve.md` before you edit the approval code. |
| Answer what a paired device can do, or limit it | Read `docs/security.md`. |

Find the repository from the working directory or ask for its path.
Do not assume that an installed skill lives inside the repository.
Run repository commands from its root unless the reference names another directory.

## Start with the current state

For an installed Flux system, run:

```sh
flux-cli version
flux-cli status --json
flux-cli doctor
```

For source work, run:

```sh
git status --short
git remote -v
```

Preserve existing changes.
Use the configured Git remote for clone and release URLs.
If no remote exists, ask for the repository URL before a remote operation.

`flux-cli setup` returns 1 when the service step or the plugin step fails.
A missing system part does not change the exit code.
Inspect its output and confirm the result with `flux-cli doctor` and `flux-cli status --json`.

## Operate Flux

1. Find the requested phone in `flux-cli status --json`.
2. Select its device ID when more than one phone is present.
3. Run the requested command from the runtime reference.
4. Check the result from the command or the next state event.

Example:

```sh
flux-cli status --json
flux-cli --device "Pixel 8" send "$HOME/Downloads/report.txt"
flux-cli status --json
```

The send command starts a transfer.
Check `transfers` in the state before you report that the file arrived.

Use `flux-cli status --json` for scripts.
Use `flux-cli watch` only when the task needs a continuous event stream.
Stop the watch process when the task ends.

`flux-cli` without arguments opens a window.
Use an explicit command for diagnostics.

## Pair and connect

1. Check that both devices use the same local network.
2. Open Flux for Android, and keep it on the screen.
3. Run `flux-cli discover`.
4. Run `flux-cli pair "Pixel 8"` with the device name from the state.
5. Ask the user to compare all 16 characters of the verification key on both devices.
6. Let the user accept the matching request on the phone.
7. Ask the user to select **Confirm** in the Flux window or in the notification on the desktop. The desktop pins the phone only after this step.
8. Confirm that the device is paired and online.

The verification key has 16 uppercase hex digits in 4 groups of 4, for example `5EE6 825F 974E D59A`.
An earlier Flux app shows only 8 characters. Tell the user to update Flux on every device before the pairing.
`flux-cli pair` prints the device ID and the key. `flux-cli status` shows the ID and the certificate fingerprint of each device.
When stdin is not a terminal, `flux-cli pair` prints a `flux-cli accept` command after the phone accepts. `flux-cli accept DEVICE` without a key prints the same command. Run it only after the user says that the phone shows the same key. The pairing stops after 30 seconds.
A name matches only a paired or connected device, and a paired device comes first. When the name still matches more than 1 device, the command returns the `ambiguous` error with the IDs. Give the ID then. `docs/cli.md#pair-and-discover` has the match rule of each command.

The desktop discovers phones through Avahi and mDNS.
The desktop opens connections to the phone, including reverse payload tunnels.
`fluxd` also listens on 1 TCP port from 12100 to 12108 and on UDP port 12100, but a connection does not need inbound traffic.
A missing connection does not require a new desktop firewall rule.
Do not open the Flux ports in the firewall, because each host that reaches them can then send a pair request.
Flux for Android takes a new computer only while Flux is on the screen or while it scans.
Check the daemon, Avahi, Wi-Fi isolation, and phone state first.

Discovery and pairing need the local network.
To reach a paired phone away from that network, add its Tailscale name as an extra address:

```sh
tailscale status
flux-cli --device "Pixel 8" addresses add pixel-8
flux-cli addresses
```

Use the device name from `flux-cli status --json` and the host name from `tailscale status`.
Read `docs/tailscale.md` for the dial order, limits, and checks.

## Respect the requested operation

SMS, notifications, clipboard transfers, and file transfers affect another device.
Use the destination and content that the user requests.
Keep private keys, notification contents, phone numbers, and signing secrets out of reports unless the task needs them.

Pairing needs the user's key comparison.
Fingerprint enrollment needs the user's fingerprint, Face ID, or Touch ID, and the key code that the user types from the device screen.
Do not claim that these physical steps succeeded without evidence.

Use `flux-cli commands add` for desktop commands that the phone can run.
`flux-cli run ID` runs a configured command on the desktop, not on the phone.
Do not expand a command's permissions beyond the user's request.

## Install locally

Install the Arch package for a complete install on Omarchy.
It includes the Qt app, CLI, daemon, plugin assets, PAM helper, desktop entry, icons, and system files.
pacman owns its files, so a later package install or update has no file conflicts.

From the repository root:

```sh
cd dist/arch
makepkg -si
flux-cli setup
flux-cli doctor
```

Run `makepkg` as a regular user. pacman runs the system setup.
Run `flux-cli setup` as each desktop user who wants Flux. The package does not start `fluxd` for the accounts on the computer.
Use `docs/install.md` for dependencies, the pacman package, and the user-only install.

`make build` and `sudo make install` also install into `/usr`, but pacman does not own those files.
Use them only on a system without pacman.
A later `makepkg -si` or `yay -S omarchy-flux` then stops with `exists in filesystem` conflicts.

To install the latest release, run `flux-cli update`.
It asks for the sudo password, so run it in a terminal that the user sees.
It checks `SHA256SUMS.sig` with the public release key when the build has one, and then the checksum of the package.
After an update, `fluxd.service` restarts into the new binary when no transfer, stream, remote desktop, Browse PC session, app send, or approval runs.
Confirm the running version:

```sh
flux-cli version
```

To send the latest Android app to a phone, run `flux-cli --device "Pixel 8" update --phone`.
The user then installs it from the notification on the phone.
A Flux app from before the port change to UDP 12100 cannot connect, so `update --phone` cannot reach it.
See `docs/troubleshooting.md#a-device-does-not-find-the-computer-after-an-update`.
`fluxd` checks GitHub once a day for a new release.
`check_updates = false` in `config.toml` turns the check off.

Use `docs/install.md` for the update command of each install method.

For a preview without installation:

```sh
make build
./bin/flux-cli setup --dry-run
```

## Develop the correct component

| Component | Source |
| --- | --- |
| CLI | `cmd/flux/` |
| Daemon entry point | `cmd/fluxd/` |
| Device state and IPC methods | `internal/core/` |
| Network and protocol | `internal/lan/`, `internal/proto/` |
| Configuration and trust | `internal/config/` |
| Desktop integration | `internal/desktop/` |
| Shared Qt views | `gui/qml/` |
| Qt host | `gui/app/` |
| Omarchy shell host | `gui/omarchy/` |
| Android app | `android/app/src/main/java/org/omarchy/flux/` |
| macOS app | `macos/Sources/FluxKit/`, `macos/App/` |
| iOS app | `ios/App/`, `ios/ShareExtension/`, and the shared `macos/Sources/FluxKit/` |
| Fingerprint approval | `internal/approve/`, `cmd/flux-approve/`, `internal/core/approve.go`, Android `core/Approve*` and `ui/ApproveActivity.kt`, `macos/Sources/FluxKit/Plugins/Approve/`, `macos/App/Features/Approve/`, `ios/App/Features/Approve/` |
| herdr agents | `internal/herdr/`, `internal/core/herdr.go`, Android `core/Herdr.kt` |
| Live terminal | `internal/herdr/terminal_session.go`, `internal/core/herdr_terminal.go`, Android `ui/HerdrTerminal.kt` and `assets/terminal/` |
| Package and system install | `dist/`, `Makefile` |

Keep network state in `fluxd`.
The CLI and both desktop hosts use its Unix socket.
Keep shared QML free of Quickshell imports.
Update both host adapters when you change their shared backend contract.
Test wire changes on the Go, Kotlin, and Swift implementations.

Use the existing tests for the component you change.
Run these checks for a complete build change:

```sh
make build test vet
cd android
./gradlew :app:testDebugUnitTest :app:lintDebug :app:assembleDebug :app:assembleRelease --no-daemon
```

On a Mac with Xcode and XcodeGen, run `make test-macos macos` and `make ios test-ios` from the repository root.
Use `docs/macos.md` for the macOS app and `docs/ios.md` for the iOS app.
For an approval change, run the Go and Android approval tests.
For an approval change in FluxKit or the Apple apps, also run the Swift approval tests with `make test-macos test-ios`. They run only on a Mac or in the `macos` and `ios` jobs of CI.

For a change in `gui/`, run `make build-gui snapshot test-gui`.
Use `docs/development.md` for isolated daemon tests, UI snapshots, and the QML view tests.
Do not run a second development daemon against the user's active socket or trust store.

## Release

Read the build and release reference before you change workflows or prepare a tag.
The workflows support stable tags in `vMAJOR.MINOR.PATCH` form.
The release workflow checks out that tag for both desktop and Android builds.

Keep one Android release key across releases.
The workflow requires signing secrets and refuses a debug-signed APK.
The AUR recipe includes a source checksum and the install hook.
The AUR job uses the tested recipe only after the GitHub release succeeds.

Do not create a tag, push, publish, or change repository secrets unless the user requests that action.
For preparation work, report the required setup and the commands without running the remote action.

## Report the result

Include:

- The completed operation or changed files.
- The selected device or release tag when relevant.
- The checks that passed.
- Any check that failed or could not run.
- The next required user action, such as a phone prompt or a release secret.

Distinguish a successful local build from a published release.
Distinguish a queued transfer from a completed transfer.
