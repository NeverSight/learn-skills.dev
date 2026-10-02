---
name: autocode-board
description: "The experiment board of the autocode loop — its view (`assets/view.html`), the data checks render.py runs before writing (`assets/validate.py`), and the templates, schemas, and verbatim prompts autocode reads at each step (`assets/reference.md`). Platform-neutral: both the Claude Code and the Codex editions of autocode render through this skill and loop-report. Reference skill: autocode names the section it needs; do not invoke it standalone."
---

# Autocode board (shared view)

autocode's page is built by loop-report from this skill's view:

```
python3 <loop-report's dir>/assets/render.py \
  --data .autocode/report/autocode.data.json \
  --out  .autocode/report/autocode.html \
  --view <this skill's dir>/assets/view.html
```

`render.py` loads `assets/validate.py` from the directory of the view it was given, so the data checks travel with the view. `<this skill's dir>` is the directory holding this SKILL.md — under the plugin install it is weed-harness's `skills/autocode-board`, under the npx installer `~/.codex/skills/autocode-board` or the platform's equivalent.

`assets/reference.md` holds what autocode's SKILL.md deliberately does not restate: the interview fields, the `program.md` and `state.json` templates, the hypothesis schema, the strategist brief and reply format, the experimenter prompt, the keep-commit and result-message templates, the board data (§ Board data) and the status / final-summary blocks. autocode names the section at the step that writes or sends that data; read only that section.

Delivery of the rendered page is not this skill's: the Codex edition of autocode runs loop-report's `deliver.py`, the Claude Code edition republishes the same file with the Artifact tool.
