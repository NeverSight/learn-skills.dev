---
name: visual-qa
description: >-
  WORKFLOW tự-kiểm THỊ GIÁC khép kín cho SPA local (app do /br sinh, hoặc bất kỳ web app):
  chụp headless từng route → BASELINE pixel-diff (bắt thay đổi ngoài ý muốn) → bất biến
  máy-kiểm (design conformance) → agent ĐỌC HẾT ảnh theo rubric → FINDINGS.md → sửa → chụp
  lại → chỉ pass khi máy VÀ mắt cùng sạch. Dùng khi đổi theme/UI/rebrand, khi extension MCP
  không chụp được localhost, hoặc cần gate UI cho frame. Trigger: "qa thị giác", "visual qa",
  "route-shots", "screenshot từng route", "kiểm giao diện", "baseline diff", "UI có regression
  không", "test giao diện headless", "/visual-qa".
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.0.0"
  loop: dev-loop
  requires:
    bin: [node]
---

# Skill: visual-qa — workflow tự-kiểm thị giác (capture → diff → judge → fix → re-verify)

> **Vì sao tồn tại:** agent sửa UI rồi *tự khen* là sai lệch có hệ thống (failure
> `ui-pass-without-full-visual-review`). Ảnh chụp ra mà không ai mở = như chưa test. Workflow
> này thay "agent tự nhìn rồi tự cho pass" bằng **ba tầng kiểm độc lập**, trong đó hai tầng là máy.
>
> **Quyết định 13/07/26 (từ /last30days):** ngành chỉ có MỘT thứ đã chín cho UI-do-AI-sinh —
> **baseline snapshot + pixel diff** (`argos-ci/argos`: *"detects unintended visual changes"*;
> Playwright `toHaveScreenshot`). Tầng "LLM-judge chấm screenshot theo rubric" còn là biên giới
> (Agent-as-a-Judge, paper-stage) — nên ta **tự làm** tầng đó, không chờ ai.

## WHAT

### Purpose và context
- **Purpose:** thay "agent tự nhìn rồi tự cho pass" bằng ba tầng kiểm độc lập cho SPA local — baseline pixel-diff (máy), bất biến design/a11y (máy), đọc hết ảnh theo rubric (agent) — và chỉ pass khi máy VÀ mắt cùng sạch, có file ảnh làm bằng chứng.
- **Trigger (when to use):**
  - Vừa đổi theme / UI / rebrand và cần biết **có làm hỏng gì ngoài ý muốn không**.
  - Frame có `ui_role≠none` cần gate acceptance (xem skill `br` § Vòng tự-kiểm thị giác).
  - Extension browser không chụp được localhost (thường gặp) → headless CLI thay thế.
  - User nói "qa thị giác", "visual qa", "route-shots", "screenshot từng route", "kiểm giao diện", "baseline diff", "UI có regression không", "test giao diện headless", "/visual-qa".
- **Non-goals:** không dẫm `computer-use` (desktop AX / Orca browser); không phải verdict senior 4-mục (đó là `/qc-uiux`, dùng engine này); không nới ngưỡng để "hết lỗi".

### Mental model
`app chạy + route list THẬT + login → route-shots (ảnh + MANIFEST, mọi theme/state) → tầng 1 baseline diff (ngưỡng 0) → tầng 2 bất biến in-page (contrast-aa · monochrome-surface · rogue-slab · shadow-clipped · overlap · row-misalign) → tầng 3 đọc đủ N ảnh theo rubric → FINDINGS.md → sửa → chụp lại + đọc lại`.

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | app đang chạy (`--base`) | có | SPA localhost |
| In | route list từ router THẬT + tài khoản login | có | không đoán; login fail thì gate phải chết |
| In | danh sách theme/state từ chính app | có | không hardcode `light,dark` khi app có nhiều hơn |
| In | thư mục baseline | không | lần đầu tự tạo |
| Out | `<out>/*.png` + `MANIFEST.json` | có | không có file = CHƯA TỪNG CHỤP |
| Out | exit code với `--assert` | có cho gate | 1 khi route lỗi / thiếu ảnh / vi phạm bất biến / lệch baseline |
| Out | `FINDINGS.md` | có | một dòng cho MỖI route, kể cả "sạch" |

### Rules và capabilities
Luật rút từ máu — đừng lặp lại:
- RULE-01 (MUST): **THỨ GÌ TÍNH ĐƯỢC thì PHẢI để MÁY tính — cấm giao cho mắt.** Tương phản chữ là *con số* (WCAG ratio = f(màu chữ, màu nền)). Rubric ghi "chữ đạt AA" mà **không cài bất biến** ⇒ evaluator MÙ: chữ mờ lọt qua cả trang đăng nhập, agent nhìn ảnh cũng không hình dung nổi. **Tiêu chí nào định lượng được → phải thành assert, không phải thành dòng chữ trong rubric.**
- RULE-02 (MUST): **KHÔNG ROUTE NÀO ĐƯỢC LÀ VÙNG MÙ.** Driver login-trước ⇒ `/auth` redirect ⇒ **trang sign-in không bao giờ được audit** — đúng trang có lỗi. Phải chụp **trạng thái CHƯA đăng nhập** trước, rồi mới login. Rà lại: còn state nào (modal, error, empty, loading) chưa từng vào khung hình?
- RULE-03 (MUST): **THEME LÀ MỘT TRẠNG THÁI — chụp ĐỦ light VÀ dark.** App thường bật dark bằng class (`.dark` trên `<html>`) theo *setting app*, KHÔNG theo `prefers-color-scheme` ⇒ headless mặc định **chỉ bao giờ thấy light**, còn dark là vùng mù tuyệt đối: user mở app ở dark thấy UI vỡ mà gate vẫn xanh. Bật `--themes light,dark` (mặc định) → lần đầu chạy lòi ra **172 chỗ** trượt AAA ở dark trong khi light sạch bong. Hệ quả thiết kế: **accent phải LẬT theo theme** (mặt sáng → accent tối; mặt tối → accent sáng); một hằng số accent cho cả 2 theme là sai từ định nghĩa. Và **cấm hardcode màu chữ trên accent** (`color:#fff`) — ở theme kia thành trắng-trên-trắng 1.13:1.
- RULE-04 (MUST): **PHỦ *MỌI* THEME APP CUNG CẤP — danh sách lấy từ APP, không tự nghĩ.** Tôi hardcode `light,dark` trong khi app có **ba** theme (`default` / `default-dark` / `paper`) ⇒ `paper` không ai đụng ⇒ nó vỡ y hệt dark, **user tìm ra chứ không phải gate**. Luật: trước khi chạy, đọc danh sách theme từ chính app (dropdown Settings→Preferences / source `THEME_OPTIONS`) rồi phủ hết. Suy rộng: mọi TRỤC trạng thái (theme, locale, role, empty/full data) phải lấy từ app, không lấy từ trí nhớ của agent.
- RULE-05 (MUST): **ĐỔI TRẠNG THÁI PHẢI ĐI ĐÚNG ĐƯỜNG APP ĐỔI — rồi VERIFY nó đã đổi thật.** Sai 2 tầng liên tiếp: ① gắn class `.dark` bằng tay (app dùng `data-theme` + inject CSS ⇒ cơ chế KHÔNG TỒN TẠI); ② set `localStorage` (app GHI ĐÈ lại từ setting tài khoản trên server). Cả 2 lần gate XANH trên trạng thái **không có thật** — tệ hơn đỏ. Đường chắc chắn đúng là đường **người dùng bấm** (Settings → Preferences → chọn). Và luôn có bất biến: **hai theme khác nhau mà nền y hệt ⇒ ảnh GIẢ ⇒ ASSERT FAIL** (gate đang chụp cùng một theme hai lần rồi tự khen).
- RULE-06 (MUST): **THEME LÀ CƠ CHẾ CỦA APP, ĐỌC SOURCE TRƯỚC.** Đừng giả định `.dark` / `prefers-color-scheme`. Grep `documentElement.classList` / `data-theme` / `localStorage` / inject `<style>` để biết app đổi theme bằng gì; theme thường nạp bằng **CSS inject lúc chạy** ⇒ nó THẮNG file theme tĩnh của mình ở token thường, nhưng THUA rule `!important` ⇒ ra giao diện **nửa nạc nửa mỡ** (nền theme-app + card theme-mình = mảng màu lạ giữa trang). Sửa đúng: viết bảng màu của mình **vào chính file theme mà app inject**, không viết block `.dark{}` ở nơi app không bao giờ đọc.
- RULE-07 (MUST): **LOGIN HỎNG = GATE PHẢI CHẾT.** Login fail ⇒ mọi route redirect `/auth` ⇒ driver audit **8 bản sao trang sign-in** rồi in "design-ok". Xanh kiểu đó tệ hơn đỏ: nó xác nhận một app mà nó chưa từng nhìn thấy. `--assert` fail ngay khi login fail.
- RULE-08 (MUST): **USER BÁO LỖI + MÁY BÁO SẠCH ⇒ MÁY SAI, KHÔNG PHẢI USER SAI.** (bài học 14/07/26 — user: *"đây là developing không phải toà án mà bảo vệ luận điểm của mình khăng khăng như vậy"*.) Gate xanh KHÔNG phải lá chắn: nó chỉ chứng minh **cái nó được dạy**, trên **state nó chụp được**. User thấy lỗi = tồn tại một state/theme/bundle mà gate chưa từng vào. **Cấm phản biện user bằng suy đoán** ("chắc do cache", "chắc bấm nhầm phím") — mỗi lần đoán là đẩy việc kiểm chứng sang cho user, và tôi đã sai 3 lần liên tiếp kiểu đó. Đúng quy trình: (1) tin báo cáo, (2) tái hiện ĐÚNG state của user (route + theme + bundle + trạng thái đăng nhập/focus), (3) chỉ nói khi đã ĐO. Không tái hiện được thì nói thẳng "chưa tái hiện được", đừng dựng giả thuyết rồi bảo vệ nó.
- RULE-09 (MUST): **KHỬ NGẪU NHIÊN TRƯỚC KHI CHỤP, ĐỪNG NỚI NGƯỠNG.** Con trỏ nhấp nháy + animation làm **mọi** route lệch baseline ~0.04% mỗi lần chụp ⇒ gate đỏ vĩnh viễn ⇒ bị phớt lờ ⇒ regression thật lọt qua. Driver tiêm CSS `animation/transition:none; caret-color:transparent` + ẩn con trỏ CodeMirror ngay lúc init ⇒ diff về **0%**. Nới `--diff-threshold` để "hết kêu" là **làm mù máy**, không phải sửa lỗi.
- RULE-10 (MUST): **SELECTOR THAM LAM = TỰ BẮN VÀO CHÂN.** `[class*="cursor"]` trong CSS khử-nhiễu trúng luôn `cursor-pointer`/`cursor-text` của Tailwind ⇒ **ẩn mất ô nhập ⇒ login chết ⇒ gate tự làm hỏng app nó đang kiểm**. Mọi CSS/selector do gate tiêm vào phải **hẹp nhất có thể** và phải chạy thử full-flow (login → mọi route) sau khi thêm.
- RULE-11 (MUST): **GATE PHẢI CHẠY ĐƯỢC TỪ REPO SẠCH.** Thiếu `playwright-core` ⇒ `node route-shots.mjs` chết ngay dòng import ⇒ acceptance_test của frame UI **không bao giờ chạy** = gate chết mà không ai biết. Deps khai trong `skills/visual-qa/assets/package.json`; cài: `npm i --prefix skills/visual-qa/assets`.
- RULE-12 (MUST): **BẰNG CHỨNG > LỜI.** Pass/fixed chỉ hợp lệ khi có FILE ẢNH. Không file = chưa làm. Cấm khai pass bằng suy luận.
- RULE-13 (MUST): **ĐỌC HẾT, không chọn lọc.** Đọc 3/7 ảnh rồi kết luận là nguyên nhân gốc của failure `ui-pass-without-full-visual-review` — lỗi nằm sẵn trong ảnh chưa mở.
- RULE-14 (MUST): **"Máy OK" ≠ "UI đẹp".** Bất biến chỉ biết những gì nó được dạy. Gate xanh KHÔNG phải cớ để bỏ bước đọc ảnh.
- RULE-15 (MUST): **NGƯỠNG là con dao hai lưỡi.** Ngưỡng lỏng → lọt lỗi thật (0.5% diff bỏ lọt một regression làm phẳng toàn bộ card). Ngưỡng chặt quá → kêu oan → **gate noisy = gate CHẾT**. Baseline dùng ngưỡng 0 + duyệt tay; bất biến DOM phải có ngưỡng phân biệt lỗi thật với nhiễu.
- RULE-16 (MUST): **CSS thì ĐO, đừng ĐOÁN.** Chẩn đoán bằng mắt sai 4 lần liên tiếp (clip → collision → sai selector → sai specificity). Chỉ khi query `getComputedStyle` mới ra gốc. Trước mọi fix CSS: **đo computed style + đo rect**, rồi mới sửa. Sau khi sửa: **đo lại** trước khi nhìn ảnh.
- RULE-17 (MUST): **Đừng làm MÙ máy để "hết lỗi".** Hạ blur xuống dưới ngưỡng detector = che lỗi, không sửa lỗi (aura vẫn bị crop). Sửa defect, đừng sửa thước đo.
- RULE-18 (MUST): **Trong container `overflow:hidden` (rail hẹp, tab bar): KHÔNG dùng bóng outset.** Nó sẽ bị cắt hoặc đổ vào khe → vệt xấu. Dùng **inset** (không thể tràn) hoặc bỏ bóng. `overflow-x:visible` KHÔNG khả thi khi trục kia là `auto` (CSS ép về auto).
- RULE-19 (MUST): **playwright-core + Chrome hệ thống** (không tải chromium 130MB). Baseline diff cần `pixelmatch` + `pngjs` (nhỏ, không có thì tự bỏ qua baseline).
- RULE-20 (MUST): **`networkidle` cấm với SPA realtime** — dùng `domcontentloaded` + chờ cố định.
- RULE-21 (MUST): **Không dẫm `computer-use`** (desktop AX / Orca browser). Skill này là headless CLI cho SPA localhost.
- Capabilities: chạy trình duyệt headless trên localhost; đo computed style + rect in-page; so pixel với baseline; ghi ảnh/manifest/findings; sửa UI dự án đích.

### Failure boundaries
- Login fail → `--assert` **failed** ngay, không audit bản sao trang sign-in.
- Thiếu `playwright-core` → gate chết từ dòng import: **blocked**, cài `npm i --prefix skills/visual-qa/assets`.
- Lệch baseline ≠ 0 → **failed** tới khi người xem + duyệt bằng `--update-baseline`.
- User báo lỗi mà máy báo sạch → máy sai: tái hiện đúng state; chưa tái hiện được thì nói thẳng "chưa tái hiện được".
- Máy sạch nhưng chưa đọc đủ N ảnh → **chưa xong**.

## HOW

### Main workflow
W01–W07 ứng với bước 0–6 bên dưới.

| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W01 | deterministic | app, router, tài khoản | Xác nhận app chạy, lấy route list THẬT + theme list từ app | route + theme list | app không chạy → blocked |
| W02 | effect | route list | Chụp bằng `route-shots.mjs` (+ `--assert`) | ảnh + `MANIFEST.json` | login fail → failed |
| W03 | deterministic | ảnh + baseline | Baseline diff ngưỡng 0 | diff | ≠ 0 → xem + duyệt (B02) hoặc sửa |
| W04 | deterministic | trang in-page | Bất biến máy-kiểm | vi phạm hoặc sạch | FAIL cứng → W06 |
| W05 | judgment | MANIFEST N route | `Read` đủ N ảnh, chấm theo rubric | dòng cho mỗi route | thiếu ảnh chưa đọc → chưa xong |
| W06 | effect | findings | `FINDINGS.md` (nguyên nhân GỐC) → sửa | code đã sửa | — |
| W07 | deterministic | code đã sửa | Chụp lại → đọc lại | máy sạch VÀ mắt sạch | còn lỗi → W06 |

Chi tiết từng bước (nguồn chân lý cho W01–W07):

**0. App phải đang chạy.** Biết route list (lấy từ router THẬT, không đoán) + tài khoản login.

**1. CHỤP + BẰNG CHỨNG.**
```bash
node skills/visual-qa/assets/route-shots.mjs \
  --base http://localhost:5230 --out <dir>/qa-shots \
  --baseline <dir>/qa-baseline \
  --user demo --pass demo --assert
```
Sinh `<out>/*.png` + **`MANIFEST.json`** (route → file → bytes). Không có file = **CHƯA TỪNG CHỤP**.

**2. BASELINE DIFF (máy tầng 1) — bắt thay đổi NGOÀI Ý MUỐN.**
Lần đầu tự tạo baseline. Lần sau so pixel-by-pixel. **Ngưỡng mặc định = 0**: mọi diff ≠ 0 đều
FAIL và phải được xem + duyệt tay bằng `--update-baseline`. Đây là tầng duy nhất bắt được loại
lỗi mà bất-biến-CSS và mắt agent đều MÙ (vd: sửa quá tay làm phẳng cả UI).

**3. BẤT BIẾN MÁY-KIỂM (máy tầng 2) — design conformance + a11y.**
Chạy in-page bằng computed style:
- `contrast-aa` — **WCAG AAA cho MỌI text node** (tính tỉ lệ tương phản từ màu chữ + nền hiệu dụng; 7:1 thường, 4.5:1 chữ lớn). **FAIL cứng.**
- `monochrome-surface` — pane lớn (sidebar/aside/nav) phải cùng màu nền. **FAIL cứng.**
- `rogue-slab` — **MỌI** phần tử ≥2% viewport có nền đục lệch nền body > 1.6:1. **FAIL cứng.**
  (`monochrome-surface` chỉ soi sidebar/aside/nav ⇒ mù với mảng màu lạ là `<div>` bất kỳ giữa trang.)
- `shadow-clipped` — aura outset trong cha `overflow:hidden` (có ngưỡng blur). Cảnh báo.
- `overlap` — hai control (`button/a/input/[role=button]`) KHÔNG phải cha-con mà rect chồng ≥4px cả hai chiều. Bắt lỗi **nút đè lên nhau** (vd `position:fixed` với magic-offset lúc badge rộng biến thiên). **FAIL cứng.**
- `row-misalign` — control cùng cha, gần cùng hàng (top lệch ≤6px) mà **chiều cao lệch >3px**. Bắt lỗi **nút cạnh nhau không bằng chiều cao** (vd nút toggle cao hơn badge do padding/font khác). **FAIL cứng.**
  (Hai rule này thêm 15/07/26 vì cả `/redesign-existing-projects` [đọc CSS TĨNH — không đo được rect] lẫn unit-test [kiểm NỘI DUNG, không kiểm toạ độ] đều mù với lỗi hình học lúc render. Ngưỡng overlap CỐ Ý không dùng %-diện-tích: bug thật chỉ clip mép nút = 18% dt, mọi ngưỡng % đều lọt — 2 control độc lập chồng ≥ vài px đã là lỗi.)

Mở rộng bất biến theo design spec của dự án.

**4. ĐỌC ẢNH — COVERAGE CỨNG + RUBRIC (tầng người/agent).**
MANIFEST có N route → **PHẢI `Read` đủ N ảnh**. FINDINGS phải có **một dòng cho MỖI route**
(kể cả "sạch"). Chấm theo **rubric**, không cảm tính — vd neumorphism: ① mặt đơn sắc ② bóng
không bị cắt ③ CTA phẳng accent ④ chữ/icon AA ⑤ empty-state đúng brand ⑥ focus ring.

**5. FINDINGS.md → SỬA.** Bảng `# · route · vấn đề · mức · **nguyên nhân GỐC** · cách sửa`.

**6. CHỤP LẠI → ĐỌC LẠI → mới pass.** Máy sạch **VÀ** mắt sạch. Thiếu một trong hai = chưa xong.

### Branches
| ID | Kind | Guard | Hành vi | Skip / failure | Rejoin |
|---|---|---|---|---|---|
| B01 | conditional_required | frame gate chỉ cần 1 route | chạy `--route <r>` | — | W03 |
| B02 | user_optional | lệch baseline là thay đổi CỐ Ý đã xem | `--update-baseline` | chưa xem ảnh → không được duyệt | W04 |
| B03 | capability_optional | có `pixelmatch` + `pngjs` | chạy baseline diff | không có → tự bỏ qua baseline | W04 |
| B04 | recovery | user báo lỗi mà gate xanh | tái hiện ĐÚNG state (route + theme + bundle + đăng nhập/focus), đo rồi mới nói | không tái hiện được → nói thẳng | W02 |

### Validation và stopping
Máy: exit code `--assert` (route lỗi / thiếu ảnh / bất biến / baseline). Mắt: FINDINGS có đủ một dòng cho mỗi route trong MANIFEST. Pass chỉ khi cả hai sạch VÀ có file ảnh; không có file = chưa làm.

### Examples
- **Positive:** đổi theme app `/br` sinh, 7 route × 3 theme từ `THEME_OPTIONS` → `route-shots.mjs --assert` exit 0, baseline diff 0%, agent `Read` đủ ảnh, FINDINGS 7 dòng "sạch" → pass kèm ảnh.
- **Boundary/failure:** light sạch nhưng chưa phủ dark → bật `--themes light,dark` lòi ra 172 chỗ trượt AAA → `--assert` exit 1; sửa accent lật theo theme rồi chụp lại, không nới `--diff-threshold`.

### Reference — Cờ driver
`--base` `--out` `--user` `--pass` · `--route <r>` (1 route, cho frame gate) · `--assert`
(exit 1 khi: route lỗi / thiếu ảnh / vi phạm bất biến / lệch baseline) · `--baseline <dir>` ·
`--update-baseline` (duyệt thay đổi cố ý) · `--diff-threshold <%>` (mặc định 0).
