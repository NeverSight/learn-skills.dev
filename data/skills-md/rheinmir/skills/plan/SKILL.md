---
name: plan
description: >-
  Mở rộng một draft SPEC ĐÃ ĐƯỢC DUYỆT thành kế hoạch thi hành được — file `DDMMYY-<tên>-PLAN.md`
  mà một agent KHÔNG có context nào (CLI rẻ chạy headless, không hỏi lại được) vẫn làm đúng:
  đường dẫn file chính xác, khối Interfaces (Consumes/Produces) khai chữ ký cho task hàng xóm,
  ràng buộc bao trùm chép nguyên văn, và từng bước 2-5 phút kiểu TDD có code thật + lệnh chạy +
  output mong đợi. Gọi SAU `/propose` và SAU khi user duyệt ở cổng, TRƯỚC khi dispatch task cho agent.
  Trigger - "viết plan", "mở rộng proposal thành plan", "plan thi hành", "chuẩn bị brief cho agent",
  "/plan". KHÔNG dùng để thiết kế hay để hỏi yêu cầu (đó là `/propose`), KHÔNG dùng khi chưa có SPEC duyệt.
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.0.0"
  loop: dev-loop
---

# Skill: plan

## WHAT

### Purpose và context
- **Purpose:** Biến SPEC đã duyệt thành văn bản mà **một kỹ sư giỏi nhưng không biết gì về codebase này, và gu thì đáng ngờ** vẫn thi hành đúng. Trong overstack, "kỹ sư" đó thường là một CLI rẻ chạy headless (`opencode` / `agy` / `kiro`): nó **không thừa hưởng context nào** của phiên chính, **không hỏi lại được**, và khi gặp chỗ mơ hồ nó sẽ **đoán rồi im lặng**. Thực đo bài học 250626: brief mỏng → giao hàng ~1/5.
- **Trigger (when to use):**
  - SPEC (`/propose`) đã được user duyệt ở cổng, và sắp dispatch task cho agent.
  - Việc nhiều bước, nhiều file, hoặc chia cho ≥2 agent chạy song song.
- **Non-goals:** KHÔNG dùng khi chưa có SPEC duyệt (dùng `/propose` trước), và không dùng cho sửa một dòng. Không dùng để thiết kế hay để hỏi yêu cầu (đó là `/propose`).

### Mental model
Cái gì không nằm trong PLAN thì agent không có. Đó là toàn bộ nguyên lý của skill này.

`SPEC đã duyệt (FR-xxx, Global constraints) → scope check → File structure → task tracer bullet (hoặc expand → migrate → contract) → mỗi task: Thoả + Files + Interfaces + Depends + Verify + Steps TDD → self-review → DDMMYY-<tên>-PLAN.md → orca orchestration task-create/dispatch --inject nguyên văn`.

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | SPEC đã duyệt `llmwiki/wiki/sources/draft/DDMMYY-<tên>.md` | có | lấy nguyên `## Context`, `## Global constraints`, `## Plan`, `## Agent Task Assignment` |
| Out | `llmwiki/wiki/sources/draft/DDMMYY-<tên>-PLAN.md` | có | đúng khuôn PLAN: frontmatter + `## Origin` + Global constraints nguyên văn + File structure + các `### Task N` |
| Out | dòng `wiki/index.md` + append `wiki/log.md` | có | theo bước 7 |
| Out | báo cáo chỗ vỡ SPEC | khi Cổng ngược kích hoạt | gom một lần, mỗi chỗ kèm câu SPEC gây ra |

### Rules và capabilities
- RULE-01 (MUST): PLAN **không cần** file `.html` — nó là thứ máy đọc. HTML gắn với SPEC (thứ người xem lúc duyệt), do `/propose` sinh. R7 miễn check diagram cho nhánh `-PLAN.md`.
- RULE-02 (MUST): Đường dẫn file **luôn chính xác**, kèm dải dòng khi sửa file có sẵn.
- RULE-03 (MUST): Bước đổi code thì **phải có code đầy đủ** — không mô tả suông.
- RULE-04 (MUST): Lệnh chạy **chính xác**, kèm **output mong đợi** (agent cần biết thế nào là fail đúng, thế nào là pass).
- RULE-05 (MUST): DRY, YAGNI, TDD, commit thường xuyên.
- RULE-06 (MUST): Trong codebase có sẵn: theo pattern đang có. Đừng nhân tiện refactor thứ ngoài task.
- Capabilities: đọc SPEC + codebase để khai đường dẫn/chữ ký thật; ghi file PLAN + index + log trong wiki; không dispatch khi chưa xong self-review.

### Failure boundaries
- Chưa có SPEC duyệt → **cancelled**, chuyển `/propose`.
- Cổng ngược (yêu cầu không quy được về task, mâu thuẫn, phương án bất khả thi, phải bịa hàm/kiểu/file) → **blocked**: DỪNG, không viết PLAN nửa vời, gom mọi chỗ vỡ báo một lần, quay về `/propose` duyệt lại.
- Còn placeholder hoặc `FR-xxx` không task nào nhận → **failed** (R7/R18 chặn), sửa tại chỗ.
- Sửa một dòng → không dùng skill.

## HOW

### Main workflow
| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W01 | deterministic | SPEC | Đọc SPEC đã duyệt, lấy nguyên các mục | nội dung SPEC | không có SPEC duyệt → dừng, `/propose` |
| W02 | judgment | SPEC | Scope check | một hoặc nhiều PLAN | nhiều hệ con → tách |
| W03 | judgment | SPEC + codebase | Vẽ `## File structure` trước khi chia task | danh sách file + trách nhiệm | file/API không tồn tại → B01 |
| W04 | judgment | File structure | Chia task tracer bullet (hoặc wide refactor) | danh sách task | WIDE REFACTOR → B02 |
| W05 | judgment | task | Viết từng task theo khuôn (đủ Files + Interfaces + Steps) | các `### Task N` | phải bịa hàm/kiểu → B01 |
| W06 | judgment | PLAN nháp | Self-review 3 mắt lưới, sửa tại chỗ | PLAN sạch | — |
| W07 | effect | PLAN | Ghi file + index + log | `DDMMYY-<tên>-PLAN.md` | R7/R18 chặn → sửa, ghi lại |
| W08 | effect | PLAN | Bàn giao: `task-create` + `dispatch --inject` nguyên văn kèm Global constraints | task đã dispatch | — |

Chi tiết từng bước (nguồn chân lý cho W01–W08):

1. **Đọc SPEC đã duyệt** — `llmwiki/wiki/sources/draft/DDMMYY-<tên>.md`. Lấy nguyên: `## Context`, `## Global constraints`, `## Plan` (các dòng `- [ ]`), `## Agent Task Assignment`.
2. **Scope check** — SPEC ôm nhiều hệ con độc lập → tách thành nhiều PLAN, mỗi PLAN tự nó ra được phần mềm chạy được và test được. Đừng nhồi.
3. **Vẽ `## File structure` trước khi chia task** — liệt kê mọi file sẽ tạo/sửa và trách nhiệm của từng file (một file một trách nhiệm; file nào đổi cùng nhau thì ở cùng chỗ). Quyết định phân rã bị chốt ở đây, không phải trong lúc code.
4. **Chia task thành TRACER BULLET** — mỗi task là một **lát cắt DỌC**: một lát mỏng xuyên hết các tầng (data → logic → giao diện/CLI), tự nó chạy được và tự chứng minh được, để lại một deliverable test được độc lập. Không phải "lát ngang" kiểu "làm hết tầng data" rồi task sau "làm hết tầng logic" — lát ngang không cái nào chạy được một mình. Setup, config, scaffolding, docs → gộp vào task cần chúng; chỉ tách khi một reviewer có thể *bác task này mà vẫn duyệt task kia*.

   **Ngoại lệ có tên — WIDE REFACTOR (expand → migrate → contract).** Một thay đổi cơ học mà **blast radius** trải khắp codebase — đổi tên một cột, đổi kiểu một symbol dùng chung — thì không lát cắt dọc nào xanh nổi: một chỗ sửa làm hàng nghìn call-site đỏ cùng lúc. Đừng ép nó vào khuôn tracer bullet. Sequence:
   - **expand** — thêm dạng MỚI cạnh dạng cũ, chưa xoá gì. Một task. Không làm hỏng gì vì dạng cũ vẫn còn.
   - **migrate theo lô** — dời call-site sang dạng mới, chia lô theo blast radius (per-package, per-directory). Mỗi lô một task, **bị chặn bởi** task expand. CI xanh từng lô vì dạng cũ vẫn sống.
   - **contract** — xoá dạng cũ khi không còn caller nào. Một task, **bị chặn bởi mọi lô migrate**.
   - Khi ngay cả từng lô cũng không tự xanh nổi: cho chúng chung một nhánh tích hợp, tất cả cùng chặn một task "integrate-and-verify" cuối — xanh chỉ được hứa ở đó.
5. **Viết từng task theo khuôn dưới** (bắt buộc đủ Files + Interfaces + Steps).
6. **Self-review** (3 mắt lưới, mục 'Self-review' bên dưới), sửa tại chỗ.
7. **Ghi file** `llmwiki/wiki/sources/draft/DDMMYY-<tên>-PLAN.md`, thêm dòng vào `llmwiki/wiki/index.md`, append `llmwiki/wiki/log.md`.
8. Bàn giao: mỗi `### Task N` là một `orca orchestration task-create`; `dispatch --inject` bơm **nguyên văn** brief của task đó **kèm `## Global constraints`**. Không tóm tắt lại — tóm tắt là chỗ context rụng.

### Branches
| ID | Kind | Guard | Hành vi | Skip / failure | Rejoin |
|---|---|---|---|---|---|
| B01 | recovery | Cổng ngược: một điều kiện DỪNG trong mục Cổng ngược xảy ra | DỪNG, gom TẤT CẢ chỗ vỡ thành MỘT lần báo, quay về `/propose` sửa SPEC + duyệt lại | — | W01 (sau khi SPEC duyệt lại) |
| B02 | conditional_required | thay đổi cơ học blast radius khắp codebase | WIDE REFACTOR: task expand → các lô migrate (chặn bởi expand) → contract (chặn bởi mọi lô); lô không tự xanh → nhánh tích hợp + task integrate-and-verify | — | W05 |
| B03 | conditional_required | SPEC ôm nhiều hệ con độc lập | tách nhiều PLAN, mỗi PLAN tự chạy được + test được | — | W03 cho từng PLAN |

### Validation và stopping
Tất định: R7 chặn placeholder (write-time + commit), R18 chặn `FR-xxx` không task nào nhận, R9/R2 chặn thiếu frontmatter/`## Origin`; dòng `**Verify:**` mỗi task là lệnh rc 0. Cần review: Self-review 3 mắt lưới (phủ SPEC, placeholder, nhất quán kiểu/tên). Dừng sau W08, hoặc ngay tại B01.

### Examples
- **Positive:** SPEC `DDMMYY-export-csv.md` đã duyệt có FR-001..FR-003 → PLAN 3 task tracer bullet, mỗi task có `**Thoả:**`, `**Files:**` đường dẫn chính xác, `**Interfaces:**` Consumes/Produces, dòng Verify là `pytest tests/test_export.py -q`, Step 1–5 TDD → ghi `DDMMYY-export-csv-PLAN.md` + index + log → dispatch từng task nguyên văn kèm Global constraints.
- **Boundary/failure:** khi khai File structure mới phát hiện API mà `## Approaches` chọn không tồn tại, và FR-002 mâu thuẫn Global constraints → DỪNG, không viết PLAN nửa vời, báo một lần cả hai chỗ kèm câu SPEC gây ra, quay về `/propose` duyệt lại.

### Reference — Khuôn PLAN
Header bắt buộc (frontmatter và `## Origin` KHÔNG được bỏ — file nằm trong `wiki/sources/draft/` nên R9 chặn nếu thiếu frontmatter, R2 chặn nếu thiếu `## Origin`):

```markdown
---
type: draft
title: <tên>-PLAN
status: proposed
timestamp: YYYY-MM-DD
task: T-YYMMDD-NN        # cùng task-id với SPEC
---

# <Tên> — PLAN thi hành

**Goal:** <một câu: cái này xây ra cái gì>
**Architecture:** <2-3 câu: cách tiếp cận>
**Tech stack:** <ngôn ngữ, lib, test runner, version>
**SPEC nguồn:** `wiki/sources/draft/DDMMYY-<tên>.md` (đã duyệt <ngày>)

## Origin
- **SPEC:** `wiki/sources/draft/DDMMYY-<tên>.md`
- **Commit:** _(verify-before-commit điền)_

## Global constraints
<chép NGUYÊN VĂN từ SPEC — sàn version, giới hạn dependency, luật đặt tên, gate trước push.
 Mỗi task ngầm mang theo section này.>

## File structure
- Tạo `path/chính/xác.py` — <trách nhiệm duy nhất của file>
- Sửa `path/có/sẵn.py` — <đổi gì>
```

Mỗi task:

````markdown
### Task N: <tên>

**Thoả:** FR-001, FR-003

**Files:**
- Tạo: `đường/dẫn/chính/xác.py`
- Sửa: `đường/dẫn/có/sẵn.py:123-145`
- Test: `tests/đường/dẫn/test_x.py`

**Interfaces:**
- Consumes: <dùng gì từ task trước — chữ ký chính xác>
- Produces: <task sau dựa vào cái gì — tên hàm, kiểu tham số, kiểu trả về>

**Depends:** Task 1, Task 3   <!-- task nào phải DONE trước; không có → ghi `—`. `/orca-graph build` đọc dòng này để dựng đồ thị phụ thuộc; thiếu thì nó SUY từ Consumes/Produces và gắn nhãn gợi-ý -->
**Verify:** `pytest tests/x.py -q`   <!-- lệnh rc 0 = task xong thật; thiếu → node chỉ đạt done_unverified -->

- [ ] **Step 1: viết test fail**

```python
def test_hanh_vi_cu_the():
    assert ham(dau_vao) == ket_qua_mong_doi
```

- [ ] **Step 2: chạy cho THẤY nó fail**

Chạy: `pytest tests/đường/dẫn/test_x.py::test_hanh_vi_cu_the -v`
Mong đợi: FAIL — `NameError: name 'ham' is not defined`

- [ ] **Step 3: code tối thiểu cho pass**

```python
def ham(dau_vao):
    return ket_qua_mong_doi
```

- [ ] **Step 4: chạy lại — PASS**

Chạy: `pytest tests/đường/dẫn/test_x.py::test_hanh_vi_cu_the -v`
Mong đợi: PASS

- [ ] **Step 5: commit**

```bash
git add tests/đường/dẫn/test_x.py src/đường/dẫn/x.py
git commit -m "feat: <việc cụ thể>"
```
````

**Vì sao `**Thoả:**` là bắt buộc:** SPEC đánh id ổn định `FR-001`, `FR-002`… cho từng yêu cầu. Mỗi task khai mình gánh id nào → câu "phủ hết SPEC" ở Self-review thôi làm bằng mắt, nó thành **dữ liệu grep được**, và **R18 chặn** nếu có `FR-xxx` nào không task nào nhận (in ra đúng id bị bỏ rơi). Một yêu cầu trôi mất giữa hai task là lỗi thầm lặng nhất của mọi kế hoạch — nó chỉ lộ ra lúc agent giao hàng thiếu, hoặc tệ hơn, lúc user dùng.

**Vì sao `Interfaces` là bắt buộc khi có ≥2 agent:** agent thi hành **chỉ nhìn thấy task của chính nó**. Không khai chữ ký thì hai agent song song đặt tên hàm lệch nhau và phần ghép vỡ — đây là lỗi *chắc chắn* xảy ra, không phải rủi ro.

### Reference — Cấm placeholder — đây là plan HỎNG, không phải plan chưa xong
R7 chặn ở write-time và commit. Không bao giờ viết:
- `TBD`, `TODO`, "điền sau", "chi tiết sau"
- "xử lý lỗi phù hợp" / "thêm validation" / "handle edge cases" — nói *làm gì*, không nói "làm cho phù hợp"
- "viết test cho phần trên" mà không có code test thật
- **"tương tự Task N"** — chép lại code ra. Agent có thể đọc task không theo thứ tự, và mỗi agent chỉ được bơm task của nó.
- Bước mô tả *phải làm gì* mà không chỉ *làm thế nào* (bước đổi code thì bắt buộc có code)
- Nhắc tới hàm/kiểu/method không được định nghĩa ở bất kỳ task nào

### Reference — Self-review
Viết xong, soi lại bằng mắt mới — sửa tại chỗ, không cần vòng hai:
1. **Phủ SPEC** — lướt từng yêu cầu trong SPEC, chỉ ra được task nào thực hiện nó. Thiếu → thêm task.
2. **Quét placeholder** — dò đúng các mẫu ở mục trên.
3. **Nhất quán kiểu/tên** — tên hàm, chữ ký, tên field dùng ở task sau có khớp cái định nghĩa ở task trước không? `clearLayers()` ở Task 3 mà `clearFullLayers()` ở Task 7 là một con bug.

### Reference — Cổng ngược — `/plan` được quyền BÁC SPEC
Viết PLAN chính là cách phát hiện SPEC sai: tới lúc phải khai đường dẫn file thật và chữ ký hàm thật thì thiết kế bất khả thi mới lòi ra. Nếu cổng duyệt đã cho qua rồi mà giờ mới lòi, nghĩa là user đã duyệt một thứ không xây được — cổng đã hỏng.

**DỪNG, không viết tiếp PLAN nửa vời**, khi gặp bất kỳ điều nào:
- Một yêu cầu trong SPEC không quy được về task nào làm được.
- Hai mục trong SPEC mâu thuẫn nhau, hoặc mâu thuẫn với `## Global constraints`.
- Phương án đã chọn ở `## Approaches` hoá ra bất khả thi (file không tồn tại, API không có, ràng buộc chặn).
- Phải bịa một hàm/kiểu/file mà SPEC không hề nhắc, để cho plan "chạy được trên giấy".

Xử lý: **gom TẤT CẢ chỗ vỡ thành MỘT lần báo** (không ngắt user từng phát một), mỗi chỗ kèm đúng câu trong SPEC gây ra nó, rồi quay về `/propose` sửa SPEC và **duyệt lại**. Một PLAN viết trên nền SPEC hỏng còn tệ hơn không có PLAN: nó bơm cái sai vào agent với vẻ mặt tự tin, và agent rẻ sẽ thi hành nguyên xi.
