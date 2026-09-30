---
name: translationese-cleaner-vi
description: Làm sạch văn phong tiếng Việt dịch sát từ tiếng Anh, gồm trật tự câu, danh hóa, bị động, business cliché và cụm đúng ngữ pháp nhưng không tự nhiên. Dùng khi bản dịch hoặc bản nháp mang cấu trúc Anh-Việt; không dùng để thay đổi thuật ngữ chuẩn, đơn giản hóa văn bản pháp lý, hay tự dịch nội dung chưa có bản tiếng Việt.
license: MIT
metadata:
  language: vi
  version: "0.2.1"
---

# Làm sạch văn phong dịch Anh-Việt

Mục tiêu là câu tiếng Việt đứng được độc lập, không phải giấu nguồn dịch. Luôn phân biệt translationese với thuật ngữ chuyên ngành, quy ước hành chính và cấu trúc pháp lý có chủ đích.

## Quy trình

1. Xác định domain, độc giả, register và mức ràng buộc với bản gốc.
2. Nếu có bản tiếng Anh, đối chiếu ý, quan hệ logic, mức chắc chắn và thuật ngữ. Nếu không có, chỉ sửa các cấu trúc có đủ ngữ cảnh.
3. Tìm cụm danh từ dài, danh hóa, chủ ngữ giả, bị động, động từ yếu và metaphor dịch từng chữ.
4. Xác định hành động, chủ thể và thông tin mới của từng câu. Sắp theo mạch tự nhiên của tiếng Việt thay vì giữ thứ tự tiếng Anh.
5. Dùng động từ trực tiếp khi chính xác hơn. Tách câu nếu chuỗi bổ nghĩa khiến người đọc phải đọc lại.
6. Rà thuật ngữ với glossary của người dùng. Khi chưa chắc, giữ thuật ngữ và nêu phương án thay thế thay vì tự quyết.
7. Đối chiếu lại bản gốc hoặc biên bản bảo toàn.

Tra [patterns](references/patterns.md) và [false positives](references/false-positives.md) trước khi sửa văn bản pháp lý, học thuật hay kỹ thuật.

## Bảo toàn

Giữ nội dung mệnh đề, quan hệ nguyên nhân, phủ định, điều kiện, mức nghĩa vụ, mức chắc chắn, số liệu và thuật ngữ. Không biến "may" thành "sẽ", "shall" thành "nên", hay "associated with" thành quan hệ nhân quả.

Không thay một cụm chung bằng cơ chế, metric hoặc ví dụ cụ thể nếu thông tin đó không nằm trong input hay context được cung cấp.

Nếu một metaphor tiếng Anh có nhiều cách hiểu, dùng diễn đạt trung tính giữ đúng chức năng hoặc hỏi lại. Không thêm ví dụ bản địa để lấp chỗ trống.

## Nguyên tắc biên tập

- "Thông qua việc" không sai mặc định; chỉ thay khi động từ trực tiếp đủ nghĩa.
- Bị động hợp lệ khi tác nhân không biết, không quan trọng hoặc cần tránh nêu vì lý do chuyên môn.
- Từ Hán-Việt phù hợp có thể chính xác hơn từ thuần Việt, nhất là trong luật, y khoa và hành chính.
- Giữ tên tính năng, slogan và thuật ngữ đã được phê duyệt, trừ khi người dùng cho phép đổi.
- Không giữ một ẩn dụ dịch sát nếu người Việt khó suy ra nghĩa thực tế.

## Anti-goals

- Không coi mọi câu dài, bị động hoặc Hán-Việt là bản dịch kém.
- Không đổi register để câu nghe thân mật hơn.
- Không phát minh thuật ngữ Việt khi ngành dùng thuật ngữ tiếng Anh ổn định.
- Không làm mất sắc thái hoặc điều kiện để đổi lấy câu ngắn.
- Không tuyên bố đoạn văn do máy dịch hay AI tạo.
- Không tối ưu cho detector.

## Cách chọn mức can thiệp

Không mặc định mọi câu có tín hiệu đều phải sửa. Chọn một mức:

- **Giữ nguyên**: cấu trúc chuyên môn, pháp lý hoặc thuật ngữ đã ổn.
- **Viết lại**: translationese có thể gọt mà không đổi mệnh đề, điều kiện hay mức chắc chắn.
- **Góp ý**: metaphor hoặc thuật ngữ cần xác minh.
- **Cần tác giả quyết định**: nhiều cách hiểu hợp lý làm đổi nghĩa.

## Đầu ra

Mặc định trả bản tiếng Việt đã sửa. Nếu người dùng cần review, liệt kê theo ba nhóm: cấu trúc dịch sát, thuật ngữ cần xác minh và chỗ giữ nguyên có chủ đích. Xem [examples](references/examples.md).
