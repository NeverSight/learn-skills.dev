---
name: supply-chain-security
description: Review new or changed dependencies for supply-chain compromise before they enter a project — malicious install scripts (preinstall/postinstall), binding.gyp/node-gyp install-time execution (June 2026 worm), self-propagating worms (Shai-Hulud, binding.gyp), credential harvesting and exfiltration, obfuscated payloads, typosquatting, slopsquatting (AI-hallucinated package names), dependency/namespace confusion, maintainer account takeover, and unpinned or unverified versions. Reads manifests, lockfiles, install scripts, and dependency diffs offline across npm, PyPI, Go, Cargo, RubyGems, Maven, NuGet, and Composer, and reports each risk at file:line with a concrete fix — no install, no execution, no phoning home. Trigger when adding or upgrading a dependency, reviewing a PR that changes package.json / requirements.txt / go.mod / a lockfile, deciding whether a package is safe to install, or when the user mentions Shai-Hulud, binding.gyp, a compromised or malicious package, typosquatting, dependency confusion, or asks "is this dependency safe to add?".
---

# Supply-Chain Security Scanner

This skill turns the model into a dependency reviewer. Read the manifests, lockfiles, install scripts, and the dependency diff; walk the detection passes; report each supply-chain risk with a severity and a concrete fix. No tools to install, no package to run, no registry to phone — the analysis is the model reading what's on disk and in the diff.

A dependency is the one thing in your project you didn't write and didn't review, running with your full privileges. The defender's problem is that it *looks* legitimate: the largest npm compromise in history rode `chalk` and `debug` (2 billion weekly downloads) through a phished maintainer, and the Shai-Hulud worm backdoored ~800 packages by republishing them under stolen tokens. Popularity is not safety. The moment to catch this is when a dependency is **added or changed** — that is what this skill reviews.

## Mental model

A new or changed dependency runs code from a stranger **twice**: once at **install time** (lifecycle scripts — on your laptop and your CI runner, before a single line is reviewed) and again at **runtime** (in your app, your users' browsers, your servers). Two questions decide whether it is safe:

- **Identity — is this the package you meant, from who you think published it?** Defeated by *typosquatting* (a misspelling of a popular name), *slopsquatting* (a plausible name an AI hallucinated and an attacker pre-registered), *dependency / namespace confusion* (an internal name claimed on a public registry), and *maintainer account takeover* (a trusted name, a stolen token).
- **Behavior — does it do something a library of its stated purpose has no reason to do?** Especially at install time. Defeated by *malicious lifecycle scripts*, *obfuscated payloads*, *credential harvesting*, *exfiltration*, *persistence*, and *self-propagation*.

The **install-time hook is the crown jewel**. It executes before any code review, on developer machines and CI runners, with full environment and token access — which is exactly why every major worm (Shai-Hulud, the nx `s1ngularity` attack, the June 2026 **binding.gyp** campaign) targets install time. Most land in `preinstall` / `postinstall`; the binding.gyp worm bypasses those hooks entirely by tricking `node-gyp` into running arbitrary shell during a fake native build. A package can be perfectly functional and still own your machine the instant you install it.

**When you cannot confirm a package's identity, or cannot explain what its install script does, treat it as untrusted and flag it.** The cost of a false positive is a held PR and a few minutes. The cost of a false negative is every credential on the machine and in CI — and your own packages republished as the next link in the worm. This asymmetry governs every judgment call below.

## Scan procedure

Walk these passes in order. Pass 0 establishes what you're reviewing and what's new — don't skip it.

### Pass 0: scope what you're reviewing

You can't assess a dependency without knowing the ecosystem and how much of it you can actually see.

- **Identify the ecosystem and files.** `package.json` + a lockfile (npm/pnpm/yarn), `requirements.txt` / `pyproject.toml` / `poetry.lock` / `uv.lock` (PyPI), `go.mod` + `go.sum`, `Cargo.toml` + `Cargo.lock`, `Gemfile` + `Gemfile.lock`, `pom.xml` / `build.gradle`, `.csproj` / `packages.lock.json`, `composer.json` + `composer.lock`. See `references/ecosystems.md` for where install hooks, pinning, integrity, and scoping live in each.
- **Find what's new or changed.** In a PR, the **diff of the manifest and lockfile is the target** — a freshly added package, a version bump, a new transitive entry, a new install script. Note for each: direct vs transitive, new package vs version change, and whether the install runs anywhere holding secrets (CI with publish tokens, a developer laptop with cloud creds).
- **Note how much you can see.** If the package source is on disk (`node_modules/`, vendored, an extracted tarball), you can read its install scripts and payload directly — do it. If you only have a name and version in a manifest, you are limited to identity and hygiene checks; say so, and recommend the confirmation commands in the closing section.

### Pass 1: identity — is this the package you meant?

Before behavior, confirm the name resolves to who you think.

- **Typosquatting.** A name within a small edit or keyboard distance of a popular package: `crossenv`↔`cross-env`, `reqeusts`↔`requests`, `lodahs`↔`lodash`, `electorn`↔`electron`. Flag any dependency whose name is one transposition/omission/duplication away from a well-known package it is not.
- **Slopsquatting (AI-hallucinated names).** Roughly **1 in 5 package names suggested by LLMs don't exist**, and the hallucinations repeat — so attackers pre-register the popular ones with malware. Be suspicious of plausible-but-unfamiliar "helper" names (`flask-gpt-helper`, `auth-helper-pro`, `py-openai-utils`, `easy-requests`). If a dependency was added on an AI's suggestion, **confirm the real package exists under that exact name before installing** — do not let a hallucinated import become an install.
- **Dependency / namespace confusion.** An **unscoped** name that looks internal (`internal-`, `corp-`, `company-`, a product codename) can be hijacked: an attacker publishes the same name publicly with a higher version and wins resolution. Also flag a scope that is *almost* the org's (`@acme-corp` vs `@acme`). The fix is scoped names pinned to the private registry in a committed config — see `references/patterns.md`.
- **Account-takeover smell.** A long-stable package that suddenly ships an odd version, changes maintainer, **adds an install script it never had**, or whose diff adds files unrelated to its purpose — especially a **`binding.gyp`** or a multi-megabyte root **`index.js`** in a package that has never shipped native code. `chalk`/`debug`, nx, Shai-Hulud, and the binding.gyp worm all rode trusted names through phished or stolen tokens. A diff that adds `preinstall` + two new files to a styling library is the shape to fear; so is a diff that adds `binding.gyp` + `index.js` to a pure-JS library.

### Pass 2: install-time execution — the crown jewel

Read every lifecycle script. In npm: `preinstall`, `install`, `postinstall`, and `prepare` in `package.json` `scripts`. Equivalents elsewhere: `setup.py` / PEP 517 build hooks (PyPI), native `extconf.rb` (RubyGems), `build.rs` (Cargo). `preinstall` is the loudest signal — Shai-Hulud 2.0 moved there specifically to run **before** any inspection tooling.

Also read **`binding.gyp`** if present. When npm sees one, it invokes **`node-gyp`** to compile what it assumes is a native addon — **even with `ignore-scripts=true`**, because this is not a lifecycle hook. The June 2026 binding.gyp worm keeps `package.json` `scripts` clean and hides execution in a ~100-byte `binding.gyp` that abuses shell expansion in the `sources` array:

```json
// [P0] binding.gyp worm — node-gyp runs arbitrary shell during "compile"
{
  "targets": [{
    "target_name": "Setup",
    "type": "none",
    "sources": ["< $(node index.js >/dev/null) >/dev/null 2>&1 && echo stub.c)"]
  }]
}
```

That silently runs a root-level `index.js` (4.5–4.9 MB obfuscated in known campaigns) during `npm install`. Flag any `binding.gyp` in a package with no legitimate native code, any `sources` entry with `$()`, backticks, or shell redirection, and any `type: "none"` target whose only job is to trigger a command.

Legitimate install scripts exist: `node-gyp`, `esbuild`, `sharp`, `bcrypt`, `playwright` compile or download a **platform binary into the package's own directory**. Distinguish that from a script that:

- makes network calls to **non-registry hosts**,
- reads environment variables, `~/.npmrc`, SSH keys, or cloud credentials,
- writes **outside** the package directory (shell rc files, `~`, system paths),
- spawns a shell, or invokes a local **AI CLI** (`claude`, `gemini`, `q`) to hunt for secrets (the nx `s1ngularity` technique), or
- installs an **alternate runtime** (Bun) to execute a payload outside Node's monitored process.

```json
// [P0] Shai-Hulud-class install hook — preinstall runs a dropped payload before review
{
  "name": "innocent-looking-util",
  "version": "1.2.4",
  "scripts": { "preinstall": "node setup_bun.js" }
}
```

The files `setup_bun.js` + `bun_environment.js` (Shai-Hulud 2.0/3.0), `telemetry.js` (s1ngularity), a malicious **`binding.gyp`** + root **`index.js`** (binding.gyp worm), or any install path that installs Bun to run an obfuscated blob are **P0 on sight** — treat the package as compromised, do not install, and rotate any credentials already exposed. See the campaign markers in `references/checklist.md`.

### Pass 3: obfuscation and dynamic code

Obfuscation in a dependency that has no reason to obfuscate **is itself the finding**. Flag:

- a large single minified/encoded blob in a package whose stated job is small;
- hex / base64 / XOR string arrays, `eval(...)`, `new Function(...)`, `vm.runInThisContext`, `atob()` piped into `eval`;
- **decode-then-execute** and **fetch-then-execute**: code pulled from a URL and run (`require()` of a downloaded file, `child_process` running a fetched script) — the staged-payload pattern that lets the attacker change the malware without republishing.

You don't have to fully deobfuscate it. A styling or date library that ships an encrypted payload and an `eval` is suspicious enough to block on.

### Pass 4: credential and secret access

Malicious packages harvest everything reachable from the install or runtime context. Flag reads of:

- `process.env` enumerated and sent off-box; `~/.npmrc` (npm token), `~/.aws/credentials`, SSH keys, `.env`, `gh auth token`;
- the cloud **instance metadata service** `169.254.169.254` (AWS/GCP/Azure IMDS) and container creds (`AWS_CONTAINER_CREDENTIALS_FULL_URI`, ECS task tokens), Vault (`VAULT_ADDR`/`VAULT_TOKEN`);
- cloud secret managers (AWS Secrets Manager, Azure Key Vault, GCP Secret Manager);
- a download or invocation of **TruffleHog** to actively scan the filesystem for secrets (a Shai-Hulud hallmark).

### Pass 5: exfiltration, C2, and self-propagation

Where harvested data goes, and how one compromised dependency becomes the next:

- **Exfiltration** to non-registry destinations: HTTP(S) POST to a hardcoded host/IP, DNS tunneling, Discord/Telegram/Slack webhooks, or **creating a public GitHub repo as a dead-drop** (Shai-Hulud's `Sha1-Hulud: The Second Coming.` repos; s1ngularity's `s1ngularity-repository-*`).
- **Self-propagation (worm).** The package reads its own file, validates an npm token (`/-/whoami`), enumerates the maintainer's other packages (`/-/v1/search?text=maintainer:...`), and runs `npm publish` to backdoor them. This is what turned one bad commit into ~800 compromised packages. Any dependency that contains its own re-publishing logic is **P0**.

### Pass 6: persistence and sabotage

- **Persistence** beyond the install: edits to `~/.bashrc` / `~/.zshrc`, a registered **self-hosted GitHub Actions runner** (named `SHA1HULUD`) plus a rogue workflow (`discussion.yaml`) for remote command execution, **injected GitHub Actions workflow steps** (`setup-bun` + payload execution — the binding.gyp worm's CI persistence), cron, or systemd units.
- **Destructive failsafe.** Shai-Hulud 2.0 attempts to **wipe the user's home directory** (`shred`, `rm -rf $HOME`, `del /F /Q /S`) if it can neither exfiltrate nor propagate. Flag any dependency containing destructive filesystem or shutdown commands.
- **Protestware.** Sabotage gated on geography or date (e.g. `node-ipc` wiping files for certain locales). A dependency that branches on `process.env.LANG`, a country, or `Date` to do something harmful is a finding even if "only" targeting others.

### Pass 7: integrity and version hygiene

This pass reads the manifest and lockfile, and applies even when you can't see the package source. Flag:

- **Floating versions** — `^`, `~`, `*`, `latest`, or a `git`/`http(s)` tarball dependency. A range means "whatever the registry serves next," including a compromised patch. Pin exact versions.
- **No committed lockfile**, or a lockfile not enforced in CI. The lockfile pins the whole transitive tree with integrity hashes; `npm ci` / `--frozen-lockfile` refuses to mutate it. Without it, every install is a fresh roll of the dice.
- **A lockfile entry with a tarball URL but no `integrity` hash** — functionally `latest`, and the entry the registry can't verify. Audit for empty/missing `integrity` and off-registry `resolved` URLs.
- **Manifest ↔ lockfile drift**, a suspicious version jump (a long-stable package leaping versions), a brand-new or recently-published version (no cooldown), and **missing provenance** where the ecosystem supports it. The fixes — cooldown / `min-release-age`, `npm audit signatures`, OSV — are in the closing section and `references/patterns.md`.

## Finding format

Report each finding in this structure. Group by severity, P0 first.

```
[P0] malicious-install-script in package.json:14 (dependency: innocent-looking-util@1.2.4)
  Adds a `preinstall` hook running `node setup_bun.js`. This is the Shai-Hulud
  install-time worm pattern: the dropped payload installs the Bun runtime and runs
  an obfuscated credential stealer before any review, on every dev machine and CI
  runner that installs this package.

  Vulnerable:
    "scripts": { "preinstall": "node setup_bun.js" }

  Fix: do not install. Remove the dependency, delete node_modules and the lockfile
  entry, clear the npm cache, and rotate every credential reachable from machines
  that already installed it (npm, GitHub, cloud, SSH). Confirm against the published
  IOC lists before trusting any nearby version.
```

If the user pastes a manifest or snippet without a path, refer to "the manifest" / "the package" and use line numbers within the snippet. Always name the **package and version**, the **pass** that fired, and **where the install or runtime context exposes secrets** — that is the proof the dependency is dangerous and the spec for the fix.

## Severity scale

- **P0** — confirmed malicious behavior reachable now: an install script that harvests and exfiltrates, a known-compromised version (campaign IOC match), worm self-propagation, fetch-then-execute of remote code, or a destructive payload. Do not install; rip it out and rotate exposed credentials.
- **P1** — high-risk and unvetted: an unexplained install script doing network/filesystem/obfuscated work, a typosquat / slopsquat / dependency-confusion candidate of a real dependency, an unscoped internal-looking name resolvable from a public registry, or a brand-new low-reputation package pulled into a sensitive path. Block merge until confirmed.
- **P2** — hygiene gaps that widen blast radius: floating version ranges, a missing or unenforced lockfile, lockfile entries without integrity hashes, no cooldown, install scripts not disabled in CI, no provenance verification. Fix in the normal review cycle.
- **P3** — defense-in-depth: no SBOM, no OpenSSF Scorecard signal, no build-script allowlist, missing dependency-review automation on PRs.

## When the dependencies look fine

After all passes, if nothing fires:

1. Say so explicitly, and state what you verified: the ecosystem and files from Pass 0, the added/changed packages reviewed, that no install scripts (or only benign platform-build ones) are present, no obfuscation or credential/exfiltration patterns in the source you could see, and that versions are pinned with a committed, integrity-bearing lockfile.
2. Note what a static read **cannot** confirm: the **published tarball may differ from the source repo** (the registry is the trust boundary, not GitHub); **transitive dependencies** you didn't open; **runtime-only** behavior; whether the version on the registry *right now* matches what you reviewed; and reputation, age, and provenance, which need a registry/OSV query you didn't run.
3. Recommend the confirming commands (the user runs these against public data — the skill itself stays offline): `npm audit signatures` (provenance), `osv-scanner --lockfile=...` (known-malicious/CVE), for a JS/TS project `cve-lite-cli` (the OWASP local-first lockfile scanner — OSV matching across npm/pnpm/yarn/bun with direct-vs-transitive visibility, copy-and-run `--fix` remediation, and an `--offline` advisory DB; matches *known-advisory* vulns, so it complements rather than replaces the behavioral passes above), `npm view <pkg> time` (recency, for a cooldown decision), and a Socket/Snyk/Aikido behavioral check. Plus a **cooldown** (`min-release-age` / `minimumReleaseAge`, 1–7 days) so a freshly published compromise gets caught by the community before it lands. Walk `references/checklist.md` for a full audit.

A clean static read does not prove the installed artifact is safe.

## Reference files

- `references/ecosystems.md` — per-ecosystem facts you need to judge a dependency: where install hooks live, how to pin and lock, the integrity/hash mechanism, namespace/scoping support (so you can call dependency-confusion exposure), the provenance mechanism, and the exact offline-and-registry verification commands — for npm/pnpm/yarn, PyPI, Go, Cargo, RubyGems, Maven/Gradle, NuGet, and Composer.
- `references/patterns.md` — "I want to add or update a dependency safely" recipes: cooldown windows, lockfile + `npm ci`, `ignore-scripts` with an allowlist, scoped names + registry pinning against dependency confusion, provenance/Trusted-Publisher verification, exact pinning, and isolating CI secrets from install scripts. Read it when proposing the fix.
- `references/checklist.md` — a flat per-dependency / per-PR-diff / per-repo / per-org checklist with a triage order, plus an appendix of **known-campaign markers** (Shai-Hulud 1/2/3, nx `s1ngularity`, the binding.gyp worm, the `chalk`/`debug` compromise). Use it for a full audit, for scanning many dependencies at once, and to match concrete IOCs.

## What this skill won't do

- It won't install, run, or otherwise execute the package (even with `--ignore-scripts`). It reads manifests, lockfiles, and any source already on disk. For runtime confirmation, pair it with a sandboxed install and behavioral monitoring (Socket, Datadog SCFW, a network-isolated container) — the dynamic complement to this static review.
- It won't silently phone home. Live reputation, recency, and provenance need a registry/OSV query; this skill hands you the exact commands to run yourself rather than shipping your dependency list anywhere.
- It won't replace a continuous SCA pipeline (OSV-Scanner, Snyk, Socket, Dependabot/Renovate with cooldown). It is the pre-install read that catches what a manifest-only scanner misses — an install script's *intent* — and the gate when you're about to add code from someone you've never met.
- It won't wave a package through because it's popular or has millions of downloads. Popular packages get compromised; that is the entire threat model. An unexplained install script in `left-pad` is more dangerous than one in a package nobody uses.
