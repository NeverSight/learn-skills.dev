---
name: skill-manager
description: skill查询与管理。列出所有可用skill清单，搜索及查看skill详细用法。
---

# skill管理器 (Skill Manager)

## 核心能力

此skill用于帮助用户了解和管理当前环境中可用的所有 AI skill。

## 使用场景

- 用户询问：“我有哪些可用的skill？”
- 用户询问：“列出所有skill。”
- 用户想查找具有特定功能的skill（如“有没有处理图片的skill？”）。
- 用户想查看某个skill的具体文档或用法。

## 执行逻辑

### 1. 列出所有skill

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Script path = `${SKILL_DIR}/scripts/<script-name>.ts`
3. Replace all `${SKILL_DIR}` in this document with the actual path

**仅**执行以下单条命令。禁止在执行前运行 `ls` 或进行其他环境检查：

```bash
npx -y bun ${SKILL_DIR}/scripts/list-skills.ts
```

### 2. 搜索skill

当用户模糊查询时（如“找一个处理PDF的skill”），可以配合 `grep` 搜索：

```bash
grep -r "PDF" "${SKILL_DIR}/../*/SKILL.md" | cut -d: -f1 | sort | uniq
```

### 3. 查看特定skill

当用户请求查看具体skill时，直接使用 `read_file` 读取对应目录下的 `SKILL.md`。

### 4. 修复缺失描述的 skill

当列表显示某个 skill 为 `❌ 缺失描述` 时，应主动提示修复：
1. 使用 `read_file` 读取该 skill 的 `SKILL.md`（注意跳过已有的或错误的 YAML 区域）。
2. 根据文件内容提取或总结其核心功能，生成包含 `name` 和 `description` 的 YAML Front Matter：
   ```yaml
   ---
   name: skill-folder-name
   description: 简短描述（100字以内，包含主要功能和触发词）
   ---
   ```
3. 将生成的 YAML 插入到文件最顶部。

## 注意事项

- skill名称即目录名称。
- 描述信息来源于 `SKILL.md` 顶部的 YAML Front Matter 中的 `description` 字段。
