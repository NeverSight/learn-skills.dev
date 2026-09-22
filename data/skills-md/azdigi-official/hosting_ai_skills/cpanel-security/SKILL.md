---
name: cpanel-security
description: Kiểm tra trạng thái bảo mật tài khoản hosting cPanel — xác thực 2 lớp (2FA) và ModSecurity (WAF) theo domain. Dùng khi người dùng hỏi về mức độ bảo mật, WAF có bật không, hoặc rà soát an ninh tài khoản.
---

# cPanel — Trạng thái bảo mật

Các lệnh **chỉ đọc** để rà soát nhanh mức độ bảo mật của tài khoản.

```bash
cpanel security:2fa-status       # 2FA (xác thực 2 lớp) của tài khoản đã bật chưa
cpanel security:modsec-status    # ModSecurity (WAF) đang bật/tắt theo từng domain
```

## Diễn giải

- `security:2fa-status` → `two_factor_auth_enabled: true/false`. Nếu `false`, khuyến nghị
  người dùng bật 2FA trong cPanel > Security > Two-Factor Authentication (cần quét QR —
  quy trình tương tác, không tự động hóa qua API được).
- `security:modsec-status` → danh sách domain kèm `modsecurity_enabled`. ModSecurity là
  tường lửa ứng dụng web (WAF) chặn tấn công phổ biến. Nên **bật** cho mọi domain.

## Lưu ý phạm vi

- Việc **bật/tắt ModSecurity theo domain** thường do quản trị máy chủ (WHM) kiểm soát và
  **không có trong UAPI người dùng** trên nhiều server — nên skill chỉ báo cáo trạng thái.
- Các tính năng bảo mật khác liên quan: `cpanel-ssl` (HTTPS/AutoSSL), `cpanel-dns`
  (DNSSEC), `cpanel-database` (giới hạn Remote MySQL theo IP).
