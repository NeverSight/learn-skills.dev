---
name: council
disable-model-invocation: true
description: >-
  Run a Karpathy-style LLM council (3-stage multi-agent evaluation) on top of
  the existing orca orchestration: N seats independently answer a question, the
  answers are BLIND peer-ranked (identities stripped so a model can't favour its
  own), and a chairman synthesizes the final answer. The orchestration makes the
  model calls; harness/scripts/council.py does the deterministic protocol math
  (anonymization, mean-rank aggregation, dissent, anchor guard, transcript). Use
  when the user says "run a council", "llm-council", "panel of models", "blind
  peer-rank these answers", "ensemble + chairman", or invokes /council. Stage-4
  is a MANDATORY HTML report, rendered inside council.py itself (offline, no CDN,
  no external skill): every `rank` writes a NEW versioned self-contained report
  (llmwiki/html/council/council-report-NNN-seed<seed>.html) — opinion cards
  (persona name + lens), a blind-vote table, and a dashboard. Isolated in
  try/except so a render bug never kills the core transcript.
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.0.0"
  loop: orchestrate
  requires:
    harness: ">=1.3.127"
    bin: [orca, python3]
    scripts: [harness/scripts/council.py]
---

# Skill: council

> 🧭 Chọn backend cho mỗi seat (model rẻ vs Claude), chạy nhiều seat song song (1 worktree/seat — KHÔNG nhiều opencode/1 folder) → xem **orca-dispatch-reference** (nguồn chân lý duy nhất).

A deterministic harness around Andrej Karpathy's `llm-council`
(https://github.com/karpathy/llm-council) three stages — Stage 1 "First
Opinions", Stage 2 "Review" (anonymized peer-rank), Stage 3 "Final Response"
(chairman) — wired onto orca orchestration.

## WHAT

### Purpose và context
- **Purpose:** chạy một hội đồng LLM kiểu Karpathy 3 stage trên orca orchestration — N seat trả lời độc lập, chấm chéo MÙ (ẩn danh), chairman tổng hợp — kèm transcript tất định và report HTML bắt buộc (Stage 4).
- **Trigger (when to use):** Hard questions where one model's answer is risky and you want a panel + an audit trail of who-ranked-what, with the favour-your-own bias removed by blinding. For a single quick answer, just ask one model. Lời gọi: "run a council", "llm-council", "panel of models", "blind peer-rank these answers", "ensemble + chairman", hoặc `/council`.
- **Non-goals:** không dùng cho câu hỏi nhanh một đáp án; `council.py` không gọi model; không chọn model cho seat (việc của adapter `harness/council.config.yaml`); report không thêm phán xét mới ngoài transcript.

### Mental model
Split of labour:

- **`harness/scripts/council.py`** owns the DETERMINISTIC protocol and never
  calls a model: anonymize (strip author → A/B/C by stable sha256 order),
  mean-rank aggregation, dissent surfacing, the anchor guard (seed-driven,
  per-judge presentation order — no `Math.random`), and the json+md transcript.
- **The orca orchestration** owns the MODEL GENERATIONS: each seat's answer,
  each judge's ranking, the chairman's synthesis. It dispatches them exactly
  like any other multi-agent wave (see `orca-workflow`, `orchestration`).
- **`harness/council.config.yaml`** is the ONE adapter (`verified: false`): which
  model fills each seat, the judge models, the chairman. Every value is an
  `# ASSUMPTION (not verified)`. The engine never branches on these — it only
  stamps them into the transcript. Finalize the council by editing this one file.

`question → Stage 1 answers.json → Stage 2a blind packet (A/B/C + presentation order) → Stage 2b judges.json → Stage 2c transcript (mean-rank, dissent, chairman_brief) → Stage 3 chairman_synthesis → Stage 4 HTML report versioned`.

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | câu hỏi | có | cùng một câu cho mọi seat; `--question` để hiện trên report |
| In | `harness/council.config.yaml` | có | seats / judges / chairman (`verified: false`) |
| In | roster persona (`--case` / `--profile` / `--personas`) | không | lens góc nhìn thêm vào prompt Stage-1 |
| In | `--seed N` | không | seed anchor guard, ghi đè `anchor_seed` |
| Out | `answers.json` · `judges.json` | có | `[{"id","author","text"}]` · `[{"judge","ranking":[...]}]` |
| Out | `scratchpad/council-<slug>/council.packet.{json,md}` + `council.transcript.{json,md}` | có | blind packet; consensus, winner, dissent, `chairman_brief`, `chairman_synthesis` |
| Out | `llmwiki/html/council/council-report-NNN-seed<seed>.html` | có (bắt buộc) | report versioned, không ghi đè; `latest.html` con trỏ |

### Rules và capabilities
- RULE-01 (MUST): **NGÔN NGỮ (bắt buộc):** mọi seat/judge/chairman PHẢI trả lời bằng **tiếng Việt CÓ DẤU đầy đủ**; chèn câu này vào MỌI prompt Stage-1/Stage-2/Stage-3.
- RULE-02 (MUST): Output run luôn dưới `scratchpad/council-<slug>/` — never bare `run/` or a repo-root folder.
- RULE-03 (MUST): Blindness, not exclusion, is the guard — judge chỉ thấy nhãn A/B/C, theo presentation order của mình.
- RULE-04 (MUST): Roster luôn cài **≥1 cặp đối-trọng**; size lẻ (3/5) để mean-rank không hoà.
- RULE-05 (MUST): Stage-4 HTML luôn render; lỗi renderer chỉ WARN, KHÔNG bao giờ giết lệnh `rank` hay `transcript.{json,md}`.
- RULE-06 (MUST): `council.py` never calls a model; engine never branches on config values — chỉ stamp vào transcript.
- Capabilities: dispatch model generation qua lớp orchestration (seat/judge/chairman); tính toán protocol tất định cục bộ; ghi file transcript + HTML; không mạng/CDN cho report.

### Failure boundaries
- `council.py selftest` không exit 0, hoặc `orca status --json` không có runtime chạy → **blocked**, không chạy council.
- Seat trả lời không dấu → report cũng mất dấu (render trung thực) → nhắc lại RULE-01 và chạy lại seat đó.
- Thiếu judges → `rank` chỉ phát blind packet rồi dừng (**partial**, chờ Stage 2b).
- Renderer HTML lỗi → WARN, transcript vẫn có (**partial** cho Stage 4, chạy lại `render`).
- Roster thiếu cặp đối-trọng → cảnh báo stderr; gõ sai case/persona → gợi ý gần nhất, không fail trơ.

## HOW

### Main workflow
| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W01 | deterministic | repo, runtime | Preconditions: `council.py selftest`, `orca status --json`, config có seats/judges/chairman | đủ điều kiện | thiếu → blocked |
| W02 | effect | câu hỏi (+ lens) | Stage 1 — dispatch một worker mỗi seat, gom `answers.json` | `answers.json` | seat lỗi/không dấu → chạy lại seat |
| W03 | deterministic | `answers.json` | Stage 2a — `council.py prepare` | blind packet | — |
| W04 | effect | packet | Stage 2b — dispatch judge với câu trả lời mù theo presentation order, gom `judges.json` | `judges.json` | — |
| W05 | deterministic | answers + judges | Stage 2c — `council.py rank` (tự ghi Stage-4 HTML) | transcript + report | render lỗi → WARN, B02 |
| W06 | effect | `chairman_brief` | Stage 3 — dispatch chairman, dán `chairman_synthesis` vào transcript | transcript đủ | — |
| W07 | deterministic | transcript | Stage 4 — `council.py render <transcript.json>` để report có synthesis | report versioned mới | lỗi → WARN, transcript giữ nguyên |

Chi tiết từng bước (nguồn chân lý cho W01–W07):

#### Preconditions
- `python3 harness/scripts/council.py selftest` exits 0 (engine is healthy).
- `orca status --json` shows a running runtime; orchestration enabled.
- Seats/judges/chairman set in `harness/council.config.yaml`.

#### Protocol (maps each stage to an orca dispatch)
##### Stage 1 — First Opinions (orchestration generates)
Dispatch one worker per seat in `council.config.yaml`, same question to each.

> **NGÔN NGỮ (bắt buộc):** mọi seat/judge/chairman PHẢI trả lời bằng **tiếng Việt
> CÓ DẤU đầy đủ** (đúng chính tả, đủ dấu thanh + dấu mũ). TUYỆT ĐỐI không viết
> tiếng Việt không dấu (ASCII). `council.py` render trung thực text đầu vào
> (`ensure_ascii=False`, không normalize) — nếu seat trả lời mất dấu thì report
> cũng mất dấu. Chèn câu này vào MỌI prompt Stage-1/Stage-2/Stage-3.


```bash
orca orchestration task-create --spec "Answer: <question>" --json
orca orchestration dispatch --task <task_id> --to <seat_handle> --inject --json
orca orchestration check --wait --types worker_done --timeout-ms 300000 --json
```

Collect the replies into `answers.json` — `[{"id","author","text"}, ...]`, where
`author` is the seat id (the real identity; it gets stripped next).

##### Stage 2a — blind packet (council.py is deterministic)
```bash
python3 harness/scripts/council.py prepare answers.json --config harness/council.config.yaml --out scratchpad/council-<slug>/
```
`<slug>` = short name for this run (e.g. `release-gate`). Always under `scratchpad/`
(gitignored, per-repo convention) — never bare `run/` or a repo-root folder; those
leak as untracked clutter that never gets cleaned up (lesson 170726, 6 stray
`run-council*/` dirs found at repo root from past sessions copying this example
literally). Writes `scratchpad/council-<slug>/council.packet.{json,md}`: the
answers relabelled A/B/C with authors
removed, plus each judge's **presentation order** from the anchor guard. Show
each judge its answers in its row's order to cancel position bias.

##### Stage 2b — Review (orchestration generates)
Dispatch each judge in `council.config.yaml` the BLIND answers, in that judge's
presentation order. Ask each to return a ranking of the **labels** (best first).
Collect into `judges.json` — `[{"judge","ranking":["B","A","C"]}, ...]`.

> Blindness, not exclusion, is the guard: a judge may be a seat, but it cannot
> recognise its own answer, so it cannot play favourites.

##### Stage 2c — aggregate (council.py is deterministic)
```bash
python3 harness/scripts/council.py rank answers.json --judges judges.json --config harness/council.config.yaml --out scratchpad/council-<slug>/
```
Writes `scratchpad/council-<slug>/council.transcript.{json,md}`: mean-rank consensus, the winner, the
dissent table (most-contested answer), and a `chairman_brief`.

##### Stage 3 — Final Response (orchestration generates)
Dispatch the chairman the `chairman_brief` from the transcript (consensus order +
the dissent points it must resolve). Its synthesis is the final answer; paste it
back under `chairman_synthesis` in the transcript for the record, then
`council.py render <transcript.json>` to regenerate the Stage-4 HTML **with the
synthesis shown** (the report auto-written during `rank` has an empty synthesis
because `rank` rebuilds from answers+judges only).

##### Stage 4 — HTML report (MANDATORY, tự render trong council.py, offline)
**Luôn render — không cần cờ, không phụ thuộc skill ngoài.** Mỗi lần `rank` thành
công, `render_report_html(t, personas)` (nằm ngay trong `council.py`) ghi **một
`.html` versioned** — `llmwiki/html/council/council-report-NNN-seed<seed>.html`
(NNN tăng dần, KHÔNG ghi đè → mỗi run một bản ghi bất biến) + `latest.html` là con
trỏ tiện dụng (gitignore, tránh diff-churn). Không CDN (system font + inline SVG
favicon/grain) → offline; không coupling `docs-site-macos`. Feed **thuần** từ
transcript vừa build (`t`) → không bịa gì mới, mọi chuỗi seat `html.escape` tại chỗ
(chống HTML-injection). Toàn khối render bọc **try/except**: lỗi renderer chỉ WARN,
KHÔNG bao giờ giết lệnh `rank` hay `transcript.{json,md}` (Taleb blast-radius guard).
Tên+lăng kính ủy viên lấy từ `council.personas.yaml`; câu hỏi hiển thị khi truyền
`--question` (bỏ trống → report ẩn dòng question thay vì in placeholder).

Trang có đúng ba section, theo thứ tự:

1. **Ý kiến hội đồng.** Mỗi seat một card (viền màu = `sha256(author)`, xếp theo
   consensus rank + huy chương), answer tự format `(1)(2)(3)` thành list.
   *Nguồn:* `t["answers"]` + `t["aggregate"]`.
2. **Bỏ phiếu KÍN (blind vote).** Bảng phiếu dùng NHÃN A/B/C ẩn danh: mỗi judge
   một hàng, ranking theo nhãn + presentation-order của anchor guard. Reveal map
   A/B/C → author chỉ ở cuối section.
   *Nguồn:* `t["judge_rankings"]` + `t["anchor_guard"]`.
3. **Dashboard cuối.** KPI (winner / most-contested / đồng thuận) + bảng mean-rank
   consensus, và `chairman_synthesis` hiển thị nổi bật KHI đã được dán vào
   transcript (rank build lại từ answers+judges nên field này rỗng cho tới khi
   chairman fill — lúc đó khối synth tự ẩn).
   *Nguồn:* `t["winner"]` / `t["most_contested"]` / `t["aggregate"]`.

Vì mọi số liệu lấy từ transcript đã deterministic, report chỉ là lớp trình bày —
không thêm phán xét mới. Same transcript → cùng HTML.

### Branches
| ID | Kind | Guard | Hành vi | Skip / failure | Rejoin |
|---|---|---|---|---|---|
| B01 | user_optional | muốn đa dạng GÓC NHÌN (ít provider) | bốc roster persona (mục Persona lenses dưới), chèn lens vào prompt Stage-1 (động) hoặc field `persona:` trong config (cố định); roster + lý do ghi vào transcript | không bốc → seat = model thuần | W02 |
| B02 | recovery | report HTML lỗi hoặc cần hiện `chairman_synthesis` | chạy lại `council.py render <transcript.json>` → versioned file mới | renderer vẫn lỗi → WARN, transcript là nguồn | kết thúc |
| B03 | conditional_required | chạy `rank` không có `--judges` | chỉ phát blind packet rồi dừng | — | W04 |

### Validation và stopping
Tất định: `selftest` (12 checks) chứng minh cùng `answers.json` + `judges.json` + seed → transcript byte-identical; report chỉ là lớp trình bày của transcript. Cần review: chất lượng synthesis của chairman. Dừng sau W07 khi report có synthesis.

### Examples
- **Positive:** "run a council: có nên tách monorepo không" với `roster --case decision` 3 ghế → 3 seat trả lời tiếng Việt có dấu → `prepare` ra A/B/C → 3 judge rank → `rank --out scratchpad/council-monorepo/` ra winner + dissent → chairman tổng hợp → `render` ghi `council-report-NNN-seed<seed>.html` có synthesis.
- **Boundary/failure:** `council.py selftest` exit khác 0 → dừng ở W01, không dispatch seat nào. Renderer lỗi trong `rank` → chỉ WARN, `council.transcript.json` vẫn được ghi, chạy lại `render` sau.

### Reference — Persona lenses — góc nhìn "vĩ nhân" (optional, ADDITIVE)
Mặc định mỗi seat = một MODEL trả lời. Lớp persona thêm **đa-dạng GÓC NHÌN**: mỗi seat đội một
**lens** (Feynman / Munger / Taleb / Rams …) — quan trọng khi đa-dạng-model bị hạn chế (chỉ có ít
provider). Engine `council.py` KHÔNG đổi: persona chỉ là chữ nhét vào prompt Stage-1.

**Quên tên ai / cú pháp gì?** `council.py roster --list` (hoặc `roster` trống) in hết **case (theo VIỆC) · profile · 18 persona** — chọn `--case` theo việc, không cần nhớ tên.
**Nhớ nhầm vẫn gọi chính xác được:** khớp theo TÊN lẫn id, không phân biệt hoa/thường (`--personas Feynman,Taleb` ok); gõ sai → **gợi ý gần nhất** (`--case risks` → "ý bạn là 'risk'?"), không fail trơ.

**Bốc 3-5 người theo case (thuần code, log-được):**
```bash
python3 harness/scripts/council.py roster --list                 # catalog: case/profile/persona
python3 harness/scripts/council.py roster --case risk            # 3 ghế, có ≥1 cặp đối-trọng
python3 harness/scripts/council.py roster --case ml-ai --size 5  # 5 ghế
python3 harness/scripts/council.py roster --profile lean         # 5 người execution-lean
python3 harness/scripts/council.py roster --personas feynman,taleb,rams --json
```
- Case tag: `design · strategy · debug · risk · product · decision · simplify · ml-ai` (bảng trong `harness/council.personas.yaml`).
- **Luật:** roster luôn cài **≥1 cặp đối-trọng** (chống phòng vọng âm); thiếu → cảnh báo ở stderr. Size lẻ (3/5) để mean-rank không hoà.
- Thư viện: 18 persona + 13 cặp đối-trọng (nguồn `github.com/0xNyk/council-of-high-intelligence`).

**Dùng trong protocol:** sau khi bốc roster, gán mỗi persona vào một seat — có 2 cách:
1. **Động (khuyên):** orchestrator lấy output `roster --json`, với mỗi seat chèn lens vào prompt Stage-1: *"Trả lời qua lăng kính \<name>: \<lens>. \<sig>."*
2. **Cố định:** điền field `persona:` mỗi seat trong `harness/council.config.yaml`.

Roster + lý do bốc (case, cặp tension) **ghi vào transcript** để auditable (Trụ 5). Phần "model nào fill seat" vẫn là unknown đã quarantine ở `council.config.yaml` (`verified`) — persona-lens độc lập với nó.

### Reference — council.py commands
| Command | Does |
|---------|------|
| `rank <answers.json> --judges <judges.json>` | full aggregation → transcript.json + .md |
| `rank <answers.json> --judges <j>` | + auto-writes versioned `llmwiki/html/council/council-report-NNN-seed<seed>.html` (Stage-4, mandatory) |
| `rank <answers.json>` (no judges) | emits the blind packet, then stops |
| `prepare <answers.json>` | blind packet only (Stage 2a) |
| `render <transcript.json>` | re-render Stage-4 HTML từ transcript đã có (vd sau khi dán `chairman_synthesis`) → versioned file mới |
| `roster --case <tag>` / `--profile <p>` / `--personas a,b,c` | bốc 3-5 persona-lens (thuần lookup, ≥1 cặp đối-trọng); `--size 3\|5`, `--json` |
| `selftest` | conformance vectors; asserts determinism + correctness |

Flags: `--seed N` (anchor-guard seed; overrides config `anchor_seed`),
`--out DIR` (transcript json/md), `--config harness/council.config.yaml`,
`--question "..."` (câu hỏi thật hiện trên report; bỏ trống → ẩn dòng question).
Stage-4 HTML versioned luôn ghi vào `llmwiki/html/council/` — no flag needed.

### Reference — Adapter boundary (build-now-adapt-later)
- **Contract (built + tested now):** the json schemas (`answers.json`,
  `judges.json`, transcript) and all the deterministic ops in `council.py`.
- **Quarantine (`verified: false`):** model identities in
  `harness/council.config.yaml`. The math is independent of them.
- **Adapt later (one file):** edit seats/judges/chairman in the config, run a
  real council, then flip `verified: true`. No engine change.

### Reference — Determinism guarantees
Same `answers.json` + `judges.json` + seed → byte-identical transcript every
run. Anonymization depends on `sha256(id)`, not input order or author, so neither
position nor authorship leaks. The anchor guard is seeded per judge from the
arg — never the global RNG. `selftest` proves all of this (12 checks).
