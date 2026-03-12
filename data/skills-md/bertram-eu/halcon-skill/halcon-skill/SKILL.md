---
name: HALCON-skill
description: Generate, refactor, run, and review HALCON HDevelop (`.hdev`) and HDevelopEVO (`.hscript`) programs with accurate operator usage, parameter defaults, value ranges, and practical vision pipelines. Use when the user asks for HDevelop or HScript code, operator selection, debugging logic, converting requirements into vision scripts, or building reusable procedures.
---

# HALCON Vision Script Authoring Skill

Use this skill to produce production-grade HALCON vision scripts in either format:
- **HDevelop** (`.hdev`) — XML-based, run with `hrun`
- **HDevelopEVO** (`.hscript`) — plain-text, run with `hscriptengine`

Both share the same HALCON operators, data model, and control flow. The differences are in file format, procedure syntax, and import mechanism.

## Target format
Ask the user which format they need if unclear. Default to `.hdev` unless the user mentions HDevelopEVO, HScript, `.hscript`, or `hscriptengine`.

## Required scope
- Generate and edit only HALCON script artifacts unless the user explicitly asks otherwise:
  - HDevelop: `.hdev` (scripts), `.hdvp` (single procedure), `.hdpl` (procedure library)
  - HDevelopEVO: `.hscript` (scripts, procedures, and libraries — all use the same extension)
- Prefer deterministic, testable logic with explicit parameters and clear pass/fail outputs.

## Testing
Check if an `images` folder is provided. This folder should contain images for testing/implemention and might be sorted into different classes (`ok`/`nok`, `io`/`nio`, `training`/`test`/`validation`). The images might further be annotated by a `json` or `yaml` file. If so, use the included content appropriately.
Output images from test or implementations runs should be written in the `result` folder by default. Keep a text file with the output of `hrun` or `hscriptengine` for each image here as well.

## Reference files
Local references in `references/`:
1. [`references/hdev_format_reference.md`](references/hdev_format_reference.md) — `.hdev` XML schema (all tags, attributes, `<interface>` declarations, `<docu>` blocks), `.hdvp`/`.hdpl` procedure formats.
2. [`references/hscript_format_reference.md`](references/hscript_format_reference.md) — `.hscript` plain-text format, procedure syntax (`proc`/`endproc`, `public`), `from ... import *` mechanism, and differences from `.hdev`.
3. [`references/hrun_reference.md`](references/hrun_reference.md) — `hrun` CLI help, usage patterns, and authoring guidelines for headless `.hdev` execution.
4. [`references/hscriptengine_reference.md`](references/hscriptengine_reference.md) — `hscriptengine` CLI help, usage patterns, authoring guidelines, and comparison with `hrun`.

HALCONROOT documentation (available at `HALCONROOT/doc/`):
- **Operator reference:** `doc/html/reference/operators/` — 2,637 HTML pages with full operator signatures, parameter descriptions, and examples. Use for operator-level details when the local references are insufficient.
- **PDF manuals:** `doc/pdf/manuals/` — `hdevelop_users_guide.pdf`, `programmers_guide.pdf`, `quick_guide.pdf`, `parallel_programming.pdf`, etc.
- **Solution guides:** `doc/pdf/solution_guide/` — application-focused guides for matching, measuring, 3D vision, classification, data codes, and image acquisition.

## Authoring workflow
1. Convert user requirements into a pipeline with explicit phases:
   - input/acquisition
   - ROI/domain restriction
   - preprocessing
   - core detection/measurement/matching
   - decision and reporting
2. Choose operators from the detailed operator reference and keep parameters valid by construction.
3. Always investigate at least three different implementation approaches and compare their pros and cons before settling on a final solution. If you are unsure which one is the absolute best and most stable solution, ask the user for clarification or preferences.
4. Tunable parameters should always be procedure parameters with sensbile defaults and a clear parameter range. In `main()` put all tunable parameters in a single block at the top for easy access and documentation.
5. Encapsulate repeated logic into local or external procedures.
6. Use `dev_` operators for visualization and debugging. Use multiple windows if multiple different visualizations are required. Prefer `dev_set_part()` over cropping for visualization. Only write annotated images in `main()`.
7. Add robust error handling (`try/catch` or return-code handling) when runtime failures are plausible.
9. Add parallelization (`par_start`/`par_join`) only for independent tasks and isolated outputs.
9. Keep output semantics explicit (`ok`/`nok`, scores, measured values, reasons).
10. `main()` is to be treated as a unit test. All parameters and input images set here should be global variables so they can be easily overridden when running with `hrun` (`-D`) or `hscriptengine` (`--input`).
11. The core image processing logic that should be used in production needs to be a separate procedure with at least an iconic `Image` input parameter and boolean `JobPass` output parameter.
12. There should not be any code accessing input sources (cameras) or external communication (network, industrial communication, file I/O) unless the user explicitly asks for it.
13. Ensure the code can run headless via `hrun` (for `.hdev`) or `hscriptengine` (for `.hscript`). This means: no `stop()` anywhere, no `dev_open_dialog`, no interactive operators. Use `try`/`catch` around visualization code so it degrades gracefully when no display is available.

## Coding rules
- Use idiomatic HDevelop syntax (`:=`, tuples, vectors, dictionaries, `if/for/while/switch`).
- Keep procedure names, procedure parameters and variable names task-specific and stable.
- Avoid hidden global state unless required for interoperability.
- Reuse expensive handles/models (measure, metrology, matching, data code) when processing many images.
- For metric output, use calibrated transforms instead of pixel approximations.
- Never use `stop()` anywhere in the script. `stop()` halts execution and waits for user input in HDevelop, which makes the script hang indefinitely when run headless via `hrun` or `hscriptengine`. For error cases, use `return ()` to exit a procedure or `throw` to propagate an error — never `stop()`.
- Document **every** procedure — including `main()` — and all procedure parameters. These descriptions are visible in the HDevelop/HDevelopEVO GUI and are essential for usability. Specifically:
  - For `.hdev`: **every** `<procedure>` (including `main`) must include a `<docu>` block. The `<docu>` block must contain:
    - `<abstract>` — detailed description of what the procedure does
    - `<short>` — one-line summary
    - `<parameters>` — a `<parameter>` for each interface parameter (empty `<parameters/>` for `main` if it has no interface)
    - `<example>` — a usage example showing how to call the procedure with realistic parameters
    - Where appropriate, also include:
      - `<attention>` — important notes the user must be aware of (e.g., required preprocessing, dependency on other procedures, constraints on input data)
      - `<warning>` — things that can go wrong or produce unexpected results (e.g., deprecated features, performance pitfalls, precision limits)
      - `<references>` — academic papers, documentation links, or standards that the algorithm is based on
      - `<complexity>` — computational complexity or performance characteristics
    - **Multi-language rule:** HDevelop only displays text matching the active GUI language. Every text element (`<abstract>`, `<short>`, `<description>`, `<attention>`, `<warning>`, `<example>`, `<references>`, `<complexity>`) must be provided in **three** variants:
      1. Without `lang` attribute — language-independent fallback, shown when no matching language copy exists
      2. With `lang="en_US"` — English copy
      3. With `lang="de_DE"` — German copy
    - If the user's locale is known and differs from `en_US`/`de_DE`, add a fourth copy with the user's `lang` tag (e.g., `lang="ja_JP"`, `lang="zh_CN"`).
    - This three-copy pattern is how HALCON's own built-in procedures work (see `HALCONROOT/procedures/general/`). Without the fallback and German copies, descriptions appear empty when the GUI is set to German.
    - Also include `<keywords>` (with `lang="en_US"` and `lang="de_DE"`), `<chapters>` (with `lang="en_US"` and `lang="de_DE"`), `<see_also>`, `<alternatives>`, `<predecessor>`, `<successor>` where applicable.
    - Per-parameter documentation must include `<default_type>`, `<default_value>`, `<sem_type>`, `<type_list>`, and `<values>` where applicable — these drive the HDevelop GUI's parameter widgets and tooltips.
  - For `.hscript`: document each procedure (including the main program section) and each parameter with `//` comments above or next to the `proc` signature, stating purpose, type, value range, units, and defaults. Provide documentation in both English and German where practical.
- Document and explain all code.

## Response contract
When delivering `.hdev` or `.hscript` solutions:
- Provide complete executable snippets, not partial pseudocode.
- State critical assumptions (image type, calibration availability, expected object polarity, lighting stability).
- Name the key operators chosen and why.
- Surface parameter ranges that are likely to need tuning.
- When generating `.hscript`: use `from ... import *` for external procedures, `proc`/`endproc` for procedure definitions, and `//` or `*` for comments.

## Environment variables

### `HALCONROOT`
Points to the HALCON installation directory. Contains the core runtime, libraries, documentation, and built-in procedures.

Key subdirectories:
| Path | Contents |
|------|----------|
| `bin/` | HALCON binaries including `hrun`, `hscriptengine`, `hdevelop`, and runtime DLLs |
| `HDevelopEVO/` | HDevelopEVO IDE application (`hdevelopevo.exe`) |
| `procedures/general/` | ~52 built-in reusable procedures (`.hdvp`/`.hdpl`) — display helpers (`disp_message`, `dev_open_window_fit_image`), camera utilities, deep learning helpers, etc. |
| `procedures/dl/` | Deep learning procedures — dataset handling, preprocessing, training, evaluation, visualization |
| `procedures/templates/` | Procedure templates for custom extensions |
| `doc/pdf/manuals/` | PDF manuals — `hdevelop_users_guide.pdf`, `programmers_guide.pdf`, `quick_guide.pdf`, `parallel_programming.pdf`, etc. |
| `doc/pdf/reference/` | `reference_hdevelop.pdf` — full operator reference |
| `doc/pdf/solution_guide/` | Solution guides for matching, measuring, 3D vision, classification, data codes, image acquisition |
| `doc/html/` | HTML documentation with searchable operator docs |
| `help/` | Operator index files (`.idx`, `.key`, `.ref`) used by HDevelop help system |
| `examples/hdevelop/` | Same as `HALCONEXAMPLES/hdevelop/` (may be symlinked or duplicated) |
| `images/` | Sample images used by examples and documentation |
| `calib/` | Calibration data files |
| `ocr/` | Pre-trained OCR font files |
| `dl/` | Pre-trained deep learning models |
| `lut/` | Look-up tables for visualization |

### `HALCONEXAMPLES`
Points to the HALCON examples directory. Contains runnable sample scripts across all HALCON domains in both formats.

Key subdirectories:
| Path | Contents |
|------|----------|
| `hdevelop/` | **941 HDevelop `.hdev` example scripts** organized by topic |
| `hdevelopevo/` | **800 HDevelopEVO `.hscript` example scripts** — same topics plus `DeepCounting/` and `Runtime/` categories, with a bundled `procedures/` directory |
| `solution_guide/` | Examples accompanying the solution guide PDFs, organized by topic (`basics/`, `matching/`, `3d_vision/`, `classification/`, `1d_measuring/`, `2d_measuring/`, `image_acquisition/`) |
| `images/` | ~108 image files and ~107 image subdirectories used by the example scripts |
| `python/`, `c/`, `cpp/`, `c#/`, `vb.net/` | Language-specific integration examples |
| `hdevengine/`, `hscriptengine/` | Engine integration examples (C++ and HScript) |

**Example categories** (shared across `hdevelop/` and `hdevelopevo/`):
1D-Measuring, 2D-Metrology, 3D-Matching, 3D-Object-Model, 3D-Reconstruction, Applications, Calibration, Classification, Control, Deep-Learning, Develop, File, Filters, Graphics, Identification, Image, ImageSource, Inspection, Manuals, Matching, Matrix, Morphology, OCR, Object, Regions, Segmentation, System, Tools, Transformations, Tuple, XLD

HDevelopEVO-only categories: `DeepCounting/`, `Runtime/` (performance benchmarks)

Notable top-level scripts:
- `hdevelop/explore_halcon.hdev` — showcase of HALCON capabilities across many domains
- `hdevelop/halcon_basic_concepts.hdev` / `hdevelopevo/halcon_basic_concepts.hscript` — introduction to fundamental HALCON concepts
- `hdevelopevo/code_snippets.hscript` — IDE snippet templates for HDevelopEVO

## Output style
- Prefer one clear main procedure plus small helpers.
- Group parameter block at top.
- Keep visualization optional and non-blocking for runtime mode.
- Keep decision logic explicit and auditable.
- For `.hscript`: use `public proc` for procedures intended to be imported, `proc` for file-local helpers. Use `from './path' import *` for external procedure imports.
- For `.hdev`: procedures are embedded as XML `<procedure>` elements with typed `<interface>` declarations.
