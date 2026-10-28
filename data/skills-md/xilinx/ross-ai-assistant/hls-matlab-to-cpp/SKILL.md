---
name: hls-matlab-to-cpp
description: Convert MATLAB sample-based code to plain C++ frame-based loops — analyze algorithm, generate C++ that compiles with g++, verify against MATLAB golden, then hand off to /hls-architect for HLS dataflow architecture.
license: MIT
argument-hint: <matlab-file.m> [part=<fpga-part>] [clock=<ns>] [throughput=<target>]
metadata:
  author: "Sai Akhil Ayyagari"
  version: "1.0.0"
---
<!--
Copyright (C) 2026, Advanced Micro Devices, Inc. All rights reserved.
SPDX-License-Identifier: MIT
-->

# MATLAB to C++ Conversion

Convert MATLAB sample-based algorithms into frame-based plain C++ that compiles with g++, then hand off to `/hls-architect` for multi-stage HLS dataflow architecture.

---

## Preamble — Verify Tooling + Capture Required Parameters

### Step 0 — Run ./reference/setup.md in tooling-only mode

All required tooling (Vitis HLS, MATLAB, OpenCV) is verified by the `./reference/setup.md` skill.
At this point in the flow there is no design directory yet, so call `./reference/setup.md` with
`mode=tooling-only` — design discovery and build commands (Steps 2 & 3 of ./reference/setup.md)
are skipped.

```
./reference/setup.md mode=tooling-only
```

The `./reference/setup.md` skill will:
- Source Vitis (and export `$XILINX_VITIS`) — Step 1
- Detect & verify OpenCV install if the testbench will use `cv::imread` — Step 4
- Locate MATLAB and export `$MATLAB_BIN` — Step 5

If `./reference/setup.md` cannot resolve a tool (e.g. MATLAB not on PATH, OpenCV lib path missing),
it prompts the user with `AskUserQuestion`. **Do not proceed until `./reference/setup.md` reports
all three checks passed (or marked N/A).**

After `./reference/setup.md` returns, the following env vars are guaranteed to be set:

| Env var          | Set by         | Used by                                   |
|------------------|----------------|-------------------------------------------|
| `$XILINX_VITIS`  | `./reference/setup.md` Step 1| g++ compile commands in Step 2 & Step 4   |
| `$OPENCV_INCLUDE`| `./reference/setup.md` Step 4| g++ `-I` flag for testbench compile       |
| `$OPENCV_LIB`    | `./reference/setup.md` Step 4| g++ `-L` flag for testbench compile       |
| `$MATLAB_BIN`    | `./reference/setup.md` Step 5| Step 0 — running the user's `.m` files    |

Downstream skills (`/hls-architect`, `/hls-optimize`, `/csim`, `/csynth`, `/cosim`) inherit
this environment — **never re-verify or re-source**.

### Capture pipeline parameters

Parse parameters from `$ARGUMENTS`:

**Expected format:**
```
/matlab-to-cpp <file.m> [part=<fpga-part>] [clock=<ns>] [throughput=<target>]
```

**Examples:**
```
/matlab-to-cpp rgbEdgeDetector.m part=xczu9eg-ffvb1156-2-e clock=3.3 throughput=4400fps
/matlab-to-cpp demosaic.m part=xczu9eg-ffvb1156-2-e clock=3.5
/matlab-to-cpp filter.m
```

**Parse logic:**
1. Extract MATLAB file path (first non-key=value argument)
2. Extract `part=...` → store as `XPART`
3. Extract `clock=...` → store as `CLOCK_NS`
4. Extract `throughput=...` → store as `THROUGHPUT_TARGET`

**No silent defaults.** If any of `<matlab-file>`, `part=`, `clock=`, or `throughput=` is missing from `$ARGUMENTS`, prompt the user with `AskUserQuestion`:

| Missing arg | Question header | Question text |
|---|---|---|
| matlab file        | "MATLAB script" | "Which MATLAB script should I convert? (path to `.m` file)" |
| `part=`            | "FPGA part"     | "FPGA part to target? (e.g. `xczu9eg-ffvb1156-2-e`)" |
| `clock=`           | "Clock period"  | "Clock period in ns? (e.g. `3.3` for ~303 MHz)" |
| `throughput=`      | "Throughput"    | "Throughput target? (e.g. `4400 FPS`, `500 Msps`, `1 GFLOPS`)" |

**Why no defaults:** silent defaults (`xczu9eg`, `3.5 ns`) used to mask user typos and propagate the wrong values into `/hls-architect` and `/hls-optimize`. The prompt forces an explicit choice and surfaces parsing failures immediately.

After all four are resolved, print confirmation:
```
─────────────────────────────────────────────────────
[matlab-to-cpp]  Pipeline parameters
  Source     : <matlab-file>
  Part       : <XPART>
  Clock      : <CLOCK_NS> ns  (≈ <MHz> MHz)
  Throughput : <THROUGHPUT_TARGET>
─────────────────────────────────────────────────────
```
  
## Flow Overview

Print this at the very start so the user can track progress throughout:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[matlab-to-cpp]  Pipeline — <design_name>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Step 0   Run MATLAB simulation → save golden I/O
  Step 0b  Range instrumentation → sim-measured types
  Step 1   Analyze MATLAB algorithm
  Step 2   Generate refactor_1 (plain C++) + verify
  Step 3   Generate refactor_2 (frame-based C++)
  Step 4   Hand off to /hls-architect → /hls-optimize
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Re-print this overview after each step completes with a `✓` next to the completed step so the user always knows where the flow is.

---

## Design Workspace

Before running Step 0, derive `design_name` from the MATLAB script filename (snake_case, no `.m` extension).

Call `./reference/design-layout.md` to orient the workspace:
```
./reference/design-layout.md  design_name=<name>  stage=show
```
This prints the full expected directory tree without creating anything. Confirm the tree with the user, then proceed — each step calls `./reference/design-layout.md` to create its directory before writing files.

---

## Step 0 / 4 — Run MATLAB Simulation (Golden Reference)

```
─────────────────────────────────────────────────────
[matlab-to-cpp]  Step 0 / 4 — Run MATLAB Simulation (Golden Reference)
─────────────────────────────────────────────────────
```

Before converting anything, run the MATLAB simulation to capture golden inputs and outputs. These are used in Step 2 to verify the generated C++.

### Launch MATLAB CLI

Use `$MATLAB_BIN` — exported by `./reference/setup.md` Step 5. Do NOT hardcode a path here; that breaks for any user other than the one whose path was baked in.

```bash
"$MATLAB_BIN" -nodisplay -nodesktop
```

If `$MATLAB_BIN` is empty at this point, `./reference/setup.md mode=tooling-only` was not run (or it failed) — go back and re-run it before continuing.

### Run the Simulation

Once the MATLAB CLI is open, run the `*_runme.m` script in the design directory:

```matlab
>> run('path/to/design_runme.m')
```

**Important:**
- Run **only the simulation section** — do **not** run any MtoHDL Coder or code generation sections
- If the runme script contains both, stop before the HDL/HLS coder calls

### Save Inputs and Outputs

Save both the **input data** (stimulus) and **output data** (golden reference) so the C++ testbench can use the same files:

```matlab
% Save input
fid = fopen('matlab_input.bin', 'wb');
fwrite(fid, input_array, 'uint8');    % match the actual data type
fclose(fid);

% Save golden output
fid = fopen('matlab_golden.bin', 'wb');
fwrite(fid, output_array, 'uint8');
fclose(fid);
```

Keep note of: output dimensions, data type, and border pixels that are undefined (e.g., warmup edges for filter kernels).

### Write to golden/

Call `./reference/design-layout.md  design_name=<name>  stage=golden`

Then copy into `design_name/golden/`:
- All MATLAB source files (`*.m`) from the input design path
- `matlab_input.bin` — saved stimulus
- `matlab_golden.bin` — saved golden reference output

Print before proceeding:
```
─────────────────────────────────────────────────────
[matlab-to-cpp]  Step 0 done — MATLAB Simulation
  Input saved  : golden/matlab_input.bin   (<N> bytes, <dtype>)
  Output saved : golden/matlab_golden.bin  (<N> bytes, <dtype>)
  Dimensions   : <ROWS × COLS or signal length>
  Border/warmup: <KSIZE/2 rows+cols invalid / N/A>
─────────────────────────────────────────────────────
✓ Step 0   Run MATLAB simulation → save golden I/O
  Step 0b  Range instrumentation → sim-measured types   ← NEXT
  Step 1   Analyze MATLAB algorithm
  Step 2   Generate refactor_1 (plain C++) + verify
  Step 3   Generate refactor_2 (frame-based C++)
  Step 4   Hand off to /hls-architect → /hls-optimize
```

---

## Step 0b — Range Instrumentation

```
─────────────────────────────────────────────────────
[matlab-to-cpp]  Step 0b — Range Instrumentation
  0b.0  Detect design type (A: script / B: function-based)
  0b.1  Generate instrumented MATLAB files
  0b.2  Re-run MATLAB, collect RANGE lines
  0b.2b Precision sweep — measure F end-to-end vs golden
  0b.3  Build range table (filter constants/masks)
  0b.4  Derive W and I for each variable
  0b.4b Select Q and O modes (closest to MATLAB double)
  0b.4c Report quantization error (from the 0b.2b measurement)
  0b.4d Size fixed-point multiply intermediates
  0b.5  Present table → user accept / refine loop
─────────────────────────────────────────────────────
```

Capture **min/max of every intermediate variable** from the MATLAB simulation. This drives exact-bitwidth type selection in Step 2 — tight widths reduce area and improve achievable II. Without this, type selection falls back to conservative static analysis.

### 0. Detect design type

Examine the design directory:

- **Type A — script-based:** the top-level runme calls no sub-function `.m` files; all computation is inline. The MATLAB `who` command can see all variables after the script runs.
- **Type B — function-based:** the design has multiple `.m` files that start with the `function` keyword. Sub-function internals are invisible to `who` — only the function's return values appear in the caller's workspace. These require per-function instrumentation.

**Detection rule:** scan the design directory for `.m` files. If more than one file begins with `function` (excluding the runme/tb scripts), it is **Type B**.

### 1. Generate instrumented MATLAB files

#### Type A — append snippet to runme

Add this block to the **end** of the `*_runme.m` script, after the main algorithm has already executed. Do not modify the algorithm itself.

```matlab
% --- Range instrumentation — append after main algorithm ---
fprintf('\n=== RANGE INSTRUMENTATION ===\n');
vars = who;
for k = 1:length(vars)
    v = eval(vars{k});
    if isnumeric(v) && ~isempty(v) && numel(v) > 1
        vmin   = double(min(v(:)));
        vmax   = double(max(v(:)));
        is_int = all(v(:) == floor(v(:)));
        fprintf('RANGE %-30s  min=%12.4f  max=%12.4f  integer=%d\n', ...
                vars{k}, vmin, vmax, double(is_int));
    end
end
fprintf('=== END RANGE INSTRUMENTATION ===\n');
```

#### Type B — auto-generate instrumented sub-functions

Use the two scripts shipped with this repo under `./hls-scripts/`:

```bash
SCRIPTS_DIR="./hls-scripts"
```

Both `gen_all_instr.py` and `gen_matlab_instr.py` ship with the repo — no external download required.

**Step 1: Generate `*_instr.m` for every sub-function:**

```bash
python3 $SCRIPTS_DIR/gen_all_instr.py --dir <design_dir>
```

This scans the design directory, finds all files starting with `function`, skips `*_instr`, `*_runme`, `*_tb`, `*_range`, `*_init`, and generates `<name>_instr.m` for each. The prefix embedded in every `RANGE` line equals the filename stem (e.g., `hb2_fir_i.m` → prefix `hb2_fir_i`).

Print the summary output from `gen_all_instr.py` — it lists every generated file and its tracked variable count.

**Step 2: Create or update an instrumented runner.**

Create `<design_name>_full_instr_runme.m` in the design directory that:
1. Calls `clear functions` at the top to reset all persistent variables
2. Calls the `*_instr` versions of every sub-function (not the originals)
3. Uses the same stimulus and parameters as the original runme
4. Prints any top-level coefficient/LUT ranges directly via `fprintf('RANGE ...')` before the pipeline loop

The RANGE lines are emitted by each `*_instr.m` function automatically at the end of their execution — no additional snippet is needed in the runner.

> **Note on loop-internal constants:** `gen_all_instr.py` tracks ALL named assignments inside the outer loop, including constants like `bit_start = 21` or `offset = fi(1025,...)`. These will appear in the RANGE output with trivial ranges (e.g., `[21,21]`). Ignore them when building the type table — they are not signal-path variables.

> **Note on output_direct temps:** assignments like `cout(i) = expr_with_no_named_intermediate` are captured via injected temp variables named `rng_<array>_N`. These appear as `RANGE prefix_rng_<array>_N` and represent the actual output signal value — keep them in the type table.

### 2. Re-run the simulation

**STOP — do not proceed until MATLAB has actually been re-run.**

The only valid source for the range table is the `RANGE` lines printed to the MATLAB console during this re-run. Any other source is forbidden:

| Forbidden source | Why it fails |
|---|---|
| Prior simulation output | Does not contain loop-internal variables |
| Code inspection / static analysis | Cannot see runtime values or conditional variables |
| Type inference from input ranges | Underestimates multiply/accumulate intermediates |
| Memory of a previous run | Stale — types may have changed |

Run the script:

```bash
# Type A
/path/to/matlab -nodisplay -nodesktop -r "run('path/to/design_runme.m'); exit"

# Type B
/path/to/matlab -nodisplay -nodesktop -r "run('path/to/design_full_instr_runme.m'); exit"
```

**How to verify:** the output must contain `RANGE` lines — one per tracked variable per function. For Type B, lines arrive interleaved as each `*_instr` function finishes its loop; collect all of them.

Collect every line beginning with `RANGE` from the output.

### 2b. Precision sweep — measure F

```
─────────────────────────────────────────────────────
[matlab-to-cpp]  Step 0b.2b — Precision sweep
  Tolerance : 1% (skill default — see 0b.4c thresholds)
─────────────────────────────────────────────────────
```

The `RANGE` lines just collected answer **how big** each variable gets. They cannot answer
**how fine** it needs to be. `F` is measured here, by running the algorithm at a series of
fractional-bit widths and comparing the **final output** against the golden from Step 0.

**Why this is measured and not derived.** `F` is a property of the algorithm and its input,
not of a variable's values. Same tolerance, same peak magnitude, wildly different answers:

| Structure | Input | F for 1% |
|---|---|---|
| 16-tap averaging FIR | white | 10 |
| adjacent-sample difference | white | 6 |
| adjacent-sample difference | oversampled (smooth) | **16** |
| single-pole IIR (`a=0.995`) | white | 8 |

Rows 2 and 3 are the *same code* on the *same amplitude* — a 10-bit swing caused only by
how correlated the input samples are. Nothing in a `min`/`max` pair can see that. Averaging
attenuates the signal while error stays put; differencing cancels the signal while errors
add; recursion accumulates error across iterations. Only running it measures the result.

#### Generate the quantized variants

```bash
# one file per design function; qF is a runtime argument, so one file serves the whole sweep
python hls-scripts/gen_matlab_instr.py <src>.m <src>_q.m <prefix> --quantize
```

This emits `<func>_q(..., qF)` with `x = q_(x, qF);` after every fractional assignment,
where `q_ = @(x,F) round(x .* 2^F) ./ 2^F` — round-to-nearest, matching `AP_RND_CONV`.
Variables detected as integer-valued are left alone (they are already on an exact grid).

#### Sweep driver

```matlab
% ── 0b.2b precision sweep ──────────────────────────────────────────────────
TOL    = 0.01;            % 1% — skill default, same number as the 0b.4c gate
F_LIST = 6:2:24;

ref  = <run the design unmodified, doubles>;      % or load golden/matlab_golden.bin
ref  = double(ref(:));
peak = max(abs(ref));
is_int_golden = all(ref == floor(ref));           % uint8/uint16 golden → bit-exact is reachable

fprintf('\nSWEEP   F   max_abs_err      rel_err   mismatch    SQNR(dB)  status\n');
fprintf('SWEEP  ─────────────────────────────────────────────────────────────\n');

F_pick = NaN;
for F = F_LIST
    out = double(reshape(<run the design with _q variants, passing qF = F>, [], 1));
    e   = out - ref;
    max_abs_err = max(abs(e));
    rel_err     = max_abs_err / peak;
    mismatch    = sum(e ~= 0);
    sqnr        = 20*log10(norm(ref) / max(norm(e), eps));

    ok = rel_err < TOL;
    if is_int_golden, ok = ok && (mismatch == 0); end   % integer golden ⇒ demand bit-exact
    if ok && isnan(F_pick), F_pick = F; end

    status = '';
    if ok, status = 'PASS'; end
    fprintf('SWEEP  %3d  %12.4e  %9.4f%%  %9d  %9.1f  %s\n', ...
            F, max_abs_err, 100*rel_err, mismatch, sqnr, status);
end
fprintf('SWEEP  smallest F meeting %.0f%% tolerance: %d\n', 100*TOL, F_pick);
```

#### Reading the result

```
SWEEP   F   max_abs_err      rel_err   mismatch    SQNR(dB)  status
SWEEP  ─────────────────────────────────────────────────────────────
SWEEP    6    1.9531e-02     4.5139%      4081       26.9
SWEEP    8    4.8828e-03     1.0723%      4079       39.0
SWEEP   10    1.2207e-03     0.2831%      4064       51.0  PASS
SWEEP   12    3.0518e-04     0.0654%      3971       63.0  PASS
SWEEP   14    7.6294e-05     0.0170%      3585       75.1  PASS
SWEEP  smallest F meeting 1% tolerance: 10
```

- **`F_pick`** is the answer. Carry it into 0b.4 as `F`, giving `W = I + F`.
- **SQNR rises ~6 dB per bit.** If it does not, quantization is not what limits accuracy —
  suspect an algorithmic difference, not a width problem.
- **`rel_err` must fall monotonically.** If it plateaus, adding bits will not help; the
  error is structural (an `Inf`/`NaN` path, a saturating clamp, a divide by a small number).
- **Never report only `F_pick`.** The whole table goes to the user at 0b.5 so the accuracy
  vs width trade is theirs to make, not the skill's.

**Margin.** `F_pick` is the *minimum* that met tolerance on *this* stimulus. Apply the same
reasoning as the Margin rule in 0b.4 and offer `F_pick + 2` as the safe default.

**If no F in the list passes:** do not silently extend the sweep forever. Extend once to
`F_LIST = 6:2:40` and re-run. If it still fails, the design is not width-limited — stop and
report that to the user rather than widening blindly.

### 3. Build the range table

**First — print every `RANGE` line exactly as captured, unfiltered:**

```
RANGE <var1>   min=...  max=...  integer=...
RANGE <var2>   min=...  max=...  integer=...
...
```

Do not omit any line. This is the raw capture — show it all before making any decisions.

**Second — classify each variable:**

| Variable | Min | Max | Keep / Filter | Reason if filtered |
|---|---|---|---|---|
| `prefix_acc` | -1.2 | 1.1 | keep | signal-path accumulator |
| `prefix_rng_cout_1` | -1.0 | 1.0 | keep | output_direct temp — actual output value |
| `prefix_bit_start` | 21 | 21 | filter | loop-internal constant (trivial range) |
| `prefix_bit_end` | 32 | 32 | filter | loop-internal constant (trivial range) |
| `prefix_offset` | 1025 | 1025 | filter | loop-internal constant (trivial range) |

**Filter rules:**
- **Loop-internal constants**: min == max (or range is trivially the literal value) — these are assigned inside the loop but never change. Filter them — they have no useful range information for HLS type sizing.
- **Type A scalars**: loop counters, config constants, boolean scalars — filter.
- **Keep everything else**: signal-path variables, accumulators, intermediate products, output_direct temps (`rng_*`).

Build the type derivation table from the **kept** rows only:

| Variable | Min | Max | All-integer? | Chosen HLS type |
|---|---|---|---|---|
| `im1_pre` | -219 | 1107 | yes | `ap_int<12>` |
| `s_horiz` | 0 | 510 | yes | `ap_uint<9>` |
| `coeff_acc` | -0.125 | 0.5 | **no** | `ap_fixed<4,1>` |

### 4. Derive HLS type for each variable

Types come from the **observed range table**, not from reading the MATLAB source. MATLAB
computes everything in double, so the instrumented ranges are the only evidence of what a
variable actually needs.

| Observed range | Type |
|---|---|
| all integers, min ≥ 0 | `ap_uint<N>` |
| all integers, min < 0 | `ap_int<N>` |
| **any** fractional value | `ap_fixed<W,I>` |

Any fractional value at all means `ap_fixed`. Using `ap_int` where MATLAB used a double
breaks bit-exactness — the property this entire flow exists to preserve.

#### Integer bits `I` — one formula for all three types

`I` is fixed entirely by observed magnitude. Compute it the same way regardless of which
of the three types you end up choosing:

```
A = max(|min|, |max|)                            peak magnitude, from the range table

if A == 0:                                       degenerate — see guard below
    I = 1
else:
    I = floor(log2(A)) + 1 + (1 if min < 0 else 0)   the +1 for sign only when min < 0
```

- `ap_uint<N>` / `ap_int<N>` — no fractional bits, so `N = I`
- `ap_fixed<W,I>` / `ap_ufixed<W,I>` — `I` is this value, and `W = I + F`

**`I` may be zero or negative — that is legal and frequently correct.** A signal whose peak
is below 1.0 needs no integer bits at all; a peak of `4.97e-3` gives `I = -7`, placing the
binary point outside the word so that all `W` bits are fractional.

This matters for precision, not area: **`F = W - I`**, so every integer bit allocated to
range the signal never reaches is a fractional bit you do not get. Holding `W = 34`, an
`I` of `1` leaves `F = 33` (LSB `1.16e-10`); the correct `I` of `-7` leaves `F = 41`
(LSB `4.55e-13`) — same width, 8 more bits of resolution.

> **Guard — `A = 0`.** If the variable is all zeros across the whole simulation — a signal
> that never activates on this stimulus, a branch that is never taken, a coefficient array
> that is genuinely zero, or a constant `0` fed in as input — then `min = max = 0`, so
> `A = 0` and `log2(0) = -inf`. The formula explodes: `I` comes out `-inf`, and any width
> derived from it is garbage.
>
> Special-case it before evaluating the log: **`if A == 0 → I = 1`** (a lone sign bit, or
> a single integer bit if unsigned). One bit is enough to represent zero exactly, and the
> type stays legal so downstream arithmetic and `W = I + F` still work.
>
> **But treat it as a signal, not just a number.** `A = 0` almost always means the
> instrumentation never exercised that variable. Before accepting `I = 1`, check which case
> you are in:
>
> | Cause | What to do |
> |---|---|
> | Stimulus never drives this path (dead branch, unused mode) | Range is **not trustworthy** — the variable is unsized, not zero-sized. Re-run 0b.2 with stimulus that exercises it, or carry it forward marked unverified. |
> | Variable is genuinely and permanently zero | `I = 1` is correct. Better: fold the constant away — it is not a signal, it is a literal. |
> | Assignment executed but the value happened to be 0 every time | Same as row 1 — the stimulus is too narrow. Widen it. |

> **Related degenerate case — `min = Inf`, `max = -Inf`.** This is *not* `A = 0`, and it is
> important not to confuse the two. The generated tracker seeds `mn_x = inf; mx_x = -inf;`
> before the loop, so a variable whose tracking line **never executed** prints:
>
> ```
> RANGE  prefix_myvar    min=           Inf  max=          -Inf  integer=0
> ```
>
> `A = max(|Inf|, |-Inf|) = Inf`, which blows up in the opposite direction. Causes: the
> assignment sits in a branch the stimulus never took, or the injection landed inside a
> `...` line continuation and silently broke. **Never size a type from an `Inf` row** — it
> is an instrumentation result, not a range measurement. Fix or re-stimulate, then re-run.
>
> The two are distinguishable straight from the RANGE line, so use that:
> `min=0, max=0` → assignment ran, value was always zero. `min=Inf, max=-Inf` → assignment
> never ran at all.

Report every `A = 0` and every `Inf` variable explicitly in the 0b.5 table with the cause
identified — never let one pass through silently as a normal sized row.

> **Exactness:** the rule is exact except when `min` is an exact negative power of two
> (`[-128, 127]` → 9 instead of 8). One bit conservative there, never unsafe — it can
> over-allocate but never under-allocate, so `AP_WRAP` stays safe by construction.

#### ap_fixed<W,I> sizing

**Formula:**
```
A = max(|min|, |max|)
I = floor(log2(A)) + 1 + (1 if min < 0 else 0)   (integer bits incl. sign; may be <= 0)
F = F_pick                                       measured in 0b.2b — never derived here
W = I + F
Example: range [-0.125, 0.5] → A = 0.5, min < 0
         I = floor(log2(0.5)) + 1 + 1 = -1 + 2 = 1
         F = 3  (from the 0b.2b sweep)  →  ap_fixed<4, 1>
```

> **`F` is never computed from the range table.** It is `F_pick` from the 0b.2b sweep.
> There is no valid formula for `F` in terms of `min`/`max`, for three reasons:
>
> 1. **The information is not there.** A rule over "the values a variable took" needs every
>    value; the `RANGE` lines carry exactly two numbers per variable.
> 2. **The question often has no answer.** `0.7` and `0.1` have no finite binary expansion —
>    no `F` represents them exactly, so "bits needed to be exact" is undefined for most data.
> 3. **`F` is a property of the algorithm, not the variable.** Quantization error propagates:
>    averaging attenuates signal while error stays put, differencing cancels signal while
>    errors add, recursion accumulates. Two designs with identical range tables need
>    different `F`. See the measured table in 0b.2b — the same code on the same amplitude
>    ranged from `F = 6` to `F = 16` purely with input correlation.
>
> `min`/`max` answer `I` exactly. They cannot answer `F` at all. `W = I + F` joins the two.

**Common ranges:**
```
[0,   1.0]  → ap_ufixed<12, 1>   A=1.0, unsigned: floor(0)+1     = 1 int, 11 frac
[-4.0, 4.0] → ap_fixed <16, 4>   A=4.0, signed:   floor(2)+1+1   = 4 int, 12 frac
[0,   6.0]  → ap_ufixed<16, 3>   A=6.0, unsigned: floor(2.58)+1  = 3 int, 13 frac
```

Note how the third row is unsigned (`min = 0`) — spending a sign bit it never uses would
cost a fractional bit. And if the first row is *measured* at `[0.027, 0.992]` rather than
declared as `[0, 1.0]`, then `A = 0.992` and `I = floor(-0.012) + 1 = 0` →
`ap_ufixed<12, 0>`, range `[0, 1)`, all 12 bits fractional. That is the correct answer, not
a bug — but see the **Margin rule** below before committing to it.

**CRITICAL - Do NOT "optimize" by converting to integers:**

Given a MATLAB weighted sum `y = 0.25*a + 0.5*b + 0.25*c` with observed range
`[0.027, 0.992]`:

❌ **WRONG:**
```cpp
// "I'll convert to uint8 for hardware efficiency"
ap_uint<8> y = (64*a + 128*b + 64*c) >> 8;  // [0, 255] range
// ❌ This changes the numeric domain → different values → mismatches
```

✅ **CORRECT:**
```cpp
// Match MATLAB's domain
ap_ufixed<12,1> y = 0.25*a + 0.5*b + 0.25*c;  // [0, 1] range
// ✅ Same numeric domain → same values → bit-exact match
```

**Why this matters:**
- Rescaling [0,1] to [0,255] changes ALL downstream computations
- Any nonlinear step (`sqrt`, compare, saturate) gives **different results** in a different domain
- Constants calibrated for [0,1] won't work in the [0,255] domain
- Result: mismatches in csim, failed verification

**Rule:** If MATLAB uses floating-point, C++ uses `ap_fixed`. Period.

---

> **Margin rule:** Add 1 extra bit beyond strict minimum when observed range comes from a single small test image. Larger production images may push extremes slightly further.

### 4b. Select Q (quantization) and O (overflow) modes

```
─────────────────────────────────────────────────────
[matlab-to-cpp]  Step 0b.4b — Q/O mode selection
─────────────────────────────────────────────────────
```

The full fixed-point type is `ap_fixed<W, I, Q, O>`. Default is `AP_TRN, AP_WRAP`. Select Q and O to minimise deviation from MATLAB's double-precision result.

Reference — all valid modes (from `ap_decl.h`):

| Q mode | Behaviour |
|---|---|
| `AP_TRN` | Truncation toward −∞ (default) |
| `AP_TRN_ZERO` | Truncation toward zero |
| `AP_RND` | Round toward +∞ |
| `AP_RND_ZERO` | Round toward zero |
| `AP_RND_MIN_INF` | Round toward −∞ |
| `AP_RND_INF` | Round away from zero (matches MATLAB `round()`) |
| `AP_RND_CONV` | Convergent / banker's rounding — round half to even (matches IEEE 754, MATLAB's default double arithmetic) |

| O mode | Behaviour |
|---|---|
| `AP_WRAP` | Wrap-around (default) |
| `AP_SAT` | Saturate at ±max |
| `AP_SAT_ZERO` | Saturate to zero on overflow |
| `AP_SAT_SYM` | Symmetrical saturation |
| `AP_WRAP_SM` | Sign-magnitude wrap |

#### Overflow mode O — always derive from the range table

| Condition | O mode | Reason |
|---|---|---|
| Range table proves I bits cover min/max | `AP_WRAP` (default) | Overflow never occurs → no saturation hardware, no overhead |
| Intermediate result can temporarily exceed I bits | Widen I instead | AP_SAT masks bugs — fix the width, do not hide the overflow |
| Final output boundary (e.g. clip to [0, 255]) | Explicit `if/else` in C++ | More readable than AP_SAT and visible in code |

**Rule: size I correctly from the range table and use AP_WRAP. Never use AP_SAT to compensate for an undersized I.**

#### Quantization mode Q — derive from how MATLAB computes each variable

MATLAB computes in IEEE 754 double precision. Q determines how the HLS type handles fractional bits that are dropped when assigning to a narrower fixed-point type.

Inspect the MATLAB expression that produces each variable:

| MATLAB operation | Q mode | Reason |
|---|---|---|
| General arithmetic (`+`, `-`, `*`, `/N`) | `AP_RND_CONV` | IEEE 754 default is round-half-to-even — AP_RND_CONV matches exactly |
| Power-of-2 divide then store (`/8`, `/16`) | `AP_RND_CONV` | MATLAB rounds the double result before storing; plain `>> N` in C++ truncates (AP_TRN) — use AP_RND_CONV to recover 1 LSB accuracy |
| Explicit `floor(x)` | `AP_TRN` | MATLAB truncates toward −∞; AP_TRN does the same |
| Explicit `round(x)` | `AP_RND_INF` | MATLAB rounds half away from zero; AP_RND_INF matches |
| Explicit `fix(x)` / `int(x)` | `AP_TRN_ZERO` | MATLAB truncates toward zero; AP_TRN_ZERO matches |
| Explicit `ceil(x)` | implement as `floor(x) + 1` or negate-floor-negate in C++ | No direct HLS mode |
| Pure integer arithmetic (no fractional bits drop) | `AP_TRN` (default) | Q is irrelevant when F=0; leave at default |

**Default when unsure:** `AP_RND_CONV` — it is the IEEE 754-compatible choice and closest to MATLAB's double-precision arithmetic. It costs one extra adder per assignment versus `AP_TRN`.

> **Note:** `AP_RND` (round toward +∞) is **not** the same as round-to-nearest. It biases positive results upward. Do not use it as a substitute for `AP_RND_CONV`.

#### Full type examples

```cpp
// xcorr: fractional, general MATLAB arithmetic → AP_RND_CONV, sized from range table
// peak is 4.97e-3, so I = floor(log2(4.97e-3)) + 1 = -8 + 1 = -7  → all 34 bits fractional
ap_ufixed<34, -7, AP_RND_CONV, AP_WRAP>  xcorr_val;

// accumulator: fractional intermediate — widen I to avoid overflow
ap_fixed<20, 4, AP_RND_CONV, AP_WRAP>    acc;

// result of explicit floor() in MATLAB
ap_fixed<16, 8, AP_TRN, AP_WRAP>         floored_val;

// result of explicit round() in MATLAB
ap_fixed<16, 8, AP_RND_INF, AP_WRAP>     rounded_val;

// index: unsigned integer — Q/O irrelevant
ap_uint<13>                               idx;

// final output clamp [0, 255] — done explicitly, not via AP_SAT
ap_uint<8> out_px;
if      (result < 0)   out_px = 0;
else if (result > 255) out_px = 255;
else                   out_px = (ap_uint<8>)result;
```

Update the range table to include the full type with Q and O:

| Variable | Min | Max | All-integer? | HLS type (full) |
|---|---|---|---|---|
| `xcorr` | 3.14e-10 | 4.97e-3 | no | `ap_ufixed<34,-7,AP_RND_CONV,AP_WRAP>` |
| `s_horiz` | 0 | 510 | yes | `ap_uint<9>` |
| `coeff_acc` | -0.125 | 0.5 | no | `ap_fixed<4,1,AP_RND_CONV,AP_WRAP>` |

### 4c. Report quantization error

```
─────────────────────────────────────────────────────
[matlab-to-cpp]  Step 0b.4c — Quantization error check
  Source : measured 0b.2b sweep (not predicted)
─────────────────────────────────────────────────────
```

For every fractional variable, report the grid the chosen type sits on:

```
F            = W - I                          (fractional bits, = F_pick from 0b.2b)
LSB          = 2^(-F)
max_q_error  = 0.5 × LSB   (AP_RND_CONV)
             = 1.0 × LSB   (AP_TRN / AP_TRN_ZERO)
```

| Variable | HLS type | LSB | Max q-error |
|---|---|---|---|
| `xcorr` | `ap_ufixed<34,-7,AP_RND_CONV,AP_WRAP>` | 4.55e-13 | 2.27e-13 |
| `coeff_acc` | `ap_fixed<4,1,AP_RND_CONV,AP_WRAP>` | 0.125 | 0.0625 |

These are **descriptive, not a verdict.** They say how coarse each variable's grid is. They
do not say whether the design is accurate — error propagates, so a coarse grid on a variable
whose error cancels downstream is fine, and a fine grid on one that feeds a subtraction is
not. The accuracy verdict is the measured 0b.2b sweep, and only that.

#### The gate

Carry the sweep table forward verbatim. This is what decides:

| F | max_abs_err | rel_err | mismatch | SQNR (dB) | Status |
|---|---|---|---|---|---|
| 6 | 1.9531e-02 | 4.5139% | 4081 | 26.9 | ✗ |
| 8 | 4.8828e-03 | 1.0723% | 4079 | 39.0 | ✗ |
| 10 | 1.2207e-03 | 0.2831% | 4064 | 51.0 | ✓ |
| 12 | 3.0518e-04 | 0.0654% | 3971 | 63.0 | ✓ |
| 14 | 7.6294e-05 | 0.0170% | 3585 | 75.1 | ✓ |

**Thresholds** — applied to the sweep's measured `rel_err`, error at the design output
relative to peak output:

| Measured rel_err | Action |
|---|---|
| < 1% | ✓ acceptable |
| 1% – 10% | ⚠ present to the user with the adjacent rows so they can trade width for accuracy |
| > 10% | ✗ do not offer this row as a default |

`F_pick` is the smallest ✓ row. Recommend `F_pick + 2` as the default and let the user choose
— see 0b.5.

> **Do not compute `rel_err` from `LSB / |signal_min|`.** The obvious-looking metric
> `max_q_error / |signal_min|` — error relative to the smallest observed sample — is wrong
> and was removed from this step. It grades a fixed-point type on *relative* precision, which
> only floating-point provides:
>
> | | precision model | error at a small sample |
> |---|---|---|
> | `ap_fixed` | uniform **absolute** grid — `LSB` is the same everywhere | grows without bound as the sample shrinks |
> | `float`/`double` | uniform **relative** — the exponent rescales | constant fraction of the sample |
>
> A correctly-sized fixed-point type fails that test, and the failure says nothing about
> whether the design is accurate. Concretely, the generated tracker records **every**
> assignment including initialization, so `acc = 0;` puts `min = 0` in the range table for
> essentially every accumulator in every design. `max_q_error / 0 = Inf` → every accumulator
> fails unconditionally, and any "add `ceil(log2(rel_err/0.01))` bits" remedy asks for
> infinitely many. The same happens for any bipolar signal crossing zero and any image with
> a black pixel. Measure the output; do not predict from the range table.

#### Width ceiling

| Limit | Value | Nature |
|---|---|---|
| `ap_[u]int` / `ap_[u]fixed` `W` | **1024 bits** default | hard, but raisable to 4096 via `#define AP_INT_MAX_W` before including `ap_int.h` |
| Native/DSP-friendly operators | ~64 bits | **QoR advisory, not a limit** — beyond this, operators decompose into multiple DSPs and carry chains, costing area and Fmax |

Source: UG1399, *Overview of Arbitrary Precision Integer Data Types*. If a design genuinely
needs `W > 64`, that is legal and synthesizes — flag the QoR cost to the user, do not refuse
the width.

---

### 4d. Fixed-point multiplication intermediates

```
─────────────────────────────────────────────────────
[matlab-to-cpp]  Step 0b.4d — Multiply intermediate sizing
─────────────────────────────────────────────────────
```

Fixed-point multiplication changes the value range: `a × b` produces a result with `W_a + W_b` total bits and `I_a + I_b` integer bits. If the result is immediately assigned to a narrower type, fractional bits are silently dropped — MATLAB never loses these bits (it stays in double throughout).

**Rule: any intermediate that is the result of a multiply must be declared at the full product width before any narrowing.**

For every multiply in the MATLAB algorithm, identify the operands and declare the intermediate:

```cpp
// MATLAB: result = a * b
// a: ap_fixed<Wa, Ia, Qa, Oa>
// b: ap_fixed<Wb, Ib, Qb, Ob>

ap_fixed<Wa+Wb, Ia+Ib, AP_RND_CONV, AP_WRAP> prod = a * b;

// Only then narrow — after the full-precision product is captured:
ap_fixed<W_out, I_out, AP_RND_CONV, AP_WRAP> result = prod;
```

For the peakPicker case — comparing `xcorr[i] >= threshold[i]`:
- This is a comparison, not a multiply — no intermediate needed
- If an accumulation or scale factor is added later (e.g. `xcorr * weight`), declare `prod` at full width first

Include a multiply-intermediate column in the range table where applicable:

| Multiply | Operand types | Intermediate type | Output type |
|---|---|---|---|
| `a * b` | `ap_fixed<16,4>` × `ap_fixed<16,4>` | `ap_fixed<32,8,AP_RND_CONV,AP_WRAP>` | `ap_fixed<16,4,AP_RND_CONV,AP_WRAP>` |

---

### 5. Present to user and validate

Print the completed table. `I` is derived from the measured range; `F` comes from the
measured sweep. Show both sources so the user can see which number came from where:

```
─────────────────────────────────────────────────────
[matlab-to-cpp]  Step 0b — Types + Measured Accuracy
  Variables instrumented : <N>
  F source : 0b.2b sweep @ F=<F_pick>   Tolerance : 1%

  Variable         Sim range              HLS type                              LSB        Max q-err
  ──────────────────────────────────────────────────────────────────────────────────────────────────
  xcorr            [3.14e-10, 4.97e-3]   ap_ufixed<34,-7,AP_RND_CONV,AP_WRAP>  4.55e-13   2.27e-13
  threshold        [1.53e-5,  4.40e-3]   ap_ufixed<34,-7,AP_RND_CONV,AP_WRAP>  4.55e-13   2.27e-13
  ...

  End-to-end accuracy vs golden (measured, 0b.2b):
   F    max_abs_err     rel_err   mismatch   SQNR(dB)
   6     1.9531e-02     4.5139%       4081       26.9
   8     4.8828e-03     1.0723%       4079       39.0
  10     1.2207e-03     0.2831%       4064       51.0   ← smallest meeting 1%
  12     3.0518e-04     0.0654%       3971       63.0
  14     7.6294e-05     0.0170%       3585       75.1

  Multiply intermediates:
  <a> × <b>  →  ap_fixed<Wa+Wb, Ia+Ib, AP_RND_CONV, AP_WRAP>   (full product width)

─────────────────────────────────────────────────────
```

Then ask the user to pick a row, using **AskUserQuestion**. Every option must be a real row
of the sweep, labelled with its measured consequence — never an abstract accept/refine:

```
Which precision do you want to build at?

  [F=12]  +2 bits margin — rel_err 0.065%, SQNR 63 dB     (recommended)
  [F=10]  minimum meeting 1% — rel_err 0.283%, SQNR 51 dB
  [F=14]  rel_err 0.017%, SQNR 75 dB — costs 2 more bits per variable
  [F=8]   below tolerance: rel_err 1.07% — only if width is critical
```

**Rules for building the options:**

1. **Recommend `F_pick + 2`**, not `F_pick`. `F_pick` is the minimum that passed on *this*
   stimulus; two bits of margin costs little and absorbs a wider input distribution. Same
   reasoning as the Margin rule for `I` in 0b.4.
2. **Offer `F_pick` itself** as the tight option.
3. **Offer one row above** so the user can buy accuracy if they want it.
4. **Offer one row below tolerance** only when it is close (1–10%), labelled as such. Never
   offer a `> 10%` row.
5. **If the golden is integer-valued** (uint8/uint16 image), state bit-exactness explicitly —
   `mismatch = 0` is a stronger and more meaningful claim than any percentage:
   `[F=14] bit-exact vs golden — 0 of 262144 pixels differ`.
6. **Never present a row the sweep did not actually run.** If the user wants a width not in
   `F_LIST`, extend `F_LIST` and re-run 0b.2b — do not interpolate.

Wait for the user's answer, then set `F = <chosen>` and `W = I + F` for every fractional
variable. **Refining is cheap now** — it is re-reading a row of a table that already exists,
not a Step 0 re-run. Only return to 0b.2b if the user asks for an `F` outside the swept list.

Once a row is chosen:

```
─────────────────────────────────────────────────────
[matlab-to-cpp]  Step 0b done — Range Instrumentation
✓ Step 0   Run MATLAB simulation → save golden I/O
✓ Step 0b  Range instrumentation → sim-measured types
  Step 1   Analyze MATLAB algorithm                     ← NEXT
  Step 2   Generate refactor_1 (plain C++) + verify
  Step 3   Generate refactor_2 (frame-based C++)
  Step 4   Hand off to /hls-architect → /hls-optimize
─────────────────────────────────────────────────────
```

Save the accepted range table in memory — Step 2 references it for every intermediate type decision.

---

## Step 1 / 4 — Analyze the MATLAB Code

```
─────────────────────────────────────────────────────
[matlab-to-cpp]  Step 1 / 4 — Analyze MATLAB Code
─────────────────────────────────────────────────────
```

Read the MATLAB code and extract:

1. **Algorithm intent** — what does it compute? (filter, transform, color space, etc.)
2. **Inputs and outputs** — types, dimensions, value ranges
3. **Sample-based operations** — identify every operation that works on a single pixel/sample at a time vs. entire frame
4. **Neighborhood access** — does it use `imfilter`, `conv2`, sliding windows, or index expressions like `A(i-1:i+1, j-1:j+1)`?
5. **Filter coefficients** — are they fixed at compile time or runtime parameters?
6. **Control flow** — loops, conditionals, switch/case based on pixel position (Bayer phase, color channel, etc.)

---

Print before proceeding:
```
─────────────────────────────────────────────────────
[matlab-to-cpp]  Step 1 done — MATLAB Analysis
  Algorithm    : <what it computes>
  Input        : <type, dimensions>
  Output       : <type, dimensions>
  Operations   : <sample-based ops identified>
  Neighborhood : <sliding window / none>
  Coefficients : <fixed at compile time / runtime>
  Assumptions  : <any assumptions made>
  Any gaps     : <MATLAB constructs with no direct HLS equivalent — or "none">
─────────────────────────────────────────────────────
✓ Step 0   Run MATLAB simulation → save golden I/O
✓ Step 0b  Range instrumentation → sim-measured types
✓ Step 1   Analyze MATLAB algorithm
  Step 2   Generate refactor_1 (plain C++) + verify    ← NEXT
  Step 3   Generate refactor_2 (frame-based C++)
  Step 4   Hand off to /hls-architect → /hls-optimize
```

## Step 2 / 4 — Generate `refactor_1` (Plain C++) + Testbench, Verify Against MATLAB

```
─────────────────────────────────────────────────────
[matlab-to-cpp]  Step 2 / 4 — Generate refactor_1 (Plain C++) + Verify
─────────────────────────────────────────────────────
```

Before writing HLS code, generate **`refactor_1`** — a plain C++ implementation (no HLS pragmas, no `ap_int`, no streams) — and a testbench that mirrors the MATLAB simulation exactly. Verify correctness first.

### `refactor_1` — Plain C++ File

- Translate the MATLAB algorithm to HLS C++ using types chosen from the **Step 0b simulation range table**. For each intermediate variable, the simulation result drives the choice among exactly three candidates:
  - **`ap_uint<N>`** — simulation shows min ≥ 0 and all values are integer
  - **`ap_int<N>`** — simulation shows min < 0 and all values are integer
  - **`ap_fixed<W,I>`** — simulation shows fractional values, or the MATLAB path uses `double`/`float` (which are forbidden in synthesis and must be replaced)
  - For variables not captured by the range table (scalars, loop counters): apply the same three-way choice using static analysis of the MATLAB code

#### Generate Typedefs from Range Table

For **every variable** in the accepted Step 0b range table, generate a typedef:

```cpp
// Generate one typedef per unique type from range table
typedef ap_ufixed<W1, I1, AP_RND_CONV, AP_WRAP> input_t;
typedef ap_fixed<W2, I2, AP_RND_CONV, AP_WRAP>  intermediate_t;
typedef ap_ufixed<W3, I3, AP_RND_CONV, AP_WRAP> output_t;
// ... one typedef for each variable in the range table
```

**Naming convention**:
- Use the MATLAB variable name as the suffix: `<var>_t`
- For shared ranges (variables with identical min/max), use one typedef with a descriptive name

#### Apply Types to All Variables

Use the generated typedefs for:
1. **Output arrays**: Must match the derived output types from Step 0b
2. **Intermediate variables**: Loop-internal calculations use the range-table types
3. **Multiply products**: Declare at full product width before narrowing

**✅ CORRECT**: Use derived types from range table:

```cpp
static intermediate_t buffer[FRAME_PIXELS];
static result_t       results[FRAME_PIXELS];

void my_kernel(input_t input_arr[FRAME_PIXELS],
               output_t output_arr[FRAME_PIXELS])  // ← use derived output_t, not float
{
    for (int i = 0; i < FRAME_PIXELS; i++) {
        intermediate_t temp = buffer[i] * buffer[i];  // ← use typed intermediate
        output_arr[i] = process(temp);
    }
}
```

**❌ WRONG**: Don't fall back to float for fixed-point variables:

```cpp
// ❌ Defeats the purpose of Step 0b range instrumentation
float output_arr[FRAME_PIXELS];
float intermediate = ...;
```

- Use the same logic, same coefficients, same normalization as the MATLAB code
- No HLS pragma constructs yet — this is a functional translation, but with HLS-compatible types
- **Always use row-major scan order** (row outer, col inner) — even if the MATLAB code uses column-major. Row-major is the HLS standard for image processing.
- **Output dimensions must match input dimensions exactly** — read `ROWS` and `COLS` from the input image; do NOT add extra rows or columns for border padding. If the algorithm has a warmup border (e.g., filter kernels), exclude those border pixels from the error comparison — do not change the output array size.

```cpp
// Row-major flat loop — always use this pattern
for (int k = 0; k < ROWS * COLS; k++) {
    int row = k / COLS;
    int col = k % COLS;
    ...
}
```

> **Pattern-string indices:** a MATLAB expression like `find(str == 'r') - 1` must be
> resolved outside the kernel — pre-encode it as an integer and pass it in as an
> `ap_uint<2>` parameter. Do not search a character array inside the kernel; it
> synthesises, but it is wasted logic and the wrong interface.

### Testbench

The testbench must mirror the MATLAB `*_runme.m` structure — same input data, same comparison against the golden output.

**Shape mismatch warning:** MATLAB stores arrays in **column-major** order; C++ iterates in **row-major** order. A direct flat index comparison will fail even on a correct implementation. The comparison must map between the two orderings:

```
MATLAB flat index (column-major): j = col * ROWS + row
C++    flat index (row-major):    i = row * COLS + col
```

```cpp
int main() {
    // 1. Load input — MATLAB saves in column-major order.
    //    Reorder to row-major for C++ kernel.
    load_bin("matlab_input.bin", matlab_in, FRAME_PIXELS);  // column-major
    for (int row = 0; row < ROWS; row++)
        for (int col = 0; col < COLS; col++)
            in_buf[row * COLS + col] = matlab_in[col * ROWS + row];

    // 2. Load MATLAB golden output (column-major)
    load_bin("matlab_golden.bin", golden, OUT_PIXELS);

    // 3. Run the C++ function TWICE. This testbench is carried forward
    //    unchanged to /hls-architect, where cosim needs back-to-back calls
    //    to report an Initiation Interval. g++ measures no II here.
    int total_mismatches = 0;
    for (int call = 1; call <= 2; call++) {
        my_kernel(in_buf, out_buf);

        // 4. Compare: map C++ row-major index to MATLAB column-major index.
        //    Compare in double. NEVER cast the kernel output to int — that
        //    truncates ap_fixed fractional bits and hides sub-LSB error,
        //    which is exactly the error the 0b.2b sweep was sizing.
        int mismatches = 0;
        for (int row = 0; row < ROWS; row++) {
            for (int col = 0; col < COLS; col++) {
                int cpp_idx    = row * COLS + col;   // C++ row-major
                int matlab_idx = col * ROWS + row;   // MATLAB column-major
                double got = out_buf[cpp_idx].to_double();   // ap_uint/ap_int/ap_fixed all define to_double()
                double expect = (double)golden[matlab_idx];
                if (fabs(got - expect) > TOLERANCE) {
                    printf("Call %d MISMATCH (%d,%d): got %.6f expected %.6f\n",
                           call, row, col, got, expect);
                    mismatches++;
                }
            }
        }
        printf("Call %d: %s\n", call, mismatches == 0 ? "PASS" : "FAIL");
        total_mismatches += mismatches;
    }

    // 5. Collapse to 0/1. The shell masks exit codes to 8 bits, so returning
    //    the raw count makes any multiple of 256 mismatches look like success.
    printf("TOTAL mismatches: %d\n", total_mismatches);
    return total_mismatches ? 1 : 0;
}
```

> **Note:** This testbench carries forward unchanged into the HLS design. `/hls-architect` uses the same testbench — only the kernel implementation changes, not the stimulus or comparison logic.

### Image I/O Detection — PNG/Image Read/Write

**MANDATORY CHECK during Step 1:** Scan the MATLAB code for image I/O:

```matlab
% Detection patterns:
imread()
imwrite()
imshow()
```

**Detection result determines testbench I/O:**

| MATLAB has | C++ testbench must |
|---|---|
| `imread()` + `imwrite()` | Read PNG input + write PNG output (OpenCV) |
| `imread()` only | Read PNG input + save `.bin` golden + write PNG output |
| Neither | Binary `.bin` I/O only |

**Rule: If MATLAB writes visual output (imwrite/imshow), C++ must write PNG for side-by-side comparison.**

---

### PNG I/O Implementation (when detected)

When image I/O is detected, the testbench must do **BOTH**:
1. Binary `.bin` comparison (numerical verification)
2. PNG write (visual comparison)

Start from the testbench above and add the four pieces below. The load, the two-call
loop, the comparison and the return are **unchanged** — do not fork a second copy of them.

```cpp
#include <opencv2/opencv.hpp>

// (a) Before the loads: resolve golden paths up front and build absolute paths.
//     Downstream tools run the testbench from their own build directory, so a
//     relative "../golden" only works for the local g++ run.
const char *GOLDEN_DIR = getenv("GOLDEN_PATH");
if (!GOLDEN_DIR) GOLDEN_DIR = "../golden";
char input_bin[512], golden_bin[512], input_png_path[512];
snprintf(input_bin,      sizeof(input_bin),      "%s/matlab_input.bin",  GOLDEN_DIR);
snprintf(golden_bin,     sizeof(golden_bin),     "%s/matlab_golden.bin", GOLDEN_DIR);
snprintf(input_png_path, sizeof(input_png_path), "%s/<input>.png",       GOLDEN_DIR);
// then load_bin(input_bin, ...) and load_bin(golden_bin, ...) instead of bare filenames

// (b) Optional: load the input PNG so you can eyeball it next to the output.
cv::Mat input_png = cv::imread(input_png_path, cv::IMREAD_GRAYSCALE);
if (input_png.empty())
    printf("Warning: input PNG not found — proceeding with binary-only input\n");

// (c) Inside the two-call loop, after the comparison: write the C++ output as PNG.
cv::Mat out_png(ROWS, COLS, CV_8UC1);
for (int row = 0; row < ROWS; row++)
    for (int col = 0; col < COLS; col++)
        out_png.at<uint8_t>(row, col) = (uint8_t)out_buf[row * COLS + col];
char filename[256];
snprintf(filename, sizeof(filename), "cpp_output_call%d.png", call);
cv::imwrite(filename, out_png);
printf("           (visual): %s written\n", filename);

// (d) After the loop, before the return: name the three files to compare.
printf("Visual comparison — open side by side:\n");
printf("  Input      : %s\n", input_png_path);
printf("  MATLAB gold: %s/<golden>.png\n", GOLDEN_DIR);
printf("  C++ output : cpp_output_call2.png (written to the current directory)\n");
```

**Hybrid testbench rules:**
- **Binary verification:** the `.bin` comparison catches precision errors
- **Visual output:** the PNG catches algorithm errors (shifts, channel swaps, wrong Bayer phase)
- **Both must pass:** binary PASS *and* visual inspection
- Use `cv::IMREAD_GRAYSCALE` or `cv::IMREAD_COLOR` to match MATLAB
- For RGB output, use `CV_8UC3` and interleave channels correctly
- Write PNG for **both calls** (call1 and call2) to verify consistency
- **Resolve every input path absolutely at generation time** — the testbench is reused by downstream tools that run it from a different working directory

### Verify

```bash
# ap_fixed/ap_int/ap_uint headers ship with Vitis at $XILINX_VITIS/include
g++ -std=c++14 -I$XILINX_VITIS/include -o verify testbench.cpp kernel.cpp && ./verify
```

Must print `PASS` before proceeding.

### Write to sample_based/

Call `./reference/design-layout.md  design_name=<name>  stage=sample_based`

Write into `design_name/sample_based/`:
- `kernel.cpp`    — the refactor_1 plain C++ kernel
- `testbench.cpp` — the testbench (loads `.bin` files from `../golden/`)

If it fails:

> **First, rule out width.** The 0b.2b sweep already ran this algorithm in MATLAB at the
> chosen `F` and measured the result against the same golden. If that row passed, the widths
> are sufficient — **the failure is not a precision problem, and widening types will not fix
> it.** Look for a behavioural difference instead. Widening in response to a csim mismatch is
> the most common wasted debug cycle in this flow: it changes the numbers, sometimes moves
> the mismatch, and never addresses the cause.
>
> Confirm the direction before spending time: if the C++ error is far larger than the sweep's
> `max_abs_err` for that `F`, it is structural. If it is the same order, re-check `Q` mode
> (`AP_TRN` vs `AP_RND_CONV`) and multiply-intermediate widths from 0b.4d.

- Check coefficient scaling (`/8` → `>> 3`, `/16` → `>> 4`)
- Check rounding vs truncation differences
- Exclude warmup border pixels from comparison for filter kernels (KSIZE/2 rows + cols)
- Check column-major (MATLAB) vs row-major (C++) index mapping — a transposed comparison
  fails everywhere except on a square, symmetric image
- Check that a multiply intermediate was declared at full product width before narrowing (0b.4d)

---

Print before proceeding:
```
─────────────────────────────────────────────────────
[matlab-to-cpp]  Step 2 done — refactor_1
  Data types   : <variable: sim range [min, max] → ap_uint<N> / ap_int<N> / ap_fixed<W,I> — list each>
  Border/warmup: <warmup = N rows/cols skipped in comparison / N/A>
  Index mapping: <row-major ↔ column-major note if applicable / N/A>
  Verify result: PASS / FAIL (<mismatch count if fail>)
─────────────────────────────────────────────────────
✓ Step 0   Run MATLAB simulation → save golden I/O
✓ Step 0b  Range instrumentation → sim-measured types
✓ Step 1   Analyze MATLAB algorithm
✓ Step 2   Generate refactor_1 (plain C++) + verify
  Step 3   Generate refactor_2 (frame-based C++)        ← NEXT
  Step 4   Hand off to /hls-architect → /hls-optimize
```

## Step 3 / 4 — Generate `refactor_2`: Sample-Based to Frame-Based Conversion

```
─────────────────────────────────────────────────────
[matlab-to-cpp]  Step 3 / 4 — Generate refactor_2 (Frame-Based C++)
─────────────────────────────────────────────────────
```

Starting from `refactor_1`, convert to **`refactor_2`** — a frame-based C++ file that iterates pixel-by-pixel in raster scan order. This is the file handed to `/hls-architect` in Step 4.

MATLAB code is inherently **sample-based**: it operates on entire arrays/matrices at once using vectorized operations. HLS requires **frame-based** code: iterate over pixels one at a time in raster scan order.

> **Image size rule:** The frame-based kernel must produce exactly `ROWS × COLS` output pixels — the same dimensions as the input. Do NOT increase the output array size to accommodate border warmup. Border pixels (e.g., first `KSIZE/2` rows and columns for a filter) are invalid and must be skipped in the testbench comparison, not padded into the output.

> **Type consistency rule:** refactor_2 uses **the exact same types** as refactor_1. The only difference is the loop structure (flat pixel iteration instead of nested row/col loops). **Do NOT change types** when converting sample-based to frame-based. If refactor_1 uses `output_t` for output arrays, refactor_2 must also use `output_t`. Copy the typedef block verbatim from refactor_1 to refactor_2.

### How to Convert

Step 3 restructures array-level MATLAB operations into pixel-level C++ loops.

**Do this:**
- Access a neighbourhood with clamped 2D indices: `buf[clamp(row±1) * COLS + clamp(col±1)]`
- Keep a full-frame intermediate buffer (`buf[ROWS*COLS]`) between stages
- The structure should be: sequential loops over a shared buffer, NOT a single-pass pipeline

Worked example — MATLAB `ndgrid` + `bitget` parity masks (Bayer phase, colour channel
selection) become row/col counters derived from the flat loop index:

```matlab
% MATLAB
[y, x] = ndgrid(0:ROWS-1, 0:COLS-1);
mask00 = and(not(bitget(y,1)), not(bitget(x,1)));
```
```cpp
// C++ — track row/col from the loop counter. bitget(v,1) is the LSB (1-indexed).
int  row    = k / COLS;
int  col    = k % COLS;
bool lsb_y  = (row & 1);
bool lsb_x  = (col & 1);
bool mask00 = !lsb_y && !lsb_x;
```

**Not this (causes shift bugs):**
- Attempting to fuse consecutive stages into a single pass
- `#pragma HLS` of any kind — pragmas belong to /hls-optimize, not here
- Re-associating filter arithmetic (pre-summing symmetric taps, folding coefficients
  into shifts) — it changes intermediate widths and breaks bit-exactness against the golden

---

### Write to frame_based/

Call `./reference/design-layout.md  design_name=<name>  stage=frame_based`

Write into `design_name/frame_based/`:
- `kernel.cpp`    — the refactor_2 frame-based C++ kernel
- `testbench.cpp` — same testbench as `sample_based/` (unchanged — same inputs, same golden comparison)

### Verify refactor_2 against MATLAB golden

Compile and run immediately after writing the files — same testbench, same golden `.bin` files:

```bash
cd design_name/frame_based/
# ap_fixed/ap_int/ap_uint headers ship with Vitis at $XILINX_VITIS/include
g++ -std=c++14 -I$XILINX_VITIS/include -o verify_frame kernel.cpp testbench.cpp && ./verify_frame
```

For OpenCV designs, add the include and link flags:

```bash
g++ -std=c++14 \
    -I$XILINX_VITIS/include \
    -I${OPENCV_INCLUDE} \
    -o verify_frame kernel.cpp testbench.cpp \
    -L${OPENCV_LIB} -lopencv_core -lopencv_imgcodecs -lopencv_imgproc \
    -Wl,-rpath,${OPENCV_LIB} \
&& ./verify_frame
```

Must print `PASS` before proceeding to Step 4. If it fails:
- A raster-order bug (scan direction, row/col swap) shows up here but not in refactor_1 — fix the loop structure
- A warmup border difference (filter edge pixels) — confirm the testbench skips the same border as in Step 2
- A type narrowing issue introduced during frame-based rewrite — check `ap_int`/`ap_fixed` intermediate widths match refactor_1

---

Print before proceeding:
```
─────────────────────────────────────────────────────
[matlab-to-cpp]  Step 3 done — refactor_2 (frame-based)
  Key changes  : <vectorised→loop, 2D→1D scan, imfilter→explicit neighbourhood loop, etc.>
  HLS types    : <ap_uint/ap_int/ap_fixed changes from refactor_1>
  Verify       : PASS / FAIL (<mismatch count if fail>)
  Handing off  : frame_based/kernel.cpp → /hls-architect
─────────────────────────────────────────────────────
✓ Step 0   Run MATLAB simulation → save golden I/O
✓ Step 0b  Range instrumentation → sim-measured types
✓ Step 1   Analyze MATLAB algorithm
✓ Step 2   Generate refactor_1 (plain C++) + verify
✓ Step 3   Generate refactor_2 (frame-based C++)
  Step 4   Hand off to /hls-architect → /hls-optimize           ← NEXT
```

## Step 4 / 4 — Call `/hls-architect`

```
─────────────────────────────────────────────────────
[matlab-to-cpp]  Step 4 / 4 — Handing off to /hls-architect
─────────────────────────────────────────────────────
```

Once the plain C++ passes verification (Step 2), hand off to `/hls-architect`.

Always pass `THROUGHPUT_TARGET`, `XPART`, and `CLOCK_NS` collected in the Preamble:

```
/hls-architect <THROUGHPUT_TARGET>  part=<XPART>  clock=<CLOCK_NS>
```

If `THROUGHPUT_TARGET` is empty, pass an empty string — `/hls-architect` will derive the best achievable target from II=1 floor and pass it to `/hls-optimize` automatically:

```
/hls-architect  part=<XPART>  clock=<CLOCK_NS>
```

Provide as context:
- `design_name` — the workspace root (architect uses this to call `./reference/design-layout.md`)
- `design_name/frame_based/kernel.cpp` — the frame-based C++ kernel (input to architect)
- `design_name/frame_based/testbench.cpp` — the testbench (carried forward unchanged)
- The identified stages and their responsibilities (from Step 3)
- Input/output types, frame dimensions, filter coefficients

`/hls-architect` will:
- Convert the plain C++ into multi-stage HLS dataflow C++
- Reuse the **same testbench** from Step 2 (same inputs, same MATLAB golden comparison)
- Run the full hls* validation battery
- Run csim — a PASS confirms the HLS C++ matches the MATLAB golden reference
- Hand off to `/hls-optimize <throughput target>` (passing the target through directly)
