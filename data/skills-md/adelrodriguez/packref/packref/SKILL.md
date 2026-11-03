---
name: packref
description: Inspect the exact dependency source referenced by a Packref project. Use when tracing package implementation, debugging exact-version behavior, comparing referenced versions, restoring missing source references, or working with Packref commands.
---

# Packref

Use Packref to inspect the exact dependency source that a project references. Do not substitute
documentation, another installed version, or an arbitrary repository revision. Packref materializes
package source references for inspection. It does not install runtime dependencies.

## Project state

Commit `.packref/packref-lock.json` so other users can restore the same package source references.
Keep `.packref/packages/` ignored by Git. This project source directory is local to each developer.
Multiple versions can coexist; the Packref lockfile records the full set of package identities.

## Inspect a package

1. Find `.packref/packref-lock.json`. If it exists, run `npx -y packref list` to review the current
   references. If it does not exist, explain that the project is not initialized. Run
   `npx -y packref init` only when the user authorizes initialization.
2. Read the Packref lockfile and select the required package identity. Match the `registry`, package
   `name`, and exact `version`. Record its `tracking` mode and `source` metadata. If the lockfile has
   multiple versions, select the version required by the task.
3. Check whether the matching package source reference exists:
   - Unscoped package: `.packref/packages/<registry>/<package>/<version>/`
   - Scoped package: `.packref/packages/<registry>/<scope>/<package>/<version>/`

   Keep the leading `@` in `<scope>`.

4. If the lockfile contains the package identity but the reference is missing, run
   `npx -y packref install`. This command restores all locked references without changing the lockfile
   or installing runtime dependencies.
5. If the lockfile does not contain the package identity, run `npx -y packref add <package-spec>` only
   when the task includes obtaining that source. For a registry package, add `@<version>` when the
   task requires an exact version; otherwise, Packref can follow the project's resolved manifest
   dependency. For a repository source, use a repository spec such as `adelrodriguez/packref` with an
   optional `@ref` (tag, branch, or full 40-character commit SHA). Without a ref, Packref pins the
   default branch commit. Read the updated lockfile before inspection.
6. Search the package source reference with local tools such as `rg` and `rg --files`. Start at the
   named public API or package exports. Follow imports until you reach the implementation that
   answers the question.
7. Report the package identity and cite the relevant project-local paths. Separate facts verified
   in the source from inferences.

When `source.directory` is present, the package source reference already starts at that package's
subdirectory. Treat `source.directory` as repository provenance. Do not append it to the local path.

## Command boundaries

Use `npx -y packref <command>` to skip the npx install confirmation prompt.

- `npx -y packref init` initializes a project. Run it only with user authorization. It can update
  `.gitignore`, `tsconfig.json`, `AGENTS.md`, the Packref lockfile, and Packref's global project
  registration. Without flags it prompts interactively; agents should run
  `npx -y packref init --non-interactive`, adding `--ignore` to update `.gitignore` and the TypeScript
  exclude list and `--agents` to write the `AGENTS.md` guidance section. `--ignore` and `--agents`
  fail without `--non-interactive`.
- `npx -y packref add [package-spec]` resolves and materializes a missing reference. The spec is a
  registry package with an optional exact version (`hono`, `hono@4.2.0`) or a direct repository
  spec (`adelrodriguez/packref`, `owner/repository[/directory][@ref]`, `github:`/`gitlab:`/`bitbucket:`/
  `sourcehut:` shorthand, a standard Git URL, or an SCP-style SSH URL). Without a package spec,
  it opens an interactive dependency selector.
- `npx -y packref list` shows all package source references recorded in the Packref lockfile.
- `npx -y packref install` materializes every reference recorded in the committed Packref lockfile.
- `npx -y packref sync` reconciles dependency-tracked references after changes to the manifest or
  package-manager lockfile. It can update or remove references.
- `npx -y packref remove [package-spec]` removes references. Run it only when the user requests
  removal.
- `npx -y packref prune` removes unused source snapshots from the global store.
- `npx -y packref clean` removes all project-local package source references.
- `npx -y packref clean --global` removes all source snapshots from the global store.
  Run `prune` and either form of `clean` only when the user explicitly requests that removal scope.

## Examples

- For `@effect/platform@0.90.0`, match its lockfile entry, then inspect
  `.packref/packages/npm/@effect/platform/0.90.0/`.
- If `npm:react@19.1.0` is locked but its reference is missing, run `npx -y packref install`, then
  inspect `.packref/packages/npm/react/19.1.0/`.
- If `hono` is not in the lockfile, run `npx -y packref add hono` only when the task includes obtaining
  its source. Read the resulting package identity and source metadata from the updated lockfile.
- If both `npm:hono@4.2.0` and `npm:hono@4.3.0` are locked, inspect the version required by the task.
  Inspect both only for a version comparison.

## Failure and fallback

If a command fails, read the error first. Check project initialization, the package identity, the
lockfile entry, and network access. Use registry metadata or web research only when Packref cannot
materialize the exact source. State this limitation and identify which findings come from fallback
evidence.
