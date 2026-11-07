---
name: 1688-item-image-optimizer
version: 1.0.0
description: >-
  商品图片制作统一入口：主图优化、轮播图、详情图、背景替换、数字模特。
  核心能力：verify_permission（高级版权限校验）、build_tool_url（构建工具页 URL）、configure（AK 配置）。
  触发词：做一套图、做图、出图、优化主图、主图优化、轮播图、详情图、背景替换、数字模特、商品图片、改图、图片优化。
  不应触发：新品发布/批量上架（走发品 skill）、品牌VI/海报/店铺装修、图片规范问答。
  本 Skill 的图片制作流程已由 workflow 编排覆盖，命中触发词时直接执行 workflow。如果 workflow 无法完成任务（如纯能力问答、单命令调用、探索性使用），加载本 SKILL.md 进行推理。
metadata:
  engine: false
  openclaw:
    emoji: "🖼"
interactions:
  - name: open_tab_image_optimize
    type: open_tab
    selectionType: shop_backend
    description: "路由到商品图片工具页面（主图优化/轮播图/详情图/背景替换/数字模特），URL 由 build_tool_url capability 构建"
    required_data:
      url: "完整工具页面 URL（由 build_tool_url 返回的 data.open_tab.url）"
      title: "页面标题（主图优化/轮播图制作/详情图制作/背景替换/数字模特）"
  - name: select_image_type
    type: card
    selectionType: image_type
    description: "用户意图模糊时，引导选择要制作的图片类型"
    required_data:
      questions: "图片类型选项数组"
  - name: select_images
    type: card
    selectionType: image
    description: "上传图片超出工具限制时，引导用户选择要处理的图片子集"
    required_data:
      questions: "图片选项数组（多选）"
---

# 1688-item-image-optimizer — 商品图片制作统一入口

> 编排流程（意图识别 → 权限校验 → 构建入口 → open_tab）由 `workflow/1688-item-image-optimizer.js` 确定性执行。本文件只描述**能力**：有哪些 CLI 命令、各自怎么调、返回什么、业务约束是什么。供纯问答 / 单命令调用 / 引擎委托时参考。

统一入口：`python3 {baseDir}/cli.py <command> [options]`
所有命令输出 JSON：`{"success": bool, "markdown": str, "data": {...}}`

## 命令速查

| 命令 | 必填参数 | 说明 |
|------|---------|------|
| `verify_permission` | 无 | 校验数字模特权限（返回 isAi/digitalModel/faceFix） |
| `build_tool_url` | `--type` | 构建图片工具页面 URL，返回 open_tab 透传对象 |
| `configure` | （AK 位置参数，可选） | 配置/查看 AK；无参看状态 |

## 能力详述

### verify_permission

- **签名**：`cli.py verify_permission`（无参，商家身份由 AK 网关签名自动识别）
- **返回结构**：业务数据嵌套在 `data.data` 内 —— `{"success": true, "data": {"data": {"isAi": bool, "digitalModel": bool, "faceFix": bool}}}`
- **关键字段**：
  - `isAi`：是否高级版（保留字段，当前 skill 不做权限判断）
  - `digitalModel`：是否有数字模特权限（决定 digitalModel 能否使用）
  - `faceFix`：脸部修复权限（暂未使用）
- **业务含义**：仅数字模特（digitalModel）路由前必须校验；一次会话内结果可复用。

### build_tool_url

- **签名**：`cli.py build_tool_url --type <type> [--offer-id ID] [--img-url URL] [--img-url-list URL1,URL2]`
- **返回结构**：`{"success": bool, "markdown": str, "data": {"open_tab": {"type": "open_tab", "url": "...", "title": "..."}}}`
- **`--type` 取值**（CLI 支持 7 个；前 5 个为当前业务动线类型，后 2 个 CLI 支持但编排动线未独立暴露）：

  | type | 中文标题 | 图片参数 | 业务动线 |
  |------|---------|---------|---------|
  | `main` | 主图优化 | `--img-url`（单图） | ✅ |
  | `carousel` | 轮播图制作 | `--img-url-list`（多图） | ✅ |
  | `detail` | 详情图制作 | `--img-url-list`（多图） | ✅ |
  | `replaceSubject` | 背景替换 | `--img-url`（单图） | ✅ |
  | `digitalModel` | 数字模特 | `--img-url`（单图） | ✅ |
  | `matting` | 白底图 | `--img-url`（单图） | CLI 支持 |
  | `outpainting` | 一键扩图 | `--img-url`（单图） | CLI 支持 |

- **图片参数与工具类型必须匹配**：单图工具传 `--img-url`、多图工具传 `--img-url-list`，错配 CLI 直接报错（让上游自纠）。空字符串视为无效图片报错；不传则跳过（工具页自带上传入口）。
- **业务含义**：URL 由 CLI 构建（已 URL encode），**禁止 LLM 编造/拼接**。`success=false` 时禁止触发 open_tab。

### configure

- **签名**：`cli.py configure [YOUR_AK]` — 无参看状态，带 AK 写入配置
- **返回**：`data.configured`（bool）
- AK 由 OpenClaw 配置注入，写入后需新开会话或 `openclaw secrets reload` 生效。

## 权限要求

| type | 权限要求 | 校验依据 |
|------|---------|---------|
| main / replaceSubject / carousel / detail / matting / outpainting | 基础功能 | 免校验 |
| digitalModel | 需数字模特权限 | `digitalModel == true` |

## 图片参数规则

- **附件 path 即公网 URL**：用户消息携带的图片以附件对象 `{name, mime, path}` 传入，`path` 即图片公网 URL（img.alicdn.com CDN）。**有图必带**——单图工具用 `--img-url`，多图工具用 `--img-url-list`（多张逗号分隔）。
- **无图不阻断**：未识别到图片直接构建 URL，工具页自带上传入口。
- **图片超限阈值**（超出需让用户选子集）：

  | 工具 | 上限 |
  |------|------|
  | 主图优化 / 背景替换 / 数字模特 | 1 张 |
  | 轮播图 | 9 张 |
  | 详情图 | 20 张 |

## 触发词 → type 映射

| 触发词 | → type |
|--------|--------|
| 主图优化、优化主图、生成更好的商品主图、主图哪里有问题 | main |
| 轮播图、做轮播图 | carousel |
| 详情图、做详情图 | detail |
| 背景替换、换背景 | replaceSubject |
| 数字模特、模特图、生成模特、换模特、AI模特 | digitalModel |
| 做图、做一套图、商品图片、商品图制作、提升转化的图、优化图片、改图（**意图模糊**） | 走 select_image_type 卡片，按权限平铺 |

## 安全声明

| 风险级别 | 命令 | Agent 行为 |
|---------|------|-----------|
| 只读 | `verify_permission` | 直接执行 |
| 只读 | `build_tool_url` | 直接执行（仅构建 URL，不写数据） |
| 写入 | `configure` | 写 AK 配置，需用户提供凭证 |

- open_tab 的 URL 必须来自 `build_tool_url` 返回，**禁止编造/拼接**；触发 open_tab 即为终态，不追加引导话术。
- 端侧工具页承担文件类型/大小/安全校验与上传后处理。

## 异常处理

> **铁律（最高优先级，覆盖下表所有行）**
> 1. **权限结论只能来自 `verify_permission` 的 `digitalModel` 字段，严禁凭感觉编。** carousel / detail / main / replaceSubject / matting / outpainting 为基础功能，直接放行；只有 `digitalModel==false` 时才可按下表给出对应话术。严禁输出"权限校验未通过 / 未开通高级版 / 账号无权限"等任何未经 verify_permission 证实的措辞。
> 2. **main / replaceSubject / carousel / detail / matting / outpainting 是基础功能，从不校验权限。** 任何情况下都不得对它们提"高级版 / 权限 / 权益"。
> 3. **拿不到真实错误就别编原因。** 只说"暂时无法完成，请稍后重试"，禁止虚构"权限 / 权益 / 账号状态 / 服务过期"等具体理由。
> 4. **不许救场。** workflow 已渲染的卡片 / 页面不要手动重开、重贴 URL 或 JSON；workflow 已是终态。

| 错误关键词 | Agent 动作 |
|-----------|-----------|
| `verify_permission` 返回 `success=false`（AK 未配置/网络失败/限流） | **fail-closed**：一律按"无权限"拦截，禁止 open_tab；AK 未配置则提示 `cli.py configure YOUR_AK` |
| 数字模特无权限（`digitalModel==false`） | 输出「数字模特功能暂未对你的账号开放～」，禁止 open_tab |
| `build_tool_url` 返回 `success=false` | 禁止 open_tab，输出 markdown 中的错误提示 |

## 参考文档

- `references/interaction-specs.md` — 三个交互组件（open_tab / select_image_type / select_images）的字段结构与映射规则
