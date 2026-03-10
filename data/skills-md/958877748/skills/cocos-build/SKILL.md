---
name: cocos-build
description: Cocos Creator 2.x 项目编译技能 - 自动触发脚本编译并验证效果
---

# cocos-build

用于 Cocos Creator 2.x 项目的开发工作流自动化。

## 前提条件

- Cocos Creator 编辑器必须正在运行（监听 localhost:7456）

## 使用场景

1. 修改或创建 TypeScript/JavaScript 脚本后需要编译
2. 创建新组件后需要生成 .meta 文件
3. 需要验证代码修改在预览中的效果

## 编译指令

修改任何 `assets/` 目录下的脚本文件后，执行以下命令触发编译：

```bash
curl.exe http://localhost:7456/update-db
```

成功返回：`Changes submitted`

## 完整工作流

1. **修改代码** - 编辑 `assets/` 下的 `.ts` 文件
2. **触发编译** - 调用 `curl.exe http://localhost:7456/update-db`
3. **验证效果** - 使用 frontend-tester agent 截图预览页面 `http://localhost:7456/`
4. **确认结果** - 检查 Label、Sprite 等组件显示是否符合预期

## 新建组件

创建新的 TypeScript 组件时：

1. 在 `assets/` 目录下创建 `.ts` 文件
2. 执行编译命令
3. Creator 自动生成对应的 `.meta` 文件（包含 uuid）

## 预览验证

使用 frontend-tester agent 截图验证：

```
task(subagent_type="frontend-tester")
```

预览地址：`http://localhost:7456/`

## 注意事项

- Windows 环境必须使用 `curl.exe` 而非 `curl`（PowerShell 别名问题）
- 编译前确保 Creator 编辑器处于打开状态