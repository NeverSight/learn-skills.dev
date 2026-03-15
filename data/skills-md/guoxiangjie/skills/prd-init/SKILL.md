---
name: "prd-init"
description: "创建标准PRD文档包结构。新项目启动或初始化PRD工作空间时调用。"
---

# PRD 文档包初始化

## 功能说明

此 skill 用于在新项目中快速初始化 PRD 文档包结构。

## 目录结构

```
prd-init/
├── SKILL.md          # 主入口
├── commands/         # 子命令
│   └── init.md       # 初始化命令
├── templates/        # 模板文件
│   ├── README.md     # README模板
│   ├── PRD_INDEX.md  # PRD索引模板
│   └── CHANGELOG.md  # 变更日志模板
├── config/           # 配置文件
│   └── config.json   # 配置信息
└── scripts/          # 辅助脚本
    └── utils.js      # 工具函数
```

## 子命令

### init
- **功能**：初始化 PRD 文档包结构
- **路径**：`commands/init.md`
- **描述**：创建完整的 PRD 文档包目录结构和基础文件

## 配置文件

配置文件位于 `config/config.json`，包含以下内容：
- 技能基本信息
- 模板文件路径
- 子命令配置
- 默认命令设置
- 变量定义

## 模板文件

模板文件位于 `templates/` 目录：
- `README.md` - 项目说明文档模板
- `PRD_INDEX.md` - PRD模块总集索引模板
- `CHANGELOG.md` - 版本变更日志模板

## 辅助脚本

辅助脚本位于 `scripts/` 目录：
- `utils.js` - 工具函数，包含日期处理、文件操作等通用功能

## 工作流程

1. **检测命令**：如果没有指定命令，默认执行 `init` 命令
2. **执行命令**：根据指定的命令执行相应的功能
3. **使用模板**：读取模板文件，替换变量生成最终文档
4. **创建结构**：在指定位置创建 PRD 文档包结构

## 使用方法

1. 调用 `prd-init` skill
2. 按照提示输入目标位置
3. 系统自动创建 PRD 文档包结构
4. 完成后可以使用 `prd-suite` skill 生成具体内容

## 注意事项

- 支持相对路径和绝对路径
- 如果目标位置不存在，会自动创建
- 所有文件使用 UTF-8 编码
- 日期格式为 YYYY-MM-DD
