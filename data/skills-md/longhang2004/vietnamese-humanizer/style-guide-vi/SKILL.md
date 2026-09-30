---
name: style-guide-vi
description: Kiểm tra và áp dụng nhất quán style guide tiếng Việt cho xưng hô, thuật ngữ, viết hoa, số, ngày giờ, đơn vị, heading, bullet và code. Dùng khi chuẩn hóa một hoặc nhiều tài liệu; không dùng để thay thế grammar review, áp quy tắc mặc định lên style guide riêng, hay đổi tên sản phẩm và nội dung được trích nguyên văn.
license: MIT
metadata:
  language: vi
  version: "0.2.1"
---

# Style guide tiếng Việt

Quy tắc của người dùng hoặc tổ chức luôn ưu tiên. Mặc định của skill chỉ dùng khi chưa có hướng dẫn và phải được áp dụng nhất quán, không hồi tố tùy tiện lên trích dẫn hoặc tên riêng.

## Quy trình

1. Tìm style guide, glossary, tài liệu chuẩn hoặc ví dụ đã được duyệt. Ghi rõ nguồn quy tắc.
2. Lập bảng quyết định cho xưng hô, thuật ngữ, tên sản phẩm, viết hoa, số, ngày giờ, tiền tệ, đơn vị, dấu câu và định dạng.
3. Xác định phạm vi ngoại lệ: code, URL, identifier, tên thương hiệu, trích dẫn, dữ liệu nhập từ hệ thống khác.
4. Quét theo từng nhóm thay vì sửa ngẫu nhiên. Ghi lại biến thể và tần suất trước khi chọn dạng chuẩn.
5. Nếu không có style riêng, dùng defaults trong references và nói rõ đó là mặc định của dự án.
6. Rà chéo để một sửa đổi không tạo mâu thuẫn mới, chẳng hạn đổi xưng hô nhưng bỏ sót động từ lịch sự.
7. Xuất bản sạch hoặc báo cáo thay đổi theo yêu cầu.

Đọc [terminology](references/terminology.md) trước khi chuẩn hóa thuật ngữ hàng loạt và [formatting](references/formatting.md) cho Markdown.

## Bảo toàn

Giữ dữ kiện, số trị, đơn vị, tên riêng, tên sản phẩm, trademark, code, URL, identifier và trích dẫn. Chuẩn hóa cách biểu diễn không được đổi giá trị: `1,5` và `1.5` chỉ đổi khi đã xác định quy ước thập phân; múi giờ phải được giữ.

Khi hai quy tắc xung đột, thứ tự ưu tiên là yêu cầu trực tiếp của người dùng, style guide dự án, glossary được duyệt, quy ước domain, rồi mới đến default của skill.

## Nhóm quy tắc

- [Pronouns](references/pronouns.md): quan hệ với độc giả và tính nhất quán.
- [Capitalization](references/capitalization.md): tên riêng, heading, tên tính năng.
- [Numbers, dates, units](references/numbers-dates-units.md): số, phần trăm, tiền tệ, giờ và múi giờ.
- [Terminology](references/terminology.md): glossary, tiếng Anh và từ viết tắt.
- [Formatting](references/formatting.md): heading, bullet, nhấn mạnh và code.

## Anti-goals

- Không áp default khi đã có style guide riêng.
- Không sửa trích dẫn, code, URL, path hoặc identifier.
- Không đổi số trị hay múi giờ trong lúc chuẩn hóa định dạng.
- Không coi khác biệt vùng miền là lỗi.
- Không đổi tên thương hiệu theo quy tắc viết hoa phổ thông.
- Không biến consistency review thành viết lại giọng tác giả.
- Không suy đoán văn bản do AI tạo hoặc tối ưu cho detector.

## Cách chọn mức can thiệp

Không mặc định mọi câu có tín hiệu đều phải sửa. Chọn một mức:

- **Giữ nguyên**: đã đúng style guide, glossary, hoặc “bạn” và “người dùng” chỉ khác vai trò.
- **Viết lại**: chuẩn hóa hình thức mà không đổi giá trị, thuật ngữ hay xưng hô đã chọn.
- **Góp ý**: biến thể cần người viết xem lại.
- **Cần tác giả quyết định**: xung đột xưng hô hoặc glossary chưa có dạng ưu tiên.

## Đầu ra

Với tài liệu ngắn, trả bản đã chuẩn hóa và ghi vài quyết định quan trọng. Với corpus nhiều file, trả bảng quy tắc đã dùng, danh sách ngoại lệ và các chỗ cần chủ sở hữu quyết định. Xem [examples](references/examples.md).
