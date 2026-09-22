---
name: cpanel-php
description: Xem và đổi phiên bản PHP theo từng domain trên hosting cPanel (MultiPHP / CloudLinux PHP Selector). Dùng khi người dùng cần đổi PHP cho một website, kiểm tra PHP đang chạy, hoặc xử lý lỗi tương thích PHP (WordPress/Laravel yêu cầu PHP mới hơn).
---

# cPanel — Quản lý phiên bản PHP theo domain

Xem và đổi PHP cho từng domain qua `bin/cpanel`.

> **Chính sách quan trọng:** Skill này **chỉ thao tác với các bản `alt-php*`** (CloudLinux
> PHP Selector), **không đặt `ea-php*`** (EasyApache) — để đồng nhất môi trường CloudLinux
> và cho phép người dùng tự quản lý extension. Lệnh `php:set` sẽ **từ chối** mọi bản `ea-php*`.

## Lệnh

```bash
cpanel php:versions                      # Liệt kê các bản alt-php* đã cài trên server
cpanel php:list                          # PHP hiện tại của từng domain (đánh dấu domain KHÔNG dùng alt-php)
cpanel php:set <domain> <alt-phpXX>      # Đổi PHP cho 1 domain (chỉ alt-php*; cần --yes)
```

## Quy trình đổi PHP cho một website

```bash
# 1. Xem các bản alt-php có sẵn
cpanel php:versions

# 2. Xem PHP hiện tại của domain
cpanel php:list

# 3. Đổi sang bản mong muốn — HỎI người dùng trước, rồi chạy kèm --yes
cpanel php:set example.com alt-php82 --yes
```

## Lưu ý

- **`php:set` là thao tác có ảnh hưởng** (đổi PHP sai bản có thể làm website lỗi). Engine
  **chặn** khi non-interactive nếu thiếu `--yes`: hãy hỏi người dùng, sau khi đồng ý mới
  chạy lại kèm `--yes`. Muốn xem trước: thêm `--dry-run`.
- Chỉ nhận định dạng `alt-phpXX` (vd `alt-php74`, `alt-php82`, `alt-php83`). Bản phải đã
  cài trên server (kiểm tra bằng `php:versions`), nếu không sẽ báo lỗi.
- `php:list` báo cáo đúng thực tế: nếu một domain đang chạy `ea-php*`, nó vẫn hiển thị và
  được đánh dấu "KHÔNG phải alt-php" — nhưng skill sẽ không tự đổi domain sang ea-php.
- Bản alt-php dùng đường dẫn CLI `/opt/alt/phpXX/usr/bin/php` (liên quan skill
  `cpanel-wordpress` khi chạy wp-cli).
