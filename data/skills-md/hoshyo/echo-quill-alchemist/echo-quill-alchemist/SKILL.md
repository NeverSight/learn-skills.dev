---
name: echo-quill-alchemist
description: Train a model on a novel, then continue writing in that novel's world — with memory of characters, places, and recent events. Load this skill whenever the user asks to train/fine-tune/learn the style of a novel or .txt, mentions Echo-Quill / Alchemist / 炼金 / 双塔, asks to open the training dashboard, asks how the system works, asks to stop or restart the training services, asks to write/continue text (with or without memory), asks to train an additional chapter or continuation they wrote, or asks to roll back to the original-novel state. The skill manages a local FastAPI backend + Vite/React dashboard, dependency installation, .env scaffolding, training, memory-mode continuation, pure-style continuation, and rollback — the user supplies a novel path or a passage, the skill handles everything underneath.
---

# Echo-Quill Alchemist — skill router

You are the natural-language entry point to the Echo-Quill Alchemist. The user has
two surface concepts:

1. **训练 (train)** — feed a `.txt` so the system learns the world (characters / places /
   events) and the style. Each training run produces a **bundle** under
   `core/data/corpora/{original,user}/<id>/`. Original-layer = the source novel.
   User-layer = a continuation the user wrote (or generated) and asked you to train.
2. **续写 (continue writing)** — two modes:
   - **memory mode** (`write.py`): knows the canon (characters / world / recent
     events) from all corpora. This is the default for any continuation request.
   - **pure-style mode** (`infer.py`): style only, no memory. Use when the user
     explicitly asks for "纯风格 / 无记忆" continuation.

Rolling back = filesystem move of bundles into `archive/`. Reversible.

The user does not understand internals (dual-tower, DPO, bge-m3, ROUGE-L).
They say "train this novel" or "续写一段". Translate to scripts. Don't lecture.

---

## The single rule that comes before everything else

**Always run `python scripts/doctor.py` first** for any echo-quill request. Its JSON
output is the ground truth. Don't guess. Don't trust state from earlier turns.

---

## Intent → action map

| User says (paraphrased)                                                  | What you do                                                                                                       |
|--------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| "train on `<novel.txt>`" / "用这本书炼金"                                | doctor → ensure deps + models + creds → start_services → open_dashboard → `train.py --path <...>` (defaults to `--layer original`) |
| "训练这一篇" / "train on this continuation" / "把刚才那篇收进来"         | `train.py --path <last_draft_or_user_text> --layer user`                                                          |
| "续写一段" / "continue this" / "write more"                              | doctor → start_services if down → `write.py --context "..."` (memory mode)                                        |
| "纯风格续写" / "无记忆续写" / "just the style, no canon"                 | `infer.py --context "..."` (legacy no-memory mode)                                                                |
| "重写 / 把 X 改成 Y / redo this" (right after a write)                   | `write.py --context "..." --redo "用户的修改要求"`                                                                |
| "回滚 / 只保留原著 / 删掉我训练的那些续写"                                | `rollback.py --to original`                                                                                       |
| "删掉刚训练的那篇 / 撤销那次 user 训练"                                   | `rollback.py --remove user/<id>` (run `rollback.py --list` first to find the id)                                 |
| "把档案里的那篇恢复回来 / 撤销刚才的 rollback"                            | `rollback.py --restore <archive_id>`                                                                              |
| "列一下训练过哪些 / show corpora"                                         | `rollback.py --list`  OR  `curl /corpora`                                                                         |
| "show me the dashboard"                                                  | doctor → start_services (if down) → open_dashboard                                                                |
| "how's training going?" / "status?"                                      | doctor + summarize backend `healthz`                                                                              |
| "stop / shut it down"                                                    | stop_services                                                                                                     |
| "explain how this works"                                                 | read `references/architecture.md` and summarize                                                                   |
| "something broke / errors"                                                | doctor → tail `core/data/logs/{backend,frontend}.log` → `references/troubleshooting.md`                          |

**After any rollback structural change, restart the backend** so its in-memory
caches refresh. Tell the user.

### Credential resolution

`doctor.py`'s `env.source` says where credentials come from:

| `env.source`    | Your action                                  |
|-----------------|----------------------------------------------|
| `claude_code` / `shell_env` / `.env` | **DO NOT ASK.** Proceed.       |
| `none`          | ASK user — activate CC Switch profile, or hand you a key (then `ensure_env.py --provider X --key Y`). |

---

## Rules of engagement

- **ASK before heavy installs.** Two distinct cost gates, both must be
  confirmed before the first training run; after that they're idempotent
  no-ops you can skip silently.
  - **pip deps** (~2 GB, mostly torch + sentence-transformers) — gated on
    `doctor.backend_deps.ok = false`. Runs `install_deps.py --backend`.
  - **model weights** (~2.4 GB total: MiniLM ~90 MB + bge-m3 ~2.3 GB) —
    gated on `doctor.models_cached.ok = false`. Runs `prefetch_models.py`.
    Do this BEFORE `start_services.py`, so the server bootstrap and the
    first canon-emitting chunk both hit a warm cache and never block a
    user-facing flow on a download.
  - **frontend npm install** (~30 s) — gated on `doctor.frontend_deps.ok = false`.
  Use AskUserQuestion. Never start silently.
- **ASK before spending API tokens.** A training run burns ~8 LLM calls/chunk
  (Best-of-N=4 + hard-neg + rule + canon + plot ≈ 8). On a 100-chunk novel
  that's ~800 calls. Memory-mode `write.py` is 1 LLM call/request. Confirm
  provider + model + scope before any large training run. Read provider
  from `doctor.py`'s `env` block — flag self-hosted relays.
- **The backend reads credentials only at startup.** If `.env` changes or the
  user switches CC Switch profile: `stop_services.py --backend` then
  `start_services.py --backend`.
- **Background services persist between turns.** `.echo-quill.state.json` at
  repo root holds PIDs. Always check `doctor.py` before spawning anything.
- **One training job at a time.** Don't kick off a second `train.py` while
  `healthz.queued > 0` or active. Ask the user to wait or cancel.
- **Translate technical errors.** Render the user-facing reason ("API key
  invalid", "novel not found", "port 8000 busy", "bge-m3 download stuck").
  Don't dump tracebacks unless explicitly asked.
- **Memory mode is the default for continuation.** Only fall back to
  `infer.py` if the user explicitly says "no memory" / "纯风格" / "ignore
  what was learned about characters".
- **Drafts are auto-archived to `core/data/drafts/<ts>.txt`.** When the user
  says "train that last continuation", use that path.

---

## Available scripts

| Script              | Purpose                                                                                  |
|---------------------|------------------------------------------------------------------------------------------|
| `doctor.py`         | JSON status — deps, env, services, data. Always run first.                               |
| `detect_provider.py`| JSON: which credential source resolves right now.                                        |
| `install_deps.py`   | `[--backend|--frontend]` — idempotent dep install.                                       |
| `prefetch_models.py`| `[--minilm|--bge-m3]` — idempotent HF model weight download (MiniLM + bge-m3).            |
| `ensure_env.py`     | Only call when `doctor.env.source = none`.                                               |
| `start_services.py` | `[--backend|--frontend|--no-wait]`.                                                      |
| `stop_services.py`  | `[--backend|--frontend]`.                                                                |
| `open_dashboard.py` | Open `http://localhost:5173`.                                                            |
| `train.py`          | `--path X.txt [--layer original|user --chunk_size N --ctx N --limit N --no-resume]`     |
| `write.py`          | `--context "..." [--redo "..." --top_canon N --top_plot N --scope CORPUS,CORPUS]` — **memory mode** |
| `infer.py`          | `--context "..." [--top_rules N --few_shot N]` — **pure-style no-memory mode**           |
| `rollback.py`       | `--list | --to original | --remove CORPUS_ID | --restore ARCHIVE_ID | --wipe-all --yes` |

Internal (do NOT call directly): `core/scripts/feeder.py` — wrapped by `train.py`.

---

## When to load reference docs

- `references/architecture.md` — when the user asks how it works, or you need
  to reason about non-obvious behavior (dual-tower, corpus layering, retrieval).
- `references/workflow-train.md` — before starting a real training run.
- `references/workflow-infer.md` — for continuation flows (memory + pure-style).
- `references/troubleshooting.md` — when `doctor.py` shows a problem.
