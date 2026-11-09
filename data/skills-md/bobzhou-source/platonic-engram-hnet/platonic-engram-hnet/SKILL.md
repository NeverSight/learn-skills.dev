---
name: platonic-engram-hnet
description: Run, verify and benchmark Platonic-Engram-HNet v2, a sub-1 MB tokenizer-free int8 byte-router with O(1) SD-card Engram memory, causal Chrono-CfC spoiler-gated entity slots and a frame-locked concept decoder, bit-exact across PyTorch, NumPy, C11 and C++20 ESP32-S3 firmware. Use when working with this repo's weights, parity gates, benchmarks or firmware kernel.
---

# Platonic-Engram-HNet v2

Author: Robert Zhou (https://robertzhou.dev/work/platonic-engram-hnet/)

Repository: https://github.com/bobzhou-source/platonic-engram-hnet · ORCID: https://orcid.org/0009-0009-2155-7215

An on-device language stack for an ESP32-S3 e-reader (8 MB PSRAM) that splits compute and memory along the memory hierarchy instead of shrinking a transformer. All device arithmetic is integer-only: int8 weights, power-of-two shifts, Q15 decay.

## Quickstart

```bash
pip install numpy
python examples/quickstart.py   # (a) byte routing + int8 concepts, (b) spoiler-gated recap, (c) PE-Writer riff
```

The published int8 weights live in `weights/`; check them with `cd weights && shasum -a 256 -c SHA256SUMS`.

## Parity gates (bit-exact)

```bash
python src/verify_c_parity.py                              # encoder + CS-PW: C11 vs NumPy vs pure Python (needs a C compiler)
python src/verify_pe_writer_parity.py --require-firmware   # PE-Writer: NumPy vs C++17 vs firmware C++20 kernel (needs clang++)
```

Both gates must report 0 mismatches. The goldens they read are in `golden/` and can be rebuilt from public inputs with `python tools/make_public_goldens.py`.

## Benchmarks

The runners in `benchmarks/` need PyTorch plus the public datasets each script names.

```bash
python benchmarks/run_segmentation_efficiency_bench.py   # SIGHAN05-PKU/MSR, UD-GSDSimp word F1, bits/byte, RAM/MACs
python benchmarks/run_wsd_xling_bench.py                 # WiC, XL-WiC, MCL-WiC, Tatoeba, STS-B, PAWS-X, BQ, ATEC
python benchmarks/run_narrative_bench.py                 # CS-PW spoiler leakage on public BookSum
python benchmarks/run_pe_writer_public_bench.py          # PE-Writer v2 on 4,226 public examples
```

Training smoke test on synthetic data, CPU only: `python src/train.py --smoke`.

## Architecture

| Pillar | Lives in | Component | File | Bytes |
|---|---|---|---|---:|
| Compute | PSRAM | PLHN: UTF-8 bytes → 2 double-gated ShortConv blocks → causal H-Net cosine router (12-byte span cap) → 2-loop shared-weight Ouro core → 128-d int8 concept | `platonic-hnet.bin` | 95,008 |
| Lexical memory | SD | Engram: 65,536 FNV-1a hashed span slots, one 64-byte read per chunk (int8 concept delta + 32-byte gloss) | `engram.bin` | 4,194,816 |
| Episodic state | PSRAM | CS-PW v2: 4 continuous-time Chrono-CfC entity slots, typed frame/phrase pointers, hard causal page-offset spoiler gate | `cspw.bin` | 393,728 |
| Syntax | PSRAM + SD | Frame-Locked PE-Writer v2: 3-step Ouro planner + frame-locked decoder over a 4,096-clause bank | `pe-writer.bin` + `writer-clauses.bin` | 641,726 + 1,048,608 |
| Physical control | internal RAM | LiquidRefresh CfC v2: 339-parameter e-ink refresh/dither policy | compiled into firmware | 339 |

Code map: `src/` (models, trainers, int8 exporters, integer references, parity gates), `firmware/` (`ConceptEngine.*` device kernel, `AdaptiveRefreshPolicy.*`, host stubs), `benchmarks/`, `tools/`, `golden/`, `weights/`. See `ARCHITECTURE.md` for binary layouts and the RAM budget, and `BENCHMARKS.md` for every table, wins and losses.

## Headline results

- Encoder RAM 96.8 KB vs 550.0 KB for a matched-RAM BPE model; beats BPE on all three Chinese segmentation sets (SIGHAN05-PKU 0.394 vs 0.322 word F1).
- CS-PW: 0.000 spoiler leakage over 9,169 public BookSum cutoff queries (1.000 with the gate removed).
- PE-Writer v2: 0.00% broken sentences and 0.0% invented names over 4,226 public examples.

## License

MIT. Engram glosses come from CC-CEDICT (CC BY-SA 4.0) and Open English WordNet (CC BY 4.0).
