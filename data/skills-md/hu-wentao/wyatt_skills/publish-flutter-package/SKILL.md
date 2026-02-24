---
name: publish-flutter-package
description: Automates the Flutter package release process via git tags and GitHub Actions. Handles multi-package workspaces, SemVer versioning suggestions based on git history, updating pubspec.yaml and CHANGELOG.md, and dry-run validation. Use when the user wants to "release", "publish", or "version" a Flutter package.
---

# Publish Flutter Package

This skill automates the Flutter package release workflow triggered by git tags.

## Workflow

### 0. Pre-check
#### 0.1 Project Root
Verify that the current working directory is the root of the Git repository (contains a `.git` folder and the main `pubspec.yaml`).
- If not at the root (e.g., inside a sub-package directory), **advise the user to switch to the project root directory** before proceeding to ensure `.github/workflows` and workspace configurations can be correctly identified.

#### 0.2 Detect Packages (Workspace Support)
Read the root `pubspec.yaml` file.
- Check for the `workspace:` field.
- If present, parse the paths (e.g., `- packages/*`) to find all nested packages.
- Ask the user which package to publish if multiple are detected.
- **Store the relative path to the selected package** (e.g., `packages/my_package`) for subsequent steps.

### 1. GitHub Actions Verification
#### 1.1 Configuration Check & Tag Format Discovery
Run `scripts/inspect_workflows.py [package_name]` to find and parse publishing workflows.
- The script returns a JSON list of identified workflows, their `uses` field, and their `on.push.tags`.
- If a package name is provided, the script ranks workflows based on relevance (e.g., if the filename contains the package name).
- **Selection Logic**:
  - Verify that the chosen workflow's `uses` points to `dart-lang/setup-dart/.github/workflows/publish.yml`.
  - Extract the expected tag format from the `tags` list (e.g., `v*`).
  - If multiple workflows exist, **recommend the one with the highest score and ask the user to confirm**.
  - **If the user skips or provides no alternative, proceed with the recommended workflow.**
  - If no matching workflow is found, show the [Github Action Template](references/github_action_template.md) and guide the user to create one.
  - For more details on the automated publishing flow, refer to [Automated publishing](https://dart.dev/tools/pub/automated-publishing).

### 2. Versioning Strategy (SemVer)
- Use `scripts/prepare_release.py <current_version> [--tag-match <pattern>] [--package-path <path>]` to analyze git history since the last tag.
  - If the tag format from Step 1.2 is non-standard (e.g., `package-name-*`), pass it as `--tag-match` to ensure the correct last tag is identified.
  - **Pass the relative path of the package** (from Step 0.2) as `--package-path` to filter the git history to only include changes affecting that package.
- This script provides a suggested version based on commit types (feat/fix/breaking) and generates a formatted `CHANGELOG.md` entry.
- Present the suggestion and the draft changelog entry to the user. **If the user skips or provides no alternative, proceed with the suggested values.**
- Allow the user to edit the version or the content before proceeding.

### 3. Documentation Updates
#### 3.1 pubspec.yaml
Update the `version` field in the relevant package's `pubspec.yaml` with the chosen version.

#### 3.2 CHANGELOG.md
Insert the confirmed `CHANGELOG.md` entry at the top of the file (after any initial headers).
Format requirement:
```markdown
## <Version> <YYYY-MM-DD>
* feat/fix/... [**important**] <content>
```
Note: Ensure the format matches the user's project-specific conventions if they differ from the suggested draft.

### 4. Git Commit & Validation (Dry Run)
#### 4.1 Git Commit
Commit the modified `pubspec.yaml` and `CHANGELOG.md` files:
```bash
git add .
git commit -m "chore(release): <version>"
```

#### 4.2 Validation (Dry Run)
Run `dart pub publish --dry-run` to verify the package contents and configuration.
- **Troubleshooting**: If publication consistently fails or you encounter unexpected issues, refer to the [official publishing guide](https://dart.dev/tools/pub/publishing) for the latest release process and requirements.
- **Proceed only if the dry run is successful.**

### 5. Git Tagging & Push
Once validated, add a new git tag and push everything to trigger the automated release.
- **Tagging**: Add a new git tag matching the format found in Step 1.1 using `git tag`.
  - Example: If the tag format is `v[0-9]+.[0-9]+.[0-9]+`, the tag should be `v<version>`.
- **Pushing**: Push the new commit and tag to the remote repository to trigger the GitHub Action:
  ```bash
  git push
  git push origin <tag_name>
  ```

## Resources

### scripts/
- `inspect_workflows.py`: Automatically discovers and parses GitHub Action workflows to identify publishing configurations and tag formats.
  - Arguments: `[package_name]`
- `prepare_release.py`: Analyze git history to suggest SemVer version and generate `CHANGELOG.md` entry.
  - Arguments: `<current_version>`
  - Optional: `--tag-match <pattern>` (e.g., `my-pkg-*` or `v*`) to find the correct previous tag.
  - Optional: `--package-path <path>` (e.g., `packages/my_pkg`) to filter changes by package directory.

### references/
- `github_action_template.md`: A template for setting up the GitHub Action for publishing.
