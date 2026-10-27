---
name: google-flow-image-generation
description: Tạo ảnh bằng Google Flow (flow.google.com) qua Claude in Chrome — nhận prompt, xác nhận khung ảnh ngang hay dọc, mở dự án Flow đã cấu hình (hoặc tạo dự án mới và lưu id), sinh ảnh, tải về rồi chuyển ảnh từ ~/Downloads vào thư mục của dự án. Dùng skill này bất cứ khi nào người dùng muốn tạo/gen/vẽ ảnh bằng Google Flow, Flow, Imagen hoặc Nano Banana trên trình duyệt, hoặc nói những câu như "tạo ảnh với flow", "gen ảnh cho dự án này", "làm thumbnail/ảnh minh hoạ bằng Flow", "generate an image in Google Flow", kể cả khi họ chỉ đưa một prompt mô tả ảnh và nhắc tới Flow. Không dùng để tạo video trong Flow hoặc tạo ảnh bằng API/code.
---

# Google Flow image generation

Skill này điều khiển Chrome thật của người dùng (đã đăng nhập Google) để tạo ảnh trong Google Flow, rồi đưa file ảnh vào thư mục của dự án đang làm.

Mọi thao tác với file và config đi qua `scripts/flow_helper.py` (chỉ dùng thư viện chuẩn của Python). Trong tài liệu này, `HELPER` là đường dẫn tuyệt đối tới script đó, nằm trong thư mục chứa file SKILL.md này. Hãy chạy script **từ thư mục gốc của dự án người dùng**, vì script đọc config từ `./skill-config.json` của thư mục đang chạy:

```bash
HELPER="<thư-mục-skill>/scripts/flow_helper.py"
cd <thư-mục-gốc-dự-án> && python3 "$HELPER" config
```

## Đầu vào cần có trước khi mở trình duyệt

1. **Prompt**: mô tả ảnh. Nếu người dùng đưa nhiều prompt thì xử lý lần lượt từng cái.
2. **Hướng ảnh: ngang hay dọc.** Hỏi nếu người dùng chưa nói rõ, vì đổi hướng sau khi sinh ảnh nghĩa là phải sinh lại từ đầu. Dùng AskUserQuestion với các lựa chọn:
   - Ngang (16:9): banner, thumbnail YouTube, ảnh bìa, slide
   - Dọc (9:16): story, reels, TikTok, hình nền điện thoại
   - Nếu Flow có thêm tỉ lệ khác (1:1, 4:3, 3:4…) và người dùng muốn thì dùng tỉ lệ đó.

   Nếu prompt đã ngầm nói rõ (ví dụ "ảnh bìa YouTube" là ngang, "story Instagram" là dọc) thì nêu lại lựa chọn trong một dòng thay vì hỏi.
3. **Số ảnh:** mặc định là 1 ảnh cho mỗi prompt, trừ khi người dùng xin nhiều hơn (Flow thường cho tối đa 4 ảnh mỗi lần).
4. **Thư mục lưu ảnh:** lấy `output_dir` từ config. Nếu người dùng muốn lưu vào chỗ khác:
   - Chỉ cho lần này: truyền `--output-dir <path>` lúc chạy `move`.
   - Cho mọi lần sau: `python3 "$HELPER" set-output-dir <path>`.

   `output_dir` trong config được tính tương đối theo thư mục chứa `skill-config.json`, nên giá trị mặc định `./flow-images` trỏ vào `flow-images/` của dự án. Còn `--output-dir` thì được tính theo thư mục đang chạy lệnh, giống mọi đường dẫn CLI khác.

## Config: `skill-config.json`

File này nằm ở **thư mục gốc của dự án người dùng**, không nằm trong thư mục skill. Nhờ vậy mỗi dự án có dự án Flow và thư mục ảnh riêng, và việc cập nhật skill không ghi đè config. Script tự tạo file với giá trị mặc định nếu chưa có. Nếu dự án là git repo, có thể nhắc người dùng một lần rằng file này chứa id dự án Flow riêng của họ, để họ tự quyết định có commit hay không.

```json
{
  "flow_project_id": "",
  "output_dir": "./flow-images",
  "downloads_dir": "~/Downloads"
}
```

`python3 "$HELPER" config` in ra config đã được resolve, gồm cả `project_url`.

## Quy trình

### 1. Đọc config

Chạy `python3 "$HELPER" config`. Ghi lại `project_url` (giá trị là `null` nếu chưa có id) và `output_dir`.

### 2. Mở Chrome

Làm theo skill `claude-in-chrome` (hoặc `chrome-browser`): nạp các tool `mcp__claude-in-chrome__*` cần dùng trong **một** lần gọi ToolSearch (tabs_context_mcp, tabs_create_mcp, navigate, computer, find, read_page, javascript_tool), gọi `tabs_context_mcp`, rồi mở **tab mới** để không đụng vào tab người dùng đang dùng.

### 3. Vào dự án Flow

- **Đã có `project_url`:** navigate tới URL đó. Nếu trang báo không tìm thấy dự án hoặc tự chuyển về trang chủ thì coi như chưa có id và làm theo nhánh dưới.
- **Chưa có id:** vào `https://flow.google.com`, bấm nút tạo dự án mới (thường có nhãn "New project" hoặc "Dự án mới"). Khi URL đổi thành `.../project/<id>`, lấy URL bằng `javascript_tool` (`location.href`) rồi lưu lại:
  ```bash
  python3 "$HELPER" set-project "<url hoặc id>"
  ```
  Báo cho người dùng biết đã tạo dự án mới và lưu id vào config.

Nếu Flow bắt đăng nhập, đồng ý điều khoản hoặc chọn tài khoản thì dừng lại và nhờ người dùng tự làm. Các bước đó thuộc về tài khoản của họ.

### 4. Đặt chế độ tạo ảnh và tỉ lệ

Giao diện Flow thay đổi khá thường xuyên, nên hãy đọc trang (`find` / `read_page` / screenshot) thay vì đoán vị trí click. Những gì thường thấy:

- Ô prompt nằm ở cuối trang, cạnh đó là bộ chọn chế độ (ví dụ "Text to Video", "Create Image"…). Chọn chế độ **tạo ảnh**.
- Nút cài đặt (biểu tượng tune/settings) cạnh ô prompt mở ra các tuỳ chọn **Aspect ratio** (Landscape 16:9 / Portrait 9:16 …), **Outputs per prompt** và model. Đặt tỉ lệ khớp với hướng ảnh đã xác nhận, và số ảnh khớp với số người dùng muốn.

Chụp screenshot để xác nhận đã chọn đúng chế độ ảnh và đúng tỉ lệ rồi mới gửi prompt. Gửi sai cấu hình là tốn một lượt sinh ảnh.

### 5. Gửi prompt và chờ

- Nhập prompt vào ô prompt (giữ nguyên lời người dùng; chỉ dịch hoặc viết lại khi họ yêu cầu) rồi bấm nút gửi/tạo.
- Ảnh thường mất từ 10 đến 60 giây. Cứ khoảng 10 đến 15 giây kiểm tra một lần bằng screenshot, đừng chụp liên tục. Ảnh xong là khi ô kết quả hiển thị ảnh thật thay vì thanh tiến trình hay phần trăm.
- Nếu Flow từ chối prompt (vi phạm chính sách, hết credit, lỗi) thì báo lại đúng thông báo của Flow và hỏi người dùng muốn sửa prompt hay dừng. Đừng tự ý viết lại prompt để lách bộ lọc.

### 6. Tải ảnh về

1. **Ngay trước khi bấm tải**, đánh dấu thời điểm:
   ```bash
   python3 "$HELPER" mark      # in ra một timestamp, ví dụ 1761200000
   ```
2. Với từng ảnh vừa sinh: rê chuột vào ảnh hoặc mở ảnh ra, bấm nút **Download**. Nếu Flow hỏi kích thước, chọn kích thước gốc trừ khi người dùng muốn bản upscale. Chỉ tải các ảnh của lượt vừa tạo, không tải ảnh cũ trong dự án.
3. Chrome lưu vào `~/Downloads`. Nếu Chrome hiện hộp thoại "Save as" (do bật "Hỏi nơi lưu"), nhờ người dùng bấm Save hoặc tắt tuỳ chọn đó, vì extension không điều khiển được hộp thoại hệ thống.

### 7. Chuyển ảnh vào thư mục dự án

```bash
python3 "$HELPER" move --since <timestamp> --expect <số ảnh> --name "<prompt hoặc tên ngắn>" [--output-dir <path>]
```

Script chờ tối đa 60 giây (`--timeout` để đổi) cho đến khi đủ số ảnh và không còn file `.crdownload`. Sau đó nó chuyển các ảnh có thời gian sửa đổi mới hơn `--since` từ Downloads sang thư mục đích, đặt tên dạng `YYYYMMDD-HHMMSS-<slug-prompt>[-n].<ext>`, và in ra JSON danh sách đường dẫn mới. Nếu thoát với lỗi "No new image found", kiểm tra lại xem nút Download đã thực sự được bấm chưa (xem thanh tải của Chrome) rồi thử lại với cùng `--since`.

Vì script chọn file theo thời gian, đừng tải thứ gì khác vào Downloads trong lúc chạy bước này.

### 8. Báo kết quả

Liệt kê đường dẫn các ảnh đã lưu, tỉ lệ đã dùng và URL dự án Flow. Có thể dùng Read để xem nhanh một ảnh nếu người dùng muốn kiểm tra. Để tab Flow mở, vì người dùng có thể muốn chỉnh tiếp.

## Khi có sự cố

- **Không tìm thấy nút hoặc bố cục khác mô tả:** chụp screenshot, đọc lại trang và tìm theo ý nghĩa (ảnh, tỉ lệ, tải xuống). Nếu sau 2 đến 3 lần vẫn không làm được thì dừng lại, mô tả điều đang thấy và hỏi người dùng.
- **Extension không phản hồi:** nhờ người dùng kiểm tra Claude in Chrome đã kết nối và đã cấp quyền cho `flow.google.com`.
- **Nhiều prompt:** lặp lại bước 4 đến 7 cho từng prompt trong cùng dự án. Mỗi prompt dùng một `mark` riêng để ảnh không bị lẫn.
