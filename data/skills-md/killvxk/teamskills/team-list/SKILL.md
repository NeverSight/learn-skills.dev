---
name: team-list
description: |
  This skill should be used when the user asks to "列出团队", "team list",
  "list teams", "show teams", "查看团队配置", "有哪些团队",
  "what teams are saved". 扫描 .team-profiles/ 目录，
  展示所有已保存配置的摘要信息。与 /team-status（查看运行中团队）不同，
  此技能查看磁盘上的持久化配置。
argument-hint: ""
disable-model-invocation: true
version: 0.1.0
---

# 团队配置列表

扫描当前项目目录的 `.team-profiles/`，展示所有已保存的团队配置摘要。

## 流程

### 步骤 1: 扫描配置目录

使用 Glob 工具匹配 `{当前工作目录}/.team-profiles/*.yaml`。

如果 `.team-profiles/` 目录不存在或没有 `.yaml` 文件：

```
当前项目没有保存的团队配置。

- /team-init  创建新团队（自动保存模板配置）
- /team-save  保存当前运行中的团队（保存快照配置）
```

结束。

### 步骤 2: 读取每个配置文件

对每个 `.yaml` 文件使用 Read 工具读取，提取：

- **文件名**（不含 .yaml 后缀）
- **format**: template 或 snapshot
- **description**: 团队描述
- **team_type_name**: 团队类型中文名（如有）
- **成员数量**:
  - template: 统计 `roles[]` 的 count 总和（每个 role 项有 `role` 代号和 `count` 数量，如 `{role: "developer", count: 2}`）
  - snapshot: 统计 `members[]` 长度
- **任务统计**（仅 snapshot）:
  - completed / in_progress / pending 各多少个

### 步骤 3: 输出列表

```
.team-profiles/ 下共 {N} 个团队配置：

  {name1}  [template]  {team_type_name} - {description 前40字}
    成员: {count} 个角色

  {name2}  [snapshot]  {description 前40字}
    成员: {count} 个  |  任务: {completed}✓ {in_progress}⚡ {pending}○

  {name3}  [snapshot]  {description 前40字}
    成员: {count} 个  |  任务: {completed}✓ {in_progress}⚡ {pending}○

使用 /team-load {name} 加载指定配置。
```

## 注意事项

- 只读取不修改任何文件
- Glob 匹配 `*.yaml` 自动排除 `.yaml.bak` 备份文件，无需额外处理
- 配置文件解析失败时跳过并提示（如 "⚠ {name}.yaml 格式异常，已跳过"）
- 按文件名字母序排列
