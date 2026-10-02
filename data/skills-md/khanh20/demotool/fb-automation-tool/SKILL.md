---
name: fb-automation-tool
description: Quản lý và tự động hóa đa tài khoản Facebook bằng Playwright (Chrome hiển thị) kết hợp Gemini AI sinh bài viết tự nhiên theo ngữ cảnh ngày/giờ. Hỗ trợ đăng bài lên tường cá nhân, đăng bài vào hội nhóm (groups), auto tương tác like/comment, và quản lý profile/cookie độc lập.
---

# Facebook Automation Skill (FB Commander)

Dự án này là một công cụ tự động hóa đa tài khoản Facebook với kiến trúc:
- **Backend**: Node.js, Express, SQLite (`better-sqlite3`), Playwright
- **Frontend**: Dashboard Web App tại `http://localhost:3000`
- **AI Engine**: Google Gemini API (`@google/generative-ai`)
- **Browser Automation**: Playwright persistent contexts (`src/core/browser.js`)

## Cấu trúc thư mục chính:
- `src/core/browser.js`: Quản lý mở Chrome thật (hiển thị), cấu hình proxy, stealth và tự lưu cookie.
- `src/core/account-manager.js`: Quản lý danh sách tài khoản (thêm/sửa/xóa, kiểm tra session, checkpoint).
- `src/core/ai-content.js`: Tích hợp Gemini AI sinh bài viết theo thời gian thực (ngày, giờ, phong cách).
- `src/core/database.js`: Cơ sở dữ liệu SQLite lưu accounts, prompts, posts, logs.
- `src/server.js`: API REST điều khiển hệ thống.
- `src/ui/`: Giao diện Dashboard quản lý.
