---
name: diagram
description: >-
  Vẽ SƠ ĐỒ và BIỂU ĐỒ bằng máy, không để model tự bịa hình. Gọi khi user nói —
  tiếng Việt "vẽ sơ đồ", "vẽ biểu đồ", "vẽ luồng", "sơ đồ kiến trúc", "sơ đồ hệ thống",
  "sơ đồ quy trình", "luồng xử lý", "flow", "graph", "đồ thị", "biểu đồ", "chart",
  "trực quan hoá", "visualize", "mô hình hoá", "vẽ hộ", "diagram hoá", "chuyển mô tả
  thành hình", "so sánh hai luồng"; tiếng Anh "draw a diagram", "architecture diagram",
  "workflow diagram", "sequence diagram", "data flow", "state machine", "lifecycle",
  "dependency graph", "org chart", "chart", "plot", "dashboard", "visualize this",
  "turn this into a diagram", "convert Mermaid", "diff two flows". Bao cả hai họ —
  sơ đồ QUAN HỆ/LUỒNG (hộp + mũi tên) và biểu đồ DỮ LIỆU (số liệu). KHÔNG dùng cho
  màn hình UI/landing page — đó là `hallmark`.
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.0.0"
  loop: utils
  requires:
    harness: ">=1.3.127"
    bin: [python3]
    scripts: [fdk/tools/frontend-antipattern.py, fdk/tools/visual-receipt.py]
    framework_scripts: [fdk/tools/build-overstack-docs.py]
---

# diagram — vẽ đúng bằng máy, không để model bịa hình

Nguyên tắc trung tâm, mượn của `archify` và giữ nguyên vì nó đúng: **model KHÔNG vẽ**.
Model chỉ điền logic vào một tờ khai có schema (có những khối nào, khối A nối khối B ra sao).
Việc dựng hình là của **code tất định**. Vẽ xong, máy tự soi lại bố cục; hỏng thì **giữ nguyên
bản tốt trước đó** và nói rõ chỗ sai, tuyệt đối không nhả ra một hình rác.

Đó cũng là lý do skill này tồn tại thay vì để model tự vẽ SVG: một cái hình sai trông vẫn
"có vẻ được", nên lỗi bố cục là loại lỗi đi lọt xa nhất.

## WHAT

### Purpose và context
- **Purpose:** vẽ SƠ ĐỒ (quan hệ/luồng) và BIỂU ĐỒ (số liệu) bằng code tất định — model chỉ điền tờ khai có schema, máy dựng hình và tự soi bố cục; hỏng thì giữ bản tốt trước đó và nói rõ chỗ sai.
- **Trigger (when to use):** user nói "vẽ sơ đồ", "vẽ biểu đồ", "vẽ luồng", "sơ đồ kiến trúc", "luồng xử lý", "flow", "graph", "chart", "trực quan hoá", "so sánh hai luồng", "draw a diagram", "sequence diagram", "state machine", "dependency graph", "plot", "dashboard", "convert Mermaid", "diff two flows" (danh sách đủ ở `description`).
- **Non-goals:** KHÔNG dùng cho màn hình UI/landing page — đó là `hallmark`. Không vẽ tay toạ độ SVG cho hình mới. Không thay generator cho sơ đồ trong tài liệu tự sinh.

### Mental model
`câu hỏi người xem → có TRỤC SỐ? → Sơ đồ (ngữ pháp → archify) hoặc Biểu đồ (dataviz + 5 luật lieflat) → file HTML → cổng nhà (frontend-antipattern, tuỳ chọn visual-receipt) → giao nguyên tử (xanh mới thay, đỏ giữ bản cũ)`. Model điền logic; code dựng hình; cổng tất định quyết đạt/không.

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | mô tả luồng/quan hệ hoặc số liệu | có | câu hỏi người xem cần trả lời |
| In | loại sơ đồ | không | `architecture`, `workflow`, `sequence`, `dataflow`, `lifecycle`; bỏ trống thì engine đoán |
| In | Mermaid có sẵn | không | dán vào, archify vẽ lại |
| In | neo mã thật | không | `sources[]` + `meta.repository` + `--repo-root` (SHA đủ 40 ký tự) |
| Out | file HTML tự chứa | có | sơ đồ hoặc biểu đồ, qua cổng nhà |
| Out | verdict cổng | có | rc của `frontend-antipattern.py` (0 sạch, 1 FAIL, 2 chỉ WARN); tuỳ chọn `visual-receipt.py` (0 pass, 1 fail, 2 BỎ QUA) + 4 ảnh + biên lai JSON + contact sheet |

### Rules và capabilities
- RULE-01 (MUST): **Model không vẽ.** Model điền tờ khai; code dựng hình. Thấy mình đang gõ toạ độ SVG bằng tay cho một hình mới là đã đi sai nhánh.
- RULE-02 (MUST): **Không nhả hình rác.** Bản mới không qua cổng thì giữ bản tốt cũ, báo rõ chỗ sai. Generator của repo này đã làm đúng vậy (`_deliver` trong `build-overstack-docs.py`: render ra file tạm, chạy cổng trên file tạm, xanh mới `os.replace`).
- RULE-03 (MUST): **BỎ QUA ≠ SẠCH.** Thiếu Chrome, thiếu mạng, thiếu engine → nói "bỏ qua", tuyệt đối không báo "đạt". Một cổng nói dối mà vẫn xanh tệ hơn không có cổng.
- RULE-04 (MUST): **Đừng bê ràng buộc phong cách của engine ngoài về làm luật nhà.** Đo trước: archify đòi mũi tên thẳng ngang/dọc, nhưng sơ đồ của repo này cố ý toả nan quạt (6·4·10 đường chéo hợp lệ ở ba sơ đồ) — nên luật đó bị loại khi hấp thụ, còn ba luật hình học kia thì nhận.
- RULE-05 (MUST): **Sơ đồ trong tài liệu tự sinh thì dùng generator, đừng gọi agent.** Mỗi sơ đồ vẽ qua chat tốn một lượt agent, mãi mãi; code sinh SVG tốn 0. Chỉ dùng nhánh chat cho hình mới hoặc hình dùng một lần.
- Capabilities: gọi engine vẽ sơ đồ tất định và engine biểu đồ; chạy cổng tĩnh 0-token trên file HTML; tuỳ chọn chạy trình duyệt thật chụp + đo request; ghi file đích theo giao nguyên tử.

### Failure boundaries
- Không rõ có trục số hay không → **clarify** (hỏi "cái tôi vẽ có TRỤC SỐ không?").
- Yêu cầu là màn hình sản phẩm → **blocked**, chuyển `hallmark`.
- Biểu đồ vi phạm kỷ luật (cắt trục, glow/3-D trên data mark, dữ liệu quá mỏng) → **từ chối/hạ cấp** có lý do, đưa phương án trung thực.
- `deliver` đỏ hoặc cổng FAIL → **failed**, file đích vẫn là bản tốt CŨ; báo chỗ sai.
- Thiếu Chrome/mạng/engine → **BỎ QUA**, không bao giờ báo "đạt" (RULE-03).
- Neo mã sai (SHA không đủ 40 ký tự, `origin` không khớp) → **blocked** (fail-closed).

## HOW

### Main workflow
| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W01 | judgment | yêu cầu | Chọn nhánh: có TRỤC SỐ → Biểu đồ; không → Sơ đồ; màn hình → `hallmark` | nhánh | UI → blocked; mơ hồ → clarify |
| W02 | judgment | câu hỏi người xem | Sơ đồ: chọn NGỮ PHÁP (topology, sequence, process, state, hierarchy, matrix); một câu hỏi một hình | archify type | hai câu hỏi → hai hình |
| W03 | effect | tờ khai | Sơ đồ: gọi archify bằng ngôn ngữ tự nhiên hoặc `node ~/.agents/skills/archify/bin/archify.mjs` (B01) | file HTML | rc 1 → failed, bản cũ giữ nguyên |
| W04 | effect | số liệu | Biểu đồ: nạp `dataviz` trước dòng code đầu tiên + 5 luật lieflat (B02) | file HTML | vi phạm kỷ luật → từ chối/hạ cấp |
| W05 | deterministic | file HTML | Cổng nhà `python3 fdk/tools/frontend-antipattern.py <file.html>` | rc 0 | 1 → sửa tờ khai, lặp W03/W04 |
| W06 | deterministic | file HTML | Tuỳ chọn bằng chứng trình duyệt `python3 fdk/tools/visual-receipt.py <file.html>` (B03) | ảnh + biên lai | 2 → báo BỎ QUA, không báo đạt |
| W07 | effect | file đã qua cổng | Giao nguyên tử: xanh mới thay file đích; đỏ giữ bản tốt cũ + báo chỗ sai | file đích | — |

Chi tiết từng bước (nguồn chân lý cho W01–W07):

#### Chọn nhánh trước khi làm bất cứ gì

| Bạn đang thể hiện cái gì | Nhánh | Engine |
|---|---|---|
| Quan hệ / luồng / trình tự giữa các thành phần (hộp + mũi tên) | **Sơ đồ** | `archify` |
| Số liệu — so sánh, phân bố, xu hướng, tỉ trọng | **Biểu đồ** | `dataviz` + kỷ luật lieflat dưới đây |
| Một màn hình sản phẩm | **không phải việc ở đây** | `hallmark` |

Không chắc? Hỏi: *"cái tôi vẽ có TRỤC SỐ không?"* Có → biểu đồ. Không → sơ đồ.

##### Trong nhánh Sơ đồ — chọn đúng NGỮ PHÁP trước khi chọn engine

Hỏi trước: *người xem phải trả lời được câu hỏi gì?* — câu hỏi quyết ngữ pháp, ngữ pháp
mới quyết hình vẽ ra sao (HÒA TAN từ `plannotator/effective-html`, xem [[design-foundation]]):

| Câu hỏi của người xem | Ngữ pháp | Ví dụ archify type |
|---|---|---|
| Có gì, nối với gì? | Topology / sơ đồ hệ thống | `architecture` |
| Chuyện gì xảy ra theo thời gian? | Sequence / timeline | `sequence` |
| Quyết định/biến đổi diễn ra thế nào? | Process flow | `workflow` |
| Cái này đổi trạng thái ra sao? | State diagram | `lifecycle` |
| Cái gì chứa/sở hữu cái gì? | Hierarchy / containment | `architecture` (nhánh lồng) |
| Các phương án so sánh nhau thế nào? | Matrix / so sánh căn hàng | bảng, không cần archify |
| Bao nhiêu / thường xuyên / nhanh cỡ nào? | Biểu đồ định lượng | → nhánh **Biểu đồ** bên dưới |

Đừng nhồi hai câu hỏi vào một hình. Cần cả hai → hai hình (hoặc lớp bật/tắt), không phải
một hình quá tải. Chọn xong ngữ pháp mới tới bước chọn engine (HTML/CSS, SVG, Canvas, WebGL)
theo mục dưới.

#### Nhánh SƠ ĐỒ — qua `archify`

Engine ngoài, KÉO NGOÀI theo `[[adapt-modes]]`: ta **không** viết lại, chỉ ghim + gọi.
Cài: `npx skills add Rheinmir/archify -g -s archify` (đích thật là `~/.agents/skills/archify`).
Đây là **fork** của `tt-a1i/archify`: thêm preset thứ 5 `macos` (liquid glass + Roboto) và đặt
làm **mặc định** — bỏ trống `meta.visual_preset` là ra đúng theme của nhà, không phải áp thêm
bước nào. Nhánh vá `macos-roboto` là nhánh MẶC ĐỊNH của fork, nên không cần ghim ref.

Hai cái bẫy đã trả giá, đừng lặp lại:

- **Không có cờ `--ref`.** Và `owner/repo@nhánh` KHÔNG ghim được nhánh lúc cài: CLI in ra
  `Source: …git @macos-roboto` nhưng vẫn cài nhánh mặc định, đồng thời hiểu phần sau `@` là
  TÊN SKILL nên báo `No matching skills found`. Đó là lý do pin bằng default-branch, không
  bằng cú pháp.
- **`-l` không thay được cài thật.** `add … -l` báo `Found 1 skill` xanh trong khi lệnh cài
  thật vẫn hỏng. Kiểm đường cài phải cài thật rồi vẽ một sơ đồ, xem `data-preset` ra gì.

Upstream ra bản mới thì rebase nhánh, đừng cài đè bằng `tt-a1i/archify`.

Gọi bằng ngôn ngữ tự nhiên trong chat — **không có prefix lệnh**:

```text
Use Archify to draw: Browser -> API -> Redis cache -> PostgreSQL fallback.
```

Nói rõ LOẠI thì khỏi phải đoán — `architecture` · `workflow` · `sequence` · `dataflow` ·
`lifecycle`. Dán Mermaid có sẵn vào cũng được, nó vẽ lại cho đẹp.

Ba điều phải biết trước khi gọi, đã kiểm chứng bằng cách chạy thật:

1. Package đặt `"private": true` — **không có trên npm**. `npx archify` không chạy. Mọi lệnh
   shell đều là `node ~/.agents/skills/archify/bin/archify.mjs …`.
2. **Mã thoát không theo quy ước 0/1**: `2` vừa là lỗi cách dùng (lệnh lạ, cờ lạ, kiểu sơ đồ
   lạ) **vừa là** "visual-check bỏ qua vì không có Chrome". `1` mới là thất bại thật của
   validate/render/deliver. Gọi trong CI phải rẽ nhánh có chủ đích.
3. Sau một `deliver` ĐỎ, **đừng đi soi file đích** — nó vẫn là bản tốt CŨ, không phải bản vừa
   hỏng. Đây là hệ quả trực tiếp của giao-nguyên-tử, không phải lỗi.

Riêng `lifecycle`, ba luật nằm trong code chứ không nằm trong schema — đo 10/09/2026,
đã vá ở fork nên bản cài mới mới có:

- **Tên lane là hợp đồng.** `main` → dải trên, **`terminal`** → dải dưới (Outcomes), mọi id
  khác dồn chung dải giữa. Đặt tên khác (`outcome`, `recover`, …) là rơi vào dải giữa và
  đè lên nhau — đây là chỗ đã đốt 4 vòng bố cục.
- **Hai sàn chiều cao khác nhau.** Không dùng dải terminal → `viewBox[1] ≥ 510`; có dùng →
  `≥ 630`. Trước bản vá cả hai đều báo 566, nên khai `terminal` ở 566 là rơi vào vòng lặp
  "State exceeds the vertical lifecycle area" không lối ra.
- **Rail chính KHÔNG tự thành quan hệ.** Thứ tự `step` chỉ vẽ đường; muốn Route Probe /
  passport / trace thấy được thì phải khai transition thật (bỏ nhãn nếu khe hẹp). Bấm một
  node rồi đọc Semantic Passport: thấy `No connected relationships` là sơ đồ rỗng ruột dù
  validate/visual-check đều xanh.

Sơ đồ kiến trúc cần bám mã thật thì khai `sources[]` (path + khoảng dòng) + `meta.repository`
+ `--repo-root`. Cổng đó **fail-closed**: revision phải là SHA đủ 40 ký tự, `--repo-root` phải
là top-level checkout có `origin` khớp. Neo sai thì nó từ chối vẽ.

#### Nhánh BIỂU ĐỒ — `dataviz` + kỷ luật lieflat-charts

Nạp skill `dataviz` **trước khi viết dòng code biểu đồ đầu tiên**, ở mọi môi trường (HTML,
SVG, matplotlib/plotly/d3/Recharts, hay ảnh PNG sẽ render). Cộng năm luật hấp thụ từ
`lieflat-charts`, tất cả **đứng trên thẩm mỹ**:

1. **Từ chối là hành vi ĐÚNG, không phải bướng.** Cắt trục (broken axis) → từ chối, đưa ba
   cách trung thực. Glow / glassmorphism / 3-D trên data mark → từ chối. Hơn sáu category mà
   vẫn đòi màu → lùi về thang mono. Dữ liệu quá mỏng cho hình đã chọn (ba node mà đòi force
   graph) → hạ cấp và nói vì sao.
2. **Số hình = số KẾT LUẬN độc lập**, không phải số cột dữ liệu. Một câu hỏi → một hình; cả
   một bài viết → bốn tới sáu; trần sáu hình một trang rồi tách trang.
3. **Tiêu đề là KẾT LUẬN**, không phải tên kiểu hình. "Churn tăng gấp đôi sau bản tháng Tư",
   không phải "Biểu đồ cột churn".
4. **Trưng bằng chứng chọn hình.** Nêu ít nhất ba ứng viên và lý do loại từng cái TRƯỚC khi
   vẽ. "Tôi dùng biểu đồ cột" mà không có ứng viên nào bị loại nghĩa là chưa hề chọn.
5. **Render tất định.** Cấm `Math.random()` trong biểu đồ — refresh hai lần phải ra đúng một
   hình. Cả file một hệ màu; trộn hai hệ là làm lại.

#### Sau khi có file HTML — chạy cổng của NHÀ

Engine ngoài gác bố cục của nó; cổng dưới đây gác thứ nó không biết: quy ước của repo này.

```bash
python3 fdk/tools/frontend-antipattern.py <file.html>     # 0 sạch · 1 FAIL · 2 chỉ WARN
```

Nó bắt, tất định và 0 token:

- **Hình học** — hai ô đè nhau một phần, ô nằm ngoài `viewBox`, chữ tràn ra ngoài ô chứa nó.
- **Accessibility + tự chứa** — thiếu `role="img"`, thiếu `<title>` hoặc `<title>` không phải
  con đầu, `<title>`/`<desc>` rỗng, và **tham chiếu remote `http`** (trang tự-chứa mà mở
  offline lại khuyết hình).
- **Neo bằng chứng** — node khai `data-src="path"` / `data-src="path:line"` mà đường dẫn không
  resolve, hoặc số dòng vượt độ dài file. Fail-closed: không khai thì không bị hỏi, đã khai thì
  phải đúng.

Cần bằng chứng trình duyệt thật (không phải chỉ phân tích tĩnh):

```bash
python3 fdk/tools/visual-receipt.py <file.html>           # 0 pass · 1 fail · 2 BỎ QUA
```

Ra bốn ảnh (1440×900 và 2048×1320, mỗi cỡ sáng + tối), một biên lai JSON, và một contact
sheet để **người** chấm. Nó kiểm trong trình duyệt thật ba thứ regex không làm được: tràn
ngang, lỗi console, và **mọi request thoát ra ngoài** — tức tính tự-chứa đo bằng hành vi chứ
không bằng chuỗi trong file.

### Branches
| ID | Kind | Guard | Hành vi | Skip / failure | Rejoin |
|---|---|---|---|---|---|
| B01 | conditional_required | không có trục số (quan hệ, luồng, trình tự) | nhánh Sơ đồ qua archify (KÉO NGOÀI, fork `Rheinmir/archify`) | archify chưa cài → cài `npx skills add Rheinmir/archify -g -s archify`; exit 2 do thiếu Chrome → BỎ QUA, không đạt | W05 |
| B02 | conditional_required | có trục số | nhánh Biểu đồ qua `dataviz` + 5 luật lieflat | yêu cầu vi phạm luật → từ chối, đưa ba cách trung thực | W05 |
| B03 | capability_optional | cần bằng chứng trình duyệt thật và có Chrome | `visual-receipt.py`: 4 ảnh, biên lai JSON, contact sheet cho người chấm | không Chrome → rc 2 BỎ QUA | W07 |
| B04 | user_optional | sơ đồ kiến trúc phải bám mã thật | khai `sources[]` + `meta.repository` + `--repo-root` | neo sai → engine từ chối vẽ (fail-closed) | W03 |
| B05 | conditional_required | sơ đồ nằm trong tài liệu tự sinh | dùng generator của repo (vd `build-overstack-docs.py`), không gọi agent | hình mới hoặc dùng một lần → nhánh chat | W05 |

### Validation và stopping
Tất định: rc của `frontend-antipattern.py` (hình học, accessibility + tự chứa, neo `data-src`) và `visual-receipt.py` (tràn ngang, lỗi console, request ra ngoài); với archify, rc 1 là thất bại thật, rc 2 vừa là lỗi cách dùng vừa là visual-check bỏ qua nên phải rẽ nhánh có chủ đích. Cần người: contact sheet của visual-receipt; với `lifecycle` bấm node đọc Semantic Passport, thấy `No connected relationships` là rỗng ruột dù cổng xanh. Dừng khi cổng xanh và file đích đã thay; đỏ thì giữ bản cũ và báo.

### Examples
- **Positive:** "vẽ luồng Browser -> API -> Redis cache -> PostgreSQL fallback" → không trục số → Sơ đồ, ngữ pháp topology → `Use Archify to draw: Browser -> API -> Redis cache -> PostgreSQL fallback.` → `frontend-antipattern.py` rc 0 → giao file HTML preset `macos`.
- **Boundary/failure:** "vẽ biểu đồ doanh thu, cắt trục cho thấy tăng mạnh" → nhánh Biểu đồ, broken axis bị từ chối (luật lieflat 1), đưa ba cách trung thực; tiêu đề là kết luận, không phải "Biểu đồ cột doanh thu".
- **Boundary:** lifecycle đặt lane `outcome` → rơi dải giữa đè nhau → đổi thành `terminal` và `viewBox[1] ≥ 630`; nếu `deliver` vẫn đỏ thì file đích là bản tốt cũ, không soi nó như bản mới.

## Origin

- Nhánh sơ đồ: `Rheinmir/archify` @ `macos-roboto` (KÉO NGOÀI — fork của `tt-a1i/archify`;
  engine sống ngoài, ta ghim + gọi). Xem `sources/draft/080926-archify-fork-pin.md`.
- Kỷ luật biểu đồ: `larashero3-dotcom/lieflat-charts` (HÒA TAN — chỉ lấy luật, không lấy bộ vẽ).
- Cổng hình học + giao nguyên tử: hấp thụ từ archify vào `fdk/tools/frontend-antipattern.py`
  và `fdk/tools/build-overstack-docs.py`, xem `wiki/sources/draft/040926-absorb-round.md`.
