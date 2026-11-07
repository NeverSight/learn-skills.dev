---
name: design-prim
description: Dọn slop UI/UX khi onboard 1 dự án bất kỳ — quét view có sẵn, chụp playwright (before), để hallmark tự đọc project và REDESIGN thật (sinh design.md của riêng nó, không đóng khung theo token slop cũ), rồi vòng lặp sửa dựa trên slop-test 58 gate + `/impeccable audit`/`critique` + `/qc-uiux` (verdict senior 4-mục, engine tất định `visual-qa`) cho tới khi sạch hoặc hết ngân sách vòng. Gọi khi user nói "dọn slop", "làm gọn UI dự án", "chuẩn hoá UI xuyên suốt", "onboard rồi làm sạch UI", "design prim", "/design-prim".
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.0.0"
  loop: utils
---

# Skill: design-prim

`design` (khoá 1 hệ thiết kế xuyên suốt) + `prim` (chuẩn chỉnh, đúng chuẩn impeccable, không xộc xệch).

Nén 1 lần: `orca-onboard` (bỏ — quá nặng, hallmark tự quét token ở Step 0 rồi) + `playwright-verify` +
`impeccable` (bundle `doyourmagic/impeccable`) + `hallmark` (sàn design + slop-test) + `qc-uiux` (verdict
senior 4-mục, dùng engine tất định `visual-qa`). Không viết lại logic của các skill này — chỉ gọi
đúng thứ tự, đúng target.

**Bẫy đã trả giá — đọc trước khi chạy:** `/impeccable document` sinh `DESIGN.md` bằng cách **chụp lại
đúng token/màu/font ĐANG CÓ trong code** (nó tả thực trạng, không đề xuất gì mới). Nếu gọi lệnh này
trước rồi đưa `hallmark redesign` đọc, Hallmark Step 0 Pre-flight coi `DESIGN.md` là **hệ đã khoá,
override mọi thứ khác** — tức là khoá cứng lại chính bộ token slop cần dọn, rồi chỉ chỉnh vài chỗ vặt
bên trên. Đây là lý do bản trước của skill này "chạy xong mà trang không đẹp lên": nó tưởng đang khoá
1 hệ mới, nhưng thực ra khoá lại hệ cũ. **Đừng gọi `/impeccable document` trong luồng dọn slop.**

## WHAT

### Purpose và context
- **Purpose:** dọn slop UI/UX khi onboard một dự án bất kỳ — chụp before, để `hallmark redesign` sinh hệ thiết kế mới của riêng nó, rồi đo + vá theo slop-test, `/impeccable audit`/`critique`, `/qc-uiux` cho tới khi sạch hoặc hết 2 vòng.
- **Trigger (when to use):**
  - Vừa nhận 1 dự án lạ (onboard) và cần đưa UI về một chuẩn nhất quán, không lộ dấu AI-slop.
  - Đã có nhiều view/màn hình rời rạc, mỗi chỗ một kiểu, cần khoá lại một hệ.
  - User nói "dọn slop", "làm gọn UI dự án", "chuẩn hoá UI xuyên suốt", "onboard rồi làm sạch UI", "design prim", "/design-prim".
- **Non-goals:** KHÔNG dùng khi chỉ sửa 1 component nhỏ (dùng thẳng `hallmark` component-scope) hoặc khi cần hiểu sâu kiến trúc/business logic ngoài UI (đó là `orca-onboard` đầy đủ, không phải skill này). Không viết lại logic của các skill được gọi.

### Mental model
`impeccable đã cài? → view/route → ảnh before → PRODUCT.md (bối cảnh, KHÔNG token cũ) → hallmark redesign (design.md mới, bước DUY NHẤT sinh code) → 3 lớp đo (slop-test · impeccable audit/critique · qc-uiux) + ảnh after → vá theo bảng finding, tối đa 2 vòng → known limitation`.

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | dự án đích (root + router/pages) | có | nơi chạy mọi lệnh chat |
| In | app đang chạy tại `<base-url>` | có cho `/qc-uiux` và ảnh | như `playwright-verify` |
| In | `design.md`/`DESIGN.md` hợp lệ muốn GIỮ | không | chỉ khi user muốn giữ hệ cũ, nói rõ trong brief |
| Out | `PRODUCT.md` + `design.md` mới + code đã redesign | có | do `/impeccable init` và `hallmark` sinh |
| Out | ảnh before/after từng view + kết quả 3 lớp đo | có | bằng chứng "đẹp hơn", không phải điểm số suông |
| Out | báo cáo cuối | có | finding còn lại sau vòng 2 ghi là *known limitation* |

### Rules và capabilities
- RULE-01 (MUST): Thứ tự 0→6 không đảo: bước 4 là bước DUY NHẤT sinh/sửa code; bước 3 chỉ là bối cảnh, bước 5–6 chỉ đo
  và vá — nếu dừng ở bước 3 hoặc chỉ chạy bước 5 mà không tới bước 4/6 thì coi như CHƯA xong việc "làm
  đẹp", dù có báo cáo điểm số.
- RULE-02 (MUST): Bước 3–6 là lệnh **chat** (`/impeccable ...`, `hallmark` là skill), không phải shell — đừng gõ vào
  terminal.
- RULE-03 (MUST): Không tự thêm `orca-onboard` lại trừ khi user cần hiểu kiến trúc/business logic ngoài phạm vi UI.
- RULE-04 (MUST): Đã cài `impeccable` global rồi (không phải project) → gỡ/cài lại đúng scope trước khi chạy bước 3,
  tránh lẫn artifact của dự án khác (xem bẫy 2 trong `dym-impeccable-install-into-your-project`).
- Capabilities: đọc cấu trúc route của dự án đích; gọi skill UI khác qua chat (không shell); chạy trình duyệt headless để chụp/đo; ghi code UI dự án đích (chỉ ở bước redesign/vá).

### Failure boundaries
- Dừng ở bước 3 hoặc chỉ chạy bước 5 mà chưa tới bước 4/6 → **CHƯA xong** việc "làm đẹp", dù có điểm số (RULE-01).
- App không chạy được tại `<base-url>` → không chụp/không `/qc-uiux` được: **blocked**, báo user.
- Còn finding sau vòng 2 → **partial**, ghi *known limitation*, không lặp vô hạn.
- Lỡ chạy `/impeccable document` trước redesign → hệ slop cũ bị khoá lại: **failed**, bỏ `DESIGN.md` đó rồi redesign lại.

## HOW

### Main workflow
W01–W07 ứng với bước 0–6 bên dưới.

| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W01 | deterministic | root dự án đích | Kiểm `.claude/skills/impeccable/`; chưa có thì cài qua hub | impeccable sẵn sàng | có rồi → skip; cài global → B01 |
| W02 | deterministic | router/pages | Liệt kê view/route | danh sách view | — |
| W03 | effect | view + `<base-url>` | Chụp before bằng `playwright-verify` | ảnh before | app không chạy → blocked |
| W04 | judgment | chat dự án đích | `/impeccable init` → `PRODUCT.md` (KHÔNG `document`) | bối cảnh sản phẩm | — |
| W05 | effect | root + tóm tắt `PRODUCT.md` | `hallmark` verb `redesign` trên gốc dự án | `design.md` + code mới | muốn giữ hệ cũ → B02 |
| W06 | deterministic | view đã redesign | 3 lớp đo + chụp after | finding + ảnh after | còn P0/P1 / gate fail / CẦN SỬA → W07 |
| W07 | effect | finding | Vá theo bảng loại finding, rồi lặp W06 | sạch | sau vòng 2 → known limitation |

Chi tiết từng bước (nguồn chân lý cho W01–W07):

0. **Check điều kiện — đã cài `impeccable` trong dự án đích chưa?** Kiểm tra tồn tại
   `.claude/skills/impeccable/` ở root dự án đích (artifact của lượt install trước). **Có rồi → bỏ
   qua bước này**, đừng cài lại. **Chưa có → gọi** `/dym-impeccable install-into-your-project` (qua
   hub, để nó tự tìm bản đúng ở 1 trong 3 nơi — sibling `npx skills add`, bundle project, hoặc
   `.claude/skills/` — không hardcode path bundle của repo framework, vì dự án đích không chắc có nó).
   Bẫy cần nhớ khi làm theo file đó: luôn `npx impeccable install -y --scope=project
   --providers=claude`, đừng gõ `--help`.
1. **Liệt kê view/route** — Explore agent hoặc grep thẳng router/pages config của dự án đích. Không
   cần skill riêng, không cần `orca-onboard`.
2. **Chụp hiện trạng (before)** từng view bằng `playwright-verify` — giữ lại để so sánh ở bước 5.
3. **Bối cảnh sản phẩm (không phải token cũ)** — gõ trong chat của dự án đích: `/impeccable init` →
   sinh `PRODUCT.md` (người dùng, mục đích, ràng buộc, giọng điệu). Đây là input bù cho việc `hallmark
   redesign` (verb) im lặng, không hỏi audience/use-case/tone — dán tóm tắt `PRODUCT.md` vào brief khi
   gọi bước 4. **KHÔNG chạy `/impeccable document`** (xem bẫy ở trên).
4. **Redesign thật — đây là bước duy nhất sinh code mới.** Gọi skill `hallmark` với verb `redesign`
   trên GỐC dự án (đường dẫn thư mục route, không phải từng file lẻ) → rơi vào multi-page flow của
   hallmark: nó tự quét tokens/brand hiện có, tự chọn genre/macrostructure/theme, **tự viết
   `design.md` của riêng nó** ở root, rồi build lại từng page theo hệ đó. Nếu dự án đã có sẵn
   `design.md`/`DESIGN.md` hợp lệ (không phải bản `document` vừa cấm ở bước 3) và user muốn GIỮ hệ đó
   thay vì viết mới, nói rõ điều đó trong brief.
5. **Quét lại + so sánh** — trên từng view đã redesign, BA lớp (không lớp nào thay được lớp kia):
   a. `hallmark` tự chấm slop-test (six-axes pre-emit + 58 gate, đã chạy trong Build của bước 4).
   b. `/impeccable audit <view>` (P0–P3: a11y, perf, theming, responsive, anti-pattern) và
      `/impeccable critique <view>` (hierarchy, IA, cognitive load).
   c. `/qc-uiux <view>` (app phải đang chạy — `<base-url>` như `playwright-verify`) — verdict senior
      4-mục (accessibility · visual-hierarchy · consistency · antipattern), phần ĐO ĐƯỢC
      (contrast WCAG, tap-target, overlap/misalign hình học) chạy tất định qua engine `visual-qa`
      (đo rect thật, không đọc CSS tĩnh) → kết luận PASS hay CẦN SỬA.
   Chụp lại (after) bằng `playwright-verify`, đặt cạnh ảnh before bước 2 — đây là bằng chứng
   "đẹp hơn", không phải điểm số suông.
6. **Vòng lặp sửa** — còn finding P0/P1, gate slop-test fail, hoặc `/qc-uiux` kết luận CẦN SỬA → sửa
   bằng đúng lệnh, không quay lại redesign từ đầu:

   | Loại finding | Sửa bằng |
   |---|---|
   | a11y (contrast, tap-target, missing label) | `/impeccable harden <view>` |
   | performance (tải, render, animation) | `/impeccable optimize <view>` |
   | theming (lệch token giữa view) | `/impeccable polish <view>` — hoặc quay lại `hallmark audit <view>` nếu lệch cả hệ |
   | responsive (breakpoint, vùng chạm) | `/impeccable adapt <view> <context>` |
   | anti-pattern / cognitive load / IA rối | `/impeccable distill <view>` hoặc `clarify <view>` (copy) |
   | slop-test gate cụ thể fail | sửa trực tiếp theo gate đó trong `hallmark/references/slop-test.md`, không cần `/impeccable` |
   | `qc-uiux` visual-hierarchy/consistency (mắt LLM, không đo được) | `/impeccable distill`/`polish <view>` theo đúng mục — `qc-uiux` chỉ cho lỗi NẶNG NHẤT + cách sửa, không tự sửa |
   | `qc-uiux` a11y/antipattern ĐO ĐƯỢC (engine `visual-qa`: contrast/tap-target/overlap/misalign) | trùng dòng a11y/anti-pattern ở trên — cùng một lỗi, hai công cụ cùng bắt |

   Chạy lại bước 5 sau mỗi vòng sửa. **Tối đa 2 vòng.** Còn finding sau vòng 2 → ghi rõ trong báo cáo
   cuối là *known limitation*, không lặp vô hạn.

### Branches
| ID | Kind | Guard | Hành vi | Skip / failure | Rejoin |
|---|---|---|---|---|---|
| B01 | recovery | `impeccable` đã cài global (không phải project) | gỡ/cài lại đúng scope trước bước 3 (RULE-04) | — | W04 |
| B02 | user_optional | dự án có `design.md`/`DESIGN.md` hợp lệ (không phải bản `document`) và user muốn GIỮ | nói rõ trong brief redesign là giữ hệ đó | — | W06 |
| B03 | recovery | còn finding P0/P1, gate slop-test fail, hoặc `/qc-uiux` CẦN SỬA | vá theo bảng ở bước 6, chạy lại bước 5 | quá 2 vòng → known limitation | W06 |

### Validation và stopping
Ba lớp đo độc lập (slop-test 58 gate, `/impeccable audit`+`critique`, `/qc-uiux` với phần đo được qua engine `visual-qa`); không lớp nào thay lớp kia. Bằng chứng cuối là cặp ảnh before/after. Dừng khi sạch hoặc hết 2 vòng vá.

### Examples
- **Positive:** "/design-prim" trên dự án admin 6 route → impeccable đã có (skip bước 0) → ảnh before 6 view → `PRODUCT.md` → `hallmark redesign` ra `design.md` mới → vòng 1 `/qc-uiux` báo contrast fail ở 1 view → `/impeccable harden <view>` → vòng 2 PASS, báo cáo kèm ảnh before/after.
- **Boundary/failure:** agent gọi `/impeccable document` ở bước 3 rồi mới redesign → `design.md` khoá lại đúng token slop cũ, trang "chạy xong mà không đẹp lên" → vi phạm bẫy đã ghi, bỏ `DESIGN.md` đó và chạy lại từ bước 3 bằng `/impeccable init`.
