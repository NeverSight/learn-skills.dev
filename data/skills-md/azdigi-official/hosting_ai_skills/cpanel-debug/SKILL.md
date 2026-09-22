---
name: cpanel-debug
description: Chẩn đoán và sửa lỗi website trên gói hosting cPanel — đọc error log, kiểm tra file, version PHP, cron, sửa lỗi 500/white screen. Dùng khi website bị lỗi, trả về 500, trang trắng, hoặc người dùng cần debug ứng dụng đang chạy trên hosting cPanel.
---

# cPanel — Debug & Sửa lỗi

Quy trình chẩn đoán lỗi website trên hosting cPanel.

## 1. Đọc error log

```bash
# Mặc định đọc public_html/error_log
cpanel log:errors

# Đọc error_log của một subdir/addon domain
cpanel log:errors public_html/newsite.com/error_log
```

Lỗi PHP thường ghi ở đây. Tìm dòng `PHP Fatal error`, `PHP Warning`, stack trace.

## 2. Đọc file cấu hình / mã nguồn

```bash
cpanel file:read public_html wp-config.php
cpanel file:read public_html/app/config app.php
```

## 3. Kiểm tra version & cấu hình PHP (escape hatch)

```bash
# Liệt kê version PHP khả dụng và version đang dùng cho từng domain
cpanel uapi LangPHP php_get_vhost_versions
cpanel uapi LangPHP php_get_installed_versions

# Đổi version PHP cho một vhost
cpanel uapi LangPHP php_set_vhost_versions vhost=example.com version=ea-php82
```

> Trên server CloudLinux, `php_get_installed_versions` có thể trả `alt-phpXX` trong khi
> vhost lại chạy `ea-phpXX`. Luôn chạy `php_get_vhost_versions` trước để biết đúng định
> dạng giá trị `version` mà server chấp nhận.

## 4. Kiểm tra cron (tác vụ nền lỗi)

```bash
cpanel cron:list                  # mỗi dòng có 'linekey'
cpanel cron:add 30 3 '*' '*' '*' 'php /home/u/cron.php'
cpanel cron:delete <linekey> --yes   # linekey lấy từ cron:list (cần --yes sau khi user đồng ý)
```

## Checklist chẩn đoán lỗi 500 / trang trắng

1. `log:errors` — đọc lỗi PHP gần nhất (đây là bước quan trọng nhất).
2. Nếu lỗi thiếu extension/sai version → kiểm tra & đổi version PHP (mục 3).
3. Nếu lỗi kết nối DB → kiểm tra credential trong file cấu hình (`file:read`) so với
   database thực tế (`cpanel db:list`).
4. Nếu lỗi permission/`.htaccess` → đọc `.htaccess` qua `file:read`.
5. Lỗi memory/timeout → cân nhắc tăng giới hạn qua MultiPHP INI Editor:
   `cpanel uapi LangPHP php_ini_set_user_basic_directives ...`

## An toàn

- Đọc log/file là thao tác **chỉ đọc** — an toàn, cứ thực hiện để chẩn đoán.
- Trước khi **sửa** file cấu hình hay đổi version PHP, mô tả thay đổi và xác nhận với
  người dùng. Backup file gốc trước khi ghi đè khi có thể.
- Không in nội dung nhạy cảm (mật khẩu DB trong `wp-config.php`) ra ngoài một cách thừa thãi.
