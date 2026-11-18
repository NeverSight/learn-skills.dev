---
name: soia-media-publish-x
description: 成文发 X：拆成编号 thread 并按授权存草稿，或把 Markdown 传到 X Articles 草稿箱并校验。触发：「发成 X thread」「拆成推文串」「thread 这篇」「发成 X Article」「推到 X 文章草稿箱」
version: 3.0.0
created_at: 2026-07-16 15:44:20
updated_at: 2026-11-11 19:00:00
created_by: gpt-5.6-luna
updated_by: claude-fable-5-2
---

# soia-media-publish-x

把成文草稿送到 X 的两个出口：**thread**（推文串文本，可选浏览器直填）和 **X Articles**（富文本长文草稿）。由原 `soia-media-publish-x-thread` 与 `soia-media-publish-x-article` 合并而来，两边的能力、触发词和脚本都在；不调用 X API。

## 客户可读说明

### 这个技能可以做什么

| 客户想要 | 走哪个子任务 | 技能会做 | 客户能看到 |
|---|---|---|---|
| 把文章发成 X thread、拆成推文串、发条 X / 发个推 | [references/thread.md](references/thread.md) | 提取主线、拆分论证、编号并控制每条 ≤280 字符；代码与链接保持原样 | 一组可复制的 Markdown 推文条目与长度检查 |
| 把 thread 填进 X、存到 X 草稿、直接发 | [references/thread.md](references/thread.md) 的「浏览器直填模式」 | 用 `scripts/x_post.py` 填入并存草稿；满足发布档条件才发布 | 单行 JSON 回执：草稿位置或推文 URL |
| 把 Markdown 长文发成 X Article、推到 X 文章草稿箱 | [references/article.md](references/article.md) | 解析标题/封面/正文图 → 新建草稿 → 富文本粘贴 → 按原位插图 → 机械校验 | 草稿 URL、校验清单和回执 |
| 先看看这篇能不能发 X Article | [references/article.md](references/article.md) 第 1 步 | 只跑解析 dry-run，不动浏览器 | 标题、封面、图片数量与缺图清单 |

按请求只读对应的一份参考：做 thread 不必读 article，反之亦然。分不清是短帖/thread 还是 Articles 长文时先问一句。

### 客户如何使用

- thread：说“发成 X thread”“拆成推文串”或“thread 这篇”，并提供成文草稿、文件内容或路径；可一并说明目标读者、口吻、CTA 方向和需要保留的代码/链接。默认只在回复里交付文本，由客户人工复制发布。
- X Articles：说“把 <文件> 发成 X Article”“上传到 X 文章”“推到 X 草稿箱”。Agent 先 dry-run 解析并汇报，封面缺失时先问；浏览器阶段全程可见，完成后给草稿 URL，由客户人工审阅并发布。账号需订阅含「撰写文章」权益。
- `soia-media-compose-article-draft` 是常见上游产物，但不是安装级强依赖；也可以直接提供任意成文草稿。

### 授权档位与安全底线

| 场景 | 默认 | 何时可以更进一步 |
|---|---|---|
| thread 文本 | 只产出回复文本，不动浏览器 | 客户说「填进 X」「存到 X 草稿」才启用浏览器直填，默认存草稿 |
| thread 发布 | 不发布 | 客户**在本次会话中逐字给出内容或确认最终文案，并明确说「发」**，才可 `send --yes`；AI 改写产物必须先展示最终文案并得到确认，逐字使用确认过的文案 |
| X Articles | 只保存草稿 | 没有更进一步：**任何情况下不点「发布/Publish」**，`x_article_post.py` 里没有发布代码路径 |

不代输凭据、不代为订阅 Premium；登录态只留在本地浏览器 profile，不导出 cookie、不进仓库和日志。不把“已生成”“已存草稿”说成“已发布”。

### 依赖与安装

默认项目单技能：`npx skills add soia-team/soia-open-cwork-office-skills -a <agent> -s soia-media-publish-x`，执行前核实当前参数。
整域需明确选择：Claude Code 使用 `claude plugin marketplace add` / `claude plugin install soia-cwork-office@soia`，Codex 使用 `codex plugin marketplace add` / `codex plugin add soia-cwork-office@soia`；市场为 soia-team/soia-open-skills，完整步骤见[官方安装说明](https://github.com/soia-team/soia-open-skills#安装)。
WorkBuddy 使用[专家安装说明](https://github.com/soia-team/soia-open-skills/blob/main/docs/install/workbuddy.md)，不由 npx 代装。上述命令不构成安装或发布授权。

- 只拆 thread 文本：无脚本、无私有配置、无 API key、无外部服务依赖。
- 浏览器直填与 X Articles：Python 3.9+，一次性 `pip install playwright && python -m playwright install chromium`；X Articles 另需账号含「撰写文章」权益的 Premium 订阅。
- X Articles 的备选路线（宿主浏览器工具 + `clipboard_x.py`）需要 macOS；主路线跨平台。

### 登录态与旧 profile

thread 与 Articles 共用一份本地浏览器 profile，登录一次两边都能用：

```bash
python3 <skill-path>/scripts/x_post.py login     # 弹窗人工登录，登录态存本地 profile
python3 <skill-path>/scripts/x_post.py status    # 检查登录态
```

profile 目录优先级：`--profile-dir` → `SOIA_X_PROFILE_DIR` → `~/.config/soia-skills/soia-media-publish-x/x-profile`。新位置不存在时，脚本按顺序原地复用旧技能名下已有的 profile：`~/.config/soia-skills/soia-media-publish-x-thread/x-profile`，再到更早的 `~/.config/soia-skills/soia-open-skills/soia-pkm/soia-pkm-publish-x-thread/x-profile`。旧目录不搬移、不删除，已登录的不用重新登录；浏览器会照常在被复用的目录里更新登录态。本技能没有私有 `config.yml`。

### 私密信息与中间数据

- 登录态只在上述本地 profile 目录；不读取日常浏览器的 cookie、Keychain 或密码。
- X Articles 的解析 JSON、HTML 和截图写系统临时目录；客户未指定落盘位置时 thread 只产出回复文本，指定位置时另存独立草稿文件，绝不覆盖源文件。
- 回执与日志不输出 cookie、token 或账号凭据。

### 日志与完成回执

每次执行都要回报实际处理范围、数量和人工发布边界。thread 的最低回执格式见 [references/thread.md](references/thread.md)「日志与完成回执」；X Articles 报草稿 URL、第 3 步校验清单逐项结果、跳过/失败项，并提示人工审阅后自行发布（见 [references/article.md](references/article.md)）。中途失败（选择器改版、登录失效）如实报告停在哪一步。

## 资源

- thread 拆条规则、输出格式、浏览器直填模式：[references/thread.md](references/thread.md)
- X Articles 工作流、格式支持边界、异常处理、脚本规格：[references/article.md](references/article.md)
- 脚本：`scripts/x_post.py`（login / status / draft / send）、`scripts/x_article_post.py`（status / check / draft）、`scripts/parse_x_article.py`（Markdown → JSON/HTML）、`scripts/clipboard_x.py`（备选路线的 macOS 剪贴板）

## 验证

脚本层前向测试不需要登录态，改脚本后必跑：

```bash
python3 <skill-path>/scripts/x_post.py --help
python3 <skill-path>/scripts/x_article_post.py --help
python3 <skill-path>/scripts/parse_x_article.py <article.md>
```

`x_post.py`：`status` 对空 profile 返回 `logged_in:false`；`draft` 未登录时拦截并指引 login；`send` 缺 `--yes` 拒绝；单条 >280 字符拒绝——均以单行 JSON 退出。`parse_x_article.py` 与 `x_article_post.py` 的 fixture 断言、已实测与未实测范围见 [references/article.md](references/article.md)「验证与测试」。带登录态的端到端验证需要客户明确同意，不借测试发布任何内容。
