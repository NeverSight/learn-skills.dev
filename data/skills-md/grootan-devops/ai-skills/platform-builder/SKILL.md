---
name: platform-builder
description: >-
  Unified platform engineering skill for CI/CD, packaging-only Dockerfiles, and Helm charts
  across GitLab CI and GitHub Actions. Detects which platform a repository targets, then
  scaffolds, migrates, and audits pipelines with least-privilege tokens, adaptive workflow
  selection, and a shared Docker/Helm contract. Use for onboarding a repo to CI, migrating
  library versions, or auditing pipeline, Dockerfile, and chart compliance.
---

# Platform Builder — GitLab CI & GitHub Actions

Generates, standardises, and audits **CI pipelines**, **packaging-only Dockerfiles**, and
**Helm charts** on either platform.

**The Docker and Helm contracts are identical on both platforms; only the CI layer differs.**
That is why this is one skill rather than two: roughly 62% of the rule engine and 98% of project
detection are platform-independent, and keeping them in one place is what stops them drifting
apart.

---

## 0. Reference Index — Load Before Acting

Load the core reference, then the addendum for the **detected** platform. Never load both
platforms' references; they will contradict each other by design.

| Load | Before you… |
| --- | --- |
| `core/references/security-core.md` | Write or audit a chart, Dockerfile, or credential handling. **Required for every onboard and audit.** |
| `core/references/language-stacks-core.md` | Scaffold build/test jobs for any stack. |
| `core/references/helm-chart-standard.md` *(shared)* | Create or modify a chart, `values.yaml`, or `values.schema.json`. §2.1 is required before naming any container, sidecar, init container or job container. |
| `core/references/file-mounts-standard.md` | The app needs a config file at runtime (nginx.conf, `application.properties`, certs). **Check this on every chart.** |
| `core/references/ignore-files-standard.md` *(shared)* | Write or audit `.gitignore`, `.dockerignore`, or `.helmignore`. The three have different semantics; `.helmignore` is read by the chart loader, so a wrong entry breaks the build rather than bloating it. |
| `core/references/migration-standard.md` *(shared)* | Run an update or apply a version migration. |
| `platforms/<platform>/references/security-addendum.md` | Anything security-related, after the core. |
| the resolved library's own `README.md` (§0.0) | **Write the actual CI YAML.** Its module catalog, inputs and worked examples are the contract. The skill keeps no copy of them. |
| `platforms/gitlab/references/stack-snippets.md` *(GitLab only)* | GitLab wiring the README does not cover: `extends:` order, `PROJECT_CACHE_KEY`, never overriding `image:`. |
| `platforms/<platform>/references/workflow-matrix.md` | Decide which workflows/options a repo declares. |
| `platforms/<platform>/workflow-map.json` | The machine-readable map. Loaded by the engine; never transcribed. |

Every reference above except the library README is a real file inside this skill. The skill is
self-contained by design: `npx skills add <repo> --skill platform-builder` copies this directory and nothing
else, so a symlink pointing outside it would install as a broken link.

### 0.0 Reference Libraries

The skill carries **no copy** of what these do. Read each library's own `README.md` and
`MIGRATION.md` at the resolved version, **every onboard, update, and audit**.

| Library | Provides |
| --- | --- |
| `gitlab-ci-library` | GitLab CI template modules — `WORKFLOW` options, job/stage tables, publishing & auth |
| `github-ci-library` | GitHub reusable workflows — module catalog, scenario files, execution matrix |
| `helm-tpl-library` | the `tpl-library` Helm library chart — values contract, `mounts:` schema, template helpers |

If you are about to write a fact that already lives above, **write a pointer instead**. A second
copy is a second thing to forget, and copies drift silently.

#### Resolving which copy to read

Reading a library "fresh" is only meaningful once the run knows *which* copy. Resolve it
first, and never guess:

```bash
python3 core/scripts/libraries.py [repo] --platform gitlab|github
```

Each library has a named flag — `--gitlab-ci-library`, `--github-ci-library`,
`--helm-tpl-library` — accepted by `libraries.py` and `audit.py` alike. `--lib NAME=SOURCE`
does the same thing generically.

A source is a local path, a git URL with an optional `@<ref>`, or the web URL you get from a
browser address bar:

| Source | Means |
| --- | --- |
| `/abs/path/github-ci-library` · `~/lib/x` · `../x` · `file:///srv/x` | local working copy, **read in place** |
| `https://github.com/org/repo` | git, default branch |
| `https://github.com/org/repo/tree/dev` | git at a branch, web URL form |
| `https://github.com/org/repo/tree/e7c31d0…` | git at a commit, web URL form |
| `https://gitlab.com/org/repo/-/tree/1.0.0` | same, GitLab's `/-/tree/` form |
| `https://host/g/repo.git@1.0.0` · `@main` · `@6de3e62` | git at a tag, branch or commit |
| `git@host:g/repo.git@1.0.0` | scp-style URL plus tag |

A `/tree/<ref>` URL takes everything after `tree/` as the ref, so a branch containing a slash
works. Otherwise only the last `@` **after** the last `/` introduces a ref — so `git@host:`
and `https://user:token@host/` parse correctly — except that `.git@` always splits, which is
how `repo.git@feature/x` works. `#` is an alternative separator.

Precedence — highest first, and per library, so one may be local while another is pinned:

| # | Layer | Use for |
| --- | --- | --- |
| 1 | `--<library-name> SOURCE`, or `--lib NAME=SOURCE` | this run only — testing an unreleased library |
| 2 | `$PLATFORM_BUILDER_LIB_<NAME>` (`-` → `_`, upper-cased) | a whole shell session or CI job |
| 3 | `<repo>/.platform-builder.json` → `{"libraries": {...}}` | the repo's own pin, committed with it |
| 4 | `core/libraries.json` | the org default |

Git sources are cloned once into `~/.cache/platform-builder/libraries`
(`$PLATFORM_BUILDER_CACHE` overrides). Only a full 40-character commit SHA is served from
cache untouched; a branch moves, a tag can be force-pushed, and a short hex ref may be a
branch that merely looks like a SHA, so all three are re-fetched. `--refresh` re-clones.

**Three rules the resolver enforces, and you must not talk your way around:**

1. **A local source is read in place, never copied.** That is the point — an uncommitted
   working copy is visible to the run. When the resolver reports `UNCOMMITTED CHANGES`, say
   so in the confirmation table: you are generating against a state no pipeline can consume
   until it is pushed and tagged.
2. **A ref on a local path is refused, not ignored.** Checking one out would mutate the
   user's tree. Drop the ref, or point at the git URL.
3. **An unusable source stops the run.** Do not scaffold against a library you could not
   read; report it and ask.

Report the resolved `name @ ref (kind, via layer)` for every library in the Phase 2
confirmation table. An audit whose library provenance is unstated cannot be reproduced —
half its findings depend on the version the repo was measured against.

#### The ref you scaffold with is the ref you resolved

**Every generated `uses:` and every `include: ref:` carries the ref the resolver reported —
never a version copied out of a README example.** Those examples write `@1.0.0` to show the
shape; writing it into a consumer pins the pipeline to a tag that may not exist. A caller
pinned to a ref the library has never published fails to resolve, and the error names the
caller, not the mistake.

| Resolved as | Write |
| --- | --- |
| a tag — `@1.0.0` | that tag |
| a branch — `@dev` | that branch |
| a commit | that SHA |
| a **local path** | the branch that copy is checked out at |

A local path deserves care. GitHub cannot consume `/Users/me/lib`: the generated workflow
has to name the library on its remote, so use the branch the local copy sits on and say so.
Two things then need stating rather than assuming:

- **Uncommitted changes.** The resolver warns when the working copy is dirty. The pipeline
  will run against what is *pushed*, not what you read. Say which, and let the user decide.
- **No such ref upstream.** If the local branch has never been pushed, the scaffold cannot
  work yet. Say so at Phase 2, before writing — not after.

Check before you write: `git -C <library> tag --list` and `git -C <library> status
--porcelain` answer both questions in one step.

### 0.1 Single-Source Law

Every fact has one home. When two places disagree, the one listed here wins — never reconcile
by copying.

| Fact | Single source |
| --- | --- |
| Module/workflow → option mapping | `platforms/<platform>/workflow-map.json` |
| Helm chart structure, values contract, schema | `core/references/helm-chart-standard.md` |
| Stack requirements (what and why) | `core/references/language-stacks-core.md` |
| Stack YAML (how) | the resolved library's `README.md`; GitLab-only wiring in `platforms/gitlab/references/stack-snippets.md` |
| Security principles | `core/references/security-core.md` |
| Platform security mechanics | `platforms/<platform>/references/security-addendum.md` |
| What a shared CI/Helm library does, and its migration steps | that library's own `README.md` and `MIGRATION.md`, **re-read every run** |
| How a file mount is declared and classified | `core/references/file-mounts-standard.md` |
| What each ignore file must and must not contain | `core/references/ignore-files-standard.md` |
| Which copy of a library a run reads | the precedence chain in §0.0, resolved by `core/scripts/libraries.py` |

### 0.2 Minimal-Change Law

**Read before you write. Change the minimum. Justify every edit.**

Except on an empty repository these commands are *editors*, not generators. A working pipeline
someone tuned by hand is the artefact of record; regenerating it discards that work and produces
an unreviewable diff.

1. **Read the existing files first.** Never write one you have not read.
2. **Diff intent against reality.** What actually differs from the standard is your entire change set.
3. **Preserve deliberate deviation.** A pinned SHA, an extra job, an unusual condition, a
   `when: never` override — assume it was intentional and ask before removing it. "It differs
   from the template" is not a reason.
4. **Preserve formatting** — key order, comments, quoting, blank lines.
5. **Justify each edit in one line**, tied to a rule or migration step.
6. **Never fork a shared template or reusable workflow** to change one line.
7. **When in doubt, propose rather than apply.** Audit never writes.

---

## 1. Platform Detection — Always First

```bash
python3 core/scripts/platform.py [repo]
```

Signals, ranked by how directly they express *intent* rather than hosting:

| Rank | Signal | Confidence |
| --- | --- | --- |
| 1 | caller passed `--platform` | explicit |
| 2 | `.gitlab-ci.yml` or `.github/workflows/` committed | certain |
| 3 | `$GITLAB_CI` / `$GITHUB_ACTIONS` in the environment | certain |
| 4 | origin host contains "gitlab"/"github" | **likely — still confirm** |
| 5 | neither, or **both** | ambiguous → **ask** |

> **Hostname is never a verdict.** Self-hosted is the norm: `gitlab.contoso.com` happens to
> contain "gitlab", but a GitLab instance at `scm.internal` or GitHub Enterprise at
> `git.company.com` carry no hint at all. When the host is inconclusive, probe
> `/api/v4/version` (GitLab) or `/api/v3` (GHE), or ask.

**Two cases are choices, not detections, and must route to a question:** a repo with **both**
config types (mirrored, or a migration in flight), and a repo with **neither** during onboard —
where a repo is *hosted* is not always where its CI should *run*.

---

## 2. Commands

| Command | Purpose |
| --- | --- |
| `platform onboard [repo]` | Scaffold CI, Dockerfile, and chart for a repo that has none. |
| `platform update [repo]` | Migrate to current standards, applying only what is required. |
| `platform ship [repo] <env>` | Add deployment wiring for a target environment. |
| `platform audit [repo]` | Read-only compliance and security audit. |

Every command accepts library sources on the same syntax as §0.0, e.g.
`platform onboard ./svc --github-ci-library https://github.com/grootan-devops/github-ci-library/tree/dev --helm-tpl-library /path/to/helm-tpl-library`.

### 2.1 Interactive Protocol — Never Scaffold Silently

**Phase 1 — Context.** Detect the platform. Then resolve the library sources (§0.0) and read
each library's `README.md` and `MIGRATION.md` **fresh every run** from the resolved path — they
change between runs, and stale assumptions produce wrong pipelines. Never answer from memory,
and never read a library the resolver did not hand you a path for.

**Phase 2 — Classify and confirm.** Run the engine to get the detected shape, then present:
platform (with confidence and signals), shape, what will be created, and anything present that
the shape does not need. **Stop and confirm before writing.**

**Phase 2b — Ask about tests. They are off by default, so silence disables them.**

Both libraries ship the jobs; neither runs without being asked for. A scaffold that omits
them is not "no tests yet", it is a pipeline that builds an artifact nobody executed.

| Present | Ask | Turns on |
| --- | --- | --- |
| a `Dockerfile` | "Smoke-test the built image?" | `docker.yml` (or `buildah.yml`) `test: true`. Runs `test-script` — default `ci_image_test.sh` — inside the image before it is pushed. GitLab: `.Image:Test`. |
| a chart | "Unit-test the chart?" | `chart.yml` `run-unittest: true` with `mock-chart` (default `test`). Runs `helm unittest` against a mock consumer chart. |

Ask for each artifact that exists, and ask **both** where both exist — they are independent
decisions. If the repository already ships the script or the mock chart, say so and default
to enabling; a test that exists and never runs is the worst of the three outcomes.

If the answer is yes and the fixture does not exist yet, scaffold it:

- **Image** — a `ci_image_test.sh` that asserts what the image promises: the binary is on
  `PATH` and reports the expected version, the declared `EXPOSE` port is listening, the
  process runs as `10001`. Assert the contract, not the base image's contents.
- **Chart** — see the scope rule in **helm-tpl-library's own README**. `tpl-library` already
  tests the Kubernetes-level rendering it owns, and duplicating that in a consumer chart
  buys nothing and breaks on every library upgrade. A consumer's tests cover what only that
  chart knows.

**Generated YAML carries no narration.** A comment in a consumer's pipeline earns its place
only by preventing a specific mistake — why a job accepts a skipped dependency, why a value
must not be re-declared. Explaining what a workflow *is*, or how it differs from another
one, is what this skill's references and the library README are for; repeated into every
generated file it becomes something to maintain and, on the next library change, something
that is quietly wrong. Applies to both platforms.

**Phase 3 — Scaffold, then validate.**

```bash
python3 core/scripts/audit.py [repo] --strict [--lib NAME=SOURCE ...]
```

Pass the same `--lib` sources you scaffolded against, so the validation measures the repo
against the library it was built for.

---

## 3. Standards

### 3.1 Adaptive Selection

A repository declares **only the CI it can actually execute**. On GitLab that means the
`WORKFLOW` option list matching the `include:` list; on GitHub it means only the workflow files
the shape needs. Either way an option or file with nothing behind it produces an empty pipeline
— a dead button for whoever clicks it. See the platform's `workflow-matrix.md`.

A Dockerfile without an application dependency manifest is an **image-only** repository. Give
it image build, smoke-test and image-scan coverage, but no source dependency-license scan, source
SBOM workflow, language build, or SonarQube workflow. Those concerns become applicable only when
a supported application manifest exists. Git-history secret scanning remains applicable.

Do not schedule placeholder jobs for absent repository features. Build a matrix from detected
files before job expansion so a repository without a Dockerfile or chart has no Dockerfile or
chart job in its run graph. On GitHub, direct public registry image references are valid and
`CI_DEPENDENCY_PROXY_GROUP_IMAGE_PREFIX` must not be generated or passed; that variable is
GitLab-only. The candidate image repository is resolved once, by the library's `init.yml`, which
normalises a path-style development suffix to a tag-style one on registries with no nested
repository paths (`<repo>/dev` becomes `<repo>-dev` on Docker Hub). Never ask a consumer to pick
the suffix per registry, never hand-write a dev repository in a caller, and never add a
validation rule for it — consume `needs.init.outputs.image-dev-repository`. A GitHub image scan pulls the pushed image from the
registry by its digest-pinned reference; do not save, upload and download an
image tar between jobs. That is a GitLab artifact-passing idiom, and on GitHub
it only adds a slow upload of something the registry already holds. Pin the
runner label (`vars.CI_RUNNER || 'ubuntu-26.04'`) rather than tracking
`ubuntu-latest`, so a platform migration cannot change the build environment
underneath a release. A pipeline change must verify itself
without releasing itself: a PR workflow that filters paths always includes `.github/**`, and the
release workflow on the default branch always carries `paths-ignore: [".github/**"]` so a
workflow-only commit cannot cut a release. A release workflow may carry a `workflow_dispatch`
trigger, but it must then refuse any ref that is not the default branch: GitLab
forbids a manual release outright (`.release-rules` sends `web`/`api` pipelines
to `when: never`), and a GitHub dispatch is looser still because it can target
any ref, so without that guard a release can be cut from a feature branch.

### 3.2 Job Grouping

One concern per workflow/dispatch mode: checks are existence and drift assertions; lint is
linters; build is dependencies → build → test; publish is publish. A job running outside its
class is a defect to report.

### 3.3 Job Wiring

Every job declares its dependencies explicitly. The platform-specific trap differs and both are
in the snippets: GitLab requires an explicit `optional:` on every `needs:` entry; GitHub has no
`optional:` at all, so cleanup jobs must declare `if: always()` or they are skipped exactly when
needed.

**Nothing runs once its input is known to be bad.** Wire `needs:` so a job starts the moment its
own inputs exist and never after a failed dependency; stage ordering alone gives neither. Runner
minutes are real money and real feedback latency, and a pipeline that keeps going after a failure
teaches people to ignore it.

Audit every edge for **both** directions of waste:

| Symptom | Fix |
| --- | --- |
| Work that runs when it cannot succeed | add the missing `needs:` edge |
| Work that waits when it needn't | remove the edge — a job that reads none of an upstream's artifacts must not wait on it |
| A ~10s job blocked behind a whole stage | declare `needs:` instead of relying on stage order |
| A gate that serialises work which could overlap | move the gate later, to the first job that must not proceed |

The last is the one most often got wrong in the safe-looking direction. Gating the *build* on unit
tests stops nothing shippable and costs the whole test duration on every run; gating the *push*
costs nothing and still lets nothing ship untested. Place a gate where it stops waste earliest
**without** serialising work that could have run concurrently.

### 3.4 Least-Privilege Tokens

Prefer the short-lived job-scoped token (`CI_JOB_TOKEN` / `GITHUB_TOKEN`) over any long-lived
credential, and scope it to the minimum. Cross-project publishing needs an explicitly granted
credential — if it "just works", something is over-permissioned. Mechanics differ per platform;
see the addendum.

### 3.5 Docker & Helm

Identical on both platforms — `core/references/language-stacks-core.md` §3 and
`core/references/helm-chart-standard.md`.

Two rules that are broken often enough to name here:

- **Dependencies are cached, never artifacted.** No `node_modules/`, `.venv/` or `vendor/`
  in an `artifacts:` block, ever. The image installs *offline* from the package cache,
  bind-mounted by BuildKit. Compiled output (`dist/`, `*.jar`, a binary) is the artifact.
  Wiring: the library's own README, plus `platforms/gitlab/references/stack-snippets.md`.
- **A consumer `values.yaml` is a replica of the library's**, not a subset — every key
  kept, empty ones included, with their examples. Consumer-only keys live under one
  `Application Configuration` banner. `helm-chart-standard.md` §3.0.
- **`main` is used exactly once per `values.yaml`** — as `containers.main`, the single
  application container. Never as an init container key, and never as a `jobs:` container
  key; `tpl-library` fails the render on both. A `cronjobs:` entry is different: it reuses the
  root `containers:`, so `main` appears in its pod by design. Every other key is
  **derived, not
  looked up**: name the role this container performs in this chart, such that the key would
  survive swapping the image and reads correctly after the component prefix
  (`order-backend-<key>`). Vendor names (`alloy`, `envoy`, `pgbouncer`) and placeholders
  (`sidecar`, `helper`, `aux`) are always wrong. Init keys name a completed precondition.
  `helm-chart-standard.md` §2.1 has the four-question test and worked examples.

### 3.6 File Mounts

**Assess on every chart.** Any file the application reads at runtime — `nginx.conf`,
`application.properties`, `appsettings.json`, a certificate — is declared in `values.yaml` under
`mounts:`, not baked into the image and not hand-written as a ConfigMap template.

Three decisions, all confirmed with the user, never inferred silently:

1. **Does the app need one?** Check the stack's usual config file and any `COPY` of a config file
   in the Dockerfile — that `COPY` is the anti-pattern this replaces.
2. **ConfigMap or Secret?** Judge the *content*, never the filename. `application.properties`
   holding a datasource password is a Secret; an `nginx.conf` with only routing is a ConfigMap.
3. **What should it derive?** Mount content is rendered through `tpl … $`, so `{{ .Values.x }}`
   works inside the file. Template the port, hostname, and sibling service names rather than
   duplicating them.

**Storage is the sibling question.** A `mounts.pvc` entry names a claim; something has to
create it. `tpl-library` ships `tpl.pvc` for exactly that, but it is an opt-in entrypoint —
`tpl.deployment` does not call it, so a chart whose `manifest.yaml` omits it, or whose
`persistence:` section is empty, leaves the pod `Pending` while `helm template` and
`helm install` both succeed. Ask "does something create this?" of every reference the values
introduce. The entrypoints and the claim-name pairing are in helm-tpl-library's README.

Full schema, examples, and anti-patterns: `core/references/file-mounts-standard.md`.
`assets/nginx-default.conf` is a placeholder showing the *shape* of a config — not the delivery
mechanism.

---

## 4. Audit

**Step 1 — Refresh context.** Detect platform; resolve library sources (§0.0); read each
library's `README.md` and `MIGRATION.md` at the resolved path.

**Step 2 — Run the engine.**

```bash
python3 core/scripts/audit.py [repo] [--platform gitlab|github] [--strict] [--json]
                              [--lib NAME=SOURCE ...] [--refresh]
```

It runs the common checks (Dockerfile, chart, ignore files, hygiene) plus the detected
platform's CI checks in one pass.

**Step 3 — Review what the engine cannot see.** Load `core/references/security-core.md` and the
platform addendum, and apply them. This is the highest-value part of the audit: credentials
embedded in values, chart posture, untrusted-input paths, token appropriateness.

**Step 4 — Report** by severity with `file:line` and a one-line rationale.

Mark every finding `[engine]` or `[judged]`. An `[engine]` finding is a reproducible fact,
stated flatly; a `[judged]` finding is a considered opinion that may be wrong, so give the
evidence and invite the user to overrule you. Never present a judged finding as if the engine
produced it. **Never fix during an audit** — propose, and let the user decide.
