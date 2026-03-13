---
name: pcp-setup
description: 一键安装 PCP（Progress Control Plane）OpenCode 插件和 skills。运行后重启 OpenCode 即可使用完整的任务队列/backlog 管理系统。
license: MIT
compatibility: opencode
---

## 目的

将 PCP 所有组件下载并安装到正确位置：
- `pcp.ts` 插件 → `~/.config/opencode/plugins/`
- `pcp-intake` skill → `~/.config/opencode/skills/pcp-intake/`
- `pcp-sprint-review` skill → `~/.config/opencode/skills/pcp-sprint-review/`
- `pcp-setup` skill → `~/.config/opencode/skills/pcp-setup/`

> **无需单独配置 agent。** PCP 行为规则通过插件的 `system.transform` hook 自动注入所有 agent，无需手动切换。

---

## 前置条件

- macOS / Linux（Windows 需手动下载）
- OpenCode 已安装
- `curl` 可用

---

## 执行步骤

### Step 1：创建目录

运行以下命令：

```bash
mkdir -p ~/.config/opencode/plugins \
         ~/.config/opencode/skills/pcp-intake \
         ~/.config/opencode/skills/pcp-sprint-review \
         ~/.config/opencode/skills/pcp-setup
```

### Step 2：下载所有组件

```bash
BASE=https://raw.githubusercontent.com/JohnnyHua/pcp-skills/main

# 插件
curl -fsSL "$BASE/plugin/pcp.ts" \
  -o ~/.config/opencode/plugins/pcp.ts

# Skills
curl -fsSL "$BASE/skills/pcp-intake/SKILL.md" \
  -o ~/.config/opencode/skills/pcp-intake/SKILL.md

curl -fsSL "$BASE/skills/pcp-sprint-review/SKILL.md" \
  -o ~/.config/opencode/skills/pcp-sprint-review/SKILL.md

curl -fsSL "$BASE/skills/pcp-setup/SKILL.md" \
  -o ~/.config/opencode/skills/pcp-setup/SKILL.md
```

### Step 3：验证安装

```bash
echo "=== 插件 ===" && ls ~/.config/opencode/plugins/pcp.ts
echo "=== Skills ===" && ls ~/.config/opencode/skills/
```

期望输出：插件路径存在，skills/ 下有 pcp-intake、pcp-sprint-review、pcp-setup。

### Step 4：重启 OpenCode

关闭并重新打开 OpenCode。插件加载后会在控制台输出 `PCP initialized`。

---

## 安装完成后的使用方式

1. 打开任意项目，首次运行调用 `pcp_init` 建立项目基线
2. 给出 todolist 或计划 → agent 自动解析并调用 `pcp_plan` 加载任务队列
3. 正常写代码——PCP 自动追踪任务，git commit 自动完成并推进到下一个任务
4. 用户说「以后做X」→ agent 自动调用 `pcp_capture` 记录到 backlog
5. 所有任务完成 → PCP 提示做新 plan
6. 新的需求 → 通过 planner 规划 → pcp_plan 加载新任务

> **所有 agent 都自动具备 PCP 能力**，无需切换到特定 agent。

详细工作流见 skill `pcp-sprint-review`。

---

## 卸载

```bash
rm ~/.config/opencode/plugins/pcp.ts
rm -rf ~/.config/opencode/skills/pcp-intake \
        ~/.config/opencode/skills/pcp-sprint-review \
        ~/.config/opencode/skills/pcp-setup
```

---

## 异常处理

| 问题 | 解决 |
|------|------|
| `curl: command not found` | macOS: `brew install curl` |
| 下载失败（404）| 检查 GitHub repo 是否为 public |
| 插件未加载 | 确认文件名为 `pcp.ts`（不是 `pcp.ts.txt`）|
| PCP 规则未注入 | 重启 OpenCode，确认控制台输出 `PCP initialized` |
