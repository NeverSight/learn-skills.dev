---
name: refactor-check
description: 重构完整性检查技能。验证重构后代码的一致性、完整性和正确性，确保没有遗漏或破坏性变更。触发场景包括"检查重构"、"重构验证"、"代码迁移检查"。
allowed-tools: Grep, Glob, Read, Bash(npm test:*, yarn test:*, npx tsc:*)
---

# 重构检查技能

## 概述

基于 7 次需要多次修复的代码问题分析，本技能提供系统化的重构验证流程，减少迭代修复次数。

## 检查维度

### 1. 导入路径检查
- 相对路径是否更新
- 别名路径是否正确
- 包导入是否更新
- 循环依赖检测

### 2. 类型定义一致性
- Interface 更新是否完整
- Type 别名是否同步
- 泛型参数是否一致
- 导出类型是否完整

### 3. 测试验证
- 单元测试是否通过
- 集成测试是否通过
- 快照是否需要更新
- 覆盖率是否降低

### 4. 遗留代码检测
- 旧命名是否残留
- 废弃函数是否清理
- 无用导入是否存在
- 死代码检测

### 5. 依赖关系
- 依赖是否正确更新
- peerDependencies 是否满足
- 版本冲突是否存在

## 检查流程

```
┌─────────────────────────────────────────────┐
│           重构检查流程                        │
├─────────────────────────────────────────────┤
│  1. 收集变更文件                              │
│     └─ git diff --name-only                 │
│                                             │
│  2. 分析重构范围                              │
│     └─ 识别重命名、移动、删除                   │
│                                             │
│  3. 检查导入路径                              │
│     └─ 扫描所有引用                           │
│                                             │
│  4. 验证类型一致性                            │
│     └─ TypeScript 编译检查                    │
│                                             │
│  5. 运行测试                                  │
│     └─ 单元测试 + 集成测试                     │
│                                             │
│  6. 检测遗留代码                              │
│     └─ 搜索旧命名和废弃代码                     │
│                                             │
│  7. 生成报告                                  │
│     └─ 汇总问题和建议                          │
└─────────────────────────────────────────────┘
```

## 使用方式

### 完整检查
```
/refactor-check
```

### 只检查导入
```
/refactor-check --imports-only
```

### 只运行测试
```
/refactor-check --test-only
```

### 指定目录
```
/refactor-check src/components
```

### 对比分支
```
/refactor-check --base main --head feature/refactor
```

## 检查规则

### 导入路径检查

#### 旧路径搜索
```bash
# 搜索旧的导入路径
grep -r "from 'old-path'" src/
grep -r 'from "old-path"' src/
```

#### 别名检查
```bash
# 检查 tsconfig paths 是否正确
grep -r "@old-alias/" src/
```

### 类型定义检查

#### 运行 TypeScript 编译
```bash
npx tsc --noEmit
```

#### 检查 any 类型
```bash
grep -r ": any" src/ --include="*.ts"
```

### 测试检查

#### 运行测试
```bash
npm test -- --passWithNoTests
yarn test --passWithNoTests
```

#### 更新快照
```bash
npm test -- -u
```

### 遗留代码检测

#### 搜索旧命名
```bash
# 假设 OldComponent 被重构为 NewComponent
grep -r "OldComponent" src/
grep -r "oldComponent" src/
grep -r "old-component" src/
```

## 输出报告

```markdown
## 重构检查报告

**检查时间**: YYYY-MM-DD HH:mm:ss
**检查范围**: [文件/目录]

---

### ✅ 通过检查

- [x] TypeScript 编译通过
- [x] 单元测试通过 (42 passed)
- [x] 无循环依赖

---

### ❌ 发现问题

#### 1. 导入路径未更新
**文件**: `src/utils/helper.ts:3`
**问题**: 引用了旧路径 `@/old-module`

\`\`\`typescript
// 当前
import { foo } from '@/old-module'

// 应改为
import { foo } from '@/new-module'
\`\`\`

**影响范围**: 3 个文件

#### 2. 类型定义不一致
**文件**: `src/types/user.ts`
**问题**: `User` 接口缺少 `role` 字段

\`\`\`diff
interface User {
  id: string
  name: string
+ role: UserRole
}
\`\`\`

#### 3. 遗留代码
**位置**: `src/deprecated/`
**说明**: 发现 2 个废弃文件未删除
- `src/deprecated/oldService.ts`
- `src/deprecated/oldHelper.ts`

---

### 📊 统计

| 检查项 | 状态 | 详情 |
|--------|------|------|
| 导入路径 | ❌ | 3 处未更新 |
| 类型定义 | ❌ | 1 处不一致 |
| 测试 | ✅ | 42/42 通过 |
| 遗留代码 | ❌ | 2 个文件 |
| TypeScript | ✅ | 无错误 |

---

### 建议操作

1. 更新以下导入路径：
   - `src/utils/helper.ts`
   - `src/components/Form.tsx`
   - `src/pages/index.tsx`

2. 补充类型定义：
   - 在 `User` 接口添加 `role` 字段

3. 清理遗留代码：
   - 删除 `src/deprecated/` 目录
```

## 常见重构场景

### 场景 1：组件重命名

```
检查项：
1. 搜索旧组件名（驼峰、短横线）
2. 检查导入语句
3. 更新测试文件
4. 更新文档
5. 检查 CSS 类名
```

### 场景 2：目录结构调整

```
检查项：
1. 更新所有相对导入
2. 更新 tsconfig paths
3. 更新 jest moduleNameMapper
4. 更新 webpack alias
5. 检查动态导入
```

### 场景 3：提取公共模块

```
检查项：
1. 检查循环依赖
2. 验证导出完整性
3. 更新 package.json 依赖
4. 运行所有依赖方测试
```

## 自动修复

### 自动更新导入路径
```bash
# 使用 sed 批量替换（谨慎使用）
find src -name "*.ts" -exec sed -i '' 's/@old-path/@new-path/g' {} \;
```

### 自动删除空文件
```bash
find src -type f -empty -delete
```

## 配置选项

```json
{
  "refactorCheck": {
    "exclude": ["**/*.test.ts", "**/dist/**"],
    "rules": {
      "importCheck": true,
      "typeCheck": true,
      "testRun": true,
      "legacyCode": true
    },
    "autoFix": false
  }
}
```

## 注意事项

1. **大范围重构**：建议分多次小重构，每次都运行检查
2. **测试覆盖**：确保测试覆盖率足够高再进行重构
3. **分支管理**：在独立分支进行重构，便于回滚
4. **渐进式**：优先修复高风险问题，再处理建议项
