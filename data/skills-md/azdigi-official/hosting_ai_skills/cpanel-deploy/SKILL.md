---
name: cpanel-deploy
description: Deploy mã nguồn website lên gói hosting cPanel qua API — static site, PHP+MySQL, WordPress trọn gói, Node.js (Passenger), và clone Git. Upload/giải nén archive, di chuyển file, ghi cấu hình. Dùng khi người dùng cần deploy/cài đặt website hoặc ứng dụng (WordPress, PHP, static, Node.js, Laravel) lên hosting cPanel, upload mã nguồn, hoặc clone repo Git về hosting.
---

# cPanel — Deploy mã nguồn

Vì toolkit gọi cPanel API **từ xa** (không SSH), việc đưa file lên server đi theo
luồng: **upload archive → giải nén trên server → di chuyển file → ghi file cấu hình**.

## Các lệnh thao tác file

| Lệnh | Mô tả |
|------|-------|
| `file:upload <local> <remotedir> [overwrite]` | Upload 1 file local lên server (multipart) |
| `file:extract <archive> <destdir>` | Giải nén zip/tar trên server (API2 fileop) |
| `file:move <src> <destdir>` | Di chuyển/đổi tên file/thư mục |
| `file:save <dir> <file> <local_content_file>` | Ghi nội dung 1 file text (vd cấu hình) |
| `file:mkdir <path> <name>` | Tạo thư mục |
| `file:delete <path>` | Xóa file/thư mục (engine chặn nếu thiếu xác nhận; chạy lại kèm `--yes`) |
| `file:chmod <path> <mode>` | Đổi quyền file (octal 3-4 chữ số, vd 644/0755; cần `--yes`) — sửa lỗi 403/500 sau restore/malware |
| `file:read <dir> <file>` | Đọc lại để kiểm tra |

Đường dẫn server tính **tương đối thư mục home** (vd `public_html`, `public_html/blog`).

## Deploy WordPress trọn gói (một lệnh)

```bash
cpanel deploy:wp <docroot> <dbname> <dbuser> <dbpass> [table_prefix]

# Ví dụ: deploy vào document root chính
cpanel deploy:wp public_html wpblog wpuser 'M@tKhau#Manh2026'
```

Lệnh này tự động:
1. Tải `wordpress.org/latest.zip` về máy local.
2. Upload lên `<docroot>` và giải nén trên server.
3. Di chuyển nội dung `wordpress/*` lên `<docroot>`, dọn zip + thư mục thừa.
4. Tạo database + MySQL user + cấp quyền (tự ghép tiền tố `<user>_`).
5. Lấy salt keys chính chủ từ WordPress.org và sinh `wp-config.php`.

Sau khi xong, mở website trên trình duyệt để hoàn tất bước cài đặt WordPress
(chọn ngôn ngữ, tạo tài khoản admin).

## Deploy static site (HTML/CSS/JS hoặc source build sẵn)

`deploy:static` nén **nội dung** thư mục local rồi upload + giải nén — không tạo thư
mục lồng, dùng được cho mọi source tĩnh hoặc đã build (React/Vue dist, Hugo, v.v.).

```bash
# nén & deploy cả thư mục
cpanel deploy:static ./dist public_html/static
# hoặc deploy 1 file zip có sẵn
cpanel deploy:static ./build.zip public_html/app
```

## Deploy PHP app + MySQL (đã kiểm chứng)

```bash
# 1. (tùy chọn) tạo subdomain cho app
cpanel subdomain:add php thachtestvibe.dev
# 2. tạo database
cpanel db:create phpapp
cpanel db:user-create phpuser '<mật khẩu mạnh>'
cpanel db:grant phpuser phpapp
# 3. deploy mã nguồn (KHÔNG kèm file secret)
cpanel deploy:static ./myphpapp public_html/php
# 4. ghi file config chứa credential TRỰC TIẾP trên server (không nằm trong zip)
cpanel file:save public_html/php config.php ./local-config.php
```
Trong config dùng **tên DB/user đầy đủ có tiền tố** (`<user>_phpapp`), host `localhost`.

## Deploy Laravel KHÔNG cần SSH (đã kiểm chứng end-to-end)

Vì không có SSH (không chạy được `composer`/`artisan` trên server), công thức là **build
local rồi bundle**:

```bash
# === LÀM LOCAL ===
# 1. Tạo app + build vendor khớp PHP server (vd server PHP 8.3 → platform 8.3)
composer create-project laravel/laravel myapp     # dùng bản Laravel còn được hỗ trợ
cd myapp
composer config platform.php 8.3.0
composer update --no-dev --optimize-autoloader     # vendor gọn, đúng PHP target
# 2. DÙNG SQLITE: pre-migrate LOCAL (khỏi chạy artisan migrate trên server)
touch database/database.sqlite
php artisan migrate --force
php artisan optimize:clear                          # tránh cache path local
cd ..

# === DEPLOY (1 lệnh) ===
cpanel deploy:laravel ./myapp public_html/myapp https://app.example.com
```

`deploy:laravel` tự: sinh `APP_KEY`, loại `.env` local khỏi zip, upload + giải nén,
ghi `.env` server (mặc định SQLite, file session/cache). Sau đó **2 bước thủ công**:

```bash
# Trỏ document root vào public/ + đặt PHP version cho vhost
cpanel subdomain:add app example.com public_html/myapp/public
cpanel uapi LangPHP php_set_vhost_versions vhost=app.example.com version=alt-php83
```

**Điểm mấu chốt đã kiểm chứng:**
- Laravel 13 cần PHP ≥ 8.3 — `composer config platform.php` phải khớp PHP server, và
  vhost phải đặt đúng version. Tránh bản Laravel EOL (vd 10.x) vì composer 2.9 chặn do
  security advisory.
- **DB**: SQLite pre-migrated local là cách sạch nhất (không cần migrate trên server,
  không cần MySQL). File `database/database.sqlite` ghi được vì PHP chạy bằng quyền user.
  Nếu cần MySQL: tạo DB (`db:*`) + sửa `.env` (`file:save`) + chạy migrate qua cron one-shot.
- **MIME/PHP version khi verify qua userdir:** xem mục dưới — path từng-là-subdomain-docroot
  bị áp PHP account-default (vd 7.4), không phải PHP của subdomain.

## Clone Git repo về hosting (đã kiểm chứng)

```bash
# path tương đối tự resolve thành tuyệt đối; tên repo tự suy từ basename
cpanel git:clone https://github.com/user/repo.git myrepo
cpanel git:list                      # xem repo + available_branches
```
Thư mục đích phải **CHƯA tồn tại**. Clone là async — đợi vài giây rồi `file:read`/
`list_files` để xác minh. Repo private cần URL có token.

## Deploy Node.js app (Passenger — đã kiểm chứng đăng ký)

```bash
# 1. subdomain làm Application URL
cpanel subdomain:add node thachtestvibe.dev
# 2. đưa code vào app root (KHÁC docroot web; vd thư mục 'nodeapp')
cpanel deploy:static ./nodeapp nodeapp
# 3. đăng ký app  (app_root, domain, app_name)
cpanel node:create nodeapp node.thachtestvibe.dev mynode app.js production
cpanel node:list
```

> **Giới hạn không-SSH:** Passenger không chạy `npm install` qua API. Hoặc dùng app
> **zero-dependency** (chỉ module built-in của Node), hoặc bundle sẵn `node_modules`
> vào zip. App nghe qua `http.createServer().listen(process.env.PORT||3000)` —
> Passenger tự hijack. Mỗi domain chỉ gắn được **một** app.

## Deploy thủ công một ứng dụng bất kỳ (file ops thô)

```bash
cpanel file:upload ./myapp.zip public_html
cpanel file:extract public_html/myapp.zip public_html
cpanel file:save public_html .env ./local.env
```

## Kiểm chứng sau deploy

```bash
# 1. File đã vào đúng chỗ
cpanel uapi Fileman list_files dir=public_html | jq -r '.data[].file'
# 2. wp-config.php đúng credential
cpanel file:read public_html wp-config.php | jq -r .data.content
# 3. Database tồn tại
cpanel db:list
```

**Xem website khi domain CHƯA trỏ DNS:** dùng URL mod_userdir của server:
`https://<server-host>/~<cpaneluser>/` (phục vụ `public_html`) hoặc
`https://<server-host>/~<cpaneluser>/<subdir>/` cho thư mục con. Đây là cách kiểm
chứng file tĩnh + PHP khi domain chưa trỏ. Lưu ý:
- File tĩnh & PHP trong `public_html/*` xem được qua userdir.
- **Node.js/Passenger và vhost subdomain KHÔNG chạy qua userdir** — cần DNS trỏ thật
  để hit đúng vhost. Khi chưa có DNS, chỉ xác minh được tới mức API trả `enabled=1`.
- Truy cập thẳng `https://<domain>/` rơi vào vhost mặc định cho tới khi DNS đúng.
- **PHP version qua userdir (CloudLinux):** thư mục là/từng-là **docroot của subdomain**
  bị áp PHP **account-default** (thường 7.4) khi truy cập qua userdir, KHÔNG theo version
  đã đặt cho subdomain. Để verify app cần PHP mới (vd Laravel/8.3) khi chưa có DNS: deploy
  vào **subdir thường dưới `public_html`** (chưa từng là subdomain docroot) để kế thừa PHP
  của domain chính, và đặt domain chính sang version cần thiết (`php_set_vhost_versions`).
  Production thật: dùng DNS + subdomain docroot→public + set PHP cho chính vhost subdomain.

## Bài học thực chiến (đã kiểm chứng trên server thật)

- **`fileop` path semantics:** `destfiles` tính **tương đối thư mục chứa nguồn**, KHÔNG
  phải home. Khi extract, dùng `destfiles="."` (giải nén tại thư mục chứa archive). Khi
  move, dùng **đường dẫn tuyệt đối** (lấy từ trường `fullpath` của `list_files`).
- **`index.html` che `index.php`:** Apache/LiteSpeed ưu tiên `index.html`. `deploy:wp`
  tự đổi tên nó thành `index.html.default-bak`; nếu deploy thủ công, nhớ làm bước này.
- **Tiền tố MySQL:** `deploy:wp` tự ghép tiền tố cho DB/user (xem `cpanel-database`).
- **Git clone (`VersionControl::create`):** `repository_root` phải **tuyệt đối**;
  `source_repository` là **JSON object** `{"url":"..."}` (không phải string); cần `name`;
  thư mục đích phải chưa tồn tại. `git:clone` lo hết các điểm này.
- **Node.js (`PassengerApps`):** hàm đúng là `register_application`, tham số `domain`
  (số ít). Không `npm install` được qua API → app zero-dep hoặc bundle `node_modules`.

## An toàn & lưu ý

- Deploy vào `public_html` sẽ **ghi đè** trang mặc định. Nếu docroot đã có site, xác nhận
  với người dùng trước; cân nhắc deploy vào thư mục con + subdomain.
- Mật khẩu DB đặt trong nháy đơn để shell không diễn giải ký tự đặc biệt; mật khẩu yếu
  có thể bị cPanel từ chối.
- `deploy:wp` không tạo admin WordPress — bước đó do người dùng làm qua trình duyệt
  (an toàn hơn việc hard-code mật khẩu admin).
- Liên kết: `cpanel-database` (DB), `cpanel-domain` (subdomain cho site mới),
  `cpanel-debug` (đọc error_log nếu deploy lỗi).
