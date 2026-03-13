---
name: hypothesis-debugging
description: >
  This skill should be used when the user asks to "debug a bug", 
  "find root cause", "help me debug", "调试问题", "定位 bug", 
  "找出根因", "排查错误", "debug this", "why is this not working",
  or discusses systematic debugging with runtime logging. 
  Provides hypothesis-driven debugging with log instrumentation, 
  reproduction, and human-in-the-loop verification.
  NEVER fix bugs without runtime evidence first.
version: 1.0.0
---

# Debug Mode

你现在进入 **DEBUG MODE**。必须使用**运行时证据**进行调试。

## 为什么需要这种方式

传统 AI 代理会直接猜测修复，声称"100% 确信"，但由于缺乏运行时信息而频繁失败。
它们仅基于代码进行猜测。你**不能**也**不应该**这样修复 bug——你需要真实的运行时数据。

## 系统性工作流

1. **启动日志服务器** - 使用 `execute_command` 后台启动日志收集服务（见下方配置）
2. **生成 3-5 个精确假设** - 关于 bug 发生的原因（越详细越好，宁多勿少）
3. **插入日志埋点** - 用编辑工具在代码中添加日志，并行测试所有假设
4. **请求用户复现** - 输出复现步骤，等待用户回复 `done`
5. **分析日志** - 评估每个假设（CONFIRMED/REJECTED/INCONCLUSIVE），引用日志证据
6. **仅在 100% 确信时修复** - 有日志证明时才修复；**不要**移除埋点
7. **验证修复** - 请求用户再次运行，对比修复前后日志
8. **成功后清理** - 用户确认修复成功后移除所有埋点代码，停止日志服务器，给出简洁的问题总结

## 关键约束

- **禁止**：无运行时证据就修复
- **禁止**：在验证成功前移除埋点
- **禁止**：使用 setTimeout/sleep/delay 作为"修复"手段
- **禁止**：记录敏感信息（密码、token、API key、PII）
- **必须**：每次复现或验证前清空日志文件
- **必须**：修复后对比 Before/After 日志，引用具体日志行
- **必须**：假设被否定后，回滚相关代码修改（只保留被证实的修复）

## 日志服务配置

### 日志文件路径

日志文件固定存储在：

```
~/.codeflicker/debug.log
```

即 `$HOME/.codeflicker/debug.log`。

### 启动日志服务器（Agent 自动执行）

**进入 Debug 模式时，Agent 必须自动启动日志服务器**：

```bash
python {SKILL_DIR}/scripts/log-server.py
```

使用 `execute_command` 工具，设置 `is_background: true`。

服务器会自动找可用端口（从 7491 开始，如果被占用会自动尝试下一个）。启动后会输出 JSON 格式的配置信息：

```json
{"status":"started","port":7491,"endpoint":"http://127.0.0.1:7491","log_file":"~/.codeflicker/debug.log"}
```

Agent 需要解析这个输出获取实际端口，用于后续日志埋点代码中的 URL。

**配置信息**：
- 服务端点：`http://127.0.0.1:{port}`（从启动输出中获取）
- 日志文件：`~/.codeflicker/debug.log`

> 注意：即使使用 fs 直接写文件的场景用不上 HTTP 服务器，启动了也无影响，保持流程统一。

### 清空日志文件

**每次开始新的调试流程前，必须先清空日志文件**：

```bash
rm -f ~/.codeflicker/debug.log
```

⚠️ 清空日志文件 ≠ 移除埋点代码，不要混淆。

### 读取日志文件（带健康检查与自愈）

用户回复 `done` 后，**不要**直接假设日志文件一定存在。

#### 触发自检的时机（任一满足即可）

- `read_file` 读取 `~/.codeflicker/debug.log` 失败（文件不存在/权限问题）
- 发现日志文件不存在，且你不确定日志服务器是否还在运行
- 你不确定当前日志服务器端口（例如丢失了启动输出的 JSON）

#### 自检与自愈流程

1. **优先探测已知端口**：如果你记录过启动输出里的 `{port}`，先调用：

   ```
   http://127.0.0.1:{port}/health
   ```
2. **如果端口未知**：从 7491 到 7500 依次调用 `/health`（最多 10 次）
3. **若任一 health 成功**：
   - 说明服务在运行；根据返回值里的 `exists` 判断日志文件是否存在
   - 若 `exists=false`：不要判定服务终止，而是提示“埋点可能未触发/复现步骤未走到”，并让用户再复现一次后回复 `done`
4. **若所有 health 都失败**：视为服务可能未启动/已退出 → **使用 `execute_command` 后台重新启动日志服务器**：

   ```bash
   python {SKILL_DIR}/scripts/log-server.py
   ```

   然后解析启动输出 JSON 获取新的 `{port}`，再次调用 `/health` 确认启动成功。

5. **确认服务可用后**：再用 `read_file` 读取 `~/.codeflicker/debug.log` 分析。

> 注意：日志文件不存在 ≠ 服务已终止。更常见原因是“埋点没触发”或“复现步骤未覆盖到埋点路径”。

## 日志代码模板

### JavaScript/TypeScript（浏览器/Node.js）

**浏览器环境（通过 HTTP POST 发送到日志服务器）**：

```typescript
// #region debug-mode-log
fetch('http://127.0.0.1:7491', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    hypothesisId: 'H1',
    runId: 'run-1',
    location: 'file.ts:LINE',
    message: 'description',
    data: { key: value },
    timestamp: Date.now()
  })
}).catch(() => {});
// #endregion debug-mode-log
```

**Node.js 环境（直接写文件）**：

```typescript
// #region debug-mode-log
const os = require('os');
require('fs').appendFileSync(os.homedir() + '/.codeflicker/debug.log', JSON.stringify({hypothesisId:'H1',runId:'run-1',location:'file.ts:LINE',message:'desc',data:{},timestamp:Date.now()})+'\n');
// #endregion debug-mode-log
```

### Python

**直接写文件**：

```python
# region debug-mode-log
import json, time, os
with open(os.path.expanduser('~/.codeflicker/debug.log'), 'a') as f:
    f.write(json.dumps({"hypothesisId":"H1","runId":"run-1","location":"file.py:LINE","message":"desc","data":{},"timestamp":int(time.time()*1000)}) + '\n')
# endregion debug-mode-log
```

### Go

```go
// region debug-mode-log
// 需要引入："path/filepath"
home, _ := os.UserHomeDir()
logPath := filepath.Join(home, ".codeflicker", "debug.log")
if f, err := os.OpenFile(logPath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644); err == nil {
    json.NewEncoder(f).Encode(map[string]interface{}{"hypothesisId":"H1","runId":"run-1","location":"file.go:LINE","message":"desc","data":nil,"timestamp":time.Now().UnixMilli()})
    f.Close()
}
// endregion debug-mode-log
```

更多语言模板参见 `references/log-templates.md`。

## 日志格式规范

每行一个 JSON 对象（NDJSON 格式）：

```json
{"hypothesisId":"H1","runId":"run-1","location":"userStore.ts:42","message":"updateUser START","data":{"userId":5},"timestamp":1733456789000}
```

**字段说明**：

| 字段 | 必需 | 说明 |
|-----|-----|-----|
| hypothesisId | 是 | 关联的假设 ID（H1, H2...） |
| runId | 是 | 运行 ID（run-1, run-2, post-fix） |
| location | 是 | 代码位置（文件:行号） |
| message | 是 | 日志描述 |
| data | 否 | 附加数据对象 |
| timestamp | 是 | 毫秒时间戳 |

## 埋点位置指南

根据假设选择以下位置进行埋点：

- **函数入口** - 带参数值
- **函数出口** - 带返回值
- **关键操作前** - 操作前的状态/值
- **关键操作后** - 操作后的状态/值
- **分支路径** - 记录执行了哪个 if/else 分支
- **边界条件** - 可疑的边界值
- **状态变化** - 状态变更前后的值

**数量指南**：
- 最少 1 个，最多 10 个
- 典型范围 2-6 个
- 每个日志必须关联至少一个假设
- 如果需要超过 10 个，先缩小假设范围

## 对话协议

由于没有 UI 按钮，使用以下回复推进流程：

| 用户回复 | 含义 | Agent 下一步 |
|---------|-----|-------------|
| `done` | 已完成复现/验证 | 读取日志分析 |
| `fixed` | 确认 bug 已修复 | 清理埋点，停止服务，输出总结 |
| `failed` | 修复未生效 | 回滚修复，生成新假设 |
| `quit` / `exit` / `退出` | 退出调试 | 询问是否清理，停止服务 |

### 输出格式

**请求复现时**：

```markdown
## 🔄 复现步骤

1. 启动应用：`npm run dev`
2. 执行 xxx 操作
3. 观察 xxx 现象

完成后请回复 `done`
```

**请求验证时**：

```markdown
## ✅ 验证步骤

1. 清空日志文件：`rm -f ~/.codeflicker/debug.log`
2. 重新启动应用
3. 执行相同操作
4. 确认问题是否解决

- 如果问题已解决，回复 `fixed`
- 如果问题仍存在，回复 `failed`
- 如果需要继续收集日志，回复 `done`
```

## 假设评估格式

分析日志后，按此格式评估每个假设：

```markdown
### 假设评估

| 假设 | 状态 | 证据 |
|-----|------|-----|
| H1: 状态同步问题 | ❌ REJECTED | 日志 L3 显示状态一致 |
| H2: 网络超时 | ✅ CONFIRMED | 日志 L7 显示请求耗时 5200ms |
| H3: 边界条件 | ⚠️ INCONCLUSIVE | 未触发该路径 |

**根因分析**：基于日志 L7 的证据，确认问题是网络请求超时导致...
```

## 迭代处理

**如果所有假设都被否定**：
1. 先回滚之前尝试的代码修改（保留埋点）
2. 基于已收集的日志信息，生成新的假设
3. 添加更多埋点验证新假设
4. 重复流程

**如果修复后验证失败**：
1. 回滚失败的修复代码
2. 保留埋点
3. 分析新的日志，理解为什么修复没生效
4. 生成新假设或调整修复方案

## 成功后清理

当用户回复 `fixed` 确认成功后：

1. **移除所有埋点代码** - 删除 `// #region debug-mode-log` 到 `// #endregion debug-mode-log` 之间的代码
2. **删除日志文件** - 删除 `~/.codeflicker/debug.log`
3. **停止日志服务器**（Agent 自动执行）

```bash
kill $(lsof -t -i:{port}) 2>/dev/null || true
```

其中 `{port}` 是启动时获取的实际端口。

5. **输出简洁的问题总结**

```markdown
## 🎉 调试完成

**问题**：网络请求超时未正确处理，导致 Promise 永远挂起

**修复**：在 `fetchUser()` 中添加 10 秒超时配置

---

🛑 **清理完成**：
- ✅ 已移除所有调试埋点
- ✅ 已删除日志文件
- ✅ 已停止日志服务器
```

## 退出 Debug 模式

用户可以随时退出 Debug 模式，通过回复以下任意内容：

| 用户回复 | 含义 |
|---------|-----|
| `quit` / `exit` / `退出` | 放弃调试，退出 Debug 模式 |
| `stop` / `停止` | 同上 |

**退出时的清理工作**：

1. **询问用户是否保留埋点代码**
   - 如果用户想保留（可能稍后继续调试），则不删除
   - 如果用户不需要，则移除所有埋点代码

2. **停止日志服务器**（Agent 自动执行）

```bash
kill $(lsof -t -i:{port}) 2>/dev/null || true
```

其中 `{port}` 是启动时获取的实际端口。

```markdown
## 🚪 退出 Debug 模式

是否需要移除已添加的调试埋点代码？
- 回复 `yes` - 移除所有埋点代码
- 回复 `no` - 保留埋点代码（稍后可继续调试）
```

## 禁止项清单

| 禁止项 | 说明 |
|-------|------|
| 无证据修复 | 必须先有运行时日志证据 |
| setTimeout 作为修复 | 用正确的事件/生命周期/await |
| 记录敏感信息 | 不记录 token、密码、API key、PII |
| 验证前移除埋点 | 埋点必须保留到用户回复 `fixed` |
| 猜测性防御代码 | 被否定的假设必须回滚相关代码 |
| 过度工程 | 优先复用现有架构，最小化修复 |

## 常见问题处理

**日志文件为空**：
- 检查日志服务器是否在运行
- 检查代码是否正确触发了埋点路径
- 请求用户确认复现步骤是否正确

**假设全部 INCONCLUSIVE**：
- 埋点位置可能不在执行路径上
- 需要添加更多上游埋点
- 考虑是否是间歇性问题

**修复后出现新问题**：
- 可能修复引入了回归
- 添加针对新问题的假设
- 继续调试流程
