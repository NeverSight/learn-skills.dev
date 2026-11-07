---
name: genesis-cicd
description: Use when adding GitHub Actions CI/CD to a project scaffolded with genesis (services/<app>-server Go API, services/<app>-web pnpm React app). Asks which CD target (Railway, Kubernetes, VM + Overwatcher) and which branch model (main = production, or main = staging + release = production), then writes one ci.yml wired with needs so GitHub renders a single pipeline graph.
user-invocable: true
disable-model-invocation: true
argument-hint: "[railway | kubernetes | overwatcher] [main-prod | release-prod] [sticky-disk]"
---

# genesis-cicd

Adds one `.github/workflows/ci.yml` to a genesis monorepo. Railway and Overwatcher templates live in [reference.md](reference.md); Kubernetes uses [kubernetes.md](kubernetes.md) with the external `lwlee2608/release-manifest` actions.

- Kubernetes: after `changes -> resolve`, independent `server -> build-server-image` and `web -> build-web-image` paths join at `publish -> deploy`.
- Overwatcher: after `changes`, independent `server -> build-server-image` and `web -> build-web-image` paths; external deployment requires both builds to succeed.
- Railway: `changes -> server/web`.

## Question flow

1. **Read the arguments first.** `railway`/`kubernetes`/`overwatcher` is the CD target; `main-prod`/`release-prod` is the branch model; `sticky-disk` opts into Blacksmith's paid Docker cache. Ask only what is missing.
2. **Ask the rest in ONE AskUserQuestion call:**
   - CD target: `railway (Recommended)` | `kubernetes` | `overwatcher` (VM running Docker Compose, deployed by the Overwatcher GitHub App)
   - Branch model: `main = production (Recommended)` | `main = staging, release = production`
   - Docker layer cache, only for `kubernetes`/`overwatcher`: `GitHub Actions cache (Recommended)` — free | `Blacksmith sticky disk` — $0.50/GB/month, also persists `RUN --mount=type=cache`
3. **Resolve target prerequisites before writing.** For Kubernetes, inspect the chart and collect missing GCP project, cluster locations, namespaces, release names, and environment values paths. Require chart support for complete digest references, not tag-only image construction. The canonical scaffold has no Helm chart: if one is missing, stop and ask whether to create it as a separate prerequisite or choose another target. Verify a published commit of `lwlee2608/release-manifest` and pin both actions to it; until available, report the dependency blocker rather than invent a version. Do not leave deployment placeholders in a generated workflow.
4. **Confirm in one sentence, then write.** Example: "kubernetes, main→staging / release→prod, GCR, GHA cache — proceed?"

## Rules

1. **Read the target project first.** Confirm service dir names, `make test` in the server Makefile, `packageManager: pnpm@…` plus `pnpm-lock.yaml` in the web. Set `pnpm/action-setup`'s `package_json_file` to the service-local file; `defaults.run.working-directory` does not affect actions. For Kubernetes, validate `Chart.yaml`, environment values files, and both image-reference keys against the images being published. Never leave `project-00`.

2. **One workflow file, jobs joined by `needs:`.** A second workflow chained via `workflow_run` breaks the Actions graph, checks out the default-branch tip unless you pass `head_sha`, and fires for both the push and PR run of the same commit.

   Cancel superseded PR runs only. Give push runs distinct concurrency groups so an irrelevant push cannot cancel or displace a pending relevant build. Serialize Kubernetes publication per release track and Helm jobs per deployment target without cancelling active jobs. One publishing workflow owns each track because `github.run_number` is workflow-scoped. Publication and deployment are separate operations; the action does not guarantee deployment order.

3. **One test job per service.** For Railway/Overwatcher and Kubernetes PRs, filter suites through `changes` (`dorny/paths-filter`). Grant it `contents: read` and `pull-requests: read`; use `base: ${{ github.ref }}`. Service changes run that suite; changes to `ci.yml` run both. Exclude documentation in these job filters, not the workflow trigger: both `paths:` and `paths-ignore:` can leave required PR checks pending. `changes` also reports deployment relevance; include actual chart/values paths and shared inputs. Kubernetes pushes instead test every image requested by `resolve`, including changes not yet published after a failed build. Explicit job status gates must allow PR tests when `resolve` is intentionally skipped.

4. **Gate downstream work on relevance and successful prerequisites, not skipped tests alone.** Overwatcher builds both images when relevant, or on every release push, in independent `build-server-image` and `build-web-image` jobs. Each needs only `changes` and its own suite (plus optional store for server); retain the base relevance and release-test skip policy. A failed suite or image build does not block the other image path, but external deployment requires both image jobs to succeed. Kubernetes runs `resolve` on every eligible push, compares caller-computed fingerprints with that track's published baseline, and builds only requested images. Each image job requires successful resolution and its own suite, independently of the other suite. `publish` requires successful change detection/resolution, relevance (requested builds, deployment changes, or a release push), success for each requested image job, and skipped status for each unrequested image job. Both image jobs skip with no requested builds; Helm changes and release pushes still publish retained references. A failed suite can leave the other image already pushed, but publication is blocked. Optional store tests gate only `build-server-image`; publish enforces them through that build's success. `deploy` requires publication success. Never let PRs publish or deploy.

5. **Branch model:**
   - `main-prod`: `push: branches: [main]` + `pull_request`.
   - `release-prod`: `push: branches: [main, release]` + `pull_request`. Kubernetes uses `staging` on main and `production` on release. Merging main into release automatically tests/builds changed images from the release commit and deploys production; unchanged production digests are retained. No manual dispatch, `source-release`, or staging-image promotion is added. For Railway/Overwatcher, retain the base release-test policy: only skip after confirming a protected, successfully tested main tree; otherwise run all suites on release pushes. Do not path-filter release pushes.

6. **CD target:**
   - `railway`: no image-build jobs, no deploy job. Railway builds from the Dockerfile on push; under `release-prod` point its production environment at `release` and staging at `main`. Configure Wait for CI and service watch paths separately; skipped GitHub jobs alone do not suppress Railway deployments. See the reference checklist for promotion exceptions.
   - `kubernetes`: use the complete Kubernetes reference, not the base GHCR workflow plus a Helm tail. GCR stores images; GitHub Release assets in the application repository store manifests. A track-aware `deploy` job runs Helm with both complete digest references from the successful publish action's `manifest` output. Under `main-prod`, main targets production; under `release-prod`, main targets staging and release targets production. Preserve the production environment gate.
   - `overwatcher`: images to GHCR, no deploy job. Also write `docker-compose.prod.yml` and `.env.example` from the reference; the genesis scaffold has no prod compose. Use the `overwatcher` skill for owctl setup. Set the service's Workflow field to `ci.yml`. Overwatcher deploys only successful runs on the service's branch; a failed image job fails the run, and a no-op run re-pulls the unchanged branch tag.

7. **Never deploy shared `latest`.** Overwatcher deploys a fixed tag per service, so the compose pins the deploy branch tag; image jobs still push SHA tags for traceability and manual rollback. Kubernetes uses unique run/attempt build tags only to push, then records/deploys `repository@sha256:...`. Fingerprints cover the full service context, workflow, and all build inputs/arguments. Use a stable build-input commit for server `COMMIT_SHA` and include it in the fingerprint, not the current unrelated workflow SHA. Whole-context docs can trigger rebuilds; root docs outside build inputs do not. Do not copy the abandoned Python release manager into generated projects.

8. **Blacksmith runners:** `blacksmith-4vcpu-ubuntu-2404` for `server`, `build-server-image`, and `build-web-image` on both image-building targets; `blacksmith-2vcpu-ubuntu-2404` elsewhere. Keep upstream `actions/setup-go` / `actions/setup-node` with `cache` on; Blacksmith accelerates the GitHub cache API transparently and its `useblacksmith/setup-*` wrappers are deprecated.

9. **Docker layer cache: `type=gha`, one scope per image, unless the user chose `sticky-disk`.** `useblacksmith/setup-docker-builder` + `useblacksmith/build-push-action` keep the builder on a sticky disk billed per GB; never add them for "speed" without the user opting in, and never mix the two approaches in one job. For Kubernetes and Overwatcher, replace the builder in each image job and use separate sticky cache keys `<app>-server` and `<app>-web`; job gates make per-step requested-image conditions unnecessary.

10. **Never commit secrets.** GHCR uses `GITHUB_TOKEN` with `packages: write` only on `build-server-image` and `build-web-image`; test jobs remain read-only. Kubernetes grants `contents: write` only to `publish`; resolution needs `contents: read`. GCR/GKE need a service-account JSON the user adds in repo settings. Kubernetes registry-auth jobs export scalar digests, not JSON: multiline secret masking can suppress JSON job outputs. Assemble newly built refs in publish's `images` step; the publish action supplies retained refs.

## Verification procedure

1. Run `actionlint .github/workflows/ci.yml`, configuring its allowed self-hosted runner labels for Blacksmith. A YAML parser is only a syntax fallback, not validation of Actions expressions or dependencies; report when actionlint was unavailable.
2. `grep -n project-00 .github/workflows/ci.yml` returns nothing.
3. Run the same steps locally: `go vet ./... && make test`; `pnpm install --frozen-lockfile && pnpm lint && pnpm build`.
4. Verify the selected target's single job graph. Kubernetes PR tests must work with skipped resolve; all write/deploy jobs must skip. Do not claim live verification without an observed Actions run.
5. Kubernetes: verify bootstrap builds both and each image starts after its own suite without waiting for the other. A server-only change retains web; Helm-only changes skip both image jobs but publish/deploy retained digests. An unrelated push retries unpublished changes after a failed build. Healthy root-docs-only main pushes skip both image jobs and do not publish/deploy. Failed/cancelled requested suites or builds block publication even if the other image was pushed. Check scalar digest outputs and publish-side JSON assembly, both cache variants with separate per-image caches, and optional store gates that block only the server build and publication, not web.
6. Kubernetes `release-prod`: merging main into release automatically uses the production baseline, tests/builds requested release-branch images, and deploys both published digests. Verify the no-new-images release path and publication/Helm failure recovery in `kubernetes.md`.
7. Railway/Overwatcher: retain the reference's behavior checks, including both-image SHA builds for Overwatcher and external no-op/deployment configuration. Verify each image starts after its own suite without waiting for the other; a failed suite/build or optional store failure does not block the other image path, but prevents deployment. Check PR/no-op skips, release builds with intentionally skipped checks, and separate per-image caches. Do not infer external CD behavior from GitHub job skips.

## Common mistakes to watch for

- **Using only the previous-commit diff for Kubernetes builds** - changes from a failed build would disappear on the next unrelated push; compare against the published manifest instead.
- **Accepting skipped requested tests** - skipped must mean an intentionally retained image, not a failed dependency.
- **Deploying both images with the current SHA in Kubernetes** - unchanged images retain older digests, not the current commit's tag.
- **Using workflow-level `paths:` or `paths-ignore:` on PRs** - required PR checks never report and block merging.
- **Treating workflow success as proof images were published** - no-op and PR runs can succeed with image jobs skipped; Kubernetes Helm-only and no-new-images release pushes can publish retained refs with both image jobs skipped.
- **Writing a deploy job for Railway or Overwatcher** — both deploy on their own; a helm/ssh job would fight them.
- **`npm ci` for the web** — ignores `pnpm-lock.yaml`.
- **Sharing one `type=gha` scope between server and web** — each build evicts the other's layers.
