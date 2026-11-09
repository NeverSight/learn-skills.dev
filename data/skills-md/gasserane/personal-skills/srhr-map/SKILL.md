---
name: srhr-map
description: SRHR interactive map skill (pilot). Refresh mode turns new internal drop-in files into a short review workbook, then writes a colleague's answers into a new map register edition. Publish mode puts an approved register edition into the map decks and builds the data workbook, the Power BI dataset and the web map from it. Call by name only.
disable-model-invocation: true
---

# SRHR interactive map skill (pilot)

This skill keeps the SRHR interactive map's data up to date. It has two modes:

- **Refresh** (ready): new files come in, a person checks what changed, and the answers go into a new edition of the map register.
- **Publish** (ready, map owner): the values of an approved register edition go into the existing map decks, and four more outputs are built from the same register: a data workbook, a Power BI dataset file, the internal web map and a summary web map for donors and partners. A change that needs new or deleted shapes on a deck is not publish: it waits for the deck generator (phase e).

**What this folder must never hold.** This repository is public. No register rows, organisation or country names, fund names, amounts, codes, or local file paths. The register, the drop-in files and the two config tables live in the organisation's own "SRHR map data" folder, never here.

## Before you start

You need the path to the "SRHR map data" folder. If the person has not given it and `SRHR_MAP_ROOT` is not set, ask: "Where is the SRHR map data folder?" Do not guess a path.

The folder holds:

- `drop_in/<reporting year>/`: the new files, one subfolder each: `dhis2/` (service statistics export), `subgranting/` (grant ledger), `business_plans/` (business-plan focus coding sheet).
- `intelligence_tool/`: the latest Intelligence Tool snapshot, `master_countries.csv`, and optionally `source_register.csv`.
- `config/`: `streams.csv` (grant stream names and legend labels) and `ma_codes.csv` (organisation codes, ticked by the map owner). Optional: `country_aliases.csv` (ledger spellings of a country) and `stream_overrides.csv` (for one country and one edition, show a ledger stream as a different map stream). Only rows the map owner ticked are used; an override row counts only for its own edition.
- `map_register/`: one register file per map edition. An existing edition is never changed.
- `review/`: the review workbooks and run files this skill writes.

The scripts are in this skill's `scripts/` folder. Every command takes `--map-root <folder>` (or uses `SRHR_MAP_ROOT`) and `--year <reporting year>`. The edition built is the next year unless `--edition` says otherwise.
On Windows, give `--map-root`, `SRHR_MAP_ROOT` and `SRHR_MASTER_COUNTRIES` as Windows paths with a drive letter, not `/c/...`. Python does not read a Git Bash `/c/...` path in an environment variable, so the tests' `public_repo_clean` check then fails with "not set or not found".

## Refresh mode, for a colleague

1. **See what files are needed.** Run `python refresh.py list --year <year>`. It names each file expected in `drop_in/<year>/` and says which are already there. Ask the person to put any missing file there.
2. **Check the files.** Run `python refresh.py check --year <year>`. If a file does not match its contract, the command stops with one line starting `Stopped:`. Read that line to the person in plain words, ask them to fix or replace the file, and run check again. Never edit a drop-in file yourself.
3. **Make the review workbook.** Run `python refresh.py review --year <year>`. It prints the path of a workbook in `review/`. Tell the person how many lines are on "Must check" and pass on every `note:` line (for example an organisation code nobody has ticked yet).
4. **The person answers.** They open the workbook, type their name and the date on "How to use", and for each line on "Must check" open the link, compare, and choose Correct, Wrong (with the right value) or Not sure. They save the file. A line that stands for several values takes Correct or Not sure only: Wrong there leaves them unanswered, because one right value cannot fit each of them.
5. **Write the answers.** Run `python refresh.py apply --year <year> --workbook <path>`. A line starting `Refused` or `Stopped` means nothing was written: say why and what to fix (often the name or date cell is empty, or the file is open in Excel). A workbook from an earlier review is refused once review has run again for its topic: ask the person to answer the newest workbook. Otherwise report how many rows were ticked and how many still need a tick.
6. **Approval (map owner only).** Run `python refresh.py approve --year <year> --by "<name>"`. It refuses while any change still needs a person's tick and lists those changes.

Rules that hold in every step:

- A person ticks every change. Never write a tick, a name or a date into the register yourself.
- Never open an existing register edition for writing. `apply` writes the new edition and backs it up before any rewrite.
- Use `--topic HIV` or `--topic funding` to refresh one topic only.
- Refresh never adds a country to the map. A country in the new files with no row in the last edition is listed as a note; adding it is a publish decision for the map owner.

## Where refresh runs: Claude Code

Refresh runs in Claude Code, not Cowork: Cowork could not open the synced "SRHR map data" folder. Start Claude Code from your usual work folder, never from inside "SRHR map data", and pass `--map-root` to every command.

The review workbook gets the full IPPF brand (logo, header and footer) when the organisation's reporting package is found: set `WORK_FOLDER_ROOT` to the work folder, or run from inside it. Without that package, the workbook uses the brand colours and font without the logo.

## Publish mode, for the map owner

Publish runs in Claude Code on Windows with desktop PowerPoint (the deck swap uses PowerPoint COM). Every step goes through one command, `python publish.py <step> --map-root <folder> --decks <deck folder>`. Each step runs alone. The edition is the latest `map_register_<year>.csv` unless `--edition` says otherwise. Give both folders as Windows paths with a drive letter. The deck folder is not inside the map root: it is the folder that holds the four `Map X - *.pptx` decks, so name it explicitly rather than guessing it from the map root. Every output goes to `publish/<edition>/` in the "SRHR map data" folder, never to this repository, because the outputs name organisations.

1. **Plan the deck swap (reads only).** Run `python publish.py plan ...`. It lists every deck shape that carries a register value, then writes the swap plan to `publish/<edition>/run_<time>/swap_plan.csv`. Read the counts to the map owner. Exit 2 means a structure change (a country changes class, gains or loses a stream, or appears on one side only). Stop there: a swap may not add or delete shapes, so that edition waits for the deck generator (phase e).
2. **Swap the decks.** Run `python publish.py swap --plan <that swap_plan.csv>` first without `--apply`. It prints the plan and opens no deck. Then, only with the map owner's yes, run it again with `--apply`. It backs up each deck, reads every planned shape before writing, sets one property per shape, reads it back, and saves only when every read-back is right.
3. **Build the data workbook, the Power BI dataset and the web map.** Run `python publish.py workbook ...`, `dataset ...` and `webmap ...`. A target that exists is never overwritten (exit 2), because a person may have edited it. If a rebuild is really needed, the map owner moves the old file first. The web map downloads its pinned country outlines and d3 7.9.0 once, into `publish/_geometry/`, and refuses a d3 file whose hash differs from the one cdnjs publishes, or a geometry file whose hash differs from the pinned one. With no network and no cached copy, it stops (exit 1) and writes nothing.
4. **Build the summary web map.** Run `python publish.py summary --map-root <folder>`. It needs no decks. It writes `publish/<edition>/webmap_summary_<edition>.html` (see "Summary web map" below).
5. **Check every output against the register.** Run `python publish.py check ...`. It exits 0 only when the decks, every workbook cell and link, every dataset cell (csv and xlsx), every web map colour, tooltip, legend, filter and title, and the summary page (views with their names and no extra view, headline sentence, no map letters on the tabs, footer text from `config/summary_page.csv`, every counted country on the WHO list, forbidden-text scan) agree with what the register gives now. While the summary page does not exist yet, check reports `FAIL summary`, as it does for any missing output. An output kept from an earlier build fails here when the register has changed since. Report any `FAIL` line in plain words.

`python publish.py all ...` chains the steps, the summary page included. It stops at step 2 when swaps are planned (exit 3), so that the map owner reads the plan before anything is written. An output that exists is kept, and the check still runs on it.

**The five approval gates.** The map owner sees and approves each output before anyone else uses it: (1) the swapped decks, (2) the data workbook, (3) the Power BI dataset, after loading it in Power BI Desktop, (4) the web map, (5) the summary web map. Record each approval as one row (output, approver, date, note) in `publish/<edition>/approvals.csv`. Never write an approval row the map owner has not given in this session.

**When the edition has not changed (route C).** The register was first filled from the decks' hover texts, so a swap on the same edition changes only what the register changed since then, and often nothing. "0 shapes changed" is evidence only if the swap has shown it changes shapes when it should. So before a real swap, run it on a copy (`swap --copy-to <scratch folder>`) with a planted change in a copy of the register. The swap must change exactly the planted shapes. Only then run the real swap, which may change only the shapes the register check reported as different.

**Web map.** The page is one self-contained file. Its tooltips are the deck hover texts with the register values put in by the same function the swap uses, so the deck and the web map say the same words. d3 is inside the file, so the map runs offline; colleagues download the file and open it in a browser (SharePoint, Teams and Outlook previews do not run it). Share the file inside the network only. A claude.ai artifact is published only on the map owner's explicit yes in that session. A version shared outside the organisation's network needs aggregated data. The map owner decides that at gate 4, and it is not built by default. To check the page in a browser, serve a copy from a scratch folder on a port nothing else uses, then hash what the URL returns and compare it with the built file: on Windows a second `python -m http.server` binds a port already in use without an error, and the older server keeps answering. A master-list country with no tooltip (withdrawn or non-member) shows only its name on hover, on both pages, and stays out of the Tab order. Grey context countries outside the master list also show only their name on hover or tap; they take no keyboard focus. `config/context_names.csv` in the map root sets those names (see below); change a grey name there, never in the code.

**Summary web map.** A second page for donors and partners, built by `publish_summary.py` with the same page code as the web map. It shows a headline ("IPPF member associations and partners work in N of the M countries of the WHO European Region.") and three maps: members and partners, IPPF funding in three bands, and new HIV diagnoses for one rate year (`register_deck_check.RATE_YEAR`; a newer year in the register is a printed note, never shown). Every number is computed at build time. Its hover texts come from its own templates, never from a deck ScreenTip, and it names no stream, fund or member association. N counts the active members, the same countries the membership map colours; a member with no map outline is still counted and named in a build note, and a counted country missing from the WHO list stops the build. The tabs read the view name only (the page data sets `tab_letters` to false); the internal web map keeps "Map A" to "Map D", which match the deck names.

It reads three config files in the map root, never in this repository, because the contact, the unit and the allowed terms belong to the organisation:

- `config/who_europe.csv` (`iso3,country`): the WHO European Region member states; M is its row count. A file saved by Excel (byte-order mark, blank rows, lower-case codes) loads the same. A file with no `iso3` column or no row stops the build. `config/who_europe.source.txt` records the source page, the date it was checked and the row count; the code does not read it, so update it whenever the list changes.
- `config/summary_page.csv` (`key,value`): `contact`, `author_unit` and `disclosure`, all three non-empty, for the page footer. The footer prints the disclosure word for word and the unit on its own line ("Prepared by ...").
- `config/context_names.csv` (`geometry_name,shown_name`) is required by both pages and by `check`. It maps a grey shape's name in the geometry file to the name its hover shows; an empty `shown_name` keeps that shape silent, and an unlisted name shows as the geometry file spells it. The map owner decides these names (some are political choices). The table stays in the private config because it names places on the master list, which this public skill must not. A missing file, a wrong header or a name listed twice stops the build, and `check` fails a kept page whose grey names differ from the file.
- `config/summary_scan_allow.csv` (`term,ticked_by,date`) is optional. A missing file means an empty allowlist. A term counts only when `ticked_by` is filled, so a row the map owner has not ticked clears nothing.

**The forbidden-text scan.** Before the file is opened, the build scans the finished page for every stream `key`, `label` and `ledger_names` value in `config/streams.csv` and every `org_name` and `ma_code` in `config/ma_codes.csv`. Scope: the visible page text outside scripts and styles, and every string value in the embedded map data. Number values (so geometry coordinates), data keys, HTML attribute values and the d3 library are not scanned. A term matches as a whole word and case-sensitive, so a key that is an ordinary English word does not hit inside a longer word. Any hit stops the build and nothing is written. If either config file yields no term or lacks one of these columns, the build stops too, so an unreachable or emptied file can never make the scan pass. A false positive is cleared only by a ticked row in the allowlist, never by editing the term list. `check` re-runs the same scan on the page as it is on disk. A scan that has never failed proves nothing: before a gate, plant one real term in a hover text of a scratch copy and confirm the scan finds exactly that one hit.

**Browser check of the web map.** The Chrome extension refuses a page opened straight from disk, so serve a copy from 127.0.0.1. Probe the port with curl first and assert a marker of the new build in the response (for example `id="zoom-in"`): on Windows a second server can bind a port while an older one keeps answering with the old file. Check every tooltip at full view and zoomed in. A Chrome window in the background draws only a few animation frames a second, so zoom transitions stall: wait until the zoom reaches the state you need, never a fixed sleep.

## Other scripts here

- `dropin_check.py`: checks one drop-in file against its contract (used by `check`).
- `derive_rows.py`, `compare_register.py`, `review_workbook.py`, `apply_answers.py`: the steps `refresh.py` chains.
- `config_tables.py`: reads and validates the two config tables.
- `register_deck_check.py`: compares a register edition with the published map decks.
- `publish.py`: the publish command; `deck_shapes.py`, `publish_plan.py`, `publish_swap.py`, `publish_workbook.py`, `publish_dataset.py` and `publish_webmap.py` are the steps it chains, and `computed.py` holds every count, class and title they share.
- `shared/srhr_data_contract.v1.json`: a byte-identical copy of the data contract shared with the SRHR Intelligence Tool. Never edit it here.
- `contracts/`: one contract per drop-in file. They name columns and rules only.
