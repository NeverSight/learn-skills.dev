---
name: mermaid-diagram-simple
description: Viết nguồn sơ đồ mermaid nền tối — chọn loại sơ đồ theo câu hỏi người đọc đang hỏi (`flowchart` mặc định), sơn nền tối thật, màu theo ngữ nghĩa khai bằng `classDef`, chọn `TD`/`LR` theo độ dài chuỗi, nhãn ngắn, không legend trong hình, giữ nguyên hình qua các lượt. Chỉ lo việc vẽ; đưa hình cho user thế nào (link, file) là việc của skill gọi nó, vd `explain-with-diagrams`. Dùng khi cần viết một sơ đồ mermaid để xem trên nền tối. Hình để dán vào tài liệu (phải đọc được cả nền sáng lẫn tối) thì dùng `mermaid-diagram-design`.
---

# Sơ đồ mermaid nền tối

## Mental model

Vẽ một sơ đồ là hai bước: **chọn loại** theo câu hỏi người đọc đang hỏi → **viết nguồn** theo sáu
luật cứng. Đưa hình tới user bằng cách nào (link, file `.mmd`) không thuộc skill này.

Sơ đồ đáng vẽ khi câu trả lời có **nhiều tầng**, **nhiều nhánh**, hoặc **thứ tự ưu tiên**. Ba cái
đó viết bằng văn xuôi thì người đọc phải tự dựng hình trong đầu. Còn một danh sách phẳng, một bảng
so sánh, hay ba dòng tuần tự thì **đừng vẽ** — bảng đọc nhanh hơn.

**Phạm vi:** sơ đồ xem trên **nền tối cứng** — kiểu trả lời trong chat. Hình để dán vào tài liệu
là việc khác: ở đó hình phải đọc được trên **cả** nền sáng lẫn nền tối, nên dùng palette pastel +
chữ đậm của `mermaid-diagram-design`, không phải bộ dưới đây.

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

Khối `subgraph ALL` bọc **tất cả** node mới là thứ thật sự sơn nền. Lề ngoài SVG vẫn theo nền của
chỗ render nó — trên mermaid.live là toggle sáng/tối của chính site (localStorage) — **nói ra cho
user biết**, đừng im.

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

Không `subgraph "Ghi chú"`, không node legend. Màu nghĩa là gì, đọc từ đâu — những thứ đó viết
thành chữ bên ngoài hình.

### 4· Một chủ đề = **một** loại sơ đồ, giữ nguyên qua các lượt

Vẽ lại cùng một thứ ở lượt sau thì **giữ nguyên loại sơ đồ, thứ tự node, tên vùng**. Người đọc đã
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

## Checklist trước khi gửi

- [ ] Loại sơ đồ chọn theo câu hỏi; `flowchart` trừ khi có lý do
- [ ] Nguồn có `%%{init}%%` dark **và** `subgraph ALL` sơn nền
- [ ] Màu khai bằng `classDef`, mỗi vai một màu, có `color:`
- [ ] Không có chú thích/legend nhét trong hình
- [ ] Chuỗi chính quá 7–8 node ⇒ `LR` ở **cả** dòng `flowchart` lẫn `direction` trong `subgraph ALL`
- [ ] Vẽ lại chủ đề cũ: giữ loại sơ đồ, thứ tự node; đổi thì nói ra
