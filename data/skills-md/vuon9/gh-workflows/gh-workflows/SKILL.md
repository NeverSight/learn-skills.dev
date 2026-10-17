---
name: gh-workflows
description: Build, evaluate, document, and open pull requests for reusable GitHub Actions workflows in this gh-workflows repository. Use when adding or changing a reusable workflow, its Go tooling, or its docs.
---

# gh-workflows

Reusable GitHub Actions workflows and the Go tooling that powers them live in this repo. Product repos stay thin: they hold only a caller wrapper plus app-specific config, while shared behavior stays here.

## Where things live

- Reusable workflow YAML: `.github/workflows/*.yml` (GitHub requires that exact path).
- CLI tooling: domain-scoped Go folders such as `ios/testflight/` and `mac/`. Put non-trivial behavior in Go with unit tests, not long shell scripts or big inline YAML blocks.
- Docs: `README.md`, one section per workflow. This is the human-facing contract.

## Build

### 1. Design the contract with `workflow_call`

Every reusable workflow exposes explicit inputs and secrets. Prefer documented inputs over hidden repository assumptions. App-specific values come in as inputs or caller-repo secrets; never hardcode a project, customer, or private name.

```yaml
on:
  workflow_call:
    inputs:
      dry-run:
        type: boolean
        default: true
    secrets:
      APP_SECRET:
        required: false
```

### 2. Check out the workflow repo at the calling commit

The job runs in the caller repo, not the workflow repo. Check out your own tooling at the exact SHA that triggered the run so the caller gets the tested version:

```yaml
- name: Check out workflow tools
  uses: actions/checkout@v6
  with:
    repository: ${{ job.workflow_repository }}
    ref: ${{ job.workflow_sha }}
    path: gh-workflows
```

Then `go build` the CLI from that checkout into `$RUNNER_TEMP` and invoke it.

### 3. Gotchas that break CI

- `permissions` MUST live on the caller job, never on the reusable `workflow_call` job. A `permissions` block inside the reusable job causes `startup_failure`.
- `if:` is not allowed on a caller job that `uses:` a reusable workflow. Gate behavior inside the reusable workflow via an input (for example a `mode` input) instead.
- Cross-repo access needs a dedicated token. The caller `GITHUB_TOKEN` cannot write to a different repo (for example a `homebrew-tap`), so require a fine-grained token as a secret (`TAP_REPO_TOKEN`).
- Pin callers to a tag or major version, not `main`. Publishing a breaking contract change means a new major tag and updated docs.

### 4. Caller wrapper

```yaml
jobs:
  release:
    uses: vuon9/gh-workflows/.github/workflows/release.yml@v1
    with:
      dry-run: true
    secrets: inherit
```

## Evaluate locally

Run before claiming anything works:

```bash
go test ./...
go build ./ios/testflight/cmd/ios-testflight
go build ./mac/cmd/macos-release
```

`act` only checks workflow wiring (YAML and trigger shape). It does NOT prove hosted-runner images, macOS signing, Xcode behavior, or external uploads.

```bash
act --validate -W .github/workflows/release.yml
act --dryrun -W .github/workflows/release.yml
```

For real validation, dry-run from a caller app repo (not this repo) before removing legacy scripts. Treat `act` as insufficient for signing, notarization, or TestFlight.

## Document

Keep the main `README.md` a short index: each workflow gets a one-line purpose plus a link to its own doc. Write the detailed contract in a per-workflow domain folder (`homebrew/README.md`, `ai-code-review/README.md`, `mac/README.md`, `ios/testflight/README.md`).

Each workflow doc covers:

- A thin caller example.
- Required caller secrets and why each is required.
- Optional secrets.
- Useful inputs with defaults.
- What the workflow does (the steps).
- Recommended caller controls (tag namespaces, manual first run, final Gatekeeper verification).

Keep every example public-safe: no certificates, provisioning profiles, API keys, private project names, or real credentials.

## Open a pull request

Use the org branch prefix convention (`feat/`, `fix/`, `refactor/`). Fill the PR description from the template in `.github/pull_request_template.md`:

- Lead with a concise **Summary** (always a real paragraph).
- List **Changes** (workflow, Go tool, docs).
- **Local verification**: check the exact commands you ran, and confirm each passed.
- State the **Docs** section added or updated.
- Note the **Versioning** impact (tag bump or major-version rationale), or `N/A`.
- Leave **Screenshots** as `N/A` unless there is a UI-visible change.

Only claim success in the PR after the verification commands actually pass.
