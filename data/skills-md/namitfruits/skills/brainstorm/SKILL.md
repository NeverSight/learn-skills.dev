---
name: brainstorm
description: >-
  Trao đổi với người dùng để làm rõ điều họ thực sự mong muốn — chỉ làm rõ, chưa phân tích. Mở đầu bằng nói lại
  đề cho người dùng sửa chỗ hiểu sai, hỏi hiện trạng (hệ thống đang có gì, chưa có gì), rồi tách đề thành module —
  module chính chỉ lấy từ chữ trong đề (vd "app đặt lịch có nhắc lịch và thanh toán" ra Đặt lịch · Nhắc lịch ·
  Thanh toán); module chính cần thứ chưa có (vd phân quyền cần
  đăng nhập) thì hỏi người dùng có thêm module bổ sung không — cho người dùng
  **tick chọn feature** của từng module — cái được tick là scope — chốt bức tranh tổng quan, rồi đi từng module:
  người dùng kể trước, agent hỏi mục tiêu và chỗ còn hở (cái gì · ai · khi nào · nhận lại gì · một ví dụ thật) tới khi
  hình dung được, rồi nói lại bằng lời mình cho người dùng xác nhận. Hỏi bằng câu có sẵn đáp án; hỏi mục tiêu, không đào
  nỗi khổ; không chốt con số, không đào trường hợp lỗi, không viết user story — đó là việc của bước phân tích sau. Ra
  thư mục `.brainstorm/NNN-slug/` gồm file brief `brief.md` theo `templates/brief.md` và file checklist
  `checklist.md` theo `templates/checklist.md`: mỗi bước lặp tới khi mọi item của bước đã đóng,
  checklist mọc thêm item khi có module, feature mới, bị ngắt thì đọc checklist để chạy tiếp. Kèm
  `templates/modules.md` (gợi ý feature cho các module hay gặp) và `scripts/verify.py` lint brief và checklist. Dùng khi người dùng nói "brainstorm", "cùng nghĩ xem tôi muốn gì", "làm rõ ý tưởng",
  "phỏng vấn tôi", "làm rõ requirement", hoặc đưa một đề liệt kê tính năng kiểu "tôi muốn làm A, B, C" mà chưa rõ
  từng cái gồm gì.
---

# brainstorm — trao đổi để làm rõ người dùng thực sự muốn gì

File này đủ để chạy skill. Vì sao skill được thiết kế như vậy thì ở [SPEC.md](SPEC.md), không cần đọc khi chạy.

## Tóm tắt

1. **Hiểu đề & hiện trạng**: agent nói lại đề bằng lời mình, người dùng sửa chỗ hiểu sai và tả hệ thống đang có
   gì, chưa có gì cho những việc trong đề.
2. **Tách module & chọn scope**: module chính chỉ lấy từ đề; xét module chính cần thứ gì khác mới chạy được, thứ chưa
   có thì hỏi người dùng có thêm module bổ sung không; rồi người dùng tick feature. Cái được tick là scope.
3. **Tổng quan**: in hiện trạng và bức tranh scope, người dùng nói "đúng" thì điền module vào brief.
4. **Làm rõ từng module**: người dùng kể trước, agent hỏi mục tiêu và chỗ còn hở, rồi nói lại cho người dùng xác nhận.
5. **Chốt**: soát chỗ nói chưa khớp nhau, xác nhận giả định, người dùng nói "đúng" thì dừng.

Mỗi bước là một vòng: hỏi → ghi → đóng item trong checklist → điểm lại → còn item mở thì hỏi tiếp. Trả lời xong một
câu chưa phải là xong bước; bước xong khi mọi item của nó đã đóng (xem "Checklist — mỗi bước là một vòng").

Chỉ **làm rõ**, không **phân tích**. Câu hỏi kiểu "có … không", "ai", "lúc nào", "nhận lại gì" là làm rõ. Câu hỏi kiểu
"bao lâu", "bao nhiêu", "nếu trùng / thiếu / quá hạn thì sao" là phân tích, để dành cho bước sau. Người dùng tự nói
ra con số hay trường hợp lỗi thì vẫn ghi lại, chỉ là không hỏi tới.

Mỗi lần chạy có một thư mục `.brainstorm/NNN-slug/` trong thư mục làm việc, chứa hai file. `NNN` là số kế tiếp
trong `.brainstorm/`, `slug` lowercase-kebab. Thư mục và hai file được tạo ở Bước 1, trước tin đầu tiên.

| File | Là gì |
| --- | --- |
| `brief.md` — **brief** | sản phẩm, theo khuôn [`templates/brief.md`](templates/brief.md): **mỗi module một section** `## Module · <tên>`, mỗi feature một `### <tên feature>`. Bước phân tích đọc file này |
| `checklist.md` — **checklist** | việc phải xong của lần chạy, theo khuôn [`templates/checklist.md`](templates/checklist.md). Quyết định khi nào sang bước sau, và chạy tiếp từ đâu khi bị ngắt |

| File của skill | Dùng ở |
| --- | --- |
| [`templates/brief.md`](templates/brief.md) | khuôn file brief, copy ra rồi điền |
| [`templates/checklist.md`](templates/checklist.md) | khuôn file checklist, copy ra rồi đóng / thêm item |
| [`templates/modules.md`](templates/modules.md) | khung hỏi chung + thứ tự module + gợi ý feature cho các module hay gặp — gợi ý, không phải danh sách đóng |
| [`scripts/verify.py`](scripts/verify.py) | lint brief và checklist đi kèm |

```bash
python3 $SKILL/scripts/verify.py .brainstorm/NNN-slug/    # $SKILL là thư mục chứa SKILL.md; kiểm cả brief.md và checklist.md
```

### Input

Hiện tại skill chỉ dùng **đề người dùng đưa trong chat** và các câu trả lời. Đọc code / docs dự án, tài liệu đính
kèm là phần **chưa thiết kế**.

### Ví dụ trong skill không phải nguồn

Mọi ví dụ trong file này và trong `modules.md` chỉ minh hoạ **cách làm**. Module, feature, hiện trạng, chữ dùng khi
chạy chỉ lấy từ **đề đang làm** và **câu trả lời của người dùng**. Đề giống ví dụ tới đâu cũng không chép bảng,
module, feature từ ví dụ; ví dụ có module mà đề không nêu thì không vì thế mà thêm. Gợi ý feature trong `modules.md`
dùng để dựng đáp án cho module đã có trong scope, không dùng để thêm module.

### Cờ `--auto`

Chỉ để chạy thử. Bật khi lời gọi có `--auto`. Mọi câu hỏi vẫn soạn đủ và in ra chat như khi hỏi thật, nhưng
**không gọi AskUserQuestion**: lấy đáp án khuyên dùng (câu chọn nhiều thì lấy các đáp án khuyên dùng), ghi vào
Nhật ký với cột Trả lời bắt đầu bằng `(--auto)`. Câu không có đáp án khuyên dùng (hiện trạng, thứ module cần mà chưa
rõ đã có chưa) thì không chọn thay: ghi vào Câu hỏi còn mở, không thêm module bổ sung. Chỗ cần "đúng" coi như người
dùng đã nói "đúng". Lời mời kể ở Bước 1 và Bước 4 coi như người dùng gõ "hỏi đi"; câu xin ví dụ coi như người dùng
không nghĩ ra, lấy ví dụ soạn sẵn khuyên dùng.

## Luật hỏi — dùng cho mọi bước

| Luật | Nội dung |
| ---- | -------- |
| hỏi khi cần làm rõ | không có hạn số câu mỗi lượt. Chưa hình dung được thì hỏi; đã rõ thì không |
| tổng quan trước | chưa chốt hiện trạng, scope và bức tranh tổng quan (Bước 1–3) thì chưa hỏi chi tiết module nào |
| hỏi mục tiêu, không hỏi nỗi khổ | "làm xong module này anh/chị muốn được gì?" kèm đáp án gợi ý. Không hỏi "đang khổ vì gì", "vì sao cần cái này". Người dùng tự kể nỗi khổ thì ghi vào **Mục tiêu** của module đó |
| dừng ở mức hình dung được | không hỏi con số, ngưỡng, thời hạn, trường hợp lỗi. "Đơn chưa thanh toán có tự huỷ không?" là làm rõ; "bao lâu thì huỷ?" để bước phân tích |
| một câu một ý | không gộp "ai duyệt và duyệt thế nào" vào một câu |
| chữ nghiệp vụ | "lưu lại để xem sau", không phải "persist vào DB" |
| đoán thì ghi giả định | thứ agent đoán mà không hỏi (vd "chỉ lễ tân dùng màn này") → `A-NN` ở Giả định, trạng thái `chờ xác nhận`, xác nhận một lượt ở Bước 5 |
| ghi ngay | mỗi câu trả lời là một dòng `Q<n>` ở Nhật ký (kèm module), giữ chữ người dùng; ý nào sinh ra từ câu đó có đuôi `(Q<n>)`. Cập nhật brief và checklist sau mỗi lượt trả lời, từ Bước 1 |

## Checklist — mỗi bước là một vòng

Checklist có một section `## Bước N — …` cho mỗi bước. Bước chỉ xong khi mọi item trong section đó đã **đóng**; còn
item mở thì chưa sang bước sau.

| Dấu | Nghĩa | Đuôi dòng |
| --- | --- | --- |
| `- [ ]` | chưa xong | — |
| `- [x]` | xong | nguồn: `(Q<n>)` hay `(đề)`. Hỏi lại hai lần vẫn chưa rõ, đã chuyển sang Câu hỏi còn mở: `(Q<n>, → OQ-NN)` |
| `- [-]` | bỏ, không làm nữa | `— <lý do> (Q<n>)`, vd `— bỏ khỏi scope (Q9)` |

**Vòng của mỗi bước.** Sau mỗi lượt người dùng trả lời:

1. Ghi câu trả lời vào brief: Nhật ký, và chỗ ý đó thuộc về.
2. Đóng item vừa xong; thêm item cho việc mới lộ ra (bảng dưới). Cập nhật `updated` của checklist.
3. In **điểm lại** trong chat, 2–4 dòng: bước này vừa đóng item nào · còn item nào mở. Điểm lại chỉ để người dùng
   thấy, không dừng chờ "đúng" — chỗ cần "đúng" đã là item riêng.
4. Còn item mở ⇒ hỏi item mở đầu tiên. Hết ⇒ sang bước sau.

```
Điểm lại Bước 2: ✓ Phân quyền cần đăng nhập → thêm module Đăng nhập (Q2)
Còn: tick feature cho Đăng nhập · Báo cáo · Cảnh báo · Insight · Phân quyền
```

**Thêm item.** Checklist mọc theo cuộc trao đổi; item cố định của mỗi bước có sẵn trong khuôn.

| Lúc | Thêm vào | Item |
| --- | --- | --- |
| Bước 2, thứ module chính cần mà chưa rõ đã có chưa | Bước 2 | `Phụ thuộc: <module> cần <thứ>`, mỗi thứ một item |
| Bước 2, chữ trong đề chưa rõ nghĩa | Bước 2 | `Chữ chưa rõ: <chữ>` |
| Bước 2, đã có bảng module | Bước 2 | `Tick feature: <module>`, mỗi module một item, kể cả module bổ sung |
| Bước 3, module chưa hình dung được ở mức tổng quan | Bước 3 | `Hình dung tổng quan: <module>` |
| Bước 3 được "đúng" | Bước 4 | mỗi module một `### Module · <tên>` gồm `Người dùng kể` · `Mục tiêu` · mỗi feature đã tick một item mang đúng tên feature · `Nói lại được "đúng"` |
| thêm module / feature giữa chừng | Bước 2 nếu Bước 3 chưa xong, không thì Bước 4 | như hai dòng trên |
| bỏ module / feature | — | đóng mọi item của nó bằng `[-]` |
| câu trả lời chọi câu trước, mở ý ngoài scope | bước đang chạy | `Chọi câu: Q<a> ↔ Q<b>` · `Ý ngoài scope: <ý>` |
| Bước 5, soát ra chỗ chưa khớp | Bước 5 | `Chưa khớp: <chỗ>`, mỗi chỗ một item |

Item feature ở Bước 4 đóng khi đã rõ **cái gì · ai · khi nào · nhận lại gì** (khía cạnh nào không áp dụng thì thôi)
và có một ví dụ thật. Item `Người dùng kể` đóng cả khi người dùng gõ "hỏi đi".

**Chạy tiếp khi bị ngắt.** Lời gọi trỏ tới một brief / checklist, hay nói "tiếp tục" mà `.brainstorm/` có brief
`status: draft` (nhiều thư mục thì hỏi thư mục nào, Questionnaire chọn một) ⇒ đọc checklist và brief, in tiến độ — mỗi bước
✓ / đang làm / chưa, kèm item mở đầu tiên — rồi hỏi tiếp từ item đó. Không hỏi lại thứ đã đóng. `verify.py` in sẵn
item mở đầu tiên.

## Cách trao đổi

Ba dạng. Chọn theo thứ cần lấy từ người dùng:

| Dạng | Dùng khi | Cách làm |
| --- | --- | --- |
| **Questionnaire** | đoán được vài đáp án hợp lý | gọi AskUserQuestion. Mỗi câu 2–4 đáp án; đáp án tin nhất đứng đầu, `label` có "(Khuyên dùng)", `description` nói chọn thì kết quả khác đi thế nào. Câu hỏi về thứ đang có (hiện trạng, thứ module cần) không gắn "(Khuyên dùng)" khi người dùng chưa kể gì làm căn cứ — đó là sự thật agent không đoán được. Đáp án loại trừ nhau thì chọn một; người dùng có thể muốn vài cái cùng lúc (feature, kênh nhận thông báo) thì `multiSelect`. Tối đa 4 câu mỗi lần gọi, cần hơn thì gọi tiếp |
| **Q&A** | cần chữ của chính người dùng: lời kể, ví dụ thật | một câu thường trong chat, rồi dừng lượt chờ người dùng viết. Không dùng AskUserQuestion |
| **Xác nhận** | đưa cách agent hiểu cho người dùng duyệt | in tóm tắt trong chat, hỏi "đúng chưa?", dừng lượt chờ trả lời bằng chữ. Không dùng AskUserQuestion. Cần chữ "đúng" rõ ràng; "tuỳ", "nghe ổn", "chắc vậy" thì hỏi lại "có chỗ nào muốn sửa không?" |

Dạng theo từng lúc:

| Lúc | Dạng |
| --- | --- |
| Bước 1 — hiểu đề & hiện trạng | một tin: nói lại đề, rồi Q&A mời kể hiện trạng; gõ "hỏi đi" thì Questionnaire, chọn một, mỗi việc trong đề một câu |
| Bước 2 — một chữ trong đề chưa rõ nghĩa | Questionnaire, chọn một |
| Bước 2 — thứ module chính cần mà chưa rõ đã có chưa | Questionnaire, chọn một, mỗi thứ một câu |
| Bước 2 — chọn feature cho từng module | Questionnaire, `multiSelect`, mỗi module một câu |
| Bước 3 — module chưa hình dung được ở mức tổng quan | Questionnaire, chọn một |
| Bước 3 — bức tranh tổng quan | Xác nhận |
| Bước 4 — mở đầu mỗi module | Q&A: mời kể |
| Bước 4 — mục tiêu, chỗ còn hở | Questionnaire |
| Bước 4 — ví dụ thật | Q&A; người dùng không nghĩ ra thì Questionnaire với 2–3 ví dụ soạn sẵn để chọn rồi sửa |
| Bước 4 — cuối mỗi module | Xác nhận: nói lại bằng lời mình |
| Bước 5 — chỗ nói chưa khớp, lệch mục tiêu | Questionnaire, chọn một |
| Bước 5 — giả định | Questionnaire: "Đúng (Khuyên dùng)" · "Sai — …", gom mọi giả định một lượt |
| Bước 5 — tóm tắt cuối | Xác nhận |

Người dùng đổi dạng lúc nào cũng được:

- Gõ vào Other ⇒ lấy chữ đó làm câu trả lời; chữ đó mở ý mới thì câu kế tiếp hỏi vào ý đó.
- Huỷ một lượt hỏi (bấm Esc / từ chối) hay gõ thẳng vào chat ⇒ **không dừng**: chờ họ viết xong, ghi phần họ viết
  vào file (`Q<n>` với câu hỏi `(tự viết)`), rồi chỉ hỏi chỗ còn hở. Câu đang hỏi dở mà phần họ viết đã trả lời thì bỏ.
- Đang Q&A mà gõ "hỏi đi" ⇒ chuyển sang Questionnaire.

### Khi câu trả lời chưa dùng được

Hỏi lại bằng cách khác — cụ thể hơn, có ví dụ, có đáp án — không lặp y nguyên câu cũ. Một chỗ hỏi lại tối đa hai lần;
vẫn chưa rõ thì ghi vào Câu hỏi còn mở rồi đi tiếp.

| Trường hợp | Ví dụ | Làm gì |
| --- | --- | --- |
| chung chung | "đầy đủ", "đẹp", "như app khác" | Questionnaire, mỗi đáp án là một cách hiểu cụ thể: "đầy đủ là thấy được những gì?" |
| hai nghĩa | "gửi cho quản lý", khi có cả quản lý chi nhánh lẫn quản lý vùng | Questionnaire, mỗi nghĩa một đáp án |
| không biết, chưa nghĩ tới | "chưa nghĩ tới", "tuỳ em" | có cách hợp lý thì đưa nó làm đáp án khuyên dùng, người dùng chọn thì ghi như câu trả lời. Việc do người khác quyết thì ghi Câu hỏi còn mở kèm ai trả lời được |
| lạc câu hỏi | hỏi "ai nhận tin nhắc lịch?", người dùng kể tin nhắc gửi lúc mấy giờ | ghi phần đã nói vào đúng chỗ nó thuộc, nói ngắn đã ghi ở đâu, rồi hỏi lại câu cũ bằng cách khác — thường đổi sang Questionnaire |
| chọi câu trước | ở Hiện trạng nói hồ sơ khách chỉ có email, ở Nhắc lịch muốn nhắc qua tin nhắn | hỏi ngay, trích nguyên văn hai câu kèm `Q<n>`; đáp án: giữ câu trước · giữ câu sau · cả hai đúng, mỗi câu cho một trường hợp |
| mở ý ngoài scope | đang ở Đặt lịch, người dùng nói muốn khách tích điểm | ghi lại, hỏi một câu: thêm vào scope (module, feature nào) hay để Ngoài phạm vi |
| đi vào chi tiết | "quá 15 phút thì huỷ" | ghi nguyên văn vào feature, không hỏi sâu thêm |

Ở Nhật ký, mỗi lần hỏi lại là một dòng `Q<n>` mới. Câu trả lời lạc câu hỏi ghi theo module mà nó thực sự nói tới.

## Bước 1 — Hiểu đề & hiện trạng

Trước khi tách việc, agent nói lại đề để người dùng thấy mình được hiểu thế nào, rồi giúp họ tả hệ thống **đang có
gì, chưa có gì** cho những việc trong đề. Đọc sai một chữ trong đề thì cả bảng module sai theo, nên chỗ hiểu sai cần
lộ ra ngay tin đầu. Thứ đã có thì Bước 2 không biến nó thành module để làm lại, và module mới biết dựa vào đâu.

1. **Nói lại đề** bằng lời mình, 2–4 dòng: người dùng đang có gì, muốn làm gì, để ai dùng (nếu đề nói). Chữ nào
   trong đề agent phải đoán nghĩa thì nói rõ cách mình hiểu, vd *"insight — em hiểu là công cụ tự chỉ ra điểm đáng
   chú ý trong số liệu"*. Chỉ nói lại đề: **chưa tách module, chưa gợi feature**, không thêm việc đề không nêu.
2. Rút từ đề những gì người dùng nói đang có (câu kiểu "tôi có…", "đang dùng…", "hiện đang…") → **Đã có**, nguồn
   `(đề)`.
3. **Tạo hai file** trước khi gửi tin: copy `templates/brief.md` ra `.brainstorm/NNN-slug/brief.md`, điền front matter, đề
   nguyên văn ở Tổng quan, Đã có `(đề)`; phần còn lại giữ khuôn tới Bước 3. Copy `templates/checklist.md` ra
   `.brainstorm/NNN-slug/checklist.md`, điền front matter, xoá khối `### Module · <tên module>` mẫu ở Bước 4.
4. Gộp nói lại đề và lời mời kể hiện trạng vào **một tin** (Q&A), rồi **dừng lượt**. Lời mời chỉ nhắc những việc
   **có trong đề**:

   ```
   Em hiểu đề thế này:
   - Phòng khám đang nhận lịch qua Zalo và điện thoại.
   - Muốn làm: khách đặt lịch online · nhắc khách trước giờ hẹn · thanh toán · phân quyền cho nhân viên.
   Chỗ nào em hiểu sai thì sửa luôn.

   Rồi kể thêm giúp em: mỗi việc trên hiện đang làm bằng gì, hay chưa có gì (vài dòng là đủ).
   Ngại viết thì gõ "hỏi đi", em đưa câu có sẵn đáp án để chọn.
   ```

5. Gõ "hỏi đi" ⇒ mỗi việc trong đề một câu chọn một: *"<việc> hiện đang thế nào?"* — "chưa có gì" · "đang làm tay
   hay bằng công cụ khác" · "đã có, muốn làm thêm / làm lại". Không gắn "(Khuyên dùng)".
6. Người dùng sửa chỗ hiểu sai ⇒ ghi vào Nhật ký (`Q<n>` · câu hỏi `Hiểu đề`), dùng cách hiểu đã sửa cho mọi bước
   sau. Không sửa gì ⇒ coi cách hiểu là đúng; bức tranh tổng quan ở Bước 3 còn một lần xác nhận. Item `Cách hiểu đề`
   đóng với nguồn là câu trả lời đó.
7. Ghi phần người dùng kể vào **Đã có** / **Chưa có**, giữ chữ của họ. Không hỏi sâu cách hệ thống đang có chạy ra
   sao — chỉ cần biết có hay chưa, đang dùng vào việc gì. Việc nào trong đề chưa biết đã có hay chưa thì item
   `Mỗi việc trong đề…` còn mở: hỏi tiếp đúng việc đó.
8. Điểm lại: cách hiểu đề (phần đã sửa nếu có) · đã có · chưa có. Hai item đóng hết ⇒ sang Bước 2.

Thứ việc trong đề cần mà đề không nhắc (đăng nhập, danh mục…) thì chưa hỏi ở bước này: Bước 2 hỏi khi xét phụ thuộc.

## Bước 2 — Tách module & chọn scope

1. **Module chính — chỉ lấy từ đề.** Mỗi việc người dùng nêu trong đề là một module. Hai chữ cùng một thứ thì gộp;
   một chữ quá rộng thì tách (vd "quản lý" thường là vài module). Thứ người dùng nói là **đang có** (Bước 1) không
   thành module. Ở nhịp này **không thêm module nào** ngoài chữ trong đề — đọc lại bảng module chính, mỗi dòng phải chỉ
   được về một chữ trong đề.
2. **Phụ thuộc.** Với từng module chính, xét nó cần thứ gì khác mới chạy được — vd Phân quyền cần biết ai đang dùng,
   tức cần đăng nhập; Nhắc lịch cần cách liên lạc với khách. Thứ đó:
   - là một module chính, hay đã có trong Hiện trạng ⇒ ghi vào cột **Dựa vào**, không hỏi. Thứ đã có ghi dạng
     `đã có: <thứ>`;
   - chưa rõ đã có chưa ⇒ hỏi, mỗi thứ một câu chọn một, nói rõ module nào cần nó và vì sao: *"Phân quyền cần biết ai
     đang dùng — đăng nhập thì sao?"* — "đã có sẵn, dùng lại" · "chưa có, thêm module Đăng nhập" · "để ngoài phạm vi
     lần này". Không gắn "(Khuyên dùng)" khi người dùng chưa kể gì làm căn cứ. Mỗi thứ phải hỏi là một item
     `Phụ thuộc: <module> cần <thứ>` trong checklist.

   Chỉ thêm **module bổ sung** khi người dùng chọn thêm. Trả lời "đã có" ⇒ ghi vào Hiện trạng · Đã có và vào cột Dựa
   vào. Trả lời "để ngoài phạm vi" ⇒ ghi vào Ngoài phạm vi. Hỏi xong thì điểm lại: danh sách module (chính, bổ sung),
   mỗi module dựa vào gì, thứ gì để ngoài phạm vi — rồi mới sang lượt checkbox.
3. Xếp **thứ tự phụ thuộc** theo [`templates/modules.md`](templates/modules.md) "Thứ tự module": nền → nghiệp vụ chính
   → phản ứng → bảo vệ & vận hành.
4. Mỗi module dựng 2–4 **feature** ứng viên: lấy từ gợi ý của module đó trong `modules.md` (hay tự dựng theo khung
   chung nếu module không có ở đó), chọn cái hợp đề nhất. Feature không làm lại thứ Hiện trạng nói đã có. Mỗi feature
   một tên ngắn và một câu mô tả người dùng làm được gì.
5. Thêm item `Tick feature: <module>` cho mỗi module. In bảng trong chat — `Module · feature · dựa vào` — module bổ
   sung ghi `(bổ sung)` sau tên. Rồi hỏi **checkbox**:
   mỗi module một câu `multiSelect` "**<Module>** — chọn feature muốn làm", đáp án là các feature (`label` = tên,
   `description` = mô tả + chọn thì kéo theo gì). Feature agent tin là cần thì `label` có "(Khuyên dùng)". Nhiều
   module thì hỏi nhiều câu trong một lần gọi, quá 4 câu thì gọi tiếp. Trên câu hỏi nhắc: *"Thiếu feature thì gõ vào
   Other."*
6. **Cái được tick là scope.** Module không tick feature nào ⇒ cả module vào **Ngoài phạm vi**; feature không tick
   mà dễ bị tưởng là có ⇒ cũng vào **Ngoài phạm vi**. Người dùng thêm feature hay module qua Other ⇒ đưa vào scope;
   module mới thì thêm item `Tick feature` cho nó và xét phụ thuộc của nó như nhịp 2.

Chữ nào trong đề chưa rõ nghĩa tới mức không dựng được feature (vd "quản lý khách" là danh sách khách để nhân viên
tra, hay khách tự quản lý hồ sơ của mình?) thì hỏi **trước** lượt checkbox, một câu riêng. Chữ đã nói cách hiểu ở
Bước 1 mà người dùng không sửa thì không hỏi lại.

**Ví dụ** (chỉ minh hoạ cách làm — xem "Ví dụ trong skill không phải nguồn"). Đề: *"phòng khám nha của tôi đang nhận
lịch qua Zalo và điện thoại, khách lưu trong phần mềm phòng khám. Tôi muốn làm: đặt lịch online, nhắc lịch, thanh
toán, phân quyền cho nhân viên"*.

- Hiện trạng (Bước 1): đã có nhận lịch qua Zalo, điện thoại; hồ sơ khách trong phần mềm phòng khám (đề).
- Module chính, đọc ra từ đề: Đặt lịch · Nhắc lịch · Thanh toán · Phân quyền.
- Phụ thuộc: Nhắc lịch cần số điện thoại khách — đã có trong phần mềm phòng khám, ghi Dựa vào, không hỏi. Phân quyền
  cần biết nhân viên nào đang dùng — chưa rõ, hỏi *"đăng nhập thì sao?"*; người dùng chọn "chưa có, thêm module Đăng
  nhập".

| Module | Feature (checkbox) | Dựa vào |
| --- | --- | --- |
| Đăng nhập *(bổ sung)* | đăng nhập · mời nhân viên · khoá tài khoản | — |
| Đặt lịch | xem chỗ trống · khách tự đặt · đổi / huỷ | — |
| Nhắc lịch | nhắc trước giờ hẹn · khách xác nhận qua tin nhắn | Đặt lịch · đã có: hồ sơ khách |
| Thanh toán | trả tại quầy · chuyển khoản · hoá đơn | Đặt lịch |
| Phân quyền | vai trò · theo màn · ai cấp quyền | Đăng nhập · mọi module trên |

## Bước 3 — Tổng quan

Scope đã có từ Bước 2. Bước này chỉ hỏi thêm khi một module trong scope **chưa hình dung được ở mức tổng quan** —
vd module Thanh toán: "thanh toán online hay tại quầy?". Không có gì cần hỏi thì sang ngay bức tranh tổng quan.

In **bức tranh tổng quan**:

```
Bức tranh tổng quan:
- Hiện trạng:  đã có <…> · chưa có <…>
- <Module 1>:  <các feature đã chọn>
- <Module 2> (bổ sung):  <các feature đã chọn>
- …
- Ngoài phạm vi: <module / feature không chọn>
Đúng chưa, hay sửa module nào?
```

Cần một câu "đúng" rõ ràng. "Tuỳ anh/chị", "nghe ổn" thì hỏi lại: "có module nào muốn thêm / bỏ feature không?".
Người dùng sửa module hay feature ⇒ quay lại item tương ứng ở Bước 2, rồi in lại bức tranh.

Được "đúng" ⇒ điền vào brief: **Tổng quan** (bảng module, Ngoài phạm vi), **Hiện trạng** (Đã có · Chưa có), **Ai
dùng** (những ai đã lộ ra từ đề), mỗi module một section có heading cho từng feature đã chọn (chưa có gạch đầu dòng).
Trong checklist, thêm vào Bước 4 mỗi module một khối `### Module · <tên>` theo thứ tự đã chốt: `Người dùng kể` ·
`Mục tiêu` · mỗi feature một item mang đúng tên feature · `Nói lại được "đúng"`.

## Bước 4 — Làm rõ từng module

Đi lần lượt từng module theo thứ tự đã chốt. Mỗi module bốn nhịp:

**1. Mời kể.** Mở đầu bằng lời mời, không phải bằng câu hỏi — người dùng thường biết module đó muốn ra sao hơn mọi đáp
án agent đoán. In một tin ngắn rồi **dừng lượt, chờ người dùng viết** (chữ thường trong chat, không dùng
AskUserQuestion):

```
Module Nhắc lịch — feature đã chọn: nhắc trước giờ hẹn · khách xác nhận qua tin nhắn.
Anh/chị kể ngắn module này muốn chạy thế nào (vài dòng là đủ, gạch đầu dòng cũng được).
Ngại viết thì gõ "hỏi đi", em đưa câu có sẵn đáp án để chọn.
```

Người dùng viết xong ⇒ ghi nguyên văn vào Nhật ký (`Q<n>` · câu hỏi `Mô tả module <tên>`), rút ý vào các feature,
rồi chỉ hỏi chỗ còn hở. Gõ "hỏi đi" ⇒ hỏi từ đầu bằng câu có sẵn đáp án.

**2. Mục tiêu.** Lời kể chưa nói module này để đạt được gì thì hỏi một câu có sẵn đáp án, vd *"Làm xong module Nhắc
lịch, anh/chị muốn được gì nhất?"* — "khách ít quên hẹn" · "lễ tân không phải gọi nhắc từng người" · "biết trước
khách nào sẽ không đến". Mục tiêu dùng để chọn đáp án khuyên dùng ở các câu sau. Thấy feature không phục vụ
mục tiêu, hay mục tiêu cần một feature chưa tick, thì hỏi.

**3. Hỏi chỗ hở.** Mỗi feature đi qua khung trong `modules.md`: **cái gì · ai · khi nào · nhận lại gì**, cộng cột
"Hỏi để làm rõ" của feature đó nếu có. Khía cạnh nào lời kể đã rõ thì bỏ qua. Cuối cùng cần **một ví dụ thật**: hỏi
mở trong chat "kể một lần cụ thể anh/chị sẽ dùng cái này". Người dùng không nghĩ ra thì hỏi lại bằng AskUserQuestion
với 2–3 ví dụ soạn sẵn để chọn rồi sửa.

**4. Nói lại.** Xong module, agent nói lại 3–5 dòng **bằng lời mình**: mục tiêu, từng feature trông ra sao khi dùng,
kèm ví dụ. In trong chat rồi hỏi *"Đúng ý chưa, hay chỗ nào chưa phải?"* và dừng lượt — không dùng AskUserQuestion,
vì chỗ cần sửa không đoán trước được. Chỗ nào sai thì hỏi lại đúng chỗ đó. Đây là cách chính
để bắt hiểu lầm: người dùng nhận ra "không phải thế" dễ hơn tự nói ra "phải thế này".

Mỗi nhịp đóng item tương ứng trong khối `### Module · <tên>` của checklist: kể → `Người dùng kể`, mục tiêu →
`Mục tiêu`, mỗi feature đủ khung và có ví dụ → item mang tên feature, nói lại được "đúng" → `Nói lại được "đúng"`.
Module xong khi mọi item của khối đã đóng. Khía cạnh nào người dùng chưa trả lời được thì vào **Câu hỏi còn mở** kèm ai
trả lời được, đừng đoán thay.

Đầu mỗi lượt hỏi in tiến độ đếm từ checklist, vd `Đăng nhập ✓ · Đặt lịch ◐ 2/3 feature · Nhắc lịch ○ · Thanh toán ○ ·
Phân quyền ○`. Module sau dùng
lại kết quả module trước — vd Nhắc lịch hỏi nhắc qua đâu thì đáp án lấy từ thông tin liên lạc đã nói ở Hiện trạng hay ở Đặt lịch.

Ghi vào file sau mỗi lượt:

- mục tiêu → dòng `**Mục tiêu:** … (Nguồn: Q<n>)` của module;
- ý đã rõ → gạch đầu dòng dưới `### <feature>`, giữ chữ người dùng, đuôi `(Q<n>)`;
- ví dụ → `- Ví dụ: … (Q<n>)`;
- người mới lộ ra → bảng **Ai dùng**;
- người dùng thêm feature giữa chừng → thêm vào bảng Tổng quan, thêm heading, thêm item trong checklist; bỏ feature →
  chuyển sang Ngoài phạm vi, đóng item của nó bằng `[-]`.

Mọi module xong ⇒ sang Bước 5.

## Bước 5 — Chốt

1. Chạy `verify.py`, sửa tới khi hết ERROR.
2. Tự đọc lại file, tìm những chỗ sau — code không bắt được:

   | Soát | Tìm |
   | ---- | --- |
   | nói chưa khớp | hai câu trả lời kéo hai hướng: nhắc lịch qua tin nhắn nhưng ở Hiện trạng nói hồ sơ khách chỉ có email |
   | lệch mục tiêu | mục tiêu "lễ tân không phải gọi nhắc từng người" mà feature nhắc lịch là danh sách để lễ tân gọi |
   | chưa hình dung được | feature chưa có ví dụ, hay còn chữ "đầy đủ", "thông minh", "như app khác" |
   | chưa rõ ai dùng | feature không gắn với ai trong bảng Ai dùng |
   | làm lại thứ đã có | feature làm lại thứ Hiện trạng nói đã có, hay module bổ sung người dùng chưa chọn thêm |

   Mỗi chỗ tìm được là một item `Chưa khớp: <chỗ>` và **một câu hỏi**, quay lại Bước 4 — không tự sửa thay người
   dùng. Soát hết mà không còn chỗ nào thì đóng item `Soát chỗ chưa khớp`.
3. **Xác nhận giả định**: gom mọi `A-NN` đang `chờ xác nhận` (đáp án "Đúng (Khuyên dùng)" · "Sai — …"). Đúng ⇒
   `đã xác nhận`; sai ⇒ sửa ý liên quan, giả định thành `bị bác`.
4. In tóm tắt trong chat: mỗi module một dòng (mục tiêu + feature) · Ngoài phạm vi · câu hỏi còn mở và ai trả lời ·
   đường dẫn file. Hỏi: *"Đây đúng là điều anh/chị muốn chưa?"* rồi dừng lượt chờ trả lời bằng chữ — cần "đúng" rõ
   ràng như Bước 3.
5. Được "đúng" ⇒ đóng item cuối, đổi `status: confirmed`, chạy lại `verify.py` (file `confirmed` mà checklist còn
   item mở là ERROR), rồi **dừng lượt**. Đề xuất bước sau, không tự làm:
   - **phân tích** — viết user story, AC, luật có con số, trường hợp lỗi, ưu tiên từ file này (skill riêng, chưa có);
   - `design-uiux` — dựng prototype để người dùng thấy tận mắt và sửa tiếp.

## Viết file

- Giữ chữ của người dùng. Một gạch đầu dòng một ý, đuôi là nguồn: `(Q<n>)`, `(A-<n>)` hoặc `(đề)`; nhiều nguồn ngăn
  bằng dấu phẩy.
- Dòng mô tả dưới `### <feature>`: một câu ai làm được gì, không có nguồn.
- **ID xuyên suốt file**: Q, A, OQ đánh số liền từ 01 (Q từ 1), không đánh lại theo module.
- **Không viết user story, AC, luật đánh số, ưu tiên** — đó là việc của bước phân tích. `verify.py` báo WARN khi thấy.
- **Không viết giải pháp kỹ thuật** — bảng nào, API nào, framework nào. Hệ thống người dùng **đang có** và phải giữ
  là sự thật của đề, ghi vào **Hiện trạng**.
- Cột **Dựa vào** ở Tổng quan: tên module, `đã có: <thứ>` cho thứ ở Hiện trạng, hoặc `—`. Module bổ sung ghi
  `*(bổ sung)*` sau tên ở cột Module.
- Người dùng nói tiếng gì thì file viết tiếng đó; tên section, `Module ·`, `Mục tiêu`, `Ví dụ` giữ nguyên để
  `verify.py` đọc được.

## Dấu hiệu đang làm sai

- Hỏi "bao lâu", "bao nhiêu", "trùng / thiếu / quá hạn thì sao" khi người dùng chưa nhắc tới — đó là phân tích.
- Viết user story, AC, luật đánh số vào file.
- Hỏi "vì sao cần", "đang khổ vì gì".
- Mở đầu bằng câu hỏi mà chưa nói lại đề.
- Nói lại đề mà đã tách module, gợi feature hay thêm việc đề không nêu.
- Tách module trước khi hỏi hiện trạng.
- Có module trong bảng mà không chỉ được về chữ nào trong đề, và người dùng cũng chưa chọn thêm.
- Biến thứ người dùng nói là đang có thành module để làm.
- Lấy module, feature, hiện trạng từ ví dụ trong skill thay vì từ đề đang làm.
- Hỏi chi tiết module khi bức tranh tổng quan chưa được "đúng".
- Vào module mới bằng câu hỏi thay vì mời người dùng kể trước.
- Xong module mà không nói lại cho người dùng xác nhận.
- Coi việc người dùng huỷ một lượt hỏi là dừng, hoặc hỏi lại y nguyên lượt vừa bị huỷ.
- Nhận "tuỳ anh/chị" hay "nghe ổn" là đồng ý.
- Câu trả lời chưa rõ mà hỏi lại y nguyên câu cũ, hoặc hỏi lại quá hai lần cùng một chỗ.
- Bỏ phần người dùng trả lời lạc câu hỏi thay vì ghi vào đúng chỗ nó thuộc.
- Viết module, feature vào brief trước khi bức tranh tổng quan được "đúng".
- Sang bước sau khi checklist của bước còn item mở.
- Người dùng trả lời xong mà không điểm lại, hay điểm lại rồi dừng chờ "đúng".
- Câu trả lời mở ra module, feature, chỗ chọi nhau mà không thêm item vào checklist.
- Đóng item mà không có nguồn.
- Chạy tiếp sau khi bị ngắt mà hỏi lại thứ đã đóng.
- Tự sửa chỗ nói chưa khớp thay vì hỏi.
- Viết tên bảng mới, endpoint, thư viện vào file.
- Được "đúng" ở Bước 5 rồi còn gọi tool làm tiếp bước sau.
