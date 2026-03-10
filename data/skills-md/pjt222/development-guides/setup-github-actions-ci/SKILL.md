---
name: setup-github-actions-ci
description: >
  Configure GitHub Actions CI/CD for R packages including R CMD check
  on multiple platforms, test coverage reporting, and pkgdown site
  deployment. Uses r-lib/actions for standard workflows. Use when setting
  up CI/CD for a new R package, adding multi-platform testing to an
  existing package, configuring automated pkgdown site deployment,
  or adding code coverage reporting to a repository.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: r-packages
  complexity: intermediate
  language: R
  tags: r, github-actions, ci-cd, testing, automation
---

# Set Up GitHub Actions CI for R Packages

Configure automated R CMD check, test coverage, and documentation deployment via GitHub Actions.

## When to Use

- Setting up CI/CD for a new R package on GitHub
- Adding multi-platform testing to an existing package
- Configuring automated pkgdown site deployment
- Adding code coverage reporting

## Inputs

- **Required**: R package with valid DESCRIPTION and tests
- **Required**: GitHub repository (public or private)
- **Optional**: Whether to include pkgdown deployment (default: no)
- **Optional**: Whether to include coverage reporting (default: no)

## Procedure

### Step 1: Create R CMD Check Workflow

Create `.github/workflows/R-CMD-check.yaml`:

```yaml
on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

name: R-CMD-check

permissions: read-all

jobs:
  R-CMD-check:
    runs-on: ${{ matrix.config.os }}

    name: ${{ matrix.config.os }} (${{ matrix.config.r }})

    strategy:
      fail-fast: false
      matrix:
        config:
          - {os: macos-latest, r: 'release'}
          - {os: windows-latest, r: 'release'}
          - {os: ubuntu-latest, r: 'devel', http-user-agent: 'release'}
          - {os: ubuntu-latest, r: 'release'}
          - {os: ubuntu-latest, r: 'oldrel-1'}

    env:
      GITHUB_PAT: ${{ secrets.GITHUB_TOKEN }}
      R_KEEP_PKG_SOURCE: yes

    steps:
      - uses: actions/checkout@v4

      - uses: r-lib/actions/setup-pandoc@v2

      - uses: r-lib/actions/setup-r@v2
        with:
          r-version: ${{ matrix.config.r }}
          http-user-agent: ${{ matrix.config.http-user-agent }}
          use-public-rspm: true

      - uses: r-lib/actions/setup-r-dependencies@v2
        with:
          extra-packages: any::rcmdcheck
          needs: check

      - uses: r-lib/actions/check-r-package@v2
        with:
          upload-snapshots: true
          build_args: 'c("--no-manual", "--compact-vignettes=gs+qpdf")'
```

**Expected:** Workflow file `.github/workflows/R-CMD-check.yaml` created with a multi-platform matrix (macOS, Windows, Ubuntu) covering release, devel, and oldrel.

**On failure:** If the `.github/workflows/` directory does not exist, create it with `mkdir -p .github/workflows`. Verify YAML syntax with a YAML linter.

### Step 2: Create Test Coverage Workflow (Optional)

Create `.github/workflows/test-coverage.yaml`:

```yaml
on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

name: test-coverage

permissions: read-all

jobs:
  test-coverage:
    runs-on: ubuntu-latest

    env:
      GITHUB_PAT: ${{ secrets.GITHUB_TOKEN }}

    steps:
      - uses: actions/checkout@v4

      - uses: r-lib/actions/setup-r@v2
        with:
          use-public-rspm: true

      - uses: r-lib/actions/setup-r-dependencies@v2
        with:
          extra-packages: any::covr, any::xml2
          needs: coverage

      - name: Test coverage
        run: |
          cov <- covr::package_coverage(
            quiet = FALSE,
            clean = FALSE,
            install_path = file.path(normalizePath(Sys.getenv("RUNNER_TEMP"), winslash = "/"), "package")
          )
          covr::to_cobertura(cov)
        shell: Rscript {0}

      - uses: codecov/codecov-action@v4
        with:
          fail_ci_if_error: ${{ github.event_name != 'pull_request' && true || false }}
          file: ./cobertura.xml
          plugin: noop
          token: ${{ secrets.CODECOV_TOKEN }}
```

**Expected:** Workflow file `.github/workflows/test-coverage.yaml` created. Coverage reports will be uploaded to Codecov on each push and PR.

**On failure:** If Codecov upload fails, verify the `CODECOV_TOKEN` secret is set in the repository settings. For public repos, the token may be optional.

### Step 3: Create pkgdown Deployment Workflow (Optional)

Create `.github/workflows/pkgdown.yaml`:

```yaml
on:
  push:
    branches: [main, master]
  release:
    types: [published]
  workflow_dispatch:

name: pkgdown

permissions:
  contents: write
  pages: write

jobs:
  pkgdown:
    runs-on: ubuntu-latest

    env:
      GITHUB_PAT: ${{ secrets.GITHUB_TOKEN }}

    steps:
      - uses: actions/checkout@v4

      - uses: r-lib/actions/setup-pandoc@v2

      - uses: r-lib/actions/setup-r@v2
        with:
          use-public-rspm: true

      - uses: r-lib/actions/setup-r-dependencies@v2
        with:
          extra-packages: any::pkgdown, local::.
          needs: website

      - name: Build site
        run: pkgdown::build_site_github_pages(new_process = FALSE, install = FALSE)
        shell: Rscript {0}

      - name: Deploy to GitHub pages
        if: github.event_name != 'pull_request'
        uses: JamesIves/github-pages-deploy-action@v4
        with:
          clean: false
          branch: gh-pages
          folder: docs
```

**Expected:** Workflow file `.github/workflows/pkgdown.yaml` created. Site builds and deploys to `gh-pages` branch on push to main or release.

**On failure:** If deployment fails, ensure the repository has `contents: write` permissions enabled. Verify `_pkgdown.yml` has `development: mode: release` set.

### Step 4: Add Status Badge to README

Add to `README.md`:

```markdown
[![R-CMD-check](https://github.com/USERNAME/REPO/actions/workflows/R-CMD-check.yaml/badge.svg)](https://github.com/USERNAME/REPO/actions/workflows/R-CMD-check.yaml)
```

**Expected:** README displays a live CI status badge that updates automatically after each workflow run.

**On failure:** If the badge shows "no status," verify the workflow filename in the badge URL matches the actual file. Push a commit to trigger the first workflow run.

### Step 5: Configure GitHub Repository Settings

1. Enable GitHub Pages (Settings > Pages) pointing to `gh-pages` branch if using pkgdown
2. Add `CODECOV_TOKEN` secret if using coverage reporting
3. Ensure `GITHUB_TOKEN` has appropriate permissions

**Expected:** GitHub Pages is configured for pkgdown deployment. Required secrets are set. Token permissions are sufficient for the workflows.

**On failure:** If Pages deployment fails, check Settings > Pages to ensure the source is set to the `gh-pages` branch. If secrets are missing, add them under Settings > Secrets and variables > Actions.

### Step 6: Push and Verify

```bash
git add .github/
git commit -m "Add GitHub Actions CI workflows"
git push
```

Check the Actions tab on GitHub to verify workflows run successfully.

**Expected:** Green checkmarks on all jobs in the GitHub Actions tab. Workflows trigger on both push and PR events.

**On failure:** Check workflow logs in the Actions tab. Common issues: missing system dependencies (add to `extra-packages`), vignette build failures (ensure pandoc setup step is present), YAML syntax errors.

## Validation

- [ ] R CMD check passes on all matrix platforms
- [ ] Coverage report generates (if configured)
- [ ] pkgdown site deploys (if configured)
- [ ] Status badge shows in README
- [ ] Workflows trigger on both push and PR

## Common Pitfalls

- **Missing `permissions`**: GitHub Actions now requires explicit permissions. Add `permissions: read-all` at minimum
- **System dependencies**: Some R packages need system libraries. Use `r-lib/actions/setup-r-dependencies` which handles most cases
- **Vignettes without pandoc**: Always include `r-lib/actions/setup-pandoc@v2`
- **pkgdown development mode**: Ensure `_pkgdown.yml` has `development: mode: release` for GitHub Pages
- **Caching issues**: `r-lib/actions/setup-r-dependencies` handles caching automatically

## Related Skills

- `create-r-package` - initial package setup including CI workflow
- `build-pkgdown-site` - detailed pkgdown configuration
- `submit-to-cran` - CI checks should mirror CRAN expectations
- `release-package-version` - trigger deployment on release
