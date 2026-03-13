---
name: wechat-send
description: Use when 需要在 macOS 上自动给微信联系人发送消息，且要通过剪贴板粘贴规避中文输入法干扰，必要时可复用 localmac-ai-ocr 提供的 GUI 与 OCR 命令做截图、找字、点击与校验。
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - osascript
        - pbpaste
        - pbcopy
      skills:
        - localmac-ai-ocr
    primaryEnv: LOCALMAC_AI_OCR_DIR
---

# WeChat Send

## 概览

这个 skill 用来在 macOS 桌面版微信里发送消息，优先走稳定的 UI 自动化顺序：

1. 激活 WeChat 并确认它是前台应用
2. 用快捷键打开搜索或切换会话
3. 联系人名和消息正文都通过剪贴板粘贴，避免输入法拦截
4. 需要点击、截图或 OCR 校验时，调用 `localmac-ai-ocr` 暴露的 `scripts/gui` 和 `scripts/ocr`

不要直接依赖另一个 skill 的 Python 模块、`.venv` 路径或某台机器上的绝对目录。跨 skill 的公共契约只认两个可执行入口：

- `scripts/gui`
- `scripts/ocr`

## 何时使用

- 用户明确要求在 macOS 微信客户端给联系人发消息
- 直接键入中文容易被输入法干扰，必须改用剪贴板粘贴
- 需要结合截图、OCR、按字点击来适配不同机器上的微信窗口位置

不要在这些场景优先使用这个 skill：

- 用户只是要发网页微信消息
- 目标环境不是 macOS 桌面
- 当前任务只需要 OCR，不需要操作微信

## 前置依赖

- macOS 已安装并登录 WeChat
- 运行环境已授予 Accessibility 权限
- 如需截图校验，还要授予 Screen Recording 权限
- `localmac-ai-ocr` 已安装并可执行

如果 `localmac-ai-ocr` 不在默认位置，运行前显式设置：

```bash
export LOCALMAC_AI_OCR_DIR="/path/to/localmac-ai-ocr"
```

也支持把 `--ocr-skill-dir /path/to/localmac-ai-ocr` 作为命令参数传入。不要把真实本地目录写死进 skill 文档、脚本或提交记录。

## 标准工作流

### 1. 先做依赖体检

```bash
python3 scripts/wechat_auto.py doctor
```

这个检查会确认：

- `WeChat` 是否可启动
- `osascript`、`pbcopy`、`pbpaste` 是否可用
- `localmac-ai-ocr` 的 `scripts/gui` 和 `scripts/ocr` 是否能被发现并执行
- `localmac-ai-ocr` 依赖的 `uv`、`screencapture`、`sips` 与 OCR 后端是否至少有一套可用

任一必需项缺失时，命令会输出错误并以非 0 退出。

### 2. 直接发送消息

从 skill 根目录执行：

```bash
scripts/send_message "文件传输助手" "测试消息"
```

需要调试信息时：

```bash
python3 scripts/wechat_auto.py send "文件传输助手" "测试消息" --debug --delay 0.8
```

### 3. 需要 OCR 辅助时再调用依赖 skill

典型用途：

- 发送前截图确认微信窗口已置顶
- 搜索结果歧义时，按文字定位联系人
- 点击后再截图核验是否真的进入目标会话

配方见 `references/integration.md`。

## 整合约定

`wechat-send` 和 `localmac-ai-ocr` 的整合方式应该保持低耦合：

1. `wechat-send` 只发现并调用 `localmac-ai-ocr/scripts/gui` 与 `localmac-ai-ocr/scripts/ocr`
2. 不 import 对方 Python 文件，不依赖对方虚拟环境路径
3. 所有 OCR 配置仍由 `localmac-ai-ocr` 自己管理，例如 `AISTUDIO_OCR_API_URL` 与 `AISTUDIO_OCR_TOKEN`
4. `wechat-send` 只负责业务流程编排，例如“激活微信 -> 搜索联系人 -> 粘贴消息 -> 发送”

这能保证：

- `localmac-ai-ocr` 内部实现换成 `uv`、venv 或别的 Python 版本时，`wechat-send` 不用跟着改
- 两个 skill 可以分别测试、分别发布
- 在任意机器上只要目录可发现或显式传入，就能运行

## 快速命令

- 体检：

```bash
python3 scripts/wechat_auto.py doctor
```

- 发送消息：

```bash
scripts/send_message "张三" "你好，这是自动消息"
```

- 指定依赖 skill 目录：

```bash
python3 scripts/wechat_auto.py send "张三" "测试消息" --ocr-skill-dir /path/to/localmac-ai-ocr
```

## 常见风险

- 没有 Accessibility 权限时，快捷键和点击都会失败
- 微信未在前台时，粘贴内容会发到错误应用
- 联系人重名时，单靠回车选中可能进入错误会话，此时要追加 OCR 校验
- 不要假设另一台机器的微信窗口坐标和你的机器一致

## 参考文件

- `scripts/wechat_auto.py`
- `scripts/send_message`
- `references/integration.md`
