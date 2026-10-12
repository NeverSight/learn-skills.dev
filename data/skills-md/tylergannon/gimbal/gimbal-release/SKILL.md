---
name: gimbal-release
description: >
  Build and deliver changes to the Gimbal application. Covers development
  priorities, model catalog refreshes, proof, generated frontend assets,
  merge, local installation, and refreshing installed Gimbal instructions.
---

# Build and release Gimbal

Deliver the requested behavior and establish that it works. Gimbal currently
serves agents on this machine; local installation is the distribution target.
For writing a workflow, use [Author workflows](../gimbal-workflows/SKILL.md).
For operating one, use [Use Gimbal](../gimbal-runs/SKILL.md).

## Priorities and working method

Work in the task worktree. Read its `AGENTS.md`, `docs/definition-of-done.md`,
and the relevant requirement. Use Godoc for the API; use research and historical
reviews to understand decisions. Materialize remote requirements locally before
giving their absolute paths to agents.

Keep implementation as simple as the requirement permits. Workflow tactics
stay visible in ordinary Go. Add no unrequested features, compatibility layers,
or abstractions. A hypothetical edge-case concern needs a reasonable actual
failing test before it becomes repair work.

Give agents outcomes and relevant facts. Scope coaches can steer planner,
worker, and validator against over-engineering; they are advisory. Review
findings are assessed against requested behavior rather than automatically
expanding the goal or becoming release blockers.

The repository's completion standard is requested functionality implemented
and seen working. Its 90–95% completion guidance permits deferring remaining
quirks; it does not permit declaring a required failing check successful.
Distinguish unmet requirements and invalid proof from optional improvements.
File genuinely deferred work rather than extending delivery indefinitely.

## Build the application

```sh
just build
```

The current recipe prepares Go and frontend dependencies, runs generation,
formats generated frontend output, builds Svelte, checks that
`web/build/skgo.manifest.json` exists, and builds `bin/gimbal` with `web/build/`
embedded directly using `embed.FS`. Generated frontend files stay local and are
not committed. Run `go install ./cmd/gimbal` only after `just build` in the same
checkout. A bare versioned `go install` does not build or include the console.

Generators own generated files. Regenerate and inspect their diff rather than
patching generated output by hand. Preserve Gimbal-owned application code when
updating a scaffold. Follow the existing application composition so tests and
the built binary exercise the same server.

## Build the macOS workspace

After `just build`, build the native microphone application with
`go tool skgo native build --platform macos --preset real`. Open
`native/build/macos-real/DerivedData/Build/Products/Debug/Gimbal.app` as a macOS
application so macOS attributes microphone and speech permissions to Gimbal.
The `synthetic` preset provides deterministic speech revisions for development.

The shell connects to an independent `gimbal` server on `127.0.0.1:8080` by
default. Start that server separately with the desired `--project` directories;
closing the shell leaves its projects, recordings, and files on the server.
`GIMBAL_SERVER_URL` overrides the shell's server target when supplied at launch.
Project-file storage reuses `uploadArtifact.r2` in `~/.gimbal/config.json`, with
the existing `GIMBAL_R2_*` environment overrides. Metadata retains the bucket
and object key; viewing generates a new temporary URL.

## Check and demonstrate the change

Run required repository checks appropriate to the change:

| Check | Purpose |
| --- | --- |
| `just vet` | Go vet, binary build, and Gimbal lint. |
| `just test` | Go and frontend unit tests. |
| `just fmt-check` | Frontend formatting. |
| `just e2e` after `just build` | Browser behavior against the built binary on an isolated port. Set `BASE_URL` to use an existing server. |

A documentation-only edit needs instruction and link checks. For application
behavior, run the real path the claim concerns: a workflow, separate CLI
processes for external steering, or the browser for a UI change. Use cheap
models for live demonstrations and name the model.

An independent validator inspects the work and whether its evidence establishes
the definition of done. Worker summaries and aggregate green gates cannot
establish unrelated behavioral claims. After relevant checks pass, repeat them
only when a change, failure, or unresolved concern warrants it.

In this repository, repeatable checks belong beside the code they test. Do not
commit proof programs, screenshots, logs, or run output. Describe observations
in the conversation or PR. Other projects using Gimbal retain their own policy
for keeping or sharing evidence.

## Review CLI documentation

For an added or changed built-in, read its rendered help as a caller. It must
explain purpose, inputs, meaningful defaults, outputs or changes, proof and
completion expectations, limits, and a useful example at suitable detail.

The entry function's doc synopsis supplies short help; package documentation
supplies long help; parameter field comments supply flag help. Check the built
command's workflow list and affected workflow help. A graph or output schema
does not document the invocation for its caller.

## Model catalog refresh

Gimbal promises to stay current with the latest models. `just models` (needs
`DIFFUSION_API_KEY`) downloads the models.dev catalog and the Diffusion Router's
`/v1/models`, then regenerates `internal/observation/model_prices_gen.go`,
`internal/modelalias/aliases_gen.go`, and `pi/diffusion_models_gen.go`. The
tracked alias families (haiku, sonnet, opus, fable, luna, terra, sol, astra,
gpt, deepseek-flash, glm, glm-flash, glm-vision) are listed in
`internal/modelcatalog/main.go`; each unversioned alias resolves to the newest
version found, so a new version of a tracked family needs no hand edit. To track
a new family, add a line to that list (a new provider also needs its models
fetched there). The hand-kept exception is Gemini `flash`, in
`internal/modelalias/modelalias.go`.

The scheduled `Refresh model catalog` Actions job runs the same command daily
and can be started manually (`workflow_dispatch`). It reads `DIFFUSION_API_KEY`
from the Doppler config that the repository secret `DOPPLER_TOKEN` grants, then
opens a PR for the generated files; it does not publish a release. The
repository's Actions setting permits bot-created PRs; the job grants only
contents and pull-request write access.

Review new and removed model IDs before merging. Aliases follow the catalog, but
built-in role defaults in `internal/builtin/defaults.json` and other configured
defaults, help, and skills name explicit models: update those to the new version
where it applies, keeping each role's intended model tier. Check the rendered
`gimbal run` role flags, not only the JSON. Tests for aliases should cover
resolution and overrides without fixing a moving shorthand to today's version.

Before tagging a release, build and install from a checkout of the pushed
commit with `just build` and `go install ./cmd/gimbal`, then start its web
listener and confirm it serves the page. After tagging, repeat from a checkout
of the exact tag. A successful install without a served page does not prove
the installed CLI works.

## Merge and refresh the local installation

Commit and push meaningful work; follow repository review and squash-merge
practice within the user's authorized scope. Retain the task worktree when the
user has asked to keep it. Every release must update `CHANGELOG.md`: move the
relevant entries from `Unreleased` under a version heading with the release date,
update comparison links when tags exist, and leave a new empty `Unreleased`
section for subsequent work. Update affected skill and plugin instructions in
their maintained source before merging. After every feature or fix merges,
reinstall both the CLI and the Gimbal skills on this machine:

1. Fast-forward the main checkout and build the merged source with `just build`.
2. Install it with `go install ./cmd/gimbal` from that built checkout.
3. Reinstall the published skills, including their supporting references:

   ```sh
   vp dlx -- skills add https://github.com/tylergannon/gimbal/tree/main/skills \
     --global --agent codex claude-code --skill '*' --yes
   ```

   The source URL scopes discovery to this repository's `skills/` directory;
   using the repository root would also discover internal `.agents/skills`.
   Keep the installer's default symlink mode. Refresh any affected plugin
   through its own installation mechanism as well.
4. Resolve the executable with `command -v gimbal`. Check `gimbal --help`,
   `gimbal run --help`, and affected workflow help; exercise the relevant
   installed behavior when a behavioral change requires it.
5. Compare installed instruction files with their maintained source. A
   successful install command alone does not establish that the copies match.

The maintained skill source is `skills/` in this repository.
The shared local installation location is `~/.agents/skills/`. The Gimbal set is
`gimbal`, `gimbal-workflows`, `gimbal-release`, and `gimbal-runs`. For an affected
plugin, inspect its actual installation and use its update mechanism; preserve
unrelated local configuration. Report when a new session is needed to load
updated instructions.

Local release needs no binary signing or scalable distribution system. The
documentation site is maintained in Gimbal View. The scheduled model-catalog
PR has its own scope; it does not imply a general CLI publishing pipeline.

## Report delivery

State the behavior observed, relevant checks, merge status, installed binary
path, and which installed instructions were refreshed. Separate local proof,
merged source, and installed behavior. Name unmet requirements and deferred
issues plainly.
