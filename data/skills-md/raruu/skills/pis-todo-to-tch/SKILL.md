---
name: pis-todo-to-tch
description: "Turn Profile Plus todos (MCP profile-plus) into a formatted Polinema internship log book (DOCX + PDF). Use whenever the user runs /pis-todo-to-tch, or asks to \"buat log book\", \"bikin laporan magang\", \"generate log book\", \"cetak log book\", \"rekap todo jadi log book\", \"log book bulanan\", or wants their Profile Plus todo/attendance data converted into the official LOG BOOK KEGIATAN document. With no period it defaults to the current work week (Mon-Fri); also supports month, month/week, and date-range periods, and outputs to a 'Laporan <Bulan>' folder in the current working directory. PDFs are converted from the DOCX via LibreOffice when available, with an fpdf2 fallback. The SETUP argument bootstraps an empty working folder (personal config, environment report)."
---

# PIS Todo → TCH (Log Book) — Profile Plus → Log Book DOCX/PDF

Turn the user's Profile Plus activity into the official internship log book document.

The output follows the Polinema template: letterhead header, student info table, a daily table (`Hari, Tanggal | Jam Masuk | Jam Pulang | Kegiatan`), and a signature block. Todos fill the Kegiatan column; attendance fills the Jam Masuk/Pulang columns.

## Invocation

```
/pis-todo-to-tch <periode>, <word|pdf>
/pis-todo-to-tch SETUP
```

Both segments are optional.

| Segment | Meaning |
|---|---|
| 1 | Period. Empty = current work week (Mon–Fri, up to today). |
| 2 | Output format: `word`, `pdf`, or empty = both. |

`SETUP` (case-insensitive, alone) is not a period — it switches to setup mode (see below). If the argument is exactly `SETUP`, jump to **Setup mode** and do not generate any document.

Period formats:

| Input | Meaning |
|---|---|
| *(empty)* | Current work week: Monday–Friday, clipped to today (never future days) |
| `September` | September of the current year (past month: full; current month: 1st → today) |
| `September 2026` | Same, explicit year |
| `September/minggu 2` | Calendar week 2 (Mon–Sun), clipped to the month |
| `September/minggu 2->3` | Calendar weeks 2 through 3 |
| `Tanggal 2026-09-01 -> 2026-09-15` | Explicit date range (only this format for dates) |

Examples:

```
/pis-todo-to-tch
/pis-todo-to-tch September
/pis-todo-to-tch September 2026, pdf
/pis-todo-to-tch September/minggu 2->3
/pis-todo-to-tch Tanggal 2026-09-01 -> 2026-09-15, word
/pis-todo-to-tch SETUP
```

## Setup mode (`/pis-todo-to-tch SETUP`)

Bootstraps an empty working folder. **Never generate a document in this mode** — only config, and only after the user answers.

1. Run the environment report from the user's workspace (working directory):
   ```
   python3 <skill-dir>/scripts/build-logbook.py --setup
   ```
   It is read-only (creates nothing) and prints JSON: `cwd`, `config_exists`, `config`, `config_error`, `git` (`repo`/`root`/`ignored`), `python`, `libs` (`docx`/`fpdf`), `libreoffice` (path to `soffice` or `null`), `fonts.serif_found`, `assets`.

2. Show a short summary: the working folder (confirm it is the intended one), config status, missing libraries, git state.

3. **Config**:
   - `config` present → show the current values, then ask via the question tool which fields to update (multi-select, one option per field plus "semua sudah benar"). If the user picks fields, ask for their new values and rewrite the file. Keep the JSON shape.
   - `config_exists` false or `config_error` set → ask via the question tool for the six fields (`nama`, `nim`, `program_studi`, `mitra_industri`, `dosen_pembimbing`, `pembimbing_lapangan`) — one question per field, using the example values as the offered options where helpful. Then write `.pis-todo-to-tch.json` in the working folder.
   - Always re-run `--setup` afterwards to confirm the file parses and has no missing fields, and report the result.

4. **Git**: if `git.repo` is true and `git.ignored` is false, ask whether to add `.pis-todo-to-tch.json` to `.gitignore` at `git.root`. If the user agrees, append the line (create the file if needed) and confirm with `--setup` that `ignored` is now true. If not a repo, skip.

5. **MCP smoke test**: call `profile-plus_get_todo_history` with `limit: 1`. Report OK or the failure — this is informational, not a blocker.

6. **Final report**: config path, git state, libs, LibreOffice, MCP, plus suggested next command (e.g. `/pis-todo-to-tch` for the current work week). Do not generate anything.

## Step 1 — Resolve the period

The bundled script does all parsing deterministically. Never compute the period yourself. The script lives next to this file:

```
python3 <skill-dir>/scripts/build-logbook.py --input "<periode>" --resolve-only
```

It prints JSON with `start`, `end`, `label`, `folder`, and `dates`. On invalid input it exits 1 with an `ERROR:` message — relay that to the user and stop.

Show the resolved period to the user in one line, e.g. `Periode: 1 – 18 September 2026 (14 hari kerja)`.

## Step 2 — Config

Personal data lives in `.pis-todo-to-tch.json` **in the working directory** (the folder where the skill is invoked — the same folder that will receive `Laporan <Bulan>/`):

```json
{
  "nama": "Kamina Botan",
  "nim": "1234567890",
  "program_studi": "D-IV Teknik Informatika",
  "mitra_industri": "PT Hoshino Teknologi Nusantara",
  "dosen_pembimbing": "Kagamihara Nadeshiko",
  "pembimbing_lapangan": "Gotoh Hitori"
}
```

Resolution order:

1. `--config <path>` — explicit, must exist.
2. `<cwd>/.pis-todo-to-tch.json` — the working-directory config.
3. Missing → the script copies `config.example.json` to `<cwd>/.pis-todo-to-tch.json` and exits 2 with `CONFIG_CREATED:`. When that happens: tell the user the config was created, show its contents, and ask them to confirm or edit the values. **Do not generate the document in the same run** — wait until the user says the data is correct, then re-run. If the folder is a git repo, the script also prints a `HINT:` about adding the file to `.gitignore` — relay it.

Always run the script with the user's workspace as the working directory (e.g. pass `workdir` to the bash tool) so the config is read from and created in the right place. There is no parent-directory lookup.

If the user gives their real data in chat, edit the config file for them, then continue.

## Step 3 — Fetch data from MCP

Fetch todos and attendance for the resolved range, then write them to a temp JSON file:

```json
{
  "todos": [{"date": "yyyy-MM-dd", "task": "...", "status": "DONE", "created_at": "..."}],
  "attendance": [{"date": "yyyy-MM-dd", "check_in": "...", "check_out": "...", "status": "HADIR"}]
}
```

- `profile-plus_get_todo_history` — call once per month the range touches (`month`/`year` params; paginate with `page` until all items are collected). Keep only entries whose `date` falls inside the range.
- `profile-plus_get_attendance_history` — one call with `start_date`/`end_date` covering the range (it accepts `yyyy-MM-dd`), paginate if needed.
- Keep the `task`, `date`, `status`, `created_at` fields from todos; keep `date`, `check_in`, `check_out`, `status` from attendance.
- Write the file to a temp path (e.g. `/tmp/pis-todo-to-tch-<timestamp>.json`), pass it via `--data`, and delete it afterwards.

If there are no todos and no attendance in the range, say so and stop — do not generate an empty document.

## Step 4 — Generate

```
python3 <skill-dir>/scripts/build-logbook.py --input "<periode>" --data <temp.json> --outdir "<cwd>" [--format word|pdf]
```

Run this with the user's workspace as the working directory (same as Step 2) — the config is read from there.

The script:

- reads `.pis-todo-to-tch.json` from the working directory,
- fills the DOCX template (placeholders → config values),
- clones one table row per day (Mon–Fri always; Sat/Sun only when that day has data),
- fills Kegiatan with one bullet per todo, duration stripped (`Module -> activity`, keeping the module prefix),
- fills Jam Masuk/Pulang from attendance (`HH:MM`), or `-` when absent,
- writes `Laporan <Bulan> <Tahun>/Log Book <label>.docx` and `.pdf` in the working directory.

PDF fidelity: when LibreOffice (`soffice`) is installed, the PDF is converted from the generated DOCX, so it matches the DOCX exactly. Without it, the script falls back to a built-in fpdf2 renderer (close but not pixel-identical) and adds a warning. The output JSON field `pdf_engine` is `"libreoffice"` or `"fpdf2"`.

It prints JSON with `config`, `files`, `rows`, `overwritten`, `pdf_engine`, `days_without_hours`, and `days_without_activities`. Requirements: Python 3 with `python-docx`; `fpdf2` only needed for the PDF fallback.

## Step 5 — Report

Report per generated file: path, number of day rows, and any warnings:

- days whose jam columns are `-` (no attendance data),
- days with an empty Kegiatan (no todos),
- if `overwritten` is true, say the previous files were replaced.

Example:

```
✅ Laporan September 2026/Log Book September 2026.docx (+ .pdf)
   14 baris hari, 4 halaman PDF
   ⚠️ 7 hari tanpa kegiatan: 2, 3, 4, 7, 8, 10, 11 September
```

## Edge cases

- **SETUP with other arguments** (e.g. `/pis-todo-to-tch SETUP, September`) → treat `SETUP` as the mode and ignore the rest; mention it.
- **SETUP when config is already valid** → do not overwrite silently; show values and offer selective updates.
- **SETUP in a non-git folder** → skip the `.gitignore` step entirely.
- **SETUP when libs are missing** → report it in the summary and include the `pip install python-docx fpdf2` hint; still finish the other steps.
- **SETUP when MCP is unreachable** → report the smoke-test failure and continue; the user can fix the MCP config later.
- **Invalid period** → relay the script's `ERROR:` message; suggest a valid format.
- **Config missing in workdir** → the script creates `.pis-todo-to-tch.json` from the example and exits 2; show it to the user and wait for confirmation before generating.
- **Config invalid JSON or missing fields** → the script prints a friendly `ERROR:`; fix the file (or ask the user) before retrying.
- **`--config` points to a missing file** → hard error; never auto-create an explicit config path.
- **Future month/week** → the script rejects it; explain the period has not started.
- **End date in the future** → the script clips it to today and adds a warning; surface it.
- **No Python / missing libs** → `pip install python-docx fpdf2` (or `uv pip install`). `fpdf2` is only needed for the PDF fallback.
- **No LibreOffice** → PDF still works via the fpdf2 fallback; tell the user the layout may differ slightly and that installing LibreOffice (e.g. `sudo pacman -S libreoffice-fresh`) makes the PDF identical to the DOCX. Never install it yourself.
- **Weekend rows** → only appear when there is todo or attendance data on those days.
- **National holidays** → not detected; the day still appears if it is a weekday with attendance data. Mention that holidays can be edited manually in the DOCX.
- **Status-only days** (CUTI/IZIN/SAKIT attendance, no todos) → Kegiatan shows the status label (Cuti/Izin/Sakit).
- **Multiple modules in one day** → all bullets are kept; do not merge or reorder them (ordered by `created_at`).
