---
name: hls-line-buffer
description: Fill the HLS line-buffer and window-buffer gap for stencil kernels, including TOTAL_ITER drain and verification. Use when generated buffer code misses the drain or the check.
license: MIT
metadata:
  author: "Sai Akhil Ayyagari"
  version: "1.0.0"
---
<!--
Copyright (C) 2026, Advanced Micro Devices, Inc. All rights reserved.
SPDX-License-Identifier: MIT
-->
# HLS Line Buffer

The LLM can generate a line buffer and window buffer structure on its own. This guide fills the gap on what it consistently gets wrong.

**Before generating code, understand the flow below, then produce code that matches it.**

**Constants** (derive before writing code):
- `KRAD = KSIZE / 2` — kernel radius (e.g. KSIZE=15 -> KRAD=7)
- `NLB = KSIZE - 1` — number of line buffer rows
- `WARMUP = KRAD * COLS + KRAD` — iterations before first valid output pixel
- `TOTAL_ITER = ROWS * COLS + WARMUP` — total loop iterations

---

## 1 — Run for TOTAL_ITER, not ROWS x COLS

After the last image pixel, the line buffer still holds KRAD rows of real data that have never been centered in the window. Without extra iterations those rows are never output.

Fix: run the compute loop for TOTAL_ITER iterations. Read the actual pixel from the stream when `n < ROWS * COLS`, otherwise use zero — all in one loop:

```cpp
U8 pixel = (n < num_pixels) ? pixel_stream.read() : 0;
```

The zeros flush the last rows through so every pixel gets centered and output. Use **one loop** — not two separate loops (two loops add an FSM transition and cost ~16 cycles).

---

## 2 — Verify the LLM applied step 1 correctly

Check these before running csim/cosim:

- `TOTAL_ITER = ROWS * COLS + WARMUP` — not just `ROWS * COLS`
- `WARMUP = KRAD * COLS + KRAD` — uses the same COLS as col_ptr wrapping (if col_ptr wraps at COLS_POW2, WARMUP must also use COLS_POW2)
- Zero tail is inline in the loop (`n < num_pixels` ternary), not a second loop
- Output is gated on `n >= WARMUP` — no output written during warmup
