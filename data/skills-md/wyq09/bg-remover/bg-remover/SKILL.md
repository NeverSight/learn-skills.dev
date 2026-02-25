---
name: bg-remover
description: 智能图片背景移除工具。当用户请求「去除图片背景」「抠图」「移除背景」「生成透明背景图片」或类似需求时使用。支持上传图片后自动识别主体并去除背景，生成带透明通道的PNG图片。
author: wuyiqun
license: MIT
---

# 图片背景移除 Skill

## 环境要求与自动修复

### 环境要求

- Python 3.8 或更高版本
- pip（Python 包管理器）
- rembg 库

### 一键自动修复环境

**重要：首次使用前，请先运行环境修复脚本！**

**macOS / Linux:**
```bash
cd ~/.claude/skills/bg-remover
./install.sh
```

**Windows (PowerShell):**
```powershell
cd ~/.claude/skills/bg-remover
.\install.ps1
```

脚本会自动：
1. 检查 Python 版本（需 3.8+）
2. 检查并安装 pip
3. 检查并安装 rembg 库
4. 测试 rembg 功能是否正常

### 自动环境检查

当用户使用此 skill 时，如果检测到环境不符合要求，系统会自动运行修复脚本。

**环境检查清单：**
- [ ] Python 3.8+ 已安装
- [ ] pip 可用
- [ ] rembg 库已安装并可正常导入

## 使用场景

当用户请求以下任何操作时，使用此 skill：
- 去除图片背景
- 抠图
- 移除图片背景
- 生成透明背景图片
- 图片背景变透明
- 抠出图片中的人物/物体
- 制作证件照（去除背景）
- 产品图去背景

## 工作流程

### 1. 接收用户输入

用户可能提供：
- 本地图片文件路径
- 图片 URL
- 直接上传的图片文件

### 2. 处理图片背景移除

根据可用资源，选择以下方法之一：

#### 方法 A：使用 remove.bg API（推荐）

如果用户有 remove.bg API 密钥：
```python
from removebg import RemoveBg
import os

# 初始化
removebg = RemoveBg("YOUR_API_KEY", "error.log")

# 处理图片
removebg.remove_background_from_img_file("input.jpg")
# 输出：input_no_bg.png
```

#### 方法 B：使用 rembg 库（本地处理）

使用开源的 rembg 库进行本地处理：
```python
from rembg import remove
from PIL import Image

# 读取图片
input_path = "input.jpg"
output_path = "output.png"

# 处理
with open(input_path, "rb") as input_file:
    input_data = input_file.read()
    output_data = remove(input_data)

# 保存结果
with open(output_path, "wb") as output_file:
    output_file.write(output_data)
```

#### 方法 C：使用在线服务

可以使用以下在线服务：
- remove.bg
- PhotoRoom API
- Clipdrop (Remove Background)
- Adobe Firefly

### 3. 输出结果

向用户提供：
- 处理后的透明背景 PNG 图片
- 对比预览（原图 vs 处理后）
- 图片保存路径或下载链接

## 安装依赖

```bash
# 使用 rembg（推荐，免费本地处理）
pip install rembg[gpu]  # GPU 加速版本
# 或
pip install rembg       # CPU 版本

# 使用 remove.bg API
pip install removebg

# 使用 rembg 命令行工具
pip install rembg-cli
```

## 使用示例

### 示例 1：基本抠图

**用户输入**：
```
帮我去除这张图片的背景：photo.jpg
```

**处理步骤**：
1. 读取图片文件
2. 使用 rembg 去除背景
3. 保存为 PNG 格式
4. 显示处理结果

### 示例 2：批量处理

**用户输入**：
```
把这个文件夹里的所有图片都去除背景
```

**处理步骤**：
1. 扫描文件夹中的所有图片
2. 逐个处理
3. 保存到输出文件夹

### 示例 3：URL 图片处理

**用户输入**：
```
去除这张图片的背景：https://example.com/image.jpg
```

**处理步骤**：
1. 下载图片
2. 处理背景
3. 返回结果

## 命令行使用（rembg）

```bash
# 基本用法
rembg i input.jpg output.png

# 处理整个文件夹
rembg p input_folder/ output_folder/

# 使用不同的 AI 模型
rembg i input.jpg output.png -m u2netp  # 轻量级模型
rembg i input.jpg output.png -m u2net   # 标准模型（默认）
rembg i input.jpg output.png -m silueta  # 人像专用

# 添加 alpha matting（边缘优化）
rembg i input.jpg output.png -a
```

## 可用模型

rembg 支持以下模型：
- `u2net`：通用模型（默认），适合大多数场景
- `u2netp`：轻量级模型，速度快
- `u2net_human_seg`：人像分割专用
- `silueta`：人像专用模型
- `isnet-general-use`：新的通用模型

## 注意事项

1. **输入格式**：支持 JPG、PNG、WebP 等常见格式
2. **输出格式**：始终输出 PNG 格式（支持透明通道）
3. **图片质量**：输入图片分辨率越高，抠图效果越好
4. **复杂背景**：复杂背景可能需要手动后期调整
5. **边缘处理**：对于精细物体（如头发），可以使用 alpha matting 优化

## 高级选项

### Alpha Matting（边缘优化）

对于边缘复杂的图片，启用 alpha matting 可以获得更好的边缘效果：

```python
from rembg import remove, new_session

session = new_session("u2net", alpha_matting=True,
                     alpha_matting_foreground_threshold=240,
                     alpha_matting_background_threshold=10,
                     alpha_matting_erode_size=10)
```

### 返回遮罩

如果只需要获取遮罩而非去除背景的图片：

```python
from rembg import remove
import io

input_data = open("input.jpg", "rb").read()
# only_mask=True 只返回遮罩
output_data = remove(input_data, only_mask=True)
```

## 错误处理

常见问题及解决方案：

1. **内存不足**：使用轻量级模型 `u2netp` 或缩小图片尺寸
2. **处理速度慢**：使用 GPU 版本或轻量级模型
3. **边缘效果不佳**：启用 alpha matting
4. **识别不准确**：尝试不同的模型

## 最佳实践

1. 选择合适的模型（人像用人像模型，通用用 u2net）
2. 根据需求在速度和质量间选择（u2netp 快但精度略低，u2net 慢但精度高）
3. 对重要图片使用 alpha matting 优化边缘
4. 批量处理时考虑使用轻量级模型提高效率
