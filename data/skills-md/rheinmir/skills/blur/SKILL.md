---
name: blur
description: Hiệu ứng WebGL "zoom blur" chuyển ảnh nền toàn màn hình (Three.js + shader GLSL riêng, parallax theo chuột, điều hướng scroll/click/phím) cho hero section/slideshow ảnh. Gọi khi user nói "hiệu ứng blur ảnh", "chuyển ảnh mờ dần kiểu zoom", "webgl blur transition", "gallery ảnh full-screen kiểu blur", hoặc /blur. KHÁC `dark-mode-maker` (circle-reveal đổi theme) — đây là hiệu ứng CHUYỂN ẢNH, không phải chuyển theme.
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.0.0"
  loop: utils
---

# Skill: blur

Component WebGL thuần — canvas full-screen, chuyển giữa các ảnh bằng "zoom blur" (radial blur hội tụ về tâm), scroll/click/phím mũi tên để điều hướng, tâm blur bám theo chuột.

## WHAT

### Purpose và context
- **Purpose:** gắn vào trang một canvas WebGL full-screen chuyển giữa các ảnh bằng hiệu ứng zoom-blur (ảnh ra mờ dần hội tụ về tâm, ảnh vào rõ dần), điều hướng bằng scroll/click/phím, tâm blur bám chuột.
- **Trigger (when to use):**
  - Hero section hoặc slideshow ảnh cần hiệu ứng chuyển CAO CẤP hơn crossfade thường (zoom-blur transition).
  - User nói "hiệu ứng blur ảnh", "webgl blur", "gallery kiểu zoom blur".
- **Non-goals:** KHÔNG dùng cho blur/frosted-glass TĨNH của UI card/panel (đó là `backdrop-filter: blur()` CSS thường, hoặc `docs-site-macos` liquid-glass) — đây là hiệu ứng CHUYỂN ĐỘNG giữa các ảnh, tốn GPU hơn hẳn. Không đổi theme (việc của `dark-mode-maker`).

### Mental model
`mảng images → mỗi ảnh = PlaneBufferGeometry + shader ZoomBlurImage → progress/targetProgress lerp → uStrength 2 layer đan chéo → frame render; input (wheel/click/phím) đổi targetProgress; chuột đổi uCenter`.

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | danh sách ảnh | có | thay mảng `images` trong `assets/blur.js` |
| In | tốc độ / easing | không | chỉnh `duration`/easing, mặc định giữ như asset |
| In | trang chứa có `gsap` global | có | `initScene()` gọi `gsap.fromTo(...)` mà không import |
| Out | `blur.html` + `blur.css` + `blur.js` đã adapt | có | canvas full-screen chạy được trong trang đích |
| Out | bằng chứng verify | có | ảnh chụp trước/sau khi cuộn + console sạch (qua `playwright-verify`) |

### Rules và capabilities
- RULE-01 (MUST): Đây là hiệu ứng NẶNG GPU (shader chạy mỗi frame trên toàn viewport) — không dùng cho nhiều instance cùng lúc trên 1 trang, và test trên máy yếu/mobile trước khi chốt (WebGL context có giới hạn số lượng đồng thời của trình duyệt).
- RULE-02 (MUST): Verify bằng `playwright-verify` — chụp trước/sau khi cuộn, đọc console (context WebGL lỗi thường im lặng ở canvas, không throw JS error thấy ngay).
- RULE-03 (MUST): Đọc mục "Nợ kỹ thuật đã biết" TRƯỚC khi dùng production — vendor hoá import CDN `useThree` trước khi giao khách hàng/sản phẩm thật.
- Capabilities: đọc asset của skill; ghi file HTML/CSS/JS vào dự án đích; chạy trình duyệt headless để chụp + đọc console.

### Failure boundaries
- Trang chứa thiếu `<script>` gsap → `gsap.fromTo(...)` ném lỗi ngay khi ảnh load xong → **blocked** tới khi thêm script.
- CDN CodePen/unpkg không tải được → canvas trắng → **failed**; hướng sửa là vendor hoá (mục Nợ kỹ thuật).
- Canvas không render nhưng không có JS error → coi là **failed** cho tới khi console/ảnh chụp chứng minh ngược lại (lỗi WebGL im lặng).
- Yêu cầu là blur tĩnh cho card/panel → ngoài phạm vi, chuyển `backdrop-filter` / `docs-site-macos`.

## HOW

### Main workflow
| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W01 | judgment | yêu cầu user | Xác nhận đây là chuyển ảnh động, không phải blur tĩnh UI | đi tiếp / chuyển skill khác | blur tĩnh → dừng, gợi ý `backdrop-filter` |
| W02 | deterministic | `assets/blur.*` | Đọc `assets/blur.html` + `assets/blur.css` + `assets/blur.js` | nội dung asset | — |
| W03 | effect | asset, ảnh của user | ADAPT: đổi mảng `images`, chỉnh `duration`/easing; đảm bảo trang có `gsap` global | file trong dự án đích | — |
| W04 | judgment | đích dùng (prototype/production) | Rà mục Nợ kỹ thuật; production → B01 | quyết định vendor hoá | — |
| W05 | deterministic | trang đã gắn | Verify bằng `playwright-verify`: chụp trước/sau cuộn, đọc console | ảnh + log console | lỗi/canvas trắng → sửa rồi lặp W05 |

### Branches
| ID | Kind | Guard | Hành vi | Skip / failure | Rejoin |
|---|---|---|---|---|---|
| B01 | conditional_required | dùng cho khách hàng/sản phẩm thật | vendor hoá pen `useThree` thành file `.js` trong `assets/`, xoá import CDN (tự viết lại nếu license pen không rõ); có bundler thì cài `three` qua npm | prototype → skip | W05 |
| B02 | recovery | console báo `gsap is not defined` | thêm `<script src="gsap...">` vào trang chứa | — | W05 |

### Validation và stopping
Xong khi ảnh chụp trước/sau cuộn khác nhau (chuyển ảnh xảy ra) và console không có lỗi WebGL/JS. Không lặp W05 vô hạn: sau 2 vòng vẫn lỗi → báo user kèm log console.

### Examples
- **Positive:** "làm hero slideshow 4 ảnh kiểu zoom blur" → thay `images` bằng 4 URL, trang đã có gsap → playwright chụp trước/sau cuộn thấy ảnh 1→ảnh 2, console sạch → giao.
- **Boundary/failure:** trang đích không nạp gsap → console `gsap is not defined` ngay khi ảnh load → B02 thêm script, verify lại; user muốn "card mờ kiểu kính" → W01 dừng, gợi ý `backdrop-filter: blur()`.

### Reference — Assets
`assets/blur.html` + `assets/blur.css` + `assets/blur.js` — đọc rồi ADAPT (đổi mảng `images`, chỉnh tốc độ `duration`/easing).

### Reference — ⚠️ Nợ kỹ thuật đã biết — đọc TRƯỚC khi dùng production
`assets/blur.js` dòng 12 import helper `useThree` từ **một CodePen pen của người khác** (`codepen.io/soju22/pen/...js`) — đây là **phụ thuộc CDN vào tài nguyên không do ta sở hữu, có thể đổi/gỡ bất cứ lúc nào không báo trước**. Snippet gốc là demo tham khảo, chưa hardened cho production.
- **ponytail: global external dependency chưa vendor hoá, nâng cấp khi cần production thật** — trước khi dùng cho khách hàng/sản phẩm thật: (1) đọc nội dung pen đó, vendor hoá thành file `.js` riêng trong `assets/`, xoá import CDN; (2) tự viết lại `useThree` (Three.js scene/camera/renderer boilerplate) nếu không rõ license của pen gốc.
- `import ... from 'https://unpkg.com/three@0.120.0/...'` (dòng 1-10) cũng là CDN runtime — chấp nhận được cho prototype, nhưng dự án có bundler nên cài `three` qua npm rồi import local, tránh phụ thuộc mạng lúc chạy.
- `gsap` dùng trong `initScene()` nhưng KHÔNG được import trong file — giả định biến global đã có sẵn (script `<script src="gsap...">` ở trang chứa nó). Thiếu `<script>` đó thì `gsap.fromTo(...)` ném lỗi ngay khi ảnh load xong.

### Reference — Cơ chế
- Mỗi ảnh là một `PlaneBufferGeometry` phủ shader tuỳ biến (`ZoomBlurImage`) — fragment shader lấy mẫu ảnh dọc theo vector hướng-về-tâm, trọng số Bezier, tạo hiệu ứng mờ hội tụ khi `uStrength` khác 0.
- Chuyển ảnh: `progress`/`targetProgress` lerp dần (`updateProgress`), `uStrength` của 2 layer ảnh đan chéo (ảnh ra mờ dần, ảnh vào rõ dần).
- Input: cuộn chuột (`wheel`) đổi `targetProgress` theo bước 1/20; click nửa trên/dưới màn hình = lùi/tiến; phím mũi tên tương tự.
- Tâm blur (`uCenter`) lerp theo vị trí chuột mỗi frame → hiệu ứng "mắt dõi theo con trỏ".

## Origin
- Nén từ `llmwiki/patterns/blur/` (snippet tham khảo chưa gắn skill nào, chưa từng track git) thành skill thật theo yêu cầu user 2026-09-17 — cùng đợt với `timeline`.
