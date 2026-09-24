---
name: containerize-remote-wrap
description: >
  Package a remote-endpoint policy wrap as a container image for the
  Manifold platform, push it to a container registry, register it with
  the endpoint URL in its config env, and offer a scored test run. Use
  after `/wrap-remote-policy`, when the model runs on the user's own
  inference server and the container only dials it.
compatibility: >
  Run from the user's policy project directory, after
  `/wrap-remote-policy` has written the wrap files under
  `<project>/.manifold/<slug>/`. Requires docker, a push credential
  for the target container registry (ghcr by default), and the
  `manifold` CLI (0.0.4 or later, for `policy init --env`). Input is
  a wrap that passes check_compatibility and verify under
  wrap-remote-policy.
---

## Summary

Take a wrap from `/wrap-remote-policy` (a Python module that exports
`PROFILE`, `BENCHMARK`, and `PIPELINE` and dials the user's inference
server) and get it running on the Manifold platform.

The output is four things:

1. **A `Dockerfile`** written to `<project>/.manifold/<slug>/Dockerfile`.
   It builds a slim image with the driver and its HTTP client, using
   the project root as the build context.
2. **A launcher script** written to `<project>/.manifold/<slug>/serve.py`.
   It imports the pairing module and calls `launch_server`. Phase 3
   shows the exact code to paste in.
3. **A container image** pushed to the registry at the agreed name
   and tag (for example
   `ghcr.io/<org>/policy-<slug>-<benchmark>:0.1.0`).
4. **A registered policy version** on the Manifold platform, with the
   endpoint URL in its `config.env` and `minimum_gpu_memory_gb: 0`.
   Registered with `manifold policy init --env KEY=VALUE
   --minimum-gpu-memory-gb 0`.

Files 1 and 2 are new files on disk. The other two live on the
registry and on the platform.

The image is different from the in-container-model case in three
ways:

- **No model, no CUDA.** The image is a slim Python base plus
  manifold-sdk, `httpx`, and any decoders the benchmark needs (for
  example `pillow` if the benchmark ships colored frames as JPEG).
- **No project source.** The wrap does not import from the user's
  project; only the pairing folder ships.
- **No GPU claim.** Registers with `minimum_gpu_memory_gb: 0`, so
  placement can put it on a GPU-less runner rather than occupying a
  card.

Once all four exist, the skill's job is done. After that, ask the
user whether to submit a scored test run against a benchmark of
their choice (Phase 4 walks through it). Do not submit a run on your
own.

This skill does not fix wrap bugs. If the wrap does not pass both
`check_compatibility` and `verify`, go back to
`/wrap-remote-policy` first.

## Rules

**Confirm before doing anything else.** First thing after this skill
loads, tell the user in your own words what it will do and why:
building a small Docker image (a few hundred MB, most of it scipy and
numpy), pushing it to their registry, and registering it on Manifold
with the endpoint URL in `config.env`, so the platform can pull and
run their driver against benchmarks. Wait for a yes before reading
`CONTEXT.md` or touching anything. Push, register, and submit still
have their own per-step confirmations later.

**Speak to the user in their language, not the SDK's.** The user has
not read the SDK docs. They will not recognize Docker fields,
registry commands, or the names of Manifold's tools and config
fields. The skill below names those identifiers freely because you
need them to write correct code. When narrating progress to the
user, translate.

Say things like:
- "I'll build the image that dials your server."
- "The image built and pushed to your registry."
- "Registered on Manifold with your endpoint URL attached to the
  version's config."
- "The scored test run finished. The score is X."

Not the identifiers from the Dockerfile snippets or tool calls
below. If the user uses one of those terms themselves, follow
their lead. Otherwise, describe what happened and why it matters.

**Run in the user's policy directory.** Once the user has said yes,
confirm the current working directory is their policy project. The
same one `/setup-manifold` and `/wrap-remote-policy` ran in. Look for
`<project>/.manifold/CONTEXT.md` and `.manifold/<slug>/` (with the
wrap files inside). If either is missing, stop and ask the user to
run the earlier skills first.

**Read `.manifold/CONTEXT.md` first.** setup-manifold already
recorded the package manager, registry, endpoint URL, auth
situation, wire contract, and benchmarks of interest; wrap-remote-policy
added anything else it learned. Read `CONTEXT.md` before asking the
user anything; ask only about details it does not cover. If
`CONTEXT.md` has `model_runtime = in_container`, stop and tell the
user this skill is for hosted-endpoint policies; `/containerize-wrap`
is the one for in-container models.

**Load provider-specific guidance.** If `CONTEXT.md` or the user
identifies the hosting platform, check `references/` for a file
named after that platform and read it. The file contains
platform-specific patterns that affect registration and auth. If no
matching file exists, the general rules in this file are sufficient.

**Write into `.manifold/<slug>/`.** The `Dockerfile` and `serve.py`
this skill produces both live under
`<project>/.manifold/<slug>/`, next to the wrap files. `docker
build` runs with the project root as the build context so the whole
project is available to `COPY`.

**Do not run this skill without an explicit user invocation.** If
another skill (for example `/wrap-remote-policy`) has just finished,
stop and wait for the user to ask for containerization by name. Do
**not** chain into this skill on your own after "the wrap is proven"
or any similar success line. Each step in the Manifold flow is a
separate skill so the user can review the previous step's output
before spending registry storage and cloud time; auto-chaining
skips that review.

**Plan the entire task in a to-do list before you start, and update
it as you go.** Use whichever planning tool your harness provides:

- **Claude Code:** `TaskCreate` to seed the plan, `TaskUpdate` to
  move items between `pending` / `in_progress` / `completed`,
  `TaskList` / `TaskGet` to read state.
- **Codex:** use `update_plan` to create and maintain an ordered
  plan, with exactly one item `in_progress` at a time. Keep the
  scored test run as an explicit item until it passes.
- **Other harnesses:** check the harness for a to-do list or
  planning tool before using the fallback below.
- **No planning tool available:** keep the plan as a plain-text
  checklist in your responses and re-post it (with statuses
  updated) each time you advance.

The intent is (1) to **structure the work** so nothing gets skipped,
and (2) to **stay accountable and informative** by updating the list
as steps start and finish, so the user can follow along without
asking.

**Ask the user before every step that costs money or writes to a
shared system.** Each of the choices below costs the user time,
cloud credits, or registry storage. Do not pick any of them
yourself:

- The target benchmark for the scored test run. Never pick "a
  reasonable benchmark" for the user.
- Pushing the image to the registry.
- Registering the policy on the platform.
- Submitting a run.

At each of those points: state what you are about to do, wait for a
confirmation, and only then proceed. Do not chain "wrap built
successfully, now submitting a run against <a benchmark>" into one
action. **If the user declines any of these, stop the skill there;
do not skip to the next step.**

The **policy name** (the thing that becomes `<slug>` in the registered
version) is **not** on that list. setup-manifold picks it and hands
it here. Do not rename the policy on the user's behalf. If the slug
is missing, ask the user once for it.

The container image name (registry, namespace, tag) is a
container-registry concept, not a user-facing choice. This skill
constructs it from the policy slug plus the org's registry and
namespace.

## How the platform runs a policy

The platform runs policies as registered container images. When a
run is dispatched, the runner pulls the image, starts it, waits for
the server inside to accept connections on port 8000, and then drives
it through the benchmark.

Consequences for the remote case:

1. **One image per wrap.** The `CMD` in the Dockerfile picks which
   wrap the container serves. Registration cannot override it.
2. **Tags become versions.** Registration reads the image tag and
   uses it as the version string. Re-running `manifold policy init`
   on an existing tag overwrites that version's config in place.
   Bump the tag anyway for every rebuild, so each run on the
   platform maps to exactly one image build.
3. **The runner injects `config.env` at container start.** The env
   map from the registered version becomes environment variables in
   the container. The driver reads the endpoint URL from one of
   those vars (for example `MY_SERVER_URL`), and any tunable
   overrides the profile exposes.
4. **Nothing local proves the image works in production conditions.**
   A clean local `docker run` shows that the driver reaches the
   endpoint and the server accepts connections on 8000. Whether the
   platform can pull, schedule, drive, and score the image is only
   settled by an actual scored run, which is up to the user to
   submit.

---

## Phase 1: Understand the inputs

Do this before writing a Dockerfile. You need the wrap module path,
the policy name, the manifold-sdk revision, and the environment
variables the driver reads pinned down first.

**The wrap.** Confirm the wrap passes both `check_compatibility` and
`verify` under `/wrap-remote-policy`. Record the module path that
exports `PROFILE`, `BENCHMARK`, and `PIPELINE`. The Dockerfile's
`CMD` will name it.

**The policy name.** This is the slug used in the registered policy
version. setup-manifold picks it (or the user does directly). If it
is missing, ask the user once for it. Do not invent one.

**The image name.** Built from the policy slug plus the org's
registry and namespace, in the shape:
`<registry>/<namespace>/policy-<slug>:<tag>`. For example,
`ghcr.io/<your-org>/policy-mypolicy-mybench:0.1.0`. The tag is a
version string; bump it for every change to the wrap or the
Dockerfile. This skill constructs the image name from those parts;
do not ask the user to type it out.

Examples below use `ghcr.io/<your-org>`. Substitute the actual
registry and namespace throughout.

**The manifold-sdk Git revision.** Read the **manifold-sdk revision**
line from the policy's subsection in `.manifold/CONTEXT.md`. It is the
full Git commit SHA installed when the wrap passed `check_compatibility`
and `verify`. Install `manifold-sdk` from that revision instead of
resolving the repository again. If the line is missing, return to
`/wrap-remote-policy`. Start with the most recent commit on the
`manifold-sdk` GitHub repository's default branch, then record its full
SHA after the wrap passes both checks.

**The endpoint URL env var.** Read `profile.py` and find the env
var the driver reads to get the server URL (for example
`MY_SERVER_URL`). This will go into the registered version's
`config.env`. If you can't find it in one grep, stop and ask the
user.

**Any tunable env vars.** Some fields on the profile are exposed as
env-var overrides (timeout, action steps, gripper convention). Read
`_ENV_OVERRIDES` in `profile.py` (or equivalent) and list them.
Only the endpoint URL is required at registration; overrides are
optional and can be added later.

**The auth model** from `CONTEXT.md`. If the endpoint needs a header
token, read `driver.py` and record the env var names the driver
reads the token from (for example `MY_AUTH_KEY` and
`MY_AUTH_SECRET`). These go into the registered version's
`config.env` next to the URL. The platform stores `config.env` in
plaintext. Tell the user this before registration. If the user can
restrict the endpoint by network instead (IP allowlist to the
runner's egress, or VPC-internal), that is the safer option.

**The benchmark decoders the image needs.** Look at the benchmark's
sensors. If the benchmark ships colored frames as JPEG, the image
needs `pillow`. If it ships depth as TIFF, same. If unsure, add
`pillow` (small, common); a missing decoder surfaces as an import
error the moment the pack tries to decode.

> **Phase 1 checkpoint.** Record before designing:
> ```
> wrap_module           = ?  (for example mywrap.mypolicy_mybench)
> checks_pass           = yes (link to wrap-remote-policy handoff)
> policy_slug           = ?  (source: setup-manifold | user)
> image_name            = <registry>/<namespace>/policy-<slug>:<tag>
>                         (constructed by this skill from the slug)
> sdk_revision          = ?  (from the policy's manifold-sdk revision line)
> endpoint_url_env      = ?  (for example MY_SERVER_URL)
> tunable_env_vars      = [list, or empty]
> auth_model            = open | network_restricted | header_token
> auth_env_vars         = [list, or empty]  (token env vars the driver reads)
> network_restriction_arranged = yes | no | n/a
> benchmark_decoders    = [list, for example httpx, pillow]
> ```

---

## Phase 2: Design the Dockerfile

Decide what the image will contain before writing any of it.
Everything in this phase is a decision, not implementation.

### What goes in the image

Assume the user has a project folder with the wrap files under
`.manifold/<slug>/`. The image does **not** contain the model, the
model's dependencies, or the project's source code.

The image contains, in this order:

1. **A slim Python base image**, pinned by digest, not by a floating
   tag like `latest`, so rebuilds are reproducible. `python:3.12-slim-bookworm`
   is a safe default. Debian, not Alpine: the runner probes the
   container's readiness with a bash `/dev/tcp` trick that busybox
   ash does not have.
2. **manifold-sdk**, installed from the full Git commit SHA on the
   policy's **manifold-sdk revision** line. In a discarded build stage,
   export the project's `uv.lock` to `requirements.txt`. Install that
   file in the image so its direct and transitive dependency versions
   match the wrap environment. Keep the `manifold-sdk` entry pinned to
   the recorded Git revision.
3. **The driver's HTTP client and any benchmark decoders.** `httpx`
   for the transport. `pillow` if the target benchmark ships
   colored frames as JPEG (LIBERO does). Pin exact versions; do not
   let a fresh resolution at build time drift.
4. **The wrap files.** Only `.manifold/<slug>/`, not the project's
   `src/`. The wrap does not import from the project.

### The wrap files

The whole `.manifold/<slug>/` folder is what ships:
`driver.py`, `profile.py`, the pairing file, and `serve.py`. Copy
them into the `WORKDIR`, then set `PYTHONPATH` so the launcher's
`import` finds them.

### Weights

There are none. The checkpoint lives on the user's inference server.
Skip every "fetch or bake" decision from the in-container-model case.

### Auth to the endpoint

Never bake a token into the image. If the endpoint needs a header
token, it goes into the registered version's `config.env` and the
driver reads it from the environment at start. The platform stores
`config.env` in plaintext. Say this to the user in Phase 4 before
registering. A network restriction on the endpoint (IP allowlist,
VPC-internal) is the safer option when the user can arrange it.

> **Phase 2 checkpoint:**
> ```
> base_image          = python:3.12-slim-bookworm@sha256:...
> deps_in_image       = manifold-sdk (pinned), httpx (pinned), pillow (pinned, if needed)
> project_source      = none (wrap does not import from it)
> weights             = none (server holds the checkpoint)
> auth_strategy       = network_restriction | token_in_config_env | none
> ```

---

## Phase 3: Build and push the image

Write the Dockerfile and build it. A local `docker run` is
meaningful here even on a CPU-only box, because the container has
no GPU work to do. Then push to the registry.

### Dockerfile rules

These apply to every image:

**Port 8000.** The container must listen on port 8000.
`DEFAULT_CONTAINER_PORT` is set to 8000 in the runner code and
registration cannot change it. Bind `0.0.0.0:8000` in the `CMD`.

**Bash is required.** The readiness probe runs
`bash -c 'exec 3<>/dev/tcp/127.0.0.1/8000'` inside the container.
`python:3.12-slim-bookworm` has bash; do not switch to Alpine or a
distroless base.

**`PYTHONUNBUFFERED=1`.** Set this in the Dockerfile. Without it, a
crashing container's last output lines stay in a write buffer and
are lost. That output is how you diagnose failures (readiness poll
timing out, endpoint URL wrong, wire codec broken).

**Layer order.** Put manifold-sdk and its transitive deps
(scipy, numpy) in early layers. Put the wrap files in late layers.
That way, editing the wrap rebuilds only the cheap layers at the end.

**Do NOT apply** the following rules from the in-container-model
case: CUDA base image, layer ordering for torch/jax/CUDA wheels,
pinning model deps (numpy, scipy) for the model's tolerance (still
pin them, but for wire-format stability rather than model
tolerance), GPU memory pre-allocation flags. No model runs here.

### Launcher and CMD

Same launcher shape as the in-container case:

```python
"""Serve a wrapped policy over TCP."""
import argparse, importlib
from manifold.recipes import launch_server, read_pairing

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--pairing", required=True)
    args = parser.parse_args()
    pairing = read_pairing(importlib.import_module(args.pairing))
    launch_server([pairing], port=args.port, host=args.host)

if __name__ == "__main__":
    main()
```

`COPY` the wrap module and the launcher into the `WORKDIR`, then:

```dockerfile
CMD ["python", "serve.py", "--pairing", "my_wrap.mypolicy_mybench", \
     "--host", "0.0.0.0", "--port", "8000"]
```

### Build

Manifold's runners are x86_64 Linux machines, so the image has to be
built for `linux/amd64`. On an Apple Silicon Mac, or any other arm64
machine, `docker build` produces an arm64 image by default. The push
to the registry succeeds. Registration succeeds too. The failure
comes later, when the runner tries to start the container. Name the
platform explicitly:

```sh
docker buildx build --platform linux/amd64 \
    -f <path-to-Dockerfile> \
    -t <registry>/<namespace>/policy-<slug>:<tag> .
```

On an x86_64 Linux machine, plain `docker build` with the same
`-f` and `-t` arguments does the same thing.

This image contains no torch, no jax, and no CUDA libraries, so
building it for amd64 on an arm64 machine is quick and reliable.

A clean `docker build` means the image assembled without errors,
nothing more. The driver has not run yet.

**Any edit under `.manifold/<slug>/` after the build makes the image
stale.** The image holds a copy of the driver, the profile, and the
pairing file from the moment of the build. If you change any of
them (for example, adding token headers to the driver), rebuild,
bump the tag, push, and register again. Never tell the user a
rebuild is unnecessary after a source edit.

### Run it locally

CPU-only local runs are meaningful for a remote wrap. The container
has no GPU work to do; its main job at startup is dialing the
endpoint and passing the readiness probe.

**If the endpoint is reachable from your local box**, run it:

```sh
docker run -p 8000:8000 -e MY_SERVER_URL=<endpoint-url> \
    <image>:<tag>
```

Look for:

- The driver's startup log line printing the endpoint URL, the
  camera list, and the state window read from the description route.
- The listening line: `listening on 0.0.0.0:8000 (TCP), up to 8
  concurrent shard(s)`.

Both must appear. If the container hangs before either, the
readiness poll is blocked. Check that the URL is right, the
endpoint is up, and (if the endpoint is network-restricted) your
local box's IP is allowlisted. If the container starts printing
`RuntimeError` from the driver's readiness poll and exits, the URL
or the description route is wrong.

**If the endpoint is not reachable from your local box** (private
VPC, internal-only), skip this step. The first real proof will be a
scored run in Phase 4.

### Push

**Save the Dockerfile and launcher before you push.** If they get
lost or overwritten later, no one can rebuild the image or see what
code went into it.

**Ask the user before pushing.** Show them the exact image name and
tag, and wait for confirmation.

```sh
docker login ghcr.io   # or the registry the user chose
docker push <registry>/<namespace>/policy-<slug>:<tag>
```

**Make sure the platform can pull the image.** Two paths:

- **Public registry** (a public ghcr package, a public Docker Hub
  repo). Pull just works, no credentials involved. A new ghcr
  package starts private; flip it to public at
  `https://github.com/orgs/<org>/packages/container/<package>/settings`
  before any run.
- **Private registry** (private ghcr package, private Docker Hub
  repo, ECR, Artifact Registry). The platform needs a pull
  credential configured on its side. Confirm with the Bifrost team
  before submitting a run.

Either way, a pull failure at run time surfaces as a scheduling or
pull error, not a permission error, so if the platform can't reach
the image, the run just looks broken.

> **Phase 3 checkpoint:**
> ```
> build_exit_code        = 0
> startup_log_printed    = yes | no | skipped (endpoint unreachable from local box)
> listening_line         = yes | no | skipped
> source_saved           = yes (where: git commit hash | folder | ...)
> push_confirmed_by_user = yes | no
> push_exit_code         = 0
> visibility             = public | private (action needed)
> ```

---

## Phase 4: Register with env, then offer a test run

Register the image with the `manifold` CLI. Then ask the user
whether to submit a scored test run. Do not submit one on your own.

### Register

**Ask the user to confirm the slug, version, image name, and
endpoint URL before running the command.** Registration creates a
catalog entry for their organization, and the tag becomes the
version string.

```sh
manifold policy init <slug> \
    --image <registry>/<namespace>/policy-<slug>:<tag> \
    --minimum-gpu-memory-gb 0 \
    --env MY_SERVER_URL=<endpoint-url>
```

The image tag becomes the version. So `--image
.../policy-mypolicy-mybench:0.1.0` registers version `0.1.0`.

**`--env` replaces the whole env map.** It does not merge with an
earlier registration. Pass every key the driver reads on every
call: the URL, any token vars, any tunable overrides. If you re-run
the command with only one `--env`, the others are gone.

**Re-running on the same tag overwrites the version's config in
place.** This is how you fix a wrong URL without a rebuild. It does
not update the image. After a source edit, rebuild (see Phase 3).

**`minimum_gpu_memory_gb: 0`.** The container has no GPU work to
do, and 0 lets placement take a GPU-less runner instead of
occupying a card. This is the opposite of the in-container-model
case, where 0 would silently deny GPU access to a model that needs
it.

**Add tunable overrides only if the user asked for them.** If the
user wants to change a timeout or a chunk stride at registration
time, add another `--env` (for example `--env MY_TIMEOUT_S=240`).
Otherwise pass only the endpoint URL and any auth vars.

**Auth caveat.** If the endpoint needs a header token, pass the
token vars with `--env` (for example `--env MY_AUTH_KEY=... --env
MY_AUTH_SECRET=...`). The platform stores `config.env` in plaintext.
Tell the user this before running the command. If the user would
rather not store the token, restrict the endpoint by network (IP
allowlist, VPC-internal) instead and drop the token vars.

**Visibility.** By default a new policy is visible only to its own
organization. Only make it public if the user asks for it.

### Offer a scored test run

Registration is done. The image is live on the platform, but you
have not yet seen the platform pull it, schedule it, drive it, and
score it. Only a scored run does that.

**Ask the user whether to submit one.** Something like: "The image
is registered as version `X` and points at your endpoint at `URL`.
Do you want to submit a scored test run? If so, which registered
benchmark should I pair it against? A run costs cloud time. If
the benchmark has a debug variant, I will run that first."

Do not pick a benchmark. Do not submit on your own. If the user
says no, stop here; the skill is done.

**Check for a debug variant before submitting.** When the user
names a benchmark, run `manifold benchmark list` and look for a
debug variant of the same family: an entry named `debug-` plus
the family name. A debug run costs much less and still makes the
platform pull the image, start it, pair it, drive episodes, and
reach the endpoint. Submit the first run against the debug
variant if one is listed, otherwise against the named benchmark.

```sh
manifold run submit <policy-slug> <debug-or-benchmark-slug>
manifold run watch <run-id>
```

If the pairing is rejected on the debug variant, submit against
the named benchmark and report the mismatch to the Bifrost team.
After a clean debug run, ask the user whether to submit the full
benchmark.

Before submitting:

- The named benchmark must be registered and must have a working
  image. If the run fails immediately with an error naming the
  benchmark image (missing image, benchmark container crash on
  start), that is a benchmark-side problem, not a wrap bug; flag
  it to the Bifrost team.
- Runs are visible to everyone in the organization; use a clear
  `--name` if the user wants the run labeled.
- The first request per task carries a fresh task sentence and the
  endpoint's language encoder may take 30 to 60 seconds on that
  request. The runner's per-request timeout must cover it; the
  wrap's `timeout_s` covers the driver's side.

### Validate the results

A completed run does not mean the wrap is correct. Check the
actual output.

**If the run used a debug variant, skip the score comparison.**
A debug suite is too small for a meaningful score. Check episode
completion, first frames, and action magnitudes below. Compare
scores only on the full run.

**Episode completion.** All episodes should reach `completed`:

```sh
manifold run get <run-id> --episodes
```

**First frames.** Dump the first observation frame from each
episode. A mostly black first frame means the scene did not load,
regardless of what the wrap did with it.

**Action magnitudes.** Actions should be in the physical range for
the embodiment (millimeters, radians). Actions stuck at the edges
(all 1.0 or all -1.0) suggest either the driver's action scaling
is off or the server is returning normalized outputs the driver
never denormalized.

**Score vs reference.** Compare `mean_success` against the
checkpoint's published or previously measured score on this suite.
A checkpoint trained on a real rig will not score well in a
simulator's scenes, so the first run tells you the connection
works, not whether the model is any good.

**This is the only point in the whole flow where convention bugs
become visible.** A wrong gripper sign, a wrong component order, a
wrong rotation encoding, a wrong depth scale, all pass
`check_compatibility` and `verify`. They only show up here as a
score near zero. For a remote wrap, add: a wrong wire codec, a
wrong description-route contract, or a stale action scaling
constant.

A near-zero score on a suite the checkpoint is known to handle
means a wrap bug until proven otherwise. Go back to
`/wrap-remote-policy` Phase 3, fix the driver, bump the tag, and
re-enter this skill at Phase 3.

**Composite benchmarks.** If the benchmark mixes several task
groups (for example `libero-plus`), do not stop at the overall
score. Break it down by task group. Use the episode list from
`manifold run get <run-id> --episodes` and group episodes by their
instruction prefix. One group scoring near zero while the others
score normally means the driver picked the wrong settings for that
group. Read the run logs for the driver's lookup warnings (see
wrap-remote-policy Phase 1, "Instruction strings"). If any appear,
the instruction matching is wrong. Fix it in the driver, rebuild,
bump the tag, and run again.

### If the run fails on connection to the endpoint

The container printed a driver error and exited, or all requests
returned 5xx. Check:

- **Zero episodes completed, and the log shows a connection timeout
  (`Errno 110`) on the very first request.** The runner could not
  reach the endpoint at all. If `curl <url>/config` works from
  another machine and nothing in the wrap changed since the last
  successful run, this is a runner placement or networking problem
  on the platform. Report it to the Bifrost team with the run ID.
  Do not change the wrap.
- The endpoint URL in `config.env` is right (typo, missing
  scheme, trailing slash).
- The endpoint is up and its description route responds. Test it
  from a machine that can reach it: `curl <url>/config`.
- The runner's egress addresses are allowlisted on the endpoint.
  If the endpoint is network-restricted and the platform's IPs are
  not allowed, every request fails.
- The wire codec matches. If `/config` answers but `/infer`
  returns a decode error, the codec assumption is wrong.

Fix, bump the tag, push, re-register the new tag with the same
`config.env`, and offer another scored test run.

### If the run is slow but works

The container has no GPU claim. That is expected; the model runs on
the user's server, and network round-trips dominate. If throughput
is a concern, the answer is either raising the sharded
concurrency (talk to the Bifrost team) or lowering the endpoint's
own response time; the wrap does not gate throughput here.

> **Phase 4 checkpoint:**
> ```
> slug                          = ?
> version                       = ? (from image tag)
> config_env_endpoint_url       = ?
> minimum_gpu_memory_gb         = 0 (always for a remote wrap)
> register_confirmed_by_user    = yes | no
> registration_result           = success | failure (message)
> test_run_offered_to_user      = yes  (must be yes; offering is required)
> user_asked_for_test_run       = yes | no  (if no: stop, skill is done)
>
> (fill in below only if the user asked for a test run)
> benchmark_slug                = ? (chosen by user)
> debug_variant                 = <name> | none  (from `manifold benchmark list`)
> debug_run_id                  = ?  (first run, when a debug variant exists)
> debug_episodes_completed      = ? / ?
> submit_confirmed_by_user      = yes | no
> run_id                        = ?
> episodes_completed            = ? / ?
> mean_success                  = ?
> reference_score               = ? (source)
> score_within_noise            = yes | no (if no: investigate)
> first_frames_checked          = yes | no
> action_range_checked          = yes | no
> connection_failure_seen       = yes | no
> (if yes:)
> fix_applied                   = ? (what changed)
> new_tag                       = ?
> ```

---

## Final checklist

Inputs

- [ ] Wrap passes `check_compatibility` and `verify` under
      `/wrap-remote-policy`
- [ ] Policy slug received from setup-manifold (not invented); image
      name constructed from it
- [ ] manifold-sdk in the image is installed from the policy's
      **manifold-sdk revision** in `.manifold/CONTEXT.md`
- [ ] Endpoint URL env var identified from `profile.py`
- [ ] Tunable env vars listed (may be empty)
- [ ] Auth model recorded; if `header_token`, the token env vars are
      listed and the user was told `config.env` is stored in
      plaintext

Image contents

- [ ] Slim Python base image, pinned by digest, not by a floating
      tag like `latest`
- [ ] Built for `linux/amd64` (`docker buildx build --platform
      linux/amd64` on any arm64 machine, including Apple Silicon)
- [ ] No CUDA base, no torch/jax, no model stack in the image
- [ ] `httpx` installed at a pinned version
- [ ] Benchmark decoders installed if the benchmark ships encoded
      frames (for example `pillow` for JPEG)
- [ ] Only `.manifold/<slug>/` copied in; no project `src/`
- [ ] No credentials baked into the image (no `ENV MY_TOKEN=...`,
      no copied credential files)

Dockerfile rules

- [ ] Dockerfile builds without errors
- [ ] Container starts locally, prints the driver's startup log
      line (endpoint URL, cameras, state window) and the listening
      line, if the endpoint is reachable from the local box;
      skipped otherwise
- [ ] Port 8000, bound on `0.0.0.0`
- [ ] `PYTHONUNBUFFERED=1` set
- [ ] Bash present in the image

Push and register

- [ ] Tag bumped for every rebuild; Dockerfile and launcher saved
      before push
- [ ] Image rebuilt after any edit under `.manifold/<slug>/`; the
      user was never told a rebuild was unnecessary after a source
      edit
- [ ] Push confirmed by the user
- [ ] Registry package visible so the platform can pull the image
- [ ] Registered with `manifold policy init --env ...
      --minimum-gpu-memory-gb 0`
- [ ] Every `--env` key passed on every registration call: endpoint
      URL, token vars if any, tunable overrides the user asked for
- [ ] `minimum_gpu_memory_gb` is `0`
- [ ] User was offered a scored test run and given the choice

If the user asked for a test run:

- [ ] Benchmark chosen by the user; submit confirmed before running
- [ ] `manifold benchmark list` checked for a debug variant of the
      named benchmark's family; when one exists, the first run
      used it
- [ ] Debug run judged on episode completion, first frames, and
      action ranges, with no score comparison
- [ ] Test run completed; score compared to reference
- [ ] If the benchmark is composite: score broken down by task
      group; run logs checked for lookup warnings
- [ ] First frames and action ranges inspected
- [ ] Connection failures diagnosed against the endpoint (URL, up,
      allowlisted, codec); zero episodes with `Errno 110` on the
      first request reported to Bifrost with the run ID
- [ ] If a fix was applied: image re-tagged and pushed, new tag
      re-registered with every `--env` key
