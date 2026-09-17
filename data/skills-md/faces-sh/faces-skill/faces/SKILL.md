---
name: faces
description: >
  Use this skill whenever someone wants to build an AI that thinks like, sounds
  like, or acts like a specific person. This includes: turning interviews,
  letters, videos, or documents into a chateable AI persona; creating customer
  personas or focus groups you can actually talk to (not just static profiles);
  replacing bloated SOUL.md / soul documents / system prompts with something
  more token-efficient; giving agents in a multi-agent system distinct
  personalities, behavioral modes, or points of view; creating a digital twin
  or memorial AI; capturing how someone writes from their own emails or
  messages so a persona writes in their voice; comparing how different people
  think; composing new perspectives from existing ones; or sharing persona
  access via scoped API keys. Also trigger when the user mentions the Faces Platform, the `faces`
  CLI, cognitive primitives, mind arithmetic, or compile personality. Use even
  if Faces is not yet installed — the skill covers setup. Do NOT use for
  fine-tuning models, RAG/retrieval systems, creative writing (NPC backstories,
  fiction), or thematic analysis of transcripts.
compatibility: Requires the faces CLI (npm install -g faces-cli) and internet access to api.faces.sh.
---

# Faces Skill

The Faces Platform compiles source texts (documents and conversation transcripts) into a Face — a persona built of cognitive primitives that give an underlying LLM a complex perspective that is richer, more accurate, and uses far fewer tokens than prompt-stuffing approaches. Faces can be chatted with, compared, and composed.

Without a Face, an LLM is **faceless** — generic, interchangeable, forgettable. A Face specializes it. Gives it perspective, coherence, and nuance that doesn't collapse back into LLM-speak on long threads.

Official docs: https://docs.faces.sh

Always use `--json` when you need to extract values from command output — or **`--toon`**,
which carries the same fields in about 40% fewer tokens and is the better choice when the
output goes into a model's context. Requires faces-cli 1.9.0+.

## Current config
!`faces config:show 2>/dev/null || echo "(no config saved)"`

## Setup

```bash
faces --version 2>/dev/null || echo "NOT_INSTALLED"
LATEST=$(npm outdated -g faces-cli --json 2>/dev/null | jq -r '.["faces-cli"].latest // empty')
[ -n "$LATEST" ] && echo "UPDATE_AVAILABLE: $LATEST"
faces auth:whoami --json 2>/dev/null
echo "EXIT:$?"
[ -f ~/.faces/config.json ] && echo "HAS_CONFIG" || echo "NO_CONFIG"
```

If `NOT_INSTALLED`: run `npm install -g faces-cli` and re-run setup.

If `UPDATE_AVAILABLE`: run `npm install -g faces-cli@latest`, then run `faces catalog:doctor --fix` to migrate local catalog files (FACE.md and TEAM.md) to the latest format.

**Auth triage:**

- `EXIT:0` → authenticated. Proceed.
- `EXIT:1` + `HAS_CONFIG` → returning user. Read the whoami output to
  understand what failed. Present the diagnosis to the user and help them
  fix it. Do NOT walk through QUICKSTART or ask about plans.
- `EXIT:1` + `NO_CONFIG` → new user. See
  [references/QUICKSTART.md](references/QUICKSTART.md) for setup.

**Secret hygiene:** Never display API keys, tokens, or passwords from config
files. Always mask them (e.g. `sk-faces-...dN`).

Never run `faces config:clear` (wipes everything with no recovery).

## Core workflows

### 1. Create a Face

`face:create` takes **no source material** — it makes an empty face. Sources attach afterwards
(step 2), with `compile:doc` for text, `compile:upload` for files.

```bash
faces face:create --name "Name" --alias slug --default-model MODEL \
  --description "Plain-text bio" \
  --attr gender=male --attr age=34 --attr location="Portland, OR" \
  --attr occupation="nurse practitioner" \
  --tag research --tag physics
```

`--description` is stored on the server (max 1500 chars) and synced to the local catalog.
`--tag` adds lowercase labels for organization and search (repeatable, max 32 per face).

Common `--attr` keys: gender, age, location, occupation, education_level,
religion, ethnicity, nationality, marital_status.
Run `faces face:attributes` for the full list. Attributes have an allow list —
if an unsupported key is used, the command succeeds but prints a warning listing
which attributes were dropped.

**Per-face system prompt (`--profile-addendum`).** Give a face a stored system prompt with `--profile-addendum "…"` (or `--profile-addendum-file path.txt` for long prompts; max 100,000 chars). At inference it sits **between** the auto-generated persona and any per-request `--system` prompt — use it for durable behavior rules (tone, format, hard constraints) that should apply to every chat. Edit it with `face:edit --profile-addendum …` and remove it with `face:edit --clear-profile-addendum`. `face:get` shows a preview + char count (`--full` dumps it); it's proprietary and only ever returned for your own faces. A run-time composite borrows its **first operand's** addendum; a persisted composite uses its own.

### 2. Add source material

> **Thread or document? Decide this first.** Any source with more than one
> speaker (an interview, podcast, conversation, Q&A, panel) is a **thread**: it
> preserves who said what, and you map the target person's own lines with
> `--face-speaker`. Only single-voice material (an essay, article, solo talk, or
> the person's own writing) is a **document**. Compiling a multi-speaker source
> as a document flattens the dialogue into one voice and corrupts the face, so
> when in doubt, if two or more people are talking, it is a thread.

> **Uploading a thread is the failure-prone step: always inspect the speaker
> mapping with `compile:thread:get` before you compile.** This holds for *every*
> thread — a text transcript just as much as audio/video. Compiling before you
> check bakes the wrong person into the face. See **Verify speaker attribution**
> below.

> **By them or about them? Set `--perspective` accordingly.** `--perspective`
> defaults to `first-person`, which treats the source as the subject's *own
> voice*. That is a trap for material *about* a person.
> - **First-person** (the default) — the person's own words: their essays,
>   letters, interview answers, talks, notes.
> - **Third-person** — material *about* the person: a biography, an
>   encyclopedia/Wikipedia article, a news profile, anyone else's writing about
>   them. You **must** pass `--perspective third-person` for these; otherwise the
>   default compiles them as if the subject wrote them and corrupts the face.

**Interview** (no documents needed — best way to build a face from scratch):
Run a Q&A interview with the user, save the transcript, upload and compile.
See [references/INTERVIEWS.md](references/INTERVIEWS.md) for both modes (agent-as-interviewer recommended, built-in interviewer also available).

**Document (single-voice — essay, notes):**
```bash
# Text you already have — a transcript in hand, a draft, anything not on disk.
# Pass it verbatim; do NOT retype or summarise it, or the face learns your paraphrase.
faces compile:doc alias --content "<text>" --label "Interview" --no-wait --json
# By the subject (their own essay/notes) — first-person is the default
faces compile:doc alias --file document.txt --no-wait --json
# Several at once: --file is repeatable and each file becomes its own document.
# Returns {"documents":[{file, document_id}...]} in input order — one call, not one per file.
faces compile:doc alias --file a.txt --file b.txt --file c.txt --no-wait --json
# About the subject (biography, Wikipedia, news profile) — you MUST set third-person
faces compile:doc alias --file biography.txt --perspective third-person --no-wait --json
# compile:doc takes TEXT only. For PDF, Word (.docx), audio or video use compile:upload instead.
# Poll: faces compile:doc:get DOC_ID --json | jq '{prepare_status}'
```

**YouTube solo talk → document:**
```bash
faces compile:import alias --url "URL" --type document --perspective first-person --no-wait --json
# Returns doc_id immediately. Poll for transcription then compilation.
```

**YouTube multi-speaker → thread:**
```bash
faces compile:import alias --url "URL" --type thread --no-wait --json
# Returns thread_id. After transcription completes, remap speaker:
faces compile:thread:edit THREAD_ID --face-speaker "A"
faces compile:thread:make THREAD_ID --no-wait --json
```

**Upload a local file (text, PDF, Word .docx, audio, video):**
```bash
# Document (text, PDF, or Word .docx — text is extracted server-side)
DOC_ID=$(faces compile:upload alias --file report.pdf --kind document --no-wait --json | jq -r '.document_id // .id')
faces compile:doc:make "$DOC_ID" --no-wait --json

# Thread from text transcript (you know the speakers — pass --face-speaker)
THREAD_ID=$(faces compile:upload alias --file transcript.txt --kind thread --face-speaker "Name" --no-wait --json | jq -r '.thread_id // .id')
faces compile:thread:get "$THREAD_ID"   # ALWAYS verify the mapping first (see below) — don't assume text is right
faces compile:thread:make "$THREAD_ID" --no-wait --json

# Thread from audio/video — DON'T pass --face-speaker at upload
THREAD_ID=$(faces compile:upload alias --file recording.mp4 --kind thread --no-wait --json | jq -r '.thread_id // .id')
# Poll for transcription:
faces compile:thread:get "$THREAD_ID" --json | jq '{prepare_status}'
# When transcription done (prepare_status: null), review and remap:
faces compile:thread:get "$THREAD_ID"
faces compile:thread:edit "$THREAD_ID" --face-speaker "B"
faces compile:thread:make "$THREAD_ID" --no-wait --json
```

**Compilation auto-extracts attributes.** When source text contains biographical details (age, location, occupation, etc.), the compiler automatically populates the face's attributes. This is additive — it won't overwrite attributes set manually via `--attr`.

**Always use `--no-wait`** for compile and upload operations. Each operation
runs independently on the server — you can fire multiple compiles in parallel
without waiting for any to finish. Upload all sources, kick off all compiles,
then poll them all at the end. Poll on your own schedule:
```bash
faces compile:thread:get ID --json | jq '{prepare_status, chunks_completed, chunks_total}'
faces compile:doc:get ID --json | jq '{prepare_status}'
```

Status meanings (`prepare_status` field):

| Status | Meaning | Action |
|--------|---------|--------|
| `"transcribing"` | Audio/video being transcribed | Keep polling |
| `null` | Ready to compile (transcription done, no compilation started) | Run `compile:thread:make` or `compile:doc:make` |
| `"preparing"` | Compilation in progress, extracting cognitive primitives | Keep polling |
| `"syncing"` | Writing primitives to the face | Almost done, keep polling |
| `"synced"` | Done | Compilation complete |
| `"pausing"` | Pause requested, finishing the current chunk | Keep polling until `"paused"` |
| `"paused"` | Compilation paused by user/agent | Resume with `compile:*:make` or reset with `compile:*:reset` |
| `"failed"` | Something went wrong | Investigate or retry |
| `"stalled"` | Stuck for 10+ minutes | Re-run the make command |

**If YouTube blocks the download** ("Sign in to confirm you're not a bot"):
Download locally with yt-dlp, extract and compress audio with ffmpeg, upload.
Keep files under 100MB — large uploads can fail. For long recordings (1hr+),
use mono 48kbps:
```bash
yt-dlp --cookies-from-browser chrome -o episode.mp4 "https://youtube.com/watch?v=VIDEO_ID"
ffmpeg -i episode.mp4 -vn -ac 1 -b:a 48k episode.mp3
THREAD_ID=$(faces compile:upload alias --file episode.mp3 --kind thread --no-wait --json | jq -r '.thread_id // .id')
# Poll for transcription, then review, remap, compile:
faces compile:thread:get "$THREAD_ID"
faces compile:thread:edit "$THREAD_ID" --face-speaker "A"
faces compile:thread:make "$THREAD_ID" --no-wait --json
```
Use `--kind document` for solo speakers.

**`--face-speaker` label rules:**
- Audio/video transcription: speakers are labeled `A`, `B`, `C` — use the short label (e.g. `--face-speaker B`)
- Text transcript uploads: the label matches the speaker name in the file (e.g. `--face-speaker Troy`)
- Match is case-insensitive but exact

**Verify speaker attribution (every thread, before `compile:thread:make`).**
An omitted or mismatched `--face-speaker`, fuzzy matching, or `A`/`B`/`C` labels
can all put the wrong person's lines on the face. Whether the source was text or
audio/video, run `compile:thread:get <thread_id>` and confirm:

1. **Roles are right** — the face's own speaker is `role=user`; everyone else
   (interviewer, host, other guests) is `role=assistant`.
2. **Spot-check, don't over-read** — check a few turns (first, middle, last) that
   the `user` turns are actually the subject speaking. For a large transcript you
   do not need to read every line; a smell-test is enough.
3. **Fix and re-check if wrong** — `faces compile:thread:edit <thread_id>
   --face-speaker …`, then `compile:thread:get` again. Only compile once the
   mapping checks out.

**Read-only (frozen) documents & threads.** Some items come back locked. A
`compile:doc:list`/`:get` or `compile:thread:list`/`:get` prints a bare `read
only` line when the item is frozen (nothing is printed when it's writable — there
is no `read_only: false`). Frozen items are fully readable and can still be
deleted, but any write — `compile:doc:edit`, `compile:thread:edit`,
`compile:thread:message`, etc. — is refused with:

```
Error (409): This document is read-only and cannot be edited.
```

(threads say `This corpus is read-only…`). Don't retry the write — surface that
the item is frozen. Today only style **corpus** uploads (`style:upload`) produce
locked threads; nothing locks individual documents. There is no per-item toggle for
these; to freeze or thaw a whole face, use `face:lock` / `face:unlock` (see
[references/REFERENCE.md](references/REFERENCE.md#face-locking)).

### 3. Capture how it writes (optional)

*Requires faces-cli 1.8.0 or newer.*

Compiling teaches a face **what it knows**. Style teaches it **how it sounds**. They are
separate acts and most faces only need the first. Capture style when the face is a real
person and you have their own writing — mail, messages, essays. First-person material only:
writing *about* someone teaches the wrong writer.

```bash
# Load a corpus. Stores only — nothing compiles, nothing is billed.
faces style:upload alias ./mail.jsonl

# Capture and install. --all takes every document and imported corpus room.
faces style:make alias --all --medium email --no-wait --json
faces style:status --face alias          # recover the job id if you lose it
```

**Always declare the medium.** Each is analysed separately, so an essay never teaches a
rule about email. A source that does not say what it is gets refused, not guessed:

```bash
faces style:make alias --all --medium email        # fills in ONLY where nothing is declared
faces style:make alias --source "$DOC_ID:essay"    # one source, one medium
```

`--medium` never overrides a source that already declares one; it only fills gaps, and a
source that already declares one is left to the server to resolve. An imported corpus room
whose messages declared nothing reads as `unknown`, which is not a medium and contributes
**no style** — correct it with `faces compile:thread:edit THREAD_ID --medium lecture`,
which sticks. A wrong declaration is
worse than a missing one — a mislabelled source teaches the wrong voice and nothing
afterwards says it happened.

**Quote `ID:MEDIUM` when the id is a shell variable.** In zsh `$DOC_ID:essay` is read as
a history modifier and silently becomes `ssay`. Use `"$DOC_ID:essay"`.

**Do not switch models to fix an auth failure.** The default model runs on the user's own
linked ChatGPT account for free; a billing model is refused rather than warned about. If a
capture fails on authentication the link has expired: `faces auth:connect openai`. Use
`--allow-paid` only when the user has said they want to pay.

A face holds one style **per medium**, so several can be in use at once and version
numbers restart per medium:

```bash
faces style:versions alias                      # REVERTABLE says whether revert will work
faces style:revert alias --medium essay --yes   # a toggle; run again to return
```

**Capturing does not apply it.** Prefix the alias with `+` to use the captured style;
without the `+` the face answers in its ordinary voice:

```bash
faces chat:chat +alias -m "..." --medium email
```

A `+` on a face with no style is a 409, not a fallback.

`--medium` picks WHICH captured style. A face holds one per medium, and `deepself` lists
the ones it has: `face:list --has-style` shows them (`[style: email, lecture]`).

A **plain alias accepts any medium** — declaring one replaces the classifier's guess and
nothing else. **`+alias` with a medium the face has no style for is a 400**, not a
fallback, so check `deepself` before offering the choice.

To see which faces already have one, without a call per face:

```bash
faces face:list --has-style          # marked [style] in the normal listing too
```

See [REFERENCE.md → Style](references/REFERENCE.md#style-how-a-face-writes-style).

### 4. Chat

```bash
faces chat:chat alias -m "message"
```

Auto-routes off the model catalog: `gpt-5.x`/codex → `/v1/responses` (free when a ChatGPT account is linked, else paid), `claude-*` → `/v1/messages`, `gpt-4o`/xai/venice/fireworks → `/v1/chat/completions`. Override the model with `--llm MODEL`. See [references/REFERENCE.md](references/REFERENCE.md#chat-auto-routing).
Subscription Connect users: add `--oauth-only` to prevent paid fallback.
In `--json` mode, response includes `_meta` with `provider`, `cost_usd`, and `endpoint`.
Reference other faces inline: `${other-alias}` → [references/TEMPLATES.md](references/TEMPLATES.md).

`chat:chat` is stateless (one turn, no memory). For a conversation the face remembers across turns, use `chat:thread` — history is stored locally and resumed by id (`--id`); set the model/system prompt once when starting. See [references/REFERENCE.md](references/REFERENCE.md#multi-turn-threads-chatthread).

**System & published faces:** every account can chat a curated set of faces served under the `head` account, using an `owner:alias@model` handle (the `@model` is **required**) — e.g. `faces chat:chat head:socrates@gpt-5.4 -m "…"`. List them with `faces face:list --system` (or `--public` for all published faces). A bare alias only ever resolves your own faces; you pay inference at normal rates, the owner is never charged. See [references/REFERENCE.md](references/REFERENCE.md#system--published-faces).

**Run-time composites:** pass a Face Math formula in the face position to chat with an on-the-fly blend of your own faces — `faces chat:chat "(alice | bob)@claude-sonnet-4-6" -m "…"` (or `--formula "alice | bob" --llm …`). No pre-creation step. See [§4 Compare & compose](#4-compare--compose).

### 5. Compare & compose

```bash
faces face:diff --face alice --face bob
faces face:neighbors alias --k 3                       # the 3 most SIMILAR faces (nearest, the default)
faces face:neighbors alias --k 3 --direction furthest # the 3 most DIFFERENT / unlike / opposite faces
faces face:create --alias new --formula "alice | bob"   # persist a composite
```

For "who is most **different / unlike / opposite**," add `--direction furthest`; the default (`nearest`) returns the most similar.

Operators: `|` union, `&` intersection, `-` difference, `^` symmetric diff.

**Compose on the fly — no need to persist.** You can chat with a composite of your own faces built per-request, by putting the formula in the face position. An explicit `@model` is **required** (a run-time composite has no `default_model`):

```bash
faces chat:chat "(alice | bob)@claude-sonnet-4-6" -m "What should we do?"
faces chat:chat --formula "alice | bob" --llm claude-sonnet-4-6 -m "What should we do?"
```

Same operators and merge semantics as a persisted composite (identical latency). A run-time composite **takes the name of its first operand** (`(alice | bob)` answers as *alice*); reach for `face:create --formula` when you want a reusable face with its own name. See [references/REFERENCE.md](references/REFERENCE.md#run-time-composite-faces).

### 6. Teams

Create named groups of faces with optional description, protocol (mermaid diagram), and tags:
```bash
# Create a team
TEAM=$(faces team:create --name "Review Panel" --description "Research critique" --tag review --json)
TEAM_ID=$(echo "$TEAM" | jq -r '.id')

# Add faces as members
faces team:add $TEAM_ID --face alice --face bob

# Set a protocol (mermaid workflow diagram)
faces team:edit $TEAM_ID --protocol-file workflow.mmd

# List teams, members
faces team:list
faces team:members $TEAM_ID
```

Teams have a local TEAM.md at `~/.faces/teams/<name>/TEAM.md` with YAML frontmatter (name, description, tags, members) and the protocol as the body.

### 7. Backup & restore

Snapshot all faces, teams, and source material for migration:
```bash
faces catalog:backup
# → ~/.faces/backups/2026-04-17T12-00-00-000Z.json
```

Restore from a backup (defaults to most recent):
```bash
faces catalog:restore                    # restore faces + source material
faces catalog:restore --compile          # restore then compile all
faces catalog:restore /path/to/file.json # specific backup file
```

Compile all outstanding (uncompiled) docs and threads:
```bash
faces compile:all
```

### 8. Account preferences

View or update server-side preferences:
```bash
faces account:preferences                            # show current
faces account:preferences default_model gpt-5.4      # set default model for new faces
faces account:preferences api_fallback true           # allow paid fallback when OAuth fails
```

## Important: never run `config:clear`

`faces config:clear` wipes all stored credentials (API key, JWT, base URL) with no recovery. Never use it to troubleshoot auth issues. If auth fails, check `faces config:show` and fix the specific value with `faces config:set`.

## Common errors

| Error | Fix |
|---|---|
| `faces: command not found` | `npm install -g faces-cli` |
| `401 Unauthorized` | `faces auth:login` or check `FACES_API_KEY` via `faces config:show` |
| status "transcribing" | Audio/video transcription in progress — poll with `compile:thread:get ID --json` |
| status "preparing" | Compilation in progress — poll with `compile:doc:get ID --json` or `compile:thread:get ID --json` |
| `402` insufficient credits | Check balance: `faces billing:balance --json`. Top up: `faces billing:topup --amount <USD>` (min $1). If no payment method on file: `faces billing:card-setup` first. See [BILLING.md](references/BILLING.md) |
| `422 oauth_rejected` | Subscription Connect only: OAuth request failed and paid fallback is disabled. Enable fallback: `faces account:preferences api_fallback true`. If no credits: `faces billing:topup` first. See [OAUTH.md](references/OAUTH.md) |
| `422` on thread import | Retry with `--type document` |
| `409` read-only on edit | The document/thread is frozen (`This document/corpus is read-only…`). Don't retry — surface that it's read-only. You can still read or delete it. Corpus-frozen items have no per-item toggle; a whole face freezes/thaws with `face:lock`/`face:unlock`. |
| Bad extraction results | Pause with `compile:thread:pause ID` or `compile:doc:pause ID` — pause is a request, so wait for `prepare_status: "paused"` before reading results (the CLI waits for you unless you pass `--no-wait`). Then either resume with `compile:*:make ID` or wipe and restart with `compile:*:reset ID` (keeps source content, removes extraction) |

## Related skills

- `/facemake` — Guided face creation (interview, research, sketch, compile)
- `/facechat` — Chat with any face in your catalog
- `/faceteam` — Compose faces into teams with collaboration protocols
- `/manyface` — Transform a skill into a multi-persona version

## Filesystem

```
~/.faces/
  config.json           # credentials, base_url, local settings
  catalog.json          # auto-generated index
  catalog/<alias>/      # individual FACE.md files
  backups/              # timestamped JSON backup snapshots (v2: faces + teams)
  teams/<team-name>/    # TEAM.md files
  skills/              # shared skills (facechat, etc.)
```

## FACE.md schema

CLI-managed fields (regenerated on sync via `catalog:doctor --fix`):
```yaml
---
name: Ada Lovelace
description: Mathematician and first computer programmer
alias: ada
default_model: gpt-5.4-mini
attributes:
  gender: female
  age: 34
  occupation: mathematician
tags: [research, mathematics]
formula: null
component_counts: 140
compiled_tokens: 47200
profile_token_count: 1024
---
```

Agent/user-managed fields (preserved by CLI, never overwritten): `role`, `source_type`, and any other keys not listed above. The markdown body after the frontmatter is always preserved.

All fields in FACE.md reflect the server state. The API returns `basic_facts` but the CLI renames it to `attributes` everywhere.

## TEAM.md schema

```yaml
---
id: 6c5f0e35-322b-4f25-af33-089e2a739b5c
name: Review Panel
description: Research critique panel
tags: [review, research]
members: [ada, einstein, skeptic]
---
```

The body after the frontmatter is the protocol (typically a mermaid diagram). Written by `team:create`, updated by `team:edit`/`team:add`/`team:remove`. Synced from server by `catalog:doctor --fix`.

## References

- [QUICKSTART.md](references/QUICKSTART.md) — First-time setup end-to-end
- [REFERENCE.md](references/REFERENCE.md) — Full CLI command reference
- [AUTH.md](references/AUTH.md) — Registration, login, API keys, plans
- [INTERVIEWS.md](references/INTERVIEWS.md) — Interview & conversation workflows
- [CONCEPTS.md](references/CONCEPTS.md) — What Faces is, cognitive primitives
- [USE_CASES.md](references/USE_CASES.md) — 14 example applications
- [TEMPLATES.md](references/TEMPLATES.md) — Face template syntax
- Accepted `--attr` keys → run `faces face:attributes`
- [OAUTH.md](references/OAUTH.md) — ChatGPT account linking
- [SCOPE.md](references/SCOPE.md) — Security boundaries
- [BILLING.md](references/BILLING.md) — Balance, top-ups, payment methods, cost reference
- [CONTRIBUTING.md](references/CONTRIBUTING.md) — File bug reports via `gh issue create`
