---
name: team-delete
description: |
  This skill should be used when the user asks to "删除团队配置", "team delete",
  "移除团队", "清理团队配置". 从 .team-profiles/ 目录中删除指定的
  YAML 配置文件。
argument-hint: "[配置名称]"
disable-model-invocation: true
version: 0.1.0
---

# 团队配置删除

从项目目录的 `.team-profiles/` 中删除指定的团队配置文件。

## 流程

### 步骤 1: 定位配置文件

- 如果 `$ARGUMENTS` 非空，直接使用作为配置名称
- 如果 `$ARGUMENTS` 为空，扫描 `.team-profiles/*.yaml`，列出供用户选择

```
AskUserQuestion:
  question: "选择要删除的团队配置"
  header: "删除配置"
  options:
    - label: "{name1}"
      description: "[{format}] {description 前30字}"
    - label: "{name2}"
      description: "[{format}] {description 前30字}"
    # ... 最多 4 个
  multiSelect: false
```

如果 `.team-profiles/` 目录不存在或为空：
```
没有可删除的团队配置。
```
结束。

### 步骤 2: 展示配置信息并确认

使用 Read 工具读取目标文件，展示摘要：

```
即将删除: .team-profiles/{name}.yaml
--------------------
格式: {format}
描述: {description}
成员: {N} 个
任务: {M} 个（仅 snapshot）
备份文件: {如果 .yaml.bak 存在则显示 "将同时删除 .yaml.bak"，否则 "无"}
--------------------
```

```
AskUserQuestion:
  question: "确认删除此配置？此操作不可恢复。"
  header: "确认删除"
  options:
    - label: "确认删除"
      description: "永久删除此配置文件"
    - label: "取消"
      description: "放弃删除"
  multiSelect: false
```

### 步骤 3: 删除文件

使用 Bash 工具执行删除：

```bash
rm "{当前工作目录}/.team-profiles/{name}.yaml"
```

如果对应的备份文件 `.team-profiles/{name}.yaml.bak` 也存在，一并删除：

```bash
rm "{当前工作目录}/.team-profiles/{name}.yaml.bak"
```

### 步骤 4: 输出结果

```
已删除: .team-profiles/{name}.yaml
```

如果同时删除了备份文件，额外提示：
```
同时清理了备份文件: .team-profiles/{name}.yaml.bak
```

如果删除后 `.team-profiles/` 目录为空，额外提示：
```
.team-profiles/ 目录已无配置文件。
```
