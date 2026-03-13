---
name: changelog-generator
description: Generates audience-aware changelogs from git history with SemVer impact classification, migration instructions for breaking changes, grouped categories (features, fixes, performance, dependencies), and upgrade guides for major versions. Use when generating changelogs, writing release notes, preparing version bumps, or when the user needs to document what changed between releases.
---

# Changelog Generator

## Overview

Generate structured, audience-aware changelogs from git history. The skill
classifies every commit by SemVer impact, groups changes into categories, writes
descriptions appropriate for the target audience (developers vs end-users), and
produces migration guides for breaking changes.

## When to use

- When generating a changelog between two git refs (tags, branches, SHAs)
- When writing release notes for a new version
- When preparing a version bump and need to determine SemVer impact
- When the user mentions "changelog", "release notes", "what changed", or
  "version bump"
- When documenting breaking changes with migration instructions

**Do NOT use when:**

- The user wants to _read_ an existing changelog (just open the file)
- The task is writing commit messages (use git-conventional-commits instead)
- The user needs a git log dump with no classification or formatting

## Workflow

### 1. Parse git history between refs

Determine the two reference points for the changelog:

- **Explicit refs:** User provides `v1.2.0..v1.3.0` or `main..release/2.0`
- **Implicit refs:** Last tag to HEAD, or last two tags

Run `git log` between the refs with a structured format:

```bash
git log --format="%H|%s|%b|%an|%ae|%aI" <from-ref>..<to-ref>
```

Parse each commit into:

- **Hash** (for linking)
- **Subject line** (primary classification input)
- **Body** (look for `BREAKING CHANGE:` footers, issue refs, PR refs)
- **Author** (for contributor attribution)

Extract PR numbers from subject lines (`(#123)`) and issue references from
bodies (`Fixes #456`, `Closes #789`).

### 2. Classify each commit by SemVer impact

Apply these rules in priority order:

| Signal                                               | SemVer Impact      | Examples                      |
| ---------------------------------------------------- | ------------------ | ----------------------------- |
| `BREAKING CHANGE:` footer in body                    | **Major**          | API removal, signature change |
| `!` after type (e.g., `feat!:`)                      | **Major**          | Any breaking change           |
| Subject contains "breaking" or "remove" + public API | **Major**          | Removed deprecated endpoint   |
| Type is `feat` or subject adds new capability        | **Minor**          | New endpoint, new CLI flag    |
| Type is `fix`, `perf`, `docs`, `chore`, `refactor`   | **Patch**          | Bug fix, optimization, docs   |
| Type is `deps` or subject updates dependencies       | **Patch**          | Bumped lodash to 4.17.21      |
| Type is `security` or subject fixes vulnerability    | **Patch** (urgent) | CVE fix, auth bypass patch    |

**The overall release version is determined by the highest-impact commit:**

- Any major commit = major version bump
- Otherwise, any minor commit = minor version bump
- Otherwise = patch version bump

### 3. Group commits by category

Organize commits into these categories, in this order:

1. **Breaking Changes** - Always first, always prominent
2. **Features** - New capabilities (`feat`)
3. **Bug Fixes** - Corrections (`fix`)
4. **Performance** - Optimizations (`perf`)
5. **Security** - Vulnerability fixes (`security`)
6. **Dependencies** - Dependency updates (`deps`, `chore(deps)`)
7. **Other** - Everything else (`docs`, `refactor`, `chore`, `test`, `ci`)

Empty categories are omitted. Each category gets a heading and its commits
listed beneath it.

### 4. Write audience-appropriate descriptions

Changelogs serve two audiences. Determine which from context:

**Developer changelog** (default — for CHANGELOG.md):

- Use technical language, reference APIs, mention file paths
- Include commit hashes (short form) and PR links
- Show the conventional commit type prefix
- Example: `fix(auth): resolve JWT expiry race condition (#342)`

**End-user release notes** (when user asks for "release notes" or
"user-facing"):

- Use plain language, describe behavior changes from the user's perspective
- No commit hashes, no file paths, no internal API names
- Group by what users care about: "What's New", "Fixed", "Improved"
- Example:
  `Fixed an issue where sessions expired unexpectedly during long operations`

**Hybrid** (when both audiences need serving):

- Produce two sections or two files: one technical, one user-facing

### 5. Handle breaking changes with migration guides

Every breaking change MUST include:

1. **What changed** - Precise description of the breaking change
2. **Why it changed** - Motivation (security, performance, design improvement)
3. **Migration steps** - Numbered steps to update from old to new behavior
4. **Before/after code examples** - Show the old way and the new way

````markdown
### Breaking Changes

#### `createUser()` now requires an `options` object instead of positional args

**Why:** Positional arguments became ambiguous as the parameter list grew. This
aligns with the builder pattern used elsewhere in the SDK.

**Migration:**

1. Replace positional arguments with a named options object
2. The `role` parameter is now required (previously defaulted to `"user"`)

```diff
- const user = createUser("jane@example.com", "Jane", "admin");
+ const user = createUser({
+   email: "jane@example.com",
+   name: "Jane",
+   role: "admin",
+ });
```
````

### 6. Add links and metadata

Include in the changelog:

- **PR links** - `[#123](https://github.com/org/repo/pull/123)`
- **Issue links** - `Fixes [#456](https://github.com/org/repo/issues/456)`
- **Compare link** -
  `[Full diff](https://github.com/org/repo/compare/v1.2.0...v1.3.0)`
- **Release date** - ISO date of the release
- **Contributors** - List of unique authors (for open-source projects)

Detect the repository URL from `git remote get-url origin` and construct links
automatically.

### 7. Produce the final output

Generate a structured changelog following this template:

```markdown
# Changelog

## [X.Y.Z](compare-link) (YYYY-MM-DD)

### Breaking Changes

- **description** — migration guide below

#### Migration: description

Steps and before/after examples...

### Features

- **scope:** description ([#PR](link))

### Bug Fixes

- **scope:** description ([#PR](link)), closes [#issue](link)

### Performance

- **scope:** description ([#PR](link))

### Security

- **scope:** description — upgrade urgency: HIGH

### Dependencies

- Bump package-name from X.Y.Z to A.B.C

---

**Full Changelog:** [v1.2.0...v1.3.0](compare-link) **Contributors:** @author1,
@author2
```

## Checklist

- [ ] Git refs identified (from-ref and to-ref)
- [ ] All commits between refs parsed with hash, subject, body, author
- [ ] Each commit classified by SemVer impact (major/minor/patch)
- [ ] Overall version bump determined from highest-impact commit
- [ ] Commits grouped by category (breaking, features, fixes, perf, etc.)
- [ ] Descriptions written for target audience (developer vs end-user)
- [ ] Every breaking change has migration steps and before/after examples
- [ ] PR and issue links included where available
- [ ] Compare link and release date included
- [ ] Empty categories omitted from output

## Example

**Input:** Generate a changelog for the commits between v2.3.0 and v2.4.0.

Given these commits:

```
a1b2c3d feat(api): add batch endpoint for bulk user creation (#201)
d4e5f6a fix(auth): resolve token refresh race condition (#198)
b7c8d9e fix(db): handle connection pool exhaustion under load (#195)
f0a1b2c perf(query): add index hint for user search queries (#199)
e3d4c5b chore(deps): bump express from 4.18.2 to 4.19.0
```

**Output:**

```markdown
## [2.4.0](https://github.com/acme/api/compare/v2.3.0...v2.4.0) (2026-03-06)

### Features

- **api:** add batch endpoint for bulk user creation
  ([#201](https://github.com/acme/api/pull/201))

### Bug Fixes

- **auth:** resolve token refresh race condition
  ([#198](https://github.com/acme/api/pull/198))
- **db:** handle connection pool exhaustion under load
  ([#195](https://github.com/acme/api/pull/195))

### Performance

- **query:** add index hint for user search queries
  ([#199](https://github.com/acme/api/pull/199))

### Dependencies

- Bump express from 4.18.2 to 4.19.0

---

**Full Changelog:**
[v2.3.0...v2.4.0](https://github.com/acme/api/compare/v2.3.0...v2.4.0)
```

**SemVer classification:** Minor (highest impact is `feat` = minor bump)

## Common mistakes

| Mistake                               | Fix                                                                                  |
| ------------------------------------- | ------------------------------------------------------------------------------------ |
| Flat bullet list of commit messages   | Group by category with headings. Never dump raw git log.                             |
| Missing SemVer classification         | Every changelog must state the version bump level and why.                           |
| Developer jargon in user-facing notes | Rewrite for the audience: "Fixed login timeout" not "fix(auth): JWT expiry race"     |
| Breaking changes buried in the list   | Breaking changes ALWAYS go first with their own prominent section.                   |
| No migration instructions             | Every breaking change needs: what changed, why, steps to migrate, before/after code. |
| Missing PR/issue links                | Extract from commit subjects and bodies. Link to the repo.                           |
| No compare link                       | Always include a GitHub/GitLab compare URL for the full diff.                        |
| Including merge commits               | Filter out merge commits — they duplicate information.                               |
| Mixing audiences                      | Pick one audience or produce separate sections. Don't mix technical and user-facing. |

## Quick reference

| Operation                | How                                                     |
| ------------------------ | ------------------------------------------------------- |
| Get commits between refs | `git log --format="%H\|%s\|%b\|%an\|%aI" v1..v2`        |
| Detect breaking changes  | Look for `BREAKING CHANGE:` footer or `!` after type    |
| Extract PR number        | Regex: `\(#(\d+)\)` in subject line                     |
| Extract issue refs       | Regex: `(?:Fixes\|Closes\|Resolves)\s+#(\d+)` in body   |
| Get repo URL             | `git remote get-url origin` then strip `.git` suffix    |
| Build compare link       | `https://github.com/{org}/{repo}/compare/{from}...{to}` |
| Determine version bump   | Highest impact wins: major > minor > patch              |

## Key principles

1. **Breaking changes are first-class citizens** - They always appear first,
   always have migration guides, and always include before/after code. A
   changelog that buries breaking changes causes upgrade failures.

2. **Audience determines language** - The same change is described differently
   for developers ("fix JWT expiry race in token refresh middleware") and users
   ("Fixed an issue where sessions expired during long operations"). Never mix
   audiences in the same section.

3. **SemVer classification is mandatory** - Every changelog must determine and
   state the version bump level. This is not optional metadata — it drives
   release decisions and communicates risk to consumers.

4. **Links connect the changelog to the codebase** - PR links, issue links, and
   compare URLs let readers drill into details. A changelog without links is a
   dead end.

5. **Categories create scannable structure** - Grouped headings (Features,
   Fixes, Performance) let readers find what matters to them. A flat list forces
   everyone to read everything.
