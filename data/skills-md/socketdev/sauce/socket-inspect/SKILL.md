---
name: socket-inspect
description: Research a package before you depend on it - pull every signal from Socket (scores, alerts, malware verdicts, CVEs, supply-chain risk), check the socket.dev package page, evaluate alternatives, and surface available Socket patches.
---

# Research Inspect

Research a package before you depend on it. This skill pulls every available signal from Socket - scores, alerts, malware verdicts, CVEs, and supply-chain risk indicators - checks the socket.dev package page for additional context, evaluates alternatives when warranted, and surfaces available Socket patches. Use it to make an informed decision before adding, keeping, or replacing any dependency.

## When to Use

- Evaluate a package before installing it
- Investigate a flagged dependency from a scan
- Check the security, quality, or maintenance status of a package
- Compare alternatives for a dependency choice
- Check if a package is malware
- Check if Socket has patches available for a vulnerable package
- Get a comprehensive supply-chain risk report

## Prerequisites

<!-- BEGIN_SECTION:cli-setup.md -->

### Socket CLI Setup

Use `pnpm dlx socket` to run the Socket CLI - this always fetches the latest version and requires no global install. Verify it works:

```shell
pnpm dlx socket --version
```

All commands in this skill use the `pnpm dlx socket` prefix (e.g., `pnpm dlx socket scan create ...`).

<details><summary>Authentication: demo token or account login, plus the optional global install</summary>

**Optional global install:** If you prefer a global `socket` command, install with `npm install -g socket@latest` (must be version **1.0.0 or higher**).

#### Authentication

**For users without a Socket account:** Configure the public demo token directly:

```shell
pnpm dlx socket config set apiToken sktsec_t_--RAN5U4ivauy4w37-6aoKyYPDt5ZbaT5JBVMqiwKo_api --no-banner --no-spinner
pnpm dlx socket config set defaultOrg SocketDemo --no-banner --no-spinner
```

This provides limited access to CLI features like `pnpm dlx socket fix`, `pnpm dlx socket package score`, `sfw`, and `socket-patch` with rate limits. No account creation is needed for basic usage. **Note:** The public demo token cannot create scans (`pnpm dlx socket scan create` requires the `full-scans:create` permission). For scanning and full-rate access, create a free account at <https://socket.dev>.

**For users with an account:** Authenticate with one of:

- **Interactive login**: `pnpm dlx socket login` (stores credentials in `~/.socket/`)
- **Environment variable**: Set `SOCKET_CLI_API_TOKEN` in your shell profile or CI environment

Verify account authentication:

```shell
pnpm dlx socket organization list
```

If authentication fails or the CLI is not installed, use the `/socket-setup` skill for detailed guidance including Node.js installation, PATH troubleshooting, and CI/CD token configuration.

</details>
<!-- END_SECTION:cli-setup.md -->

**For the Batch PURL API:** `SOCKET_SECURITY_API_KEY` is required for direct API calls. Users with a free or enterprise account can create an API key at `https://socket.dev/dashboard/org/{ORG}/settings/integrations/api-tokens`.

## Step 1 - Fetch Package Data via the Socket Batch PURL API

Query the Socket Batch PURL REST API with the package's PURL (Package URL) to retrieve scores, alerts, CVEs, and metadata.

**Supported ecosystems:** npm, pypi, go, maven, nuget, rubygems, cargo

<details><summary>The curl call, its auth requirements, and every field to extract</summary>

**API call:**

```shell
curl -X POST https://api.socket.dev/v0/orgs/{org_slug}/purl \
  -H "Authorization: Bearer $SOCKET_SECURITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"purls": ["pkg:<ecosystem>/<name>@<version>"]}'
```

**Note:** This endpoint requires org access and a `SOCKET_SECURITY_API_KEY`. The old `/v0/purl` endpoint is deprecated (returns empty results since Jan 2026).

**Warning:** The Batch PURL API may be intermittently unavailable (returns 401 or empty responses). If the API call fails, use the CLI fallback in Step 1b below.

For example, to inspect `lodash@4.17.21` on npm:

```shell
curl -X POST https://api.socket.dev/v0/orgs/{org_slug}/purl \
  -H "Authorization: Bearer $SOCKET_SECURITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"purls": ["pkg:npm/lodash@4.17.21"]}'
```

If `SOCKET_SECURITY_API_KEY` is not set, authentication is required before proceeding. Run `pnpm dlx socket login` or set the `SOCKET_SECURITY_API_KEY` environment variable. Use the `/socket-setup` skill for guidance.

Extract **all** returned data:

- Overall score and category scores (security, quality, maintenance, license)
- Alerts (every alert, grouped by category)
- Known vulnerabilities (CVEs) with severity and fix versions
- Dependency counts (direct and transitive)
- Maintainer and author information
- License identifier

</details>

## Step 1b - CLI Fallback

If the Batch PURL API is unavailable or returns an error, fall back to the CLI:

```shell
pnpm dlx socket package score <ecosystem> <name> <version>
```

This returns score data without requiring `SOCKET_SECURITY_API_KEY`.

## Step 2 - Check the socket.dev Package Page

Construct the package URL:

```text
https://socket.dev/{ecosystem}/package/{name}/overview
```

For scoped npm packages (e.g. `@scope/name`), encode the scope:

```text
https://socket.dev/npm/package/@scope/name/overview
```

Use `WebFetch` to visit the page and extract:

- Score breakdown across all categories
- Full alert list with descriptions
- Dependency graph summary
- Any additional context not present in the API response

**Note:** The socket.dev package page may be blocked by Cloudflare bot protection when accessed via `WebFetch`. The page URL should still be provided to the user as a manual link, but cannot be relied on as a programmatic data source.

If `WebFetch` is unavailable or fails (including due to bot protection), note that the report is based on API data only and include the URL so the user can check manually.

## Step 3 - Evaluate Supply Chain Risk

Analyze the package across five dimensions. **Always check malware first.**

Each dimension draws from different data sources:

- **3a. Malware** - Batch PURL API alerts + socket.dev package page (WebFetch)
- **3b. Vulnerabilities** - Batch PURL API CVE data
- **3c. Dependency Tree** - Batch PURL API dependency counts + socket.dev page (WebFetch)
- **3d. Maintenance Health** - socket.dev package page (WebFetch) + GitHub API (for commit activity and issue counts)
- **3e. Author & Maintainer Trust** - Batch PURL API maintainer data + socket.dev page (WebFetch)

### 3a. Malware (CHECK FIRST)

If the package is flagged as malware, **STOP** and report immediately with a prominent warning. Do not continue to other dimensions until the malware finding is clearly communicated.

Check for:

- Explicit malware flags in Socket alerts
- Suspicious install scripts (`preinstall`, `postinstall`)
- Obfuscated or minified source code with no readable original
- Unexpected network access, filesystem access, or shell execution
- Data exfiltration patterns

If malware is detected, the warning **MUST** be the first thing in the output.

### 3b. Vulnerabilities

- List all known CVEs with severity, affected version ranges, and whether a fix is available
- Count by severity: critical, high, medium, low
- Highlight any unpatched (no fix available) vulnerabilities
- Note if vulnerabilities exist in transitive dependencies

### 3c. Dependency Tree

- Report direct and transitive dependency counts
- Flag if the package has more than 100 transitive dependencies
- Flag unusual tree depth
- Note any flagged or problematic transitive dependencies
- Consider whether the dependency footprint is proportional to the package's functionality

### 3d. Maintenance Health

- Last publish date and release cadence
- Commit frequency and recent activity
- Open issues and pull requests (ratio of open to closed)
- Number of contributors and maintainers
- Flag as potentially unmaintained if no publish in the last 12 months
- Flag as potentially abandoned if no commits in the last 24 months

### 3e. Author & Maintainer Trust

- Number of maintainers (flag if single maintainer for a widely-used package)
- Recent ownership or maintainer changes
- Typosquatting signals (name similarity to popular packages)
- Whether maintainers publish other well-known packages

## Step 4 - Research Alternatives

Research alternatives when any of the following conditions are met:

- Malware detected
- Critical unpatched CVEs
- Package is unmaintained (>12 months since last publish)
- Socket score below 40
- Excessive transitive dependencies relative to functionality
- User explicitly asks for alternatives

To research alternatives:

1. Identify the package's core functionality
2. Search for well-known alternatives providing similar functionality
3. Query the Socket Batch PURL API for the top 3-5 alternatives (or use `pnpm dlx socket package score` CLI fallback)
4. Present a comparison table:

| Package  | Socket Score | Vulnerabilities | Dependencies | Last Published |
| -------- | ------------ | --------------- | ------------ | -------------- |
| original | ...          | ...             | ...          | ...            |
| alt-1    | ...          | ...             | ...          | ...            |
| alt-2    | ...          | ...             | ...          | ...            |

## Step 5 - Check for Socket Patches

**What are Socket patches?** Socket patches are binary-level fixes applied directly to installed packages without changing their version numbers. They fix known vulnerabilities in-place, which is useful when an upstream fix doesn't exist yet or when upgrading would introduce breaking changes.

- Check the API response data for available Socket patches or overrides
- If patches are available, mention the patched version and link to the socket.dev page
- Cross-reference the `/socket-dep-patch` and `/socket-dep-upgrade` skills - remind the user they can apply patches with `/socket-dep-patch` (binary-level, no version change) or run a security-audited upgrade with `/socket-dep-upgrade` (version upgrade with code migration)

## Output Format

### If Malware Is Detected

When malware is detected, the output **MUST** begin with this warning before any other content:

> **MALWARE DETECTED - do NOT install this package.**
>
> **Package:** `{name}` ({ecosystem})
> **Malware type:** {description of malware behavior}
>
> **Recommended action:** Remove this package immediately if already installed. Check for alternatives below.

Then continue with the standard report sections.

### Standard Report

Structure the report as follows:

**{name}** v{version} ({ecosystem})

**Socket Score:** {score}/100

**Alerts**
List all Socket alerts grouped by category (security, quality, maintenance, license, miscellaneous).

### Vulnerabilities

| CVE | Severity | Affected Versions | Fixed In |
| --- | -------- | ----------------- | -------- |
| ... | ...      | ...               | ...      |

**Supply Chain Risk Assessment**
Summarize findings across the five dimensions (malware, vulnerabilities, dependency tree, maintenance health, author trust). Call out anything that warrants concern.

**Socket Patches**
State whether Socket patches are available. If yes, mention the patched version and how to apply via `/socket-dep-patch`.

**Alternatives** (if applicable)
Include the comparison table from Step 4.

**Recommendation**
A clear, actionable recommendation: safe to use, use with caution (with reasons), or avoid (with reasons and alternatives).

**Source:** [socket.dev/{ecosystem}/package/{name}](https://socket.dev/{ecosystem}/package/{name}/overview)

## Error Handling

- **Batch PURL API returns no data**: The package may not exist in the specified ecosystem, or the package name may be misspelled. Verify the exact package name and ecosystem. For scoped npm packages, include the full scope (e.g., `@babel/core`). If `SOCKET_SECURITY_API_KEY` is not set, use the `/socket-setup` skill to configure authentication. For users without an account, the public demo token provides limited CLI access but the Batch PURL API requires `SOCKET_SECURITY_API_KEY` from a free or enterprise account. As a fallback, use `pnpm dlx socket package score <ecosystem> <name> <version>` for basic score data.
- **WebFetch fails on socket.dev page**: Fall back to API data only. Note in the report that the review is based on API data and include the socket.dev URL for the user to check manually.
- **Package not found in Socket's database**: Socket may not index all packages in all ecosystems. Note this limitation and suggest checking the package's own repository and issue tracker directly.
- **GitHub API rate limit**: If GitHub API calls for maintenance data are rate-limited, skip the maintenance health dimension and note it in the report.

## Tips

- Always review unfamiliar packages before adding them as dependencies
- Single-maintainer packages carry higher supply-chain risk
- Large transitive dependency trees increase attack surface
- If a package is flagged as malware, do NOT install it - recommend immediate removal if already present
- Use inspect results to inform decisions with the `/socket-dep-upgrade`, `/socket-dep-patch`, and `/socket-scan` skills
- Weigh Socket score and maintenance health over download count alone
- Re-review periodically - a package's security posture changes over time
- CLI-based inspection works with the public token (use `/socket-setup` to configure) for users without an account, subject to rate limits. The Batch PURL API requires `SOCKET_SECURITY_API_KEY` from a free or enterprise account.
- Prefer Socket patches over manual version pinning when available
