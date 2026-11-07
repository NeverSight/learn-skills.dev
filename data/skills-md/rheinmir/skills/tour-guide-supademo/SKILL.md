---
name: tour-guide-supademo
description: >
  Style thiết kế Supademo cho in-app product tour (dùng kèm skill tour-guide — component
  gốc 0 dependency): blinker hotspot pulse, tooltip card, step counter + nav buttons,
  progress bar, theme tokens — quy ra recipe Tailwind/CSS dùng ngay. Trigger:
  "/tour-guide-supademo", "tour kiểu Supademo", "style supademo", "blinker hotspot".
  Quy ước: style distill từ sản phẩm khác sẽ là skill riêng /tour-guide-<tên>.
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.0.0"
  loop: utils
---

# tour-guide-supademo — Tour style kiểu Supademo

Distill từ player Supademo (supademo.com, 2026-06). Docs họ không công bố hex/px chính xác — đây là design language quy ra recipe dùng được ngay. Component nền lấy từ skill **tour-guide**; skill này là lớp style đè lên.

Nguyên tắc: brand color là 1 token duy nhất (`--tour-brand`), mọi thứ ăn theo.

## WHAT

### Purpose và context
- **Purpose:** phủ lớp style kiểu Supademo (blinker hotspot, tooltip card, control bar, progress/timer bar, transition, theme tokens) lên component tour của skill **tour-guide**, dưới dạng recipe Tailwind/CSS copy dùng ngay, ăn theo một token brand duy nhất.
- **Trigger (when to use):** "/tour-guide-supademo", "tour kiểu Supademo", "style supademo", "blinker hotspot"; khi đã/ sẽ dùng component `tour-guide` và muốn giao diện kiểu Supademo.
- **Non-goals:** không chứa UX mechanic (đo/cuộn/step, branching, cơ chế timer — thuộc skill **tour-guide**); không hardcode hex brand gốc của Supademo; style của sản phẩm khác là skill riêng `tour-guide-<tên>`.

### Mental model
`--tour-brand (1 token) → blinker · tooltip card · control bar · progress bar · autoplay timer bar · transition · backdrop per-spot → map sang TOUR_THEME của tour-guide`. Skill này = lớp style; tour-guide = component nền + cơ chế.

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | component tour từ skill **tour-guide** | có | nền để đè style |
| In | màu brand | có | gán vào `--tour-brand` |
| In | `theme` light/dark, `showProgress`, `showNav`, `showStepCount` | không | theme tokens, map sang `TOUR_THEME` |
| Out | CSS/Tailwind của tour theo recipe | có | blinker + card + control bar + bars + transition |
| Out | hành vi tickbox "Bỏ qua phần menu" + auto-open TẮT | có | theo bài học thực chiến |

### Rules và capabilities
- RULE-01 (MUST): Nguyên tắc: brand color là 1 token duy nhất (`--tour-brand`), mọi thứ ăn theo.
- RULE-02 (MUST): Font tooltip **1rem cố định** — đừng làm chữ tooltip bé như hint; 3 cỡ width S/M/L, đừng auto-width theo chữ khi label dài.
- RULE-03 (MUST): Đừng auto-mở tour khi load trừ khi được yêu cầu rõ (Auto-open: mặc định TẮT).
- RULE-04 (MUST): Tickbox là "bỏ qua step khung" — KHÔNG phải "đừng hiện tour nữa"; persist 2 lớp `localStorage` + `window.name`, bọc try/catch.
- RULE-05 (MUST): Quy ước mở rộng — style sản phẩm khác distill thành skill riêng `tour-guide-<tên>` theo đúng format file này; UX mechanic gửi về skill **tour-guide**.
- Capabilities: ghi CSS/Tailwind/TSX vào dự án đích; đọc component tour-guide. Không mạng.

### Failure boundaries
- Chưa có component tour-guide trong dự án → **blocked**: dựng nền bằng skill **tour-guide** trước.
- Yêu cầu là UX mechanic (step mode, branching, timer) → ngoài phạm vi, chuyển **tour-guide**.
- Yêu cầu style của sản phẩm khác (Intercom, Driver.js…) → không nhét vào đây; tạo `tour-guide-<tên>`.
- Hex/px chính xác của Supademo → không có (docs họ không công bố); dùng recipe quy đổi, nói rõ là ước lượng.

## HOW

### Main workflow
| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W01 | judgment | yêu cầu | Xác nhận có component tour-guide + đây là việc style | đi tiếp | thiếu nền → tour-guide trước |
| W02 | effect | màu brand | Đặt `--tour-brand`, theme tokens map sang `TOUR_THEME` | token | — |
| W03 | effect | recipe | Áp blinker, tooltip card, control bar (+ tickbox), progress + autoplay timer bar, transition, backdrop per-spot | tour mang style Supademo | overflow control bar → tickbox xuống hàng riêng |
| W04 | judgment | tour chạy | Kiểm: auto-open tắt, tickbox hiệu lực ngay, Esc đóng, font 1rem | đạt | lệch → sửa, lặp W04 |

Chi tiết từng bước (nguồn chân lý cho W01–W04): recipe dưới mục "Reference — Supademo design recipe".

### Branches
| ID | Kind | Guard | Hành vi | Skip / failure | Rejoin |
|---|---|---|---|---|---|
| B01 | user_optional | spot chỉ cần ring + blinker, không dim | flag `noDim?: boolean` trên TourSpot | mặc định dim | W04 |
| B02 | user_optional | yêu cầu rõ auto-open lần đầu | guard `!overlay` cả trước và sau delay | mặc định TẮT | W04 |
| B03 | user_optional | label dài, demo-style | typewriter effect cho label | mặc định không | W04 |
| B04 | conditional_required | trang không có step riêng khi tickbox đang tick | đóng tour | — | kết thúc |

### Validation và stopping
Cần mắt: card 280px không overflow, font 1rem, blinker đúng tâm target. Có thể kiểm tất định: tickbox persist qua reload (`localStorage`/`window.name`), Esc đóng, click nền sang bước kế. Dừng khi W04 đạt.

### Examples
- **Positive:** "tour kiểu Supademo màu tím cho dashboard" → `--tour-brand` = tím, blinker `animate-ping` ở tâm nút, card M ≈ 280px `rounded-xl`, control bar `4 / 9` + [Quay lại] [Tiếp], progress bar 2–3px mép trên overlay.
- **Boundary/failure:** control bar nhét tickbox + counter + 2 nút trên một hàng trong card 280px → overflow; sửa bằng tickbox xuống hàng riêng + `white-space:nowrap`. User muốn "tour kiểu Intercom" → không sửa file này, distill skill `tour-guide-intercom`.

### Reference — Supademo design recipe

#### Blinker hotspot (signature look)

Chấm tròn ~12px màu brand + vòng ripple `animate-ping` lan ra, đặt tại tâm element cần click. Transparency vòng ngoài ~25–30%.

```tsx
<span className="absolute flex h-3 w-3" style={{ top: cy, left: cx }}>
  <span className="absolute inline-flex h-full w-full animate-ping rounded-full opacity-30"
    style={{ background: "var(--tour-brand)" }} />
  <span className="relative inline-flex h-3 w-3 rounded-full"
    style={{ background: "var(--tour-brand)" }} />
</span>
```

Hợp với step mode: blinker chỉ vào chỗ cần click, tooltip giải thích bên cạnh.

#### Tooltip card

- Nền trắng; dark theme: `bg-slate-900 text-white`.
- Bo `rounded-xl` (~12px), shadow mềm `shadow-[0_4px_16px_rgba(0,0,0,0.12)]`, padding `px-3.5 py-2.5`.
- Font **1rem cố định** — Supademo cố tình không cho chỉnh size; đừng làm chữ tooltip bé như hint.
- Mũi tên nhỏ chỉ vào target.
- 3 cỡ width: S ≈ 200px / M ≈ 280px / L ≈ 360px — đừng auto-width theo chữ khi label dài.

#### Control bar (share chung mọi bước)

Hàng dưới của tooltip card, layout cố định: `[lối thoát] · i/n ……… [Quay lại] [Tiếp/Xong]`
- Trái: counter `4 / 9` chữ xám nhỏ (`text-xs text-slate-400`); hàng riêng bên dưới: tickbox **"Lần sau bỏ qua phần menu"** (xem mục dưới). Tickbox xuống hàng riêng + `white-space:nowrap` — card 280px không nhét nổi tickbox + counter + 2 nút trên 1 hàng (sẽ overflow).
- Phải: Back (ghost) + Next (nền brand, `rounded-lg px-3 py-1.5`).
- Label nút custom được ("Tiếp", "Xong") thay vì luôn Next/Previous.
- Esc luôn đóng; click nền = bước kế (bước cuối = đóng).

#### Tickbox "bỏ qua step trùng lặp" (bài học thực chiến)

Tour nhiều trang luôn có 2 loại step: **khung** (menu/sidebar/header — trang nào cũng hệt nhau) và **riêng của trang**. User xem khung 1 lần là đủ — bắt xem lại mỗi lần mở tour là điểm gây ức chế số 1.

- Tickbox = `[ ] Bỏ qua phần menu` (label ngắn — user feedback: đừng dài dòng "lần sau…") — KHÔNG phải "đừng hiện tour nữa". Tick → flag persist; `measure()` lọc bỏ nhóm spots khung, chỉ giữ spots `data-tour-*` của view đang active. Cơ chế đo/cuộn/step nằm bên skill **tour-guide**.
- **Hiệu lực ngay khi tick**: re-measure + nhảy về step nội dung đầu tiên (`steps=measure(); idx=0; render()`), không bắt user đi nốt phần khung. Trang không có step riêng → đóng tour.
- Untick (mở tour lại sẽ thấy box đang tick) → xoá flag, menu quay lại danh sách.
- Persist 2 lớp: `localStorage` + `window.name` (file:// có browser chặn storage — window.name sống qua reload cùng tab). Bọc try/catch.
- Bắt bằng `change` delegation trên overlay (innerHTML re-render mỗi bước, đừng gắn listener vào input).

#### Auto-open: mặc định TẮT

Đừng auto-mở tour khi load trừ khi được yêu cầu rõ. Bài học: auto-open + cache cũ/đa origin (file:// vs localhost = 2 localStorage khác nhau) tạo cảm giác "tắt rồi vẫn hiện", user mất niềm tin vào toggle. Tour mở bằng nút trigger (`?`) là đủ; nếu thật sự cần auto-open lần đầu, guard `!overlay` cả trước và sau delay để không toggle-đóng tour user vừa tự mở.

#### Progress bar

Thanh mảnh 2–3px màu brand chạy ngang mép trên overlay, `width = (step+1)/total*100%`, toggle được.

#### Autoplay timer bar

Thanh 2px màu brand chạy trên **mép trên của tooltip card** (khác progress bar tổng ở mép màn hình): fill 0→100% linear đúng thời lượng autoplay (mặc định 2.5s/bước — 1.75s thử thực tế quá gấp để đọc) rồi tự qua bước kế. Card cần `overflow:hidden` để bar ôm bo góc. Hover card → bar đứng (`animationPlayState:paused`), rời chuột → bar + đồng hồ chạy lại từ đầu. Cơ chế timer nằm bên skill **tour-guide**.

#### Transition

- Tooltip vào: fade + slide-in nhẹ (`transition-all duration-200`, translate-y 4px → 0).
- Giữa các step: KHÔNG animate vị trí (nhảy thẳng), chỉ fade nội dung.
- Typewriter effect cho label là tuỳ chọn — chỉ đáng khi label dài, demo-style.

#### Backdrop per-spot

Style "Default" của Supademo chỉ ring quanh element, không dim màn hình → map sang flag `noDim?: boolean` trên TourSpot nếu muốn spot chỉ có ring + blinker.

#### Theme tokens

Supademo workspace-level cho chỉnh đúng các thứ sau — map sang `TOUR_THEME` của tour-guide là ngang tính năng:

| token | ý nghĩa |
|---|---|
| `brand` | màu chủ đạo (blinker, Next, progress) |
| `theme` | `"light" \| "dark"` cho tooltip card |
| `showProgress` | bật/tắt progress bar |
| `showNav` | bật/tắt Back/Next |
| `showStepCount` | bật/tắt counter "i / n" |

#### Quy ước mở rộng

Muốn style từ sản phẩm khác (Intercom, Driver.js, Stripe…) → distill thành skill riêng `tour-guide-<tên>` theo đúng format file này: token brand duy nhất, recipe Tailwind/CSS copy được (không mô tả suông), không hardcode hex brand gốc, ghi nguồn + ngày distill cuối file. UX mechanic (step mode, branching…) thì gửi về skill **tour-guide**, không để trong skill style.


## Sources

[Hotspot docs](https://docs.supademo.com/customize/hotspot) · [HTML hotspots](https://docs.supademo.com/customize/hotspot/html-based-hotspots) · [Workspace theme](https://docs.supademo.com/customize/personalize/custom-branding/workspace-theme) — distill 2026-06-10
