---
name: timeline
description: Component timeline dọc (mốc theo ngày, cuộn-hiện dần bằng IntersectionObserver, tự chuyển layout mobile→desktop ở 768px) cho trang changelog/lịch sử/roadmap/writing-archive. Gọi khi user nói "làm timeline", "dòng thời gian", "lịch sử phiên bản dạng timeline", "changelog timeline", "roadmap timeline", hoặc /timeline. KHÁC /diagram (sơ đồ luồng/kiến trúc) — đây là danh sách MỐC THEO THỜI GIAN của MỘT trục, không phải quan hệ nhiều node.
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.0.0"
  loop: utils
---

# Skill: timeline

Component HTML/CSS/JS thuần (không framework) — danh sách mốc dọc, mỗi mốc có ngày + tiêu đề + nguồn, cuộn tới đâu hiện tới đó.

## WHAT

### Purpose và context
- **Purpose:** đưa vào trang đích một timeline dọc MỘT trục thời gian (mốc ngày + tiêu đề + nguồn), cuộn-hiện dần, responsive mobile→desktop ở 768px, dữ liệu thật.
- **Trigger (when to use):**
  - Trang cần liệt kê MỐC THEO THỜI GIAN: changelog, lịch sử dự án, roadmap, writing archive, timeline sự kiện.
  - User nói "làm timeline", "dòng thời gian", "lịch sử dạng timeline".
- **Non-goals:** KHÔNG dùng cho sơ đồ quan hệ/luồng (đó là `/diagram`) hay biểu đồ dữ liệu số (đó là `dataviz`) — đây chỉ là MỘT trục thời gian tuyến tính.

### Mental model
`dữ liệu mốc thật (API/markdown/CMS) → <li class="timeline__item"> (time + a + small) → IntersectionObserver gắn timeline__item--in → CSS transition hiện dần`. Asset mẫu là điểm xuất phát để ADAPT, không phải bản copy.

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | trang đích | có | nơi gắn timeline |
| In | dữ liệu mốc thật | có | ngày (ISO) + tiêu đề + link + nguồn; thiếu thì chưa wire được (chỉ có demo faker) |
| In | `design.md` / token dark-mode-maker | không | có thì đổi class/token theo hệ design dự án |
| Out | HTML/CSS/JS đã adapt | có | không còn import faker, class BEM khớp CSS và JS |
| Out | bằng chứng verify | có | ảnh chụp + cuộn thử qua `playwright-verify` |

### Rules và capabilities
- RULE-01 (MUST): **`assets/timeline.js` dòng 1 import `faker` từ `esm.sh` chỉ để SINH DỮ LIỆU GIẢ cho demo** (`generateArticles()`) — khi wire vào dự án thật, XOÁ import đó + `generateArticles()`, thay `this.articles` bằng dữ liệu THẬT (API/markdown/CMS) trước khi build(). Để nguyên import faker trong production là phụ thuộc thừa + lộ dữ liệu giả.
- RULE-02 (MUST): Class đặt tên theo BEM (`timeline__item-time`...) — đổi tên class thì đổi cả CSS lẫn JS `querySelector`, đừng đổi một bên.
- RULE-03 (MUST): Ngưỡng `threshold: 1` của `IntersectionObserver` nghĩa là mốc phải vào khung nhìn TOÀN BỘ mới hiện — mốc cao hơn viewport (nội dung dài) sẽ không bao giờ đạt threshold 1, hạ xuống `0.5` nếu mốc có nội dung dài.
- RULE-04 (MUST): Verify bằng `playwright-verify` (chụp + cuộn thử) sau khi wire dữ liệu thật, không tự khen "chạy được" chỉ vì không lỗi console.
- Capabilities: đọc asset mẫu của skill; ghi file front-end của trang đích; chạy trình duyệt headless để chụp/cuộn kiểm.

### Failure boundaries
- Chưa có dữ liệu mốc thật → **clarify** nguồn dữ liệu; không giao bản còn faker.
- Việc thật ra là sơ đồ quan hệ/luồng hoặc biểu đồ số → **blocked**, chuyển `/diagram` hoặc `dataviz`.
- Verify playwright thấy mốc không hiện khi cuộn → **failed**, sửa (vd hạ threshold) rồi verify lại.

## HOW

### Main workflow
| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W01 | deterministic | skill assets | Đọc `assets/timeline.html` + `assets/timeline.css` + `assets/timeline.js` | hiểu cấu trúc | — |
| W02 | judgment | asset, `design.md` | ADAPT vào trang đích: đổi class/token theo hệ design dự án (BEM đồng bộ CSS + JS) | component trong trang | không có design.md → giữ token mẫu |
| W03 | effect | dữ liệu thật | Xoá import faker + `generateArticles()`, thay `this.articles` bằng dữ liệu THẬT trước build() | JS không còn faker | thiếu dữ liệu → clarify |
| W04 | judgment | dự án | Chọn dark-mode: giữ `prefers-color-scheme` hoặc thay bằng token `dark-mode-maker` (B01) | một cơ chế dark duy nhất | — |
| W05 | deterministic | trang | Verify bằng `playwright-verify`: chụp + cuộn thử | ảnh + mốc hiện đủ | mốc không hiện → B02 |

Chi tiết từng bước (nguồn chân lý cho W01–W05):

#### Assets
`assets/timeline.html` + `assets/timeline.css` + `assets/timeline.js` — đọc rồi ADAPT vào trang đích (đổi class/token theo hệ design của dự án nếu đã có `design.md`), không copy máy móc y nguyên.

#### Cơ chế
- Mỗi mốc là `<li class="timeline__item">` chứa `<time>` (ngày, `datetime` attr chuẩn ISO) + `<a>` tiêu đề + `<small>` nguồn.
- `IntersectionObserver` gắn class `timeline__item--in` khi mốc cuộn vào khung nhìn → CSS transition làm nó "hiện dần" (opacity + translateX), KHÔNG animate bằng JS trực tiếp.
- Responsive: mobile — chấm mốc + đường nối bên trái, ngày nằm trong dòng. `≥768px` — ngày tách ra cột riêng bên trái (`position: absolute`).
- Dark theme qua `@media (prefers-color-scheme: dark)` — đổi 3 biến `--bg/--fg/--primary`; nếu dự án đã có `dark-mode-maker` (toggle chủ động, không chỉ theo OS) thì thay khối này bằng biến token của `dark-mode-maker`, đừng để hai cơ chế dark-mode chỏi nhau.

### Branches
| ID | Kind | Guard | Hành vi | Skip / failure | Rejoin |
|---|---|---|---|---|---|
| B01 | conditional_required | dự án đã có `dark-mode-maker` | thay khối `prefers-color-scheme` bằng biến token của `dark-mode-maker` | không có → giữ khối mẫu | W05 |
| B02 | recovery | mốc có nội dung dài, cao hơn viewport, không bao giờ hiện | hạ `threshold: 1` xuống `0.5` (RULE-03) | vẫn không hiện → failed, báo user | W05 |

### Validation và stopping
Xong khi: grep không còn `faker`/`generateArticles` trong JS trang đích, class CSS và JS khớp, và `playwright-verify` chụp được mọi mốc hiện sau khi cuộn. Không lỗi console chưa đủ để kết luận (RULE-04).

### Examples
- **Positive:** "làm changelog timeline từ CHANGELOG.md" → adapt 3 asset, dữ liệu parse từ markdown thay `this.articles`, xoá faker → playwright cuộn thấy mọi mốc có class `timeline__item--in`, desktop ≥768px ngày nằm cột trái.
- **Boundary/failure:** mốc roadmap mô tả dài hơn chiều cao màn hình → với `threshold: 1` mốc đứng opacity 0 mãi → B02 hạ `0.5`, verify lại thấy hiện.

## Origin
- Nén từ `llmwiki/patterns/timeline/` (snippet tham khảo chưa gắn skill nào, chưa từng track git) thành skill thật theo yêu cầu user 2026-09-17 — cùng đợt với `blur`.
