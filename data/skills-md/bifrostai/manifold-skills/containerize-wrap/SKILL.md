---
name: containerize-wrap
description: >
  Package a verified policy wrap as a container image for the Manifold platform,
  then build it, push it to a container registry, register it, and run it. Use
  when asked to "containerize my policy", "build the policy image", "push my
  wrap to ghcr", "register my policy on the platform", or "get my wrap running
  on the platform". This skill is for the case where the model loads into the
  container. For policies where the model runs on the user's own inference
  server, use `/containerize-remote-wrap` instead.
compatibility: >
  Run this skill from the user's policy project directory, after
  `/wrap-policy` has written the wrap files under
  `<project>/.manifold/<slug>/`. Requires docker, a push credential for
  the target container registry (ghcr by default), and the manifold CLI
  authenticated with `manifold auth login`. Input is a wrap that passes
  check_compatibility and verify under wrap-policy.
---

## Summary

Take a wrap from the `wrap-policy` skill (a Python module that exports
`PROFILE`, `BENCHMARK`, and `PIPELINE`) and get it running on the Manifold
platform.

The output is four things:

1. **A `Dockerfile`** written to `<project>/.manifold/<slug>/Dockerfile`.
   It builds the policy image with the project root as the build
   context.
2. **A launcher script** written to `<project>/.manifold/<slug>/serve.py`.
   It imports the pairing module from `.manifold/<slug>/` and calls
   `launch_server`. Phase 3 shows the exact code to paste in.
3. **A container image** pushed to the registry at the agreed name and
   tag (e.g. `ghcr.io/<org>/policy-<slug>:0.1.0`).
4. **A registered policy version** on the Manifold platform. This is a
   catalog entry created by `manifold policy init` that points at the
   image.

Files 1 and 2 are new files on disk. The other two live on the registry
and on the platform.

This skill is for the case where the model loads into the built
container. If the model runs on the user's own inference server (Modal
endpoint, private HTTPS box), use `/containerize-remote-wrap` instead.

Once all four exist, the skill's job is done. After that, ask the user
whether to submit a scored test run against a benchmark of their choice
(Phase 4 walks through it). Do not submit a run on your own.

This skill does not fix wrap bugs. If the wrap does not pass both
`check_compatibility` and `verify`, go back to `wrap-policy` first.

## Rules

**Confirm before doing anything else.** First thing after this skill
loads, tell the user in your own words what it will do and why:
building a Docker image (10 to 30 GB of local disk), pushing it to their
registry, and registering it on Manifold, so the platform can pull and
run their policy against benchmarks. Wait for a yes before reading
`CONTEXT.md` or touching anything. Push, register, and submit still
have their own per-step confirmations later.

**Speak to the user in their language, not the SDK's.** The user has
not read the SDK docs. They will not recognize Docker fields,
registry commands, or CLI flag names. The skill below names those
identifiers freely because you need them to write correct code.
When narrating progress to the user, translate.

Say things like:
- "I'll build the image that contains your policy."
- "The image built and pushed to your registry."
- "Registered on Manifold as version 0.1.0."
- "The scored test run finished. The score is X."

Not the identifiers from the Dockerfile snippets or CLI examples
below. If the user uses one of those terms themselves, follow
their lead. Otherwise, describe what happened and why it matters.

**Run in the user's policy directory.** Once the user has said yes,
confirm the current working directory is their policy project. The
same one `/setup-manifold` and `/wrap-policy` ran in. Look for
`<project>/.manifold/CONTEXT.md` and `.manifold/<slug>/` (with the
wrap files inside). If either is missing, stop and ask the user to run
the earlier skills first.

**Read `.manifold/CONTEXT.md` first.** setup-manifold already recorded
the package manager, registry, weights location, deployment style,
GPU / VRAM, and benchmarks of interest; wrap-policy added anything
else it learned. Read `CONTEXT.md` before asking the user anything;
ask only about details it does not cover.

**Stop if this is a hosted-endpoint policy.** If `CONTEXT.md` has
`model_runtime = hosted_endpoint`, this skill is the wrong one. Stop
and point the user at `/containerize-remote-wrap`, which packages
wraps for policies that run on the user's own inference server.

**Write into `.manifold/<slug>/`.** The `Dockerfile` and `serve.py`
this skill produces both live under
`<project>/.manifold/<slug>/`, next to the wrap files. `docker build`
runs with the project root as the build context so the whole project
is available to `COPY`.

**Do not run this skill without an explicit user invocation.** If another
skill (for example `/wrap-policy`) has just finished, stop and wait for
the user to ask for containerization by name. Do **not** chain into this
skill on your own after "the wrap is proven" or any similar success line.
Each step in the Manifold flow is a separate skill so the user can
review the previous step's output before spending registry storage and
cloud time; auto-chaining skips that review.

**Plan the entire task in a to-do list before you start, and update it as
you go.** Use whichever planning tool your harness provides:

- **Claude Code:** `TaskCreate` to seed the plan, `TaskUpdate` to move items
  between `pending` / `in_progress` / `completed`, `TaskList` / `TaskGet` to
  read state.
- **Codex:** use `update_plan` to create and maintain an ordered plan, with
  exactly one item `in_progress` at a time. Keep the scored test run as an
  explicit item until it passes.
- **Other harnesses:** check the harness for a to-do list or planning tool
  before using the fallback below.
- **No planning tool available:** keep the plan as a plain-text checklist in
  your responses and re-post it (with statuses updated) each time you advance.

The intent is (1) to **structure the work** so nothing gets skipped, and
(2) to **stay accountable and informative** by updating the list as steps
start and finish, so the user can follow along without asking.

**Ask the user before every step that costs money or writes to a shared
system.** Each of the choices below costs the user time, cloud credits, or
registry storage. Do not pick any of them yourself:

- The target benchmark for the scored test run. Never pick "a reasonable
  benchmark" for the user.
- Pushing the image to the registry.
- Registering the policy on the platform.
- Submitting a run.

At each of those points: state what you are about to do, wait for a
confirmation, and only then proceed. Do not chain "wrap built successfully,
now submitting a run against <a benchmark>" into one action. **If the user
declines any of these, stop the skill there; do not skip to the next
step.**

The **policy name** (the thing that becomes `<slug>` in
`manifold policy init <slug>`) is **not** on that list. setup-manifold
picks it and hands it here. Do not rename the policy on the user's
behalf. If the slug is missing, ask the user once for it.

The container image name (registry, namespace, tag) is a
container-registry concept, not a user-facing choice. This skill
constructs it from the policy slug plus the org's registry and
namespace.

## How the platform runs a policy

The platform runs policies as registered container images. When a run is
dispatched, the runner pulls the image, starts it, waits for the server
inside to accept connections on port 8000, and then drives it through the
benchmark.

Three consequences follow:

1. **One image per wrap.** The `CMD` in the Dockerfile picks which wrap the
   container serves. Registration cannot override it.
2. **Tags become versions.** `manifold policy init` reads the image tag and
   uses it as the version string. Never reuse a tag; old tags are
   immutable.
3. **Nothing local proves the image works in production conditions.**
   A clean local `docker run` only shows that the server starts.
   Whether the platform can pull, schedule, drive, and score the image
   is only settled by an actual scored run, which is up to the user to
   submit.

---

## Phase 1: Understand the inputs

Do this before writing a Dockerfile. You need the wrap module path, the
policy name, and the manifold-sdk revision pinned down first.

**The wrap.** Confirm the wrap passes both `check_compatibility` and
`verify` under `wrap-policy`. Record the module path that exports
`PROFILE`, `BENCHMARK`, and `PIPELINE`. The Dockerfile's `CMD` will name
it.

**The policy name.** This is the slug used in `manifold policy init
<slug>`. setup-manifold picks it (or the user does directly). If it
is missing, ask the user once for it. Do not invent one.

**The image name.** Built from the policy slug plus the org's registry
and namespace, in the shape:
`<registry>/<namespace>/policy-<slug>:<tag>`. For example
`ghcr.io/<your-org>/policy-mypolicy-mybench:0.1.0`. The tag is a version
string; bump it for every change to the wrap or the Dockerfile. This
skill constructs the image name from those parts; do not ask the user
to type it out.

Examples below use `ghcr.io/<your-org>`. Substitute the actual registry
and namespace throughout.

**The manifold-sdk Git revision.** Read the **manifold-sdk revision**
line from the policy's subsection in `.manifold/CONTEXT.md`. It is the
full Git commit SHA installed when the wrap passed `check_compatibility`
and `verify`. Install `manifold-sdk` from that revision instead of
resolving the repository again. If the line is missing, return to
`/wrap-policy`. Start with the most recent commit on the `manifold-sdk`
GitHub repository's default branch, then record its full SHA after the
wrap passes both checks.

> **Phase 1 checkpoint.** Record before designing:
> ```
> wrap_module      = ?  (e.g. mywrap.mypolicy_mybench)
> checks_pass      = yes (link to wrap-policy handoff)
> policy_slug      = ?  (source: setup-manifold | user)
> image_name       = <registry>/<namespace>/policy-<slug>:<tag>
>                    (constructed by this skill from the slug)
> sdk_revision     = ?  (from the policy's manifold-sdk revision line)
> ```

---

## Phase 2: Design the Dockerfile

Decide what the image will contain before writing any of it. Everything in
this phase is a decision, not implementation.

### What goes in the image

Assume the user has a project folder with the model's code and
dependencies. Whether it's a cloned git repo, a fork, a local working
directory, or a messy research folder on a shared workstation. Treat
it the same way.

The image contains, in this order:

1. **A base image** with Python and CUDA matching what the model was
   trained on. Pin it by digest, not by a floating tag like `latest`,
   so rebuilds are reproducible. If unsure, an official CUDA runtime
   image on Ubuntu for the trained CUDA version is a safe default.
2. **The model project's dependencies**, installed with `uv`. In most
   cases: `uv sync` if the project has a `pyproject.toml` and
   `uv.lock`, or `uv pip install -r requirements.txt` if it only ships
   a requirements file. Fall back to whatever the project actually
   supports (conda env, raw `pip`) only if `uv` cannot handle it.
3. **manifold-sdk**, installed from the full Git commit SHA on the
   policy's **manifold-sdk revision** line:
   `uv pip install "manifold-sdk @ git+https://github.com/bifrostai/manifold-sdk.git@<commit>"`.
4. **The parts of the project folder that the wrap imports from.**
   `driver.py` names what inference needs. Trace its imports (and
   their transitive imports) back to the folders they live in, and
   `COPY` only those. Skip everything else: training scripts, datasets,
   logs (`wandb/`, `tb_logs/`), notebooks, alternate checkpoints,
   `.git`. Use a `.dockerignore` or an explicit list of `COPY` paths.
   If the container crashes at startup on a missing import, add that
   path. Set `ENV PYTHONPATH=/app` (or wherever you copied to) so the
   imports resolve.
5. **The wrap module and the launcher** (`profile.py`, `driver.py`,
   the pairing file, and `serve.py`), copied into the `WORKDIR`.

### Pin the project source

For rebuilds to match, the project folder's state has to be pinned.
If the folder is in git, pin the commit with a build `ARG` and check
it out during build. If it isn't, snapshot the folder (a tarball
saved somewhere durable) and record which snapshot the image was
built from. Bumping that pin is a separate decision from bumping the
manifold-sdk revision.

### Weights: fetched or baked?

Two ways to get the model checkpoint into the running container:

- **Fetched at first load.** The profile's `default_weights` contains a
  hub id or path. Point the model library's checkpoint cache at
  `/opt/manifold/cache` (whatever env var it uses: `HF_HOME` for
  Hugging Face, `TORCH_HOME` for torch hub, etc.). The platform mounts
  a persistent host directory at that path, so the download happens
  once per box and is reused across runs.

  The container has a 10-minute window to become ready (bind port 8000
  and accept a TCP connection). That window covers both the download
  and the load into GPU memory. A large checkpoint may not finish in
  time on a cold box; for those, prefer baking.

  **If the checkpoint needs a credential** (gated Hugging Face repo,
  private hub repo, private S3 bucket), you cannot use "fetched at
  first load" today; the platform does not currently give you a way
  to hand a run-time credential to your container. Bake the checkpoint
  in instead. Do **not** try to work around this by putting the
  credential in the image (`ENV HF_TOKEN=...`, copied
  `~/.huggingface/token`, etc.); anyone who pulls the image gets it.
- **Baked into the image.** Copy the checkpoint files in at build
  time. Two common cases:
  - **You already have the weights on disk** (a checkpoint from your
    training run, a folder you downloaded earlier). Just `COPY` the
    files into the image. No auth, no download, done.
  - **You need to fetch them from a private source at build time.** Do
    it on a machine where you already have the credential, so `pip`,
    `huggingface-cli`, or `aws` can resolve the download using your
    local auth. The credential never enters the image, only the
    resolved files do.

  Only copy what inference needs; hub snapshots often include
  optimizer states, training configs, and alternate checkpoints that
  add size without being used. Baking trades a larger image and
  slower pushes for not having to fetch at run time.

### How the wrap gets served

The container's `CMD` runs a small launcher script that imports the wrap
module and hands its `PROFILE` / `BENCHMARK` / `PIPELINE` to
`launch_server`. Phase 3 shows the launcher and the `CMD` line. Nothing
else in the image needs to know about the wrap.

> **Phase 2 checkpoint:**
> ```
> base_image         = ?  (pinned by digest)
> project_pin        = ?  (git commit ARG | tarball snapshot path)
> weights_approach   = fetched at first load | baked
> ```

---

## Phase 3: Build and push the image

Write the Dockerfile and build it. On a GPU box, run it locally to prove
the server starts; on a CPU-only box, skip the local run. Then push it
to the registry.

### Dockerfile rules

These apply to every image:

**Port 8000.** The container must listen on port 8000.
`DEFAULT_CONTAINER_PORT` is set to 8000 in the runner code and registration
cannot change it. Bind `0.0.0.0:8000` in the `CMD`.

**Bash is required.** The readiness probe runs
`bash -c 'exec 3<>/dev/tcp/127.0.0.1/8000'` inside the container. Install
bash if the base image doesn't have it.

**`PYTHONUNBUFFERED=1`.** Set this in the Dockerfile. Without it, a
crashing container's last output lines stay in a write buffer and are lost.
That output is how you diagnose failures.

**Layer order.** Put the model's large dependencies (torch, jax, CUDA
wheels) in early layers. Put manifold-sdk and your wrap code in later
layers. That way, editing the wrap rebuilds only the cheap layers at
the end.

**Pin the model's dependencies.** manifold-sdk declares dependency
floors with no ceilings. A fresh resolution inside a rebuild can
upgrade a package the model cannot use. Pin the model's `numpy`,
`scipy`, and similar packages in the image to prevent that.

**No network fetches at model construction.** If the loader downloads
anything at construction time (pretrained weights, tokenizer files),
disable it or copy the files into the image at build time. A container in
an offline environment will fail at load otherwise.

**GPU memory pre-allocation.** Some frameworks claim all GPU memory at
startup; JAX does this by default. Disable that behavior in the
Dockerfile with the framework's environment variable. Otherwise, on a
shared box, all GPU memory is consumed before the benchmark renderer
starts.

### Launcher and CMD

Write a small launcher script that imports the wrap module by name and
starts the server:

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

`COPY` the wrap module (the file exporting `PROFILE`, `BENCHMARK`,
`PIPELINE`, plus `profile.py` and `driver.py`) and the launcher into the
`WORKDIR`, then:

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

Building a CUDA image for amd64 on an arm64 machine runs the build
steps under emulation. That is slow, and some GPU wheels fail to
install under it. Build this image on a Linux x86_64 machine when the
user has one.

A clean `docker build` means the image assembled without errors, nothing
more. The server has not run yet.

### Run it locally (only if the local box has a GPU)

Skip this step on a CPU-only machine. A robotics policy needs a GPU to
load and serve, so a CPU-only local run only tells you whether Python
could import, not whether the container actually works. On CPU-only,
proceed straight to Push; the container will first be exercised for
real when the user submits a run in Phase 4.

On a GPU box, start the container and confirm the server prints its
listening line:

```sh
docker run --gpus all <image>:<tag>
```

Look for:
```
listening on 0.0.0.0:8000 (TCP), up to 8 concurrent shard(s)
```

Dependency conflicts, import errors, and model loading failures surface
here, not during build. If the listening line does not appear (crash,
hang, silent exit), **do not push**. Fix the Dockerfile or the wrap
and rebuild first.

### Push

**Save the Dockerfile and launcher before you push.** If they get lost
or overwritten later, no one can rebuild the image or see what code
went into it.

**Ask the user before pushing.** Show them the exact image name and tag,
and wait for confirmation.

```sh
docker login ghcr.io   # or the registry the user chose
docker push <registry>/<namespace>/policy-<slug>:<tag>
```

**Make sure the platform can pull the image.** Two paths:

- **Public registry** (a public ghcr package, a public Docker Hub repo).
  Pull just works, no credentials involved. A new ghcr package starts
  private. Flip it to public at
  `https://github.com/orgs/<org>/packages/container/<package>/settings`
  before any run.
- **Private registry** (private ghcr package, private Docker Hub repo,
  ECR, Artifact Registry). The platform needs a pull credential
  configured on its side. Confirm with the Bifrost team before
  submitting a run.

Either way, a pull failure at run time surfaces as a scheduling or pull
error, not "permission denied", so if the platform can't reach the
image, the run just looks broken.

> **Phase 3 checkpoint:**
> ```
> build_exit_code        = 0
> listening_line         = yes | no | skipped (CPU-only local box)
> source_saved           = yes (where: git commit hash | folder | ...)
> push_confirmed_by_user = yes | no
> push_exit_code         = 0
> visibility            = public | private (action needed)
> ```

---

## Phase 4: Register, then offer a test run

Register the image. Then ask the user whether to submit a scored test run.
Do not submit one on your own.

If `CONTEXT.md` records `local_test_run_possible = no`, add this when
offering the run: there was no test run on the user's machine, so
this run executes the wrap code for the first time. If the run
crashes, check the wrap code before the image.

### Register

**Ask the user to confirm the slug and version before running the CLI.**
Registration creates a catalog entry for their organization, and the tag
becomes an immutable version string.

```sh
manifold policy init <slug> \
  --image <registry>/<namespace>/policy-<slug>:<tag> \
  --minimum-gpu-memory-gb <N>
```

The image tag becomes the version. So
`--image ghcr.io/<your-org>/policy-mypolicy-mybench:0.1.0` registers version
`0.1.0`.

**`--minimum-gpu-memory-gb` does two things.** It filters which runners
can accept this image (the scheduler compares against reported GPU
memory), and it decides whether the container gets GPU access (`--gpus
all` is only added to `docker run` when `minimum_gpu_memory_gb > 0`). A
GPU model registered with 0 starts without GPU access. It will run very
slowly on CPU or crash at model load. Set `<N>` to the model's actual GPU
memory footprint, rounded up.

**Visibility.** By default a new policy is visible only to its own
organization. Add `--visibility public` only if the user asks for it.

### Offer a scored test run

Registration is done. The image is live on the platform, but you have
not yet seen the platform pull it, schedule it, drive it, and score it.
Only a scored run does that.

**Ask the user whether to submit one.** Something like: "The image is
registered as version `X`. Do you want to submit a scored test run? If
so, which registered benchmark should I pair it against? A run costs
cloud time. If the benchmark has a debug variant, I will run that
first."

Do not pick a benchmark. Do not submit on your own. If the user says no,
stop here; the skill is done.

**Check for a debug variant before submitting.** When the user names
a benchmark, run `manifold benchmark list` and look for a debug
variant of the same family: an entry named `debug-` plus the family
name. A debug run costs much less and still makes the platform pull
the image, start it, pair it, and drive episodes. Submit the first
run against the debug variant if one is listed, otherwise against
the named benchmark.

```sh
manifold run submit <policy-slug> <debug-or-benchmark-slug>
manifold run watch <run-id>
```

If the pairing is rejected on the debug variant, submit against the
named benchmark and report the mismatch to the Bifrost team. After a
clean debug run, ask the user whether to submit the full benchmark.

Before submitting:

- The named benchmark must be registered and must have a working image.
  If the run fails immediately with an error naming the benchmark image
  (missing image, benchmark container crash on start), that is a
  benchmark-side problem, not a wrap bug; flag it to the Bifrost team.
- Runs are visible to everyone in the organization; use a clear
  `--name` if the user wants the run labeled.
- There is no hardware check before scheduling. A benchmark that needs
  a specific GPU will be scheduled onto a box without one and fail at
  runtime.

### Validate the results

A completed run does not mean the wrap is correct. Check the actual
output.

**If the run used a debug variant, skip the score comparison.** A
debug suite is too small for a meaningful score. Check episode
completion, first frames, and action magnitudes below. Compare scores
only on the full run.

**Episode completion.** All episodes should reach `completed`:

```sh
manifold run get <run-id> --episodes
```

**First frames.** Dump the first observation frame from each episode. A
run once scored 0.4 in a scene with no background. A mostly black first
frame means the scene did not load.

**Action magnitudes.** Actions should be in the physical range for the
embodiment (millimeters, radians). Actions stuck at the edges (all 1.0 or
all -1.0) suggest missing denormalization.

**Score vs reference.** Compare `mean_success` against the checkpoint's
published or previously measured score on this suite.

**This is the only point in the whole flow where convention bugs become
visible.** A wrong gripper sign, a wrong component order, a wrong rotation
encoding, or a wrong proprioception mapping all pass `check_compatibility`
and `verify`. They only show up here as a score near zero.

A near-zero score on a suite the checkpoint is known to handle means a
wrap bug until proven otherwise. Go back to `wrap-policy` Phase 3, fix
the pipeline or session, bump the tag, and re-enter this skill at
Phase 3.

### If the container ran out of GPU memory

An OOM at runtime means the VRAM floor registered with the version was
too low for the model. The wrap code and the image itself are fine.
Signals:

- `manifold run get <run-id>` shows the run as failed with an
  out-of-memory reason.
- The container's stderr (from the platform's logs, or from a local
  test run) says "CUDA out of memory" (torch),
  "RESOURCE_EXHAUSTED" (jax), or the container was `OOMKilled`
  (visible via `docker inspect` on a local run).

**Ask the user before bumping.** A re-register plus a new run is
another spend cycle. State the current floor, the higher floor you
want (round the observed peak up, add ~20% headroom), and the fact
that the image contents do not change. If the user declines, stop.

If the user says yes, the fix is a re-tag, push, and re-register. No
rebuild needed since the image is unchanged:

```sh
# Same image contents, new tag.
docker tag <registry>/<namespace>/policy-<slug>:<old-tag> \
           <registry>/<namespace>/policy-<slug>:<new-tag>
docker push <registry>/<namespace>/policy-<slug>:<new-tag>

# Re-register the new tag with the higher floor.
manifold policy init <slug> \
  --image <registry>/<namespace>/policy-<slug>:<new-tag> \
  --minimum-gpu-memory-gb <new-floor>
```

Then offer another scored test run against the same benchmark. If it
OOMs again, repeat with a higher floor. Each retry needs a fresh
user yes. Do not silently keep bumping.

Also update `CONTEXT.md`'s peak-VRAM entry for this policy to the
value that actually worked, so future runs of setup-manifold don't lowball
again.

> **Phase 4 checkpoint:**
> ```
> slug                          = ?
> version                       = ? (from image tag)
> minimum_gpu_memory_gb         = ? (> 0 for GPU models)
> register_confirmed_by_user    = yes | no
> test_run_offered_to_user      = yes  (must be yes, offering is required)
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
> container_oom                 = yes | no
> (if yes:)
> vram_bump_confirmed_by_user   = yes | no
> new_tag                       = ?
> new_gpu_memory_floor_gb       = ?
> context_md_vram_updated       = yes | no
> ```

---

## Final checklist

Inputs

- [ ] Wrap passes `check_compatibility` and `verify` under `wrap-policy`
- [ ] Policy slug received from setup-manifold (not invented); image
      name constructed from it
- [ ] manifold-sdk in the image is installed from the policy's
      **manifold-sdk revision** in `.manifold/CONTEXT.md`

Image contents

- [ ] Base image pinned by digest, not by a floating tag like `latest`
- [ ] Project source pinned (git commit `ARG` or snapshot tarball) so
      rebuilds match
- [ ] Only the folders `driver.py` imports from are `COPY`ed;
      `PYTHONPATH` set so those imports resolve
- [ ] Model's Python dependencies pinned (`numpy`, `scipy`, etc.) so
      a rebuild can't silently upgrade them
- [ ] Weights approach decided: fetched at first load *or* baked in
- [ ] No credentials baked into the image (no `ENV HF_TOKEN=...`, no
      copied `~/.aws/credentials`, no copied `~/.huggingface/token`)

Dockerfile rules

- [ ] Dockerfile builds without errors
- [ ] Image built for `linux/amd64` (`docker buildx build --platform
      linux/amd64` on any arm64 machine)
- [ ] On a GPU box, container starts and prints its listening line;
      on a CPU-only box, skipped (rely on Phase 4)
- [ ] Port 8000, bound on `0.0.0.0`
- [ ] `PYTHONUNBUFFERED=1` set
- [ ] Bash present in the image
- [ ] No network fetch at model construction (weights are already local
      by the time the model loads)
- [ ] GPU pre-allocation disabled where the framework does it by
      default (e.g. JAX)

Push and register

- [ ] Tag never reused; Dockerfile and launcher saved before push
- [ ] Push confirmed by the user
- [ ] Registry package visible so the platform can pull the image
- [ ] Registration confirmed by the user; correct
      `--minimum-gpu-memory-gb` (never 0 for GPU models)
- [ ] User was offered a scored test run and given the choice

If the user asked for a test run:

- [ ] Benchmark chosen by the user; submit confirmed before running
- [ ] `manifold benchmark list` checked for a debug variant of the
      named benchmark's family; when one exists, the first run used it
- [ ] Debug run judged on episode completion, first frames, and
      action ranges, with no score comparison
- [ ] Test run completed; score compared to reference
- [ ] First frames and action ranges inspected
- [ ] Container OOM checked (from `manifold run get` and the container's
      stderr)
- [ ] If OOM: user asked before bumping VRAM; image re-tagged and pushed
      (no rebuild); new tag re-registered with a higher
      `--minimum-gpu-memory-gb`; `CONTEXT.md`'s peak VRAM updated to
      what worked
