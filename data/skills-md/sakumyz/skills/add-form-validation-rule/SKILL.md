---
name: add-form-validation-rule
description: 为 Vue 3 + Ant Design Vue 表单系统新增自定义校验规则。支持正则校验、值范围校验、日期校验等。包含类型定义、校验实现、单元测试的完整流程。
---

# 新增表单校验规则

本 skill 提供一套标准的工作流程，用于为项目的表单验证系统添加新的校验规则。

## 概述

项目采用 **Ant Design Vue 4.x** + **自定义规则引擎** 的表单验证方案：

- **类型定义**：`src/components/atoms/AtmForm/index.ts` 中的 `BuiltInRules` 接口
- **规则实现**：`src/hooks/useForm/getAntDFormRules.ts` 中的规则转换逻辑
- **验证函数**：`src/utils/validation/` 目录下的具体验证实现
- **单元测试**：`src/hooks/useForm/getAntDFormRules.spec.ts` 中的测试用例

## 核心流程

### 1. 添加类型定义

**位置**：`src/components/atoms/AtmForm/index.ts`

在 `BuiltInRules` 接口中添加新的规则属性：

```typescript
export interface BuiltInRules {
  // 示例：添加新规则
  myNewRule?: string | number | boolean | RegExp
}
```

**规则类型指南**：

- **简单布尔规则**（无参数）：`boolean` — 如 `email?: boolean`
- **带参数的规则**：根据参数类型 — 如 `dateFormat?: string`、`maxValue?: number`
- **多参数规则**：`string`（JSON格式）— 如 `range?: '[1,10]'`
- **正则表达式**：`RegExp` 类型
- **数组参数**：`string[] | string` — 如 `fileExtension?: string | string[]`

### 2. 实现规则逻辑

**位置**：`src/hooks/useForm/getAntDFormRules.ts`

#### 简单规则（simpleRules）- 正则/直接模式

用于无需参数的规则，在 `simpleRules` 对象中添加：

```typescript
const simpleRules: Record<string, Rule> = {
  mySimpleRule: {
    pattern: /your-regex-pattern/,
    message: '错误提示文案',
    trigger: 'blur'
  }
}
```

#### 复杂规则（getValidationRule）- 自定义验证器

在 `getValidationRule` 函数返回的规则对象中添加：

```typescript
myComplexRule: {
  validator: (_, value) => {
    // 验证逻辑
    return validationHelper(validateResult, errorMessage);
  },
  trigger: rule?.trigger || 'blur',
  transform: rule?.transform
}
```

**验证函数调用**：优先使用已有验证函数（如 `validateDateFormat`、`validateNumberRange`），减少新增文件。

### 2.1 更新 isBuiltInRule 函数

**位置**：`src/hooks/useForm/getAntDFormRules.ts` 中的 `isBuiltInRule` 函数

在添加新规则属性到 `BuiltInRules` 接口后，**必须**在 `isBuiltInRule` 函数中的 `ruleKeys` 数组里添加对应的属性名：

```typescript
function isBuiltInRule(value: any): value is RuleOptions {
  if (!isObject(value)) return false

  const ruleKeys = [
    'required',
    'pattern',
    // ... 其他现有属性 ...
    'myNewRule' // ← 添加新属性名
  ]

  // ... 后续逻辑保持不变 ...
}
```

> ⚠️ **这一步容易遗漏！** 如果不更新 `ruleKeys`，新规则将被错误地识别为无效对象，导致规则处理失败。

### 3. 添加或重用验证函数

**位置**：`src/utils/validation/` 目录

**决策树**：

1. 如果是**正则模式**（简单规则），直接在 `simpleRules` 中定义，**不需要**创建验证函数
2. 如果需要**复杂验证逻辑**：
   - ✅ **优先选择**：现有的 `.ts` 文件（`date.ts`、`number.ts`、`string.ts`、`file.ts`）
   - ❌ **最后选择**：创建新的验证文件，仅当逻辑完全不相关时

**验证函数特征**：

- 输入参数是值和规则配置
- 返回 `boolean` 或 `{ valid: boolean; message?: string }`
- 处理 `null`、`undefined` 等边界情况

### 4. 编写单元测试

**位置**：`src/hooks/useForm/getAntDFormRules.spec.ts`

**测试模板**：

```typescript
it('myNewRule 规则正确转换', () => {
  const rules: FormRules = {
    field: {
      myNewRule: true // 或对应的参数值
    }
  }

  const result = getAntDFormRules(rules)
  const fieldRules = result!.field as Rule[]

  expect(fieldRules).toContainEqual({
    pattern: expect.any(RegExp), // 或 validator: expect.any(Function)
    message: expect.any(String),
    trigger: 'blur'
  })
})

// 对于带参数的规则，添加验证器功能测试
it('myNewRule 验证器正确工作', async () => {
  const rules: FormRules = {
    field: {
      myNewRule: 'paramValue'
    }
  }

  const result = getAntDFormRules(rules)
  const fieldRules = result!.field as Rule[]
  const myRule = fieldRules.find(rule => rule.validator)

  // 成功情况
  await expect(myRule!.validator!({}, 'validValue', () => {})).resolves.toBeUndefined()

  // 失败情况
  await expect(myRule!.validator!({}, 'invalidValue', () => {})).rejects.toThrow('错误提示文案')
})
```

### 5. 执行测试

```bash
# 运行指定测试文件
npm test -- getAntDFormRules.spec.ts --run

# 运行所有表单相关测试
npm test -- useForm --run

# 查看测试覆盖率
npm test -- --coverage --run
```

## 代码示例

### 示例 1：简单的正则校验规则

添加一个**汉字验证**规则：

**1. 类型定义** (`AtmForm/index.ts`)：

```typescript
export interface BuiltInRules {
  chineseCharacters?: boolean
}
```

**2. 规则实现** (`getAntDFormRules.ts`)：

```typescript
const simpleRules: Record<string, Rule> = {
  chineseCharacters: {
    pattern: /^[\u4e00-\u9fff]+$/,
    message: '仅支持汉字输入',
    trigger: 'blur'
  }
}
```

**3. 单元测试** (`getAntDFormRules.spec.ts`)：

```typescript
it('chineseCharacters 规则正确转换', () => {
  const rules: FormRules = {
    name: { chineseCharacters: true }
  }
  const result = getAntDFormRules(rules)
  expect(result!.name).toContainEqual({
    pattern: expect.any(RegExp),
    message: '仅支持汉字输入',
    trigger: 'blur'
  })
})
```

### 示例 2：带参数的自定义验证规则

添加一个**字符串长度百分比**验证规则（例如，验证实际输入不超过最大长度的80%）：

**1. 类型定义** (`AtmForm/index.ts`)：

```typescript
export interface BuiltInRules {
  percentageLength?: number // 0-100 表示百分比
}
```

**2. 验证函数** (`src/utils/validation/string.ts` - 复用现有文件)：

```typescript
export function validatePercentageLength(value: unknown, percentage: number): boolean {
  if (!value || percentage <= 0 || percentage > 100) return true
  const maxLength = Math.ceil((value as string).length / (percentage / 100))
  return (value as string).length <= maxLength
}
```

**3. 规则实现** (`getAntDFormRules.ts`)：

```typescript
// 在 getValidationRule 函数中添加
percentageLength: {
  validator: (_, value) => {
    if (isNumber(ruleValue)) {
      return validationHelper(
        validatePercentageLength(value, ruleValue),
        `输入长度不能超过最大值的${ruleValue}%`
      );
    }
    return Promise.reject(new Error('percentageLength 规则值必须为数字'));
  },
  trigger: rule?.trigger || 'blur',
  transform: rule?.transform
}
```

**4. 单元测试** (`getAntDFormRules.spec.ts`)：

```typescript
it('percentageLength 验证器正确工作', async () => {
  const rules: FormRules = {
    field: { percentageLength: 80 }
  }
  const result = getAntDFormRules(rules)
  const fieldRules = result!.field as Rule[]
  const rule = fieldRules.find(r => r.validator)

  await expect(rule!.validator!({}, 'test', () => {})).resolves.toBeUndefined()

  await expect(rule!.validator!({}, 'x'.repeat(1000), () => {})).rejects.toThrow()
})
```

## 重要检查清单

- [ ] 已在 `BuiltInRules` 接口中添加新属性（必须）
- [ ] 已在 `isBuiltInRule` 函数的 `ruleKeys` 数组中添加对应属性名（必须）
- [ ] 已在 `getValidationRule` 或 `simpleRules` 中实现规则逻辑（必须）
- [ ] 如有新的验证函数，已添加到相应的 `src/utils/validation/*.ts` 文件（可选）
- [ ] 已编写单元测试用例（必须）
- [ ] 所有测试通过：`npm test -- getAntDFormRules.spec.ts --run`
- [ ] 代码遵循项目的 TypeScript 和 ESLint 规范

## 关键注意事项

1. **isBuiltInRule 函数更新**：这一步已在核心流程的第 2.1 步中详细说明，添加新规则属性后，**必须**在 `getAntDFormRules.ts` 中的 `isBuiltInRule` 函数的 `ruleKeys` 数组中添加新属性名，否则规则将被识别为无效对象。

2. **错误消息本地化**：所有错误消息应使用日语，可通过以下方式获取：
   - 使用 `getMessageByCode()` 调用已有的常数消息
   - 或直接编写日语文本

3. **验证函数复用**：优先复用 `src/utils/validation/` 中已有的函数，减少代码重复和维护成本。

4. **边界情况处理**：验证函数必须正确处理以下情况：
   - `null`、`undefined` → 应返回 `true`（表示通过，因为非必填）
   - 空字符串 `''` → 应返回 `true`（非必填字段）
   - 空数组 `[]` → 应返回 `true`
   - 仅 `required: true` 时才对空值进行拒绝

5. **触发时机**：根据规则类型选择合适的 `trigger`：
   - `'blur'` — 字符格式、文本长度等验证
   - `'change'` — 文件上传、枚举选择等
   - 数组 `['blur', 'change']` — 需要多次触发的验证

## 常用验证函数参考

| 函数                   | 位置                   | 功能                                     |
| ---------------------- | ---------------------- | ---------------------------------------- |
| `validateDateFormat`   | `validation/date.ts`   | 验证日期格式                             |
| `validateDateRange`    | `validation/date.ts`   | 验证日期在某个范围内                     |
| `validateNumberRange`  | `validation/number.ts` | 验证数值范围                             |
| `validateEmail`        | `validation/string.ts` | 验证邮箱格式                             |
| `validateVisualLength` | `validation/string.ts` | 验证可视长度（全角2字符、半角1字符计算） |
| `valideFileExtension`  | `validation/file.ts`   | 验证文件扩展名                           |
