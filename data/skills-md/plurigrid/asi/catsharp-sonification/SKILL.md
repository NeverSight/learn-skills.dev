---
name: catsharp-sonification
description: Sonify GF(3) color streams via CatSharp scale. Maps Gay.jl colors to pitch classes and plays through sox. No voice synthesis.
trit: 0
triggers:
  - sonification
  - catsharp
  - play colors
  - audio gf3
  - topos of music
---

# CatSharp Sonification

Sonify deterministic color streams using the CatSharp scale (Mazzola's Topos of Music).

## Galois Chain

```
seed ⊣ γ ⊣ color ⊣ hue ⊣ pitch ⊣ freq ⊣ tone
```

## Mappings

### Hue → Trit (Gay.jl spec)

| Hue Range | Trit | Role | Temperature |
|-----------|------|------|-------------|
| 0-60°, 300-360° | +1 | PLUS | warm |
| 60-180° | 0 | ERGODIC | neutral |
| 180-300° | -1 | MINUS | cold |

### Trit → Waveform

| Trit | Waveform | Character |
|------|----------|-----------|
| +1 | sine | smooth, harmonic |
| 0 | triangle | balanced, neutral |
| -1 | square | harsh, digital |

### Hue → Pitch Class

```
pitch_class = floor(hue / 30) mod 12
```

30° per semitone maps the color wheel to the chromatic scale.

### CatSharp Pitch → Trit

| Pitch Classes | Trit | Structure |
|---------------|------|-----------|
| {0, 4, 8} (C, E, G#) | +1 | Augmented triad |
| {3, 6, 9} (Eb, F#, A) | 0 | Diminished subset |
| Circle of fifths | -1 | Fifths stack |

## Usage

### Python (sox required)

```python
import subprocess

def play_color(r, g, b, duration=0.15):
    hue = rgb_to_hue(r, g, b)
    trit = hue_to_trit(hue)
    pc = int(hue / 30) % 12
    freq = 261.63 * (2 ** (pc / 12))  # C4 base
    wave = {1: "sine", 0: "triangle", -1: "square"}[trit]
    subprocess.run(["play", "-q", "-n", "synth", str(duration), 
                    wave, str(freq), "vol", "0.3"])
```

### Babashka

```clojure
(defn play-trit [trit freq]
  (let [wave (case trit 1 "sine" 0 "triangle" -1 "square")]
    (shell "play" "-q" "-n" "synth" "0.15" wave (str freq) "vol" "0.3")))
```

### Julia (Gay.jl)

```julia
using Gay

function sonify_stream(seed, n=12)
    Gay.gay_seed!(seed)
    for _ in 1:n
        c = Gay.next_color()
        hue = Gay.Colors.convert(Gay.HSL, c).h
        pc = mod(round(Int, hue / 30), 12)
        freq = 261.63 * 2^(pc / 12)
        trit = hue < 60 || hue >= 300 ? 1 : hue < 180 ? 0 : -1
        wave = Dict(1 => "sine", 0 => "triangle", -1 => "square")[trit]
        run(`play -q -n synth 0.15 $wave $freq vol 0.3`)
    end
end
```

## GF(3) Conservation

Every tripartite emission sums to 0 mod 3:

```
MINUS(-1) + ERGODIC(0) + PLUS(+1) = 0
```

## Modelica Formulation

See `catsharp.mo` for acausal equation-based model.

## Dependencies

- `sox` (via flox: `flox install sox`)
- Python 3.x or Julia with Gay.jl
- macOS `afplay` as fallback

## Related Skills

- `gay-mcp`: Deterministic color generation
- `rubato-composer`: Mazzola's mathematical music theory
- `topos-of-music`: Full categorical music implementation
