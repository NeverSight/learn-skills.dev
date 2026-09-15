---
name: vidgate
description: 通过 vidgate CLI 发布视频到 TikTok / TikTok Shop（挂车带货）、查询坐席与商品、跟踪发布状态、TTS 预审。Use when the user wants to upload or publish videos to TikTok / TikTok Shop, query seats or shoppable products, run TTS precheck, upload covers, search music, or check publish status via the vidgate API platform.
metadata:
  author: beervid
  version: "0.4.0"
---

# vidgate 视频发布

vidgate 是 TikTok / TikTok Shop 视频发布 API 平台。本 skill 教你用官方 CLI（`vidgate`）完成发布全流程。

## 0. 前置自举（每次会话先检查）

```bash
which vidgate || npm install -g @vidgate/cli   # 要求 Node ≥22
vidgate auth status                            # 退出码非 0 = 未配置凭据
vidgate version                                # 核对能力版本
```

- 无凭据 → 提示用户提供 API Token（控制台「API Keys」页创建）：`vidgate auth login --token <t>`，或 `export VIDGATE_API_TOKEN=vg_live_...`。
- **能力版本门**：稳定版 **≥ 1.4.0** 具备全部命令（只读 + 写链路 + `skill install`）；beta 通道自 `0.0.2-beta` 起同样全量。拿不准就以 `vidgate --help` 输出为准（含 `videos upload` 即具备写能力）；版本过旧就提示用户 `npm update -g @vidgate/cli`。

## 1. 凭据纪律（安全红线）

- Token 一律经环境变量或 `auth login` 注入；**禁止**写进任何源码、脚本、git 提交。
- Token 明文只在控制台创建时可见一次；丢失就引导用户重建，不要尝试找回。

## 2. 输出纪律

- **永远带 `--json`**：恒输出服务端 envelope `{ code, message, data }`；**以 `code === 0` 判成败**（HTTP 200 也可能是官方失败）。
- 退出码：0 成功 / 1 本地参数 / 2 认证 / 3 业务拒绝 / 4 限流配额 / 5 上游官方 / 6 内部。429 限流 CLI 已自动退避。
- 全局 flag（`--json` `--token` `--base-url` `--timeout`）可前可后。

## 3. 平台心智模型（先读，再动手）

- **坐席（Seat）**：1 个 TikTok 账号 = 1 坐席；一个坐席可绑两种能力。**TT 能力的账号 ID 是 businessId；TTS 能力是 creatorUserOpenId**——两个 ID 都从 `vidgate seats list --json` 拿，别混用。
- **视频库分两库**：TT 库上传返回 `videoUrl`（公网 URL，**7 天有效**，发布用）；TTS 库上传返回 `fileId`（**一次性消耗**，发布/预审用）。
- **账号健康**：坐席 `authStatus=expired` 说明授权失效 → 引导用户去控制台坐席页重新绑定，不要反复重试发布。

## 4. 流程路由

### TT 发布（TikTok 普通视频）

```bash
vidgate seats list --json                    # 拿 TT 账号 businessId
vidgate videos upload <file> --json          # → videoUrl（7 天有效）
vidgate publish tt --video-url <url> --account-id <id> --caption "文案 #话题" --wait --json
```

### TTS 挂车（TikTok Shop 带货视频）

```bash
vidgate seats list --json                                        # 拿 TTS 账号 creatorUserOpenId
vidgate videos upload <f> --library tts --account-id <id> --json # → fileId（一次性！）
vidgate products query --account-id <id> --json                  # 拿可挂车 productId
vidgate precheck submit --file-id <f> --account-id <id> --product-id <p> --product-title <锚点> --wait --json  # 可选但建议
vidgate publish tts --file-id <f> --account-id <id> --product-id <p> --product-title <锚点> --wait --json
```

**深入细节按需读 references/**：
- `references/cli-commands.md` — 全部命令与 flag 完整参考
- `references/tt-publish.md` — TT 视频规格/官方限频/字段语义/数据回收
- `references/tts-publish.md` — fileId 规则/商品分页/预审双 check 读法/封面与音乐
- `references/errors.md` — 错误码 × 退出码 × 处置动作全表
- `references/concepts.md` — 平台概念与限制全集（有效期/配额/限流）

## 5. TTS 四条硬规则（官方规则，违反必失败）

1. **fileId 一次性消耗**：发布调用即消耗，**失败也不可复用**；重发必须重新上传。
2. **fileId 绑定上传账号**：upload 与 publish 的 `--account-id` 必须一致。
3. **锚点文案（productTitle）**：≤30 字符，不含标点和 emoji（官方校验，违规透传 3001）。
4. **预审可选但建议**：配额 50 次/天/账号；violation FAIL 不建议发布（是否发布由用户决定并承担后果）。

## 6. 通用排错姿势

1. 先看退出码定位错误类别，再读 envelope 的 `message`（3001 时含官方原因）。
2. `code=1005` 先怀疑账号/资源归属：用 `seats list` 核对 ID 口径（businessId vs creatorUserOpenId）。
3. 发布失败（`publish_failed`）读 `failReason` / `beervid.reason` 向用户解释官方原因，不要自行猜测。
4. 完整处置表见 `references/errors.md`。

## 7. 无 CLI 降级

用户拒绝安装 CLI 时：优先按本 skill 包内 `references/endpoints.md` 直连 HTTP（端点/参数/错误码速查，与 openapi spec 同源，skill 单独安装也自洽）；envelope 与错误码语义同上（`code === 0` 判成败）。控制台文档站「API 参考」页（/docs，需登录）可作补充参考。
