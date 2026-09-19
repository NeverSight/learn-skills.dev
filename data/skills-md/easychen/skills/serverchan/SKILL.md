---
name: serverchan
description: 通过 Server 酱（方糖）向微信/App 推送消息通知。当你需要把执行结果、告警、任务完成情况等推送到自己的手机（Server酱Turbo SCT 或 Server酱³ SC3 均支持，自动按 SendKey 前缀识别）时使用本技能。支持标题、Markdown 正文，以及 tags/short/channel 等可选参数。
tags: [notification, push, serverchan, wechat]
allowed-tools:
  - Bash
env_vars:
  - key: SERVERCHAN_SENDKEY
    required: true
    desc: Server 酱 SendKey。SCT(Turbo) 形如 SCTxxxxxx；SC3 形如 sctp<数字>t<token>。在当前项目环境变量中配置，脚本按前缀自动选择推送端点。
---

# Server 酱 · 微信消息推送

通过 Server 酱把消息推送到微信/App。逻辑对齐 [easychen/serverchan-sdk](https://github.com/easychen/serverchan-sdk)，
**同时兼容 Server酱Turbo(SCT) 与 Server酱³(SC3)**，按 SendKey 前缀自动选择端点，无需额外配置：

- SendKey 以 `sctp` 开头 → SC3：`https://<num>.push.ft07.com/send/<sendkey>.send`（`num` 取自 `sctp<num>t`）
- 其余（`SCT…`）→ Turbo：`https://sctapi.ftqq.com/<sendkey>.send`

> 本技能自包含，所有命令内联在本文件中，不依赖任何外部脚本文件——直接复制运行即可。

## 安全红线（务必遵守）

- **绝不 echo / print / log `SERVERCHAN_SENDKEY`**——它会进入 stdout 被平台采集并展示。SendKey 等同推送凭证，泄露即可被他人冒发。
- curl 不要加 `-v`/`--verbose`（端点 URL 内含 SendKey，会被打到日志）。下面的命令已用 `-sS` 并且不回显 URL。
- 用 `--data-urlencode` 传 `title`/`desp`，转义交给 curl，无需手工拼接 JSON。

## 第一步：自检环境变量（务必先做）

```bash
if [ -z "${SERVERCHAN_SENDKEY:-}" ]; then
  echo "[serverchan] ✗ 缺少环境变量 SERVERCHAN_SENDKEY，已停止。"
  echo "  请在 Server 酱后台获取 SendKey 并加入当前项目环境变量 SERVERCHAN_SENDKEY："
  echo "  · Server酱Turbo(SCT)：https://sct.ftqq.com  → SendKey 形如 SCTxxxxxx"
  echo "  · Server酱³(SC3)    ：https://sc3.ft07.com   → SendKey 形如 sctp<数字>t<token>"
else
  case "$SERVERCHAN_SENDKEY" in
    sctp*) echo "[serverchan] ✓ SendKey 已配置（SC3 / sctp…，长度 ${#SERVERCHAN_SENDKEY}）" ;;
    SCT*)  echo "[serverchan] ✓ SendKey 已配置（SCT / SCT…，长度 ${#SERVERCHAN_SENDKEY}）" ;;
    *)     echo "[serverchan] ⚠ SendKey 已配置，但前缀既非 sctp(SC3) 也非 SCT(Turbo)，请确认是否正确" ;;
  esac
fi
```

若提示缺失，**不要硬编码任何 SendKey**，向用户索取后写入当前项目环境变量 `SERVERCHAN_SENDKEY` 再继续。

## 第二步：发送消息（内联命令，直接运行）

把 `title`、`desp` 换成你要推送的内容即可。端点会按 SendKey 前缀自动选择：

```bash
KEY="$SERVERCHAN_SENDKEY"
case "$KEY" in
  sctp*)
    NUM="$(printf '%s' "$KEY" | sed -n 's/^sctp\([0-9][0-9]*\)t.*/\1/p')"
    URL="https://${NUM}.push.ft07.com/send/${KEY}.send" ;;
  *)
    URL="https://sctapi.ftqq.com/${KEY}.send" ;;
esac

curl -sS -X POST "$URL" \
  --data-urlencode "title=部署完成" \
  --data-urlencode "desp=服务已上线 ✅

版本 v1.2.3"
```

- `desp` 支持 Markdown，多行直接写换行即可（上例正文含标题+空行+版本号）。
- 服务端返回 `{"code":0,...}` 表示成功；`code` 非 0 或 HTTP 非 2xx 表示失败，按返回内容排查。

### 可选参数（tags / short / channel 等）

Server 酱支持额外字段，追加 `--data-urlencode` 即可透传：

```bash
curl -sS -X POST "$URL" \
  --data-urlencode "title=服务器告警" \
  --data-urlencode "desp=CPU **95%**，请及时处理" \
  --data-urlencode "tags=运维|告警" \
  --data-urlencode "short=CPU 95%"
```

常用字段：`tags`（`|` 分隔多标签）、`short`（卡片摘要）、`channel`（指定通道）、`noip`（隐藏调用 IP）。

## 范式：把执行结果推送给自己

```bash
KEY="$SERVERCHAN_SENDKEY"
case "$KEY" in
  sctp*) NUM="$(printf '%s' "$KEY" | sed -n 's/^sctp\([0-9][0-9]*\)t.*/\1/p')"; URL="https://${NUM}.push.ft07.com/send/${KEY}.send" ;;
  *)     URL="https://sctapi.ftqq.com/${KEY}.send" ;;
esac

if some_task; then
  curl -sS -X POST "$URL" --data-urlencode "title=任务成功" --data-urlencode "desp=✅ 已完成于 $(date '+%F %T')" >/dev/null
else
  curl -sS -X POST "$URL" --data-urlencode "title=任务失败" --data-urlencode "desp=❌ 请查看日志排查" --data-urlencode "short=任务失败" >/dev/null
fi
```

> 批量/高频场景：请把多条结果**合并成一条**摘要推送，尊重免费额度（每天有限），避免刷屏。
