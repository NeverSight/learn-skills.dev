---
name: order-analysis
description: 分析产品升级工单，识别共性问题并提出产品改进建议。通过 agent-browser工具 访问工单系统，提取工单数据，进行问题分类、趋势分析和根因定位，输出改进方案。
---

## 核心工作流程

### 步骤 1: 前置检查
执行以下两个检查脚本，确保环境准备就绪：
```bash
# 检查 Chrome Debug 模式
sh scripts/check-cdp.sh

# 检查 agent-browser 工具
sh scripts/check-agent-browser.sh
```

### 步骤 2: 打开工单系统页面
```bash
agent-browser --cdp 9222 open "https://inner.example.com"
```
### 步骤 3: 准备输出目录
创建以时间命名的输出目录（格式：YYYYMMDD-HHMMSS）：
```bash
OUTPUT_DIR=".output/order-analysis/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$OUTPUT_DIR"
```

### 步骤 4: 获取订单数据
在浏览器中打开页面后，**在同一 shell 会话中**执行以下命令获取订单的所有JSON数据：
```bash
agent-browser --cdp 9222 eval "$(cat scripts/order-analysis.js)" > "$OUTPUT_DIR/order.json"
```

### 步骤 5: 分析数据
针对获取的订单数据，识别共性问题并提出产品改进建议，并将分析结果保存到 `$OUTPUT_DIR/order_report.md`


## agent-browser 使用方法

使用 `agent-browser` 进行网页自动化操作。运行 `agent-browser --help` 查看所有命令。
**注意**: 所有 `agent-browser` 命令应加上 --cdp 9222 参数，例如 `agent-browser --cdp 9222 open https://www.baidu.com/`

用法:
1. `agent-browser --cdp 9222 open <url>` - 访问指定页面
2. `agent-browser --cdp 9222 snapshot -i` - 获取可交互元素及其引用 (@e1, @e2)
3. `agent-browser --cdp 9222 click @e1` / `fill @e2 "text"` - 通过引用与页面元素交互
4. 页面变化后重新执行 snapshot

