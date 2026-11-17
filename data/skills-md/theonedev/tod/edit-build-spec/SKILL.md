---
name: edit-build-spec
description: Author, update, and validate a OneDev CI/CD build spec in .onedev-buildspec.yml.
---

# Edit a OneDev build spec

Use configured `tod` from the OneDev repository root.

1. Read the server schema with `tod build get-spec-schema`. If
   `.onedev-buildspec.yml` exists, run `tod build check-spec` before editing.
   It can rewrite the file to upgrade its schema. Read the resulting file
   and use any validation errors to guide the edit.
2. Inspect the relevant project files for tool versions, images, and
   commands. Apply the requested changes to `.onedev-buildspec.yml`.
3. Run `tod build check-spec` on the final spec and correct validation errors.

## Jobs and steps

- Add a checkout step when a job needs repository files.
- Run new command steps in a container by default. Preserve an existing
  step's execution mode unless the requested change requires a different one.
- Steps share the job working directory. Keep setup and commands that need
  its installed tools in one step unless you persist those dependencies in
  the working directory.
- Put cache setup before build or test steps that use it. Use dependency
  lockfiles as checksum inputs when available, and set the upload strategy
  to `UPLOAD_IF_NOT_HIT` for that cache.
- To pass files between jobs, publish them with a publish-artifact step and
  retrieve them through a job dependency.
