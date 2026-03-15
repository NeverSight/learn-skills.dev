---
name: setup-renovate-for-tuist
description: Sets up Renovate automated dependency updates for Tuist iOS projects. Detects integration style (Project.swift-based or Tuist/Package.swift-based), handles registry vs URL packages, and creates renovate.json plus an optional GitHub Actions workflow. Use when you want to automate dependency bump PRs for a Tuist project.
---

# Setup Renovate for Tuist

Renovate automates dependency update PRs for your Tuist iOS project. This skill creates the correct `renovate.json` based on your project's integration style and package format.

## Preflight Checklist

Before starting:
- [ ] Confirm the project uses Tuist (look for `Tuist.swift` or `Tuist/` directory)
- [ ] Identify the integration style (see below)
- [ ] Check whether Tuist registry is enabled
- [ ] Confirm the project is hosted on GitHub (Renovate GitHub App or self-hosted)

## Step 1 — Detect Integration Style

Check where packages are declared:

**Tuist/Package.swift-based** — look for non-empty `dependencies` array:
```swift
// Tuist/Package.swift
let package = Package(
    dependencies: [
        .package(url: "https://github.com/firebase/firebase-ios-sdk", from: "11.8.1")
    ]
)
```

**Project.swift-based** — search for `Project.swift` files anywhere in the project that contain a non-empty `packages:` array:

```bash
grep -rl "packages:" --include="Project.swift" .
```

```swift
// (location varies per project)
let project = Project(
    packages: [
        .remote(url: "https://github.com/firebase/firebase-ios-sdk", requirement: .upToNextMajor(from: "11.8.1"))
    ]
)
```

> A project uses one style only. If `Tuist/Package.swift` has non-empty dependencies → Tuist/Package.swift-based. If any `Project.swift` file has a non-empty `packages:` array → Project.swift-based.

## Step 2 — Detect Package Format

Within the detected files, check whether packages use **URL format** or **registry format**:

| Format | Example |
|--------|---------|
| URL-based | `.package(url: "https://github.com/firebase/firebase-ios-sdk", from: "11.8.1")` |
| Registry-based | `.package(id: "firebase.firebase-ios-sdk", from: "11.8.1")` |
| URL-based (Project.swift) | `.remote(url: "https://github.com/...", requirement: .upToNextMajor(from: "1.0.0"))` |

Also note any packages using `requirement: .branch("...")` — these cannot be tracked by Renovate and should be left out (see Branch Dependencies below).

## Step 3 — Check for mise.toml

Check if `mise.toml` exists in the project root. If yes, Renovate can also update tool versions (tuist, swiftlint, etc.) automatically.

## Step 4 — Ask for Schedule Preference

Ask the user: *"When would you like Renovate to check for updates? (e.g. 'every Monday morning', 'weekly on Friday', 'daily')"*

Use the answer to set the `schedule` field in `renovate.json`. Renovate uses natural language scheduling:

| User preference | Renovate schedule value |
|----------------|------------------------|
| Monday morning | `"before 9am on monday"` |
| Friday afternoon | `"after 2pm on friday"` |
| Weekly (any) | `"once a week"` |
| Daily | `"every day"` |

Full syntax reference: https://docs.renovatebot.com/configuration-options/#schedule

If using a self-hosted GitHub Actions workflow, also convert the chosen schedule to a matching cron expression.

## Step 5 — Create renovate.json

Create `renovate.json` in the project root based on the detected configuration.

---

### Case A: Tuist/Package.swift + URL-based packages (most common)

The Renovate Swift manager natively handles `Package.swift` files. The default pattern `/(^|/)Package\.swift/` already matches `Tuist/Package.swift`.

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended"],
  "packageRules": [
    {
      "matchManagers": ["swift"],
      "groupName": "Swift dependencies",
      "schedule": ["<schedule>"]
    }
  ]
}
```

---

### Case B: Tuist/Package.swift + Registry-based packages (id: format)

Renovate's Swift manager only understands `url:`-based packages. For `id:`-based registry packages, use `customManagers` with a regex that:
- Handles both `from:` and `exact:` requirements
- Matches multiline declarations (packages formatted across multiple lines will be silently missed otherwise)
- Transforms dot notation to slash notation for GitHub lookups (`firebase.firebase-ios-sdk` → `firebase/firebase-ios-sdk`)
- Uses triple braces `{{{ }}}` in `packageNameTemplate` to prevent HTML-escaping the `/`

Use two managers (releases + tags) as fallback since some packages only publish tags, not releases:

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended"],
  "enabledManagers": ["custom.regex"],
  "customManagers": [
    {
      "customType": "regex",
      "managerFilePatterns": ["/Tuist/Package\\.swift/"],
      "matchStrings": [
        "\\.package\\(id:\\s*\"(?<depName>[\\w\\-.]+?)\"[\\s\\S]*?(?:from|exact):\\s*\"(?<currentValue>[^\"]+)\"\\)"
      ],
      "datasourceTemplate": "github-releases",
      "packageNameTemplate": "{{{replace '\\.' '/' depName}}}"
    },
    {
      "customType": "regex",
      "managerFilePatterns": ["/Tuist/Package\\.swift/"],
      "matchStrings": [
        "\\.package\\(id:\\s*\"(?<depName>[\\w\\-.]+?)\"[\\s\\S]*?(?:from|exact):\\s*\"(?<currentValue>[^\"]+)\"\\)"
      ],
      "datasourceTemplate": "github-tags",
      "packageNameTemplate": "{{{replace '\\.' '/' depName}}}"
    }
  ],
  "packageRules": [
    {
      "matchManagers": ["custom.regex"],
      "groupName": "Swift dependencies",
      "schedule": ["<schedule>"]
    }
  ]
}
```

> **Note on dotted repo names**: If a repo name had dots replaced with underscores (e.g., `groue.GRDB_swift`), the `packageNameTemplate` replacement `groue/GRDB_swift` won't match the real GitHub repo `groue/GRDB.swift`. For these packages, add an explicit `packageRules` override:
> ```json
> {
>   "matchPackageNames": ["groue.GRDB_swift"],
>   "packageName": "groue/GRDB.swift"
> }
> ```

---

### Case C: Project.swift-based + URL-based packages

Project.swift uses `.remote(url:)` which is a Tuist-specific syntax, not standard SPM. Renovate's Swift manager won't parse this. The regex must:
- Handle multiline declarations
- Handle optional `https://` prefix and `.git` suffix
- Cover all requirement types: `.upToNextMajor`, `.upToNextMinor`, `.exact`

Use two managers (releases + tags) as fallback:

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended"],
  "enabledManagers": ["custom.regex"],
  "customManagers": [
    {
      "customType": "regex",
      "managerFilePatterns": ["/(^|/)Project\\.swift$/"],
      "matchStrings": [
        "\\.remote\\(url:\\s*\"(?:https?:\\/\\/)?github\\.com\\/(?<depName>[\\w\\-_]+\\/[\\w\\-_.]+?)(?:\\.git)?\"[\\s,]*requirement:\\s*\\.(?:upToNextMajor|upToNextMinor)\\(from:\\s*\"(?<currentValue>[^\"]+)\"\\)"
      ],
      "datasourceTemplate": "github-releases"
    },
    {
      "customType": "regex",
      "managerFilePatterns": ["/(^|/)Project\\.swift$/"],
      "matchStrings": [
        "\\.remote\\(url:\\s*\"(?:https?:\\/\\/)?github\\.com\\/(?<depName>[\\w\\-_]+\\/[\\w\\-_.]+?)(?:\\.git)?\"[\\s,]*requirement:\\s*\\.(?:upToNextMajor|upToNextMinor)\\(from:\\s*\"(?<currentValue>[^\"]+)\"\\)"
      ],
      "datasourceTemplate": "github-tags"
    },
    {
      "customType": "regex",
      "managerFilePatterns": ["/(^|/)Project\\.swift$/"],
      "matchStrings": [
        "\\.remote\\(url:\\s*\"(?:https?:\\/\\/)?github\\.com\\/(?<depName>[\\w\\-_]+\\/[\\w\\-_.]+?)(?:\\.git)?\"[\\s,]*requirement:\\s*\\.exact\\(\"(?<currentValue>[^\"]+)\"\\)"
      ],
      "datasourceTemplate": "github-releases"
    },
    {
      "customType": "regex",
      "managerFilePatterns": ["/(^|/)Project\\.swift$/"],
      "matchStrings": [
        "\\.remote\\(url:\\s*\"(?:https?:\\/\\/)?github\\.com\\/(?<depName>[\\w\\-_]+\\/[\\w\\-_.]+?)(?:\\.git)?\"[\\s,]*requirement:\\s*\\.exact\\(\"(?<currentValue>[^\"]+)\"\\)"
      ],
      "datasourceTemplate": "github-tags"
    }
  ],
  "packageRules": [
    {
      "matchManagers": ["custom.regex"],
      "groupName": "Swift dependencies",
      "schedule": ["<schedule>"]
    }
  ]
}
```

---

### Case D: Mixed (URL + registry packages)

Combine the `customManagers` entries from Case B and Case C. Set `enabledManagers` to include only the managers you use:

```json
{
  "enabledManagers": ["custom.regex"]
}
```

---

### Branch Dependencies

Packages declared with `requirement: .branch("...")` use mutable Git refs — there is no semantic version for Renovate to track. Do not add regex patterns for these. If Renovate picks them up accidentally, disable them explicitly:

```json
{
  "matchDatasources": ["git-refs"],
  "enabled": false
}
```

---

### Adding mise.toml support (optional)

If `mise.toml` exists, add `mise` to `enabledManagers`:

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended"],
  "enabledManagers": ["mise", "custom.regex"],
  "packageRules": [
    {
      "matchManagers": ["mise"],
      "groupName": "Dev tools",
      "schedule": ["<schedule>"]
    }
  ]
}
```

> The `mise` manager reads `mise.toml` and updates tool versions like `tuist`, `swiftlint`, etc.

---

### Recommended packageRules additions (optional)

Consider adding these to control merge behaviour:

```json
{
  "packageRules": [
    {
      "matchUpdateTypes": ["patch"],
      "automerge": true,
      "automergeType": "branch"
    },
    {
      "matchUpdateTypes": ["minor"],
      "automerge": false
    },
    {
      "matchUpdateTypes": ["major"],
      "automerge": false
    }
  ]
}
```

And these top-level options to prevent PR floods:

```json
{
  "prConcurrentLimit": 3,
  "prHourlyLimit": 2
}
```

## Step 6 — Dry-run Verification

Run a local dry-run to confirm the `renovate.json` detects the expected packages before merging.

**Check if Renovate is installed:**

```bash
renovate --version
```

- If installed → proceed to run the dry-run below.
- If not installed → ask the user: *"Renovate is not installed. Can I install it with `npm install -g renovate`?"* Only install if the user confirms.

**Run the dry-run:**

```bash
RENOVATE_GITHUB_TOKEN=<github-pat> renovate --dry-run=full <org>/<repo>
```

A GitHub PAT with `repo` scope is required. Ask the user to provide it if not already available in the environment.

**What to check in the output:**
- Each expected package appears as a detected dependency with its current version
- No `matched 0 files` warnings for your `managerFilePatterns`
- Registry packages show the correct transformed `depName` (e.g. `firebase/firebase-ios-sdk`, not `firebase.firebase-ios-sdk`)

**If a package is missing:**
- Paste the actual Swift declaration (including surrounding lines) into [regex101.com](https://regex101.com) using the JavaScript flavor
- Test the failing `matchStrings` pattern directly
- Common culprits: multiline declaration not matched by `[\s\S]*?`, unhandled requirement type (e.g. `.upToNextMinor`, `.exact`)

## Step 7 — Enable Renovate

Choose one of the two approaches:

### Option A: Renovate GitHub App (recommended)

1. Install the [Renovate GitHub App](https://github.com/apps/renovate) on the repository.
2. Merge the `renovate.json` — Renovate will auto-create an onboarding PR, then begin raising dependency update PRs.

No additional files needed.

### Option B: Self-hosted via GitHub Actions

**1. Check for an existing Renovate workflow:**

```bash
ls .github/workflows/
```

Search for any workflow file that already references Renovate:

```bash
grep -rl "renovate" .github/workflows/
```

- **If a Renovate workflow already exists** — show its contents to the user and ask whether to update the schedule/token or leave it as-is. Do not create a new file.
- **If no Renovate workflow exists** — before creating the file, check the latest release tag of `renovatebot/github-action`:

```bash
gh release list --repo renovatebot/github-action --limit 1
```

Use the major version from that tag (e.g. if latest is `v40.3.2`, use `renovatebot/github-action@v40.3.2`). Do not use a bare major tag like `@v40` as it may not exist.

Then create `.github/workflows/renovate.yml`:

```yaml
name: Renovate

on:
  # Disabled until tested — uncomment after confirming the workflow runs correctly
  # schedule:
  #   - cron: '<cron expression matching chosen schedule>'
  workflow_dispatch:

permissions:
  contents: write
  pull-requests: write

jobs:
  renovate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: renovatebot/github-action@<latest-version>
        with:
          configurationFile: renovate.json
          token: ${{ secrets.RENOVATE_GITHUB_TOKEN }}
        env:
          LOG_LEVEL: 'debug'
          RENOVATE_REPOSITORIES: ${{ github.repository }}
```

**2.** The `schedule` cron is commented out so the user can test manually first. After the workflow file is merged, ask the user to trigger it manually from the Actions tab (`workflow_dispatch`) and confirm it runs correctly.

Once the user confirms it works, uncomment the `schedule` block and push the change.

**3.** Set `RENOVATE_GITHUB_TOKEN` in GitHub repository secrets. Ask the user which token type they are using:

**Fine-grained personal access token** — requires these permissions (set token lifetime to ≤ 366 days — some organizations such as `tuist` enforce this limit and will reject tokens with longer lifetimes):
- Administration: Read-only
- Contents: Read and write
- Dependabot alerts: Read-only
- Issues: Read and write
- Metadata: Read-only (auto-granted)
- Pull requests: Read and write

**Classic personal access token** — requires:
- `repo` (full read/write)

> For additional self-hosted configuration options (autodiscover, git author, PR limits, etc.), refer to the [Renovate self-hosted configuration docs](https://docs.renovatebot.com/self-hosted-configuration/). Ask the user if they need any of these before finalising the workflow.

## Step 8 — Verify

After merging:
- Renovate creates a **Configure Renovate** PR (if using GitHub App) — merge it
- Renovate opens PRs for outdated packages on the configured schedule
- Check `https://app.renovatebot.com/dashboard` for run logs

## Common Issues

| Issue | Fix |
|-------|-----|
| No PRs created | Confirm `renovate.json` is valid JSON; check app dashboard for errors |
| `customManagers` not matching | Test the regex against your actual Swift file at regex101.com (use JavaScript flavor) |
| Multiline declarations not detected | Ensure `[\\s\\S]*?` is used instead of `.+?` in `matchStrings` |
| Wrong package gets updated (e.g. LSExtensions bumped with kakao's version) | `[\\s\\S]*?` is spanning across multiple `.remote()` blocks — use `[\\s,]*` between the URL and `requirement:` to constrain the match within a single block |
| Registry package PRs have wrong version | Override `packageName` in `packageRules` to point to the correct GitHub repo |
| Renovate opens too many PRs at once | Add `"prConcurrentLimit": 3` to `renovate.json` |
| Package updates break build | Add `"automerge": false` (it's the default — confirm it's not set to `true`) |
| Renovate scan is very slow | Add `"enabledManagers": ["custom.regex"]` to skip irrelevant built-in managers |
| `Datasource unknown error` for `tuist/tuist` with fine-grained PAT | The `tuist` org forbids fine-grained PATs with lifetime > 366 days — shorten the token expiry or switch to a classic PAT with `repo` scope |

## Done Checklist

- [ ] `renovate.json` created in project root with correct config for detected style
- [ ] JSON is valid (no syntax errors)
- [ ] `customManagers` regex tested against actual Swift file content (including multiline examples)
- [ ] Branch dependencies excluded or disabled
- [ ] `renovate --dry-run` confirms all expected packages are detected
- [ ] Renovate GitHub App installed OR `.github/workflows/renovate.yml` created
- [ ] `RENOVATE_GITHUB_TOKEN` secret set (self-hosted only)
