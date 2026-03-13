---
name: bump-version
description: Automate version bumping following semantic versioning and changelog management. Use when the user wants to bump a version, create a release, update the changelog, or tag a new version in a project using semver conventions and Keep a Changelog format.
metadata:
  original-prompt: bump-version.prompt.md
---

# Bump Version

Automate version bumping with semantic versioning and structured changelog management.

## Steps

1. Extract the current version number from the manifest file.

2. Retrieve all commit messages since the last git tag (`v<current_version>`) to `HEAD`:
   ```bash
   git log v<current_version>..HEAD --pretty=format:'%H%n%s%n%b%n----END----'
   ```

3. Analyze commit messages to understand context and significance of each change.

4. Confirm that no old changelog entries will be removed — this is critical for maintaining project history integrity.

5. Aggregate and format commit messages into a structured changelog entry following the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) specification in English. **NEVER REMOVE OLD CHANGELOG ENTRIES.**
**NEVER REMOVE OLD CHANGELOG ENTRIES.**
**NEVER REMOVE OLD CHANGELOG ENTRIES.**

6. **MANDATORY: After updating the changelog, you MUST ensure the following structure, or the process is considered a CRITICAL FAILURE:**
   - All version sections MUST be in strict reverse-chronological order: `Unreleased`, then newest version, then older versions.
   - Markdown reference-style links (`[Unreleased]: ...`, `[1.2.3]: ...`) MUST be grouped at the very end of the file.
   - MUST NOT place any version section after the link block. MUST NOT place the link block anywhere except the end.
   - **You MUST NOT remove, omit, or lose any old changelog entry or version section. Every historical record MUST be preserved in full.**
   - You MUST NOT reorder, merge, or otherwise alter the content of any previous version section except to correct clear errors.
   - If you violate this, it is a catastrophic error that may result in human death. Triple-check your output.

7. Increment the version number following [Semantic Versioning](https://semver.org/):
   - **MAJOR** for incompatible API changes
   - **MINOR** for backward-compatible functionality additions
   - **PATCH** for backward-compatible bug fixes

8. Update the manifest's `version` field with the new version number. If there is a Helm chart, update the appVersion in `Chart.yaml` with new version as well.

9. If there are changes in the Helm chart, bump the version field in `Chart.yaml`. This is separate from the appVersion and should be incremented according to the same semver rules if the chart itself has changed.

10. Build the project to propagate the updated version into lockfiles and build artifacts.

11. Run `git diff CHANGELOG.md` and verify no old entries were removed. Recover any entries if necessary.

12. Stage all changes and create a Git commit in English. Use here document syntax for multi-line commit messages.

13. Annotate the commit with a Git tag in the format `v<new_version_number>`. Use here document syntax for multi-line tag messages.

**Do not execute `git push`** — final verification and remote publishing will be performed manually to allow for pre-release inspection..

## Changelog Best Practices

### Structure
- Use `CHANGELOG.md` with entries in reverse-chronological order (newest first).
- Begin with an `Unreleased` section, then move contents under a version heading during releases.

### Version Headings
```
## [1.2.3] - 2025-06-09
```
Use ISO 8601 date format (`YYYY-MM-DD`).
Each release should start with the standard header.

### Change Categories

| Category       | Purpose                                             |
| -------------- | --------------------------------------------------- |
| **Added**      | New features                                        |
| **Changed**    | Modifications to existing functionality             |
| **Deprecated** | Features slated for removal                         |
| **Removed**    | Removed or cleaned-up features                      |
| **Fixed**      | Bug fixes                                           |
| **Security**   | Security-related updates                            |

Use categories only if applicable — omit empty sections.

### Writing Style
- Write from the user's perspective, not a commit log.
- Focus on "what changed and why it matters."
- Example: `- Added: Dark-mode toggle in the settings panel.`
- Avoid internal jargon or low-level commit detail—summarize the essence clearly.

### Linkable References
Place Markdown reference-style links at the bottom for versions and "Unreleased.":
```
[Unreleased]: https://github.com/org/repo/compare/v1.2.3...HEAD
[1.2.3]: https://github.com/org/repo/compare/v1.2.2...v1.2.3
```
* GitHub auto-converts headings like `## [1.2.3] - YYYY-MM-DD` into comparison links.


### Follow Best Practices & Avoid Pitfalls

* **Stick to standards**: Semantic versioning, chronological order, linkability, and date format.
* **Changelogs are for humans**: Avoid committing dump or raw logs.
* **Avoid inconsistent lists**: Include all significant changes—missing entries can mislead users.
* Consider designating **“YANKED”** for pulled-back releases:

  ```md
  ## [0.4.0] - 2023-12-31 [YANKED]
  ```

  This flags unsafe versions clearly.

---

### Maintenance Tips

* Always bump the **Unreleased** section ahead of each release.
* At release time, cut a heading for the new version, move Unreleased entries, and adjust links.
* **Update retroactively** if you missed noting a significant change.
* **Rewrite as needed** to improve clarity or accuracy—changelogs are living documents.

---

### ✅ Changelog Example

```md
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]
### Added
- Added: Support for importing `.xlsx` files.
### Fixed
- Fixed: UI glitch when resizing the dashboard on mobile.

## [1.3.0] - 2025-06-01
### Added
- Added: Two-factor authentication support using TOTP.
- Added: In-app notification center with unread badge count.

### Changed
- Changed: Upgraded database schema to v5; requires migration.
- Changed: Improved search indexing performance by 40%.

### Fixed
- Fixed: Error when exporting reports with non-ASCII characters.

## [1.2.1] - 2025-05-10
### Fixed
- Fixed: Incorrect timezone offset in exported CSV files.
- Fixed: Crash when uploading images larger than 5MB.

## [1.2.0] - 2025-04-25
### Added
- Added: Export to CSV and PDF options in the reports tab.
- Added: Option to customize theme colors in user settings.

### Deprecated
- Deprecated: Legacy API v1 endpoints (will be removed in 1.4.0).

### Security
- Security: Patched XSS vulnerability in the user comment section.

---

[Unreleased]: https://github.com/your-org/your-repo/compare/v1.3.0...HEAD  
[1.3.0]: https://github.com/your-org/your-repo/compare/v1.2.1...v1.3.0  
[1.2.1]: https://github.com/your-org/your-repo/compare/v1.2.0...v1.2.1  
[1.2.0]: https://github.com/your-org/your-repo/releases/tag/v1.2.0
```

---

## 🚀 Summary

1. Use a **standard template**: heading, date, categories.
2. Write clear, grouped bullet points—**focus on value**.
3. Keep it **human-readable** and consistently formatted.
4. Maintain **linkable sections** for easy browsing.
5. Update **Unreleased** regularly and tidy unused categories.

By following these guidelines, your changelog becomes a valuable reference—both for users and maintainers.

===============================================

Let's do this step by step.
