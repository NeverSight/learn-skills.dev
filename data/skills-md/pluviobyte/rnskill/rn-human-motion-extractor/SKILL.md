---
name: rn-human-motion-extractor
description: "Extract anonymized frame-by-frame body and hand trajectories from an authorized reference video, with skeleton previews, confidence evidence, and machine-readable keypoints. Use when the user asks to 提取博主动作, 提取人体动作轨迹, 做姿态参考, 生成骨架视频, or prepare motion control data for an avatar; do not route graphic-animation replication here."
---

# RN Human Motion Extractor

Convert a selected range of an authorized reference video into reusable motion
data. Preserve motion and timing; do not package the source person's appearance,
voice, subtitles, or footage as a reusable identity asset.

## Boundary

- Use only a public or local reference the user is authorized to analyze.
- Keep source footage and identity-preserving overlay previews in the private
  project workspace. The pure-skeleton video and keypoint data are the portable
  motion assets.
- This Skill extracts evidence; it does not promise that a generative video
  model will obey every keypoint.
- Do not call a result "exact hand motion" when fingers are occluded, blurred,
  outside the frame, or below the confidence gate. Report coverage instead.
- Route designed cards, connectors, typography, and UI motion to
  `rn-motion-replica`; route full-frame replica claims to `rn-replica-qc`.

## Workflow

### 1. Lock the range and timebase

Confirm the input file and desired range. Probe the source with `ffprobe` and
record width, height, fps, duration, frame count, and audio presence. Default to
the full clip only when the range is already short and unambiguous.

### 2. Create a local runtime

The bundled extractor requires FFmpeg plus Python 3.10–3.12. Use an isolated
environment; do not modify the system Python.

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r \
  <skill-dir>/scripts/requirements.txt
```

### 3. Extract the trajectory

```bash
.venv/bin/python <skill-dir>/scripts/extract_motion.py \
  --input <reference.mp4> \
  --output <private-project-dir>/motion-extraction \
  --start 0 \
  --duration 10
```

Omit `--duration` to process from `--start` to the end. Use `--no-overlay` when
an identity-preserving QC preview is unnecessary.

The extractor records:

- 33 MediaPipe pose landmarks
- 21 landmarks for each detected hand
- raw coordinates and confidence-aware smoothed coordinates
- normalized image `x/y`, relative `z`, visibility, frame index, and timestamp

Short missing spans may be interpolated. Long gaps remain missing; never fill a
long occlusion with invented finger choreography.

### 4. Inspect evidence

Open both the overlay preview and pure-skeleton preview. Inspect at least the
beginning, every major gesture change, and the final frame. Read
`qc/extraction-stats.json` before describing fidelity.

The preview convention is:

- yellow: body
- blue/red: left/right hands
- thin gray: low-confidence body nodes

Verify that shoulders, elbows, wrists, and hand clusters stay on the correct
limbs through crossings. If a hand swaps sides or jumps, keep the raw data,
mark the affected time range, and correct it with manual keyframes before using
it as a hard control signal.

### 5. Deliver claims at the proved level

The expected output is:

```text
motion-extraction/
├── data/
│   ├── motion-keypoints.json
│   └── motion-keypoints.npz
├── qc/
│   ├── extraction-stats.json
│   ├── media-probe.json
│   ├── motion-overlay.mp4
│   ├── motion-skeleton.mp4
│   └── contact-sheet.jpg
└── work/
    └── *.mp4
```

Report body coverage and left/right hand coverage separately. A useful body and
wrist trajectory can coexist with incomplete finger tracking; say so plainly.
For the JSON contract and handedness rules, read
[references/keypoint-schema.md](references/keypoint-schema.md).

## Completion gates

- Source range, fps, and processed frame count agree.
- JSON parses and contains one entry per processed frame.
- Both final MP4s decode without FFmpeg errors and match the extracted duration.
- Contact sheet has been visually inspected.
- Confidence gaps and occlusions are reported, not hidden by smoothing.
- No paid generation task is implied or submitted by this extraction Skill.
