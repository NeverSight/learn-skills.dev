---
name: archlang
description: Use when the user wants to create, edit, or inspect an architectural floor plan / building layout as code — e.g. "draw a 2-bedroom apartment", "add a bathroom to this plan", "make the bedroom 1 m wider", "lay out an office floor". ArchLang is a tiny text language that compiles a .arch file to a professional floor-plan drawing (SVG/PNG/PDF/DXF). Drive it entirely through the `archlang` CLI; do not hand-render.
---

# ArchLang — author floor plans as code

ArchLang turns a small `.arch` text file into a professional floor-plan drawing. It is built for
agents: deterministic, self-correcting (errors carry a machine code, a prose `fix`, and often a
**machine-applicable** fix `archlang fix` can apply), and verifiable without ever looking at an image
(`archlang describe`).

## Setup (zero-install)

The CLI runs straight from npm — no clone, no build:

```bash
npx -y @chanmeng666/archlang --help
```

Or `npm i -g @chanmeng666/archlang` for a global `archlang` command. Every call below is written
`archlang <cmd>`; without the global install, write `npx -y @chanmeng666/archlang <cmd>`. Never run
a bare `arch`: the package installs it as an alias, but on Linux, macOS and Git Bash coreutils
owns that name, so the shell runs the wrong program.

## The loop (always follow this)

1. **Learn the language first.** Run `archlang spec` and read it — the entire language in one page.
   (`archlang context` prints *everything*: spec + this workflow + CLI reference + error catalog.)
   Do this before writing any `.arch`.
2. **Write the plan** to a `.arch` file (or pipe via stdin with `-`), preferring the **placement
   sugar** below so you never hand-compute a coordinate.
3. **Render it:** `archlang compile plan.arch -o plan.svg --json`. The JSON is `{ ok, diagnostics,
   summary }`.
4. **Auto-fix the mechanical faults:** if `ok` is false, run `archlang fix plan.arch --dry-run --json`
   to preview the **machine-applicable** edits (off-wall opening → attachment form, out-of-range
   position clamped, …), then re-run without `--dry-run` to apply. Anything `fix` can't resolve stays
   in `diagnostics[].fix` for you to edit by hand. Exit code `2` means a deterministic user error —
   fix it, don't blindly retry (`1` = IO/internal, `3` = bad usage).
5. **See the plan without an image:** `archlang compile plan.arch -f txt` (or `archlang preview plan.arch
   --ascii`) prints a zero-dependency ASCII floor plan you can read straight from stdout.
6. **Verify intent:** `archlang describe plan.arch --json` returns the rooms (areas, adjacency), what each
   door connects, and totals. Confirm the room count, labels, and areas match what was asked.
   Each room reports two areas: `area_m2` on wall centrelines and `net_area_m2`, the floor no wall
   stands on (the room less every wall band inside it, computed exactly, or absent when it cannot
   be, and then so is the net total); `totals` sums both. Quote `net_area_m2` as floor area, and name
   which figure you report.
7. **Gate on soundness — don't ship a flagged plan.** `archlang validate plan.arch --strict --json`
   (parse + resolve + lint). `--strict` makes **every advisory warning fail** (exit `2`) — the gate a
   generation pipeline runs before it ships. Add `--graph g.json` to also assert the intended
   room-to-room adjacency (`{ "living": ["kitchen","hall"], … }`); a mismatch fails. Read each
   `diagnostics[].fix`, edit, and re-run until it passes — or, if a warning is deliberate, say so.
8. **Check the plan against the brief.** Write the user's brief as an `intent.json` — its checkable
   expectations as data (room count, per-room concepts with area/window bands, total area, optional
   adjacency/reachability). Two disciplines keep it brief-grounded: assert an area band only where the
   brief gives a number ("about/~N" → ±10%; "at least N" → `min` only; qualitative words → nothing),
   and assert the top-level room `count` only when the brief **enumerates** the rooms. Gate with
   `archlang validate plan.arch --intent intent.json --feedback --json`: a gating miss (room
   count/existence/area/total-area/window) fails (exit `2`) with a per-violation correction prompt —
   iterate on the feedback and re-run. Adjacency/reachability are advisory (reported, never fail the
   gate). Use `archlang score plan.arch --brief intent.json --json` as a continuous satisfaction meter
   (always exit `0`) to watch the plan approach the brief across edits. See
   [`/intent.schema.json`](https://archlang.uk/intent.schema.json).
9. **Fix furniture geometry:** `archlang repair plan.arch -o fixed.arch` pushes furniture out of
   walls/doorways/swing arcs (the geometric corrector; distinct from `fix`). It rewrites a piece in
   the form you wrote it (an `at` point, or the `inset` of an `in <room> anchor …` placement) — and
   **always read `unresolved`**: a piece it may not rewrite (one `for`/component statement drawing
   several pieces, expression coordinates, an `against wall` anchor) is reported there with the fault
   and why, never silently skipped. `changed: false` with a non-empty `unresolved` means *you* edit
   the source.
10. **Finish the drawing:** once lint is clean, run `archlang finish plan.arch --dry-run --json`, then
   without `--dry-run` to apply. It first furnishes each rectangular room that holds no furniture,
   by the room's use (single-storey plans; a furnished room is never touched — a partly furnished one is
   named in `unresolved` with the categories it lacks, not topped up), then adds the sheet
   statements the plan lacks — `paper`, `scale`, `dims auto`, `title`, `schedule rooms`,
   `legend` — on the smallest sheet the drawing fits. It fills only what is missing and deletes
   nothing. Read `unresolved`: a room it left empty or a statement it left out is named there
   with the reason (`--only furnish`/`--only sheet` runs one step; `--reissue` lets it replace a
   `paper`/`scale` the drawing does not fit).
11. **Show the user:** `archlang preview plan.arch -o plan.png` renders a PNG (`--install` fetches the
   optional renderer if missing). To hand the user the plan itself, rendered and with nothing to
   install, run `archlang link plan.arch` (or `npx -y @chanmeng666/archlang link plan.arch`): it
   prints a playground URL that opens the plan; `--json` adds the embed URL.

## Write it right the first time (placement sugar — the preferred path)

A geometry-blind generator that emits absolute coordinates produces plans that render but are
physically wrong (openings off their wall, furniture through walls). Author by **attachment** instead
— the compiler computes the coordinate, and fails loudly if the reference is ambiguous:

- **Attach openings to a wall by position, not `at (x,y)`.** `door on <wall> at <pos> …` /
  `window on <wall> at <pos> …` / `opening on <wall> at <pos> …`, where `<pos>` is millimetres along
  the wall or a percentage (`50%`). `swing into <room>` picks the swing direction toward a named room;
  `hinge near start|end` hinges at the segment end nearer a wall end. (Off-wall/ambiguous →
  `E_ATTACH_WALL_REF`; past the wall → `E_ATTACH_POS_RANGE`.)
- **Lay rooms with `strip`.** `strip right at (0,0) gap 0 height 4000 { room … room … }` places a row
  (or column, with `down`/`up` + `width`) of rooms end to end — no per-room `at`.
- **Place furniture by anchor.** `furniture <kind> in <room> anchor <9-point anchor> [flush] [inset <mm>] …`
  snaps a piece to a room corner or edge — the anchor is one of `top-left`, `top`, `top-right`,
  `left`, `center`, `right`, `bottom-left`, `bottom`, `bottom-right`; `against wall <id>` backs
  plumbing/kitchen fixtures onto a real wall face. Both are closed-form and never float or penetrate.
- **Add `flush` and never compute half a wall thickness.** A room's rectangle runs along wall
  *centerlines*, so a bare `anchor bottom` leaves the piece's back inside the solid
  (`W_FURNITURE_WALL_COLLISION`). `anchor bottom flush` measures from the backing wall's inner **face**
  instead, and `flush inset 50` from 50 mm off it — so write `furniture wc in r_bath anchor bottom flush
  size 400x700`, not an `inset 100` you worked out from a thickness you never named. (`flush` needs an
  anchored edge: on `centered`/`anchor center` it is `E_FURN_FLUSH`.)
- **Every room still needs a way in** — put a `door` or cased `opening` on a wall of *every* room
  (an open-plan space still needs a modeled opening), and keep furniture out of the doorway approach
  (≥300 mm) and the leaf's swing.
- **Absolute `at (x,y)` is the fallback**, not the default — reach for it only when no attachment
  expresses what you mean.

See `examples/attached.arch` for a full one-bedroom authored this way, and `archlang spec` for the grammar.

## Author a repeating piece ONCE, then place it (v1.22)

When a building repeats — two wings, six wards, a floor of identical units — do **not** copy the
statements and re-add an offset to every coordinate. That is how a plan gets 40 hand-edited numbers
that drift apart the first time the brief changes. Author the piece in its **own** coordinates from
`(0,0)` and place it:

```
component wing() {
  wall id=shell exterior thickness 300 { (0,0) (18000,0) (18000,12000) (0,12000) close }
  room id=main at (0,0) size 18000x9000 label "Gallery" uses living
  room id=corr at (0,9000) size 18000x3000 label "Corridor" uses circulation
}

place wing() as west at (0,0)
place wing() as east at (42000,0) mirror x
```

- **`as` names the instance, `at` places it; both are required.** Ids inside become
  `west.main` / `east.main`, and you address them by that dotted name everywhere a reference is
  taken: `wall west.shell`, `in west.main`, `archlang describe --room west.main`. (A dotted name in a
  *declaration* is `E_DOTTED_DECL` — the namespace belongs to the `place`.)
- **`rotate 0|90|180|270` and `mirror x|y` are exact**, and a mirror is real physics: door swings,
  fire exits and fixture facings all come out mirror-image. Prefer `mirror x` over `rotate 180` for a
  symmetrical pair — a 180° turn also swaps which side the corridor is on.
- **A whole FILE can be the component:** `import "wing.arch" as wing` binds that file's top-level
  drawable statements as a zero-argument component (its plan settings are ignored — the root plan
  owns the sheet). One file, one room or wing, exactly as you would organise components in code.
- **A `place`d instance is also a zone**, so `describe().zones`, `archlang describe --zone west` and the
  grouped `schedule rooms` table work with no extra declaration.
- **The bare call `wing()` is the OLD inline macro** — caller's coordinates, caller's id counters, no
  namespace. Keep it for a small parameterised motif; use `place` for a piece of building.
- **A component is a closed world going out:** the plan can reach into it (`wall west.shell`), but
  the component cannot reach out. Let the parent draw the connecting doors — that is the whole
  composition contract. Verify with `archlang describe --json` → `instances[]`.

See `examples/museum-wing.arch` + `examples/museum-wings.arch`.

## Self-correct with data, not guesswork

`archlang compile --json` returns every problem as a `Diagnostic` with a byte span, `line`/`col`, a
catalogued `E_*`/`W_*` code, and a prose `fix`. Where the correction is a mechanical text edit, the
diagnostic also carries **machine-applicable `fixes`**:

- **`archlang fix`** applies them in a bounded, self-checking fixpoint — **only `machine-applicable` by
  default** (`--unsafe` also applies `maybe-incorrect`; `--dry-run` previews; `--force` keeps a pass
  that would otherwise roll back). Use it to clear the syntactic faults before you touch anything by
  hand.
- **`archlang fix` is syntactic; `archlang repair` is geometric.** `fix` rewrites text where the right text is
  known (e.g. an off-wall door → the attachment form); `repair` *moves furniture* to a position no
  text edit could express. They compose — fix first, then repair.
- **`archlang fix` also applies fix-carrying *lint* advisories**, not only compile-stage faults — e.g.
  `W_ALIAS_MATCH` (a room's use inferred from an indirect label alias) fixes by inserting the explicit
  `uses …` it inferred. Before editing, `archlang describe --json`'s **`freedom`** block tells you which
  element positions were **hand-authored** (`absolute`) vs **derived** by the resolver
  (relational/strip/attached/anchored/against-wall), so you know which numbers are safe to nudge.

## Fix the topology: add doors & windows the room graph needs

`fix`/`repair` never add a door or a window — *where* to put one is a design choice the compiler must
not make. When lint reports `W_ROOM_UNREACHABLE`, `W_ROOM_DISCONNECTED`, `W_NO_ENTRANCE`,
`W_BATH_VIA_BEDROOM`, or `W_BEDROOM_NO_WINDOW`, ask ArchLang for candidates:

- **`archlang suggest plan.arch --json`** returns ready-to-paste `door`/`window` statements (furniture-aware
  — a door candidate never opens onto a wardrobe; each references its wall by a **stable ref** — an
  authored id or a unique category — or absolute coordinates, never a re-bindable positional id) plus a
  rationale for each — for a room with no path back (`W_ROOM_UNREACHABLE`), a building with no way in
  (`W_NO_ENTRANCE`), a bath reachable only through a bedroom (`W_BATH_VIA_BEDROOM`), or a windowless
  bedroom (`W_BEDROOM_NO_WINDOW`). Choose one and insert it, then re-run the loop. This replaces
  hand-computing coordinates.
- **Manual fallback** (if `suggest` offers nothing that fits): from `describe().access`, connect each
  unreachable room in priority — (1) a new **exterior entrance** `door on <exterior wall> at <pos>`
  into a living/kitchen/hall with an exterior edge (avoids routing through a bedroom); else (2) a
  `door on <shared wall> at <pos>` to an adjacent reachable, non-bedroom room; and give a windowless
  bedroom a `window on <its exterior wall> at <pos> width 1200`. Never make a bathroom reachable only
  through a bedroom. Then `archlang repair` (a new door may pinch furniture) and re-gate.

> An *existing* opening `validate` reports **off its wall** (`W_DOOR_OFF_WALL` /
> `W_WINDOW_OFF_WALL` / `W_OPENING_OFF_WALL`) is a mis-coordinate, not a missing connector — run
> `archlang fix` (it rewrites it to the attachment form) rather than adding a new one.

### Pick the door KIND before you widen the room

A door has a kind — `hinged` (the default) · `sliding` · `barn` · `bifold` · `pocket` · `garage` —
and it changes what the checks can say, not just the drawing. **Only `hinged` sweeps an arc**, so
`W_SWING_OBSTRUCTED` cannot apply to any of the others.

That makes the kind a legitimate answer to a diagnostic, and often the *right* one:

- `W_SWING_OBSTRUCTED` on a door into a tight room — a `sliding` or `pocket` leaf sweeps nothing, so
  the warning goes away because the plan genuinely fixed it, not because you silenced a rule. Moving
  the furniture is the alternative; pick whichever the brief actually wants.
- A `pocket` earns its own check instead: `W_POCKET_RUN` measures the wall the panel must slide into.
  Swapping one warning for the other is a real trade, so read the new one rather than assuming a win.
- Clauses are kind-specific and a wrong pairing **refuses** (`E_DOOR_KIND_CLAUSE`): `hinge` is
  hinged-only, `slide`/`open` are sliding-family-only, and `garage` takes no clause at all — which
  side it parks on is derived from which face has floor. A non-hinged kind on an `arc` wall also
  refuses (`E_DOOR_KIND_CURVED`).

`archlang spec` has the full grammar; `examples/bungalow.arch` is the worked plan.

### Declare `site` when the brief mentions orientation

`site { street <north|south|east|west> [hemisphere …] }` **draws nothing**. It exists so orientation
becomes a *fact the tools can check*, and without it two things silently cannot run:

- `describe --json` gains a `site` block naming five directions — `street`, `back`, `equator_side`,
  `sunrise_side`, `sunset_side` — and an intent's `windows.facing` may assert those names. **With no
  `site` declared, that assertion fails with `E_INTENT_NO_SITE`** rather than passing vacuously.
- `W_ROOM_NOT_EQUATOR_FACING` is the one rule that reads it, flagging a room whose windows all face
  away from the equator side.

So: if the brief says "south-facing living room", "morning light in the kitchen", or "faces the
street", declare `site` first — otherwise you have written a plan whose central requirement nothing
can verify. **It is a drafting heuristic for an aspect, not a daylight measurement**: there is no sun
model, no latitude and no date, and `_side` names must not be read as more than an orientation.

`examples/bungalow.arch` demonstrates both this and the door kinds above.

### Write a `height` only when the brief gives one

`height <mm>` (plan, `level` or `wall`) and `sill`/`head` on an opening are the vertical **datum**:
they draw nothing, because a plan is a horizontal cut, and `describe --json` reports them **only if
the source wrote one** — so adding a height you were not asked for changes what every consumer sees
for no gain. Write them when the brief names a ceiling, a parapet or a cill line; otherwise leave
them out and read the defaults from `archlang manifest --json`'s `datum` block.

## Ask the CLI, and read only what you need

The CLI documents itself, and every read can be narrowed at the source — never pull a whole plan's
facts into context just to filter them yourself.

- **`archlang <cmd> --help`** prints that one command's flags *and worked
  examples* — every command carries at least one copy-pasteable invocation. `archlang --help` lists the
  commands; `archlang --version` prints the version. A flag a command doesn't take is a usage error
  (exit `3`) with a did-you-mean, never a silently-swallowed filename — so a typo fails loudly
  instead of compiling the wrong thing.
- **`archlang describe --select <keys>`** emits only the named top-level keys (`rooms`, `doors`,
  `windows`, `openings`, `furniture`, `access`, `circulation`, `totals`, `freedom`, `caption`, …);
  the `ok`/`plan`/`units`/`diagnostics` envelope is always kept, so narrowing can't lose the verdict.
  **`archlang describe --room <ids>`** keeps only those rooms plus the doors/windows/furniture that touch
  them (whole-plan facts — `bbox`, `totals`, `caption`, each room's `adjacent` — stay whole-plan, so a
  narrowed read never lies about the building). Both mark the result with `filtered: true`.
- **`archlang lint|validate --code <CODE,…>` / `--severity error|warning`** show only the diagnostics you
  asked for. These are **display filters only**: `ok` and the exit code are always computed from the
  *unfiltered* set, so reading less can never turn a failing plan green. A filtered result carries
  `filtered: true` + `total_diagnostics`.
- **`archlang context --section spec|workflow|cli|errors`** prints one section of the bundle
  instead of all of it (about 109 KB in all) — `errors` for the diagnostic catalog, `cli` for the
  command reference.
- **`archlang fix --dry-run`** prints the exact unified diff it would write (to stderr; `--json` also
  carries it as `diff`) and touches nothing. When you do apply in place, **`--backup`** keeps the
  original bytes at `<file>.bak`.

## Structured authoring & constrained generation (optional)

- **Plan JSON.** Author or ingest the machine-native shape and compile it: `archlang compile plan.json
  --from-json -o out.svg`. The schema is served at
  [`/plan.schema.json`](https://archlang.uk/plan.schema.json).
- **GBNF.** To force a local model to emit only parseable ArchLang, constrain decoding with
  [`/archlang.gbnf`](https://archlang.uk/archlang.gbnf).

## Commands

```bash
archlang spec                              # the whole language in one page — READ THIS FIRST
archlang context                           # everything in one call: spec + this workflow + CLI reference + error catalog
archlang context --section errors          # just one section of it (spec|workflow|cli|errors)
archlang --help                            # list the commands
archlang manifest --json                   # the whole CLI API as data: commands, flags, formats, lint rules, error codes
archlang compile plan.arch -o out.svg --json   # render (also -f dxf|txt|json|pdf|png)
archlang compile plan.arch -f txt          # zero-dependency ASCII text plan on stdout
archlang compile plan.json --from-json -o out.svg   # compile structured Plan JSON (see /plan.schema.json)
echo '<source>' | archlang compile - -o - -f svg    # compile stdin → SVG on stdout
archlang fix plan.arch --dry-run --json    # preview the machine-applicable fixes as a unified diff (drop --dry-run to apply; --backup keeps <file>.bak)
archlang suggest plan.arch --json          # advisory door/window statements: unreachable room / no entrance / bath-via-bedroom / windowless bedroom
archlang describe plan.arch --json         # semantic facts: rooms, areas, adjacency, door connections, circulation
archlang describe plan.arch --select rooms,totals --room kitchen --json   # narrow the facts to what you actually need
archlang lint plan.arch --json             # architectural soundness warnings
archlang lint plan.arch --code W_NO_ENTRANCE --json   # display filter only — never changes `ok` or the exit code
archlang validate plan.arch --strict --json           # parse + resolve + lint; --strict fails on warnings (the ship gate)
archlang validate plan.arch --graph g.json --json     # also check interior-door adjacency against an intended graph
archlang repair plan.arch -o fixed.arch    # geometric corrector: furniture out of walls/doorways/swings + change log
archlang finish plan.arch --dry-run --json # after lint is clean: preview the furniture and sheet statements it would add (drop --dry-run to apply)
archlang fmt plan.arch --write             # canonical formatting
archlang batch a.arch b.arch -f svg --json # render many plans/variants at once → results[]
archlang preview plan.arch -o plan.png     # render a PNG to SHOW the user (--install fetches resvg if missing)
archlang new -o plan.arch                  # scaffold a starter plan
archlang explain E_ROOM_SIZE --json        # look up any diagnostic code
```

(An optional MCP server, `@chanmeng666/archlang-mcp`, wraps these same library functions for
MCP-native hosts — prefer the CLI when you have a shell; it costs nothing in context until called.)

## Key rules (full detail in `archlang spec`)

- **Units are millimetres** (a 4 m wall is `4000`); **origin top-left, +x right, +y DOWN**. An
  optional metric suffix is exact sugar for the same mm value — `4m` = `4000`, `40cm` = `400`,
  `20mm` = `20` — so you can write `4m` instead of hand-multiplying; bare numbers are unchanged.
- **Attach openings to walls** (`on <wall> at <pos>`) so they always sit on a segment; a raw `at`
  that lands off any wall warns (and `archlang fix` rewrites it).
- **Furniture draws real symbols, not boxes.** Every catalogued kind (`archlang manifest --json` →
  `fixtureCategories`) renders a plan symbol and **ignores `label`**; an uncatalogued word falls
  back to a labelled rectangle. Most kinds also carry a footprint, so `furniture <kind> against
  wall <id> in <room>` needs no `size` — `offset` is the piece's CENTRE along the wall run. Put
  fixtures in every bath and kitchen so lint stays quiet.
- **`dims auto`** draws dimension strings for you (`overall`, `rooms`, `walls`, or `all`).
- Edit is cheap: "make the bedroom 1 m wider" is a one-number change, then recompile.

Treat the CLI as the source of truth — author, render, and verify through it rather than reasoning
about SVG by hand.

## Task skills

Four short skills sit beside this one in `skills/`, one job each
(`npx skills add ChanMeng666/archlang` offers them with this one). Each is a
checklist of CLI calls and holds no language reference of its own:

- `archlang-brief-to-plan`: write a new plan from a written brief and check it against the brief.
- `archlang-edit-plan`: change an existing `.arch` with the smallest edit, then re-verify.
- `archlang-export`: deliver SVG, PNG, PDF or DXF files, with paper size, scale and storeys.
- `archlang-review-plan`: check a plan (lint profiles, the intent gate, suggestions) without editing it.
