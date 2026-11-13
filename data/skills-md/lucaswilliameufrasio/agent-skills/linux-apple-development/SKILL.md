---
name: linux-apple-development
description: >-
  Plan, set up and verify iOS/macOS development from CachyOS, Arch, Debian or
  Ubuntu, with a Mac used as an SSH controller or an optional Apple build/test
  host. Use for omarchy-apple-dev, xtool, Swift/Darwin SDKs, Linux-built Apple
  apps, Flutter iOS builds, device deployment, signing or notarization across
  Linux and macOS. Separate Linux build capability from Apple runtime validation;
  inspect distro, language, toolchain and SDK compatibility before installing.
  Do not assume Swift tooling builds Cargo apps or that remote administration
  requires an Apple development toolchain.
---

# Apple development from Linux, controlled from a Mac

Reuse maintained upstream tools instead of maintaining a second distribution of
their SDK patches. This skill owns selection, safe orchestration and evidence;
the upstream project owns its installer and tool implementations. A Mac terminal
controlling a server does not make that server a macOS machine.

## 1. Resolve the actual job and topology

Inspect repository instructions and manifests before proposing a toolchain.
Identify:

- Goal: build an Apple app, exercise it, sign/package it, deploy to a device,
  publish it, or simply administer Linux servers? For ordinary SSH administration,
  explain that `omarchy-apple-dev` is unrelated; do not install Apple tooling.
- App: Swift/SwiftUI, Objective-C/C/C++, Flutter, Rust/Cargo, or mixed native
  dependencies? Record iOS versus macOS, deployment target and CPU architectures.
- Hosts: where the source, build, tests, SDKs and credentials live; which machine
  runs the agent; which device actually runs the app. Do not assume an iPhone,
  paid account, Xcode or remotely reachable Mac exists because the user has a Mac.
- Requested authorization: proposal, read-only audit, installation, local build,
  device control, signing, upload and submission are separate scopes.

Read [topologies and upstream scope](references/topologies.md). Prefer the user's
existing workflow. One Mac can remain the interactive controller and Apple runtime
verifier while Linux performs compatible builds. It need not become an always-on
public CI service or receive every build job.

## 2. Choose a verified route, not a universal installer

Read [distribution preflight](references/distros.md) for the actual OS/version and
architecture. Check current upstream documentation/source at a recorded revision;
read support receipts, not just headlines. Distinguish upstream-tested,
community-reported, locally verified and untested combinations in every plan.

For Swift-family projects, `omarchy-apple-dev`/xtool may provide the Linux build
route. Ubuntu already has upstream documentation and dated partial run records;
do not describe a new fork as necessary just to use Ubuntu. Arch evidence does
not automatically prove CachyOS. Debian requires its own dependency/ABI proof or
an explicitly selected compatible builder environment.

For Rust applications, discover the existing Cargo cross-build/macOS workflow.
Do not route `Cargo.toml` through the upstream SwiftPM `ship-mac.sh`. SDKs and
signing knowledge may be relevant, but Rust targets, linker, native libraries,
app bundling and platform-specific tests still need a project-specific solution.
When this is unproven, use an approved Mac native build rather than claiming
arbitrary Rust desktop cross-compilation is supported.

## 3. Read-only preflight before mutation

Inspect only the approved hosts. Use shell preflight appropriate to each host;
the Mac's shell, the SSH remote shell and script Bash requirements can differ.
Do not source login profiles or dump environment variables to discover versions.

Record OS release, architecture, free disk/inodes on both build and scratch
volumes, tool locations and versions, compiler/clang selection, dynamic library
readiness, SDK registration and exact source revision. Do not treat a registered
SDK name, a successful `swift --version` or a working SSH connection as a build
test. SSH sessions may not have the same PATH/XDG configuration as desktop shells.

Check for existing Swift/mise/asdf installations, SDK caches and user-global
tool symlinks before proposing changes. Obtain only secret metadata/references;
do not open Apple private keys, auth caches, pairing records or keychain contents.

## 4. Plan installation and compatibility explicitly

Show selected upstream revision, mode, host, installation prefixes, dependencies,
download/build footprint, credentials needed later and expected side effects.
Ask before downloads, package installs, AUR builds, user tool replacement, SDK
registration/removal, service/USB/TUN changes or persistent host configuration.
The request to author a skill does not authorize configuring the user's hosts.

Review the actual installer and helpers before executing. `--user-only` avoids
system packages, not user-global mutation: it can replace `~/.local/bin` symlinks,
register/remove the Darwin SDK, rebuild a Python environment and modify writable
toolchain/SDK files. Back up or isolate approved owned paths; preserve existing
SDKs, device pairing and authentication. Do not run `--repair` merely to inspect
health, or delete a shared `.build` directory to cure an unproven cache problem.

Select the mode explicitly, including noninteractive SSH runs:

- **full:** requires authorized Xcode SDK artifacts and a compatible Swift/xtool
  toolchain. Inspect exact release/build matching, SDK stamps and project features;
  do not assume matching a major version alone is sufficient.
- **no-xcode:** experimental, with a restricted framework/SwiftUI feature set and
  different device/shipping coverage. It is not a drop-in SDK or macOS-app route.
  Check current test matrix for what linked, launched or was actually exercised.

Obtain Apple artifacts through authorized channels and review applicable terms;
do not suggest redistributing SDKs or bypassing licenses. Copy from a Mac only
when authorized and compatible; having one Mac does not require exporting its
SDK or credentials to every server. Pin and verify downloads/dependencies using
the toolchain's current authenticity mechanisms. Do not invent ABI fixes with
system-wide SONAME symlinks or blanket library-path changes.

## 5. Prove one build without shipping it

Start with the existing app's smallest representative supported build or an
explicitly approved disposable sample. Use owned disk-backed build/scratch paths,
bounded resources and unique output directories. Do not put a repository checkout
under a temporary filesystem. Record the full toolchain/SDK/upstream revision.

Inspect the artifact rather than trusting command exit: executable format and
architecture, bundle metadata, embedded libraries/resources and deployment target.
An arm64 Mach-O is not a Linux executable. A Linux unit test cannot verify AppKit,
SwiftUI, native dialogs, Metal, Gatekeeper, keychain or an iPhone runtime.

For a Mac runtime check, transfer the exact approved artifact with a manifest and
hash, validate it on the Mac, then launch/control only within approved scope.
SSH command access alone does not grant an interactive macOS GUI session or
screen-recording/accessibility consent. For iOS, prove provisioning, installation,
launch and an observable journey on the actual device separately. Build-only
success remains build-only when those resources are unavailable.

## 6. Keep devices, credentials and publication separate

Read [security and release gates](references/security-release.md) before any
device, signing or upload step. Prefer keeping signing identities on the existing
trusted Mac or designated signer when practical; do not automatically export keys
to Linux to avoid a signing-stage boundary. Check identity/team/entitlement and
artifact compatibility independently of where compilation happened.

USB pairing, wireless access and TUN tunnels depend on device/OS/tool versions
and physical access. Do not assume the Mac's USB cable is visible to the Linux
server or that Tailscale provides USB, mDNS, GUI permission or device trust.
Never scan a network or copy pairing material to other hosts without scope.

Inspect shipping script defaults: “build” commands may also sign, provision,
create certificates, upload or use test identities. TEST/ad-hoc signatures are
not distribution acceptance. Ask separately before Apple account changes,
notarization, TestFlight/App Store upload or review submission. Record Apple's
processing result when authorized; do not call an upload a published release.

## 7. Report the actual support boundary

Report route and host roles, OS/architecture/toolchain/SDK/source versions,
artifacts and verification evidence. Mark install, compile, sign, runtime,
device deploy, notarization and publication independently as passed/failed/not
run. State what remains blocked and the smallest next action/owner.

Do not claim CachyOS, Debian and Ubuntu parity from testing only one host, or
claim every framework works because a sample compiled. Keep caches and evidence;
clean up only owned resources and stop owned device/tunnel sessions. Put exact
project commands in its own runbook/verifier. Maintain no silent global agent
configuration or background Mac build service as a side effect of this skill.
