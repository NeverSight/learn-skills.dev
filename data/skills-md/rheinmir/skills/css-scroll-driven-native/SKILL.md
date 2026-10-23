---
name: css-scroll-driven-native
description: Hiệu ứng cuộn trang thuần CSS qua Native CSS Scroll-Driven Animations API (animation-timeline scroll()/view(), animation-range) — ZERO JavaScript. Gọi khi user nói "css scroll driven animation", "animation-timeline", "scroll animation không js", "css thuần cuộn trang", "scroll-driven CSS", hoặc /css-scroll-driven-native. KHÁC `skills/scroll-effects` (đó dùng IntersectionObserver JS, chạy MỌI trình duyệt hiện đại) — skill này 0 JS nhưng trình duyệt CHƯA hỗ trợ đủ (Firefox/Safari còn behind flag/rollout), dùng làm progressive enhancement phía trên scroll-effects, không thay thế khi cần chạy chắc trên mọi trình duyệt.
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.0.0"
  loop: utils
---

# Skill: css-scroll-driven-native

Hiệu ứng cuộn trang bằng **CSS spec công khai** — `animation-timeline: scroll()` / `view()` + `animation-range` — không một dòng JavaScript.

## WHAT

### Purpose và context
- **Purpose:** thêm hiệu ứng cuộn (progress bar, reveal-on-view, parallax nhẹ) bằng CSS thuần `animation-timeline` làm progressive enhancement — trình duyệt chưa hỗ trợ hoặc bật reduce-motion vẫn thấy đủ nội dung tĩnh.
- **Trigger (when to use):** user nói "css scroll driven animation", "animation-timeline", "scroll animation không js", "css thuần cuộn trang", "scroll-driven CSS", hoặc /css-scroll-driven-native; hoặc muốn thêm "độ mượt" 0-JS phía trên `scroll-effects`. Chọn theo bảng "Khi nào chọn cái này vs `scroll-effects`" (mục Reference).
- **Non-goals:** không phải cơ chế chính khi cần chạy chắc production đa trình duyệt ngay (đó là `scroll-effects`, JS IntersectionObserver); không viết JS; không cứng số phiên bản trình duyệt.

### Mental model
`timeline (scroll(root) | view()) + animation-range → keyframes; toàn bộ nằm trong @supports → @media not (prefers-reduced-motion: reduce); ngoài hai khối đó = trạng thái tĩnh hiện đủ nội dung`.

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | cơ chế cần (progress / reveal / parallax) | có | chọn 1–3 trong 3 cơ chế |
| In | `design.md` của dự án | không | có thì đổi token màu/spacing theo nó |
| Out | CSS (+ markup tối thiểu) adapt từ `assets/demo.css` / `assets/demo.html` | có | mọi animation trong `@supports` + reduce-motion guard |
| Out | bằng chứng verify | có | ảnh 0%/50%/100% scroll + ảnh reduce-motion qua `playwright-verify` |

### Rules và capabilities
Rules (BẮT BUỘC):
- RULE-01 (MUST): **Luôn có fallback `@supports`**: mọi animation nằm trong `@supports (animation-timeline: scroll())` hoặc `@supports (animation-timeline: view())`. Bên NGOÀI khối `@supports` là trạng thái TĨNH mặc định — phần tử **hiện đủ nội dung**, không animation, **KHÔNG BAO GIỜ ẩn/opacity:0 làm mặc định**. Nếu viết `opacity:0` cho hiệu ứng reveal, giá trị đó CHỈ được đặt bên trong `@supports`, không phải ở rule gốc.
- RULE-02 (MUST): **`prefers-reduced-motion`**: bọc animation trong `@media not (prefers-reduced-motion: reduce)` (lồng bên trong `@supports`, xem `demo.css`). Người dùng bật reduce-motion → mọi phần tử về trạng thái tĩnh giống hệt trình duyệt không hỗ trợ.
- RULE-03 (MUST): KHÔNG cứng số phiên bản vào code hay comment — kiểm tra [caniuse.com/css-scroll-driven-animations](https://caniuse.com/css-scroll-driven-animations) mỗi lần dùng thật (bảng hỗ trợ ở mục Reference).
- RULE-04 (MUST): `animation-duration` vẫn phải khai (`1ms` hoặc giá trị bất kỳ >0) dù thời lượng thật do timeline điều khiển — một số engine yêu cầu giá trị này để kích hoạt animation.
- RULE-05 (MUST): Verify bằng `playwright-verify` trên trình duyệt Chromium (CDP mặc định hỗ trợ scroll-driven animations): chụp ảnh tại 0%/50%/100% scroll, assert progress bar/scaleX và card opacity đổi theo vị trí cuộn; đồng thời chụp thêm với `prefers-reduced-motion: reduce` giả lập (Playwright `emulateMedia`) để assert KHÔNG animation nhưng nội dung vẫn hiện đủ.
- Capabilities: đọc asset skill + `design.md`; ghi CSS/HTML vào dự án đích; chạy trình duyệt Chromium headless có giả lập media.

### Failure boundaries
- Yêu cầu "phải chạy chắc trên mọi trình duyệt ngay" → **clarify**/chuyển `scroll-effects` làm nền, skill này chỉ override.
- Nội dung bị ẩn khi `@supports` sai hoặc reduce-motion bật → **failed** (vi phạm RULE-01/02), sửa trước khi giao.
- Ảnh 0%/50%/100% giống hệt nhau trên Chromium → **failed** (animation không kích hoạt, thường thiếu `animation-duration`).

## HOW

### Main workflow
| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W01 | judgment | yêu cầu + đích trình duyệt | Chọn skill này hay `scroll-effects` theo bảng so sánh; kiểm caniuse | quyết định | cần chắc đa trình duyệt → B01 |
| W02 | deterministic | `assets/demo.*` | Đọc `assets/demo.html` + `assets/demo.css`, lấy cơ chế cần | snippet | — |
| W03 | effect | snippet, `design.md` | ADAPT token màu/spacing; đặt animation trong `@supports` + reduce-motion | CSS trong dự án | — |
| W04 | deterministic | trang đã gắn | Verify RULE-05: chụp 0/50/100% + `emulateMedia` reduce | ảnh + assert | assert đỏ → sửa, lặp W04 |

### Branches
| ID | Kind | Guard | Hành vi | Skip / failure | Rejoin |
|---|---|---|---|---|---|
| B01 | user_optional | cần chạy chắc đa trình duyệt nhưng vẫn muốn 0-JS mượt hơn | kết hợp: `scroll-effects` làm nền, skill này override khi trình duyệt hỗ trợ | chỉ cần Chromium → skip | W02 |

### Validation và stopping
Assert tất định ở W04 (scaleX/opacity đổi theo vị trí cuộn; reduce-motion không animation, nội dung đủ). Cần mắt: độ mượt/hợp design. Dừng khi hai loại ảnh đều đạt; 2 vòng vẫn đỏ → báo user kèm ảnh.

### Examples
- **Positive:** "thêm progress bar đọc bài bằng css thuần" → `.csdn-progress` với `animation-timeline: scroll(root)` trong `@supports` + reduce-motion guard → ảnh 0%/50%/100% cho scaleX 0 → ~0.5 → 1.
- **Boundary/failure:** reveal card đặt `opacity:0` ở rule gốc → trên Firefox chưa hỗ trợ card biến mất → vi phạm RULE-01, chuyển `opacity:0` vào trong `@supports` rồi verify lại với reduce-motion.

### Reference — Khi nào chọn cái này vs `scroll-effects`

| | `css-scroll-driven-native` (skill này) | `scroll-effects` |
|---|---|---|
| JS | 0 dòng | IntersectionObserver + rAF |
| Hỗ trợ trình duyệt | Chrome/Edge tốt; Firefox/Safari đang rollout, có thể chưa bật mặc định | Mọi trình duyệt hiện đại |
| Khi dùng | Progressive enhancement — thêm "độ mượt" cho trình duyệt đã hỗ trợ, KHÔNG phải cơ chế chính nếu cần chạy chắc production đa trình duyệt ngay | Cơ chế chính khi cần chạy chắc ngay, không đợi rollout |

Khuyến nghị: dùng skill này bên trong `@supports (animation-timeline: scroll())`, fallback tĩnh (không animation, không ẩn nội dung) — hoặc kết hợp cả hai: `scroll-effects` làm nền, skill này override khi trình duyệt hỗ trợ.

⚠️ **Kiểm tra hỗ trợ thật trước khi dùng production** tại [caniuse.com/css-scroll-driven-animations](https://caniuse.com/css-scroll-driven-animations) — đừng tin số liệu cứng ghi trong tài liệu này, API đang rollout nhanh và bảng hỗ trợ có thể đã đổi.

**Bảng hỗ trợ trình duyệt hiện tại** (ghi tại thời điểm viết skill, 2026-09 — có thể đã đổi, luôn tự kiểm tra):
| Trình duyệt | `animation-timeline: scroll()` | `animation-timeline: view()` |
|---|---|---|
| Chrome / Edge | Có | Có |
| Firefox | Behind flag / đang rollout | Behind flag / đang rollout |
| Safari | Đang rollout, chưa ổn định | Đang rollout, chưa ổn định |

### Reference — Assets

`assets/demo.html` + `assets/demo.css` — 3 cơ chế demo, đọc rồi ADAPT (đổi token màu/spacing theo `design.md` của dự án nếu có). Mở trực tiếp bằng trình duyệt hỗ trợ (Chrome/Edge mới) để xem chạy thật; trình duyệt chưa hỗ trợ sẽ tự rơi về trạng thái tĩnh.

### Reference — 3 cơ chế (markup tối thiểu + cơ chế)

#### 1. Progress bar theo cuộn trang
Thanh cố định trên cùng, dài theo % đã cuộn hết trang.
```html
<div class="csdn-progress"></div>
```
```css
.csdn-progress {
  animation-name: progress-scale;
  animation-duration: 1ms; /* giá trị bất kỳ để kích hoạt engine — thời lượng thật do timeline điều khiển */
  animation-timeline: scroll(root);
  animation-fill-mode: both;
}
@keyframes progress-scale {
  from { transform: scaleX(0); }
  to   { transform: scaleX(1); }
}
```
`scroll(root)` bám vào tiến độ cuộn của toàn trang — không cần `scroll` listener, không cần tính `scrollY / scrollHeight` bằng tay.

#### 2. Reveal-on-view khi phần tử vào khung nhìn
```html
<article class="csdn-card">…</article>
```
```css
.csdn-card {
  animation-name: reveal-in;
  animation-timeline: view();
  animation-range: entry 0% cover 40%;
  animation-fill-mode: both;
}
```
`view()` là timeline riêng của TỪNG phần tử theo vị trí trong viewport của chính nó — thay hẳn IntersectionObserver. `animation-range: entry 0% cover 40%` nghĩa là animation chạy từ lúc phần tử bắt đầu vào viewport (`entry 0%`) tới khi đã "cover" 40% quãng đường qua viewport.

#### 3. Parallax nhẹ dùng `view()`
Nền và nội dung dùng **`animation-range` khác nhau** trên cùng một timeline `view()` → tạo cảm giác lớp trôi khác tốc độ, không cần tính toán `scrollY` thủ công.
```css
.parallax-bg      { animation-timeline: view(); animation-range: cover 0% cover 100%; }   /* trôi chậm, suốt cả quãng */
.parallax-content { animation-timeline: view(); animation-range: entry 0% cover 35%; }    /* chạy nhanh, chỉ đoạn đầu */
```
Xem `assets/demo.css` mục 3 để có keyframes đầy đủ.

## Origin

- Bổ sung cho `skills/scroll-effects` (JS-based, chạy mọi trình duyệt) một lựa chọn 0-JS cho trình duyệt đã hỗ trợ — hai skill KHÔNG thay thế nhau, dùng theo bảng "Khi nào chọn cái này" ở trên.
