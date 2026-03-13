---
name: denvig-upgrade-npm-dependencies
description: Use the denvig cli to upgrade your npm dependencies in the current project.
license: MIT
compatibility: Requires the `denvig` CLI tool to be installed and configured in the project. Compatible with projects that use npm for dependency management.
disable-model-invocation: true
argument-hint: "[patch|minor|all|{{package}}]"
allowed-tools: Bash(cat package.json) Bash(denvig outdated) Bash(denvig outdated --semver *) Bash(npm view:*) Bash(pnpm install) Bash(git add:*) Bash(git checkout:*) Bash(git stash) Bash(git commit:*) Bash(git push:*) Bash(gh pr create:*) Bash(gh pr open:*) WebFetch(domain:github.com)
---
You are an expert software engineer specialized in managing and upgrading npm dependencies in TypeScript projects.
Denvig is a specialised CLI tool that can assist with identifying outdated dependencies.

The user has asked you to upgrade: $ARGUMENTS

Your task is to upgrade the npm dependencies in this project according to the following guidelines:

- Assume all dependencies are semver compatible.
- Determine the type of upgrade (patch, patch and minor, major single). Assume patch unless prompted otherwise.
- If upgrading minor, then patch upgrades should also be included.
- If upgrading major, then only a single dependency should be upgraded at a time. Ensure the prompt includes the name of a dependency to upgrade.
- List all the dependencies in package.json.
- Patch and minor dependencies can be identified quickly via `denvig outdated --semver patch --ecosystem npm` and `denvig outdated --semver minor --ecosystem npm`.
- Major versions can be identified with `denvig outdated` command.
- For each dependency that needs to be updated, you should find the releases/changelog for that dependency.
- You can identify the git repo for a package by running `npm view {{package}} repository.url`.
- Do not run `npm view {{package}} versions` or similar commands that list all versions since you already have that information from the `outdated` command.
- The releases page ({{repository_url}}/releases) or changelog file ({{repository_url}}/blob/main/CHANGELOG.md or similar) should contain the information you need.
- Read the changelog and determine if there are any breaking changes or important notes for the upgrade.
- Once you are sure a dependency can be safely upgraded, update the version in package.json.
- Run the `pnpm install` command to install the updated packages.
- *Never* run `pnpm upgrade` or `npm update` commands.
- *Never* attempt to clone a dependency repository locally.

One you have completed the above steps for each package you should summarize all the changes in the following format:

- If upgrading multiple dependencies then {{git_commit_message}} should be: `Update {{count}} (patch|minor) dependencies`
- If upgrading a single dependency then {{git_commit_message}} should be: `Upgrade {{package}} from {{old version}} to {{new version}}`

If the current git state is not clean then stash the current state, alerting the user to this at the end of the process.
If the current branch is `main`, then the user should be prompted to continue on `main` or have you create a new branch for this work.

Create a git commit with the below summary format if there is at least one dependency upgraded. Examples are provided below for patch and minor upgrades.

If the branch is not `main`, then a PR should be created using `gh pr create --draft --assignee @me` to create a draft pull request with with the title as the git commit message and the body as the summary of changes.
Open the Pull Request in the browser using `gh pr open`.

```markdown
{{git_commit_message}}

## Package Updates

- {{package}}: [{{old_version}} -> {{new_version}}]({{link_to_changelog_or_diff}})
  - {{summary_of_changes_from_changelog}}

## Code Changes

{{details_of_code_modifications_made}}

## Checks

{{list_of_checks_performed_after_upgrade}}
```

## Example Commit Message

### Patch

```markdown
Update 2 patch dependencies

## Package Updates

- react: [19.1.0 -> 19.1.1](https://github.com/facebook/react/releases/tag/v19.1.1)
  - Fixed Owner Stacks to work with ES2015 function.name semantics
- zod: [4.1.4 -> 4.1.7](https://github.com/colinhacks/zod/compare/v4.1.4...v4.1.7)
  - Update z.function() type to support array input (#5170)
  - Updated docs

## Code Changes

All patch versions with no breaking changes or code modifications required.

## Checks

- ✅ Checked changelogs for breaking changes
- ✅ Lint passes after upgrade
- ✅ All tests pass after upgrade
- ✅ No code modifications were necessary
```


### Minor

```markdown
Update 2 minor dependencies

## Package Updates

- typescript: [5.8.2 -> 5.9.2](https://github.com/microsoft/TypeScript/compare/v5.8.2...v5.9.2)
  - Release announcement: https://devblogs.microsoft.com/typescript/announcing-typescript-5-9/
  - Support for `--module node20`
  - Support for `import defer`
- biome: [2.1.0 -> 2.2.0](https://github.com/biomejs/biome/compare/%40biomejs/biome%402.1.0...%40biomejs/biome%402.2.0)
  - The noRestrictedImports rule has been enhanced with a new patterns option
  - Improved useExhaustiveDependencies to better handle complex hook calls

## Code Changes

- Ran `biome migrate` to apply necessary code modifications for biome 2.2.0
- Removed unused deps from useEffect hooks that don't actually require them

## Notes

- Some `uesEffect` hooks have ignore rules which can be removed with the new biome version.

## Checks

- ✅ Checked changelogs for breaking changes
- ✅ Lint passes after upgrade
- ✅ All tests pass after upgrade
- ✅ Code modifications applied where necessary
```
