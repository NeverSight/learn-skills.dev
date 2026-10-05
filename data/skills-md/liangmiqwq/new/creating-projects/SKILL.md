---
name: creating-projects
description: Load this skill when you are required to create projects. Do not load this skill when you are creating reproduction/poc repo.
---

When you are creating a project, you should make it usable and maintainable, you need to make infrastructure tools, release and validation system work perfectly.

When creating projects, what you should focus on is not the project code, but everything except project code.

You can create a small placeholder like `todo!()` macro and `console.error()`. You can fill the code later if I required. If I don't require you implement any logic, just keep placeholders.

**Read [guide.md](./guide.md) before writing any file.** It explains how to read the request, what you may change in a template and why, how to write the docs, and what to do when no template fits.

## Required initialization gate

For a completely new project, finish the managed project initialization before writing any scaffold or project files:

1. Load the `$global-projects` skill and use its paired resolver to find the configured project root and project CLI.
2. Resolve the repository owner and name. If either is missing or ambiguous, ask the user before creating the project directory.
3. Resolve whether the repository should be public or private. If the user did not specify visibility, ask before continuing. "Private" only sets the GitHub repository visibility. It never makes a package `private: true` and never removes npm publishing from the release workflow.
4. Resolve a one-sentence description of what the project does. If the request doesn't say, ask. Never describe the scaffold instead, like "Private TypeScript workspace for <repo>".
5. Run the selected CLI's `init` command with the explicit visibility option from `<root>/<owner>/<repo>`.
6. Verify the local path and `origin` remote, then create the scaffold inside that initialized repository (see [Templates](#templates)).

An explicit request to create or initialize a new project authorizes the managed initialization. Once the owner, name, visibility, and description are known, do not ask for a second confirmation before running `moi init --public`, `moi init --private`, or the paired `mo` command.

Do not create the project in the current task directory, `work/`, `outputs/`, or another artifact directory unless the user explicitly chose that location. Generic artifact-output guidance does not override the managed project workflow.

Do not use plain `git init` as a substitute for `moi init` or `mo init`. Do not silently skip managed initialization because a required choice is missing; ask the user for that choice instead.

## Templates

Templates live in `templates/` next to this file. Load `$choosing-tools` to pick the stack, then copy its layers in order into `<root>/<owner>/<repo>`:

| Stack    | Layers                     | Use for                    |
| -------- | -------------------------- | -------------------------- |
| `rust`   | `common` + `rust`          | Rust crates and CLIs       |
| `js-lib` | `common` + `js` + `js-lib` | npm libraries              |
| `js-cli` | `common` + `js` + `js-cli` | Node.js command line tools |

Websites and napi-rs projects have no template yet. Build them by hand, still following `common` and the aspects below.

For a workspace (monorepo), apply the stack in two levels as described in [guide.md](./guide.md#workspaces).

While copying:

1. Rename `_name` paths to `.name`, and `__repo__` paths to the repo name.
2. Don't copy `AGENTS.part.md` and `CONTRIBUTING.part.md`. Merge every layer's part, in layer order, into the `{{toolchain}}` line of `AGENTS.md` and the `{{setup}}` line of `CONTRIBUTING.md`.
3. Fill `{{owner}}`, `{{repo}}`, `{{repo_ident}}` (the repo name with `-` replaced by `_`), `{{description}}`, `{{year}}` and `{{rust_version}}` (from `rustc --version`).
4. Add `.github/FUNDING.yml` with `github: [<owner>]` when the owner has a GitHub Sponsors profile.

Templates don't pin dependency versions. Add them at their latest versions inside the new project instead, and never copy pinned versions from other projects:

- `js`: Write the current Node major version to `.node-version`. Add `vite` (aliased to `npm:@voidzero-dev/vite-plus-core@<version>`), `vite-plus` (pinned to the version `@liangmi/vp-config` supports), `@liangmi/vp-config`, `typescript`, `@typescript/native-preview`, `@types/node` and `bumpp` to the catalog and to `devDependencies` as `catalog:`, as described in [guide.md](./guide.md#dependencies). Override `vite@*` to `catalog:` and allow any `vite` version in `peerDependencyRules`, then run `vp install`.
- `js-cli`: Add `cac` and `picocolors` the same way, as dev dependencies (CLI dependencies are bundled).
- `rust`: `cargo add insta --dev -p <repo>`, `cargo add criterion --dev -p benchmark`, `cargo add <repo> --path crates/<repo> --dev -p benchmark`, then `dprint config update --yes`.

After scaffolding:

1. Write every `{{TODO: ...}}` placeholder, mostly in `AGENTS.md`. Config owned by a fast-moving tool, like `vite.config.ts` for `@liangmi/vp-config`, is left as a placeholder; write it by following that tool's skill. Delete a section instead of leaving it empty. Keep what you write into `AGENTS.md` short, so the file stays around 40 lines.
2. Adjust the scaffold to the project: the package name (for example a scoped npm name), extra crates or packages, CLI binaries, and the CI matrix.
3. Set the GitHub repo settings (squash merge only, PR title and description as the commit message, auto delete branches, a description):

   ```bash
   gh repo edit <owner>/<repo> --description "<description>" --enable-squash-merge --enable-merge-commit=false --enable-rebase-merge=false --delete-branch-on-merge
   gh api -X PATCH repos/<owner>/<repo> -f squash_merge_commit_title=PR_TITLE -f squash_merge_commit_message=PR_BODY
   ```

4. Run the stack's checks: `just ready` for Rust, `vp run check && vp run build && vp run test` for JavaScript. They must not leave formatting changes behind.
5. Search for `{{` to make sure no placeholder is left.
6. `diff` every generated file against its template, and check each difference as described in [guide.md](./guide.md#changing-a-template-file).

If a template itself is wrong or outdated, fix it in the `liangmiQwQ/new` repository instead of only patching the generated project.

## Related skills

When you are initializing a project, like handling infrastructure and related data, you are supposed to load `$choosing-tools` skills. You can also use `$global-projects` to find how my other projects use CI and tools. Load `$use-vp-config` for details of the `@liangmi/vp-config` preset in JavaScript projects.

## Aspects of a project

When you are initializing a project, you should care about these aspects:

1. Project layout (single-package, or a workspace, one language or multiple-languages mixed)
2. Basic toolchain (Do not only care about build, care about linting, formatting, testing, git hooks, staging)
3. Package Release (Skip for website, how to trigger, maintenance comment in response, GitHub compatible)
4. CI checking (Add CI checks, including test, build, snap tests, e2e tests, codestyle, linting, formatting)
5. Document placeholder (MIT License or other license as required, basically README.md)
6. Editor settings (`.vscode` folder, format and lint)
7. Scripts (For manually validation, and installing the developing products onto the using computer)
8. Deploy (Websites)
9. Tools version (Node version, Rust version)
10. GitHub repo description, PR merge setting (Squash, Description as message, Auto delete branch)
11. AGENTS.md document
12. `.github/FUNDING.yml`, and Sponsorships button enable settings (only when users has public sponsor profile)

You should prepare them in detail but should not make them too complex, for example, linting CI shouldn't be run on all macOS, Linux and Windows, a small library also doesn't need a VitePress website for docs, `.editorconfig` shouldn't be provided most of the time.
