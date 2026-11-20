---
name: zach-3d-films
description: Makes a 3D cartoon "what if" explainer short (9:16) entirely in code with three.js, in the style of Zack D. Films-type videos. The same skill as /zach-d-films under the name used in the reel. Procedural cartoon people, props and effects, slow-motion impacts, a red force ripple and 1 to 3 word captions timed to the voiceover. Use when the user runs /zach-3d-films or asks for a 3D cartoon explainer or a "could X stop Y" short.
---

# /zach-3d-films

This is `/zach-d-films` under another name: the same engine, the same worked example (the armour short, where the arrow hits the plate and his jaw drops) and the same steps.

1. Point at the real skill folder:
   ```bash
   SKILL_DIR=$(python3 -c 'import os,sys;print(os.path.realpath(os.path.join(sys.argv[1],"..","zach-d-films")))' "<base directory of this skill>")
   ```
2. Read `$SKILL_DIR/SKILL.md` and follow it exactly, with that `SKILL_DIR`.

If `$SKILL_DIR/SKILL.md` is missing, the repo was copied without `skills/zach-d-films`. Install the whole repo (see its README).
