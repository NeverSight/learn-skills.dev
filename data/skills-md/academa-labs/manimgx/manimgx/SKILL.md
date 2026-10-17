---
name: manimgx
description: Create and refine mathematical or 3D animations in Python with ManimGX, including scene authoring, layout inspection, and video export.
license: MIT
---

# ManimGX

Use ManimGX to turn the user's explanation into a scene, inspect its layout and timing,
and deliver the rendered video with its editable Python source.

Use the project's existing Python environment. For a standalone installation,
`uv tool install --python 3.14 manimgx` provides the `manimgx` command. Python 3.13 or newer
is required. Text, mathematics, and video encoding are included in the package.

Import `manimgx as m`. Its authoring API follows Manim Community Edition; check ManimGX's
own [reference](https://manimgx.academa.ai/reference/) for supported options and behavior.
[The agent primer](https://manimgx.academa.ai/llms.txt) links the guides and examples as
Markdown. Read the relevant page when using an unfamiliar feature.

## Author a scene

Put the animation in a `Scene` subclass's `construct` method. Time advances through
`self.play(...)` and `self.wait(...)`; `self.add(...)` only adds objects. Compose placement
with `VGroup`, `next_to`, `arrange`, and `to_edge` so labels follow their subjects. Use `Text`
for prose and `MathTex` with raw strings for LaTeX mathematics.

For example, save this as `scene.py`:

```python
import manimgx as m


class CircleArea(m.Scene):
    def construct(self) -> None:
        circle = m.Circle(radius=1, color=m.BLUE, fill_opacity=0.3)
        formula = m.MathTex(r"A = \pi r^2").next_to(circle, m.RIGHT, buff=0.6)
        m.VGroup(circle, formula).center()
        self.play(m.Create(circle), m.Write(formula))
        self.wait(1)
```

For changing values, animate a `ValueTracker` and derive dependent geometry from its
value. An updater should use elapsed time or current state, not the number of frames;
changing the export frame rate should preserve the motion. Use `ThreeDScene` for a 3D
camera.

## Inspect and deliver

```sh
manimgx inspect scene.py CircleArea
manimgx render scene.py CircleArea -r 1280x720 --fps 30 -o draft.mp4
```

`inspect` writes a storyboard and reports the timeline and sampled 2D layout problems.
Look at the pictures and fix unintended overlap or clipping; use `-t 0.5,end` to inspect
particular moments. These are sampled checks, and 3D scenes receive storyboards without
2D layout checks. Review the draft's motion as well as its still frames.

Render the final video at the user's requested size and frame rate (`-r WIDTHxHEIGHT`
and `--fps RATE`). Without those options, export is 1920×1080 at 60 fps. Include the output
path and the scene source when delivering it.
