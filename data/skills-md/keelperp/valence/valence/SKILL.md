---
name: valence
description: >-
  Give an agent a reward/punishment readout derived from the Drosophila
  mushroom-body connectome. Turns any state — a text snippet, an embedding, a
  telemetry or market snapshot — into a 16-dimensional compartment signature
  plus a signed appetitive-minus-aversive scalar. The 16 compartments and their
  valence signs are not hand-assigned: they fall out of the PAM:PPL1 dopaminergic
  synapse ratio in a real fly brain. Use when an agent needs a stable, cheap,
  deterministic affect channel to compare states, detect regime changes, or rank
  situations. This layer has no update rule: nothing in it changes with use.
license: MIT
metadata:
  source: neuPrint male-cns:v1.0 (public, token-free)
  neurons: 4064 Kenyon cells, 97 MBONs, 340 DANs, 2 APL
  synapses: 463640 KC->MBON, 376252 PN->KC, 406552 KC<->APL
---

# valence

A readout layer wired from a real fly brain. You hand it a state, it hands back
16 numbers and a scalar.

## Run it

```bash
scripts/valence read "the build failed and the oncall page fired"
scripts/valence read --json '{"pnl":-0.42,"latency_ms":812,"error_rate":0.19}'
echo "some agent state" | scripts/valence read --raw     # JSON out
scripts/valence demo                                     # see it discriminate
scripts/valence gates                                    # every gate arm
scripts/valence info                                     # provenance + valence table
```

From Node:

```js
import { read, fitScale, applyScale } from './src/valence.mjs';
const out = read('deploy succeeded, all tests green');
out.readout;   // 16 z-scores, one per mushroom-body compartment
out.scalar;    // appetitive - aversive, weighted by innervation lopsidedness
out.compartments; // ["CA","a'1","a'2","a'3","a1","a2","a3","b'1","b'2","b1","b2","g1","g2","g3","g4","g5"]
out.valence;   // [0,-1,-1,-1,1,-1,-1,1,1,1,1,-1,-1,1,1,1]
```

## The pipeline

```text
input --> 512 features --> locality-sensitive linear projection
      --> 54 glomerular channels --> real PN->KC synapses
      --> 4,064 Kenyon cells --> real APL feedback loop (sparsification, ~11.6%)
      --> real KC->MBON synapses --> 97 MBONs
      --> 16 compartments, each signed by its PAM:PPL1 ratio
```

## Two things you must not "simplify"

Both were measured, both have a gate arm that is proven red.

1. **The projection is a linear random projection, never a hash.** Swap in
   sha256 and a one-byte input change decorrelates the readout completely.
   Near-pair vs far-pair separation over 20 independent corpora of 500 pairs,
   from `gates/projection.mjs`:

   ```console
   separation at p10 of 20 seeds: sha256 -0.0847  ->  linear 0.8791
   separation on the WORST seed:       sha256 -0.1625  ->  linear 0.8011
   ```

   and "near beats far, pair by pair" drops from 93.2% to 44.7% at the same
   percentile — chance. The bands do not touch on any of the 20 seeds. The far
   pair is measured within each input type as well as across it, and judged on
   the worst of the three; the old construction drew 99.6% of its far pairs
   across the string/vector boundary.

2. **Sparsification is the anatomical APL loop, never a fixed threshold — and
   the anatomy means the measured synapse counts, not just the loop.** Kenyon-
   cell activation-rate CV across 5 corpora, from `gates/sparsity.mjs`:

   ```console
   CV, worst seed: fixed 0.3577  ->  flat anatomy 0.2177  ->  real anatomy 0.1110
   ```

   "flat anatomy" is the same feedback loop with the same topology and every
   KC<->APL synapse count replaced by 1. It costs half the stability, which is
   why the word "anatomical" is load-bearing and has its own break arm.

## What "does not learn" means here — read this before you repeat it

It means the layer **has no update rule**. There is no state, no fit to your
labels, nothing that changes with use. Same input, same output, forever.

It does **not** mean the synapse counts are structureless. They are not, and
`gates/no-learning.mjs` now asserts that they are not:

```console
  relative gain (base-ctrl)/base   0.0627..0.1898 median 0.1284 p90 0.1786
  excess over the worst shuffle    0.3584
```

The first line: over 20 corpora x 3 degree-preserving shuffles, the real
KC->MBON counts buy a median 12.8% more pattern-separation d' than a shuffle of
themselves — small, consistently positive, never zero. The second: on the matrix
itself, the real counts beat their own shuffle by 0.3584 of top-1% MBON-pair
weight cosine. That is real edge-level structure.

So: say "it has no update rule". Do not say "the synapse counts are random" or
"the real weights carry no separation". Both were claimed here before and both
are false.

The second line was cross-calibrated against a second connectome,
`hemibrain:v1.2.1`, which measures 0.3440 against this one's 0.3584 — so the
edge-level structure claim rests on two flies. The bound on the FIRST line does
not transfer: hemibrain's shuffle control measures 0.2929 where this fly's
measures 0.1786, so gate (c)'s 0.20 is a `male-cns:v1.0` number. If you rebuild
this on another dataset, re-calibrate it.

If you want the scalar to track *your* notion of good and bad, fit a linear
probe on top of `out.readout`. That probe is your learning, not the layer's.

## Numeric inputs need scaling

A return of 0.04 and a volume of 3.4 are not comparable and L2 normalisation
cannot know that. Fit the scales against your own history:

```js
const scale = fitScale(historyRows);           // per-key mean and sd
read(applyScale(currentRow, scale));
```

Unscaled, two very different market snapshots read at cos = 0.9953. Scaled:

```console
    RALLY   vs FLAT     cos = 0.4467
```

The demo prints both.

## Cost

0.640 ms per read after warm-up (measured: 3,000 reads, 1,563 reads/s, by
`node scripts/bench.mjs`), single-threaded, no dependencies, no network.
