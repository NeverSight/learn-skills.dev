---
name: grammar-checker-vi
description: Kiểm tra chính tả, dấu câu, khoảng trắng, cấu trúc câu, tham chiếu đại từ và kết hợp từ trong văn bản tiếng Việt. Dùng khi người dùng yêu cầu soát lỗi hoặc proofread; không dùng để áp một phong cách, đổi nội dung, sửa code/URL/identifier, hay coi lựa chọn register và phương ngữ là lỗi ngữ pháp.
license: MIT
metadata:
  language: vi
  version: "0.2.1"
---

# Kiểm tra ngữ pháp tiếng Việt

Phân biệt lỗi có thể chứng minh với lựa chọn phong cách. Khi có nhiều cách sửa hợp lệ, ưu tiên cách ít đổi nghĩa và phù hợp giọng hiện có.

## Quy trình

1. Xác định loại tài liệu và vùng nội dung được phép sửa. Che code block, inline code, URL, path, command, identifier và trích dẫn nguyên văn nếu người dùng không yêu cầu.
2. Soát lỗi ký tự: Unicode, khoảng trắng, dấu câu, viết hoa và lỗi gõ.
3. Soát từ và cụm: lặp từ ngoài chủ đích, thiếu hoặc thừa từ, kết hợp từ không tự nhiên.
4. Soát câu: chủ ngữ, vị ngữ, quan hệ bổ nghĩa, tham chiếu đại từ và mơ hồ.
5. Soát tính nhất quán nhưng không gắn nhãn "sai ngữ pháp" cho một preference.
6. Với lỗi chắc chắn, sửa trực tiếp. Với câu mơ hồ, nêu hai cách hiểu và hỏi nếu lựa chọn làm đổi nghĩa.
7. Rà lại sau sửa để phát hiện lỗi mới do thay đổi khoảng trắng hoặc dấu câu.

Thứ tự kiểm tra chi tiết nằm ở [checks](references/checks.md). Xem [punctuation](references/punctuation.md) cho khác biệt với thói quen tiếng Anh.

## Bảo toàn

Không đổi dữ kiện, giọng, register, thuật ngữ, tên thương hiệu, trích dẫn, số, đơn vị hay mức chắc chắn. Không chuẩn hóa code, command, URL, path và identifier. Nếu tên thương hiệu cố ý viết khác quy tắc, giữ nguyên.

## Phân loại phát hiện

- Error: có quy tắc và cách sửa đủ chắc chắn.
- Warning: câu có thể mơ hồ, lặp hoặc thiếu thành phần nhưng cần ngữ cảnh.
- Preference: lựa chọn nhất quán, không nên tự sửa nếu chưa có style đã chọn.
- Heuristic: tín hiệu bề mặt cần đọc cả câu, đoạn hoặc tài liệu.

Các lỗi thường gặp và ngoại lệ nằm ở [common errors](references/common-errors.md).

## Anti-goals

- Không biến soát lỗi thành viết lại phong cách.
- Không áp một chuẩn vùng miền duy nhất.
- Không sửa thuật ngữ chuyên ngành chỉ vì ít gặp.
- Không tự ý chuẩn hóa trích dẫn hoặc nội dung trong code.
- Không kết luận câu lạ là sai khi thiếu ngữ cảnh.
- Không tuyên bố văn bản do AI tạo hoặc hướng dẫn lách detector.

## Cách chọn mức can thiệp

Không mặc định mọi câu có tín hiệu đều phải sửa. Chọn một mức:

- **Giữ nguyên**: câu đã đúng nghĩa, hoặc tín hiệu catalog không đủ chắc.
- **Viết lại**: lỗi có quy tắc và cách sửa đủ chắc, không đổi dữ kiện.
- **Góp ý**: câu mơ hồ; nêu vị trí và lựa chọn.
- **Cần tác giả quyết định**: cách hiểu làm đổi nghĩa, gồm thành phần bổ nghĩa gắn sai chủ thể.

## Đầu ra

Nếu người dùng yêu cầu bản sạch, trả văn bản đã sửa. Nếu yêu cầu review, ghi vị trí, loại lỗi, đề xuất và độ chắc chắn. Với câu cần tác giả quyết định, giữ nguyên trong bản sạch và nêu riêng. Xem [examples](references/examples.md).
