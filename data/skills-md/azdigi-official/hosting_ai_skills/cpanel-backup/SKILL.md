---
name: cpanel-backup
description: Sao lưu tài khoản hosting cPanel — tạo full backup về thư mục home hoặc lên FTP từ xa, liệt kê backup hiện có. Dùng khi người dùng cần backup toàn bộ tài khoản, sao lưu trước khi sửa/deploy rủi ro, hoặc tải bản sao lưu. Bao gồm ghi chú về JetBackup.
---

# cPanel — Sao lưu (Backup)

Tạo và liệt kê backup qua `bin/cpanel` (UAPI module `Backup`). Đây là **cPanel Backup
tích hợp sẵn**, chạy được với token cPanel user.

## Liệt kê backup

```bash
cpanel backup:list
```

Trả `managed_backups` (backup do cPanel/hệ thống quản lý) và `homedir_backups` (file
`backup-*.tar.gz` on-demand trong thư mục home, kèm dung lượng MB).

## Tạo full backup về home

```bash
cpanel backup:create                      # không gửi email
cpanel backup:create you@example.com      # gửi email khi xong
```

- Backup chạy **nền** trên server; file `backup-<ngày>_<user>.tar.gz` xuất hiện trong
  home khi hoàn tất (kiểm tra bằng `backup:list`).
- Backup chiếm dung lượng đĩa — kiểm tra quota trước bằng `cpanel-metrics` (`metrics:quota`).
- Tải về: dùng FTP (`cpanel-ftp`) hoặc File Manager. Dọn bớt file backup cũ để tiết kiệm đĩa.

## Tạo full backup lên FTP từ xa

```bash
cpanel backup:create-ftp ftp.example.com ftpuser 'MatKhau!' 21 /backups you@example.com
```

Tham số: `<host> <user> <pass> [port=21] [rdir] [email]`. Hữu ích để đưa backup ra
ngoài server (off-site).

## Khôi phục (restore)

Restore một phần qua escape hatch (cần tham số `backup`):
```bash
cpanel uapi Backup restore_databases backup=<tên_file>
cpanel uapi Backup restore_email_filters backup=<tên_file>
```
Restore là thao tác **ghi đè** — luôn xác nhận với người dùng và backup hiện trạng trước.

## ⚠️ Về JetBackup (quan trọng)

Nhiều hosting tích hợp **JetBackup** (giải pháp backup bên thứ ba) thay cho backup cPanel.
**API JetBackup KHÔNG truy cập được bằng token cPanel user** (đã kiểm chứng):

- Endpoint JetBackup: `https://<host>:2087/cgi/addons/jetbackup5/api.cgi` — **cổng WHM**,
  cần header `Authorization: whm <user>:<token>` (tức **WHM API token**, không phải cPanel).
- Token cPanel user gọi `api.cgi` (cổng 2083) → **HTTP 403 Forbidden** (cPanel chặn token
  user truy cập cgi của plugin bên thứ ba).
- Module UAPI `JetBackup5` có load nhưng **không expose hàm** nào cho user.

→ Muốn điều khiển JetBackup qua API: cần **WHM API token** (root/reseller) có quyền
"Third Party Services — JetBackup". Khi đó dùng `cpanel_uapi`-tương tự nhưng đổi sang
header `whm` và cổng 2087. Hiện toolkit dùng token cPanel user nên dùng cPanel Backup gốc
ở trên. Nếu người dùng có WHM token, có thể mở rộng toolkit cho JetBackup.
