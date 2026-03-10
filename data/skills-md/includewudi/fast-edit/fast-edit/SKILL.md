---
name: fast-edit
description: 大文件编辑、批量修改、剪贴板/stdin粘贴、多文件写入、编辑验证/回滚。用于替代慢速的 Edit/Write 工具。（重构测试版）
---

# Fast Edit

行号定位的文件编辑工具。绕过 LSP 等待、权限弹窗、历史数据库。**自动备份 + 验证/回滚**，编辑出错可一键恢复。

> **按需加载子文档**：本文档包含核心决策树和安全守则。详细用法见 `skills/` 子文档，仅在需要时加载。

---

## 我需要做什么？（决策树）

```
任务类型
  │
  ├─ 编辑已有文件
  │    ├─ 单处小改 → replace（先 show 确认行号！见 §安全守则1）
  │    ├─ 多处编辑 / 含特殊字符 → batch --stdin（见 §安全守则4）
  │    ├─ Python 符号级编辑 → outline + apply（见 skills/outline-apply.md）
  │    └─ 编辑后 → verify + lsp_diagnostics（见 §验证三连）
  │
  ├─ 保存用户粘贴的代码
  │    ├─ 首选: save-pasted（零 token，见 §安全守则2）
  │    ├─ 降级: paste --stdin（save-pasted 失败时）
  │    └─ 特殊字符多: paste --stdin --base64
  │
  ├─ 从零创建新文件
  │    ├─ ≤150 行 → heredoc / Write
  │    ├─ >200 行 + 有规律 → fast-generate --stdin（见 skills/large-file.md）
  │    ├─ >200 行 + 无规律 → 分段 heredoc（见 skills/large-file.md）
  │    └─ 必须先评估行数！（见 §安全守则3）
  │
  ├─ 编辑出错，需要恢复
  │    ├─ 刚编辑的文件 → restore（一键回滚）
  │    └─ 之前 session 写的大文件 → recover（见 skills/recover.md）
  │
  └─ 多语言编辑（Go/PHP/TS/JSX/Vue/Java）
       → 检查 §安全守则4 的危险字符触发器
       → 详细矩阵见 skills/shell-safety.md
```

---

## ⚠️ 安全守则（内联，必读）

### 守则 1: replace 前必须确认行号

> **绝对不要凭记忆 replace。** 行号会因为之前的编辑而偏移，AI 数行号容易 off-by-one。

```
replace/delete 操作
  │
  ├─ 第1步: fe show FILE START END
  │    确认首行和末行内容是否匹配你要替换的目标
  │    ⚠️ 重点检查 END 行 — off-by-one 最常发生在末行
  │
  ├─ 第2步: 确认行号正确后，再执行 replace
  │    fe replace FILE START END "content\n"
  │
  └─ 第3步: 检查返回的 warnings 字段
       如果有 warnings，立即检查并修复
```

**常见 off-by-one 错误模式：**

| 错误 | 后果 | 预防 |
|------|------|------|
| END 少了1行 | 目标的最后一行残留，与新内容重复 | show 确认 END 行内容 |
| END 多了1行 | 多删了下一行代码 | show 确认 END+1 行不是你要保留的 |
| START 偏移 | 替换了错误的起始位置 | show 确认 START 行内容 |

**反面案例：**
```bash
# ❌ 错误：凭记忆 replace，END 少1行
fe replace file.dart 74 78 "new widget code\n"
# 结果：第79行残留了旧代码，与新代码重复 → 编译错误

# ✅ 正确：先 show 确认
fe show file.dart 74 80    # 看清楚79行是什么
fe replace file.dart 74 79 "new widget code\n"  # 确认后再替换
```

### 守则 2: save-pasted 优先级

> 用户粘贴代码需要保存时，**始终优先尝试 `save-pasted`**。
> 零 token 输出、零 shell 转义问题。仅当不可用时才降级。

```
用户粘贴了代码，要求保存到文件
  │
  ├─ 首选: save-pasted FILE [--extract]
  │    零 token、零转义、自动从本地存储提取
  │    150+ 行时强烈推荐（echo/heredoc 可能截断）
  │
  ├─ 降级: paste FILE --stdin (< 150 行、save-pasted 失败时)
  │    echo '内容' | fe paste FILE --stdin
  │
  └─ 特殊字符多: paste FILE --stdin --base64
       含 $、反引号、引号嵌套时用 base64 编码
```

### 守则 3: 大文件生成的 AI 能力上限（硬性限制）

> **你的 token 输出上限约 100-150 行。fast-generate 不会改变这个事实。**
> fast-generate 的代码本身也是你的 token 输出。如果 generate 代码超过 80 行，你很可能写不完。

```
AI 需要创建新文件
  │
  ├─ ≤100 行 → 直接 heredoc / Write（安全区）
  │
  ├─ 100-150 行 → 尝试单次输出，截断则分段
  │
  ├─ >150 行 + 内容有规律（配置/数据/批量）
  │    → fast-generate --stdin
  │    ⚠️ generate 代码必须 ≤80 行！超过则拆分任务
  │    ⚠️ 仅适用于有循环/规律的内容，不是万能压缩器
  │
  └─ >150 行 + 内容无规律（自由文本/文章）
       → 分段 heredoc（每段 ≤120 行）+ cat 合并
```

**强制检查清单：**
- [ ] generate 代码是否 ≤80 行？（超过 = 你写不完，必须拆分）
- [ ] 内容是否真的有规律？（无规律 = 不要用 generate，用分段 heredoc）
- [ ] 是否评估了总行数？（不确定 = 按 >150 行处理）

详细用法见 `skills/large-file.md`。

### 守则 4: 危险字符触发器

代码包含以下**任一字符**时 → **必须** `batch --stdin`，禁止 CLI `replace`：

| 触发字符 | 影响语言 | 风险 |
|----------|----------|------|
| `\n` `\t` 字面量 | Go, Java, TS, JSX | shell 展开为真换行/Tab |
| `$variable` | PHP, Bash | shell 变量展开 |
| 反引号 `` ` `` | Go, TS/JSX/Vue | shell 命令执行 |
| 模板字面量 `` `${var}` `` | TS, JSX, Vue | `$` + `` ` `` 双重危险 |
| `<tag>` / `>` | JSX, Vue, Java 泛型 | shell 重定向 |
| `\` 命名空间 | PHP | 需四重转义 |
| `"""` 三引号 | Python | 引号嵌套 |
| `A \| B` 联合类型 | TypeScript | shell pipe |

**安全管道模式（必须用 heredoc，禁止 `python -c`）：**
```bash
# ✅ 正确：heredoc 避免反引号被 shell 执行
python3 - <<'PY' | fe fast-batch --stdin
import json, sys
spec = {'file': 'f.go', 'edits': [{'action': 'replace-lines', 'start': 10, 'end': 12, 'content': 'code\n'}]}
json.dump(spec, sys.stdout)
PY

# ❌ 禁止：python -c "...`...`..." — shell 会先执行反引号内容
# python3 -c "json.dump({'content': '`date`'}, sys.stdout)"  ← 反引号被执行！
```

详细语言矩阵见 `skills/shell-safety.md`。

### 守则 5: action ≠ type

> ⚠️ Batch JSON 的字段名是 **`"action"`** 不是 `"type"`！
> 写成 `"type": "replace"` 会**报错 `'action'`（KeyError）**，不会静默忽略。

正确写法：
- `"action": "replace-lines"` / `"action": "insert-after"` / `"action": "delete-lines"`

---

## 命令速查

```bash
# ✅ 优先用 fe() 函数封装（❌ 不要用变量赋值，zsh 下会 command not found）
fe() { python3 "/path/to/fast-edit/fast_edit.py" "$@"; }

# 所有命令支持 fast-* 前缀避免 shell 内置命令冲突
# 如: fast-write, fast-paste, fast-batch, fast-verify

# ── 结构化编辑 (Python AST) ──
fe outline FILE.py                     # 查看文件符号结构 (JSON)
fe outline FILE.py --format tree       # 查看文件符号结构 (树形)
fe apply spec.json --dry-run           # 预览符号级编辑
fe apply spec.json --apply             # 执行符号级编辑
echo '{...}' | fe apply --stdin --dry-run   # stdin 输入 (预览)
echo '{...}' | fe apply --stdin --apply     # stdin 输入 (执行)

# ── 编辑命令 ──
fe show FILE START END                # 预览行
fe replace FILE START END "content\n" # 替换行
fe insert FILE LINE "content\n"       # 插入（LINE=0 表示开头）
fe delete FILE START END              # 删除行

# ── 批量编辑 (JSON) ──
fe fast-batch spec.json
echo '{"file":"a.py","edits":[...]}' | fe fast-batch --stdin

# ── 粘贴保存 ──
fe fast-paste FILE                    # 从剪贴板
fe fast-paste FILE --stdin            # 从 stdin
fe fast-paste FILE --stdin --extract  # 提取 ```...``` 代码块
fe fast-paste FILE --stdin --base64   # stdin 内容是 base64 编码

# ── 批量写文件 ──
fe fast-write spec.json
echo '{"files":[...]}' | fe fast-write --stdin
# ⚠️ --stdin 管道传 JSON 时，echo 中的 \n 会被 shell 解释为真换行，导致 JSON 无效
# 推荐用 heredoc << 'EOF' 构造 JSON（禁止 python3 -c，反引号会被 shell 执行）

# ── 代码生成写文件（推荐用于批量生成 200+ 行） ──
echo 'python_code' | fe fast-generate --stdin -o output.json   # 单文件
echo 'python_code' | fe fast-generate --stdin                   # 多文件(stdout=JSON)
fe fast-generate script.py -o output.json                       # 脚本文件模式
fe fast-generate script.py -o out.json --timeout 60             # 自定义超时
fe fast-generate --stdin -o out.json --no-validate              # 跳过 JSON 验证

# ── 验证/回滚 ──
fe verify FILE                        # 对比当前文件与备份的差异
fe verify FILE --context 3            # 显示更多上下文行
fe restore FILE                       # 回滚到最近备份
fe backups FILE                       # 列出所有备份
fe verify-syntax FILE                 # 语言感知语法检查

# ── 其他 ──
fe check FILE                         # Python 类型检查
fe check FILE --checker mypy
fe save-pasted FILE                   # 自动找最近的大粘贴 (>=20行)
fe save-pasted FILE --min-lines 50    # 自定义行数阈值
fe save-pasted FILE --msg-id msg_xxx  # 指定消息 ID
fe save-pasted FILE --extract         # 提取 ```...``` 代码块
fe save-pasted FILE --nth 2           # 第2个最近的大粘贴
fe recover FILE --list               # [OpenCode 专属] 列出最近对 FILE 的所有写操作
fe recover FILE                       # [OpenCode 专属] 恢复最近一次写操作的内容
fe recover FILE --nth 3              # [OpenCode 专属] 恢复第3次最近的写操作
fe recover FILE --session ses_xxx    # 从指定 session 恢复
fe recover FILE -o /tmp/out.py       # 输出到指定文件
fe help
```

---

## 使用场景表

| 场景 | 命令 |
|------|------|
| 大文件 (100+ 行) 小改动 | `replace` / `batch` |
| 同文件多处编辑 | `batch` |
| **用户粘贴代码，保存文件（首选）** | **`save-pasted`** |
| 用户粘贴代码，save-pasted 不可用时 | `paste --stdin` |
| 用户粘贴含特殊字符的代码 | `paste --stdin --base64` |
| 用户粘贴多份代码，保存多文件 | `write --stdin` |
| 从剪贴板保存 | `paste` |
| 编辑后检查是否改对了 | `verify` |
| 编辑改坏了，一键回滚 | `restore` |
| 编辑后语法检查（多语言） | `verify-syntax` |
| 编辑后类型检查 | `lsp_diagnostics` (推荐) 或 `check` |
| AI 从零生成大文件/批量文件 (200+行) | **`fast-generate --stdin`**（仅限有规律内容，generate 代码 ≤80 行） |
| AI 从零生成大文件 (备选, 无 Python) | 分段 heredoc → `cat` 合并 → `paste --stdin` |
| AI 写了大文件但有小错，想恢复重编辑 | **`recover`** [OpenCode 专属] |
| Python 文件查看符号结构 | `outline` / `outline --format tree` |
| Python 符号级替换/删除/插入 | `apply` (spec.json \| --stdin) |

---

## Batch JSON 格式

```json
{
  "file": "/path/to/file.py",
  "edits": [
    {"action": "replace-lines", "start": 10, "end": 12, "content": "new\n"},
    {"action": "insert-after", "line": 25, "content": "# comment\n"},
    {"action": "delete-lines", "start": 40, "end": 42}
  ]
}
```

多文件: `{"files": [{"file": "a.py", "edits": [...]}, ...]}`

---

## replace/batch 自动 warnings

| Warning | 含义 | 常见原因 |
|---------|------|----------|
| `DUPLICATE_LINE` | 替换内容的最后一行与紧邻的下一行完全相同 | END 行号少了1（off-by-one），旧代码残留 |
| `BRACKET_BALANCE` | 替换前后 `(){}[]` 括号平衡发生变化 | 替换内容缺少闭合括号，或多包含了开括号 |

**收到 warnings 后必须：**
1. `DUPLICATE_LINE` → 检查是否 END 需要 +1，用 `show` 确认后重新 `replace`
2. `BRACKET_BALANCE` → 检查替换内容的括号是否完整闭合
3. 如果是误报（故意的不平衡替换）→ 忽略即可

---

## 验证三连（每次编辑后）

```bash
fe verify FILE              # 1. 对比差异
lsp_diagnostics(file)       # 2. 类型检查（首选）
fe verify-syntax FILE       # 3. 语法检查（备选，参考信号）
```

回滚: `fe restore FILE`（回滚前自动保存当前状态）

---

## 何时打开子文档

| 子文档 | 打开时机 |
|--------|----------|
| `skills/shell-safety.md` | 编辑 Go/PHP/TS/JSX/Vue/Java 代码时 |
| `skills/large-file.md` | 需要创建 >200 行新文件时 |
| `skills/workflows.md` | 需要完整工作流示例（粘贴、生成、验证）时 |
| `skills/recover.md` | 需要从 OpenCode session 恢复文件时 |
| `skills/formats.md` | 需要查看命令返回 JSON 格式时 |
| `skills/outline-apply.md` | 需要 Python 符号级编辑时 |
| `skills/api.md` | 需要查看命令详细参数和选项时 |
| `skills/configuration.md` | 需要配置路径、平台相关设置时 |
| `skills/development.md` | 需要开发/贡献 fast-edit 本身时 |

---

## 文件结构

```
fast-edit/
├── fast_edit.py   # CLI 入口
├── core.py        # 文件 I/O
├── edit.py        # 编辑操作（自动备份）
├── paste.py       # 粘贴/写入
├── pasted.py      # OpenCode 存储提取
├── generate.py    # 代码生成写文件（fast-generate）
├── recover.py     # OpenCode Session 存储恢复（recover, OpenCode 专属）
├── outline.py     # Python AST 符号提取（outline）
├── apply.py       # 符号定位编辑（apply）
├── check.py       # Python 类型检查
├── verify.py      # 验证/备份/回滚/语法检查
└── skill.md       # 本文档
```

## 性能对比

| 场景 | Edit 工具 | fast-edit |
|------|-----------|-----------|
| 500行文件 3处编辑 | ~15s (3次调用) | **<0.1s** (batch) |
| AI Token 输出 | old+new 字符串 | **仅行号+内容** |
| LSP 等待 | 每次 0-5s | **0** |

## 编辑后验证

**推荐**：编辑完成后调用 `lsp_diagnostics` 检查类型错误：

```
lsp_diagnostics(filePath="/path/to/edited_file.py")
```

**备选**：如果 LSP 不可用：

| 方式 | 优点 | 缺点 |
|------|------|------|
| `lsp_diagnostics` | 快（LSP 热启动）、支持所有语言 | 需要 LSP 服务运行 |
| `fe verify-syntax` | 多语言语法检查（Go/Py/Rust/C/TS/Java） | 仅检查语法，不检查类型 |
| `fe verify` | 查看编辑前后差异，确认改对了 | 需要先有备份 |
| `fe check` | Python 类型检查 | 仅支持 Python |
