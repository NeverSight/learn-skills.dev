---
name: test-generator
description: 前端测试用例生成器。根据组件或函数签名自动生成基础测试用例，支持 Jest/Vitest + React Testing Library / Vue Test Utils。适用于：(1) 为现有组件补充测试，(2) 为新组件生成测试骨架，(3) 为工具函数生成单元测试。
---

# 测试用例生成器

为组件和函数自动生成测试用例骨架。

## 工作流程

### 1. 环境探测

1. 读取 `package.json` 确认测试框架（Jest / Vitest）
2. 检查测试配置文件（`jest.config.*` / `vitest.config.*`）
3. 扫描现有测试文件了解命名和组织规范
4. 确认测试工具库（React Testing Library / Vue Test Utils / Enzyme）

### 2. 分析目标代码

读取目标文件，提取：
- 导出的函数/组件名
- Props/参数类型定义
- 内部状态和副作用
- 事件处理函数
- 依赖的外部模块（用于 mock）

### 3. 生成策略

#### 工具函数测试

```typescript
describe('functionName', () => {
  // 正常情况
  it('应该 [预期行为] 当 [正常输入]', () => {})

  // 边界情况
  it('应该 [预期行为] 当输入为空', () => {})
  it('应该 [预期行为] 当输入为 null/undefined', () => {})

  // 异常情况
  it('应该 [抛出错误/返回默认值] 当 [异常输入]', () => {})
})
```

#### React 组件测试

```typescript
describe('ComponentName', () => {
  // 渲染测试
  it('应该正常渲染', () => {})
  it('应该渲染所有必需的 UI 元素', () => {})

  // Props 测试
  it('应该正确显示 [prop] 内容', () => {})
  it('应该使用默认值当 [prop] 未传入', () => {})

  // 交互测试
  it('应该在点击 [按钮] 后 [预期行为]', () => {})
  it('应该在输入变化后 [预期行为]', () => {})

  // 异步测试
  it('应该在加载完成后显示数据', async () => {})
  it('应该在请求失败时显示错误信息', async () => {})
})
```

#### Vue 3 组件测试

```typescript
describe('ComponentName', () => {
  // 渲染测试
  it('应该正常渲染', () => {
    const wrapper = mount(ComponentName, { props: {} })
    expect(wrapper.exists()).toBe(true)
  })

  // Props 测试
  it('应该响应 props 变化', async () => {
    const wrapper = mount(ComponentName, { props: { value: 'initial' } })
    await wrapper.setProps({ value: 'updated' })
    expect(wrapper.text()).toContain('updated')
  })

  // 事件测试
  it('应该触发 [事件名] 事件', async () => {
    const wrapper = mount(ComponentName)
    await wrapper.find('button').trigger('click')
    expect(wrapper.emitted('eventName')).toBeTruthy()
  })
})
```

### 4. 测试文件放置

遵循项目现有模式：
- `__tests__/` 目录：`src/__tests__/ComponentName.test.tsx`
- 同级目录：`src/components/ComponentName.test.tsx`
- spec 后缀：`src/components/ComponentName.spec.tsx`

### 5. Mock 策略

- API 请求：mock HTTP 客户端或使用 MSW
- 路由：mock router（useNavigate / useRouter）
- 状态管理：提供 mock store/provider
- 定时器：使用 `vi.useFakeTimers()` / `jest.useFakeTimers()`

## 重要原则

- **生成骨架，不猜测业务逻辑**：测试体内用 TODO 标记需要补充的断言
- **覆盖基础场景**：渲染、Props、交互、边界值
- **遵循 AAA 模式**：Arrange → Act → Assert
- **测试行为而非实现**：不测试内部 state，测试 UI 输出
