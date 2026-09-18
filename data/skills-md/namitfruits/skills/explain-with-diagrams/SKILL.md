---
name: explain-with-diagrams
description: Giải thích một cơ chế, một bug, một luồng quyết định hay một kiến trúc bằng sơ đồ mermaid nền tối, màu theo ngữ nghĩa, kèm link mermaid.live/edit mở được ngay — hai mode — `easy` (mặc định) giải thích bằng ví von ứng 1-1 theo khuôn *một câu → ví von → chuyện thật diễn ra thế nào*, `tech` (`--tech`) gọi đúng tên file/hàm/field theo khuôn `Context` · `Problem` · `Root cause`. Chỉ giải thích hiện tượng, không đề xuất cách sửa; không dán nguồn mermaid vào chat. Dùng khi user nói "vẽ sơ đồ", "diagram hoá", "mermaid", "vẽ cho dễ hiểu", "mô tả bằng sơ đồ", khi user hỏi "tại sao X" mà câu trả lời có nhiều tầng / nhiều nhánh / nhiều trạng thái, hoặc khi đã giải thích bằng chữ mà user vẫn chưa nắm được. Kèm `mermaid-link.mjs` sinh link offline + verify round-trip.
---

# Giải thích bằng sơ đồ

## Mental model

**Hình mang cấu trúc. Câu trả lời mang lời giải.** Hai thứ này không đổi chỗ cho nhau được:

- Hình trả lời *"có những gì, nối với nhau ra sao, đi theo thứ tự nào"*.
- Chữ trả lời *"vì sao lại thế, chỗ nào đáng nhìn, cái gì không đọc ra được từ hình"*.

Nhét lời giải vào trong hình thì hình thành một trang văn bản có viền, và người đọc mất đúng cái mà
sơ đồ sinh ra để cho: **nhìn một phát thấy hình dạng**.

Một sơ đồ đáng vẽ khi câu trả lời có **nhiều tầng**, **nhiều nhánh**, hoặc **thứ tự ưu tiên**. Ba cái
đó viết bằng văn xuôi thì người đọc phải tự dựng hình trong đầu. Còn một danh sách phẳng, một bảng
so sánh, hay ba dòng tuần tự thì **đừng vẽ** — bảng đọc nhanh hơn.

**Phạm vi:** sơ đồ **trả lời trong chat** — nền tối cứng, kèm link mở được ngay. Hình để dán vào
tài liệu là việc khác: ở đó hình phải đọc được trên **cả** nền sáng lẫn nền tối, nên dùng palette
pastel + chữ đậm chứ không phải bộ dưới đây.

## Mục tiêu: giải thích hiện tượng, không đề xuất giải pháp

Skill này dừng ở chỗ **hiểu**. Không có mục "cách sửa", không "nên làm gì", không xếp hạng phương
án, không đưa patch.

Hai việc đó cần hai loại chắc chắn khác nhau. Giải thích đúng thì chỉ cần khớp với bằng chứng đang
có. Đề xuất sửa thì phải biết ràng buộc, biết ai chịu hệ quả, biết đánh đổi — những thứ chưa ai nói
trong lượt này. Trộn vào thì người đọc nhận một bản sửa nghe rất chắc, dựng trên đúng một cách hiểu
còn chưa được xác nhận.

Trong lúc điều tra mà lộ ra chỗ sửa quá rõ ⇒ được nhắc **một câu**, đặt cuối, và nói rõ đó là quan
sát: *"Chỗ gọi `fetch` có `AbortSignal` sẵn mà không truyền vào."* Hết. User hỏi tiếp thì mới sang
việc thiết kế.

## Chọn loại sơ đồ

Chọn theo **câu hỏi người đọc đang hỏi**, không theo cái nào nhìn ngầu hơn.

| Người đọc đang hỏi | Loại |
| --- | --- |
| *"gồm những gì, nối nhau ra sao"* · *"luật nào quyết định"* · *"đi đường nào"* · *"xếp tầng thế nào"* | **`flowchart` — mặc định** |
| *"ai gọi ai, theo thứ tự nào"* — N bên **trao đổi qua lại**, tên từng bên là một phần câu trả lời | `sequenceDiagram` |
| *"đi từ trạng thái nào sang trạng thái nào, do event gì"* — transition có tên, có vòng lặp | `stateDiagram-v2` |
| *"bảng nào khoá vào bảng nào, một-nhiều hay nhiều-nhiều"* | `erDiagram` |
| *"việc nào trước việc nào, dài bao lâu"* — có **ngày thật** | `gantt` |
| nhánh · merge của git | `gitGraph` |
| còn lại (`mindmap` · `journey` · `timeline` · `classDiagram` · `quadrantChart`…) | đừng dùng trừ khi user xin — bảng thường đọc nhanh hơn |
| `C4Context` · `C4Container` | **cấm** — dùng `flowchart` có vùng |

**`flowchart` là mặc định** vì nó cho overview tốt nhất: có shape mang nghĩa, có `subgraph` để phân
vùng, sơn được nền tối, và đọc được cả khi người ta chỉ liếc qua. Ba loại dưới nó là **ngoại lệ có
lý do**, không phải lựa chọn ngang hàng.

Hai câu gỡ khi phân vân:

- **flowchart hay sequence?** Bỏ tên các bên đi — hình còn đúng không? Còn đúng ⇒ `flowchart`.
  Một trục thời gian một chiều mà không ai trả lời ai thì vẫn là `flowchart`.
- **flowchart hay state?** Câu hỏi là *"đang ở ô nào"* (⇒ state) hay *"cái gì quyết định ra ô đó"*
  (⇒ flowchart)? Ví dụ: 8 ô trạng thái agent nhưng câu hỏi là thứ tự ưu tiên của luật suy ra ô ⇒
  `flowchart`, không phải `stateDiagram`.

## Hai mode

| Mode | Dùng khi | Khuôn |
| --- | --- | --- |
| **`easy` — mặc định** | user đang muốn *hiểu chuyện gì đang xảy ra* | Một câu · Ví von · Chuyện thật diễn ra thế nào |
| **`tech`** | user xin, hoặc user đã nắm cơ chế và đang cần đúng tên thật | Context · Problem · Root cause |

Mặc định là **`easy`**, kể cả khi user là dev: hiểu hình dạng vấn đề trước, tên thật sau. Sang `tech`
khi user nói *"giải thích kỹ thuật"* · *"đi vào code"* · *"bỏ ví von"*, hoặc gọi
`/explain-with-diagrams --tech`; quay lại bằng `--easy`. Đổi rồi thì **giữ mode đó cho cả cuộc trò
chuyện**.

Hai thứ giống nhau ở cả hai mode: sơ đồ đứng ở mục nói **cơ chế**, và câu trả lời chỉ có link chứ
không có khối ```mermaid.

| Phần | Nó cho cái gì |
| --- | --- |
| **Link `/edit`** | thấy hình, phóng to, pan/zoom, sửa tại chỗ, đổi theme, export PNG/SVG, copy nguồn |
| **Phần chữ** | lời giải — thứ hình không nói được |

## Mode `easy` — khuôn

Khuôn cứng chỉ có **ba mục**:

````
## Một câu
<cả vấn đề gói trong 1–2 câu, không một thuật ngữ nào>

## Ví von
<một đồ vật đời thường, 3–4 bullet ứng 1-1 với thứ thật>
<một câu: ít thì không sao, nhiều thì …>

## Chuyện thật diễn ra thế nào
**[▶ Mở trên mermaid.live](https://mermaid.live/edit#pako:…)**
**Màu:** …
1. <mỗi bước một mệnh đề kiểm chứng được, nối bằng →>
2. …
````

| Mục | Trả lời | Hỏng khi |
| --- | --- | --- |
| **Một câu** | cả vấn đề; dừng ở đây cũng hiểu | có thuật ngữ, tên file, mã số |
| **Ví von** | cùng cấu trúc, bằng đồ vật quen | ví von chỉ để cho đẹp, không ứng được 1-1 |
| **Chuyện thật** | cơ chế thật, từng mắt một | viết thành văn xuôi, hoặc có bước không kiểm chứng được |

### Mục thêm: đặt tên theo cái bài toán có

Hết ba mục trên là dừng được. Thêm mục chỉ khi **chính bài toán đó có một tính chất chưa kể xong** —
và tên mục gọi thẳng tính chất ấy, không lấy từ một danh sách dựng trước.

Ví dụ bài `/sessions` gọi quá nhiều lần: hệ quả của nó **không tăng tuyến tính** — số lượt gọi nhân
với chi phí mỗi lượt — nên có thêm *"Chỗ làm nó tệ gấp bội"*, rồi *"Kết"* để chốt hai thứ đó nhân
nhau và nó không tự hết. Bài khác sẽ ra mục khác: *"Vì sao chỉ hỏng trên prod"*, *"Ai mất dữ liệu"*,
*"Vì sao log không thấy gì"*.

❌ Đừng giữ *"Chỗ làm nó tệ gấp bội"* như một ô trống phải điền. Vấn đề nào tăng tuyến tính thật thì
viết mục đó là bịa. Dấu hiệu bịa: bỏ mục đi mà câu trả lời không thiếu gì.

### Ví von phải ứng 1-1

Đây là mục dễ làm sai nhất. Ví von chạy được không phải vì nó hay, mà vì **cấu trúc giữ nguyên**:
mỗi thứ trong ví von ứng với đúng một thứ thật, và quan hệ giữa chúng cũng vậy.

| Trong ví von | Trong hệ thống |
| --- | --- |
| cái chuông trong kho | tin server hô lên cho mọi tab |
| nhân viên đang đứng trong phòng | tab đang mở trang đó |
| chạy đi kiểm kê cả kho | gọi API tải lại cả trang |
| bỏ dở mà vẫn tốn công | request bị huỷ ở client, server chạy nốt |

Cách kiểm: nói một **hệ quả** trong ví von rồi dịch sang hệ thống thật. *"Mười người cùng làm thì
chuông kêu liên tục"* → *"mười người cùng gõ thì tin bắn liên tục"* — dịch ra vẫn đúng ⇒ ví von
đứng được. Và người đọc **tự suy ra** được hệ quả đó mà không ai phải nói cho họ; đó là chỗ ví von
trả công.

Dịch ra mà sai ở một chỗ ⇒ bỏ ví von, đừng cố chữa. Ví von lệch dẫn người đọc đi xa hơn là không có
ví von nào.

### Chuyện thật: chuỗi nhân quả, không văn xuôi

Mỗi bước một mệnh đề **kiểm chứng được** — số thật, tên hàm thật — nối bằng `→`. Văn xuôi bắt người
đọc tự dựng lại mũi tên trong đầu; đánh số thì họ đếm được mắt nào hỏng.

Sơ đồ đứng ở mục này vì nó **là** chuỗi đó vẽ ra. Chuỗi đánh số đi đúng thứ tự node trên hình ⇒
không cần khối *cách đọc* nữa, chuỗi chính là nó. Chỉ còn **Màu** cần một dòng chú giải.

### Bớt mã số

Trong `easy`, mặc định **không nhắc mã số**. `065`, `P13`, `CP-23.15` chỉ có nghĩa với người đã mở
đúng file đó; câu dẫn bằng một mã là câu viết cho người đã biết sẵn.

❌ *"065 để lại 15 probe đánh số P1…P15; 043 để lại một gate."*

✅ *"Việc tối ưu đường đọc số session đã đo xong và có số thật: đỉnh 41 session bẩn cùng lúc. Nhưng
cơ chế dot đổi màu realtime thì chưa ai nghiệm thu — tới giờ chưa từng được xác nhận kể cả với một
session đang gõ."*

Bản ❌ đếm **số lượng ký hiệu**, phải mở hai file plan mới hiểu. Bản ✅ đọc một lượt là biết việc nào
đã có bằng chứng, việc nào còn hổng.

Cần dẫn nguồn thì gắn mã ở **cuối** câu, dạng chú thích hoặc link — *"(plan 065)"* — đừng để nó làm
chủ ngữ. Luật này áp cả cho **nhãn node trên hình**: ô tên `P13` không nói gì, ô tên *"đo đỉnh
session cùng lúc"* thì đọc ra ngay.

## Mode `tech` — khuôn

Bỏ ví von, gọi đúng tên thật. Mã số và ID được dùng thoải mái, chỉ cần lần đầu kèm nó là gì.

````
**Context:** <hệ thống nào, ai đang chạy cái gì>
**Problem:** <nhìn thấy gì sai — số thật, dòng log thật>

**[▶ Mở trên mermaid.live](https://mermaid.live/edit#pako:…)**

**Colors:** <mỗi màu nghĩa là gì>
**How to read:** <đi từ đâu, dừng ở đâu>
**Root cause:** <chỗ trên hình làm kết luận đứng được>
````

`Context` + `Problem` đứng **trên** link còn `Root cause` đứng **dưới**, vì hình là **bằng chứng**:
dựng câu hỏi, xem hình, rồi mới kết luận. Đảo lại thì kết luận đứng trước thứ chứng minh nó.

`Root cause` là mục duy nhất không thể bỏ. Nó là **lý do** sơ đồ đó tồn tại; `Colors` và `How to
read` chỉ là chú giải. ❌ Không diễn lại nhãn đã có trên hình (*"ô A hỏi inflight > 0, nếu đúng thì
sang ô B"*) — user đọc được rồi.

Dùng `Root cause` chứ không `Tracing`: tracing là **việc đi tìm**, còn nhãn này mang **thứ tìm ra**.

## Một sơ đồ là mặc định

Một bài toán ⇒ **một sơ đồ**, khuôn viết một lượt. Người đọc theo được một mạch, không phải nhớ chỗ
nào đang nói chuyện gì.

Vẽ thêm sơ đồ chỉ khi **yêu cầu chứa nhiều bài toán khác nhau** — khác hiện tượng, khác nguyên nhân,
sửa ở chỗ khác nhau. Khi đó mục *Chuyện thật diễn ra thế nào* (hoặc phần `Problem` ở `tech`)
chia thành mấy phần con, mỗi phần một link + một chuỗi riêng; còn *Một câu* và *Ví von* vẫn viết một
lần cho cả bài.

Dấu hiệu tách sai: hai sơ đồ cùng một hiện tượng, hoặc kết luận của chúng là một câu nói theo hai
cách ⇒ gộp lại.

## Không dán nguồn sơ đồ vào câu trả lời

Khối ```mermaid dài hơn cả phần chữ, chiếm hết màn hình, và **không cho thêm gì** — mở link ra là có
hình đầy đủ, phóng to được, export được, copy nguồn được ngay trong editor. Câu trả lời chỉ có link
+ chữ.

User xin nguồn để dán vào doc/PR ⇒ đưa **file `.mmd`** đã sinh sẵn cho `mermaid-link.mjs`, hoặc chỉ
sang tab *Code* trên mermaid.live. Đừng dán lại vào chat.

## Nguồn sơ đồ — sáu luật cứng

### 1· Nền phải tối thật

`theme: 'dark'` **một mình không đủ** — nó chỉ đổi màu node, canvas vẫn trắng. Cần cả hai:

```
%%{init: {'theme':'dark', 'themeVariables': {'background':'#0d1117'}}}%%
flowchart TD
    subgraph ALL[" "]
    …toàn bộ node…
    end
    style ALL fill:#0d1117,stroke:#0d1117
```

Khối `subgraph ALL` bọc **tất cả** node mới là thứ thật sự sơn nền. Lề ngoài SVG trên mermaid.live
vẫn theo toggle sáng/tối của chính site đó (localStorage) — **nói ra cho user biết**, đừng im.

### 2· Màu theo **ngữ nghĩa**, khai bằng `classDef`

Không tô vài ô cho có màu. Mỗi *loại* node một màu, khai một lần rồi `class` vào:

```
classDef bug fill:#5a1e1e,stroke:#ff7b72,color:#ffdedb,stroke-width:3px
class A,FAIL bug
```

| Vai trò | fill | stroke | color |
| --- | --- | --- | --- |
| nguồn dữ liệu · điểm vào | `#10324a` | `#58a6ff` | `#cfe8ff` |
| chỗ hỏng · `failed` | `#5a1e1e` | `#ff7b72` | `#ffdedb` |
| suy ra · cảnh báo | `#5a4a1e` | `#e3b341` | `#fff6d5` |
| kết luận "đang chạy" · thành công | `#14532d` | `#4ade80` | `#dcfce7` |
| trung tính · đã nghỉ · `done` | `#2a2f36` | `#8b949e` | `#d6dbe1` |
| câu hỏi · nhánh quyết định | `#1c2431` | `#8b9cff` | `#dfe3ff` |
| chờ người | `#5a3410` | `#ffb454` | `#ffe9cc` |
| biến đổi · nén · xử lý | `#3a2a5a` | `#bc8cff` | `#ece0ff` |
| song song · chờ con | `#14453d` | `#39d3bb` | `#d6fff7` |

Pastel sáng (`#ffdddd`, `#ddffdd`) là màu cho nền trắng — trên nền tối nó thành mảng chói. Luôn khai
cả `color:` (màu chữ), nếu không mermaid để chữ tối trên nền tối ở vài node.

**Nhuộm cạnh** theo màu đích khi sơ đồ có hai kết cục đối nhau — nhìn màu cạnh là biết nhánh đó dẫn
về đâu: `linkStyle 1 stroke:#ff7b72,stroke-width:4px`. Index đếm từ **0**, theo thứ tự cạnh xuất hiện
trong nguồn; `A --> B & C` là **hai** cạnh. Đếm sai chỉ tô nhầm cạnh, không vỡ hình.

### 3· Không chú thích trong hình

Không `subgraph "Ghi chú"`, không node legend. Chú giải sống trong câu trả lời (khối 1–3 ở trên).

### 4· Một chủ đề = **một** loại sơ đồ, giữ nguyên qua các lượt

Vẽ lại cùng một thứ ở lượt sau thì **giữ nguyên loại sơ đồ, thứ tự node, tên section**. Người đọc đã
dựng bản đồ trong đầu từ lượt trước; đổi hình là bắt họ học lại từ đầu, và họ sẽ tưởng nội dung đã
đổi chứ không phải chỉ cái vỏ.

Buộc phải đổi (ràng buộc kỹ thuật, phát hiện hình cũ sai) ⇒ **nói ra một câu ngay dưới hình**: đổi
cái gì, vì sao. Đổi im lặng là lỗi.

⚠️ Bẫy đã dính: `sequenceDiagram` **không có `subgraph`**, nên không sơn được nền tối bằng khối
`ALL` — canvas của nó trong suốt, theo nền site. Đừng vì thế mà lặng lẽ đổi sang `flowchart`: loại
sơ đồ chọn theo **câu hỏi** (xem *Chọn loại sơ đồ*), chọn xong thì giữ, và nếu `sequenceDiagram` là
đúng loại thì **chấp nhận canvas trong suốt + nói ra một câu**.

### 5· Chuỗi dài ⇒ `LR`, không `TD`

mermaid.live và mọi chỗ render inline đều **fit cả hình vào khung**. Một chuỗi 10 bước xếp theo `TD`
thành cột cao và hẹp, fit theo chiều cao ⇒ chữ nhỏ tới mức phải zoom từng đoạn mới đọc được, và mất
đúng cái sơ đồ sinh ra để cho: **nhìn một phát thấy hình dạng**. Màn hình rộng hơn cao — hình nằm
ngang dùng được hết chỗ đó.

Ngưỡng: **chuỗi chính quá 7–8 node ⇒ `LR`**. Ngắn hơn thì `TD` đọc tự nhiên hơn, giữ `TD`.

Đổi hướng phải sửa **hai chỗ** — `subgraph` có `direction` riêng và nó thắng cái khai ở dòng
`flowchart`:

```
flowchart LR
    subgraph ALL[" "]
    direction LR
    …
```

Sửa một chỗ thôi thì hình vẫn dọc như cũ, không báo lỗi gì — bẫy đã dính.

Trong hình `LR`, các nhánh song song xếp theo chiều dọc. Đó là chỗ hình được phép cao lên: một mắt
xích bị N nguồn dồn vào thì N nguồn đó nằm thành cột, đọc ra ngay là phép nhân.

### 6· Nhãn ngắn, `<br/>` để xuống dòng

Một node quá 3 dòng là dấu hiệu nó đang ôm hai ý — tách ra, hoặc đẩy phần thừa xuống phần chữ.

## Sinh link mermaid.live

```bash
node ~/.claude/skills/explain-with-diagrams/mermaid-link.mjs a.mmd b.mmd
```

Script giữ **đúng khuôn state 7 field** và tự verify round-trip. Ba điều phải nhớ:

| Điều | Vì sao |
| --- | --- |
| **`/edit`, không `/view`** | live editor có code + hình cạnh nhau, sửa tại chỗ, đổi theme, export. Cùng payload, chỉ khác path |
| **7 field**: `code` · `mermaid` · `autoSync` · `updateDiagram` · `rough` · `panZoom` · `editorMode` | thiếu 3 field cuối ⇒ site hiện diagram *"Loading URL failed"*, **không** báo lỗi gì rõ |
| **Verify round-trip rồi mới đưa** | giải mã lại payload, so từng byte. Không tự nhận là đã kiểm việc **render** — cái đó chỉ mở link mới biết |

Hỏng link mà chưa rõ vì sao ⇒ đừng đoán tiếp: nhờ user mở [mermaid.live](https://mermaid.live), gõ
đại một sơ đồ, dán URL lại. Giải mã URL đó ra là thấy đúng schema bản họ đang chạy.

⚠️ **Auto-mode classifier chặn** heredoc ghi file `.mjs` **kèm** chạy `node` trong cùng một lệnh
bash. Tách ra: Write tool cho script, Bash cho `node`. Ghi `.mmd` bằng heredoc thì không sao.

## Checklist trước khi gửi

- [ ] Không có mục "cách sửa" / "nên làm gì" — dừng ở chỗ hiểu
- [ ] `easy`: đủ *Một câu* · *Ví von* · *Chuyện thật*; mục thêm nào bỏ đi mà không thiếu gì thì bỏ
- [ ] Ví von dịch một hệ quả sang hệ thống thật vẫn đúng
- [ ] `easy`: không câu nào dẫn bằng mã số, nhãn node cũng vậy
- [ ] `tech`: `Context` · `Problem` trên link, `Root cause` dưới link
- [ ] Một bài toán ⇒ **một** sơ đồ
- [ ] Không có khối ```mermaid trong câu trả lời
- [ ] `roundtrip_ok=true` cho mọi link
- [ ] Nguồn có `%%{init}%%` dark **và** `subgraph ALL` sơn nền
- [ ] Chuỗi chính quá 7–8 node ⇒ `LR` ở **cả** dòng `flowchart` lẫn `direction` trong `subgraph ALL`
- [ ] Màu khai bằng `classDef`, mỗi vai một màu, có `color:`
- [ ] Không có chú thích/legend nhét trong hình
