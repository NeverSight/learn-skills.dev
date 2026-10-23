---
name: build-now-adapt-later
description: When a task is blocked by missing or unverified information (an undocumented protocol, an unknown API shape, a value only real hardware/prod can confirm), build everything that does NOT depend on the unknown right now, and quarantine the unknown behind a single adapter boundary — best-guess defaults + a verified flag + a conformance/adapt kit — so adapting later means editing one file, not rewriting the project. Trigger when the user says "làm những gì có thể trước", "build what we can now", "wrap the unknowns", "isolate/quarantine the unknown parts", "don't block on missing info", "adapter so we can swap later", "ready to adapt", or invokes /build-now-adapt-later. Also applies whenever a spec has ⚠️ "to be verified" items but most of the work doesn't actually depend on them.
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.0.0"
  loop: dev-loop
---

# Skill: build-now-adapt-later

Ship the certain part now; isolate the uncertain part so it costs one file to finalize later.

## WHAT

### Purpose và context
- **Purpose:** khi task bị chặn bởi thông tin thiếu/chưa xác minh, build ngay mọi thứ KHÔNG phụ thuộc vào ẩn số và cách ly ẩn số sau MỘT adapter boundary, để adapt sau là sửa một file.
- **Trigger (when to use):** A task contains some facts you cannot pin down yet (undocumented byte layout, unconfirmed
  port/endian, an external API you can't call yet, a value only real hardware or production
  reveals) — BUT most of the work doesn't truly depend on those facts. Don't stall the whole
  project waiting, and don't scatter guessed values across the codebase. Draw one boundary.
- **Non-goals:** Do NOT use when the unknown is the whole task (e.g. "we don't know what to build"), or when
  the unknown is cheap to resolve right now (then just resolve it). Ngoài ra: không đoán rồi trình bày như đã xác minh; không trừu tượng hoá thứ đã chắc chắn "cho chắc" (over-engineering).

### Mental model
> Everything that depends on a stable **domain contract** is built and tested now.
> Everything that depends on an **unknown** lives behind one adapter, defaulted to a
> documented best-guess, flagged `verified:false`, and swappable in a single edit.

`unknowns (⚠️ + source-of-truth) → contract ổn định (không ⚠️) → quarantine (1 config + 1 adapter, verified:false) → core build đủ trên contract → mock cùng contract → Adapt-kit (checklist + conformance) → guard boundary`.

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | task + spec có mục ⚠️ "to be verified" | có | phần lớn việc không phụ thuộc ẩn số |
| In | tài liệu best-guess cho từng ẩn số | không | thiếu → default vẫn phải ghi nguồn + fail-safe |
| Out | contract (domain types/interface) | có | không chứa giá trị ⚠️ nào |
| Out | config + adapter quarantine | có | mọi ẩn số, `verified: false`, mỗi giá trị `ASSUMPTION` có nguồn |
| Out | core + mock chạy E2E hôm nay | có | build + test trên contract |
| Out | `ADAPT-CHECKLIST` + conformance tests/vectors | có | gate trước khi flip `verified:true` |
| Out | handoff | có | cái đã build+verify, cái đang đoán, đường một-file để chốt từng ⚠️ |

### Rules và capabilities
- RULE-01 (MUST): The adapter + its config are the ONLY places an unknown lives. Same guess in two files = a leak.
- RULE-02 (MUST): Every guess is flagged AND sourced. NEVER present a guess as verified, in code or in prose.
- RULE-03 (MUST): Default behavior under `verified:false` must be **fail-safe**, not optimistic — assume the guess
  is wrong until conformance proves otherwise (especially for anything physical, financial, or destructive).
- RULE-04 (MUST): Quarantine only what is genuinely unknown. Don't abstract certain things "just in case" — that's
  over-engineering, not isolation.
- RULE-05 (MUST): The contract is the deliverable downstream work depends on. Keep it stable; widen it deliberately,
  not per-guess.
- RULE-06 (MUST): State plainly in your handoff: what was built and verified, what is guessed and pending, and the
  one-file path to finalize each ⚠️.
- Capabilities: đọc spec/tài liệu sẵn có; ghi code dự án (contract, core, adapter, mock, test); không cần truy cập hardware/prod thật.

### Failure boundaries
- Ẩn số chính là toàn bộ task ("chưa biết build gì") → **không áp dụng** skill này, clarify với user.
- Ẩn số rẻ để giải ngay → tra luôn, không quarantine.
- Một giá trị đoán xuất hiện ở hai chỗ → isolation đã vỡ → **blocked** cho tới khi sửa (bước 7).
- Conformance chưa qua → giữ `verified:false`, hành vi mặc định fail-safe (**partial**, nói rõ trong handoff).

## HOW

### Main workflow
| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W01 | judgment | spec | Enumerate the unknowns, tag ⚠️ + source-of-truth | danh sách ẩn số | tra được rẻ → không phải ẩn số |
| W02 | judgment | ẩn số | Define the stable boundary (contract) | contract không ⚠️ | contract dính ⚠️ → làm lại |
| W03 | effect | ẩn số | Quarantine: 1 config + 1 adapter, best-guess + `verified: false` | config + adapter | — |
| W04 | effect | contract | Build everything above the boundary — fully | core đã test | import giá trị quarantine → sửa |
| W05 | effect | contract + adapter | Mock/stub cùng contract | E2E offline | — |
| W06 | effect | adapter | Ship the Adapt-kit: `ADAPT-CHECKLIST` + conformance | kit | — |
| W07 | deterministic | codebase | Guard the boundary (lint/review note) | không rò | rò → sửa trước khi đi tiếp |

Chi tiết từng bước (nguồn chân lý cho W01–W07):

1. **Enumerate the unknowns.** List every fact you don't have or can't verify. Tag each ⚠️ and
   note its source-of-truth (real hardware, prod data, a doc you lack, a stakeholder decision).
   If a "fact" can be looked up cheaply now — look it up; it's not an unknown.

2. **Define the stable boundary (the contract).** Write the domain-level interface that
   everything else speaks — types / function signatures / message schema that describe *intent*,
   not the unknown encoding. Rule: the contract must NOT contain any ⚠️ value. (e.g. a
   `SemanticCommand`/`Telemetry` model, not byte offsets; a `PaymentRequest`, not the gateway's
   wire format.)

3. **Quarantine the unknowns.** Put EVERY unknown-dependent constant in ONE config file and
   EVERY unknown-dependent logic in ONE adapter module behind the contract. Seed each with a
   best-guess default from whatever doc you have, mark each `// ASSUMPTION (source / not verified)`,
   and add an explicit `verified: false` flag. The adapter is the only thing that knows the unknown.

4. **Build everything above the boundary — fully.** UI, business logic, transport, safety/error
   handling, validation: all written against the contract, complete and tested. They never import
   a quarantined value.

5. **Build a mock/stub that speaks the same contract.** It lets the whole system run end-to-end
   *today* without the real unknown. Make the mock honor the same adapter/config so it doubles as
   the conformance harness later.

6. **Ship the Adapt-kit.** Produce (a) a short `ADAPT-CHECKLIST` — the exact steps to finalize once
   the unknown is known (edit config → edit adapter → run conformance → flip `verified:true`), and
   (b) conformance tests / vectors that must pass before the guessed values are trusted in
   production / against real hardware.

7. **Guard the boundary.** Add a lint rule or review note: quarantined values must not leak past
   the adapter. If a guessed constant appears in two places, the isolation is already broken — fix
   it before moving on.

### Branches
| ID | Kind | Guard | Hành vi | Skip / failure | Rejoin |
|---|---|---|---|---|---|
| B01 | recovery | W07 thấy một giá trị đoán ở hai chỗ | dời về adapter/config, xoá bản thứ hai | — | W07 |
| B02 | conditional_required | project có `llmwiki/` | viết draft report (mục Delivery) | không có `llmwiki/` → skip | kết thúc |

### Validation và stopping
Tất định: test core + mock E2E chạy xanh trên contract; conformance tests/vectors là cổng duy nhất để flip `verified:true`. Cần review: contract không chứa ⚠️, ranh giới không rò (lint rule hoặc review note). Dừng khi handoff liệt kê đủ built/verified vs guessed/pending.

### Examples
- **Positive:** lite3-controller-ui — protocol MotionSDK (command codes, byte offsets, endian, ports) chưa xác minh với hardware → contract `SemanticCommand`/`Telemetry`, quarantine `protocol.config` + `motionsdk-codec`, UI/WS/bridge/safety build đủ, UDP mock host cho E2E offline, Adapt-kit biến việc chốt protocol thành sửa một file.
- **Boundary/failure:** user nói "chưa biết app này làm gì, cứ build trước" → ẩn số là toàn bộ task → không áp dụng skill, hỏi làm rõ yêu cầu. Cổng thanh toán chưa rõ wire format, mặc định `verified:false` phải từ chối giao dịch thật (fail-safe), không giả định thành công.

### Reference — Quick template (adapt to the stack)
```
contract/         # stable domain types — NO unknown values        (built now, tested now)
  └ model.*       #   intent-level: commands, telemetry, requests
core/             # UI / logic / transport / safety on the contract (built now, tested now)
adapter/
  ├ config.*      # ⚠️ ALL unknown constants + verified:false       (quarantine)
  └ codec.*       # ⚠️ encode/decode against the unknown            (quarantine, swap 1 file)
mock/             # speaks the same adapter → E2E offline + conformance harness
ADAPT-CHECKLIST.* # 5-step finalize procedure when the unknown is known
conformance.*     # vectors that gate verified:true
```

### Reference — Worked example (where this was distilled from)
lite3-controller-ui: the MotionSDK protocol (command codes, byte offsets, endian, ports) was
unverified vs real hardware. The contract = `SemanticCommand`/`Telemetry`; the quarantine =
`protocol.config` + `motionsdk-codec`; UI/WS/bridge/safety built fully on the contract; a UDP
mock host gave full E2E offline; an Adapt-kit (checklist + conformance vectors) made finalizing
the protocol a one-file edit. See `llmwiki/wiki/draft/orca/150626-lite3-adapter-isolation.md`.

### Delivery — Output Report (only if the project has an `llmwiki/`)

After the work completes, write a draft report so the decision is traceable.

**1. Filename:** `llmwiki/wiki/draft/orca/DDMMYY-<ten>.md` — `DDMMYY` = today, `<ten>` = 2–4 kebab words.

**2. Write:**
```
---
type: draft
title: "DDMMYY-<ten>"
status: proposed
tags: [<skill-name>, output-report]
timestamp: YYYY-MM-DD
---

# DDMMYY-<ten>
**Type:** draft
**Status:** proposed
**Tags:** build-now-adapt-later, output-report
**Proposed:** YYYY-MM-DD

## What
<One sentence — what was built now vs what was quarantined>

## Boundary
- Contract: <the stable domain types/interface>
- Quarantine: <config + adapter files holding the ⚠️ unknowns>

## Unknowns (⚠️) pending verification
| Unknown | Best-guess source | Finalize by |
|---------|-------------------|-------------|

## Files
| File | Action |
|------|--------|

## Notes
- Invoked via: `/build-now-adapt-later` skill

## Origin
- **Draft:** `wiki/draft/orca/DDMMYY-<ten>.md`
- **Commit:** _(filled by verify-before-commit)_
- **Date promoted:** _(filled by verify-before-commit)_
```

**3.** Append a row to `llmwiki/wiki/index.md` and a line to `llmwiki/wiki/log.md`.
