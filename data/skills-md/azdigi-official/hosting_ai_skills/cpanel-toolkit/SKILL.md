---
name: cpanel-toolkit
description: Thao tác trên gói hosting cPanel của người dùng qua API token — kiểm tra kết nối, gọi bất kỳ hàm UAPI/API2, và là điểm khởi đầu cho mọi tác vụ cPanel (database, domain, deploy, debug, cron, email). Dùng khi người dùng nhắc tới cPanel, hosting, gói host, addon domain, hoặc cần thao tác lên tài khoản hosting.
---

# cPanel Toolkit

Bộ công cụ thao tác lên tài khoản hosting cPanel thông qua **API token** (quyền của
chính chủ tài khoản, không phải root/WHM). Mọi thao tác đi qua một lệnh duy nhất:
`cpanel` (engine `bin/cpanel`, tự có trong PATH khi plugin được bật).

## Thiết lập credential

1. Tạo API token trong cPanel: **Security > Manage API Tokens**.
2. Mỗi website/dự án có **`.env` riêng** trong thư mục của nó (credential của hosting
   tương ứng). Engine nạp credential theo thứ tự — dùng cái đầu tiên có:
   `$CPANEL_ENV_FILE` → `./.env` (thư mục hiện tại) → `~/.cpanel-ai.env` (fallback chung).
   ```bash
   # trong thư mục dự án của website đang thao tác:
   printf 'CPANEL_HOST=...\nCPANEL_USER=...\nCPANEL_API_TOKEN=...\n' > .env
   chmod 600 .env
   ```
3. Kiểm tra kết nối (chạy trong thư mục website đó):
   ```bash
   cpanel doctor
   ```

> Mỗi website một `.env` riêng → không lẫn credential giữa các tài khoản cPanel/khách
> hàng khác nhau. Nếu chỉ quản lý một tài khoản cho mọi việc, đặt `~/.cpanel-ai.env`.
> **Không in token ra output; không commit `.env`.**

## Cách dùng

Mọi lệnh trả **JSON ra stdout**; log/diễn giải ra stderr. Xem toàn bộ lệnh:

```bash
cpanel help
```

Lệnh thường dùng:

| Mục đích            | Lệnh |
|---------------------|------|
| Kiểm tra kết nối    | `cpanel doctor` |
| Liệt kê domain      | `cpanel domain:list` |
| Liệt kê database    | `cpanel db:list` |
| Đọc error log       | `cpanel log:errors` |

## Escape hatch — gọi BẤT KỲ hàm cPanel nào

Không phải mọi chức năng đều có lệnh riêng. Khi cần, gọi trực tiếp UAPI/API2:

```bash
cpanel uapi <Module> <function> key=value key2=value2
cpanel api2 <Module> <function> key=value
```

Ví dụ — bật lại version PHP, thêm email, tạo redirect... đều là một lệnh `uapi`.
Tra cứu module/hàm tại https://api.docs.cpanel.net/ (UAPI Modules).

## Skill chuyên biệt liên quan

- `cpanel-database` — tạo/quản lý MySQL database & user.
- `cpanel-domain` — addon domain, subdomain, DNS.
- `cpanel-debug` — đọc log, chẩn đoán lỗi website.

## Quy tắc an toàn (BẮT BUỘC)

1. **Thao tác phá hủy có cổng xác nhận trong engine.** Các lệnh xóa (`db:delete`,
   `db:user-delete`, `subdomain:delete`, `file:delete`, `email:delete`,
   `email:fwd-delete`, `ftp:delete`, `redirect:delete`, `dns:remove`, `cron:delete`)
   sẽ **DỪNG** nếu chạy non-interactive mà không có xác nhận. Quy trình: hỏi người dùng
   → sau khi đồng ý, chạy lại lệnh kèm cờ **`--yes`**. Xem trước không thực thi: thêm
   **`--dry-run`**. (Escape hatch `uapi/api2` KHÔNG qua cổng này.)
2. **Không in token ra ngoài.** Không echo `$CPANEL_API_TOKEN` vào output.
3. Trước khi tạo mới (database/domain), chạy lệnh `:list` tương ứng để tránh trùng.
4. Nếu `doctor` thất bại, dừng lại và báo người dùng kiểm tra `.env` — đừng đoán mò.
5. Database/MySQL user bắt buộc có tiền tố `<user>_`. CLI **tự ghép tiền tố** (lệnh
   `db:*`), nên truyền tên ngắn cũng được; nhưng trong file cấu hình ứng dụng phải dùng
   tên đầy đủ mà `db:list` trả về.
