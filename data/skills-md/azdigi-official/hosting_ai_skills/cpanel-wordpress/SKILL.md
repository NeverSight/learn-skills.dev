---
name: cpanel-wordpress
description: Quản lý WordPress trên gói hosting cPanel KHÔNG cần SSH — xem & cập nhật phiên bản WordPress core, plugin, theme; backup trước khi update; chạy lệnh wp-cli bất kỳ. Dùng khi người dùng cần update WordPress, plugin/theme, kiểm tra bản cập nhật đang chờ, hoặc thao tác wp-cli trên website WordPress đang chạy ở hosting cPanel.
---

# cPanel — Quản lý WordPress (wp-cli, không cần SSH)

Thao tác WordPress trên hosting cPanel qua `bin/cpanel`. Vì toolkit chỉ có **API token
(không SSH)** và server thường **không cài sẵn wp-cli**, các lệnh `wp:*` dùng kỹ thuật
đã kiểm chứng:

1. Tải `wp-cli.phar` về `$HOME` của server (một lần, tự động).
2. Chạy wp-cli bằng **đúng PHP-CLI của domain** (tự dò qua `LangPHP`; cron mặc định là
   PHP 7.4 — KHÔNG khớp site nên không dùng).
3. Thực thi qua một **cron một-lần** (cách chạy shell duy nhất khi không có SSH), ghi
   output ra log, poll đọc, rồi **tự dọn cron + file tạm**.

> ⏱️ Host thường **trễ cron vài phút** mới chạy lần đầu. Mỗi lệnh `wp:*` có thể mất
> 2–9 phút. Hãy chạy ở chế độ nền hoặc đặt timeout dài (vd `WP_WAIT_SECS=540`).
> Mặc định `docroot` là `public_html`.

## Quy trình CHUẨN khi cập nhật (BẮT BUỘC làm theo)

Website thường là **production đang chạy** — cập nhật có thể làm vỡ site. Luôn:

1. **Kiểm tra trạng thái trước:**
   ```bash
   cpanel wp:status
   ```
   Xem core đã mới nhất chưa, plugin/theme nào có bản cập nhật, có bản **nhảy major**
   hay **plugin premium** không.

2. **Cảnh báo & xin xác nhận phạm vi với người dùng** trước khi update, đặc biệt khi:
   - Nâng **major version** trình dựng trang (vd Elementor 3→4) **trong khi bản Pro còn
     ở major cũ** → gần như chắc chắn vỡ giao diện. Khuyến nghị GIỮ NGUYÊN.
   - Plugin **premium** (Elementor Pro, WP Smush Pro, WPMU DEV, WP Staging Pro, iThemes…)
     thường **không update được bằng wp-cli** (báo `Download failed "Unauthorized"`) vì
     cần license/dashboard. Chỉ plugin/theme trên wp.org mới update được.
   → Đề xuất các nhóm: *chỉ minor/patch an toàn* / *tất cả trừ cái rủi ro* / *tất cả*.

3. **Backup trước** (các lệnh `wp:update-*` đã **tự backup** DB + `wp-content/plugins` +
   `themes` vào `~/backup_pre_update/`, trừ khi đặt `WP_SKIP_BACKUP=1`). Có thể backup
   thủ công: `cpanel wp:backup`. Với thay đổi lớn, cân nhắc full backup bằng
   skill `cpanel-backup`.

4. **Cập nhật theo phạm vi đã chốt** (xem lệnh dưới).

5. **Verify site sau update:** kiểm tra HTTP 200 và không có lỗi fatal:
   ```bash
   curl -s -o /dev/null -w "HTTP %{http_code}\n" -L https://<domain>/
   curl -s -L https://<domain>/ | grep -iE "fatal error|critical error" | head
   ```

## Lệnh

```bash
cpanel wp:status [docroot]                   # version core + bản cập nhật đang chờ
cpanel wp:backup [docroot]                   # export DB + nén plugins/themes về home
cpanel wp:update-core [docroot]              # cập nhật WordPress core (+ update-db)
cpanel wp:update-plugins [docroot] [slug...] # update plugin (bỏ slug = tất cả)
cpanel wp:update-themes [docroot] [slug...]  # update theme (bỏ slug = tất cả)
cpanel wp:update-all [docroot]               # core + tất cả plugin + theme
cpanel wp:cli <docroot> <wp args...>         # chạy lệnh wp-cli bất kỳ
```

Ví dụ cập nhật **chọn lọc** (an toàn nhất cho production):

```bash
# Chỉ update vài plugin cụ thể (slug lấy từ cột name của wp:status)
cpanel wp:update-plugins public_html classic-editor wordfence google-sitemap-generator
# Update theme mặc định
cpanel wp:update-themes public_html twentytwentyfive
```

Escape hatch — chạy wp-cli tùy ý:

```bash
cpanel wp:cli public_html option get siteurl
cpanel wp:cli public_html plugin deactivate elementor
cpanel wp:cli public_html cache flush
```

## Biến môi trường

| Biến | Ý nghĩa |
|------|---------|
| `WP_PHP_VERSION` | Ép version PHP (vd `ea-php82`, `alt-php83`) nếu dò sai. |
| `WP_PHP` | Đường dẫn PHP-CLI đầy đủ (ưu tiên cao nhất). |
| `WP_SKIP_BACKUP=1` | Bỏ qua backup tự động trong `wp:update-*`. |
| `WP_WAIT_SECS` | Thời gian chờ cron tối đa (mặc định 480s). Host trễ thì tăng. |

## Giới hạn & lưu ý

- **Không update được plugin/theme premium** (cần license) — sẽ báo `Unauthorized`,
  các plugin/theme còn lại trong cùng lệnh vẫn update bình thường.
- Đường dẫn `wp:cli` **không hỗ trợ ký tự `%`** (xung đột với cron). Tránh dùng `%`.
- `docroot` tính **tương đối thư mục home** (vd `public_html`, `public_html/blog`).
- File `wp-cli.phar` được giữ lại trong home sau lần chạy đầu để tái dùng.
- Nếu một lệnh bị timeout, tăng `WP_WAIT_SECS`; lệnh sẽ tự dọn cron, không để lại rác.

## Liên quan

- `cpanel-backup` — full backup tài khoản trước thay đổi lớn.
- `cpanel-debug` — đọc error log, sửa lỗi 500/trang trắng nếu update gây lỗi.
- `cpanel-metrics` — kiểm tra dung lượng đĩa trước khi backup.
- `cpanel-deploy` (`deploy:wp`) — cài MỚI WordPress (khác với update ở đây).
