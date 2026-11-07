---
name: version-aware-recommendations
description: Use when recommending, installing, deploying, or pinning software versions, or listing features and capabilities of any external software, library, or tool
---

# Version-Aware Recommendations

**Core rule: never recommend a version or feature set from internal memory. Always verify against current, external sources.**

Agent memory of software versions drifts within months. Feature sets change, major releases land, and "latest stable" becomes wrong. Every version recommendation must be grounded in a live lookup.

## When to Use

- Recommending a language runtime, framework, library, or tool version
- Installing or deploying software (apt, pip, npm, docker, homebrew, etc.)
- Pinning a dependency to a specific version
- Listing features, capabilities, or requirements of external software
- Comparing software options ("Which database should we use?")
- Setting up CI/CD toolchains, base images, or SDK targets

**NOT needed for:** project-internal versions (your own app version, internal monorepo packages).

## Procedure

1. **Identify the software** — name the exact package, image, or tool.
2. **Search the official source** — use `web_search` or `read` the official URL. Primary sources: project website, GitHub/GitLab releases, Docker Hub, package registry (PyPI, npm, crates.io, Maven), Homebrew formula.
3. **Determine latest stable** — filter out alpha/beta/RC/pre-release tags. Identify the latest stable release version.
4. **Verify current documentation** — read the current docs for the identified version. Features, defaults, and deprecations change; do not rely on memory. Use the documentation lookup table below.
5. **Recommend with evidence** — state the version and link to the source where you found it. Include the feature set from current docs, not memory.

### Documentation Lookup (step 4)

| Available tools | Use for | Do NOT use for |
|-----------------|---------|----------------|
| context7 MCP tools (exposed as `resolve-library-id` + `query-docs`, or device paths `xd://mcp__context_context_resolve_library_id` / `xd://mcp__context_context_query_docs`) | Verifying features, configuration, defaults, code examples, and deprecations of libraries/frameworks **from their official docs** | Version numbers — registries and release pages are authoritative |
| Official docs via `read` | Fallback when context7 is unavailable or has no entry; always for version/release facts | — |

When context7 is available, run it FIRST for the docs step — do not guess doc URLs:

1. `resolve-library-id` with `{libraryName: "FastAPI", query: "<what you need to verify>"}`. Pick the match with exact name, High/Medium source reputation, and most code snippets.
2. `query-docs` with `{libraryId: "/org/project", query: "<one specific topic>"}`. The parameter is `query`, not `topic`. One concept per call; scope a separate call per distinct concept.
3. To verify docs for a specific version, use the version-pinned ID (e.g. `/vercel/next.js/v14.3.0`) — pick it from the versions listed by `resolve-library-id`.
4. If `resolve-library-id` returns no good match after ≤3 attempts, fall back to official docs via `read`, and corroborate critical feature claims against the project's own release notes.

**Per-question budget:** each context7 tool errors past 3 calls. Multi-concept verification must stay within one `query-docs` call per concept and still stop at 3 — merge concepts into one query only when they interact, otherwise prioritize the concept your recommendation hinges on and corroborate the rest via official docs `read`.

### Pre-release Exception

**Default to stable.** Pre-releases (alpha, beta, RC, nightly, canary, -dev, -preview) are rejected unless one exception applies:

- **Required feature gap:** A specific feature or bug fix exists only in a pre-release and is required by the current requirements. State which feature and why stable is insufficient.
- **No recent stable:** The project has no stable release in the last 12 months, or is early-stage / abandoned. State the project's release history and why pre-release is the best available option.

If an exception applies, the agent must explicitly state:
1. Which exception applies
2. Why stable is not suitable
3. The pre-release version being recommended
4. The risk of depending on pre-release software

### Version Pinning

When pinning to a non-latest version, document the rationale:

| Rationale | Example |
|-----------|---------|
| Compatibility constraint | "Pinned to v3.2 because v4.0 drops support for Node < 18" |
| Known regression | "Avoid v2.7.1 — upstream issue #1234 breaks our use case; v2.7.0 works" |
| Reproducibility | "Pinned to v1.4.3 to match existing CI and production" |
| EOL / security | "Pinned to v5.x LTS; v6.x is unsupported for our platform" |

**Never pin silently.** The pin and its reason must be visible in code comments, lock files, or documentation.

## Pitfalls

- **Memory drift:** "Python 3.11 is latest" — wrong; 3.12 or 3.13 may be current. Always look up.
- **Feature hallucination:** Listing capabilities from outdated memory. Read the current docs.
- **Doc-URL guessing:** Fabricating doc paths (`/tutorial/websockets/` → 404) and retrying variants. When context7 is available, query it; otherwise start from the docs index or a site-scoped search.
- **context7 for versions:** context7 indexes documentation, not release registries. Version numbers still come from PyPI/npm/GitHub releases/Docker Hub.
- **Pre-release as stable:** "v2.0.0-rc.1" is not stable. Filter pre-releases unless an exception applies.
- **Silent pinning:** Pinning `flask==2.2.0` without explaining why. Future agents (or you) will not know the constraint.
- **Partial verification:** Looking up the version but guessing features. Both version AND feature set need live verification.
- **Secondary sources:** Blog posts, Stack Overflow, or third-party articles may be outdated. Always confirm against the official source.

## Verification

After making a recommendation, confirm:
- The version number matches what's on the official source (link included)
- Features listed match current documentation, not memory
- If pre-release: exception is stated with justification
- If pinned: rationale is documented inline

Quick check before proceeding:
```
Is this version number from a live lookup? If no → stop, search.
Am I listing features from memory? If yes → stop, read docs.
Did I guess a documentation URL while context7 was available? If yes → stop, use query-docs.
Is this a pre-release without documented justification? If yes → stop, either find stable or document exception.
Is this pin documented with a reason? If no → stop, add rationale.
```
