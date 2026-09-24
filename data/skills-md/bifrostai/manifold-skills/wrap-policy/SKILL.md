---
name: wrap-policy
description: >
  Wrap a researcher's policy for the Manifold platform, then prove it with
  check_compatibility, verify, and a live run of the driver (the live run
  is skipped, with the user's consent, on a machine that cannot run the
  model). Use when the model loads into the built container. For policies where the model
  runs on the user's own inference server (Modal, private HTTPS box),
  use `/wrap-remote-policy` instead.
compatibility: >
  Run this skill from the user's policy project directory, after
  `/setup-manifold` has written `<project>/.manifold/CONTEXT.md`. Everything this
  skill writes goes inside `<project>/.manifold/<slug>/`, where `<slug>`
  is the policy name recorded in `CONTEXT.md`.
---

## Summary

Use the manifold-sdk to write the files that let a Manifold benchmark
run the user's policy. The output is a folder of Python files. Three
kinds of file, each with its own role. The skill uses these three
words as labels for the files throughout:

- The **driver** loads the model and runs it.
- The **profile** describes what the model expects as input and returns
  as output.
- The **pairing** ties one driver-plus-profile to one benchmark. There
  is one pairing file per benchmark the user wants to run against.

Together these files are called the **wrap**.

This skill is for the case where the model loads into the built
container. If the model runs on the user's own inference server (Modal
endpoint, private HTTPS box), use `/wrap-remote-policy` instead.

All conversions and transformations happen in the wrap. The benchmark
side is fixed.

Your task is complete when both `check_compatibility` and `verify` pass AND
the wrap runs cleanly under `evaluate`. The two checks pass specs and dummy
data through the PIPELINE only. Any wrong gripper polarity, action width, or
proprioception can pass them but crash (or fail silently) at runtime, which
is why the live `evaluate` run is mandatory. One exception: on a machine
that cannot run the model, the task is complete when both checks pass, the
`evaluate` run is skipped, and the handoff says so (see "Run the wrap").

## Rules

**Confirm before doing anything else.** First thing after this skill
loads, tell the user in your own words what it will do and why:
adding `manifold-sdk` to the project's deps and creating files under
`<project>/.manifold/`, both so the wrap can run in their own
environment against their own model code. Wait for a yes before
reading `CONTEXT.md` or touching anything.

**Speak to the user in their language, not the SDK's.** The user has
not read the SDK docs. They will not recognize class names, method
names, config fields, or enum values. The skill below names those
identifiers freely because you need them to write correct code.
When narrating progress to the user, translate.

Say things like:
- "I'll write the files that let the benchmark run your policy."
- "The wrap passes the SDK's compatibility check."
- "The test run finished without errors."
- "Some parts of the wrap were not tested by the check."

Not the identifiers from the code blocks below. If the user uses
one of those terms themselves, follow their lead. Otherwise,
describe what happened and why it matters.

**Run in the user's policy directory.** Once the user has said yes,
confirm the current working directory is their policy project: the
same one `/setup-manifold` ran in. Look for `<project>/.manifold/CONTEXT.md` at
the root; if it does not exist, stop and ask the user to run `/setup-manifold`
first. If the current directory does not look like their policy project
(no `pyproject.toml` / `requirements.txt` or similar), ask for the
correct path.

**Read `.manifold/CONTEXT.md` next.** setup-manifold already
interviewed the user and recorded everything wrap-policy would
otherwise ask: package manager, source folders, weights location,
GPU / VRAM, deployment style, registry, and the policy slug and
benchmarks of interest. Read that file before asking the user
anything else; ask only about details `CONTEXT.md` does not already
cover.

**Stop if this is a hosted-endpoint policy.** If `CONTEXT.md` has
`model_runtime = hosted_endpoint`, this skill is the wrong one. Stop
and point the user at `/wrap-remote-policy`, which handles wraps for
policies that run on the user's own inference server.

**Check whether this machine can run the model, before Phase 1.**
Phase 3 finishes with a test run that loads the user's real
checkpoint, and that run needs Linux and an NVIDIA GPU. No earlier
step needs a GPU. `CONTEXT.md` records the answer as
`can_run_model_locally`, and records `os`, `arch`, and `gpu_present`
next to it. If the file predates those fields, run the lookups
yourself: `uname -s`, `uname -m`, `nvidia-smi`.

A machine that cannot run the model does not block the wrap, but the
user decides. If `CONTEXT.md` already records
`local_test_run_possible = no`, the user said yes to this during
`/setup-manifold`. Restate it in one sentence and continue. If the
field is absent, ask now: the wrap cannot be tested on this machine
because it has no GPU, so do they want to proceed anyway? On a yes,
record `local_test_run_possible = no` in `CONTEXT.md`, write the
wrap, run both checks, and skip the test run as described under
"Run the wrap". On a no, stop, and help them move to a machine with
a GPU or switch to `/wrap-remote-policy`.

**Jobs setup-manifold delegated to this skill.** setup-manifold wrote
`CONTEXT.md` and nothing else. Once you've read it, do these before
writing any wrap code:

- Add `manifold-sdk` to the project's dependency file **and** install
  it into the project's environment. Start with the most recent commit
  on the `manifold-sdk` GitHub repository's default branch, then pin
  the dependency to that commit's full SHA. With uv:

  ```
  uv add "manifold-sdk @ git+https://github.com/bifrostai/manifold-sdk.git@<commit>"
  ```

  With plain `requirements.txt`, add the same pinned Git URL, then run
  `pip install -r requirements.txt`. Add a **manifold-sdk revision**
  line with the full SHA to the policy's `### <policy-name>` subsection
  in `.manifold/CONTEXT.md`. This records the SDK revision used for the
  wrap's checks. Use the same revision when building the container.
  Recording without installing (or the reverse) leaves the project
  half-set-up. If the install fails on a dependency conflict, stop and
  hand the error to the user.
- Create the folder `<project>/.manifold/<slug>/`. The slug is in
  `CONTEXT.md`. All wrap files below live inside it.

**Plan the entire task in a to-do list before you start, and update it as
you go.** Use whichever planning tool your harness provides:

- **Claude Code:** `TaskCreate` to seed the plan, `TaskUpdate` to move items
  between `pending` / `in_progress` / `completed`, `TaskList` / `TaskGet` to
  read state.
- **Codex:** use `update_plan` to create and maintain an ordered plan, with
  exactly one item `in_progress` at a time. Keep validation as an explicit item
  until it passes.
- **Other harnesses:** check the harness for a to-do list or planning tool
  before using the fallback below.
- **No planning tool available:** keep the plan as a plain-text checklist in
  your responses and re-post it (with statuses updated) each time you advance.

The intent is (1) to **structure the work** so nothing gets skipped, and
(2) to **stay accountable and informative** by updating the list as steps
start and finish, so the user can follow along without asking.

## Folder structure

All wrap files live under `<project>/.manifold/<slug>/`, where
`<slug>` is the policy name recorded in `CONTEXT.md`:

| File | Description | Imports the model? |
|---|---|---|
| `.manifold/<slug>/driver.py` | endpoint + session | yes |
| `.manifold/<slug>/profile.py` | frozen dataclass: signature, weights, chunk, exec_steps, layouts, `load()` | no |
| `.manifold/<slug>/<benchmark>.py` | pairing file, exports `PROFILE` / `BENCHMARK` / `PIPELINE` (one file per benchmark) | no |

- `driver.py` loads the model onto the GPU and runs it.
- `profile.py` is a lightweight spec describing what the model expects (image sizes, state shape, chunk length, weights path).
- `<benchmark>.py` is the pairing file. It builds the signature and layouts, instantiates the profile, and declares `PROFILE`, `BENCHMARK`, and `PIPELINE`.

`PROFILE` points at the model spec (from profile.py)
`BENCHMARK` points at the test to run
`PIPELINE` is the list of adapters that translate between the benchmark's data and what the model wants.

---

## Phase 1: Understand the policy and target benchmark

Do this before writing any Manifold code. You need a full picture of both sides
to design anything.

### Policy side

**Find the real policy class**, the main policy model code the project runs to
ingest observations and get actions.

**Read any inference or evaluation code** in files and folders like `eval*`,
`infer*`, `scripts*`, `benchmark*`, `env*`, `run*`, `*server*`, `rollout*`. If
there are existing benchmarks or simulation code in the user's policy repository,
note that these are likely NOT Manifold benchmarks. Still, it is necessary to
read them to understand if any conversions and transformations need to be
implemented in the policy wrap, such as image resize, gripper sign and threshold,
and normalization.

**Identify the chunk numbers:**
- *chunk* = actions predicted per forward pass
- *exec_steps* = actions executed in simulation before running the next forward pass

Find the chunk-returning method (e.g. `predict_action_chunk` is common), and
call that from your driver. Let manifold-sdk's queue handle open-loop dispensing.

Manifold's serving contract is strictly open-loop (predict a chunk, execute the
chunk, predict next chunk).

**Write down the action width** from a model source. Check by hand that it
equals `SIGNATURE.action_space.expected_length()`. No SDK assertion exists.

**If the checkpoint is LeRobot-shaped**, run
`manifold.recipes.from_lerobot_checkpoint(path)` first. It returns a
`SignatureSuggestion` with cameras, action dim, and an explicit undetermined
list. Caveats: camera names are LeRobot feature names (not benchmark sensor
names), and `draft_policy_spec` always builds `JointActionSpace` (wrong for EE
policies).

**Check for normalization.** Normalizer artifacts in the checkpoint directory
mean the model does not normalize itself. The method tutorials call may return
normalized values.

**Find the checkpoint** from the project itself. Do not proceed against a known
embodiment mismatch.

**Note observation preprocessing:** resizes, flips, channel swaps, frame
stacking, proprio re-encoding, normalization.

**Declare camera orientation relative to the real scene. Do not declare
it relative to another step in the pipeline.** Ask: if a person stood in
the scene, how would this image look to them? `UPRIGHT` means the image
looks correct. `FLIPPED_VERTICAL` means the image is upside down, because
the rows are in reverse order. If you declare an orientation using the
wrong reference, the checks will still pass, and the policy will score
near zero.

**If the target benchmark is based on MuJoCo or LIBERO, confirm the
orientation of the training data before you design the signature.** Do not
trust code comments. Comments about LIBERO orientation contradict each
other across the ecosystem. The common LIBERO training sets (OpenVLA RLDS,
HuggingFaceVLA/libero) were rotated 180 degrees during conversion, so their
images are horizontally mirrored relative to the real scene. Confirm the
orientation in one of two ways:

- Trace the training data. Find the dataset that was used to train the
  checkpoint, open a few sample frames, and look for printed text or an
  object with a known left and right side. If text in the frames is
  mirrored, the images are mirrored. Do not judge by gravity alone. A
  mirrored scene still looks normal.
- Ask the user. If the user does not know and you cannot reach the
  dataset, stop. Guessing the orientation is the known cause of LIBERO
  scores near zero.

Record the answer, and the evidence for it, in the Phase 1 checkpoint.

### Benchmark side

**Find the target Manifold benchmark** in `manifold.benchmarks` (e.g. LIBERO,
SIMPLER, ROBOCASA). Use the manifold-sdk's `Benchmark`, not the user's policy
project's vendored copy.

**Read the `Benchmark`:** `embodiment.action`, `embodiment.proprioception`,
`sensors` (name, resolution, mount), `instruction`.

**If the benchmark is not available**, stop and notify the user. The benchmark
must be authored first.

> **Phase 1 checkpoint.** Record before designing anything:
> ```
> Policy side:
>   action_width      = ?  (source: file:line)
>   action_space      = EE|Joint|Unified
>   rotation          = ?  (source: file:line)
>   gripper           = ?  (source: file:line)
>   delta             = ?  (source: file:line)
>   frame             = ?  (source: file:line)
>   chunk             = ?  (source: file:line)
>   exec_steps        = ?  (source: file:line)
>   normalization     = yes|no, location: ?
>   checkpoint        = ?
>   cameras           = [{name, shape, orientation}]
>   orientation_evidence = dataset sample | user answer  (REQUIRED for MuJoCo/LIBERO targets; unknown -> stop)
>   instruction       = true|false
>   proprioception    = ee_pose|joint_pos|none
>
> Benchmark side:
>   target_benchmark  = LIBERO|SIMPLER|ROBOCASA|...
>   embodiment_action = {type, rotation, gripper, delta, frame}
>   cameras_published = [{name, shape, orientation}]
>   instruction       = true|false
>
> Feasible: true|false  (if false: why, and stop)
> ```

---

## Phase 2: Design the signature, layouts, and profile

Decide what your wrap will look like before writing any code. Everything here
is a decision, not implementation.

**Which file holds which thing:**

| Thing | File |
|---|---|
| `Profile` class (the dataclass template) | `profile.py` |
| `PolicySignature(...)` instance | pairing file |
| Two `NativeLayout(...)` instances (input + output) | pairing file |
| Profile instance (`POLICYNAME_BENCHMARKNAME = MyProfile(...)`) | pairing file |
| `PROFILE`, `BENCHMARK`, `PIPELINE` module-level names | pairing file |

`profile.py` defines the Profile class and its fields (weights, chunk size,
layouts, and so on). The pairing file creates one and fills those fields with
real values.

### The signature: what the model emits and consumes

The pairing file declares a signature. This is a description of the
action space the model emits and the observation it consumes. In
code it is a `PolicySignature`.

**Stop if the action is not end-effector, joint, or a unified
variant** (in code: `EEActionSpace`, `JointActionSpace`, or
`UnifiedActionSpace(payload=...)`). Same if the state is not
end-effector pose or joint position (`ee_pose` or `joint_pos`).
Anything else is benchmark work, not a wrap.

- Report real-world units. Meters, radians, gripper state. If your model outputs
  normalized values, convert them in the driver before returning.
- The checks won't catch lies about your model. They compare your signature to the
  benchmark, not to what your model actually does. Wrong shapes pass the checks and
  crash at runtime.
- Describe cameras as what the model actually sees, after your pipeline reshapes them.
  Include extra dimensions from frame stacking.
- No proprioception? Say so with an empty `Proprioception()`. Don't invent fake data
  to fill the gap.
- No instruction? Just set `instruction=False`.
- Don't conflate the two things called "chunk":
  - One action holding N steps (almost always 1)
  - Actions predicted per forward pass (often 10)
- The chunk queue needs both `pack` and `unpack`. Skip either and the server crashes.

Spell out every convention field (`rotation=`, `gripper=`, `delta=`, `frame=`)
from the project's eval. Do not copy the benchmark's action object.

### The layout: benchmark observation to model input, model output to action

The benchmark hands the wrap an observation object. The model
expects a dictionary. A layout describes how each dictionary key
gets filled from the observation, and how the model's output is
sliced back into an action. In code these are two `NativeLayout`
instances.

The input layout maps observation channels to dictionary keys. The
output layout maps raw model output back to an action. Key renames
are entries with no ops.

- **Plain `(chunk, dim)` output**: use
  `LayoutEntry(key=..., source=SourceKind.STATE, source_name=None,
  ops=(Slice(start=0, stop=dim),))`. `Slice` takes keyword args only.
  `Slice(0, dim)` raises `TypeError`.
- **`state["ee_pose"]` layout**: `[pos3, rotation, gripper_qpos]`. Widths from
  `ee_step_layout` / `expected_length()`. Be careful, wrong slices don't get
  caught by pre-flight checks.
- **Instruction entry**: use `SourceKind.INSTRUCTION`. Every step, the current
  task's instruction is sent to the policy. Do not cache it on the policy.

### The profile: the wrap's spec

The profile is a small object that carries the signature, the input
and output layouts, the weights location, and two chunk-related
numbers. It also has a `load()` method that opens the model. In
code it is a frozen dataclass satisfying `recipes.PolicyProfile`,
with fields `signature`, `default_weights`, `input_layout`,
`output_layout`, `chunk`, `exec_steps`, and a
`load(weights, device) -> PolicyEndpoint` method.

Defer the driver import into `load()` so `profile.py` imports without
the model stack. Take `device` as a `load()` parameter. Checkpoints
bake in the training device, and the caller passes the runtime one at
load time.

- **`chunk`/`exec_steps` have no check.** Missing `exec_steps` by exact name
  fails at the first step in `advance`. Missing `.profile` on the endpoint
  kills the connection pre-READY: `PairingRejected("policy rejected the
  pairing (no READY)")`.

> **Phase 2 checkpoint:**
> ```
> PolicySignature:
>   action_space        = {type}(rotation=?, gripper=?, delta=?, frame=?, chunk_size=1)
>   action_width_check  = expected_length() == model source width? yes|no
>   proprioception      = {ee_pose: ..., joint_pos: ...}
>   cameras             = [{name, shape, dtype}]
>   instruction         = true|false
>
> NativeLayout input keys:  [list with source_kind and source_name]
> NativeLayout output keys: [list with ops]
>
> Profile: chunk=?, exec_steps=?, default_weights=?
> ```

---

## Phase 3: Implement the wrap

Write the driver, assemble the pipeline, pass both checks, then prove it live.

### File skeletons

Write these three files. Each snippet below is the minimum shape. Fill in the
model-specific logic, then flesh out with the rules that follow.

**`profile.py`**. Frozen dataclass, no model-stack imports at top level:

```python
from dataclasses import dataclass
from manifold.core.native_layout import NativeLayout
from manifold.core.policy import PolicySignature

@dataclass(frozen=True)
class MyProfile:
    signature: PolicySignature
    default_weights: str
    input_layout: NativeLayout
    output_layout: NativeLayout
    chunk: int
    exec_steps: int

    def load(self, weights: str, device: str | None):
        from mywrap.driver import MyEndpoint  # deferred: keeps profile.py light
        return MyEndpoint(self, weights, device)
```

**`driver.py`**. Endpoint (loads the model once) + session (one per runner):

```python
import threading
from manifold.recipes import OpenLoopChunkQueue

class MyEndpoint:
    def __init__(self, profile, weights, device=None):
        self._profile = profile
        self.signature = profile.signature       # expose by identity, not copy
        self._model = load_the_model(weights, device)
        self._lock = threading.Lock()

    @property
    def profile(self):
        return self._profile

    def session(self):
        return MySession(self)

    def forward(self, native):
        with self._lock:
            return self._model.predict_action_chunk(native)   # or whatever

class MySession(OpenLoopChunkQueue):
    def _forward(self, native):
        return self._endpoint.forward(native)
```

**`<policyname>_<benchmarkname>.py`**. The pairing file. Builds the signature
and two layouts, instantiates the profile, then declares `PROFILE`,
`BENCHMARK`, `PIPELINE`:

```python
from manifold.core.pipeline import Pipeline
from manifold.adapters import PackToNativeLayout, UnpackFromNativeLayout
from mywrap.profile import MyProfile

SIGNATURE = PolicySignature(...)
INPUT_LAYOUT = NativeLayout(entries=(...))
OUTPUT_LAYOUT = NativeLayout(entries=(...))

MYPOLICY_MYBENCH = MyProfile(
    signature=SIGNATURE,
    default_weights="...",
    input_layout=INPUT_LAYOUT,
    output_layout=OUTPUT_LAYOUT,
    chunk=...,
    exec_steps=...,
)

PROFILE = MYPOLICY_MYBENCH
BENCHMARK = ...    # the manifold.benchmarks entry
PIPELINE = Pipeline(
    observation=[...],   # benchmark form -> signature's consumed form
    action=[...],        # signature's emitted form -> benchmark's
    pack=PackToNativeLayout(PROFILE.input_layout),
    unpack=UnpackFromNativeLayout(PROFILE.output_layout, SIGNATURE.action_space),
)
```

The rest of this phase is the rules for filling those `...` in correctly.

### Where to put each translation

The benchmark's data won't match what your model expects. Something has to
convert between them: resize a camera, change a rotation format, normalize a
state vector, and so on.

The SDK gives you three places to put those conversions. They trade
off how much the SDK can check for how much freedom you have. Higher
on the list below, the SDK can check what you did. Lower on the
list, you can do anything but the SDK cannot check it.

- **Pipeline adapters**. For reusable typed conversions. Built-in adapters
  cover rotation format, gripper polarity, camera resize/flip/channel-order,
  frame rebase, and frame history. `check_compatibility` inspects the chain
  and validates it.
- **NativeLayout entries**. For building the input dictionary the
  model reads: renaming keys, casting to `float32`, slicing arrays,
  splitting one vector into two. Not typed, so `check_compatibility`
  cannot reason about them, but `verify` pushes data through and
  confirms the shapes come out right.
- **Driver session code**. For per-model idiosyncrasies the SDK has no
  adapter for: normalization stats baked into a specific checkpoint,
  transposing image axes to `(C, H, W)` for torchvision, computing a gripper
  "openness" from raw joint positions. Neither check sees any of this.

Prefer the highest place that fits. Every session-side operation is invisible
to the checks, so name each one in the pairing docstring.

### Driver

`driver.py` defines two classes: an **endpoint** (loads the model once, shared
by all runners) and a **session** (one per runner, holds the chunk buffer).

**Expose the profile's `SIGNATURE` object as `endpoint.signature`**, not a
copy. The live check reads it by identity.

**Take a `threading.Lock` around the model in `forward`.**

**Keep nothing mutable on the endpoint.** Per-episode state goes in the
session or a stateful adapter.

**Chunked policy**: subclass `OpenLoopChunkQueue`, implement only `_forward`,
return the full chunk. Do not build your own chunk buffer.

**Instruction**: `native[key]` arrives as `("text",)`. Unwrap with `str(x[0])`.

**Axis transpose**: no permute op exists; `SwapChannelOrder` is RGB↔BGR only.
Torchvision models need `(C, H, W)`. Transpose in the session.

**Override `reset()`** (calling `super().reset()`) only if the model holds
per-episode state.

### Pipeline

`recipes.resolve(policy, benchmark, adapters)` finds a chain that bridges the
pairing. Use it as a head start when filling in the pipeline's observation and
action adapter lists. It cannot discover stateful adapters (filters them out).

**Convert encodings, never spaces.** Rotation re-encode, gripper polarity,
resize: encodings. Joint↔EE, position↔velocity: different controllers. Wrong
checkpoint, stop.

**No loose convention math in the driver.** Use catalog adapters or write a
custom adapter (see the `manifold.core.adapter` protocol).

**Replicate every step of the project's action postprocessing.** Read
every line. Helpers routinely scale, then negate, then clip.

**Prove each conversion is needed.** Sample the model's output at low,
middle, and high inputs and compare to what the benchmark expects.
If they already match, add no adapter.

**Wire every input the signature consumes.** Zeros for a trained state input
scores zero silently.

### Traps

Three edge cases the checks won't catch.

**`StackFrameHistory` stacks only cameras.** The adapter stacks camera frames
over time, but leaves proprioception alone. If your model wants stacked state
too, either buffer state history yourself in the session, or write a custom
adapter.

**Action adapters that read a value written by observation adapters fail
`verify`.** Adapters can pass data across the two halves through a shared
Python dictionary (`state_key`). `verify` tests the action chain with an
empty dictionary and never runs the observation chain to populate it, so any
such value is missing, so the action adapter either crashes (`verify` fails) or
fakes a default (`verify` passes, but the first action of every real episode
is silently wrong). Workaround: do the conversion in the driver session;
checks don't inspect session code. Real fix: `verify` should run the
observation chain first. File as an SDK bug.

**No absolute↔delta adapter ships.** The SDK has no action adapter that
converts between absolute pose and delta pose. If your model wants deltas but
the benchmark gives absolutes (or vice versa), write the pair yourself: the
observation adapter writes the current `ee_pose` to the shared dictionary,
the action adapter subtracts it. For chunked models (`exec_steps > 1`), only
the first predicted action has a real reference pose to subtract, since the rest
would need faked references. Flag it and stop; don't fake it.

### Check the wrap

Two checks confirm the wrap is well-formed before you try to run it.

- **`check_compatibility`** compares your signature to the benchmark, walking
  through the pipeline's adapter chain. It returns one of three verdicts:
  `COMPATIBLE`, `COMPATIBLE_VIA_PIPELINE` (works after the adapters run), or
  `INCOMPATIBLE`.
- **`verify`** pushes fake data through the pipeline and reports which pieces
  it managed to exercise. Anything under `not_checked` is a piece only a live
  run can prove.

```python
from manifold.core.check import check_compatibility
from manifold.core.verify import verify

report = check_compatibility(SIGNATURE, BENCHMARK, PIPELINE)
verified = verify(SIGNATURE, BENCHMARK, PIPELINE)
```

Fix your code until both pass. **Never change the signature to shut a check
up.** A signature that doesn't actually match the model will pass the checks
but crash the moment a real observation arrives.

Once both pass, confirm the module itself is well-formed:

```sh
python -c "
import importlib
from manifold.recipes import read_pairing
print(read_pairing(importlib.import_module('<your wrap module>')))
"
```

If `verify` reports `not_checked` entries, list them in the handoff. Do not
claim the wrap is "verified" if pieces went untested.

**When `check_compatibility` returns INCOMPATIBLE**, dump both specs
(`model_dump(mode="json")`) and diff key by key. The table below lists the fix
for each kind of mismatch:

| Mismatch | Fix |
|---|---|
| action-space class (Joint vs EE vs Unified) | STOP: different controller |
| `rotation` (action) | `RotationFormatAdapter` |
| `rotation` (proprio) | `ProprioRotationAdapter` |
| `gripper` polarity (action) | `GripperPolarityAdapter`; `GripperThresholdAdapter` for continuous |
| gripper on Unified action | `UnifiedGripperThresholdAdapter` or `DiscreteBinarize` |
| gripper encoding (observed) | `ObservedGripperAdapter` |
| `frame` (proprio) | `FrameRebaseAdapter` / `DynamicFrameRebaseAdapter` |
| camera shape | `ResizeCameras` |
| camera orientation/channel | `Rotate180Cameras` / `FlipVerticalCameras` / `SwapChannelOrder` |
| camera name mismatch | no rename adapter, custom adapter needed |
| camera rank (clip vs frame) | `StackFrameHistory` + clip shape in signature |
| action width (EE → padded) | `BasePinWiden` (EE→Unified); `UnifiedSliceAdapter` (Unified→EE) |
| `chunk_size` | set to 1, the chunk lives in raw output |
| `delta` (single-step) | custom stateful adapter pair (see Traps above) |
| `delta` (chunked) | open problem, flag it |
| `frame` (action) | no adapter, needs kinematics, STOP |
| joint ↔ EE | STOP: different controller |

Both orientation values describe the image relative to the real scene. The
adapter converts from the benchmark's declared orientation to the policy's
declared orientation. `verify` cannot test orientation with synthetic data,
so the policy's declared orientation must come from the evidence in the
Phase 1 checkpoint. Do not guess it.

### Run the wrap (MANDATORY)

The two checks only test the pipeline. Your driver code doesn't run until a
benchmark connects. That's the last thing to prove.

This step is mandatory on any machine that can run the model. Skip it
only when the machine cannot (`local_test_run_possible = no` in
`CONTEXT.md`, or `can_run_model_locally = no`). When you skip it, say
three things in the handoff: the wrap passed both checks, the driver
has not run yet, and the first full test happens when the user
submits a run after `/containerize-wrap`. Do not describe the wrap as
verified.

Use `evaluate` to run the wrap in a single Python process with no server. Any
exception comes back as a traceback:

```python
from manifold.recipes import evaluate
result = evaluate(
    endpoint, BENCHMARK, reset, step,
    pipeline=PIPELINE, episodes=2, max_steps=12,
)
```

You supply `reset` and `step`: `reset()` starts a new episode and returns the
first observation; `step(action)` applies an action and returns
`(next_observation, reward, done, info)`. Together they are a minimal
stand-in for the benchmark's real physics. Use the catalog `Benchmark` for
shapes and write the simplest possible step logic (integrating action deltas
into a pose, rendering a frame that changes each step). The run scores
nothing. It exists to prove the driver runs a full episode without
raising an exception.

**How to describe this run to the user.** Call it "a test run with
dummy inputs to check that the driver runs without errors." Do NOT
say you are "faking the physics" or "using fake data." Those
phrases are correct SDK jargon but read as untrustworthy to a
non-engineer.

**Do not treat episode-to-episode differences as a wrap bug.** With
hand-written `reset` and `step`, the two episodes will not exactly
reproduce each other unless the stand-in is deterministic. That is
expected. The live run only tests one thing. Did the driver run
without raising an exception? If both episodes finish
without an exception, proceed to the handoff. Do not go back and
edit the wrap to make the episodes match.

> **Phase 3 checkpoint:**
> ```
> Pipeline observation adapters: [list, in order]
> Pipeline action adapters:      [list, in order]
> Session-side operations:       [list]
>
> Trap decisions:
>   StackFrameHistory proprio    = handled|n/a
>   Cross-side stateful adapter  = identity-fallback|session-side|n/a
>   Absolute↔delta pair          = written|n/a
>
> Conversions NOT added: [list, with three-extremes justification]
>
> Checks:
>   check_compatibility          = COMPATIBLE|COMPATIBLE_VIA_PIPELINE|INCOMPATIBLE
>     lossless                   = true|false
>     reasons                    = [if any]
>   verify                       = N checked, M failed, K not checked
>     failed                     = [list]
>     not_checked                = [list, quote in handoff]
>   read_pairing                 = success|failure
>
> Live run:
>   episodes                     = ?
>   forward_count                = ? (expected: ceil(steps / exec_steps) * episodes)
>   ran without raising          = yes | no | skipped (machine cannot run the model)
> ```

---

## Final checklist

- [ ] The policy's **manifold-sdk revision** line in
      `.manifold/CONTEXT.md` records the full SDK commit SHA used for
      the checks
- [ ] `read_pairing` accepts the module without the model stack
- [ ] Action width: `expected_length()` == model source width
- [ ] `chunk` and `exec_steps` spelled exactly so on the profile; endpoint
      exposes `.profile`
- [ ] Every convention traces to a line in the project's eval (noted in
      docstring)
- [ ] Signature states what the session returns/consumes, in physical units
- [ ] Split clean: conventions as adapters, structural maps as layout, only
      normalization/axis-order/derived tensors in the session
- [ ] Chunked: `OpenLoopChunkQueue` subclass, only `_forward`, both layouts,
      `chunk_size=1`
- [ ] Three-extremes test for each conversion written and NOT written
- [ ] Nothing mutable on endpoint; `endpoint.signature` is the profile's
      object; instruction unwrapped as `str(x[0])`; `ee_pose` sliced against
      embodiment spec
- [ ] Checks pass; `verify` zero failed (or documented exception);
      `not_checked` quoted in handoff
- [ ] **`evaluate` ran** at least 2 episodes without raising; forward
      cadence counted. Or, on a machine that cannot run the model:
      skipped, `local_test_run_possible = no` recorded, and the
      handoff says the driver has not run
- [ ] Handoff states what was and was not proven

---

## Stop here, hand back to the user

The skill ends at the checklist above. Do **not** invoke another skill
automatically. In particular, do **not** call `/containerize-wrap` on
your own after saying "the wrap is proven"; that skill costs registry
storage and often cloud time, and the user has to opt in first. Each
step in the Manifold flow is a separate skill by design; auto-chaining
skips the user's chance to review.

**Keep the handoff SHORT.** A long summary reads as "we're done." The
user needs to see, at a glance, that there is a next step. Aim for
under 8 lines total, and put the next step in a visible box so it
does not get buried in prose.

Do NOT restate the wrap's design. Do NOT list what was done in Phase
1 or Phase 2. Do NOT review the checks. The user watched those
happen; the handoff is about what is next.

Use this exact shape:

1. **One line: status.** Example: "Wrap is written and passes the
   checks."
2. **One line: what got made.** The module path and the pairing name.
3. **Caveats, only if any.** One line each. `verify` entries under
   `not_checked`, or a credential the user still needs to arrange.
   Skip this entirely if there are none.
4. **Next step, boxed.** Present the next skill as a bordered
   call-out so it stands apart from the prose. For example:

   ```
   ┌────────────────────────────────────────────────────────┐
   │  NEXT: run  /containerize-wrap                         │
   │  Packages the policy and registers it on Manifold.     │
   └────────────────────────────────────────────────────────┘
   ```

   A one-row markdown table works too, if box-drawing characters
   render badly in the harness:

   | Next step | What it does |
   |---|---|
   | Run `/containerize-wrap` | Package the policy and register it on Manifold. |

Then stop. Wait for the user to invoke the next skill.

---

## Reference: import paths

- `manifold.recipes`. `read_pairing`, `launch_server`, `serve`, `evaluate`,
  `run_benchmark`, `run_sharded_benchmark`, `run_episodes`, `write_rollup`,
  `OpenLoopChunkQueue`, `ChunkEndpoint`, `PolicyProfile`, `resolve`,
  `from_lerobot_checkpoint` / `SignatureSuggestion`, `describe`, `Recorder`,
  `dump`, `load`, `NO_RECORDER`
- `manifold.recipes.serving`. `PolicyEndpoint` and `Session` protocols (NOT
  re-exported by `manifold.recipes`)
- `manifold.core.check`. `check_compatibility` returns `Report`
- `manifold.core.verify`. `verify` returns `VerifyReport`
- `manifold.core.pipeline`. `Pipeline`
- `manifold.core.policy`. `PolicySignature`
- `manifold.core.embodiment`. `EEActionSpace`, `JointActionSpace`,
  `UnifiedActionSpace`, `Proprioception`, `EEObservationSpec`,
  `GripperObservationSpec`
- `manifold.core.conventions`. `RotationFormat`, `GripperFormat`, `Frame`
  (pass enum members, never string values)
- `manifold.core.native_layout`. `NativeLayout`, `LayoutEntry`
  (`.from_camera` / `.from_state` / `.from_instruction`), `SourceKind`,
  `Slice`, `Split`, `BatchAxis`, `DtypeCast`, `Component`, `Assemble`
- `manifold.benchmarks`. `ALL`, `LIBERO`, `SIMPLER`, `ROBOCASA`
- `manifold.adapters`. `PackToNativeLayout`, `UnpackFromNativeLayout`,
  `ObservationTap`, `ActionTap` (convention adapters are one level down)
- `manifold.adapters.observation`. `ProprioRotationAdapter`,
  `FrameRebaseAdapter`, `DynamicFrameRebaseAdapter`, `ObservedGripperAdapter`,
  `ResizeCameras`, `Rotate180Cameras`, `FlipVerticalCameras`,
  `SwapChannelOrder`, `StackFrameHistory`
- `manifold.adapters.action`. `RotationFormatAdapter`,
  `GripperPolarityAdapter`, `GripperThresholdAdapter`,
  `UnifiedGripperThresholdAdapter`, `UnifiedSliceAdapter`, `BasePinWiden`,
  `DiscreteBinarize`
- `manifold.lib.rotation.convert`. Driver-side rotation re-encode
- `manifold.lib.gripper`. Action-side gripper remaps
