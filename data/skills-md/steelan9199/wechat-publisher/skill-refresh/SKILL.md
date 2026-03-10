---
name: skill-refresh
description: 刷新技能。当用户需要刷新技能时使用此技能
---

# 刷新技能

使用自动化脚本批量刷新所有技能。

## 快速使用

直接执行 skill-refresh 目录下的脚本：

```bash
node skill-refresh/refresh-all-skills.js
```

## 脚本功能

- **自动扫描多个技能源目录中的所有技能**
- 批量安装所有技能
- 显示每个目录的处理进度和总计统计结果
- **安装完成后显示失败技能列表（包含绝对路径）**
- 自动跳过不存在的目录

### 输出示例

```
=== 所有目录处理完成 ===
总计: 20 个技能
成功: 15 个
失败: 5 个

=== 安装失败的技能 ===

1. douyin-video
   路径: D:/script/work-sop/49-1-我使用的skills/skills/douyin-video
2. excalidraw-diagram-generator
   路径: D:/script/work-sop/49-1-我使用的skills/skills/excalidraw-diagram-generator
...
```

## 配置说明

脚本内置了默认的技能源目录配置。如需修改，请编辑 `refresh-all-skills.js` 文件中的 `skillSourceDirs` 数组：

```javascript
// 配置：技能源目录列表
const skillSourceDirs = [
  "D:/software/skills/skills",
  "D:/script/work-sop/49-1-我使用的skills/skills"
];
```

按需要添加、删除或修改路径即可。
