---
name: glm-understand-image
description: 使用 GLM 视觉 MCP 进行图像理解和分析。触发条件：(1) 用户要求分析图片、理解图像、描述图片内容 (2) 需要识别图片中的物体、文字、场景 (3) 使用 GLM 的视觉理解功能
---

# glm-understand-image

使用 GLM 视觉 MCP 服务器进行图像理解和分析。

## 执行流程（首次需要安装，后续直接步骤6调用）

### 步骤 1: 检查并安装依赖

#### 1.1 检查 mcporter 是否可用

```bash
npx -y mcporter --version
```

如果命令返回成功，说明 mcporter 可用，跳到步骤 2。

mcporter 可以直接通过 npx 使用，无需安装。

### 步骤 2: 检查 API Key 配置

```bash
cat ~/.openclaw/config/glm.json 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('api_key', ''))"
```

如果返回非空的 API Key，跳到步骤 4。

### 步骤 3: 配置 API Key（如果未配置）

#### 3.2 如果没有找到 Key，向用户索要

询问用户提供智谱 API Key。

如果用户没有智谱 API Key，可以访问 https://www.bigmodel.cn/glm-coding?ic=OOKF4KGGTW 购买。


#### 3.3 保存 API Key

```bash
mkdir -p ~/.openclaw/config
cat > ~/.openclaw/config/glm.json << EOF
{
  "api_key": "API密钥"
}
EOF
```



### 步骤 4: 添加 MCP 服务器

使用 mcporter 添加 GLM 视觉 MCP 服务器：

```bash
mcporter config add glm-vision \
  --command "npx -y @z_ai/mcp-server" \
  --env Z_AI_API_KEY="your-key" \
  --env Z_AI_MODE="ZHIPU" \
  --env HOME="$PWD"
```

注意：将 `your-key` 替换为实际的智谱 API Key。`HOME` 环境变量设置为当前工作目录以避免日志文件权限问题。

### 步骤 5: 测试连接

```bash
mcporter list
```

确认 `glm-vision` 服务器已成功添加。

### 步骤 6: 使用 MCP 处理图像

#### 6.1 准备图片

将图片放到可访问路径，例如：
- `~/.openclaw/workspace/images/图片名.jpg`
- 或者使用 URL

#### 6.2 使用 mcporter 调用 MCP 工具

使用 mcporter 调用 MCP 服务：

```bash
mcporter call glm-vision.analyze_image prompt="<对图片的提问>" image_source="<图片路径或URL>"
```

**示例：**

```bash
# 描述图片内容
mcporter call glm-vision.analyze_image prompt="详细描述这张图片的内容" image_source="~/image.jpg"

# 使用 URL
mcporter call glm-vision.analyze_image prompt="这张图片展示了什么？" image_source="https://example.com/image.jpg"

# 提取图片中的文字
mcporter call glm-vision.extract_text_from_screenshot image_source="~/screenshot.png"

# 诊断错误截图
mcporter call glm-vision.diagnose_error_screenshot prompt="分析这个错误" image_source="~/error.png"
```

#### 6.3 API 参数说明

| 参数 | 说明 | 类型 |
|------|------|------|
| image_source | 图片路径或 URL | string (必填) |
| prompt | 对图片的提问 | string (必填) |


## 支持的工具

**重要提示：如果出现问题以官方说明为准**
官方版说明 ： https://docs.bigmodel.cn/cn/coding-plan/mcp/vision-mcp-server

GLM 视觉 MCP 服务器提供以下工具：
- `ui_to_artifact` - 将 UI 截图转换为代码、提示词、设计规范或自然语言描述
- `extract_text_from_screenshot` - 使用先进的 OCR 能力从截图中提取和识别文字
- `diagnose_error_screenshot` - 解析错误弹窗、堆栈和日志截图，给出定位与修复建议
- `understand_technical_diagram` - 针对架构图、流程图、UML、ER 图等技术图纸生成结构化解读
- `analyze_data_visualization` - 阅读仪表盘、统计图表，提炼趋势、异常与业务要点
- `ui_diff_check` - 对比两张 UI 截图，识别视觉差异和实现偏差
- `analyze_image` - 通用图像理解能力，适配未被专项工具覆盖的视觉内容
- `video_analysis` - 支持 MP4/MOV/M4V 等格式的视频场景解析，抓取关键帧、事件与要点

## MCP 配置

MCP 服务器名称：`glm-vision`

MCP 服务器配置：`@z_ai/mcp-server`

环境变量：
- `Z_AI_API_KEY` - 智谱 API Key（必需）
- `Z_AI_MODE` - 服务平台选择，默认为 `ZHIPU`
