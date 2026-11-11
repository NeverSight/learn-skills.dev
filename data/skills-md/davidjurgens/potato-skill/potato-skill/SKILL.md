---
name: potato-skill
description: Design, build, run, monitor and visually check Potato annotation tasks. Use when turning a research description into an annotation task, creating or editing a Potato config.yaml, choosing an annotation_type or scale, laying out the annotation interface with instance_display, setting up consent/instructions/training/survey phases, adding attention checks or gold standards, deciding how many annotators an item needs, importing existing annotations from COCO/CVAT/Label Studio or transcripts or a ConvoKit corpus, exporting annotations to CSV/COCO/CoNLL/Parquet or any other format, checking how a running study is going or why agreement is empty, changing a task after annotators have started, resetting an annotator's login, leaving a server running for a researcher, or debugging a task that will not start, renders wrong, or silently does nothing.
---

# Potato annotation tasks

A Potato task is one YAML config plus a data file. Building one is three jobs:
deciding what to ask and how, writing it down correctly, and running it until you
have watched a person get from the login screen to the end of the study. The
second job is the one with a validator behind it, which is why it is tempting to
start and stop there. It is the least likely to be where the study breaks.

Read `AGENTS.md` in the project root if it is there — it carries project
conventions on top of this.

## If you were invoked with no task described

Someone typed `/potato-skill` and there is no brief in the conversation. Do not
start building, and do not open with "what would you like to make?" — a
researcher who has not used Potato cannot answer that usefully.

Ask for one sentence, propose a design from it, then confirm only what you had
to guess. `references/interviewing.md` is the question bank: the opening ask,
the four-line proposal, then two rounds of multiple-choice covering the
modality, the unit, the response format, annotators per item, quality control,
the export target and who gets to log in — then a third round that offers the
seven capability clusters as a menu and drills into only what gets ticked.

Two things it is emphatic about. Ask what **modality** the data is, every time:
it decides the display, the scheme family and the per-family key that says where
the media lives, and getting it wrong is silent. And do not push phases —
`consent`, `training` and `prestudy` are protocol decisions, most tasks want
none of them, and a researcher who needs one knows they need it.

The standing rule to build with stated assumptions rather than wait still holds
— it applies once the interview has something to assume *from*. With nothing at
all in context, asking four structured questions is faster for the researcher
than any guess you could make.


## Installing Potato

Most of this skill drives the `potato` command and imports Potato's registries.
Neither works if the package is not in the environment you are running commands
in.

```bash
python -c "import potato" || pip install potato-annotation
```

Do not use `potato --version` as that guard. Releases up to 2.7 have no such
flag and exit 2 with a usage message, so the `||` branch fires every time and a
released wheel lands on top of whatever was already installed, an editable
checkout included. An import is the version-independent check.

For the version itself, ask Potato: `potato --version` where it exists, and
`report_issue.py` otherwise. Neither `importlib.metadata.version` nor
`potato.__version__` is reliable on its own -- each gives a different answer
depending on which directory you run it from. `references/reporting-upstream.md`
has the measurements.

The browser walk in `scripts/walk_task.py` additionally needs Playwright:
`pip install 'potato-annotation[preview]' && playwright install chromium`.

## The scripts in this skill

Nine of the procedures below are scripts rather than instructions, because they
are long enough to get wrong by hand and they are what you will run repeatedly.
They live beside this file in `scripts/`.

The commands below write this file's directory as `<skill-dir>`; put the real
path in its place. Claude Code shows it as "Base directory for this skill" when
the skill loads. An `npx skills add` install puts it at `.agents/skills/potato-skill/`
for Codex and Cursor and at `.claude/skills/potato-skill/` for Claude Code. A `/plugin install`
keeps it in Claude Code's plugin cache, so read the path rather than assume
one.

| Script | What it does |
|---|---|
| `boot_and_check.py config.yaml -p 8000` | Boots, waits for a 200, and names every feature that is configured but loaded nothing |
| `walk_task.py --url … --config … --task-dir .` | Registers an annotator, walks the whole study, and checks the answers reached `user_state.json` **as the values it submitted**. `--grade` answers the gold and attention items from their own files and reports the verdict Potato recorded; `--answers file.json` annotates with judgements you supply instead of first options |
| `estimate_effort.py config.yaml --rate 15` | Items, annotators needed, minutes each, total hours and cost |
| `find_design.py --type span --with-instructions` | Searches 444 published task designs in the Potato Showcase |
| `handover.py config.yaml --confirm` | Removes the accounts you made while testing and writes `RUNNING.md` |
| `check_ui.py --url … --config config.yaml` | Renders every page and reports schemes below the fold, empty media, empty choice tiles, schemes with no control to answer with, answers nothing collects, what the widgets say went wrong, keybinding conflicts and schemes that never appeared. `--phase poststudy` measures a page the walk cannot reach |
| `study_status.py --url … --task-dir .` | Progress, per-annotator pace, agreement, and what looks wrong on a **running** study |
| `model_prices.py config.yaml` | Fetches live model prices and puts them beside what Potato's compiled table would charge, before you choose an `ai_budget.cap_usd` |
| `report_issue.py bug --title …` | Assembles a bug report or a feature request against Potato: version and commit, whether the config passes `--strict`, the data's shape, a duplicate search, secrets redacted. Files nothing without `--submit --confirm` |

Each takes `--help`, and `boot_and_check`, `walk_task`, `check_ui` and
`study_status` take `--json` when you want to act on the result rather than read
it.

## The loop

```bash
potato validate config.yaml --strict               # structure and unknown keys
potato preview config.yaml                         # what the form declares
potato preview config.yaml --screenshot out.png    # render one page, report browser errors
nohup potato start config.yaml -p 8000 > server.log 2>&1 &    # boot it and read the log
```

The first three return promptly. The fourth never returns — background it, poll
`curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8000/` for a 200, and
read `server.log`.

`potato --help` lists these under **other commands**, below the `start` flags.
Each has its own grammar, so `potato validate --help` and `potato preview --help`
are where their options are.

### Each step catches a different class of failure

| Step | Catches | Blind to |
|---|---|---|
| `validate --strict` | Missing required keys, bad types, unknown keys at 1–2 levels | Side files, phase types, anything inside a scheme entry |
| `preview` | What schemes and keybindings the config declares | Whether any of it renders |
| `preview --screenshot` | Uncaught exceptions, `console.error`, failed requests on **one** page | Everything below 900px, every conditional widget, every other phase |
| **boot + read the log** | Side-file formats, phase assembly, subsystem initialization | What it looks like |
| **drive it in a browser** | The actual study | — |

Skipping the last two is how a task ships that validates, screenshots clean, and
loses its training phase, its attention checks and a third of its items.

## Boot it early

The startup log is the real validator. It is the only thing that reports whether
the parts of the config that `validate` never opens actually worked:

```bash
grep -E "ERROR|Traceback|Loaded [0-9]+|phase|missing required" server.log
```

A healthy boot on a task with training and attention checks says
`Loaded 3 training instances` and `Loaded 2 attention check items`, and says
nothing about phases. Anything else is a feature that is configured and off.

Boot as soon as the config parses — before the interface is finished, before the
instructions are written. `running-a-task.md` has the backgrounding recipe, the
readiness check, the log-line table, and which generated files to delete after an
edit.

## Three silent failure modes

**Enabled is not running.** `attention_checks.enabled: true` with a malformed
items file logs one warning, then `Loaded 0 attention check items`, then runs the
whole study with quality control off. Check the count, not the config.

**`--strict` does not reach everything.** On 2.13.1 it catches four mistakes
that 2.12.1 validated clean:
- `key_binding` instead of `key_value` on a radio label fails, with "Did you
  mean: 'key_value'?".
- A phase `type:` that does not exist is an error that lists the real types.
- An `automatic_assignment` block is reported as not read.
- So is a `surveyflow` block.

A clean `--strict` still means only that none of its checks fired. Boot the
task and look at it.

**The screenshot is the viewport, not the page.** `--screenshot` writes
1280×900. On a task with an instructions banner, that is the banner and half the
item — none of the questions. Advice to "look at the PNG and check the Next
button is above the fold" cannot be followed with this tool alone. Drive a
browser and screenshot `full_page=True`.

## Find out what they already have

A brief plus a data file is the common case, not the only one. Ask four things
before designing anything, because each has a command behind it and each is
expensive to discover after the config is written:

| Ask | Because |
|---|---|
| What format is the data in, and where is the media? | Transcripts and conversation corpora have their own converters |
| Do you already have annotations? | `potato import` reads 48 formats and writes a runnable project |
| What has to come out at the end? | 72 export formats. Check the target one **before** anyone annotates |
| Who runs it after handover, and for how long? | Decides hosting, logins and the allowlist |

```bash
potato import --list-formats                      # coco, cvat, labelme, labelbox, via, …
potato transcripts interviews/ -r --dry-run       # whisper, srt, vtt, textgrid, eaf, …
potato convokit reddit-corpus-small --unit conversation --emit-config
```

`references/importing-existing-work.md` covers all three, including the one
decision that matters most: whether imported annotations are **pre-annotations**
a human corrects, or `--seed-user` work that marks the item done.

## Underspecified briefs

Read `references/asking-the-experimenter.md` before writing the config. Decide it
yourself when being wrong is cheap; ask when it is expensive, irreversible or not
yours — the unit of annotation, the annotator budget, consent wording, and
anything involving identifiable people.

Never wait on an answer. Build with stated assumptions, write the questions into
`QUESTIONS.md` alongside something that runs, and say which assumption you would
revisit first.

## Look for the feature before you build one

Potato has more built in than a config reference makes obvious. The expensive
mistake is not an invented type name — validation catches that. It is
hand-assembling something Potato already does.

`references/modes-and-subsystems.md` is the routing table from what a researcher
said to the block that does it: QDA and codebooks, solo mode, rooms,
adjudication, review workflow, sessions, pocket, active learning, judges,
crowdsourcing, publishing, telemetry. Check it before writing a scheme that
sounds like a workaround.

It opens with **the seven clusters** — material, the answer, unit, people, trust,
model help, output — which is the same map the interview offers as a menu. Run it
against the brief as a checklist: the clusters a brief never mentions are where a
researcher is most likely to be missing something they would want. Raise at most
two of them, and only where they matter; the rest goes in `QUESTIONS.md`.

The cluster researchers miss most reliably is **the answer**. They ask for
`radio` and `likert` and stop, and `soft_label`, `range_slider`,
`semantic_differential`, `constant_sum` and `confidence` never get reached for.

## Designing it

`references/designing-a-task.md` covers the seven decisions behind every task:
the unit, the questions, the response format, annotators per item, item order,
quality control, and the phases either side.

**The routing table covers the common asks and stops.** Eleven types are named
nowhere but the generated reference, so they never get reached for: `multirate`
(ten ratings on one scale, not ten `likert` schemes), `hierarchical_multiselect`
(a taxonomy, collapsed, with search), `select`, `soft_label` (a distribution
rather than a forced choice), `range_slider`, `semantic_differential`,
`conjoint`, `card_sort`, `extractive_qa`, `multi_document_event`, `code_review`.
Each has a working example and a row in `designing-a-task.md`.

Two that are easy to get wrong and expensive to discover late:

- **The response format decides the agreement metric.** Potato picks it from the
  schema kind. A 1–5 rating stored as a `radio` is scored as unordered, so
  "1 vs 2" and "1 vs 5" count the same. That is a measurement error, not a
  cosmetic one. Table in `references/assignment-and-agreement.md`.
- **`num_annotators_per_item` sets the target, `max_annotations_per_user` sets
  what one person actually sees.** Left unset the cap is the item count, so
  everyone is offered the whole corpus. Set it below that and an annotator who
  reaches the cap is shown the ordinary completion page, which tells them they
  finished the task rather than that they hit a quota.
  `automatic_assignment.instance_per_annotator` looks like the key for this and
  is not read at all. From 2.13.1 `--strict` says so and names
  `max_annotations_per_user`. `per_annotator_quota` is real and overrides
  `max_annotations_per_user`.

## The design record and the cost

Two files next to the config, neither of which the config can hold:

- **`DESIGN.md`** — the unit of annotation and why, why each response format,
  annotators per item, what quality control is for, and a separate, explicit
  list of the choices you assumed because the brief did not say. That last paragraph is
  what makes the document worth opening.
- **`QUESTIONS.md`** — what you could not decide at all. Never wait on an
  answer; ship something that runs alongside the question.

```bash
python <skill-dir>/scripts/estimate_effort.py config.yaml --rate 15
```

reports how many annotators the design needs, how long each is working, total
hours and a cost. Run it before the instructions get written — it is the cheapest
place to catch a design nobody can afford.

If the task also calls a model, the other half of the bill is per token, and
Potato prices it from a table compiled into the package that matches on the
longest substring of the model name. A model the table does not list is priced
from whatever shorter row its name happens to contain, and `ai_budget.cap_usd`
then refuses or permits work on that number. Potato logs a warning when that
happens, but the projection it warns about is still the one the cap uses.

```bash
python <skill-dir>/scripts/model_prices.py config.yaml
```

fetches current prices when you run it, puts them next to what Potato would
charge, and names the row the charge came from. Where they disagree, set the
right figure in `ai_budget.prices` rather than editing Potato. Do this rather
than writing a rate into `DESIGN.md`: a price copied into a document is wrong at
the next repricing and goes on reading as though somebody had checked it.

`references/recording-decisions.md` has the `DESIGN.md` template and what moves
the estimate.

## Start from a published design

Before writing a scheme from a field list, look for one somebody already ran:

```bash
python <skill-dir>/scripts/find_design.py --query "stance" --with-instructions
python <skill-dir>/scripts/find_design.py --show text/argumentation-stance/argument-quality
```

The Potato Showcase is 444 annotation task designs, most built from a published
paper, with real label sets and real question wording — and **285 of them carry
written instructions**. None of them has a `phases` block, a consent page or a
training round, so take the questions from there and the study around them from
`worked-example.md`. `references/finding-a-design.md` covers what to change
before reusing one.

## Writing the instructions

The config has a validator behind it. The text an annotator reads does not, and
it is where most of the disagreement in a finished dataset comes from.

`references/writing-guidelines.md` covers the four surfaces annotator-facing
text can live on (the `instructions` phase, the `annotation_instructions`
banner, `annotation_codebook_url`, and the per-scheme `description`), what a
label definition has to contain to settle an argument, tie-break rules, worked
examples including the borderline ones, and iterating the guidelines from the
pilot's disagreements. `examples/advanced/long-guidelines/` is a working model
of all of it.

Two things to get right without reading further:

- **The banner is not the codebook.** `annotation_instructions` sits on every
  page, expanded by default. A long one pushes the questions below the fold on
  every item of the study. Definitions go on the instructions phase.
- **Label definitions are usually the researcher's, not yours.** Ask for their
  codebook or the paper the scheme comes from before writing any. If they have
  none, draft them, mark them as drafts, and say plainly that these are the
  sentences that decide what the dataset means.

## Building the interface

`references/building-the-ui.md` covers `instance_display`, the 31 display types,
`span_target`, keyboard shortcuts, `display_logic`, and the **form layout** —
`layout.grid` puts short questions side by side, `layout.groups` gives them
collapsible headings, and a per-scheme `layout` says how many columns each one
takes. Without a `layout` block every scheme stacks full-width in config order,
which is how a twelve-question task becomes twelve screens. The same file has
what to reach for, in order, when a page is too long.

`references/evaluating-the-ui.md` covers what to do with the rendered page. Read
it before the first screenshot.

Without `instance_display`, Potato renders `text_key` as plain text — right for
text classification, wrong for an image, a PDF, a dialogue or an agent trace.

`references/data-and-access.md` covers the other end: data files and formats,
`item_properties`, `media_directory` for local images and audio, remote and
polled sources, where output lands, and who is allowed to log in.

## Anything that is not text

`references/modalities.md` routes a medium to its display type, its scheme type
and its quirks: images and CV, video, audio and speech, dialogue and podcasts,
point clouds, robot episodes. `references/agent-traces.md` covers the agent
family — about twenty evaluation schemes, eight trace displays and sixty
examples.

Three facts that decide whether a non-text task works at all:

- **Every family has its own key for "where is my data".** `source_field` on
  image, video, audio and 3D schemes; `video_key` on `temporal_grounding`;
  `audio_key` on `speech_transcript`; `steps_key` on the whole agent family;
  `image_key` on `table_grid`. The wrong one gives an empty widget, a clean
  `--strict`, and a silent log.
- **A geometry scheme does not fetch its own media.** The canvas takes its
  bitmap from the `<img>` that `instance_display` renders, so a config without
  the display field comes up blank.
- **`--screenshot` cannot verify any of this.** A canvas that never loaded and
  one that loaded look identical in a PNG. Boot it, draw one box, and read
  `user_state.json`.

## The pages either side of annotation

`references/phases-and-pages.md`. Consent, instructions, training and post-study
surveys are the half of a study that `validate` barely sees: `phases` and
`surveyflow` have no documented sub-keys, and inside `phases` only the page
rules and orderings are checked.

There are exactly six phase types (`consent`, `instructions`,
`training`, `annotation`, `poststudy`, `prestudy`), and a page can also be
`type: jspsych`, which runs a jsPsych timeline in a prestudy or poststudy slot.
Every other non-annotation page needs a `file:` pointing at a JSONL of
annotation schemes, one per line; prose goes in a `pure_display` scheme; and a
phase named in `order` but not defined is skipped with a warning.

## Experiments

`references/experiments.md`. Between-subjects `conditions`, a screener that ends
the study (`exit_when`), pages only some participants see (`show_when`),
counterbalanced pages, shuffled questionnaire items, timed trials on Potato's
own items, jsPsych tasks inside a Potato study, and `cloze`. A page rule reads
survey answers and `condition.<factor>`, never per-item annotations, and the
server refuses to start on a rule naming a question no earlier page asks.
Screen-outs are in `participants.csv`, not marked in `annotations.csv`.

## Quality control

`references/quality-control.md` has the file formats for training, attention
checks and gold standards, none of which are documented anywhere else:

- training data: an **object** with `training_instances`; each needs `id`,
  `text`, `correct_answers`
- attention items: an array; each needs `id`, `expected_answer`
- gold items: an array; each needs `gold_label`

## Start from something that runs

`references/worked-example.md` is a complete study skeleton — consent,
instructions, a practice round with model answers, attention checks, the
annotation itself and a closing survey — with every side-file format filled in.
It validates under `--strict` and boots clean. Copy it and replace the labels
and prose.

Potato also ships 261 example projects, all checked in CI:

```python
from potato.server_utils.examples_manifest import search_examples
search_examples(annotation_type="span", display_type="image")
search_examples(config_key="gold_standards")
search_examples(query="dialogue")
```

They are the better starting point for one unusual scheme or display type. They
are single-purpose demos, so none of them shows a whole workflow.

## Picking an annotation type

There are 80. `references/annotation-types.md` has all of them with fields and a
worked example lifted from a config that really runs.

```python
from potato.server_utils.schema_examples import example_scheme_for
example_scheme_for("bws")
```

Never invent a type name. `sentiment`, `classification` and `qa` are not types.

## Config keys

`references/config-keys.md` lists the 180 documented **top-level** keys.
`references/config-keys-nested.md` lists the 624 documented **sub-keys** — the
level where features are actually configured, and the level the generated pack
drops. It also lists the 24 blocks whose sub-keys `--strict` does not check at
all, where a typo is silent.

```python
from potato.server_utils.config_key_docs import get_key_doc
get_key_doc("attention_checks.frequency")
```

## Interrogating the software

Roughly forty config blocks take an object and document nothing about its
contents, including `training`, `phases`, `surveyflow`, `quality_control` and
`adjudication`. Guessing key names one at a time is slow, and a wrong guess is
usually silent.

`references/interrogating-potato.md` has the four methods that recovered every
undocumented format in this pack: batch candidate keys through `--strict` and
read what it rejects, provoke type errors to learn the shape, delta-debug a side
file against the boot log, and provoke the errors that enumerate valid values.
It also has the one trap — an *ignored* key proves nothing, because validation
stops two levels down.

## Checking it

**Look at the PNG.** A clean exit means nothing threw, not that the interface is
usable — and `preview --phase consent --screenshot` **exits 1 on a task that is
completely fine**, because Potato's phase pages log four harmless 404s that get
counted as errors. Judge the PNG and the error list, not `$?`. The list is in
`troubleshooting.md`; `scripts/walk_task.py` filters it for you. The preview CLI
also refuses `--phase prestudy`, which the server supports.

**`preview` is the only thing that reports keyboard conflicts.** Two schemes both
declaring `key_value: '1'` validate clean, boot silently, and on the live page
only the first scheme's shortcut works — the second is dead with no warning
anywhere. Take `KEYBINDING CONFLICTS` seriously and confirm by pressing the key
on a running page. Details in `building-the-ui.md`.

`validate` also passes a config full of invented phase types that the server
drops at boot, which is what `boot_and_check.py` is for.

## Then drive it

```bash
python <skill-dir>/scripts/walk_task.py \
    --url http://localhost:8000 --config config.yaml --task-dir .
```

It registers a fresh annotator, answers every page, walks to the end, goes back
to an earlier item, and reads `annotation_output/<user>/user_state.json` to check
the server kept what the page showed. Pass `--config` on a task with a practice
round: training grades the answer, so without the model answers the walk loops on
the first question whose right answer is not the first option.

Four things it is checking, each of which has shipped broken:

1. A conditional scheme appears once its gate is answered. A hidden input still
   has a bounding box, so visibility has to be judged on the ancestor chain.
2. Answers survive **navigating away and back**. Never test this with a refresh:
   browsers restore form state themselves, so the check passes when the server
   stored nothing.
3. The workflow reaches its own last page.
4. The answers are in `user_state.json`, not just on the screen.

Left alone it answers generically — first option for everything — so it proves
the machinery works, not that the labels make sense. Two flags go further.

**`--grade`** answers the gold and attention items from the files the config
names and reports the verdict Potato recorded for each, read out of
`annotation_output/quality_control_results.json` rather than recomputed. It
needs `--config` and `--task-dir`, and it keeps three outcomes apart, because
they send you to three different places:

- **graded wrong** — the answer never reached the grader, or the labels in the
  side file are not the labels in `annotation_schemes`
- **too fast** — `attention_checks.min_response_time` refused the answer for
  arriving quickly, whatever it said. That is the walker's speed, not a fault
  in the item
- **never served** — the walk did not meet the item at all. Checks are injected
  on a frequency, so a short walk can finish having seen none, and an empty
  results file otherwise reads exactly like a study running with quality
  control switched off

**`--answers file.json`** takes `{instance id: {scheme: label}}` and annotates
with those. This is the half a script cannot do for itself: read the items and
the guidelines, decide the labels yourself, and the walk types them in. A label
set nothing fits and an instruction that contradicts the labels are both
invisible to a first-option pass and obvious to this one.

Spans, a drag-and-drop sort and a canvas region it still cannot drive; it names
the schemes it left holding nothing when it stops. For those,
`references/running-a-task.md` has the selectors, the span-drag recipe including
the scroll offset that stops the drag landing on the navbar, and a driver to
adapt.

## Then check the interface itself

`walk_task.py` proves the answers reach the server. It says nothing about whether
a person can find the questions.

```bash
python <skill-dir>/scripts/check_ui.py \
    --url http://localhost:8000 --config config.yaml --shots ui/
```

It measures each page in the live layout rather than judging a PNG, and reports
what `validate` and `--screenshot` both miss:

- **Which schemes and which button are below the fold**, with pixel positions, at
  the same 1280×900 the screenshot uses. It is the check the screenshot section
  above says you cannot make with `--screenshot` alone.
- **How many screens tall each page is.** Over about two and a half, reach for
  `instance_display.layout` before the study starts, not after.
- **Schemes declared and never detected** on the annotation page — a scheme that
  did not render, or a `display_logic` gate the initial state never satisfies.
- **Image, canvas, video and audio widgets that came up empty**, which is the one
  failure a screenshot genuinely cannot distinguish from success.
- **Keyboard shortcuts claimed by two labels.** Only the first works and nothing
  warns you.

A config with a duplicate `key_value` and ten questions on one page passes
`potato validate --strict` with `OK — no issues found`.

The walk starts at the landing page and goes forward, so on a real corpus all
twelve steps are annotation pages and a `poststudy` survey is hundreds of items
out of reach. Measure that page on its own:

```bash
python <skill-dir>/scripts/check_ui.py \
    --config config.yaml --phase poststudy --phase consent
```

That boots a throwaway debug server per phase and lands directly on the phase
route. It takes `consent`, `instructions`, `training`, `annotation` and
`poststudy` — not `prestudy`, which the preview route table does not carry and
which the ordinary walk reaches anyway because it comes first.

## Leaving it running

If the point is a server a researcher can open (see `deploying.md` if it needs to
outlive your session or reach anyone else):

```bash
pkill -f "potato start config.yaml -p 8000"        # wipe with it stopped
python <skill-dir>/scripts/handover.py config.yaml \
    --url http://your-host:8000 --port 8000 --confirm
```

`handover.py` removes the accounts you created while checking — they are real
annotators holding real assignments, and their answers count toward agreement —
and writes `RUNNING.md` with the URL, how to start and stop it, where the admin
key lives and where the data is. Run it with the server **stopped**: item and
user state are already in memory, so a wipe while it runs resets nothing and the
next annotator to arrive gets the completion page.

## Watching a live study

```bash
python <skill-dir>/scripts/study_status.py \
    --url http://localhost:8000 --task-dir .
```

Progress, per-annotator counts and pace, agreement per scheme, attention-check
failures, stale assignments, and anything that looks wrong. It exits non-zero
when it found a problem.

The admin surfaces it reads are not linked from the annotation page and are not
open:

```bash
curl -s -o /dev/null localhost:8000/admin    # the key file appears on first admin request
curl -H "X-API-Key: $(cat admin_api_key.txt)" localhost:8000/admin/iaa
```

`/admin` itself serves HTML without a key. Every admin **JSON API** returns
`403 {"error":"Admin access required"}` without one, which reads like a broken
build if you do not know the key exists. `admin_api_key.txt` is written the
first time an admin route is requested — not at boot, so it is missing if you
look straight after starting the server.

`references/after-annotators-start.md` maps each question a researcher asks to
the route that answers it, and covers reclaiming abandoned assignments,
resetting a login, and adjusting one person's quota.

## Changing a task after annotators start

Adding items, editing prose and adding annotators are all safe. Editing
`annotation_schemes` is not, and nothing errors:

- **Adding a question** collects nothing from anyone who already finished.
  Completion is tracked per item, never per question, so an annotated item is
  never offered again.
- **Renaming one** makes the old answers invisible to every report. The overview
  reads 100% complete, agreement reports zero items for each configured scheme,
  and the CSV export carries columns named after the scheme that is gone,
  because exports are driven by what was stored rather than by the config.

The boot log is the only place this surfaces: `Saved annotations name N
scheme(s) that annotation_schemes no longer defines`. Read it after any scheme
edit on a task with data in it. `after-annotators-start.md` has what to do
instead.

**Accounts do not survive a restart by default.** The default auth backend is
in-memory, so registrations are lost when the server stops while the annotations
stay safe on disk. Set `authentication.user_config_path: user_config.json` on
anything an annotator will come back to — it matters most on `render` and
`huggingface`, which restart containers on their own.

## Getting the data out

There is one storage format — `annotation_output/<user>/user_state.json` — and
72 export formats. `output_annotation_format` is deprecated: the loader
reads it as `export_annotation_format` and warns. Write the live key.

```yaml
export_annotation_format: [csv]     # on a timer, into annotation_output/exports/csv/
```

```bash
curl -H "X-API-Key: $K" -H "Content-Type: application/json" \
     -X POST -d '{"format":"coco"}' localhost:8000/admin/api/export
```

`references/getting-the-data-out.md` routes a downstream use to its format —
`conll_2003` for NER, `coco`/`yolo` for detection, `parquet` for analysis at
scale, `textgrid`/`eaf` for phonetics, `keystrokes` for writing process. Ask
which one they need **before** the annotating starts; a task designed without a
target format can produce answers that do not survive the conversion.

Two traps: the admin export route writes to the **server's** disk and hands back
paths rather than a download, and a misspelled `export_annotation_format`
validates clean, boots clean, and only warns at runtime after the first save.

## Deploying it

`potato deploy` and `potato share` are in the same **other commands** list.

```bash
potato share config.yaml                                # temporary public HTTPS URL
potato deploy providers --verify                        # 15 targets; which credentials work
potato deploy check config.yaml --provider aws          # preflight; changes nothing
potato deploy up    config.yaml --provider aws --dry-run  # the plan and the monthly cost
potato deploy up    config.yaml --provider aws          # provision
potato deploy pull  config.yaml --dest ./collected      # get the annotations back
```

`references/deploying.md` covers the fifteen targets and how to choose between
them, credentials, backup and restore, deploy buttons, what the bundle ships (the
whole task directory, minus `annotation_output/`), and the preflight — which is
the part worth learning, because it names what the deployment exposes and blocks
on `debug: true`.

Run `--dry-run` before any `potato deploy up` that costs money, and show the
researcher its cost line and its warnings. A plan the real deploy would refuse
ends in `REFUSED:` and exits 2.

Three that decide whether a deployment is safe to hand over:

- **Some hosts wipe their disk.** On `heroku`, `render` (free), `huggingface`
  and `aws-ecs`, annotations survive a restart only through `--backup hf` or
  `--backup s3`, which restores into the empty server at boot. `heroku` and
  `aws-ecs` refuse to deploy without one; `heroku` also accepts `--demo` for a
  disposable run. `render` and `railway` need `--backup` on every deploy, since
  it is how the project reaches the container.
- **`user_config.allow_all_users` defaults to true**, so anyone with the URL can
  register. Set an allowlist before exposing anything.
- **Pull before you destroy.** `destroy` refuses without a prior successful pull
  unless forced, and that guard is the only thing between a finished study and an
  empty directory.

## Things that go wrong

`references/troubleshooting.md` is the full table. The ones worth memorizing:

| Symptom | Cause |
|---|---|
| A command never returns | `potato start` blocks. Background it |
| A feature does nothing, config is right | Typo'd key in a block `--strict` does not check |
| A phase never appears | Named in `order`, never defined; or invalid `type:` |
| `Loaded 0 <anything>` | Side file is missing a required field |
| `ConfigSecurityError: Path … outside the project directory` | Wrong working directory, or a path escaping `task_dir` |
| A scheme is missing from the screenshot | Behind `display_logic`; the initial render does not satisfy it |
| The item shows a file path, not an image | No `instance_display` |
| Both top-level and phase-level schemes | Phase-level schemes *replace* the top-level list; you cannot have both |
| `400 Required annotation(s) not completed` | A required span scheme; the client cannot check it, so the only feedback is a corner toast |
| Annotations look wrong after a restart | Something hand-edited `output_annotation_dir`. Never do that |
| A codebook holds labels you already changed | The first run seeds `project.sqlite`. `potato codebook config.yaml` re-syncs |

## Reporting a bug or asking for a feature

Three things look the same from a chair: a config mistake, a bug, and something
Potato was never built to do. Sort them before offering to file anything.

- `--strict` fails, or the log says `Loaded 0 <something>` → a config mistake.
  `troubleshooting.md`.
- Potato does something other than what it documents → a bug.
- Potato does exactly what it documents and that is not enough → a feature
  request, once you have named the closest existing type or key and said why it
  does not fit. It exists more often than people expect.

For the last two, offer to file it. `references/reporting-upstream.md` has the
checks and what a report needs; the helper assembles it:

```bash
python <skill-dir>/scripts/report_issue.py bug \
    --title "Waveform never generates for media_directory audio" \
    --observed "..." --expected "..." --repro "..." \
    --config config.yaml --log server.log
```

It prints the report and a prefilled GitHub URL, redacts API keys, credentials,
email addresses and home directories first, and says what it took out. **Show
the body to whoever owns the study and get an answer before filing.** Filing is
public and cannot be withdrawn, so `--submit` needs `--confirm` as well, and it
refuses a body still holding a placeholder.

## Reference map

| File | For |
|---|---|
| `worked-example.md` | A complete study skeleton that validates and boots |
| `asking-the-experimenter.md` | What to confirm, what to assume, how to ask |
| `importing-existing-work.md` | Existing annotations, transcripts, conversation corpora, questionnaires (Qualtrics, REDCap, XLSForm and four more), Ibex, IIIF, camera-trap and bioacoustics files |
| `designing-a-task.md` | The seven decisions |
| `finding-a-design.md` | The Potato Showcase, and what to change before reusing a design |
| `writing-guidelines.md` | Label definitions, tie-break rules, the codebook an annotator reads |
| `recording-decisions.md` | `DESIGN.md`, `QUESTIONS.md`, and estimating effort |
| `annotation-types.md` | All 76 types with worked examples *(generated)* |
| `building-the-ui.md` | `instance_display`, display types, spans, shortcuts, `display_logic` |
| `modalities.md` | Images, video, audio, dialogue, 3D, listening tests, spectrograms, maps, protein structures, genome loci, glossing, ego networks — display, scheme and quirks |
| `agent-traces.md` | Trace displays, the agent-evaluation schemes, world-model rollouts |
| `evaluating-the-ui.md` | What to look at in a render, and when to stop |
| `interviewing.md` | The multiple-choice question bank, for when the skill is invoked with no brief |
| `phases-and-pages.md` | Consent, instructions, training, surveys, page files |
| `experiments.md` | Conditions, screen-outs, page and question order, timed trials, self-paced reading, jsPsych, headphone checks, external tasks, cloze, LexTALE, list experiments, incentivized elicitation and bonus payment |
| `quality-control.md` | Training, attention checks, gold standards, adjudication, side-file formats |
| `assignment-and-agreement.md` | Quotas, ordering, and which metric each schema kind gets |
| `modes-and-subsystems.md` | The rest of Potato, routed from what the researcher said |
| `model-assistance.md` | `ai_support` against a self-hosted LLM: where the keys go, which `endpoint_type` works; training a model on the annotations |
| `labeling-engine.md` | Models label, people label a blind sample, contracts decide what is accepted (2.11) |
| `interrogating-potato.md` | Recovering an undocumented block from the validator and the boot log |
| `data-and-access.md` | Where items come from, output files, login, serving |
| `getting-the-data-out.md` | The 72 export formats, what the CSV holds, phase data |
| `after-annotators-start.md` | Monitoring a live study, what is safe to change, fixing things |
| `config-keys.md` | 180 top-level keys *(generated)* |
| `config-keys-nested.md` | 624 sub-keys, plus what is undocumented and what is unvalidated |
| `running-a-task.md` | Backgrounding, logs, browser driving, handover |
| `deploying.md` | Sharing, choosing a host, credentials, backups, the preflight, bundles, deploy buttons, SAML and Hugging Face sign-in, offline hosts, pulling data back |
| `troubleshooting.md` | Symptom → cause → fix |
| `reporting-upstream.md` | Telling a config mistake from a bug from a gap, and filing the last two |

## MCP

`potato mcp` is two servers. `potato --help` lists both under **other
commands**, after the long `start` flag list.

**Authoring.** `potato mcp serve --root .` speaks MCP over stdio and answers out
of the same registries this pack is generated from: `list_annotation_types`,
`describe_annotation_type`, `list_display_types`, `describe_display_type`,
`list_config_keys`, `describe_config_key`, `get_config_schema`, `list_examples`,
`get_example`, `validate_config`, `preview_config`, `render_task_screenshot`.
Prefer them over reading the references when the server is connected —
`describe_annotation_type` returns the required and optional fields for one type,
which is the question the references are usually opened to answer.
`render_task_screenshot` hands back the rendered page as an image with browser
errors attached; it is still one page, and still the viewport. One join to know:
`list_examples` returns each example's `dir`, and `get_example` takes that value
under a parameter called `name` — the basename and the task name are both
refused.

```bash
potato mcp config --root .       # prints the client config block to save
potato mcp tools                 # the tool list, without starting anything
```

**A running task.** `potato mcp connect --url http://host:port --token …` bridges
a live instance, if that task's config carries an `mcp` block naming the tools in
`mcp.tools` and an agent holds a token:

```bash
potato mcp issue-token --config config.yaml --name some-agent --role admin
```

The bridge exposes the authoring tools *and* the live ones, the live ones
prefixed `live_`: `live_get_status`, `live_get_config`, `live_get_progress`,
`live_list_items`, `live_get_item`, `live_list_annotators`, `live_get_agreement`,
`live_submit_annotation`, `live_assign_items`, `live_export_data`,
`live_add_items`, `live_delete_annotations`, and for the labeling engine
`live_engine_status`, `live_engine_requests`, `live_engine_run`,
`live_engine_certify`, `live_engine_certificate` — 17 in all. `live_delete_annotations`
clears one annotator's work on one item, so it also has to be listed in
`mcp.destructive` and called with `confirm: true`; Potato refuses it otherwise. Each
publishes a real parameter schema, so `tools/list` is enough to call them —
`live_get_item` declares `instance_id` required, `live_submit_annotation`
declares `username`, `instance_id` and `annotations`. `mcp.tools` names them
without the `live_` prefix, and a name Potato does not know refuses the boot
with the full list.

Everything an agent calls lands in `mcp_audit.jsonl`, one JSON object per call,
recording the tool, the agent, the role, the argument *names*, and the outcome —
a separate line for a write that succeeded, errored or was refused.
