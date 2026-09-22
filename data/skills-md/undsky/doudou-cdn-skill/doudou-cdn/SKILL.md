---
name: doudou-cdn
description: 把本地图片上传到图床并获取公开 CDN 链接或 Markdown 图片语法，共三种模式：公共图床 API 模式 (scripts/upload-api.mjs)、GitHub 仓库直传模式 (scripts/upload-github.mjs)、Cloudflare R2 直传模式 (scripts/upload-r2.mjs)，统一入口 scripts/upload.mjs 支持智能自动调度。当没有配置 GitHub、R2 时，自动使用公共图床 API；如果配置了，那么自动使用配置的模式上传。只要用户提到上传图片、传图到图床、把图片转成 Markdown 链接、要给图片配个外链/CDN URL、生成文章配图链接、把截图/本地图片公开发布以供他人浏览或嵌进文档/聊天，或明确点名传到 GitHub 仓库 / Cloudflare R2 存储桶时，就使用这个 skill —— 哪怕他们没说“图床”或“CDN”。
---

# 上传图片到图床 (CDN)

本技能提供三种上传模式，统一入口 `scripts/upload.mjs` 支持**全自动智能调度**：**当没有配置 GitHub、R2 时，使用图床 API；如果配置了，那么自动使用配置的模式上传**。用户也可随时通过命令行选项显式指定模式。

---

## 模式选择与调用规范

统一入口 `node <SKILL_DIR>/scripts/upload.mjs` 遵循以下调度策略：

1. **智能自动判定模式（推荐默认使用）**：
   - **未配置 GitHub / R2**：自动切换为 **公共图床 API 模式**（开箱即用，免配置任何 Token/Bucket，单文件上限 5MB）；
   - **配置了 Cloudflare R2**（`.env` 或环境变量包含 `DOUDOU_CDN_R2_*`）：自动切换为 **Cloudflare R2 直传模式**（原生 S3 直传，生成专属 CDN 链接，单文件最高 100MB）；
   - **配置了 GitHub**（`.env` 或环境变量包含 `DOUDOU_CDN_GITHUB_*`）：自动切换为 **GitHub 仓库直传模式**（单文件最高 100MB，提供三路加速链接）；
   - 若两者均配置，默认优先使用性能与分发更优的 Cloudflare R2 模式。
2. **显式指定模式（命令行最高优先级）**：
   - 传入 `-r` / `--r2`：强制走 Cloudflare R2 直传模式（也可直接调用 `upload-r2.mjs`）；
   - 传入 `-g` / `--github`：强制走 GitHub 仓库直传模式（也可直接调用 `upload-github.mjs`）；
   - 传入 `-a` / `--api`：强制走公共图床 API 模式（也可直接调用 `upload-api.mjs`）。

| 模式                                | 对应脚本 / 参数                                                 | 调度规则 / 特点                                                                 | 限制                 |
| ----------------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------- | -------------------- |
| **智能自动调度**（推荐优先使用）     | `node <SKILL_DIR>/scripts/upload.mjs`                           | **智能自适应**：未配置 GitHub/R2 时走图床 API，已配置则自动切换至对应直传模式   | 视实际匹配通道而定   |
| **公共图床 API 模式**（免配置）     | `node <SKILL_DIR>/scripts/upload-api.mjs` 或 `upload.mjs -a`    | **开箱即用**，未配置任何 Token/仓库时自动生效，适合常规文章配图、截图、图标     | 单文件 5MB（压缩后） |
| **Cloudflare R2 模式**（配置优先）  | `node <SKILL_DIR>/scripts/upload-r2.mjs` 或 `upload.mjs -r`     | 配置 R2 凭据后自动使用；原生 S3 直传，不依赖第三方服务，生成稳定高质量 CDN 链接 | 单文件最高 100MB     |
| **GitHub 直传模式**（配置使用）     | `node <SKILL_DIR>/scripts/upload-github.mjs` 或 `upload.mjs -g` | 配置 GitHub 凭据后自动使用；单文件上限 100MB，支持三路 CDN 加速链接             | 单文件最高 100MB     |

---

## 快速示例

> 以下示例假定当前目录就是技能目录。从项目其它位置调用时，请把 `scripts/` 换成 `<SKILL_DIR>/scripts/`（与上方表格一致）。

### 1. 推荐：统一入口智能上传（自动识别配置）

```bash
# 上传单张图片（未配置 GitHub/R2 时自动走图床 API，配置后自动走已配置模式）
node scripts/upload.mjs shot.png

# 直接输出 Markdown 语法（推荐拼进文章时使用）
node scripts/upload.mjs shot.png -m

# 批量上传多张图片
node scripts/upload.mjs a.png b.jpg c.webp

# 缩放图片宽度（等比缩放为 600 像素宽）
node scripts/upload.mjs photo.jpg --resize 600
```

### 2. 用户指定或专属调用：Cloudflare R2 模式

当用户指定“上传到 Cloudflare R2”、“走 R2 上传”，或显式传入 `-r` 时使用：

```bash
# 通过统一入口指定 -r 模式
node scripts/upload.mjs shot.png -r

# 或直接使用专属脚本
node scripts/upload-r2.mjs shot.png -m

# 批量上传并指定存储目录
node scripts/upload-r2.mjs a.png b.jpg --folder docs/images
```

### 3. 用户指定或专属调用：GitHub 仓库直传模式

当用户指定“上传到我的 GitHub”、“走 GitHub 直传”，或原图体积较大（>5MB）时使用：

```bash
# 直传个人 GitHub 仓库
node scripts/upload-github.mjs huge.png --repo myuser/img-bed --github-token ghp_xxxx

# 如果 .env 中已配置 DOUDOU_CDN_GITHUB_REPO 与 DOUDOU_CDN_GITHUB_TOKEN，可直接执行：
node scripts/upload-github.mjs huge.png -m
```

### 4. 强制指定：公共图床 API 模式

即使配置了 GitHub 或 R2，仍可传入 `-a` 强制走免配置的公共图床 API：

```bash
node scripts/upload.mjs shot.png -a
```

---

## 选项参数

### 通用选项（脚本均支持）

| 选项                    | 作用                                                                                                        | 默认               |
| ----------------------- | ----------------------------------------------------------------------------------------------------------- | ------------------ |
| `-m`, `--markdown`      | 直接输出 Markdown 图片语法 `![alt](url)`（也可在 `.env` 配置 `DOUDOU_CDN_OUTPUT_MARKDOWN`）                 | 关（输出友好文本） |
| `-f`, `--format <格式>` | 输出格式：`url` / `markdown` / `json`（也可在 `.env` 配置 `DOUDOU_CDN_OUTPUT_FORMAT`）                      | 默认文本           |
| `--json`                | 输出接口原始 JSON 结构                                                                                      | 关                 |
| `-s`, `--silent`        | 静默模式，仅在 stdout 输出最终结果（也可在 `.env` 配置 `DOUDOU_CDN_OUTPUT_SILENT`）                         | 关                 |
| `--resize <宽度>`       | 图片等比缩放到指定宽度（16-20000 像素）；默认 600 存轻量缩略图；`0` / `off` 不缩放（也可在 `.env` 配置 `DOUDOU_CDN_IMAGE_RESIZE`） | `600`（**轻量缩略图**） |
| `--no-compress`         | 关闭图片有损压缩优化（也可在 `.env` 配置 `DOUDOU_CDN_IMAGE_NO_COMPRESS`）                                   | 关（默认优化压缩）      |
| `--original`            | 原图直传，等价于 `--no-compress --resize 0`（也可在 `.env` 配置 `DOUDOU_CDN_IMAGE_ORIGINAL`）               | 关                      |
| `--filename <名字>`     | 指定上传文件名（须带扩展名，**仅单文件可用**）                                                              | 自动时间戳+随机数       |
| `--keep-name`           | 保留原文件名（特殊字符会被转为安全下划线，也可在 `.env` 配置 `DOUDOU_CDN_IMAGE_KEEP_NAME`）                 | 关                      |
| `--max-size <MB>`       | 自定义本地图片体积校验上限（单位：MB，也可在 `.env` 配置 `DOUDOU_CDN_IMAGE_MAX_SIZE`）                      | API: 5 / 直传: 100      |
| `--force`               | 强制上传，跳过本地大小校验与 ImageMagick 缺失阻断（也可在 `.env` 配置 `DOUDOU_CDN_IMAGE_FORCE`）            | 关                      |
| `--thumb [宽度]`        | 在本地同时生成轻量缩略图 `<原名>_thumb`（也可在 `.env` 配置 `DOUDOU_CDN_GENERATE_THUMB`，支持同时指定宽度） | 开（由自身控制）        |
| `--no-thumb`            | 显式关闭本地缩略图生成                                                                                      | —                       |
| `--doctor`              | 自检运行环境（Node、ImageMagick、直连连通性）                                                               | —                       |

### GitHub 直传专属选项 (`upload-github.mjs`)

| 选项                   | 作用                                                                           | 默认              |
| ---------------------- | ------------------------------------------------------------------------------ | ----------------- |
| `--repo <owner/repo>`  | GitHub 目标仓库（也可在 `.env` 中配置 `DOUDOU_CDN_GITHUB_REPO`）               | 读 `.env`         |
| `--github-token <tok>` | GitHub Personal Access Token（也可在 `.env` 中配置 `DOUDOU_CDN_GITHUB_TOKEN`） | 读 `.env`         |
| `--branch <分支>`      | GitHub 目标分支                                                                | `main`            |
| `--folder <目录>`      | GitHub 通道保存子目录（支持多级）                                              | UTC `YYYY/MM/DD`  |
| `--no-cdn`             | 兼容选项（默认已同时返回原始链接、Fastly jsDelivr 加速链接与国内加速链接）     | 默认返回 3 个链接 |

### Cloudflare R2 专属选项 (`upload-r2.mjs`)

| 选项                           | 作用                                                                                                                                                                       | 默认      |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| `--folder <目录>`              | R2 存储桶前缀目录（也可在 `.env` 中配置 `DOUDOU_CDN_R2_FOLDER`）                                                                                                           | `cdn`     |
| `--account-id <id>`            | Cloudflare 账户 ID（也可在 `.env` 中配置 `DOUDOU_CDN_R2_ACCOUNT_ID`）                                                                                                      | 读 `.env` |
| `--access-key-id <id>`         | R2 API 访问密钥 ID（也可在 `.env` 中配置 `DOUDOU_CDN_R2_ACCESS_KEY_ID`）                                                                                                   | 读 `.env` |
| `--secret-access-key <key>`    | R2 API 秘密密钥（也可在 `.env` 中配置 `DOUDOU_CDN_R2_SECRET_ACCESS_KEY`）                                                                                                  | 读 `.env` |
| `--bucket <name>`              | R2 存储桶名称（也可在 `.env` 中配置 `DOUDOU_CDN_R2_BUCKET`）                                                                                                               | 读 `.env` |
| `--cdn, --public-domain <url>` | 绑定在存储桶上的公开访问 CDN 域名（也可在 `.env` 中配置 `DOUDOU_CDN_R2_PUBLIC_DOMAIN`）。**必填**：缺失时无法生成可访问链接（S3 端点需签名，`pub-<hash>.r2.dev` 无法推导） | 读 `.env` |

---

## 图片格式与本地优化约定

- **支持格式**：`jpg`, `jpeg`, `png`, `gif`, `webp`, `svg`, `bmp`, `tif`, `tiff`, `heic`, `heif`, `avif`, `ico`。
- **默认等比缩小存轻量缩略图**：为优化网络分发与极速加载，`resize` 默认 600（云端直接存储轻量缩略图，单图降至 ~200KB）；若需要原图保真上传，传入 `--original` 或 `--resize 0`。
- **动图与矢量图保护**：`svg` 和 `ico` 不做光栅化压缩；多帧 `gif` / `webp` 动图自动跳过重编码，保护动画完整性。
- **隐私保护**：自动 `-strip` 去除相机 EXIF 元数据（含 GPS 坐标），并在压缩前通过 `-auto-orient` 自动摆正方向。

---

## 故障排查

| 报错现象                                | 原因与解决建议                                                                                                                                                                                                                       |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `未检测到本机安装的 ImageMagick`        | 本机未安装 `magick` 命令行工具。运行 `node scripts/upload-api.mjs --doctor` 查看安装向导（Windows: `winget install ImageMagick.ImageMagick`）；若暂时不想安装，可添加 `--no-compress` 直传原图                                       |
| `图片处理后体积超过默认 API 上限 (5MB)` | 默认 API 通道限制 5MB：① 加 `--resize 1200` 缩小尺寸；② 切换至 GitHub 直传模式 `upload-github.mjs`（上限 100MB）；③ 加 `--force` 跳过本地校验                                                                                        |
| `GitHub 直传缺少 Token 或仓库格式错误`  | GitHub 直传模式需在 `.env` 中配置 `DOUDOU_CDN_GITHUB_TOKEN` 与 `DOUDOU_CDN_GITHUB_REPO`（格式形如 `user/repo`），或通过 `--github-token` 与 `--repo` 传入                                                                            |
| `缺少 Cloudflare R2 直传必须配置参数`   | Cloudflare R2 模式需在 `.env` 中配置 `DOUDOU_CDN_R2_ACCOUNT_ID`、`DOUDOU_CDN_R2_ACCESS_KEY_ID`、`DOUDOU_CDN_R2_SECRET_ACCESS_KEY`、`DOUDOU_CDN_R2_BUCKET`、`DOUDOU_CDN_R2_PUBLIC_DOMAIN`（公开域名为必填，缺失时无法生成可访问链接） |
| `Cloudflare R2 鉴权失败 (HTTP 403)`     | 检查 `DOUDOU_CDN_R2_ACCESS_KEY_ID` 和 `DOUDOU_CDN_R2_SECRET_ACCESS_KEY` 是否正确，确认在 Cloudflare 控制台创建的 API 令牌拥有该存储桶的写入权限 (Object Read & Write)                                                                |
| `Cloudflare R2 存储桶不存在 (HTTP 404)` | 确认 `DOUDOU_CDN_R2_BUCKET` 指定的存储桶是否已在 Cloudflare 控制台中创建                                                                                                                                                             |
| `--resize / --max-size 的值不合法`      | 常见于 `.env` 行尾注释写法有误。注释的 `#` 前须留空格（`KEY=0   # 说明`）；值本身含 `#` 时请加引号（`KEY="#fff"`）                                                                                                                   |
