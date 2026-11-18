---
name: soia-media-publish-wechat-draft
description: 把成文草稿排版成符合微信公众号限制的内联样式 HTML，机械校验通过后推入微信公众号草稿箱；只建草稿，绝不自动群发。Triggers：「把这篇发成公众号」「排版这篇公众号」「推到公众号草稿箱」「公众号 draft」
version: 3.3.1
created_at: 2026-07-02 17:49:40
updated_at: 2026-11-18 10:00:00
created_by: claude opus 4.6
updated_by: gemini-4-hydrogen
---

# soia-media-publish-wechat-draft

媒体内容工作流的**公众号发布环节（发）**：将已写好的成文草稿排版、机械校验并安全投递到微信公众号草稿箱；发表后负责连同配图归档。**只建草稿，绝不自动群发。**

## 客户可读说明

### 这个技能可以做什么

对成稿**默认不改正文、不重写标题**，接管配图衔接、内联 HTML 排版、三级草稿投递与发布后归档：

| 客户想要 | 技能会做 | 客户能看到 |
|---|---|---|
| 本地排版并预览 / 一键复制（零配置最稳） | 运行 `render_wechat.py` 或 `publish.py --dry-run`，通过红线校验生成 `<stem>.html` 与 `<stem>.copy.html` | 带「复制公众号富文本」按钮、标题/作者/摘要栏、`2.35:1` 首图与中央 `1:1` 分享安全框、`5:2` X 封面、`390px` 手机视口预览与 7 项检查清单的 `.copy.html` |
| 推入公众号草稿箱（新建或原地更新） | 按 `--account` 解析凭据、传本地正文图换 CDN URL、传封面取 `thumb_media_id`；新建调 `draft/add`，已有 `wechat_draft_media_id` 调 `draft/update` | 草稿 `media_id`、上传图片数、排版 HTML 路径与后台预览提醒 |
| 浏览器辅助存草稿（无 API 权限时） | 在客户已扫码登录的公众号后台填入标题、作者、摘要、封面与内联 HTML 并保存草稿 | 草稿箱保存状态（停在草稿箱，绝不点发表/群发） |
| 正式发表后归档留底 | 运行 `archive.py --move` 更新 `status: 已发布`、`published_at`、`url`，连同源 `.md` 与 `assets/<篇名>/` 迁入发布归档区并清理临时 `.html`/`.copy.html` | 归档后的正式 Markdown 与配图路径 |

### 客户如何使用

- 「不要改这篇的正文和标题，先用 `minimal` 纯墨主题排版并生成 `copy.html` 给我预览。」
- 「把这篇推到 `<alias>` 公众号草稿箱，封面用 `01-wechat-cover.png`，开启 `--save-draft-id` 方便后续原地更新。」
- 「改了封面和两处错字，原地更新刚才那条公众号草稿，不要新建第二条。」
- 「这篇公众号已发表（附链接 `https://mp.weixin.qq.com/s/...`），帮我连同配图归档到发布目录。」

### 依赖与安装

默认项目单技能：`npx skills add soia-team/soia-open-cwork-office-skills -a <agent> -s soia-media-publish-wechat-draft`（`<agent>` 换成明确宿主；仅明确选择全局时加 `-g`）。整域需明确选择：`claude plugin marketplace add soia-team/soia-open-skills && claude plugin install soia-cwork-office@soia`（Codex 用 `codex plugin add soia-cwork-office@soia`）。**WorkBuddy** 使用[专家安装说明](https://github.com/soia-team/soia-open-skills/blob/main/docs/install/workbuddy.md)，不由 npx 代装。上述命令不构成安装或发布授权。纯文本与 HTML 渲染零外部依赖；API 推草稿箱需已认证公众号与私有配置。

### 私密信息与中间数据

公众号凭据与多账号映射只放 `${XDG_CONFIG_HOME:-~/.config}/soia-skills/soia-media-publish-wechat-draft/config.yml` 或 `$SOIA_MEDIA_PUBLISH_WECHAT_DRAFT_CONFIG_FILE`（示例见 [assets/config.example.yml](assets/config.example.yml)），不进仓库/vault，日志严格脱敏且不落盘 `access_token`；`.html`/`.copy.html` 为草稿同目录可重建产物，发表归档时自动清理。

### 日志与完成回执

每次执行汇报：输入文章与风格、校验结果（红线/裸文字 warning）、HTML/`.copy.html` 路径或草稿 `media_id`（提示“确认无误后在后台手动群发，发表后通知我归档”）；不打印任何 `app_secret` 或 `access_token`。

## 微信 HTML 红线与排版模型

公众号编辑器（网页粘贴及 `draft/add` 接口）会剥离外链与块级样式。渲染前自查，并用 `scripts/validate_wechat_html.py` 机械把关（硬违规 exit 1）：

- **禁用（必剥离）**：`<div>`（改用 `<section>`/`<p>`）、`class`/`id`、`position`/`float`、`@media`/`@keyframes`、CSS 变量 `var(--x)`/`--x:`、`<style>` 整块。
- **强制要求**：样式全写内联 `style=""`；可见文字节点均套 `<span style="...">`（`<code>`/`<pre>` 原样代码除外，裸文字触发 warning）；代码区用内联 `<section>` + 等宽背景模拟；正文图片正式推送前经 `media/uploadimg` 换微信 CDN URL；Alt 为空不渲染 caption，有 Alt 须写具体描述；遵循客户提供的个人说明书口吻（无定义时用通用口吻）。
- **强调密度模型**：锚点层（`#`/`##` 标题 + 单句金句）全篇 **≤5 处**；标记层（主题色 `**加粗**` + 红色 `==高亮==`）每段 **1–3 处**且总强调占比 **<15%**；容器层（引文金句卡/代码块/图片）按内容形态触发，随笔优先 `--theme minimal`。

## 主流程（6 步）与三级投递通道

1. **核对元数据与配图**：`digest`（20–40 字，紧扣单篇，不拿 `series_intro` 顶替）与 `preface` 仅写入摘要栏，不进入正文首段；若拟开原创/赞赏，核对 `author` 与赞赏账户一致。缺配图时先调 `soia-media-generate-article-image` 生成 `2.35:1` 首图（中央 `1:1` 安全区必检，可选 `5:2` X 封面）及 1–3 张克制正文图存入 `assets/<篇名>/`。
2. **发表前勘误**：只检重字、错别字与标点缺漏列对照表，不擅改正文观点或重写标题。
3. **渲染双产物**：运行 `scripts/render_wechat.py` 产出 `<stem>.html` 与 `<stem>.copy.html`（含一键复制富文本、390px 手机预览、双比例封面安全框与 7 项检查清单）。
4. **机械校验**：`scripts/validate_wechat_html.py` 必须 exit 0；建议顺手清 warning。
5. **三级投递（默认先 `--dry-run` 确认；仅客户明确说“直接推”可跳过确认）**：
   - **通道一：`.copy.html` 一键复制富文本**（零配置最稳，适合未认证个人订阅号），粘贴至公众号后台保存草稿。
   - **通道二：浏览器已登录态辅助存草稿**（无 API 权限或需扫码时），填入标题/作者/摘要/封面/HTML 后停在草稿箱。
   - **通道三：官方 API 自动投递（`scripts/publish.py`）**：换 token → 正文图 `media/uploadimg` → 封面 `material/add_material?type=image` → 新建 `draft/add` 或传 `--draft-media-id`（或 frontmatter `wechat_draft_media_id`）原地 `draft/update`（可配 `--save-draft-id` 回写）。
6. **草稿箱 7 项自查与发表归档**：提醒客户在手机预览检查封面清晰度/1:1 裁切、标题与署名、摘要自然度、正文图片、手机间距、外链与去 AI 味后再手动群发；发表并回传链接后运行 `scripts/archive.py --move` 迁入正式发布区。

## 脚本、多账号与凭据边界

- **脚本入口**：
  - `scripts/render_wechat.py [--file <in.md>] [--output <out.html>] [--copy-html <copy.html>] [--cover <png>] [--x-cover <png>] [--strip-h1] [--theme default|minimal]`（支持 Obsidian `![[img|caption|600]]` 与双链清洗）。
  - `scripts/validate_wechat_html.py [--file <html>] [--json]`（纯标准库 `html.parser` 机械门禁）。
  - `scripts/publish.py --article <md> [--cover <png>] [--x-cover <png>] [--account <alias>] [--config <path|name>] [--theme default|minimal] [--html-out <path>] [--copy-html <path>] [--no-copy-html] [--draft-media-id <id>] [--draft-index 0] [--save-draft-id] [--dry-run] [--list-accounts] [--check-auth]`（支持多账号单/分文件配置，未设 `default_account` 且传参不明或不存在时 **fail-closed** 拒绝回退；Obsidian 短附件名多处重名时同样报错停止）。
  - `scripts/archive.py --article <md> [--url <link>] [--date YYYY-MM-DD] [--platform 公众号] [--account <alias>] [--archive-dir <dir>] [--move] [--force]`（更新 `tags`/`status: 已发布`/`published_at`/`url`，`--move` 同步迁移 `assets/<篇名>/` 并清理草稿区 `.html`/`.copy.html`）。
- **AppID / AppSecret 与 IP 白名单**：官方 `draft/add` 仅对**已认证**订阅号/服务号开放；在 `mp.weixin.qq.com`「设置与开发 → 开发 → 基本配置」取 AppID、扫码重置 AppSecret（只显示一次，别处共用会被顶掉）并将运行机公网 IP 加入**IP 白名单**（漏配报 `40164 invalid ip`）。运行前可用 `--check-auth` 测通 `access_token`。

## 验证与前向测试

```bash
python3 -m unittest tests.test_wechat_draft
```

前向测试须实测：`render_wechat` → `validate_wechat_html`（exit 0）→ `.copy.html` 打开渲染与复制可用；已配凭据时 `--check-auth` → `--dry-run` → `draft/add` 与 `--draft-media-id` 原地更新，确认草稿箱无重复条目、发表后 `archive.py --move` 连带 `assets/` 自包含迁出。
