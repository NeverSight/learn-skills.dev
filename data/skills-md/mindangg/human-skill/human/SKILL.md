---
name: human
description: "Viết hoặc viết lại văn bản tiếng Việt cho đọc như người viết, sửa từ cấu trúc chứ không chỉ sửa câu chữ. Dựa trên nghiên cứu StoryScope (Đại học Maryland và Google DeepMind). Dùng khi người dùng gõ /human, nhờ viết cho tự nhiên, bớt giọng AI, hoặc hỏi bài này có giống AI viết không."
---

# /human

Phần lớn mẹo "chống giọng AI" chỉ xoá chữ: bỏ dấu gạch ngang dài, bỏ "hành trình", bỏ "trong thời đại số". Có ích, nhưng không phải chỗ AI lộ nhiều nhất.

Nghiên cứu StoryScope (Russell, Rajendhran, Pham, Iyyer, Wieting, arXiv 2604.03136) so 61.608 truyện do người và năm model viết trên cùng đề bài. Một bộ phân loại chỉ nhìn **cách truyện được dựng** (cốt truyện, thứ tự thời gian, nhân vật, chủ đề), không nhìn chữ nào, vẫn tách được người với AI ở mức 93,2% macro-F1. Khi xoá các dấu hiệu văn phong AI khỏi bài, bộ phân loại gần như không kém đi. AI lộ ở khung bài, không ở dấu câu.

Nên skill này sửa khung trước, sửa chữ sau.

## Ba cách dùng

1. **Viết mới.** `/human viết caption TikTok về tháng đầu mình bán khoá học`. Dựng bài theo các nguyên tắc dưới ngay từ bản đầu. Đừng viết bản kiểu AI rồi vá.
2. **Viết lại.** Người dùng dán bài và nhờ sửa. Soi bài theo các nguyên tắc rồi viết lại. Giữ ý, giữ số liệu, giữ giọng của người viết. Đổi khung, không đổi nội dung.
3. **Soi.** Người dùng hỏi "bài này có giống AI không", "soi giúp". Liệt kê lỗi cấu trúc kèm câu chứa lỗi. Chỉ viết lại khi được nhờ.

## Chi tiết phải thật

Nhiều nguyên tắc dưới đây đòi con số, cái tên, chi tiết riêng. Với bài kể chuyện thật của người dùng (caption, bài Facebook, email cho khách), **không bịa** số tiền, số đơn, giờ giấc, tên người hay sự việc họ chưa kể. Dùng chi tiết họ đã đưa. Thiếu thì để chỗ trống trong ngoặc vuông, ví dụ `[giá khoá học]`, nhưng **tối đa ba chỗ**, chỉ cho những chi tiết đắt nhất. Phần còn lại viết bằng những gì đã biết, đủ cụ thể mà không cần số. Có chỗ trống thì sau bài ghi đúng một dòng: "Điền mấy chỗ trong ngoặc vuông bằng chuyện thật của bạn." Truyện hư cấu thì được tự nghĩ chi tiết.

Nghiên cứu làm trên truyện hư cấu. Mỗi nguyên tắc dưới đây có ghi cách áp sang caption, bài Facebook, script video, email. Con số để bạn hiểu lực kéo mạnh cỡ nào, không phải để trích lại cho người dùng.

## Chín nguyên tắc cấu trúc

### 1. Đừng nói ra bài học
Người kể AI nói thẳng chủ đề của truyện 77% số lần, người là 52%. Lời thoại của AI biến thành tranh luận triết lý 59% số lần, người là 34%.

Cắt câu chốt giải thích ý nghĩa: "Và mình nhận ra rằng...", "Bài học ở đây là...", "Suy cho cùng...". Kết ở một chi tiết, một hành động, một con số, để người đọc tự đi bước cuối. Bài chia sẻ kiến thức vẫn được có một luận điểm rõ, nói một lần ở đúng chỗ, đừng nhắc lại thành đoạn tổng kết.

### 2. Gọi tên cảm xúc
AI tả cảm xúc qua cơ thể hoặc thời tiết 81% số lần, người là 38%. Người gọi thẳng tên cảm xúc 29%, AI chỉ 8%. AI cũng tả mùi nhiều hơn hẳn (82% so với 57%).

"Tim mình đập thình thịch, tay run run" là bản AI của "mình sợ". Mặc định nói thẳng: sợ, tức, xấu hổ, mừng. Chỉ dùng chi tiết cơ thể khi nó cụ thể và có lý do.

### 3. Nêu tên thật
Người nhắc tới sách, người, tác giả cụ thể 47% số lần, AI là 24%. AI ám chỉ mơ hồ ("như người xưa nói", "một câu chuyện cổ") 72%, người là 50%.

Thay cái chung bằng cái tên: tên app, tên quán, tên người, con số, ngày tháng, số tiền. "Một nghiên cứu cho thấy" thành tên nghiên cứu. "Nhiều chuyên gia cho rằng" thành ai nói, hoặc bỏ.

### 4. Nói với người đọc
Người kể của người viết nói thẳng với độc giả 28% số lần, AI chỉ 7%. Người phá bức tường thứ tư 67%, AI 39%.

AI đứng xa, lịch sự. Người viết thì xích lại: gọi "bạn", chêm một câu bên lề, hỏi người đọc, thừa nhận đây là một bài đăng. Caption, script video, bài Facebook gần như lúc nào cũng nên nói với một người cụ thể. Xưng "mình" và gọi "bạn", tránh "chúng ta" và "người dùng".

### 5. Đừng thắt nơ
AI giải quyết truyện bằng việc nhân vật "chấp nhận", "thấu hiểu" 47% số lần, người là 27%. Người viết nhân vật có đạo đức nước đôi 59%, AI 38%.

AI muốn mọi thứ khép lại: ai cũng hiểu ra, vấn đề nào cũng có bài học, kết có hậu. Bài thật để lại chút lấn cấn. Một lựa chọn chưa chắc đúng, một kết quả nửa vời, một câu "mình cũng chưa biết". Bài kết bằng câu hỏi thật lòng thường giống người hơn bài kết bằng bài học gọn, nhưng đừng bài nào cũng kết bằng câu hỏi, đó lại thành một tật khác. Phần lấn cấn phải là thứ người viết thật sự còn phân vân, đừng dựng cho họ một lựa chọn sai trái để có kịch tính, nhất là trong bài bán hàng hay email cho khách.

### 6. Cho bài đi lạc một chút
79% truyện AI không có tuyến phụ nào, người là 57%. Người cài tuyến phụ nối vào chủ đề chính 42% số lần, AI 21%.

AI chạy một đường thẳng. Người viết có một sợi chỉ thứ hai: một chi tiết bên lề, một chuyện nhỏ tưởng không liên quan rồi quay lại sau. Thêm một cái khi độ dài cho phép, ngắn và có dính tới ý chính.

### 7. Đảo thứ tự
Truyện của người nhảy thời gian nhiều hơn hẳn: hồi tưởng, nhảy cóc, bắt đầu giữa chừng. AI kể theo thứ tự, có model còn dồn hết bối cảnh lên đầu.

Đừng mở bằng bối cảnh. Mở ở khoảnh khắc đáng chú ý nhất, kết quả hoặc bước ngoặt, rồi mới quay lại kể vừa đủ.

### 8. Đẩy căng thẳng lên đỉnh
Trong các model được đo, Claude có độ leo thang sự kiện thấp nhất: căng thẳng hiếm khi lên tới đỉnh trước khi được giải quyết. Claude cũng có giọng kể đều nhất, thái độ kính cẩn nhất với chất liệu, và hay thêm phần vĩ thanh.

Bạn nhiều khả năng đang chạy trên Claude, nên tự soi điều này trong bản nháp của mình. Cho mức cược tăng dần. Đặt khoảnh khắc lớn nhất gần cuối, đừng rải đều. Đổi độ dài câu và nhịp để giọng không đều đều một tông. Cắt đoạn kết thêm sau cái kết thật.

### 9. Chọn góc ít hiển nhiên
Truyện AI tụm vào một vùng hẹp, truyện người tản ra rộng. Cùng một đề, bản của người là bản lạ nhất trong sáu bản 57,8% số lần, trong khi xác suất ngẫu nhiên chỉ 16,7%.

Góc dễ nghĩ ra nhất là góc của AI. Trước khi viết, gọi tên ý đầu tiên nảy ra, rồi chọn một bản riêng hơn: lối vào bất ngờ, một chi tiết chỉ người này có, một quan điểm ngược mà tác giả thật sự giữ. Đừng lạ cho có. Viết sao cho không ai khác viết ra đúng như vậy.

## Dấu vân tay của từng model (khi viết lại bài do model khác viết)
- **ChatGPT:** hay dựng truyện bằng tin đồn, lời bàn tán (64%, các nguồn khác 44 đến 55%), hay kể như hồi tưởng chuyện từ nhiều năm trước, hay lật ngược kỳ vọng chỉ để lật.
- **Gemini:** tả nhân vật từ bên ngoài (ngoại hình) thay vì họ muốn gì, kết gọn nhất với đoạn kết kéo dài, bối cảnh u ám.
- **DeepSeek:** dồn bối cảnh quan trọng lên đầu trước khi chuyện bắt đầu chạy.

## Lượt dọn chữ (sau khi khung đã đúng)
Khung đúng rồi mới dọn chữ, vì người đọc vẫn nhận ra những thứ này:

- **Mở bài sáo:** "Trong thời đại số / công nghệ 4.0", "Bạn đã bao giờ tự hỏi...", "Hãy cùng khám phá / tìm hiểu", "Như chúng ta đã biết".
- **Từ sáo:** hành trình, chìa khoá, bí quyết, nâng tầm, khai phá tiềm năng, đột phá, mở ra cánh cửa, đóng vai trò quan trọng, không thể phủ nhận, vô cùng, đầy cảm hứng, một cách hiệu quả.
- **Khuôn câu:** "không chỉ... mà còn...", "Không phải X, mà là Y", "Điều quan trọng là...", "Hãy nhớ rằng...", "Nói cách khác...". Liệt kê đúng ba ý theo phản xạ.
- **Văn dịch:** "việc + động từ" mở câu ("Việc sử dụng AI giúp..."), bị động "được thực hiện bởi", "thực hiện / tiến hành" thay cho động từ thường, "điều này" mở câu liên tục, "nó" thừa.
- **Kết sáo:** "Tóm lại", "Nhìn chung", "Hy vọng bài viết hữu ích", "Chúc bạn thành công", câu hỏi chung chung "Bạn nghĩ sao?".
- **Trình bày:** không dùng dấu gạch ngang dài (—), dùng dấu phẩy, dấu chấm, ngoặc đơn. Không viết hoa từng chữ trong tiêu đề. Không in đậm tràn lan. Không gắn emoji đầu mỗi dòng.
- **Chính tả:** tiếng Việt có dấu đầy đủ, không viết tắt kiểu "ko", "dc", "vs".
- Không xếp chồng các câu cụt một dòng để tạo kịch tính. Để câu nối với nhau.
- Không tóm tắt lại điều vừa nói.

Nếu người dùng có hồ sơ giọng văn, bài mẫu hoặc luật viết riêng, những thứ đó đè lên các mặc định ở đây. Viết như người đó thật sự viết.

## Đầu ra
Đưa bài viết xong rồi dừng. Không mở đầu, không giảng nguyên tắc, không liệt kê đã sửa gì, trừ khi người dùng hỏi sửa gì hoặc nhờ soi. Nếu được hỏi, nêu hai ba thay đổi lớn nhất về khung, mỗi cái một dòng.

## Ví dụ

**Trước (khung AI):**
> Trong thời đại số, việc xây dựng thương hiệu cá nhân đóng vai trò vô cùng quan trọng. Khi mới bắt đầu làm TikTok, tim mình đập thình thịch và tay run run mỗi lần bấm đăng. Ba tháng đầu là một hành trình đầy thử thách nhưng cũng nhiều bài học quý giá. Mình nhận ra rằng thành công không phải là đích đến, mà là cả một hành trình. Cuối cùng, mình hiểu rằng bắt đầu chính là quyết định đúng đắn nhất.

**Sau (/human):**
> Video thứ 31 của mình được 212 view, trong đó chắc 40 view là mình tự xem lại để tìm lỗi. Mình sợ thật, không phải sợ flop mà sợ Tết về bị hỏi "làm TikTok được bao nhiêu tiền". Video thứ 32 lên 18 nghìn view và tới giờ mình vẫn không biết vì sao. Mình đang quay video thứ 33, còn cái thứ 32 thì chưa dám mở ra xem lại.

Khác ở đâu: cảm xúc được gọi tên thay vì tim đập tay run, "thử thách" mơ hồ thành con số và chuyện Tết, bài học "hành trình" bị bỏ, cái kết để ngỏ thay vì tuyên bố quyết định đúng đắn nhất.
