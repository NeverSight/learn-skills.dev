---
name: fortify-cicd-integration
description: Integrate Fortify application security (SAST, SCA, DAST) with GitHub Actions, GitLab Pipelines, Azure DevOps, Jenkins & other CICD/DevSecOps pipelines.
license: MIT
metadata:
  version: "1.0.2"
  tested-with:
    fcli: "3.23"
---

# Fortify CI/CD Integration

## Step 1: Investigate the repository first

Before asking the user anything or generating output, inspect the repository to determine context automatically.

### Detect the CI/CD platform

Look for these platform-specific files (check root and common subdirectories):

| Path / file | Platform |
|---|---|
| `.github/workflows/*.yml` | GitHub Actions |
| `.gitlab-ci.yml` | GitLab CI |
| `azure-pipelines.yml` | Azure DevOps |
| `Jenkinsfile` | Jenkins |
| `bitbucket-pipelines.yml` | Bitbucket Pipelines → generic fcli ci |
| `.travis.yml` | Travis CI → generic fcli ci |
| `.circleci/config.yml` | CircleCI → generic fcli ci |
| `teamcity-settings.kts` or `.teamcity/` | TeamCity → generic fcli ci |
| `.buildkite/pipeline.yml` | Buildkite → generic fcli ci |
| `bamboo-specs/` | Bamboo → generic fcli ci |

If multiple are present, note all of them and generate for whichever the user's request implies (or ask if ambiguous).

If no known platform file is found, use the **generic fcli `ci` action approach** — see [references/generic-ci-ssc.md](references/generic-ci-ssc.md) for the SSC case or [references/generic-ci-fod.md](references/generic-ci-fod.md) for the FoD case.

### Detect the build tool and language

Check in this priority order:

1. **Existing CI/CD config files** — read the platform's existing workflow/pipeline files to find setup steps already in use. Extract the exact toolchain and version already specified — use these verbatim so the Fortify workflow matches the project's existing build environment.
2. **Build manifest files** — use the presence of files such as `requirements.txt`, `pom.xml`, `build.gradle`, `package.json`, `*.csproj`, `go.mod`, etc. to identify the language and build tooling required. Ensure the generated Fortify workflow includes any setup steps needed to successfully build the project with that toolchain. Refer to the platform-specific guidance file for the correct setup action/step syntax.

### Check for an existing Fortify configuration

Search for any existing Fortify-related files (`fortify.yml`, `fod.yaml`, files containing `fortify/github-action`, `fcli`, `FOD_`, `SSC_`) to understand whether Fortify is already partially configured and what credentials/variables are already referenced.

### Check for an active Fortify session

If you are still not sure whether the user wants to integra with FoD or SSC, check if there is an active fcli session for either platform.

```bash
fcli fod session ls --query "expired=='No'"
fcli ssc session ls --query "expired=='No'"
```

---

## Step 2: Clarify only what cannot be determined from explicit user input or repository inspection

After investigation, ask the user **only** for information that cannot be inferred from the repository or user prompt:

1. **Fortify platform:** Fortify on Demand (FoD) or Fortify SSC (self-hosted / on-prem / private cloud)?
2. **FoD region URL:** — Only relevant for FoD, not applicable to SSC. Options include:

| Region | URL |
|---|---|
| US (default) | `https://ams.fortify.com` |
| EMEA | `https://emea.fortify.com` |
| EU | `https://eu.fortify.com` |
| APAC | `https://apac.fortify.com` |
| SGP | `https://sgp.fortify.com` |

3. **Optional Features** — SCA (open source scanning) and Aviator (AI-assisted auditing) are enabled by default in the generated workflow. Policy checks (`DO_CHECK_POLICY`) and PR/MR comments (`DO_PR_COMMENT`) are disabled by default. Ask the user if they want to review and customize these optional features.

---

## Step 3: Confirm before generating

Before writing any workflow file, present a concise pre-generation summary and wait for the user to confirm:

```
CI/CD platform:      [e.g., GitHub Actions]
Fortify deployment:  [FoD / SSC]
Build toolchain:     [e.g., Maven 3.9 / Node.js 20 / .NET 8]
Existing Fortify config: [none / partially configured — describe]
Output file:         [e.g., .github/workflows/fortify.yml]
Scan types:          [SAST / SAST + SCA]
Optional features:   Aviator [on/off] · Policy check [on/off] · PR comments [on/off]
Auth method:         [FoD PAT / FoD API key / SSC token]
```

Then ask: **"Does this look right? Shall I generate the workflow?"**

Do NOT generate or write the workflow file until the user confirms. If any item above is still unknown after Step 1 and Step 2, resolve it before presenting this summary.

---

## General guidelines

- **Prefer the official Fortify managed action/plugin** for platforms that have one (GitHub Actions, GitLab CI, Azure DevOps, Jenkins).
- **Keep secrets in the platform's secret store**; hardcode or use variables only for non-sensitive configuration (e.g., Fortify server URL). After generating the workflow, remind the user to configure the required secrets in their platform's secret management UI.
- **FOD_URL / SSC_URL must never be placed in secrets** — these are non-sensitive endpoints. Store as a repository/pipeline variable or hardcode directly.
- **Default to FoD PAT authentication** unless they explicitly request to use API client credentials (or API key). Only include user/password or Client Credentials, never use both.
- **Pin action/plugin versions** to major version tags (e.g., `@v3`) for a balance of stability and automatic patch updates.
- **Never invent optional features, configuration settings or attributes** Always refer to the official documentation for the platform's Fortify action/plugin to ensure all inputs are valid and up-to-date. If documentation is unclear, default to the most basic configuration that will work and flag any uncertainties to the user.

---

## Platform-specific references

Load the appropriate reference file for the detected platform and Fortify deployment before generating any workflow content. These reference files contain the exact environment variables, configuration options, and best practices for that specific integration.

| Platform | Fortify Deployment | Reference |
|---|---|---|
| GitHub Actions | FoD | `references/github-fod.md` |
| GitHub Actions | SSC | `references/github-ssc.md` |
| GitLab CI | FoD | `references/gitlab-fod.md` |
| GitLab CI | SSC | `references/gitlab-ssc.md` |
| Azure DevOps | FoD or SSC | `references/azure-devops.md` |
| Jenkins | FoD or SSC | `references/jenkins.md` |

For any other platform (Bitbucket Pipelines, Travis CI, CircleCI, TeamCity, Buildkite, Bamboo, etc.) should load:
- FoD: `references/generic-ci-fod.md` 
- SSC: `references/generic-ci-ssc.md`

---

## Post-generation checklist

After delivering the workflow file, confirm with the user:

- [ ] Secrets added to the platform secret store (`FOD_TENANT`, `FOD_USER`, `FOD_PAT` for FoD PAT auth; `FOD_CLIENT_ID`, `FOD_CLIENT_SECRET` for FoD API key auth; or `SSC_TOKEN`, `SC_SAST_TOKEN` for SSC)
- [ ] `FOD_URL` / `SSC_URL` configured as a repository/pipeline variable (not secret)
- [ ] Branch names in trigger conditions match the actual repository (verify these were pulled from existing workflows — if placeholders remain, flag them to the user)
